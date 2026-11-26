#!/usr/bin/env python3
"""
compute_me.py -- per-event matrix elements for the extended MEM (ExtendedMEM.tex, Sec. 2-3)

Input : events.h5 from prepare_events.py
Output: one file per model, aligned event by event with events.h5
        (events<suffix>.h5 -> me_<model><suffix>.h5)

me_Scalar / me_VLF
    born       (N,2)      float64  SM Born |M|^2 [gg, qq] at alpha_s(mu0)   (averaged over spins/colours)
    rho_gg     (Nm,N)     float32  I_gg / Born_gg at y_DM = 1, for each mass of attrs['masses']
    rho_qq     (Nm,N)     float32  I_qq / Born_qq (q qbar, quark from beam 1; symmetric under beam swap)
    flag       (N,)       bool     MadLoop return code not 'stable' even after a re-evaluation
    checks/    scale test (rho at mu_R = mu0/2, 2 mu0), beam-swap test (q qbar)
me_Zprime
    {u,d}_{fw,bw}/K       float32  |M_Z'|^2 = K / D
    {u,d}_{fw,bw}/R, I    float32  2Re(M_EW^* M_Z') = [(s-M^2) R + M Gamma I] / D,  D = (s-M^2)^2 + M^2 Gamma^2
                                    (g_q = g_t = 1; fw = quark from beam 1)

The run is resumable: finished chunks are recorded in each file (done_*), and a restarted
run only computes the missing ones.

Usage
    python3 compute_me.py --events ../data/events_s40.h5 --nproc 15          # test subsample
    nohup python3 compute_me.py --nproc 15 > ../data/compute_me.log 2>&1 &    # full sample
"""
import argparse
import json
import multiprocessing as mp
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import h5py
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mem import config as cfg          # noqa: E402
from mem import io                     # noqa: E402
from mem import mg                     # noqa: E402

N_CHECK = 1000          # events used for the scale / beam-swap / Breit-Wigner checks


def me_path(events_path, model):
    d, b = os.path.split(os.path.abspath(events_path))
    suffix = b[len("events"):] if b.startswith("events") else "_" + b
    return os.path.join(d, f"me_{model}{suffix}")


def open_out(path, N, nchunks, attrs, layout):
    """Open (resume) or create an output file. layout: {name: (shape, dtype, chunks)}."""
    if os.path.exists(path):
        h5 = h5py.File(path, "a")
        same = h5.attrs.get("N") == N and h5.attrs.get("nchunks") == nchunks and \
            all(h5.attrs.get(k) is not None and np.array_equal(np.asarray(h5.attrs[k]), np.asarray(v))
                for k, v in attrs.items() if k in ("masses",))
        if same:
            return h5
        h5.close()
        print(f"[warn] {path} does not match the current events/configuration: recreating", flush=True)
        os.remove(path)
    h5 = h5py.File(path, "w")
    h5.attrs["N"] = N
    h5.attrs["nchunks"] = nchunks
    for k, v in attrs.items():
        h5.attrs[k] = v
    for name, (shape, dtype, chunks) in layout.items():
        if name.startswith("done"):
            h5.create_dataset(name, data=np.zeros(shape, dtype=bool))
        else:
            fill = np.nan if np.issubdtype(np.dtype(dtype), np.floating) else 0
            h5.create_dataset(name, shape, dtype, chunks=chunks, fillvalue=fill, **io.H5_COMP)
    return h5


def run_pool(tasks, nproc, label):
    """Run (fn, kwargs, tag) tasks in fresh processes; yield (tag, result)."""
    if not tasks:
        return
    ctx = mp.get_context("spawn")
    t1 = time.time()
    with ProcessPoolExecutor(max_workers=nproc, mp_context=ctx, max_tasks_per_child=1) as ex:
        futs = {ex.submit(fn, **kw): tag for fn, kw, tag in tasks}
        for i, fu in enumerate(as_completed(futs), 1):
            yield futs[fu], fu.result()
            el = time.time() - t1
            print(f"[{label}] {i}/{len(tasks)} tasks | {el / 60:.1f} min | ETA {el / i * (len(tasks) - i) / 60:.1f} min",
                  flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--events", default=os.path.join(cfg.DATA_DIR, "events.h5"))
    ap.add_argument("--models", default="Scalar,VLF,Zprime")
    ap.add_argument("--chunk", type=int, default=20000)
    ap.add_argument("--nproc", type=int, default=max(1, os.cpu_count() - 1))
    args = ap.parse_args()
    models = [m.strip() for m in args.models.split(",") if m.strip()]

    with h5py.File(args.events, "r") as ev:
        mtt = ev["mtt"][:]
        n = ev["n"][:]
        a0 = ev["alphas0"][:]
        alphas3 = ev["alphas"][:N_CHECK].astype(np.float64)
    N = len(mtt)
    pm = np.sqrt(np.maximum(0.25 * mtt ** 2 - cfg.MT ** 2, 0.0))
    mu0 = np.sqrt(cfg.MT ** 2 + (pm * np.hypot(n[:, 0], n[:, 1])) ** 2)     # exact H_T/2
    chunks = [slice(a, min(a + args.chunk, N)) for a in range(0, N, args.chunk)]
    nc = len(chunks)
    kc = slice(0, min(N_CHECK, N))
    print(f"[start] {N} events, {nc} chunks of {args.chunk}, {args.nproc} workers, models {models}", flush=True)
    t0 = time.time()

    # ---------------------------------------------------------------- one-loop models
    for model in [m for m in models if m in cfg.LOOP_MODELS]:
        masses = cfg.LOOP_MODELS[model]["masses"]
        nm = len(masses)
        path = me_path(args.events, model)
        layout = {"born": ((N, 2), np.float64, (min(N, 1 << 16), 2)),
                  "rho_gg": ((nm, N), np.float32, (1, min(N, 1 << 16))),
                  "rho_qq": ((nm, N), np.float32, (1, min(N, 1 << 16))),
                  "flag": ((N,), np.uint8, (min(N, 1 << 16),)),
                  "done_gg": ((nc,), bool, None), "done_qq": ((nc,), bool, None)}
        h5 = open_out(path, N, nc, dict(model=model, masses=masses, events=os.path.abspath(args.events),
                                        definition="rho_c = I_c/Born_c at y_DM=1 (theta=y_DM^2); "
                                                   "m_DM = M - 100 GeV"), layout)
        tasks = []
        for ch in ("gg", "qq"):
            for ic, s in enumerate(chunks):
                if h5[f"done_{ch}"][ic]:
                    continue
                kw = dict(model=model, ch=ch, mtt=mtt[s], n=n[s], alphas0=a0[s], mu0=mu0[s], masses=masses)
                if ic == 0:
                    kw["check_scales"] = (alphas3[kc, 0], 0.5 * mu0[kc], alphas3[kc, 2], 2.0 * mu0[kc])
                tasks.append((mg.task_loop, kw, (ch, ic)))
        if "checks/swap_qq" not in h5:
            tasks.append((mg.task_loop_swap, dict(model=model, mtt=mtt[kc], n=n[kc], alphas0=a0[kc],
                                                  mu0=mu0[kc], mass=1500.0), ("swap", 0)))
        recheck = float(h5.attrs.get("recheck_max", 0.0))
        for (ch, ic), res in run_pool(tasks, args.nproc, model):
            if ch == "swap":
                d = h5.create_dataset("checks/swap_qq", data=res)
                d.attrs["layout"] = "[orientation fw/bw, (born, rho), event]; mass 1500"
                continue
            s = chunks[ic]
            h5["born"][s, 0 if ch == "gg" else 1] = res["born"]
            h5[f"rho_{ch}"][:, s] = res["rho"]
            h5["flag"][s] = h5["flag"][s] | res["flag"].astype(np.uint8)
            if res["scale_test"] is not None:
                d = h5.require_dataset(f"checks/scale_{ch}", res["scale_test"].shape, np.float64)
                d[...] = res["scale_test"]
                d.attrs["layout"] = f"rho at (mu0/2, 2 mu0), first mass {masses[0]}, events 0..{len(res['scale_test'])}"
            recheck = max(recheck, res["recheck"])
            h5.attrs["recheck_max"] = recheck
            h5[f"done_{ch}"][ic] = True
            h5.flush()
        print(f"[{model}] flagged events: {int(h5['flag'][:].sum())} | max re-evaluation deviation "
              f"{recheck:.1e} | complete: {bool(h5['done_gg'][:].all() and h5['done_qq'][:].all())}", flush=True)
        h5.close()

    # ---------------------------------------------------------------- Z'
    if "Zprime" in models:
        path = me_path(args.events, "Zprime")
        layout = {}
        for q in cfg.ZP_SUBDIRS:
            for o in ("fw", "bw"):
                for f in ("K", "R", "I"):
                    layout[f"{q}_{o}/{f}"] = ((N,), np.float32, (min(N, 1 << 16),))
        for piece in ("A", "B"):
            for q in cfg.ZP_SUBDIRS:
                layout[f"done_{piece}_{q}"] = ((nc,), bool, None)
        h5 = open_out(path, N, nc, dict(model="Zprime", events=os.path.abspath(args.events),
                                        definition="B=|M_Z'|^2=K/D; A=2Re(M_EW^* M_Z')=[(s-M^2)R+M*Gamma*I]/D; "
                                                   "D=(s-M^2)^2+M^2 Gamma^2; g_q=g_t=1 (theta=g_q g_t)"), layout)
        tasks = [(mg.task_zprime, dict(piece=p, q=q, mtt=mtt[s], n=n[s], validate=N_CHECK if ic == 0 else 0),
                  (p, q, ic))
                 for p in ("A", "B") for q in cfg.ZP_SUBDIRS for ic, s in enumerate(chunks)
                 if not h5[f"done_{p}_{q}"][ic]]
        bw_dev = float(h5.attrs.get("bw_dev_max", 0.0))
        for (p, q, ic), res in run_pool(tasks, args.nproc, "Zprime"):
            s = chunks[ic]
            for o, arrs in res["out"].items():
                for f, v in arrs.items():
                    h5[f"{q}_{o}/{f}"][s] = v.astype(np.float32)
            bw_dev = max(bw_dev, res["bw_dev"])
            h5.attrs["bw_dev_max"] = bw_dev
            h5[f"done_{p}_{q}"][ic] = True
            h5.flush()
        print(f"[Zprime] max deviation from the Breit-Wigner form: {bw_dev:.1e}", flush=True)
        h5.close()

    print(f"[done] {(time.time() - t0) / 60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
