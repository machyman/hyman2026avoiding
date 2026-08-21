# Capstone: Re-analysis of a published COVID-19 $\mathcal{R}_0$ estimate

## At a glance

| | |
|---|---|
| Chapter | 17 — COVID-19: A Case Study |
| Effort | about 15–25 hours over 3–4 weeks |
| Tier | term project — the student analyses a disease and defends a corrected conclusion about it |
| Deliverable | a corrected $\mathcal{R}_0$ or $\mathcal{R}_e(t)$ estimate with quantified uncertainty, and a documented critique of the original |

The only project in the catalog whose subject is a published paper. It is the closest thing the
book offers to the reviewing that professional practice actually consists of, and students
consistently report it as the one that changed how they read literature.

## Prerequisites

Chapter 17 worked through, in particular §17.3 (Model Formulation), §17.4 (Parameter Estimation and
Fitting) and §17.7 (Lessons from the COVID-19 Case Study). §17.2 supplies the epidemiological
context needed to judge whether an original analysis's assumptions were reasonable *at the time it
was written* — a distinction objective 4 depends on. Chapters 8 and 9 are hard prerequisites.

Moderate programming.

## Learning objectives

By the end, the student can:

1. Read a published modeling paper closely enough to reconstruct what it actually did, as distinct
   from what it reported.
2. Identify methodological issues in a published estimate using the infected-viewpoint framework.
3. Produce a corrected estimate with uncertainty that is honest about what the original data
   supports.
4. Distinguish an error from a defensible choice made under the information available at the time.
5. Write a critique that a competent author would recognize as fair.

## The task

The book's specification, from Chapter 17's exercises:

> Re-analyzing a published $\mathcal{R}_0$ or $\mathcal{R}_e(t)$ estimate from the COVID-19 literature using the book's
> infected-viewpoint framework, identifying any methodological issues in the original analysis, and
> producing a corrected estimate with quantified uncertainty.

Early-2020 papers are the richest source, because they were written under genuine uncertainty with
incomplete data and short series. That is also why objective 4 carries real weight: a paper that made
a reasonable choice in February 2020 with the data then available has not made an error, and grading
rewards students who can tell the difference.

## Materials

**No chapter-specific code ships in this repository for Chapter 17.** Recorded plainly rather than
implied: every printed repository path must resolve, and this one would not.

**Provided in this repository.** `src/sir_i_model.py` for the forward model.
`notebooks/ch08/ch8_preprocessing.py` for surveillance preprocessing, which is where a large share of
the methodological issues in this literature actually live. `notebooks/ch08/ch8_influenza_fit.py`
as the fitting pattern. `notebooks/ch09/ch9_figures.py` for bootstrap and profile-likelihood
machinery, which is the most direct route to the uncertainty quantification this project requires.
`notebooks/ch07/ch7_reporting_lag.py` treats reporting delay, a recurring defect in early estimates.
`requirements.txt` and `REPRODUCIBILITY.md`.

**Student-supplied.** The published paper, and the incidence data. **No epidemiological data is
redistributed here.** Where the original paper's data is available, use it — a re-analysis on
different data is a different study, and that distinction should be stated explicitly if the original
data cannot be obtained. National public-health agencies and the archived JHU CSSE repository are the
usual sources.

**Deliberately not provided.** A list of papers with known defects. Selecting a paper and forming an
independent judgement is the project; a curated list of flawed papers converts it into confirmation.

## The six steps

1. **Parameter elicitation.** Reconstruct the original analysis: its model, its parameters, what was
   fitted, what was fixed, and what data over what window. Much of this will be under-reported, and
   recording what *cannot* be determined from the paper is itself a finding — often the most
   important one.
2. **Mathematical analysis.** Re-derive the original's $\mathcal{R}_0$ or $\mathcal{R}_e(t)$ within the infected-viewpoint
   framework. Where the original's definition differs from the book's, establish whether the
   difference is substantive or notational before calling it an error. Several apparent errors in
   this literature are definitional.
3. **Numerical validation.** Reproduce the original's estimate as closely as the reporting allows —
   this is the check that the reconstruction is right — then produce the corrected estimate with
   uncertainty. Report both, and the gap between them.
4. **AI-collaborative audit.** Ask an AI system to critique both the original and the re-analysis.
   Two distinct failure modes are worth recording: confident assertions about a paper it has not
   read, and defects in the student's own re-analysis. The second is the useful output; the first is
   the chapter's lesson.
5. **Disclosure.** Log every interaction, particularly any claim about the original paper that had
   to be verified against the paper itself.
6. **Final memo.** The critique and the corrected estimate, written as a fair-minded review.

## Deliverable

A memo of roughly 3,000–4,500 words. The audience is the original authors: the critique should be
one a competent author would concede rather than dispute on grounds of fairness. That framing is the
grading standard for objective 5, and it is a demanding one.

Required: a reconstruction of the original method with gaps identified; the original and corrected
estimates side by side with uncertainty; and an explicit separation of errors from defensible
contemporaneous choices.

## Assessment

Weighting is the instructor's. What follows is what to look for, not what each is worth; courses
differ in how much they weigh the sharpness of the critique against the fairness of it, and these
materials do not legislate that.

| criterion | what a strong submission shows |
|---|---|
| Reconstruction of the original | accurate; under-reported elements identified rather than assumed |
| Methodological critique | issues real and substantive; definitional differences not miscalled as errors |
| Corrected estimate | defensible, with uncertainty quantified by a stated method |
| Fairness | contemporaneous choices distinguished from errors |
| Disclosure completeness | AI claims about the paper verified against the paper |
| Memo quality | reads as a review the authors could accept |

Fairness carries more weight here than elsewhere. Reporting a definitional difference as an error is
the single most common failure in this project, and the chapter warns about it directly.

## Notes for instructors

**Scaling.** Requiring paper selection to be approved in week one prevents students choosing papers
too under-reported to reconstruct, which is the main cause of stalled projects here. Two students on
the same paper independently, compared at the end, is an unusually strong final session — the
disagreements are more instructive than the agreements.

**Common failure modes.** Critiquing what the paper reported rather than what it did. Calling a
definitional difference an error. Re-analyzing on different data without saying so. Judging a
February 2020 paper by what was known in 2022. Accepting an AI's characterization of a paper it has
not read — the disclosure log is designed to catch this and instructors should read it.

**Team option.** Best run individually, since the critique is a judgement and shared judgements
converge early. Where teams are used, the strongest structure is independent re-analysis followed by
reconciliation, with disagreements documented rather than resolved. AI disclosure is per person.
Teams are offered, not required, and here the default of one student is the recommendation.
