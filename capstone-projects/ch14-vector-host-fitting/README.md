# Capstone: Full vector-host implementation and fitting project

## At a glance

| | |
|---|---|
| Chapter | 14 — Vector-Borne Diseases |
| Tier | term project — the student analyses a vector-borne disease and defends an intervention conclusion |
| Scope | one pathogen, one vector-host model, one fit, one sensitivity-weighted recommendation, one memo |
| Span | 3–4 weeks |
| Deliverable | a fitted vector-host model with sensitivity-weighted intervention recommendations |

The most parameter-hungry project in the catalog. Vector-host models carry entomological
parameters that epidemiological surveillance does not measure, and confronting that gap honestly is
the substance of the work.

## Prerequisites

Chapter 14 worked through, in particular §14.2 (Vector Biology), §14.3 (The Vector-Host $SIR$ Model),
§14.4 (The Ross-Macdonald Reproductive Number) and §14.5 (Interventions and Their Effect on $\mathcal{R}_0$).
§14.6 (Case Study: Malaria) is the worked example. Chapter 8 for fitting and Chapter 10 for
sensitivity are both hard prerequisites — the deliverable requires all three.

Substantial programming.

## Learning objectives

By the end, the student can:

1. Implement a vector-host system and verify it against the Ross–Macdonald reproductive number.
2. Elicit entomological parameters from the vector-biology literature and state their conditioning —
   temperature, season, species, setting.
3. Fit the host-side dynamics to surveillance data while the vector side is largely unobserved, and
   say honestly what that asymmetry costs.
4. Rank interventions by their effect on $\mathcal{R}_0$, weighted by parameter sensitivity.
5. Judge which of the recommendation's conclusions survive the entomological uncertainty.

## The task

The book's specification, from Chapter 14's exercises:

> Implementing a vector-host model for a chosen vector-borne pathogen (suggested options span dengue,
> malaria, Zika, and West Nile), fitting the model to outbreak data, and producing intervention
> recommendations weighted by the vector-host parameter sensitivities.

Dengue and malaria have the richest parameter literature and are the safer choices. Zika and West
Nile are more exposed on entomological parameters, which makes objective 5 sharper and the project
harder; students choosing them should expect wider uncertainty and should not treat that as failure.

## Materials

**No chapter-specific code ships in this repository for Chapter 14.** Stated plainly rather than
papered over: citing a path that does not resolve is the defect class that cannot be corrected once
printed.

**Provided in this repository.** `src/sir_i_model.py` for the single-host dynamics and as the
structure the vector-host system generalizes. `notebooks/ch08/ch8_preprocessing.py` and
`ch8_influenza_fit.py` for the fitting workflow, which transfers with the caveat in objective 3.
`code/python/ch10_sensitivity/ch10_sobol_panel.py` for the sensitivity weighting in step 3 —
this project needs global sensitivity, not local, because the entomological ranges are wide.
`requirements.txt` and `REPRODUCIBILITY.md`.

**Student-supplied.** The vector-host implementation; human incidence data for the chosen pathogen;
and entomological parameter ranges from the vector-biology literature. **No epidemiological data is
redistributed here.** Dengue and malaria incidence are published by WHO and by national programmes;
West Nile by national surveillance systems. Entomological parameters — biting rate, vector
competence, extrinsic incubation period, vector lifespan — come from the entomological literature
and are typically reported per species and per temperature, which is exactly the conditioning
objective 2 asks students to record.

**Deliberately not provided.** An entomological parameter table for any suggested pathogen. Building
one, and discovering how strongly the values depend on setting, is the core of the elicitation step.

## The six steps

1. **Parameter elicitation.** Two literatures, kept separate. Host-side epidemiological parameters
   are fitted or sourced conventionally. Vector-side entomological parameters are almost always
   fixed from the literature, and each must record species, temperature and setting. A biting rate
   from a different species in a different climate is not a value, it is a guess with a citation.
2. **Mathematical analysis.** Derive $\mathcal{R}_0$ following §14.4 (The Ross-Macdonald Reproductive Number) and verify the implementation reproduces
   it. Establish what the system reduces to as the vector dynamics become fast relative to the host —
   the reduction that connects this chapter to the direct-transmission models, and a check on the
   implementation.
3. **Numerical validation.** Verify against the analytical $\mathcal{R}_0$, then fit the host-side dynamics.
   Run the global sensitivity analysis over the entomological ranges — the ranges are wide enough
   that local indices around a point estimate will mislead. Confirm the intervention ranking is
   stable under resampling.
4. **AI-collaborative audit.** Ask an AI system to critique the parameter elicitation, specifically
   whether any entomological value has been transported across species or setting without
   justification. This is the characteristic error in vector-borne modeling and the one most
   invisible in the output.
5. **Disclosure.** Log every interaction.
6. **Final memo.** The model, the fit, the ranking, and the honest uncertainty.

## Deliverable

A memo of roughly 3,000–5,000 words plus code, written for a vector-control programme manager: a
reader who will act on the ranking and who knows more about the vector than the modeler does. The
memo should be credible to that reader, which means the entomological conditioning must be visible.

Required: the entomological parameter table with sources and conditioning; verification against
Ross–Macdonald $\mathcal{R}_0$; a sensitivity-weighted intervention ranking; and a statement of which
conclusions survive the parameter uncertainty and which do not.

## Assessment

Weighting is the instructor's. What follows is what to look for, not what each is worth; courses
differ in how much they weigh entomological elicitation against the modeling that consumes it, and
these materials do not legislate that.

| criterion | what a strong submission shows |
|---|---|
| Entomological elicitation | species, temperature and setting recorded per parameter; transported values flagged |
| Implementation and $\mathcal{R}_0$ verification | reproduces Ross–Macdonald analytically and numerically |
| Fit quality | host-side fit sound; vector-side unobservability addressed, not ignored |
| Sensitivity-weighted ranking | global analysis over defended ranges; stability demonstrated |
| Robustness of conclusions | states which recommendations survive the uncertainty |
| Disclosure completeness | complete, including rejections |

Propagation of the entomological uncertainty deserves more weight than its row suggests. With ranges
this wide, a ranking that does not propagate them is an artifact of the point estimates chosen rather
than a finding.

## Notes for instructors

**Scaling.** Supplying a vetted entomological parameter table removes the parameter-elicitation
step from the scope, at the cost of the elicitation skill — a reasonable trade in a course where
Chapter 10 already covers elicitation. Assigning pathogens rather than allowing free choice prevents the whole
class choosing dengue.

**Common failure modes.** Entomological parameters transported across species or climate without
comment. Local sensitivity used where the ranges demand global. The vector side fitted as though it
were observed. A confident ranking whose order reverses under a defensible alternative parameter set.

**Team option.** The two literatures divide naturally: one student handles host-side fitting, the
other entomological elicitation and sensitivity, and they meet at the ranking. Given the breadth,
teams of two are worth encouraging, though not required. AI disclosure is accounted per person, and
the memo names who covered which literature.
