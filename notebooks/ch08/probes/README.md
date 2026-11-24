# Chapter 7 probes

Diagnostic scripts for the Route B question of the fitting chapter: whether an incidence-only fit of R0 depends on
the assumed susceptible population N^c, and in which regime. They use their own synthetic regime (R0 = 2.0), not the
shared baseline in [`../../../src/`](../../../src/). They print results and write no figure; no figure in the book
comes from them.

- [`ch8_route_b_probe.py`](ch8_route_b_probe.py): the probe itself.
- [`ch8_route_b_robustness.py`](ch8_route_b_robustness.py): the early and through-peak regimes across models and seed
  choices; the next three scripts read its set-up.
- [`ch8_route_b_ascertainment.py`](ch8_route_b_ascertainment.py): what a reporting fraction does to the fit.
- [`ch8_route_b_identifiability.py`](ch8_route_b_identifiability.py): tests whether the fit fixes R0 only through
  the assumed population divided by the ascertained one.
- [`ch8_route_b_lossfn_diagnostic.py`](ch8_route_b_lossfn_diagnostic.py): whether weighted and unweighted loss functions
  give the same minimum.

Run from the repository root (see [../README.md](../README.md)).
