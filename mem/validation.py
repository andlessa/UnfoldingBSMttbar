"""Independent LO cross-checks (no MadGraph): analytic Born matrix elements and a direct
Monte Carlo integration of the LO SM cross section in the generation region."""
import numpy as np

from . import config as cfg
from .io import get_pdf, fluxes


def born_lo(mtt, cost, alphas, mt=cfg.MT):
    """Spin/colour-averaged LO |M|^2 for gg -> t tbar and q qbar -> t tbar (Nason-Dawson-Ellis form)."""
    s = mtt ** 2
    beta = np.sqrt(1 - 4 * mt ** 2 / s)
    t1 = 0.5 * (1 - beta * cost)          # (m^2 - t)/s
    t2 = 0.5 * (1 + beta * cost)          # (m^2 - u)/s
    rho = 4 * mt ** 2 / s
    g4 = (4 * np.pi * alphas) ** 2
    qq = g4 * 4 / 9 * (t1 ** 2 + t2 ** 2 + rho / 2)
    gg = g4 * (1 / (6 * t1 * t2) - 3 / 8) * (t1 ** 2 + t2 ** 2 + rho - rho ** 2 / (4 * t1 * t2))
    return gg, qq


def lo_integration(n_points=4_000_000, pt_range=(500.0, 3500.0), mtt_max=None, seed=1,
                   chunk=500_000, mt=cfg.MT):
    """Weighted LO SM events in the generation region (signed PDFs, mu_R = mu_F = H_T/2).

    mtt_max: optional generation ceiling on m_tt (None = no cut).
    Sampling: m_tt ~ m_tt^-5, y_tt and cos(theta*) uniform.
    Returns dict(w, w_gg, w_qq [pb], pt, mtt); w = w_gg + w_qq.
    """
    pdf = get_pdf()
    rng = np.random.default_rng(seed)
    S = cfg.SQRT_S ** 2
    mlo = 2 * np.sqrt(mt ** 2 + pt_range[0] ** 2)
    p = 5.0
    mtt_max = cfg.SQRT_S if mtt_max is None else mtt_max      # None: no m_tt ceiling
    a, b = mlo ** (1 - p), mtt_max ** (1 - p)
    out = dict(w=[], w_gg=[], w_qq=[], pt=[], mtt=[])
    for start in range(0, n_points, chunk):
        n = min(chunk, n_points - start)
        mtt = (a + rng.random(n) * (b - a)) ** (1 / (1 - p))
        jm = (b - a) / (1 - p) * mtt ** p
        tau = mtt ** 2 / S
        ymax = -0.5 * np.log(tau)
        y = (2 * rng.random(n) - 1) * ymax
        c = 2 * rng.random(n) - 1
        beta = np.sqrt(1 - 4 * mt ** 2 / mtt ** 2)
        pt = 0.5 * mtt * beta * np.sqrt(1 - c ** 2)
        x1, x2 = np.sqrt(tau) * np.exp(y), np.sqrt(tau) * np.exp(-y)
        mu = np.sqrt(mt ** 2 + pt ** 2)
        als = np.array([pdf.alphasQ(float(q)) for q in mu])
        gg, qq = born_lo(mtt, c, als, mt)
        F = fluxes(x1, x2, mu, pdf)
        jac = beta / (32 * np.pi * mtt ** 2) * (2 * mtt / S) * jm * (2 * ymax) * 2.0 * cfg.GEV2_TO_PB / n_points
        ok = (pt > pt_range[0]) & (pt < pt_range[1])
        wg = F[:, 0] * gg * jac * ok
        wq = F[:, 1:].sum(axis=1) * qq * jac * ok
        out["w"].append(wg + wq)
        out["w_gg"].append(wg)
        out["w_qq"].append(wq)
        out["pt"].append(pt)
        out["mtt"].append(mtt)
    return {k: np.concatenate(v) for k, v in out.items()}


def hist_with_err(x, w, bins):
    h, _ = np.histogram(x, bins, weights=w)
    e2, _ = np.histogram(x, bins, weights=w ** 2)
    return h, np.sqrt(e2)
