"""Extended (unbinned) Matrix Element Method for the Scalar / VLF / Z' top-philic hypotheses.

Reference document: ExtendedMEM.tex. Modules:
    config    paths, physics constants, model definitions
    io        LHE reading, kinematics, PDF fluxes, HDF5 helpers
    mg        MadGraph library loading and param_card editing (used by scripts/compute_me.py)
    analysis  density ratios, Asimov deviance, Step A (best fits) and Step B (q_A), binned limit
    validation independent LO cross-checks
"""
