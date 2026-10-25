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
> [current pre-publication draft (v2_108_2)](https://github.com/machyman/hyman2026avoiding/blob/main/docs/hyman2026avoiding_v2_108_2.pdf)
> is posted for comment, with the
> [claim audit ledger as of v2_108_2](https://github.com/machyman/hyman2026avoiding/blob/main/docs/AUDIT_LEDGER_v2_108_2.md).
> The published book will be available from Springer.

## What the book is about

This book lays a solid foundation for building mathematical models of infectious disease spread. It describes the
basic building blocks of susceptible-infected-recovered (SIR) transmission models: how each term is derived, what it
assumes, and how the model's predictions follow from its structure. Along the way it shows how to avoid the mistakes
most often made when simple models are fitted to data or extended to more complex settings. These pitfalls are rarely
exotic. Two teams can fit the same model to the same outbreak data and report reproductive numbers that differ by more
than a factor of three, because of a single assumption each made before fitting began. The book collects 28 such
pitfalls, explains where each one arises, and shows how to avoid it.

With that foundation in place, the book shows how to fit models to outbreak data, quantify the uncertainty in the
results, and find which parameters matter most. It then extends the model to the most common applications:

- latent periods, waning immunity, quarantine, disease-induced deaths and asymptomatic infection;
- populations with groups that mix unevenly;
- sexually transmitted infections, such as gonorrhea and HIV;
- vector-borne diseases, such as malaria;
- transmission from mother to child;
- age structure and infectiousness that changes over the course of an infection.

Three case studies, COVID-19, dengue and HIV, bring these tools together on real diseases, and a final chapter draws
the lessons they share.

The book is written for readers who work with AI assistants. Its exercises teach them to catch the fluent, confident
errors these tools make on exactly the questions the pitfalls concern. All 276 exercises are answered in an
instructor's guide, available to instructors on request; every chapter ends with a guide to further reading; and the
code behind every computed figure is in this repository, so each one can be regenerated.

## Who it's for

Upper-level undergraduates and beginning graduate students in applied mathematics, quantitative public health and
related fields, and the instructors who teach them. The book assumes a first course in ordinary differential
equations, linear algebra and calculus-based probability and statistics, but no prior exposure to epidemic modeling.

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
