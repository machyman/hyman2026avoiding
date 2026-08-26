# Capstone: Full sensitivity-driven intervention recommendation

## At a glance

| | |
|---|---|
| Chapter | 10 — Sensitivity Analysis |
| Tier | term project — the student defends an intervention conclusion, not merely a ranking |
| Scope | one sensitivity analysis, one intervention ranking, one uncertainty assessment, one memo |
| Span | 3–4 weeks |
| Deliverable | an intervention recommendation driven by sensitivity analysis, with uncertainty in the ranking quantified |

Classified as a term project because the deliverable is a defended recommendation for a policy
audience. The sensitivity analysis is the instrument; the recommendation is the claim.

## Prerequisites

Chapter 10 worked through, in particular §10.2 (Local Sensitivity: The Normalized Sensitivity
Index), §10.6 (Global Sensitivity: Latin Hypercube Sampling and PRCC) and §10.7 (The
Invasion–Burden Partition: Quantitative Version). §10.5 (Tornado Plots) supplies the presentation
form, and §10.4 (Correlated Parameters) matters directly: the ranges sampled in step 3 are rarely
independent, and treating them as such is the most common way a global analysis goes quietly wrong.
Chapter 6's invasion–burden distinction is a hard prerequisite, since §10.7 (The Invasion–Burden
Partition: Quantitative Version) is its quantitative version and the recommendation turns on it.

Moderate programming, including sampling.

## Learning objectives

By the end, the student can:

1. Compute local sensitivity indices and say precisely what they hold fixed.
2. Design a global sensitivity analysis, including parameter ranges defended from sources.
3. Explain when local and global analyses disagree, and which to trust in that case.
4. Propagate parameter uncertainty into uncertainty in the *ranking*, not merely in the output.
5. Convert a ranking into an intervention recommendation without overstating what sensitivity
   analysis can establish.

## The task

The book's specification, from Chapter 10's exercises:

> Using local and global sensitivity analysis to drive an intervention recommendation for a specific
> epidemic-modeling problem, with quantified uncertainty in the ranking and a written recommendation
> memo for a policy audience.

The recommendation must name an intervention, not a parameter. "Reduce $c_I$" is a sensitivity
result; "prioritise isolation of symptomatic cases over mass screening" is a recommendation. Making
that translation, and being honest about what is lost in it, is the hardest part of the project.

## Materials

**Provided in this repository.** `code/python/ch10_sensitivity/ch10_sobol_panel.py` implements
variance-based global sensitivity and is the starting point for step 3.
`ch10_index_divergence.py` demonstrates local and global indices disagreeing — the phenomenon
objective 3 asks students to explain — and is the single most useful file here.
`notebooks/ch10/ch10_figures.py` produces the tornado and PRCC presentations.
`src/sir_i_model.py` supplies the model. `requirements.txt` and `REPRODUCIBILITY.md`.

**Student-supplied.** The modeling problem and its intervention menu, and parameter ranges with
sources. Ranges are the critical input: a global sensitivity analysis is only as meaningful as the
ranges sampled, and an indefensible range produces a confident, precise, worthless ranking. No
dataset is required.

**Deliberately not provided.** A parameter-range table, and a worked recommendation. Defending the
ranges is a graded criterion precisely because it is the step most often skipped.

## The six steps

1. **Parameter elicitation.** Establish ranges, not point values, each with a source and a stated
   distribution. Where evidence is thin, widen the range rather than guessing narrowly — and say so.
2. **Mathematical analysis.** Compute closed-form local sensitivity indices where §10.3 (Closed-Form
   Sensitivity Indices for the $SIR_I$ Model) provides them. These are exact and cheap, and they
   give a check on the sampled results later.
3. **Numerical validation.** Run the global analysis. Confirm convergence in the sample size rather
   than assuming it: re-run at two sample sizes and check the ranking is stable. Compare against the
   local indices and, where they disagree, diagnose why rather than choosing the congenial answer.
4. **AI-collaborative audit.** Ask an AI system to critique the sampling design and the ranking's
   interpretation. Sensitivity analysis attracts a specific overclaim — that a high index implies an
   effective intervention — and whether the AI reproduces or catches that overclaim is worth
   recording either way.
5. **Disclosure.** Log every interaction.
6. **Final memo.** The recommendation, the analysis behind it, and its limits, for a policy reader.

## Deliverable

A memo of roughly 2,500–4,000 words for a decision-maker who will not read an appendix. The
recommendation belongs in the first paragraph. Technical material — sampling design, convergence
evidence, index tables — goes in appendices.

Required: a tornado or PRCC figure; evidence of ranking stability under resampling; an explicit
statement of what the sensitivity analysis does *not* establish about intervention effectiveness.

## Assessment

Weighting is the instructor's. What follows is what to look for, not what each is worth; courses
differ in how much they weigh the sensitivity analysis against the intervention argument built on it,
and these materials do not legislate that.

| criterion | what a strong submission shows |
|---|---|
| Parameter ranges | sourced and defended; thin evidence met with wider ranges, stated |
| Local analysis | correct, with what is held fixed made explicit |
| Global analysis | design defended; convergence demonstrated, not assumed |
| Ranking uncertainty | uncertainty in the ranking itself, not only in the output |
| Recommendation quality | names an intervention; translation from parameter defended; limits stated |
| Disclosure completeness | complete, including rejected suggestions |

The translation from parameter to intervention carries more than its share. A recommendation that
names a parameter has not done the project's work, however sound the analysis behind it.

## Notes for instructors

**Scaling.** Assigning a shared modeling problem with different intervention menus makes the
sensitivity results comparable across the class while keeping the recommendations distinct. In a
small class, free choice of problem works and produces a wider final discussion.

**Common failure modes.** Ranges invented to be narrow, producing precise and meaningless rankings.
Global analysis run at one sample size with convergence assumed. Local and global disagreement
resolved by picking the preferred answer. Treating a high sensitivity index as proof an intervention
will work — the overclaim this chapter exists to prevent.

**Team option.** Two students can run local and global analyses independently and reconcile, which
makes the disagreement in objective 3 a genuine finding rather than an exercise. If teams are used,
AI disclosure is per person. Teams are offered, not required.
