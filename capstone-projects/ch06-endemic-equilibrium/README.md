# Capstone: Endemic-equilibrium analysis for a chosen pathogen

## At a glance

| | |
|---|---|
| Chapter | 6 — The $SIR_I$ Model: Analysis |
| Tier | term project — the student analyses a disease and defends a conclusion about it |
| Scope | one pathogen, one equilibrium analysis, one invasion--burden argument, one memo |
| Span | 2–3 weeks |
| Deliverable | an endemic-equilibrium analysis for one pathogen, with the invasion–burden distinction argued explicitly |

The shortest term project, and the natural first one for a course that wants students working with a
real pathogen early. It asks for analysis rather than fitting, so it can run before Chapter 8.

## Prerequisites

Chapter 6 worked through, in particular §6.5 (The Endemic Equilibrium), §6.6 (Stability of the
Endemic Equilibrium) and §6.7 (The Invasion–Burden Distinction). §6.1 (The Basic Reproductive
Number: Heuristic Derivation) and §6.3 (The Basic Reproductive Number: Next-Generation Matrix), the
two derivations of $\mathcal{R}_0$, are needed because the project asks which one the chosen
pathogen's literature actually
used. Chapter 5's derivation is assumed.

Light programming, at the level of `notebooks/ch06/`.

## Learning objectives

By the end, the student can:

1. Locate parameter estimates for a chosen pathogen in the primary literature and state what each
   estimate conditions on.
2. Compute the endemic equilibrium and assess its stability for that pathogen.
3. Argue whether the pathogen's public-health burden is invasion-driven or burden-driven, using the
   chapter's partition rather than intuition.
4. Identify at least one place where the $SIR_I$ structure is wrong for the chosen pathogen, and say
   what the error costs.
5. Defend a conclusion about the pathogen to a reader who may disagree.

## The task

The book's specification, from Chapter 6's exercises:

> Applying the chapter's analytical, numerical, and AI-collaborative tools to a pathogen with
> substantial endemic prevalence (suggested options include hepatitis B, tuberculosis, measles, or
> HIV in defined subpopulations).

The suggestions are genuinely suggestions. Any pathogen with a documented endemic state and
published parameter estimates works. HIV in a defined subpopulation is the most demanding of the
four, because the $SIR_I$ structure fits it worst — which some students will find the most
interesting part, and which step 4 is designed to surface.

## Materials

**Provided in this repository.** `src/sir_i_model.py`, which exposes `endemic_general()` and
`endemic_equal_contact()` as separate functions — the distinction matters here, and choosing the
wrong one silently is a graded failure mode. `notebooks/ch06/ch6_bifurcation.py`,
`ch6_phase_portrait.py` and `ch6_invasion_burden.py` cover the three analyses this project repeats
for a new pathogen; the last is the direct model for step 2. `requirements.txt` and
`REPRODUCIBILITY.md`.

**Student-supplied.** Parameter estimates for the chosen pathogen, from the primary literature. No
dataset is required; this is an analysis project, not a fitting project. Every parameter is cited to
a source, with its population and time period recorded, because an equilibrium computed from
parameters drawn from four incompatible settings is a graded failure mode rather than a rounding
issue.

**Deliberately not provided.** A parameter table for any suggested pathogen. Assembling one, and
discovering how much the published estimates disagree, is a substantial part of what the project
teaches.

## The six steps

1. **Parameter elicitation.** Assemble the parameter set from the literature. Record for each: the
   value, the source, the population it was estimated in, and the period. Where estimates conflict,
   record the range and pick a central value with a stated reason — do not average silently.
2. **Mathematical analysis.** Compute $\mathcal{R}_0$, the endemic equilibrium and its stability. Use
   `endemic_general()` unless equal contact rates are defensible for this pathogen, and if they are,
   say why in one sentence.
3. **Numerical validation.** Confirm the analytical equilibrium against a long-run simulation, and
   confirm the stability conclusion by perturbing away from it. An equilibrium that the simulation
   does not approach is a finding to chase, not a discrepancy to note.
4. **AI-collaborative audit.** Ask an AI system where the $SIR_I$ structure misrepresents this
   pathogen — no latent class for TB, no waning for measles, no risk structure for HIV. Then check
   its claims against the chapter. This step routinely produces both a real structural criticism and
   a confident invention; separating them is the exercise.
5. **Disclosure.** Log every interaction, including the invented criticism and how it was caught.
6. **Final memo.** The analysis, the invasion–burden verdict, and the structural limitations,
   written for a public-health reader rather than a modeler.

## Deliverable

A memo of roughly 2,500–4,000 words for a public-health audience: someone who will act on the
conclusion but will not check the algebra. The parameter table with sources is a required appendix,
as is the AI disclosure log.

The invasion–burden verdict must be stated as a claim the reader could disagree with, not hedged
into unfalsifiability.

## Assessment

Weighting is the instructor's. What follows is what to look for, not what each is worth; courses
differ in how much they weigh parameter elicitation against the equilibrium analysis it feeds, and
these materials do not legislate that.

| criterion | what a strong submission shows |
|---|---|
| Parameter elicitation | every value sourced, with population and period; conflicts surfaced rather than averaged away |
| Equilibrium and stability | correct, with the general/equal-contact choice justified |
| Invasion–burden argument | uses the chapter's partition; states a falsifiable verdict |
| Structural critique | at least one real limitation, with its cost named |
| Disclosure completeness | invented AI claims recorded alongside real ones |
| Memo clarity | actionable by a non-modeler |

One thing deserves more weight than its row suggests: whether `endemic_equal_contact()` was used
without justification. It is the error the chapter exists to prevent, and it is invisible in the
output — a submission can look entirely clean and still have made it.

## Notes for instructors

**Scaling.** Pathogen choice can be free in a class of fifteen; in a class of forty, assigning from
a list of six keeps parameter-source grading feasible and makes cross-project comparison possible in
the final session, which is where the invasion–burden distinction lands hardest.

**Common failure modes.** Parameters assembled from incompatible settings without noticing.
Equal-contact $\mathcal{R}_0$ used because it is the familiar formula. Treating the AI's structural criticism
as authoritative without checking it. Hedging the invasion–burden verdict into a statement no one
could disagree with.

**Team option.** Two students can split parameter elicitation from analysis, but the split is less
natural than in the derivation projects because elicitation drives everything downstream. If teams
are used, both members should work the elicitation and divide afterwards. AI disclosure is per
person. Teams are offered, not required.
