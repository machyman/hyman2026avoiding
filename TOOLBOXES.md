# Open toolboxes for fitting and forecasting

These open tools let you reproduce and extend the fitting and forecasting workflows of *Foundations and Pitfalls in
Epidemic Modeling*, Chapters 7 and 8. Every number the book prints comes from the scripts in this repository; the
tools below are for going further. Checked 2026-11-08.

| Tool | Language | What it does | Cite |
|---|---|---|---|
| [GrowthPredict](https://github.com/gchowell/forecasting_growthmodels) | MATLAB | Fits and forecasts the generalized growth, generalized logistic, generalized Richards, Richards, logistic and Gompertz models; least squares or maximum likelihood with Poisson or negative-binomial error; parametric bootstrap; MAE, MSE, coverage and the weighted interval score. Its U.S. mpox series is the data of Section 8.8. | Chowell et al. (2024), *Sci. Rep.* 14, 1630, doi:10.1038/s41598-024-51852-8 |
| [scoringutils](https://epiforecasts.r-universe.dev/scoringutils) | R | Scores probabilistic forecasts, including the weighted interval score and interval coverage. | Bosse et al., arXiv:2205.07090 |
| [StructuralIdentifiability.jl](https://docs.sciml.ai/StructuralIdentifiability/dev/) | Julia | Local and global structural identifiability of ODE models; identifiable combinations of parameters. The box in Section 7.3 shows the call. | Dong, Goodbrake, Harrington and Pogudin (2023), *SIAM J. Appl. Algebra Geom.* 7(1), 194–235 |
| [GenSSI 2.0](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5905618/) | MATLAB | Structural identifiability by generating series, including multi-experiment analysis. | Ligon et al. (2018), *Bioinformatics* |

The book's own Python code:

- [`figs_src/ch9_benchmarks.py`](figs_src/ch9_benchmarks.py): Section 8.8 and the bootstrap lab of Section 8.2.1
  (four models, negative-binomial maximum likelihood, rolling-origin scores, AICc weights). Data:
  [`data/us_mpox_2022_weekly_cdc.txt`](data/us_mpox_2022_weekly_cdc.txt), copied unchanged from GrowthPredict
  (GPL-3.0; see [`data/`](data/)).
- [`figs_src/ch8_structural_identifiability.py`](figs_src/ch8_structural_identifiability.py): the rank test behind
  the box in Section 7.3.

Not yet checked for this list: R's pomp, EpiEstim and EpiNow2. Suggestions are welcome through the repository's
[issues](https://github.com/machyman/hyman2026avoiding/issues/new/choose).
