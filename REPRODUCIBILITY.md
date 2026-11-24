# Regenerating the figures reproducibly

## In this repository

The sections below describe the book's build tree, where every generator sits in `figs_src/`. Here most sit in
`notebooks/chNN/` and `code/python/ch10_sensitivity/`, and the shared model in `src/`. Two, `ch8_structural_identifiability`
and `ch9_benchmarks`, sit in [`figs_src/`](figs_src/), because the book prints that path for them. Run a script from
the repository root with the model on the path:

```bash
export SOURCE_DATE_EPOCH=1750000000 MPLBACKEND=pdf PYTHONPATH=src
mkdir -p figs notebooks/figs
python3 notebooks/ch07/ch7_figures.py
```

As of book v2_134_0 the repository carries all 25 generators, and each is byte-identical to the book's own copy
(checked by SHA-256 on 2026-11-23). Three of them, `ch11_same_R0`, `ch12_herd_boundary` and
`ch16_generation_interval`, save to `../figs/` beside their own folder, which here is `notebooks/figs/`. The two in
`figs_src/` find the repository root from their own position: `ch9_benchmarks` reads `data/` and writes to `figs/`
there, and both write their printed values beside themselves. The others write to `figs/` at the repository root.
The registry check named below is the book's tool and is not part of this repository.

The scripts were not re-run from this layout for this update. The last such run, at book v2_110_2 (2026-10-24),
reproduced the book's 32 figures of that version byte for byte.

**The Python pin.** `requirements.txt` gives minimum versions, enough to run the code. Byte-identical figures
need the versions the book's figures were made with: matplotlib 3.10.8, numpy 2.4.4 and scipy 1.17.1, with
`MPLBACKEND=pdf`. The book's pin file also lists scipy 1.16.3 and sympy 1.14.0 for `ch9_benchmarks` and
`ch8_structural_identifiability`. Later versions can move labels and vertices by about a point without changing any
plotted value. One figure needs its own epoch: `ch3_exp_vs_linear_beta` reproduces at `SOURCE_DATE_EPOCH=1787747549`.

**The zlib.** Matplotlib compresses each PDF stream with Python's zlib. The standard zlib and zlib-ng, which some
systems install in its place, compress the same content to different bytes, so a byte-for-byte match also needs the
zlib the figure was made with. Check with `python3 -c "import zlib; print(zlib.ZLIB_RUNTIME_VERSION)"`. A figure that
differs only in this way has the same decoded content.

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
MPLBACKEND=pdf PYTHONPATH=figs_src python3 figs_src/<generator>.py
```

With `SOURCE_DATE_EPOCH` set, output is byte-identical across runs and the registry check is a
genuine reproducibility test rather than a check that nobody has rerun anything.

`PYTHONPATH=figs_src` is required by the generators that import the shared model, which is every generator
except `ch6_ngm_map`, `ch6_r0_paths`, `ch8_structural_identifiability`, `ch9_benchmarks`, `ch12_herd_boundary`,
`ch16_generation_interval`, `ch17_figures` and `ch18_figures`.

## Regenerate everything — all 25 generators, all 38 figures (book v2_134_0)

```bash
export SOURCE_DATE_EPOCH=1750000000
export MPLBACKEND=pdf
export PYTHONPATH=figs_src
for g in ch3_exp_vs_linear_beta ch4_alpha_vs_lambda ch6_bifurcation ch6_invasion_burden \
         ch6_ngm_map ch6_phase_portrait ch6_r0_paths ch7_figures ch7_reporting_lag ch8_central_comparison \
         ch8_influenza_fit ch8_preprocessing ch8_structural_identifiability ch8_weighting ch9_benchmarks \
         ch9_figures ch10_figures ch10_index_divergence ch10_sobol_panel ch11_multistage_ic ch11_same_R0 \
         ch12_herd_boundary ch16_generation_interval ch17_figures ch18_figures; do
  python3 "figs_src/$g.py"
done
```

Run from the directory containing `figs/`; the generators write relative paths. Output counts, which
sum to 38: `ch9_figures` writes 6, `ch7_figures` 4, `ch8_preprocessing` 3, `ch9_benchmarks` 3, `ch10_figures` 3,
`ch8_structural_identifiability` none (it writes its values file only), and the remaining nineteen write one each.

The other file in `figs_src/`, `sir_i_model.py`, is the shared model. In this repository the five
`notebooks/ch08/probes/ch8_route_b_*.py` scripts are diagnostics that print results and write nothing.

## Seeding

Stochastic generators seed with `default_rng(<chapter>)` or a fixed integer seed recorded in the script. That
seeding governs the plotted data, while `SOURCE_DATE_EPOCH` governs the file metadata. Both are required.

## Verifying a regeneration

Byte-compare against the registry, not by eye:

```bash
python3 tools/registry_check.py .
```

A clean run reports every registered file present and matching (0 missing, 0 mismatched). If figures differ only in
`/CreationDate`, `SOURCE_DATE_EPOCH` was not exported. If they differ in body content, check that the LaTeX packages
above are installed — a missing `dvipng` or `cm-super` changes glyph rendering without any error.
