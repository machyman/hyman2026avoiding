# figs_src

The two scripts the book cites by a `figs_src/` path. They sit here, at the printed paths, rather than in
[`../notebooks/`](../notebooks/), so that every path the book prints resolves. Both locate their inputs and
outputs from their own position, so they run from any directory; the repository root is the usual one.

Scripts and the values they print:
- [`ch9_benchmarks.py`](ch9_benchmarks.py): Chapter 8, Section 8.8 (benchmarks, forecasts and rival models) and
  the parametric-bootstrap lab of Section 8.2.1. Four models (GGM, GLM, Richards, SIR) fitted to the U.S. mpox
  series by negative-binomial maximum likelihood; rolling-origin scores; AICc weights. Reads
  [`../data/us_mpox_2022_weekly_cdc.txt`](../data/us_mpox_2022_weekly_cdc.txt) (GPL-3.0, see
  [`../data/`](../data/)). Writes `figs/ch9_bootstrap_lab.pdf`, `figs/ch9_benchmark_fits.pdf` and
  `figs/ch9_forecast_scores.pdf` (Figures 8.3, 8.8 and 8.9) at the repository root; run `mkdir -p figs` first.
- [`ch9_benchmarks_values.txt`](ch9_benchmarks_values.txt): every value the text quotes from that script, as the
  book's run printed it. A new run overwrites it.
- [`ch8_structural_identifiability.py`](ch8_structural_identifiability.py): Chapter 7, Section 7.3, the box
  "Check Structural Identifiability Before You Fit". The Lie-derivative rank test for local structural
  identifiability, in exact rational arithmetic. Needs SymPy. No figure.
- [`ch8_structural_identifiability_values.txt`](ch8_structural_identifiability_values.txt): the ranks and
  unidentifiable directions, as the book's run printed them. A new run overwrites it.

The file names keep the book's source-file numbers (`ch8`, `ch9`), as the folders in `notebooks/` do. Related open
tools in MATLAB, R and Julia are listed in [`../TOOLBOXES.md`](../TOOLBOXES.md).
