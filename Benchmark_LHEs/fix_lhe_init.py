#!/usr/bin/env python3
"""Rewrite the <init> block of a fixed-order aMC@NLO LHE file so Pythia8 accepts it.

Sets pp beams (2212, 2212) with the given energies, removes <eventgroup> tags,
replaces the placeholder colour tags (599) by a valid colour flow and sets the
mothers of the outgoing tops. Optionally truncates the file to N events.

Supported 4-particle events: g g > t t~ (one of the two possible colour flows,
chosen at random per event) and q q~ > t t~ (q = d, u, s, c, b, in either
beam order; s-channel colour-octet flow).
"""
import argparse
import gzip
import io
import random
import os
import sys

from tqdm import tqdm

GG_FLOWS = (
    {"g1": (501, 502), "g2": (502, 503), "t": (501, 0), "tbar": (0, 503)},
    {"g1": (501, 502), "g2": (503, 501), "t": (503, 0), "tbar": (0, 502)},
)
QQ_FLOW = {"q": (501, 0), "qbar": (0, 502), "t": (501, 0), "tbar": (0, 502)}


def fix_event(lines, rng):
    """lines: header + particle lines of one event; returns fixed lines."""
    if len(lines) != 5:
        raise ValueError("only 4-particle events are supported")
    parts = [l.split() for l in lines[1:]]
    ids = [int(f[0]) for f in parts]
    status = [int(f[1]) for f in parts]
    if status != [-1, -1, 1, 1] or sorted(ids[2:]) != [-6, 6]:
        raise ValueError("unexpected event content, not initial > t t~: " + "".join(lines[1:]))

    if ids[0] == 21 and ids[1] == 21:
        flow = rng.choice(GG_FLOWS)
        colours = [flow["g1"], flow["g2"]]
    elif ids[0] == -ids[1] and 1 <= abs(ids[0]) <= 5:
        colours = [QQ_FLOW["q"] if i > 0 else QQ_FLOW["qbar"] for i in ids[:2]]
        flow = QQ_FLOW
    else:
        raise ValueError(f"unsupported initial state {ids[:2]}")
    colours += [flow["t"] if i == 6 else flow["tbar"] for i in ids[2:]]

    out = [lines[0]]
    for k, (f, (col, acol)) in enumerate(zip(parts, colours)):
        f[4], f[5] = str(col), str(acol)
        if k >= 2:
            f[2], f[3] = "1", "2"
        out.append("  ".join(f) + "\n")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--ebeam", type=float, default=6500.0, help="energy per beam [GeV]")
    ap.add_argument("--pdfset", type=int, default=247000, help="PDFSET id (PDFSUP/PDFGUP)")
    ap.add_argument("--max-events", type=int, default=0, help="stop after N events (0 = all)")
    args = ap.parse_args()

    opener = lambda f, m: gzip.open(f, m) if f.endswith(".gz") else open(f, m)
    new_init = [
        "<init>\n",
        f"2212 2212 {args.ebeam:.8e} {args.ebeam:.8e} 0 0 {args.pdfset} {args.pdfset} -4 1\n",
        "1.0 0.0 1.0 1\n",
        "</init>\n",
    ]
    rng = random.Random(12345)
    nev = 0
    buf = None
    in_init = False
    raw = open(args.input, "rb")  # progress is tracked on the (compressed) bytes read
    fin = gzip.open(raw, "rt") if args.input.endswith(".gz") else io.TextIOWrapper(raw)
    pbar = tqdm(total=os.path.getsize(args.input), unit="B", unit_scale=True, desc="Converting")
    with fin, opener(args.output, "wt") as fout, pbar:
        for line in fin:
            if nev % 1000 == 0:
                pbar.update(raw.tell() - pbar.n)
            s = line.strip()
            if in_init:
                if s == "</init>":
                    in_init = False
                continue
            if s == "<init>":
                fout.writelines(new_init)
                in_init = True
            elif s in ("<eventgroup>", "</eventgroup>"):
                continue
            elif s == "</LesHouchesEvents>":
                break
            elif s == "<event>":
                buf = []
                fout.write(line)
            elif buf is not None and not s.startswith(("#", "<", "</")):
                buf.append(line)
            else:
                if buf is not None:
                    fout.writelines(fix_event(buf, rng))
                    buf = None
                fout.write(line)
                if s == "</event>":
                    nev += 1
                    pbar.set_postfix(events=nev)
                    if args.max_events and nev >= args.max_events:
                        break
        fout.write("</LesHouchesEvents>\n")
    print(f"Wrote {nev} events to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
