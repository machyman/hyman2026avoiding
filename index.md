---
title: Home
layout: default
nav_order: 1
description: Companion site for the book "Foundations and Pitfalls in Epidemic Modeling."
---

# Foundations and Pitfalls in Epidemic Modeling

*An Introduction to Formulating, Analyzing, and Fitting Models*
James M. Hyman · Zhuolin Qu · Ling Xue — Springer (Interdisciplinary Applied
Mathematics), under review.

This is the companion site for the book. It hosts the reproducible code behind
the book's figures and numerical results, together with datasets and guided labs
as they are finalized.

> **The book is under review with Springer.** With Springer's permission, the
> [current pre-publication draft (v2_110_2)](https://github.com/machyman/hyman2026avoiding/blob/main/docs/hyman2026avoiding_v2_110_2.pdf)
> is posted for comment, with the
> [claim audit ledger as of v2_110_2](https://github.com/machyman/hyman2026avoiding/blob/main/docs/AUDIT_LEDGER_v2_110_2.md).
> The published book will be available from Springer.

## What the book is about

This book lays a foundation for building mathematical models of how infectious diseases spread. It starts from the
rate at which new infections occur and builds the susceptible-infected-recovered (SIR) model one term at a time,
asking where each term comes from, what it assumes, and what the model's behavior owes to it. A reader who finishes
the book should be able to formulate a model for a new disease, analyze it, fit it to data, and judge how far its
conclusions can be trusted.

Along the way the book marks the places where simple models most often mislead. A model can be fitted to a quantity
the data do not report. A parameter the data cannot determine can be reported as if it were known. An intervention
can be judged by its effect on the threshold for an outbreak rather than by the disease it prevents. Each of these
mistakes produces an answer that looks reasonable and is wrong. The book names each pitfall where it is most
tempting, shows how to recognize it, and shows how to avoid it.

With that foundation in place, the book shows how to fit models to outbreak data, check which parameters the data can
determine, and quantify the uncertainty in the results. It then extends the model to the settings met most often in
practice:

- latent periods, waning immunity, quarantine, disease-induced deaths and asymptomatic infection;
- populations whose groups mix unevenly;
- sexually transmitted infections, such as gonorrhea and HIV;
- vector-borne diseases, such as malaria and dengue;
- transmission from mother to child;
- structure in age and in time since infection, which leads to the renewal equation.

Three case studies, COVID-19, dengue and HIV, bring these tools together on real diseases, and a final chapter draws
the lessons they share.

The book is written for readers who work with AI assistants. Its tagged exercises teach them to catch the fluent, confident
errors these tools make in exactly the places the pitfalls describe. Every exercise is answered in an instructor's
guide, available to instructors on request; every chapter has a guide to further reading; and the code behind
every computed figure is in this repository, so each one can be regenerated.

## Who it's for

Upper-level undergraduates and beginning graduate students in applied mathematics, quantitative public health and
related fields, and the instructors who teach them. The book assumes a first course in ordinary differential
equations, linear algebra and calculus-based probability and statistics, but no prior exposure to epidemic modeling.
It is also written for working modelers who want a practical reference on fitting epidemic models to real data.

## Navigating the materials

- **[Code](https://github.com/machyman/hyman2026avoiding/tree/main/notebooks)** —
  per-chapter scripts (`ch03`, `ch04`, `ch06`–`ch12`, `ch16`, `ch17`) that reproduce the figures, built on a
  [shared model](https://github.com/machyman/hyman2026avoiding/tree/main/src).
- **[Data](https://github.com/machyman/hyman2026avoiding/tree/main/data)** —
  provenance and pointers for the case-study datasets (e.g., the WSU 2009 H1N1
  data via the MIDAS catalog).
- **[Capstones](https://github.com/machyman/hyman2026avoiding/tree/main/capstone-projects)** —
  the book's chapter capstone projects, one directory per project.
- **[Draft and audit ledger](https://github.com/machyman/hyman2026avoiding/tree/main/docs)** —
  the pre-publication draft (PDF) and the record of corrections to printed claims.
- **Labs** — guided, multi-step notebooks *(in preparation)*.
- **Errata & questions** — please
  [open an issue](https://github.com/machyman/hyman2026avoiding/issues/new/choose).
- **[Repository changelog](https://github.com/machyman/hyman2026avoiding/blob/main/CHANGELOG.md)** —
  reader-facing changes to the companion materials.

## Running the code

```
pip install -r requirements.txt
mkdir -p figs
PYTHONPATH=src python notebooks/ch07/ch7_figures.py
```

Run from the repository root with `PYTHONPATH=src`; figures are written to `figs/`. Anything involving
randomness is seeded for reproducibility.

## Citing

```bibtex
@book{hyman2026avoiding,
  title     = {Foundations and Pitfalls in Epidemic Modeling: An Introduction to
               Formulating, Analyzing, and Fitting Models},
  author    = {Hyman, James M. and Qu, Zhuolin and Xue, Ling},
  year      = {2026},
  publisher = {Springer},
  series    = {Interdisciplinary Applied Mathematics},
  note      = {Under review}
}
```

See also
[`CITATION.cff`](https://github.com/machyman/hyman2026avoiding/blob/main/CITATION.cff).
The ISBN and a Zenodo DOI for this repository are pending.
