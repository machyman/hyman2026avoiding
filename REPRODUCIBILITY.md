# Regenerating the figures reproducibly

All figure PDFs in `figs/` are registered in `hyman2026avoiding_STATUS.yaml`
with SHA-256 hashes of both the generator script and its outputs. For those
hashes to be meaningful, regeneration must be byte-deterministic.

Matplotlib embeds a `/CreationDate` timestamp in PDF output, so two runs of an
otherwise identical generator produce different bytes. Pin the timestamp:

```bash
export SOURCE_DATE_EPOCH=1750000000
MPLBACKEND=Agg python3 figs_src/<generator>.py
```

With `SOURCE_DATE_EPOCH` set, output is byte-identical across runs and the
registry check in the status file is a genuine reproducibility test rather than
a check that nobody has rerun anything.

Regenerate everything:

```bash
export SOURCE_DATE_EPOCH=1750000000
for g in ch6_phase_portrait ch7_figures ch7_reporting_lag ch8_preprocessing \
         ch8_central_comparison ch9_figures ch11_multistage_ic; do
  MPLBACKEND=Agg python3 "figs_src/$g.py"
done
```

Stochastic generators additionally seed with `default_rng(<chapter>)`; that
seeding governs the plotted data, while `SOURCE_DATE_EPOCH` governs the file
metadata. Both are required.
