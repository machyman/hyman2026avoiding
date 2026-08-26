# Capstone: Full two-group $SIR_I$ fitting and intervention recommendation

## At a glance

| | |
|---|---|
| Chapter | 12 — Two-Group Models |
| Tier | term project — the student analyses a stratified outbreak and defends an intervention conclusion |
| Scope | one two-group model, one fit, one heterogeneity-aware recommendation, one memo |
| Span | 3–4 weeks |
| Deliverable | a fitted two-group model with a heterogeneity-aware intervention recommendation |

Among the most demanding projects in the catalog: it combines Chapter 8's fitting with Chapter 12's
structure, and the parameter count roughly doubles while the data rarely does. That tension is the
point.

## Prerequisites

Chapter 12 worked through, in particular §12.2 (The Mixing Matrix), §12.3 (The Two-Group $SIR_I$ Dynamics),
§12.4 (The Basic Reproductive Number via the Next-Generation Matrix) and §12.7 (Herd Immunity in
Heterogeneous Populations). §12.8 (A Numerical Case Study) is the worked pattern. Chapter 8 is a hard
prerequisite: this is a fitting project before it is a heterogeneity project.

Substantial programming.

## Learning objectives

By the end, the student can:

1. Specify a mixing matrix and state what its off-diagonal structure asserts about behavior.
2. Fit a two-group model to stratified incidence and report which parameters the stratification
   actually identifies.
3. Compute $\mathcal{R}_0$ via the next-generation matrix for the fitted system.
4. Show how a heterogeneity-aware intervention recommendation differs from the homogeneous one, and
   quantify the difference.
5. Judge whether the available data supports two groups at all.

## The task

The book's specification, from Chapter 12's exercises:

> Fitting a two-group $SIR_I$ model to an outbreak with observable group-level heterogeneity
> (suggested options include age-stratified COVID-19, risk-group-stratified HIV, school-age-
> stratified influenza, or vaccination-stratified measles), and producing an intervention
> recommendation that accounts for the heterogeneity.

Objective 5 is not a formality. A defensible outcome of this project is a well-argued finding that
the data does not support the two-group structure, with the homogeneous model preferred. That
conclusion earns full marks if it is properly established.

## Materials

**No chapter-specific code ships in this repository for Chapter 12.** This is stated plainly because
the alternative — citing a path that does not resolve — is the defect class that cannot be fixed
after printing. The general materials below apply, and the project is built on them.

**Provided in this repository.** `src/sir_i_model.py` for the single-group dynamics the two-group
system must reduce to when the groups are made identical — that reduction is the primary
implementation check and step 3 requires it. `notebooks/ch08/ch8_preprocessing.py` and
`ch8_influenza_fit.py` supply the fitting workflow, which carries over directly; the identifiability
probes in `notebooks/ch08/probes/` matter more here than in Chapter 8, because the parameter count is
higher. `requirements.txt` and `REPRODUCIBILITY.md`.

**Student-supplied.** The two-group implementation, and stratified incidence data. **No
epidemiological data is redistributed here.** Age-stratified COVID-19 incidence is published by most
national public-health agencies; risk-group-stratified HIV surveillance by UNAIDS and national
programmes; school-age influenza by sentinel surveillance systems. Whichever is used, the
stratification must be present in the *data*, not imposed on an aggregate series — imposing it is a
graded failure mode.

**Deliberately not provided.** A mixing-matrix parameterization. Choosing one and defending it is
the chapter's central skill.

## The six steps

1. **Parameter elicitation.** Specify the groups, the mixing matrix form, and which of its entries
   are fitted against fixed. State the assortativity assumption explicitly — every mixing matrix
   encodes one, and leaving it implicit is how heterogeneity results become uninterpretable.
2. **Mathematical analysis.** Derive $\mathcal{R}_0$ via the next-generation matrix for the specified structure,
   before fitting. Establish what the two-group system reduces to when the groups are identical;
   this is both a check and a limiting case the fit must respect.
3. **Numerical validation.** Verify the implementation against the reduction in step 2 — identical
   groups must reproduce `src/sir_i_model.py` to numerical tolerance. Then fit, with multi-start
   convergence checks. Test identifiability seriously: with roughly twice the parameters and
   commonly the same information, some combinations will not be identified, and finding out which is
   part of the deliverable.
4. **AI-collaborative audit.** Ask an AI system to critique the mixing specification and the
   identifiability treatment. A known failure mode is confident interpretation of a
   non-identifiable parameter; whether the AI commits it is worth recording.
5. **Disclosure.** Log every interaction, including rejected reparameterisations.
6. **Final memo.** The fit, the heterogeneity finding, and the recommendation.

## Deliverable

A memo of roughly 3,000–5,000 words plus code. The audience is a public-health decision-maker
choosing between a targeted and an untargeted intervention: the memo must say which, and what
confidence the data supports.

Required: the mixing matrix with its assumptions stated; evidence of the identical-groups reduction;
an identifiability statement; and a quantified comparison of the heterogeneity-aware and homogeneous
recommendations.

## Assessment

Weighting is the instructor's. What follows is what to look for, not what each is worth; courses
differ in how much they weigh the mixing specification against the identifiability analysis, and
these materials do not legislate that.

| criterion | what a strong submission shows |
|---|---|
| Mixing specification | form defended; assortativity assumption explicit |
| Implementation validation | identical-groups reduction demonstrated numerically |
| Fit and identifiability | multi-start; non-identifiable combinations named, not silently reported |
| $\mathcal{R}_0$ via next-generation matrix | correct for the fitted structure |
| Recommendation | targeted-versus-untargeted addressed; difference quantified |
| Disclosure completeness | complete, including rejections |

Fitted group-specific parameters reported without an identifiability analysis should weigh heavily
against a submission. Doubling the parameters against the same data is precisely where confident
meaningless estimates appear.

## Notes for instructors

**Scaling.** This is a heavy project; in a shorter course consider supplying the two-group
implementation and grading fitting and interpretation only, which removes roughly a third of the
effort without touching the chapter's central skills. Assigning a shared dataset with different
stratifications makes cross-project comparison possible.

**Common failure modes.** Stratification imposed on aggregate data rather than found in it. The
identical-groups reduction skipped, so implementation errors survive into the fit. Group-specific
parameters interpreted confidently when the data cannot separate them. Recommending a targeted
intervention on a difference within the fitting uncertainty.

**Team option.** This project divides better than most: one student builds and validates the
two-group implementation while the other prepares the data and the mixing specification, meeting at
the fit. Given the size, teams of two are worth actively encouraging here, though still not required.
AI disclosure is accounted per person, and the memo names who did which.
