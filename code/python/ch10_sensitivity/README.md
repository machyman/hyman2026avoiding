# Chapter 10 sensitivity module

Python implementations for the Chapter 10 sensitivity analysis:

- [`ch10_index_divergence.py`](ch10_index_divergence.py) — normalized
  sensitivity-index divergence of the endemic burden as R0 approaches 1.
- [`ch10_sobol_panel.py`](ch10_sobol_panel.py) — the Sobol variance-based
  panel (analytic indices against Monte Carlo estimates).

The LHS-PRCC driver that produces the chapter's tornado and PRCC figures is
[`../../../notebooks/ch10/ch10_figures.py`](../../../notebooks/ch10/ch10_figures.py);
its README is [`../../../notebooks/ch10/`](../../../notebooks/ch10/).
Run everything from the repository root.
