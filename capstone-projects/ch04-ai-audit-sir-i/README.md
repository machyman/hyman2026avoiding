# Capstone: Audit an AI's exposition of the SIR_I model

## At a glance

| | |
|---|---|
| Chapter | 4 — The Force from Infection: Infected Viewpoint |
| Effort | about 6–10 hours over 1–2 weeks |
| Tier | chapter project — the student demonstrates a technique rather than analyzing a disease |
| Deliverable | a corrected exposition, with an audit log of every defect found |

The shortest project in the catalog, and a good first one: it needs no data, no fitting and no
implementation, so it can run in week two or three of a semester while the modeling machinery is
still being assembled.

## Prerequisites

Chapter 4 worked through, in particular the susceptible and infected viewpoints and the formal
equivalence between them. Chapter 3's force-of-infection treatment is assumed. No programming is
required.

## Learning objectives

By the end a student can:

1. State the operational definition of the force of infection from either viewpoint, and say which
   quantity a given expression is measuring.
2. Detect symbol overloading — the same symbol standing for different quantities within one
   derivation — in text they did not write.
3. Distinguish a definitional error from a notational shortcut, and say why the distinction matters
   for what a model predicts.
4. Correct a flawed exposition without importing the flaw into the correction.
5. Record where an AI system's account was right, wrong, and unfalsifiable as written.

## The task

From Chapter 4's exercises:

> Prompt an AI system to explain the SIR model, the basic reproductive number R₀, and the
> operational meaning of the force of infection; audit the response against the chapter's framework,
> identifying every conflation, omission, and definitional drift; and produce a corrected exposition.

The chapter's own audit exercise, immediately preceding, practises the habit on a published-style
derivation where the overloading is already known. This project removes that safety net.

## Materials

Provided here: an audit log template, and the chapter's checklist of definitional
distinctions in a form that can be worked down.

Student-supplied: the AI transcript. Any current system is acceptable. The transcript is part of the
deliverable — an audit whose subject cannot be inspected cannot be assessed.

Deliberately not provided: a worked example of a completed audit. Seeing one first collapses the
exercise into pattern-matching.

## The six steps

1. **Parameter elicitation** — not a fitting project. The elicitation here is of *definitions*:
   before prompting, write down what the force of infection, R₀ and the transmission rate each mean,
   with units. This is the standard the audit will be conducted against, and fixing it in advance is
   what stops the AI's framing from becoming the student's.
2. **Mathematical analysis** — derive R₀ from both viewpoints and confirm they agree. A student who
   cannot do this cannot audit someone else doing it.
3. **Numerical validation** — light. Where the transcript makes a quantitative claim, check it
   arithmetically. Most will not be checkable, which is itself a finding worth recording.
4. **AI-collaborative audit** — the project's substance. Work the transcript line by line against
   the definitional standard from step 1. Classify each defect: conflation, omission, definitional
   drift, or unfalsifiable as written. That last category matters most and is the one students miss.
5. **Disclosure** — the full transcript, the prompts, the system and date. If an AI was also used to
   help write the audit, that is disclosed separately.
6. **Final memo** — the corrected exposition, written for a reader who has not seen the transcript.

## Deliverable

Three to five pages plus the transcript as an appendix. The audience is a student one course behind
the author. The corrected exposition must stand on its own; a reader should not need the flawed
original to follow it.

## Assessment

Weighting is the instructor's. What follows is what to look for, not what each is worth; courses
differ in how much they weigh the quality of the audit against the quality of the correction that
follows it, and these materials do not legislate that.

| criterion | what a strong submission shows |
|---|---|
| Definitional standard (step 1) | units stated, distinctions drawn before the transcript is read |
| Defects found | classified rather than listed; unfalsifiable claims identified |
| Correctness of the correction | the corrected text is right, and imports no new errors |
| Disclosure | complete and honest, including the student's own AI use |
| Writing | stands alone for the stated audience |

Recording *no* defects is not a failing verdict if the audit is thorough and the reasoning is sound.
Some current systems handle this material well. An audit that manufactures defects to fill a quota
is the worse error, and should be marked as such.

## Notes for instructors

**Scaling.** Works from eight students to sixty. Because each transcript differs, submissions do not
converge, and the marking load is bounded by the page limit rather than by class size.

**Common failure modes.** Students accept the AI's framing and audit within it — step 1 exists to
prevent this and should be collected separately before step 4. Students also treat fluency as
correctness, and confidently-worded material draws fewer flags than hedged material.

**Team option.** This project runs well individually and does not need a team. If teams are used,
the natural split is one transcript per member with a joint corrected exposition, which surfaces
disagreements about what counts as a defect. Each member's AI use is disclosed separately.

Back to the [capstone index](../README.md) · [template](../TEMPLATE.md).
