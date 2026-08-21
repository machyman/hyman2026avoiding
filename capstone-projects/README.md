# Capstone projects

Multi-week capstone projects assigned in the book's chapter exercises, one directory per project,
numbered by chapter. Each follows the book's six-step workflow (parameter elicitation, mathematical
analysis, numerical validation, AI-collaborative audit, disclosure, and final memo), and each
directory follows the same structure, so a project you have not read is navigable on sight.

**Two tiers.** A *term project* asks the student to analyze a disease and defend a conclusion about
it. A *chapter project* asks them to demonstrate that a technique works. Hours do not separate the
two — the longest project in the catalog is a chapter project and one of the shortest is a term
project — so the tier is recorded here rather than inferred.

## Chapter projects

- [`ch04-ai-audit-sir-i/`](ch04-ai-audit-sir-i/) — Chapter 4: Audit an AI's exposition of the SIR_I model (about 6–10 hours over 1–2 weeks). *No data, no fitting, no implementation; the natural first project.*
- [`ch07-debugging-project/`](ch07-debugging-project/) — Chapter 7: Full SIR_I implementation, verification, and debugging project (15–25 hours over 3–4 weeks). *The most programming-heavy project; judged as software.*
- [`ch08-fitting-uncertainty/`](ch08-fitting-uncertainty/) — Chapter 8: Full AI-collaborative fitting project (about 15–25 hours over 3–4 weeks). *Permits synthetic data, which is the only route on which the uncertainty quantification can itself be checked.*
- [`ch03-force-of-infection-extended/`](ch03-force-of-infection-extended/) — Chapter 3: Force of infection for a structurally richer contact model (about 20–30 hours over 3–4 weeks). *The longest chapter project; a derivation, with no disease to choose.*

## Term projects

- [`ch06-endemic-equilibrium/`](ch06-endemic-equilibrium/) — Chapter 6: Endemic-equilibrium analysis for a chosen pathogen (13–20 hours over 2–3 weeks). *The shortest term project; analysis rather than fitting, so it can run before Chapter 8.*
- [`ch10-sensitivity-intervention/`](ch10-sensitivity-intervention/) — Chapter 10: Full sensitivity-driven intervention recommendation (about 15–25 hours over 3–4 weeks). *Requires translating a parameter ranking into a named intervention.*
- [`ch17-covid-reanalysis/`](ch17-covid-reanalysis/) — Chapter 17: Re-analysis of a published COVID-19 R0 estimate (about 15–25 hours over 3–4 weeks). *The only project whose subject is a published paper.*
- [`ch12-two-group-fitting/`](ch12-two-group-fitting/) — Chapter 12: Full two-group SIR_I fitting and intervention recommendation (about 20–30 hours over 3–4 weeks). *Roughly doubles the parameter count against the same data.*
- [`ch14-vector-host-fitting/`](ch14-vector-host-fitting/) — Chapter 14: Full vector-host implementation and fitting project (about 20–30 hours over 3–4 weeks). *Carries entomological parameters that epidemiological surveillance does not measure.*

## How the projects connect

They ladder. Chapter 8's fitting workflow is a prerequisite for the Chapter 12, 14 and 17 projects,
and Chapter 10's sensitivity analysis feeds the Chapter 14 ranking. A student who has completed the
Chapter 8 project is substantially prepared for any of the three that build on it; a course running
one project per term can follow that order deliberately.

## Data

**No epidemiological data is redistributed in this repository.** Every project that needs data names
its source and its terms of use; see [`data/README.md`](https://github.com/machyman/hyman2026avoiding/blob/main/data/README.md) for provenance. Several
projects can be run entirely on constructed or synthetic data, which is noted in each.

## Code

Chapters 3, 6, 7, 8 and 10 have supporting code under [`notebooks/`](https://github.com/machyman/hyman2026avoiding/tree/main/notebooks) and
[`code/`](https://github.com/machyman/hyman2026avoiding/tree/main/code). Chapters 12, 14 and 17 have no chapter-specific code; those projects state so
directly and build on [`src/sir_i_model.py`](https://github.com/machyman/hyman2026avoiding/blob/main/src/sir_i_model.py) together with the Chapter 8
and Chapter 10 material.
