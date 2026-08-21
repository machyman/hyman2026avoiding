# Capstone: Full $SIR_I$ implementation, verification, and debugging project

## At a glance

| | |
|---|---|
| Chapter | 7 — The $SIR_I$ Model: Simulations |
| Effort | about 15–25 hours over 3–4 weeks |
| Tier | chapter project — the student demonstrates that a verification technique works |
| Deliverable | a working $SIR_I$ simulator with a verification suite that provably catches seeded defects |

The most programming-heavy project in the catalog and the only one whose deliverable is judged
primarily as software. It suits a course with a computational emphasis, and it is the natural
partner to Chapter 7 for students who arrive already able to code.

## Prerequisites

Chapter 7 worked through, in particular §7.2 (Numerical Implementation), §7.7 (Verification Against
the Analysis) and §7.8 (When the Parameters Themselves Change in Time). §7.3 and §7.4 supply the two
scenarios the suite must reproduce. Chapter 6's analytical results are the verification targets, so
Chapter 6 is a hard prerequisite rather than a soft one.

Substantial programming. This is the wrong project for a student writing their first numerical code.

## Learning objectives

By the end, the student can:

1. Implement a compartmental model from its equations, with the integration scheme chosen and
   justified rather than defaulted to.
2. Build a verification suite that tests against analytical results, not against its own output.
3. Demonstrate that each test fails when the defect it targets is present — a test that has never
   failed has not been shown to work.
4. Distinguish a numerical artifact from a structural error in the model.
5. Apply the chapter's audit–fix–verify loop as a discipline rather than an ad-hoc debugging session.

## The task

The book's specification, from Chapter 7's exercises:

> Building a production-quality $SIR_I$ simulator from scratch with a complete verification suite,
> applying the chapter's audit-fix-verify loop to catch the structural errors the chapter identifies.

"From scratch" is meant literally: `src/sir_i_model.py` is the comparison target at the end, not the
starting point. Students who begin by reading it produce a simulator that reproduces its choices,
including any it makes for reasons they have not examined.

## Materials

**Provided in this repository.** `src/sir_i_model.py` as the reference implementation, to be
consulted only after the student's own is passing its suite. `notebooks/ch07/ch7_figures.py` and
`ch7_reporting_lag.py` show the scenarios and outputs the suite must reproduce.
`notebooks/ch06/ch6_phase_portrait.py` supplies the analytical targets to verify against.
`requirements.txt` and `REPRODUCIBILITY.md` pin the environment; byte-reproducibility is part of the
grade, so `SOURCE_DATE_EPOCH` handling is not optional.

**Student-supplied.** The simulator, the verification suite, and the seeded-defect set used to prove
the suite works. No data is required — every verification target is analytical.

**Deliberately not provided.** A test suite to copy, and a list of defects to seed. Deciding what
could go wrong is the substance of the project; being handed the list reduces it to implementation.

## The six steps

1. **Parameter elicitation.** Take the chapter's baseline parameters and, before writing code,
   record what each analytical result predicts for them: $\mathcal{R}_0$, the endemic equilibrium, the final
   size, the peak timing. These are the verification targets, and writing them down first prevents
   the suite being fitted to whatever the simulator happens to produce.
2. **Mathematical analysis.** Derive the quantities the suite will test against, from Chapter 6.
   Include at least one that the simulator does not compute directly, so the test is not a tautology.
3. **Numerical validation.** Implement, then verify: convergence under step refinement, conservation
   of the population total, agreement with the analytical equilibrium, and reproduction of both
   Chapter 7 scenarios. Then seed defects — a sign error in a transfer term, a mis-stated initial
   condition, an off-by-one in the reporting lag — and demonstrate each test fails as intended.
4. **AI-collaborative audit.** Have an AI system review the implementation for structural errors,
   then check its findings against the suite. The instructive case is a defect the AI reports that
   the suite does not catch: that gap is a missing test, and closing it is part of the deliverable.
5. **Disclosure.** Log every interaction, including AI-suggested code that was rejected and why.
6. **Final memo.** The design of the suite, the seeded-defect results, and the audit, written for a
   reader who will maintain this code without having written it.

## Deliverable

Working code with its verification suite, plus a memo of roughly 2,000–3,000 words. The audience is
the next maintainer. A README that lets them run the suite and interpret a failure is part of the
deliverable, not an extra.

Required evidence: a table of seeded defects against which tests caught them, including any that
nothing caught.

## Assessment

Weighting is the instructor's. What follows is what to look for, not what each is worth; courses
differ in how much they weigh working code against the suite that proves it works, and these
materials do not legislate that.

| criterion | what a strong submission shows |
|---|---|
| Correctness of implementation | matches analytical results within a stated tolerance |
| Verification suite design | tests against analysis, not against its own output; covers both scenarios |
| Seeded-defect demonstration | every test shown to fail when its target defect is present |
| Audit-fix-verify discipline | fixes verified rather than assumed; gaps closed with new tests |
| Disclosure completeness | rejected AI code recorded with reasons |
| Maintainability | a new reader can run and interpret the suite |

A suite in which no test has ever been observed to fail should count heavily against a submission,
whatever its coverage. This is the project's central lesson: a gate that cannot fail is
indistinguishable from a gate that passes.

## Notes for instructors

**Scaling.** Grading is heavier here than elsewhere — allow time to run each suite. In a large
class, requiring a fixed seeded-defect set for part of the grade, with student-chosen defects for
the rest, makes comparison tractable while preserving the design exercise.

**Common failure modes.** Tests written against the simulator's own output, which pass forever and
verify nothing. Reading `src/sir_i_model.py` first. Fixing a defect and declaring victory without
re-running the suite. Treating byte-reproducibility as optional and then being unable to explain why
two runs differ.

**Team option.** This project divides well: one student writes the simulator, the other writes the
suite against the analytical targets, and neither sees the other's code until integration. That
structure makes the tests genuinely independent, which is hard to achieve alone. If teams are used,
say who wrote which, and account AI disclosure per person. Teams are offered, not required.
