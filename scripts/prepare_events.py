#!/usr/bin/env python3
"""
prepare_events.py -- LHE sample -> events.h5 (weights, kinematics, PDF/scale ingredients)

Weights (ExtendedMEM.tex, Sec. 3.2)
    In a biased aMC@NLO fixed-order run the LHE weights have the correct (unbiased) shape
    WITHIN each integration channel, but in each channel they sum to that channel's BIASED
    cross section (res_*.txt). A single kappa therefore mis-weights gg against q qbar
    (by 7.5% for the SM sample). The weights are normalised per channel:
        w_j = kappa_c w_j^LHE,   kappa_c = sigma_c / sum_{j in c, selected} w_j^LHE,   c in {gg, q qbar}
    --norm channel (default): sigma_c from an independent LO integration (mem.validation),
                              whose total is checked against summary.txt;
    --norm total            : one kappa = sigma_gen / sum w^LHE (sigma_gen from summary.txt or
                              --xsec); only correct when the run has a single channel type.
    With --stride/--nmax only a subset is kept and kappa_c is computed on that subset.

Contents of events.h5
    w, w_lhe                (N,)      float64  normalised weight [pb], raw LHE weight
    x1, x2, mtt, ytt        (N,)      float64
    n                       (N,3)     float64  top direction in the t tbar rest frame
    pt, mu0, cost           (N,)      float32  top pT, mu0 = H_T/2, cos(theta*)
    alphas0                 (N,)      float64  alpha_s(mu0)  (used in the ME evaluation)
    alphas                  (N,3)     float32  alpha_s(muR), muR = (0.5, 1, 2) mu0
    flux                    (N,3,G)   float32  signed ordered-pair parton luminosities at
                                               muF = (0.5, 1, 2) mu0, groups = FLUX_GROUPS
    gen_scale               (N,K)     float32  generator <rwgt> weights / nominal weight
PDF replicas are not stored: they follow from (x1, x2, mu0) with mem.io.fluxes.

Usage
    python3 prepare_events.py                                  # SM sample, all events
    python3 prepare_events.py --stride 40 --out ../data/events_s40.h5
    python3 prepare_events.py --run-dir <scalar run> --kin-only --out ../data/scalar_lhe.h5
"""
import argparse
import json
import os
import sys
import time

import h5py
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mem import config as cfg          # noqa: E402
from mem import io                     # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run-dir", default=cfg.SM_RUN)
    ap.add_argument("--out", default=os.path.join(cfg.DATA_DIR, "events.h5"))
    ap.add_argument("--xsec", type=float, default=None, help="true sigma [pb] (default: summary.txt)")
    ap.add_argument("--stride", type=int, default=1, help="keep every k-th event")
    ap.add_argument("--nmax", type=int, default=None, help="read at most this many events")
    ap.add_argument("--kin-only", action="store_true", help="only weights and observables")
    ap.add_argument("--norm", choices=("channel", "total"), default="channel")
    ap.add_argument("--lo-points", type=int, default=8_000_000, help="points of the LO integration")
    ap.add_argument("--mtt-max", type=float, default=None,
                    help="m_tt ceiling applied at generation, if any (must match the run's cuts)")
    args = ap.parse_args()

    t0 = time.time()
    lhe = io.find_lhe(args.run_dir)
    sigma = args.xsec if args.xsec is not None else io.read_summary_xsec(args.run_dir)
    ev = io.read_lhe(lhe, args.nmax)
    n_read = len(ev["w"])
    sel = slice(None, None, args.stride)
    w_lhe = ev["w"][sel]
    t, tb, rw = ev["t"][sel], ev["tb"][sel], ev["rwgt"][sel]
    chan = io.channel_labels(ev["init"][sel])
    is_gg = chan == 0
    norm = dict(mode=args.norm, sigma_summary=sigma)
    if args.norm == "channel":
        from mem import validation
        lo = validation.lo_integration(args.lo_points, mtt_max=args.mtt_max)
        sig_c = {"gg": float(lo["w_gg"].sum()), "qq": float(lo["w_qq"].sum())}
        err_c = {"gg": float(np.sqrt(np.sum(lo["w_gg"] ** 2))), "qq": float(np.sqrt(np.sum(lo["w_qq"] ** 2)))}
        kap = {"gg": sig_c["gg"] / w_lhe[is_gg].sum(), "qq": sig_c["qq"] / w_lhe[~is_gg].sum()}
        w = np.where(is_gg, kap["gg"], kap["qq"]) * w_lhe
        norm.update(sigma_lo=sig_c, sigma_lo_err=err_c, kappa=kap, mtt_max=args.mtt_max)
        if abs(sum(sig_c.values()) / sigma - 1) > 3e-3:
            print(f"[warn] LO integration ({sum(sig_c.values()):.5f} pb) differs from summary.txt ({sigma} pb) "
                  "by more than 0.3%: check that the cuts (--mtt-max) match the run", flush=True)
        msg = (f"       LO integration: sigma_gg = {sig_c['gg']:.5f} +- {err_c['gg']:.5f}, sigma_qq = "
               f"{sig_c['qq']:.5f} +- {err_c['qq']:.5f}, total {sum(sig_c.values()):.5f} pb "
               f"(summary.txt: {sigma})\n       kappa_gg = {kap['gg']:.6g}, kappa_qq = {kap['qq']:.6g} "
               f"(ratio {kap['qq'] / kap['gg']:.4f})")
    else:
        kap = sigma / w_lhe.sum()
        w = kap * w_lhe
        norm.update(kappa=kap)
        msg = f"       single kappa = {kap:.6g} (sigma_gen = {sigma} pb)"
    kin = io.kinematics(t, tb)
    N = len(w)
    print(f"[read] {lhe}\n       {n_read} events read ({ev['n_skipped']} skipped), {N} kept "
          f"(stride {args.stride}) in {time.time() - t0:.0f}s\n{msg}\n"
          f"       negative weights: {np.mean(w < 0):.3%} of events, {w[w < 0].sum() / w.sum():.2e} of sigma\n"
          f"       median m_top = {np.median(kin['mtop']):.4f} (MEs use {cfg.MT}), "
          f"max pT(tt) = {kin['pt_tt_max']:.1e} GeV", flush=True)
    if abs(np.median(kin["mtop"]) - cfg.MT) > 0.01 or kin["pt_tt_max"] > 1e-3:
        sys.exit("[error] events are not LO 2->2 with m_top = MT")

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    meta = dict(run_dir=args.run_dir, lhe=lhe, sigma_summary=sigma, sigma_sample=float(w.sum()), norm=norm,
                sum_w_lhe_sel=float(w_lhe.sum()),
                n_read=n_read, n_skipped=ev["n_skipped"], stride=args.stride, sqrt_s=cfg.SQRT_S, mt=cfg.MT,
                lhaid=cfg.LHAID, muF=cfg.MUF_FACTORS, muR=cfg.MUR_FACTORS, flux_groups=cfg.FLUX_GROUPS,
                created=time.strftime("%Y-%m-%d %H:%M:%S"))
    with h5py.File(args.out, "w") as h5:
        h5.attrs["meta"] = json.dumps(meta)
        h5.create_dataset("w", data=w)
        h5.create_dataset("w_lhe", data=w_lhe)
        h5.create_dataset("channel", data=chan)
        h5["channel"].attrs["labels"] = "0 = gg, 1 = quark from beam 1, 2 = quark from beam 2"
        h5.create_dataset("pt", data=kin["pt"].astype(np.float32))
        h5.create_dataset("mtt", data=kin["mtt"])
        h5.create_dataset("cost", data=kin["cost"].astype(np.float32))
        h5.create_dataset("ytt", data=kin["ytt"])
        if args.kin_only:
            print(f"[done] {args.out}", flush=True)
            return
        for k in ("x1", "x2"):
            h5.create_dataset(k, data=kin[k])
        h5.create_dataset("n", data=kin["n"])
        h5.create_dataset("mu0", data=kin["mu0"].astype(np.float32))
        h5["mu0"].attrs["note"] = "float32 copy; recompute exactly as sqrt(MT^2 + pt^2) from n, mtt if needed"

        pdf = io.get_pdf()
        mu0 = kin["mu0"]
        a0 = io.alphas(mu0, pdf)
        h5.create_dataset("alphas0", data=a0)
        d_as = h5.create_dataset("alphas", (N, 3), np.float32, **io.H5_COMP)
        d_fl = h5.create_dataset("flux", (N, 3, len(cfg.FLUX_GROUPS)), np.float32,
                                 chunks=(min(N, 1 << 16), 3, len(cfg.FLUX_GROUPS)), **io.H5_COMP)
        d_fl.attrs["groups"] = json.dumps(cfg.FLUX_GROUPS)
        d_fl.attrs["muF"] = cfg.MUF_FACTORS
        d_as.attrs["muR"] = cfg.MUR_FACTORS
        for k, f in enumerate(cfg.MUF_FACTORS):
            d_fl[:, k, :] = io.fluxes(kin["x1"], kin["x2"], f * mu0, pdf).astype(np.float32)
        for k, f in enumerate(cfg.MUR_FACTORS):
            d_as[:, k] = (a0 if f == 1.0 else io.alphas(f * mu0, pdf)).astype(np.float32)
        if rw.shape[1]:
            g = h5.create_dataset("gen_scale", data=(rw / w_lhe[:, None]).astype(np.float32), **io.H5_COMP)
            g.attrs["ids"] = json.dumps(ev["rwgt_ids"])
            g.attrs["info"] = json.dumps(ev["rwgt_info"])
    print(f"[done] {args.out} ({os.path.getsize(args.out) / 1e6:.1f} MB) in {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
