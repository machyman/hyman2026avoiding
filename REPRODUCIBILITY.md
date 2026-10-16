# Regenerating the figures reproducibly

## In this repository

The sections below describe the book's build tree, where the generators sit in `figs_src/`. Here they sit in
`notebooks/chNN/` and `code/python/ch10_sensitivity/`, and the shared model in `src/`. Run a script from the
repository root with the model on the path:

```bash
export SOURCE_DATE_EPOCH=1750000000 MPLBACKEND=Agg PYTHONPATH=src
mkdir -p figs
python3 notebooks/ch07/ch7_figures.py
```

As of book v2_87_1 the repository carries 15 of the 17 generators. `ch4_alpha_vs_lambda` and `ch8_weighting`
are not here yet. The registry check named below is the book's tool and is not part of this repository.

All figure PDFs in `figs/` are registered in `hyman2026avoiding_STATUS.yaml` with SHA-256 hashes of
both the generator script and its outputs. For those hashes to be meaningful, regeneration must be
byte-deterministic.

## System requirement: a LaTeX installation

The generators set `text.usetex = True`. Matplotlib then typesets every label through LaTeX rather
than its own math renderer, which is what keeps the figures free of Type 3 fonts — publishers
including SIAM and Springer require Type 1 or TrueType, and Type 3 renders poorly when zoomed and is
not reliably searchable.

This means **`pip install -r requirements.txt` is not sufficient.** The following must be present on
the system, and they are not Python packages:

    texlive-latex-base  texlive-latex-recommended  texlive-fonts-recommended
    cm-super  lmodern  dvipng  ghostscript

On Debian or Ubuntu:

```bash
sudo apt-get install -y --no-install-recommends \
    texlive-latex-base texlive-latex-recommended texlive-fonts-recommended \
    cm-super lmodern dvipng ghostscript
```

Without these, every generator fails at import time or falls back to Matplotlib's own renderer and
reproduces **Type 3** figures whose hashes will not match the registry.

## Pin the timestamp

Matplotlib embeds a `/CreationDate` in PDF output, so two runs of an otherwise identical generator
produce different bytes. Pin it:

```bash
export SOURCE_DATE_EPOCH=1750000000
MPLBACKEND=Agg PYTHONPATH=figs_src python3 figs_src/<generator>.py
```

With `SOURCE_DATE_EPOCH` set, output is byte-identical across runs and the registry check is a
genuine reproducibility test rather than a check that nobody has rerun anything.

`PYTHONPATH=figs_src` is required by the generators that import the shared model
(`ch6_phase_portrait`, `ch7_figures`, `ch10_figures`, `ch11_multistage_ic`).

## Regenerate everything — all 17 generators, all 29 figures (book v2_87_1)

The earlier version of this file listed seven generators covering 17 of the 28 figures, so
"regenerate everything" never did. The complete set:

```bash
export SOURCE_DATE_EPOCH=1750000000
export MPLBACKEND=Agg
export PYTHONPATH=figs_src
for g in ch3_exp_vs_linear_beta ch4_alpha_vs_lambda ch6_bifurcation ch6_invasion_burden \
         ch6_phase_portrait ch7_figures ch7_reporting_lag ch8_central_comparison \
         ch8_influenza_fit ch8_preprocessing ch8_weighting ch9_figures \
         ch10_figures ch10_index_divergence ch10_sobol_panel ch11_multistage_ic ch17_figures; do
  python3 "figs_src/$g.py"
done
```

Run from the directory containing `figs/`; the generators write relative paths. Output counts, which
sum to 29: `ch7_figures` writes 4, `ch9_figures` 6, `ch10_figures` 3, `ch8_preprocessing` 3, and the
remaining thirteen write one each.

The other seven files in `figs_src/` are not figure generators. `sir_i_model.py` is the shared model;
`ch8_likelihood_bridge_check.py` and the five `ch8_route_b_*.py` scripts are diagnostics that print
results and write nothing.

## Seeding

Stochastic generators seed with `default_rng(<chapter>)`. That seeding governs the plotted data,
while `SOURCE_DATE_EPOCH` governs the file metadata. Both are required.

## Verifying a regeneration

Byte-compare against the registry, not by eye:

```bash
python3 tools/registry_check.py .
```

At book v2_87_1 a clean run reports `49/49 (0 missing, 0 mismatched)`. If figures differ only in `/CreationDate`,
`SOURCE_DATE_EPOCH` was not exported. If they differ in body content, check that the LaTeX packages
above are installed — a missing `dvipng` or `cm-super` changes glyph rendering without any error.
