# Capstone: Force of infection for a structurally richer contact model

## At a glance

| | |
|---|---|
| Chapter | 3 — The Force of Infection: Susceptible Viewpoint |
| Tier | chapter project — the student demonstrates that a derivation technique extends, rather than analyzing a disease |
| Scope | one contact structure, one derivation, one validation sweep, one memo |
| Span | 3–4 weeks |
| Deliverable | a derived force-of-infection expression for one richer contact structure, validated numerically against the chapter's baseline |

The longest chapter project in the catalog, and the reason tiers are not read off duration: this runs
longer than three of the term projects while remaining squarely about method. There is no disease to
choose and no data to fit. What is being demonstrated is that the chapter's stochastic-Poisson
argument survives contact with a structure it was not written for.

**What moves the estimate.** Chapter 3 prints about 20–30 hours over 3–4 weeks. That figure describes
a solo student who already handles graphs and works without AI assistance. Choosing a network
structure without that background roughly doubles it. A team of two shortens elapsed time but not
total effort. Using AI as a checked collaborator relocates effort rather than removing it: whatever
step 2 delegates, step 4 has to audit. Plan against the scope and the span; treat the hours as a
description of one case rather than a promise.

## Prerequisites

Chapter 3 worked through in full, in particular §3.1 (The Susceptible Individual's Perspective) and
§3.2 (The Force of Infection from the Stochastic Contact Process), which supply the Poisson argument
this project generalizes. §3.3 (Discrete-Time Issues) matters if the chosen structure is simulated on
a daily step. Chapter 2's infection equation is assumed.

Programming is needed for the validation step only, at the level of `notebooks/ch03/`. Students
choosing a network structure need enough graph handling to build and sample an adjacency structure;
this is the single most common reason a project runs past its estimate.

## Learning objectives

By the end, the student can:

1. State precisely which independence assumption in the chapter's derivation fails under their
   chosen structure, and where in the argument it enters.
2. Re-derive the force of infection from the contact process, rather than patching the result.
3. Recover the chapter's $\lambda = c_S \beta P_I$ as a limiting case, and say what limit is being
   taken.
4. Validate a closed-form expression against stochastic simulation, including a stated criterion for
   what counts as agreement.
5. Distinguish a structural effect from a sampling artifact when the two disagree.

## The task

The book's specification, from Chapter 3's exercises:

> A multi-week project deriving the chapter's force-of-infection expression
> $\lambda = c_S \beta P_I$ for one of several structurally richer settings (heterogeneous contact
> rates, age-stratified mixing, network-based contact, or others) from first principles using the
> chapter's stochastic-Poisson framework as the starting point.

The chapter states the task; the details live here. One structure is enough. Attempting two is the
second most common reason a project overruns.

## Materials

**Provided in this repository.** `src/sir_i_model.py` for the baseline dynamics the derivation must
reduce to. `notebooks/ch03/ch3_exp_vs_linear_beta.py` as the worked pattern for comparing a
closed-form expression against a numerical alternative — the validation step here has the same
shape. `requirements.txt` and `REPRODUCIBILITY.md` for the environment.

**Student-supplied.** The contact structure itself: a mixing matrix, a degree distribution, or a
generated network, together with its parameters. Where a structure is drawn from published work, the
source is cited and its parameters recorded in the memo. No dataset is required — this project can
run entirely on constructed structures, which is why it works in a course with no data access.

**Deliberately not provided.** A worked derivation for any of the suggested structures. The
derivation is the deliverable; supplying one converts the project into a transcription exercise.

## The six steps

1. **Parameter elicitation.** Fix the baseline first: the chapter's $c_S$, $\beta$ and $P_I$, and the
   value of $\lambda$ they imply. This is the number the richer expression must reproduce in the
   limit, and eliciting it before generalizing prevents a derivation that agrees with nothing.
2. **Mathematical analysis.** Re-derive from the contact process. Name the assumption being relaxed
   before relaxing it — homogeneous contact rate, proportionate mixing, or independence between a
   susceptible's contacts — and carry the derivation through to a closed form. For a network
   structure a closed form generally does not exist without a moment closure. A pair approximation
   is acceptable, and arguably the better project: stating the closure and what it costs is the same
   skill as naming the relaxed assumption. State it explicitly and test its cost in step 3 rather
   than assuming it is small.
3. **Numerical validation.** Simulate the contact process directly and compare the realized hazard
   against the derived expression across a parameter sweep. State the agreement criterion in
   advance. A closed form that matches at one parameter value has not been validated. Where the two
   disagree, adjudicate rather than average: say whether the gap is a structural effect the
   derivation missed or sampling noise in the simulation, and give the evidence — a wider sweep,
   more realizations, or a tighter interval. Which one it was belongs in the memo.
4. **AI-collaborative audit.** Put the derivation to an AI system and ask it to find the step where
   the independence assumption is used implicitly. This is the failure mode the chapter warns about
   and the one most likely to survive a student's own reading. Record what it found and what it
   missed; both go in the log.
5. **Disclosure.** Record every AI interaction: what was asked, what was returned, what was kept and
   what was rejected. Rejected suggestions matter as much as accepted ones.
6. **Final memo.** The derivation, the validation, the audit and the limiting case, written for a
   reader who knows Chapter 3 but not the chosen structure.

## Deliverable

A memo of roughly 3,000–5,000 words with the derivation set out in full, plus the validation code
and the AI disclosure log as appendices. The audience is a classmate who has read Chapter 3: the
memo should let them reconstruct the derivation without the source the structure came from.

Figures: at minimum one showing derived against simulated hazard over the swept parameter, with the
agreement criterion visible.

## Assessment

Weighting is the instructor's. What follows is what to look for, not what each is worth; courses
differ in how much they weigh derivation against communication, and these materials do not legislate
that.

| criterion | what a strong submission shows |
|---|---|
| Correctness of the derivation | each step justified; the relaxed assumption named where it enters; any closure stated |
| Recovery of the baseline limit | the chapter's expression recovered, with the limit stated explicitly |
| Numerical validation | criterion stated in advance; swept, not a single point; disagreement adjudicated rather than smoothed |
| AI audit quality | a real defect found, or a substantiated argument that none remains |
| Disclosure completeness | rejected suggestions recorded alongside accepted ones |
| Memo clarity | reconstructible by the stated audience |

The limiting case deserves particular attention. It is the only available check that the
generalization is of *this* model: a derivation that is internally correct but never reduces to the
chapter's baseline may be a perfectly good derivation of something else.

## Notes for instructors

**Scaling.** Assigning structures rather than letting students choose keeps grading tractable and
prevents the whole class converging on age-stratified mixing, which has the most accessible
literature. Four structures across a class of thirty works well.

**Common failure modes.** Patching the result instead of re-deriving — the tell is an expression
that cannot be traced back to the contact process. Validating at a single parameter value. Choosing
a network structure without the graph-handling background, which roughly doubles the work and is the
most common cause of an overrun. Attempting two structures.

**Team option.** Teams of two work naturally here, since the derivation and the simulation validate
each other and can be developed in parallel by different hands before being reconciled. If teams are
used, AI disclosure is accounted per person, not per team: each member logs their own interactions,
and the memo names who derived and who validated. Teams are offered, not required; the project is
sized for one student.
