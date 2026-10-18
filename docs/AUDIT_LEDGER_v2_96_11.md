# Claim audit ledger, draft v2_96_11

This ledger lists corrections made to printed claims during the 2026 pre-publication audit of the manuscript. Each claim was checked against its own sources, the book's equations, or a recomputation with the book's own models and code. Each row is a finding the authors ruled on, with the version of the draft in which the correction landed. The current draft is v2_96_11. Wording-only style fixes, such as dashes and punctuation, are not listed.

Chapter and section numbers are those of the printed book. Values are given as the check measured them.

## Printed Chapters 10, 11, 12, 17, 19 and 20 (RG-200, landed v2_91_0)

| ID | Where | What the earlier draft said or did | What the check found | Correction (as ruled) |
|---|---|---|---|---|
| RG-200.1 | Ch 11, Sections 11.7 and 11.8, summary item 5 | Gave a proportional-mixing herd-immunity formula attributed to Anderson and May (1985), with a threshold of 0.614, above the uniform 0.575. | The formula is not in the cited paper and contradicts the section's own uniform result. At 0.614 the case study still has Re = 0.909. Coverage weighted by contact rate needs a total of 0.379, less than uniform. | Replaced by contact-weighted coverage: 0.38 on the case study, between the uniform 0.575 and the cheapest allocation's 0.19, with a closed form under proportionate mixing. The citation moved to the minimum-total paragraph, which the paper supports; summary item 5 follows. |
| RG-200.2 | Ch 20 text and Figs. 20.1 and 20.2; Ch 19 Scenario 1 and summary | Chapter 20 used HIV's additive total: R0 1.70, condoms 0.91, ART 0.17, population average 0.45, sensitivity weights 0.93 and 0.07. Chapter 19's Scenario 1 used 0.012 for the vertical term. | Chapter 19 makes the spectral radius rho(K) the threshold quantity. Under it the values are 1.64, 0.85, 0.16 and 0.44, the weights 0.96 and 0.04, and the vertical term 0.008. No scenario changes side of 1. | rho(K) used throughout Chapters 19 and 20, in the text and both figures. Scenario 1 uses 0.008. Chapter 19's summary gives the vertical share as 4 percent, its weight under rho(K). |
| RG-200.3 | Ch 10, Section 10.2, SIRS endemic formula | Presented the formula with "one finds", without saying when it holds. | It is exact only for equal contact rates. With the book's rates it falls short by 0.27, 1.33 and 2.60 percent for mean immunity of 5 years, 1 year and 180 days. | Stated for equal contact rates, with a note that with the book's rates it is within 3 percent. |
| RG-200.4 | Ch 12, gonorrhea case study; Ch 19, delta-method interval | Chapter 12 printed 0.0621/0.018 as 3.46 and a treated value of 0.42. Chapter 19 printed the interval [0.97, 2.31]. | The division gives 3.45, and the treated value is 0.41 at the unrounded removal rate. 1.64 times (1 plus or minus 1.96 x 0.211) is [0.96, 2.32]. | 3.45 and 0.41 in Chapter 12; [0.96, 2.32] in Chapter 19. |
| RG-200.5 | Ch 17, growth equation; Ch 10, Section 10.3 | Chapter 17 wrote the growth equation with r and a capital I, the only such use in the book. Chapter 10 repeated Section 5.3's next-generation calculation without saying so. | A notation left over from a symbol change, and an unmarked overlap. | The growth rate is written sigma with the book's prevalence symbol. Section 10.3 gains one back-reference to Section 5.3. |

## Printed Chapters 1 and 2, and the end-of-chapter exercise notes (RG-209, landed v2_93_3)

| ID | Where | What the earlier draft said or did | What the check found | Correction (as ruled) |
|---|---|---|---|---|
| RG-209.2 | Ch 1, Section 1.4.3, lab exercise | Compared the linear and exact transmission probability only at the baseline, where R0 runs from 4.6 to 24, and asked for the final size 1 - S(infinity)/N. | The epidemics saturate there, which hides the difference. With births and deaths S(infinity) is the endemic level, not a final size. At a matched R0 of about 1.92 the linear form overstates peak prevalence by 13, 40 and 93 percent. | Asks for the size of the first wave, and adds a repeat of the comparison with R0 matched to about 1.92. |
| RG-209.3 | Ch 1, Section 1.7, Ex. 7(a) | Called lambda an aggregate quantity in people per unit time. | The book's Section 3.4 defines lambda per susceptible; lambda S is the aggregate. | Rewritten: lambda S = alpha I is the aggregate rate, and the reader states the units of lambda. |
| RG-209.4 | End-of-chapter note on section-level exercises, in printed Chapters 1, 3, 4, 7, 13, 14, 15, 18, 19 and 20 | Each note gave a count and list of the exercise sets above it. | The count or the list was wrong in 10 of 17 chapters, because sets were added after the notes were written. | Each note regenerated from the actual sets, with an automated check so a new set cannot leave a note stale. |
| RG-209.5 | Ch 2, Section 2.4, Ex. 1 | Used a per-minute rate rho = 0.05. | At that rate every listed contact duration overstates beta by more than 10 percent (the threshold is 3.9 minutes), so the question has no contrast. | rho = 0.005 per minute: errors of 1.3 to 33 percent, crossing between 30 and 60 minutes. |

## Printed Chapter 5 (RG-211, landed v2_94_0)

| ID | Where | What the earlier draft said or did | What the check found | Correction (as ruled) |
|---|---|---|---|---|
| RG-211.1 | Section 5.6, proof of Theorem 5.5 (general case) | The Routh-Hurwitz argument used printed coefficients a2 and a3 and an inequality (iii), A*B* + gamma_R C* > 0. | The printed a2 and a3 are not the coefficients of the characteristic polynomial, and (iii) is false: -4.47 x 10^-7 at the baseline, and negative in 2,651 of 17,293 random parameter sets with R0 > 1. The theorem itself holds. | Coefficients corrected; (iii) replaced by C* < 0, which the section already shows; a corrected factorization of a1 a2 - a3. Checked symbolically and against a numerical Jacobian of the book's model. |
| RG-211.2 | Section 5.8, Ex. 6 | Asked the reader to show that the false inequality (iii) holds. | Follows from RG-211.1. | The reader verifies the corrected coefficients, then evaluates the quantity at the baseline and finds it negative: a lesson in checking a lemma numerically. |
| RG-211.3 | Section 5.6, equal-contact case, Jacobian | Printed the (2,1) entry of the Jacobian incorrectly. | The entry is nu_m(R0 - 1). The printed matrix did not give the (correct) polynomial printed below it. | Entry corrected. |

## Printed Chapter 6 (RG-213, landed v2_94_1)

| ID | Where | What the earlier draft said or did | What the check found | Correction (as ruled) |
|---|---|---|---|---|
| RG-213.1 | Section 6.2 | Said a horizon of 10,000 days is enough to come within 10^-5 of equilibrium. | The largest deviation is 9.2 x 10^-2 at 10,000 days; the trajectory is within tolerance only after 60,000 days, because the recurrent epidemics damp slowly. | Says more than 60,000 days are needed and points to the closed form as the efficient check. |
| RG-213.2 | Section 6.9, Ex. 2 | Said two forms agree to within 3 x 10^-13. | Contradicts Section 6.5; measured 1.7 x 10^-16 and 8.9 x 10^-16. | "Agree to round-off (about 10^-16)". |
| RG-213.3 | Section 6.9, Ex. 9(c) | Said prevalence peaks near 0.01 and that default solver tolerances give peak times wrong by 5 to 10 percent. | The peak is 0.174. Default tolerances shift the peak time by 0.14 percent and its height by 0.42 percent. | Peak about 0.17; default tolerances differ in the third significant figure, enough to fail a four-digit comparison. |
| RG-213.4 | Section 6.9, Ex. 8, bug 3 | A step size of 5 days, described as longer than tau_R. | tau_R is 12 days. At 5 days Euler's method stays positive; at 15 days a component goes negative. | Step size of 15 days. |
| RG-213.5 | Section 6.2, AI Lab box, step 3; Section 6.9, Ex. 8(c) | Checked a simulation against the conservation-law peak and the final size, and said a gap above 1 percent points to a mismatch. | Both are equal-contact results. A correct simulation at the baseline misses them by 20.2 and 5.6 percent. | Checks Re = 1 at the simulated peak and the endemic equilibrium instead, and says the two formulas hold only for equal contact rates. |

## Printed Chapter 7 (RG-215, landed v2_94_2)

| ID | Where | What the earlier draft said or did | What the check found | Correction (as ruled) |
|---|---|---|---|---|
| RG-215.1 | Section 7.3 caution; Fig. 7.5 caption; Section 7.8, Ex. 12(b) | Said that when the generation time is shorter than tau_R*, the exponential-period conversion underestimates R0. | The direction is reversed. The book's own Section 15.5 example gives 1.46 against the true 1.30, an overestimate. | "Overestimates" in all three places, with the reason stated. |
| RG-215.2 | Section 7.3, worked example | Said three parameter sets give trajectories "not close, but equal to within numerical tolerance" in the growth phase. | Incidence differs by 0.27 percent after 10 days, 1.7 percent after 30 and 12 percent after 60. | Indistinguishable early, separating by about 2 percent after 30 days and 12 percent after 60, where the depletion phase carries information about c_I. |
| RG-215.3 | Section 7.8, Ex. 6(a) | Said endemic prevalence is sensitive to R0 through a factor that diverges as D goes to 0. | The derivative vanishes as D goes to 0, while the elasticity stays near 1.09. | Asks why the derivative vanishes while the relative sensitivity stays of order one. |
| RG-215.4 | Section 7.2, Ex. 2 (and Ex. 3) | Said the companion repository provides a real surveillance dataset. | No such dataset is staged; the chapter's series is synthetic. On 60 days the weekly peak also splits between frequency bins. | Uses the chapter's synthetic series or any public daily series, and tells the reader to trim to whole weeks. |
| RG-215.5 | Section 7.8, Ex. 10 | Asked for residual autocorrelation at lags of 1, 2, 7 and 30 days on weekly data. | Daily lags do not exist in weekly data, and nine points leave almost no pairs at 30 days. | Lags of one, two and four observations (weeks). |

## Printed Chapter 8 (RG-219, landed v2_95_0)

| ID | Where | What the earlier draft said or did | What the check found | Correction (as ruled) |
|---|---|---|---|---|
| RG-219.1 | Section 8.3; Table 8.1; Section 8.5, delay example | Read a generation time of 1.91 days as the data's, giving R0 = 1.37 (2.58 for 3.6 days). The delay example used a growth rate of 0.19 per day and a 44 percent bias. | The chapter's series grows at 0.0761 per day, which gives 1.15, 1.27 and 1.38 for generation times of 1.91, 3.6 and 5 days. The delay bias at that rate is 20 percent. In the model the generation time equals tau_R*, so Table 8.1 set two priors on one quantity. | The text says the data fix the growth rate, not R0, and gives the three values. A note under Table 8.1 says the generation-time row is not a second prior. The delay example uses the series' rate (20 percent), with the 0.19 case kept as a contrast. |
| RG-219.2 | Section 8.2, Ex. 3 | Asked the reader to show that a population-size term in the delta-method interval is nonzero. | Under the consistent conversion the elasticity is 0; for an incidence-only fit it is -0.041 or -0.153, not -1. | The reader shows the term vanishes, then estimates the incidence-only elasticity from the chapter's figure. |
| RG-219.3 | Fig. 8.3 and caption; Section 8.3, AI box | The profile-likelihood figure was drawn from a formula plus noise but captioned as computed on the chapter's series. The box's multistart rule accepted a fit on a parameter bound. | Computed, the profile with tau_R free is flat from 0.1 to 100 seeds. All 20 starts converge to the lower bound on tau_R. | Figure regenerated from the computed profile, with the tau_R penalty in the right panel (about 2.5 to 13 index cases). The box adds that a cluster on a bound is a boundary solution, not an estimate. |
| RG-219.4 | Section 8.5, AI box, structural verification | Its one-line test showed the ascertainment rate rho cancelling even when it changes. | With prevalence built from past reports, the estimate doubles on the day rho doubles and relaxes over about 11 days. | Rewritten: rho cancels only if incidence and prevalence are ascertained by the same factor at the same time. |
| RG-219.5 | Ch 8 exercises | The chapter's 24 exercises printed unnumbered, the only chapter to do so. | A reader could not cite them. | Numbered within each section, as in every other chapter. |
| RG-219.6 (1) | Section 8.1, Ex. 1 | Gave data that imply R0 = 0.75. | The outbreak is declining, which the exercise did not address. | Numbers kept; the exercise asks whether the outbreak is growing and what that says about when the estimate measures R0. |
| RG-219.6 (2) | Section 8.1, Ex. 3 | A population-size range of 15,000 to 30,000. | No crossing occurs in that range. | Range of 10,000 to 40,000, matching the chapter's figure. |
| RG-219.6 (3) | Section 8.2, AI box | Called the delta-method formula exact for separately estimated parameters. | It is a first-order approximation. | "Valid, to first order". |
| RG-219.6 (4) | Section 8.8, Ex. 1 | "The plateau median". | Algorithm 1 uses the mean. | "The plateau mean". |
| RG-219.6 (5) | Section 8.7 and its Ex. 1 | Wrote the stage thresholds as prevalence. | They are cumulative-incidence fractions. | Restated as cumulative incidence (3 to 6 percent; about 75 percent). |

## Printed Chapters 8 and 9 (RG-222, landed v2_96_0)

| ID | Where | What the earlier draft said or did | What the check found | Correction (as ruled) |
|---|---|---|---|---|
| RG-222.1 | Ch 9: Table 9.1, Section 9.3.6, Section 9.7 tables and text, the endemic-prevalence panels of four figures | Classed the contact rates c_S and c_R as negligible for endemic prevalence I*, to be neglected in first-order analyses. | Those are equal-contact results. In the general model their elasticities are +0.52 and -0.52, burden parameters at the chapter's threshold of 0.5. The equal-contact formula is accurate at the baseline only because c_S = c_R there; with c_R = 4, I* is 72 percent higher. | General values in the table, the text and both partition tables; Section 9.3.6's reason restated; the four figure panels regenerated from the general formula. |
| RG-222.2 | Section 9.9, Ex. 1 | Called the estimator asymmetry "the sensitivity-theoretic justification" of the fitting-advantage claim. | The block it cites calls it one half of the argument. | "Only the sensitivity-theoretic half", and the exercise asks for the other half. |
| RG-222.3 | Section 9.9, Ex. 8(b) and (c) | (b) said two estimates should agree; (c) named tau_R and tau_m as acting linearly. | (b) fails for c_S and c_R. tau_m is as curved as c_I, because I* scales as 1/tau_m. | (b) compares c_S and c_R with the general indices; (c) names tau_R and explains tau_m. |
| RG-222.4 | Section 9.8, Check Your Work, check 2 | "If the top ranks change, M was too small." | Fails for ties: c_I, beta and tau_R are tied for R0, and their order never settles as M grows. | Adds an exception for parameters tied within their sampling error. |
| RG-222.5 | Ch 8, Section 8.8, Open Project | "The plateau median". | Algorithm 1 and Section 8.8 Ex. 1 use the mean. | "Mean". |
| RG-222.6 | Ch 8 summary | Wrote the Stage 2 threshold with the prevalence symbol. | Section 8.7 now uses cumulative incidence. | "A cumulative incidence of about 3 to 6 percent". |

## Printed Chapters 9 and 10 (RG-225, landed v2_96_1)

| ID | Where | What the earlier draft said or did | What the check found | Correction (as ruled) |
|---|---|---|---|---|
| RG-225.1 | Ch 10, Section 10.2, Ex. 2 | Asked students to show two endemic equilibria below R0 = 1 (a backward bifurcation) for reinfection factor theta between 0 and 1. The force formula was garbled, and it cited a modeling pathology that appears nowhere in the book. | Impossible for theta at most 1; a scan of 225 cases found no equilibrium below threshold. One appears only for theta above a critical value, about 1.004 (10-year immunity) or 1.013 (1-year) at the baseline. | Restated: show the bifurcation is forward for theta at most 1, then find the critical theta above 1. The stray citation is dropped. |
| RG-225.2 | Ch 10, Section 10.7, Ex. 1 | Asked for "the four ingredients". | The section lists five. | "Five". |
| RG-225.3 | Ch 9, partition schematic, caption | Said c_I and beta sit in the invasion-only region and affect I* only weakly. | The chapter's table classes them as mixed, with an I* index of 1.09. | Unit sensitivity for R0 and about 1.09 for I*: invasion-dominant at this baseline. |
| RG-225.4 | Ch 9, partition schematic, labels | The labels of c_I and beta overlapped, and tau_m's label overlapped "burden". | The labels could not be read. | One shared label for the shared point; class labels moved clear. No data change. |
| RG-225.5 | Ch 10, Section 10.8, Ex. 11(a) | Called the late-time behavior a plateau at the new endemic equilibrium. | After five years prevalence still swings by 33 percent of its mean. | Uses the average over the fifth year, and describes the approach as a damped oscillation. |

## Printed Chapter 11 (RG-227, landed v2_96_2)

| ID | Where | What the earlier draft said or did | What the check found | Correction (as ruled) |
|---|---|---|---|---|
| RG-227.1 | Section 11.2, Eq. 11.4 and the sentence after Eq. 11.5 | Defined each group's contact pool by summing its rates over every group's state. A sentence read "N^c_k is approximately N^c_k". | Read literally, Eq. 11.4 does not reduce to Eq. 11.9: at the disease-free state it gives 0.0940 and 0.0802 per day, where the next-generation form gives 0.300 and 0.120. | The pool is defined pairwise, as the contacts group k directs at group j. Eq. 11.4 then reduces exactly under equal contact rates, and the sentence is corrected. |
| RG-227.2 | Section 11.6; Section 11.9, Ex. 4 | "All three quantities cross the threshold value 1 together." | True of R0 and the cycle number C0, false for the stage numbers. In Ex. 4's example R0 crosses 1 at beta = 0.0341, the stage numbers at 0.0278 and 0.0418. | R0 and C0 cross together; a stage number can sit below 1 while the infection invades. Ex. 4 asks for that range of beta. |
| RG-227.3 | Section 11.9, Ex. 8 | Asked students to verify that the ratio of the two groups' estimates matches the row ratio of the mixing matrix. | Early in an epidemic both groups give the same rate: the simulated ratio is 0.989, against the rows' 2.50. | Asks why the two estimates agree early, and where in the data the mixing matrix does leave a trace. |
| RG-227.4 | Section 11.9, Ex. 3 | "Double the assortativity parameter to 0.6". | The case study's value is 0.35. | "Raise the assortativity parameter to 0.6" (R0 from 2.35 to 2.66). |
| RG-227.5 | Section 11.8 | Said disassortative mixing can make a population-averaged calculation overestimate R0. | The comparison used a plain average. Under balance, with common transmission and removal rates, the size-weighted average never exceeds the true value (a Rayleigh-quotient argument); 20,000 random matrices agree. | States that the averaged rate never overestimates R0 and matches it only when every group makes the same number of contacts. Worked example: 2.00 against 1.60. The convexity sentence is dropped. |
| RG-227.6 | Section 11.3 | Deferred the endemic-equilibrium details to "Exercise 2". | The closed-form equilibrium is Ex. 1. | The reference points to Ex. 1. |
| RG-227.7 | Section 11.1 | Said this chapter extends its techniques to m-group models. | The multigroup extension is in Chapter 12, Section 12.5. | Points to Chapter 12 for sexual transmission and the multigroup model, and to the vector-host chapter. |
| RG-227.8 | Section 11.9, Ex. 7 | Called the assortativity value 0 "proportional mixing". | In the case-study construction only group 1's row is then proportional; balance fixes group 2's. | "Group 1 mixing in proportion to group size". |
| RG-227.9 | Section 11.9, note on the exercises | "Four section-level retrieval exercises appear above." | There are five, and one is a derivation, not retrieval. | "Five section-level exercises appear above". |

## All chapters: the exercise notes (RG-228, landed v2_96_3)

| ID | Where | What the earlier draft said or did | What the check found | Correction (as ruled) |
|---|---|---|---|---|
| RG-228.1 | End-of-chapter note on section-level exercises, 17 chapters | Each note counted exercise sets, not exercises, and called them all "retrieval" exercises. | The reader counts exercises. The count was wrong in about a dozen chapters, and "retrieval" in most. | Each note counts exercises and drops "retrieval", as in Chapter 11. An automated check enforces the rule. |

## Printed Chapter 12 (RG-229, landed v2_96_4)

| ID | Where | What the earlier draft said or did | What the check found | Correction (as ruled) |
|---|---|---|---|---|
| RG-229.1 | Section 12.7, sensitivity to contact rate; summary item 4; Section 12.8, Ex. 4 | Gave an elasticity of R0 to the male-female contact rate of 1/2, so halving contacts cuts R0 by 29 percent, and explained weak behavioral interventions by "square-root dampening". | The chapter's balance equation ties the two directions' contact rates together, so halving contacts halves R0: the elasticity is 1. The 1/2 holds only for one-sided parameters, such as a per-contact probability. | Rewritten: the sensitivity to contact rate is 1, and the square root halves only the sensitivity to one-sided parameters. The summary and Ex. 4 follow. |
| RG-229.2 | Section 12.4.1, reader note; summary item 5 | "All four cross 1 together." | The stage numbers need not. Lowering beta, the female-to-male number falls below 1 while R0 is still above it. | R0 and the cycle number cross together; the stage numbers need not. |
| RG-229.3 | Section 12.4.1, reader note | Gave literature values for untreated gonorrhea without a source, inconsistent with an uncited range in Section 12.4.2. | The two ranges conflict. The chapter's own parameters give 3.3 to 3.5 per generation and 10.8 to 12.0 per cycle. | The note uses the chapter's own numbers (about 3.3 per generation, 11 per cycle). |
| RG-229.4 | Section 12.8, Ex. 3 | Called 0.5 contacts per day "10 times higher" than the general population's rate. | 0.1 per week is 0.014 per day, so 0.5 is 35 times higher. | "About 35 times higher". |
| RG-229.5 | Section 12.7, endemic equilibrium | Applied the equal-beta formula to the case study's unequal beta: 71 percent prevalence in each sex. R0 appeared as both 3.45 and 3.46. | Solving the coupled system gives 68.3 percent of males and 73.7 percent of females. | Says 71 percent would hold with equal beta, and gives about 68 and 74 percent, with R0 = 3.45. |
| RG-229.6 | Section 12.2, force of infection | Defined the susceptible fraction as an approximation for compartment-independent contact rates. | With the pairwise pool adopted in Chapter 11, the equality is exact. | Uses Chapter 11's pairwise pool; the equality is exact for compartment-independent rates. |

## Printed Chapter 13 (RG-231, landed v2_96_5)

| ID | Where | What the earlier draft said or did | What the check found | Correction (as ruled) |
|---|---|---|---|---|
| RG-231.1 | Section 13.6 list and text; Sections 13.4.3 and 13.5.2; Fig. 13.3 caption; summary item 4; Section 13.4, Ex. 1 | Gave the sensitivity of R0 to vector mortality as -1/2, named the biting rate the most sensitive parameter, and called biting-rate reduction the most cost-effective intervention. | The case study puts survival through the extrinsic incubation period into transmission, so mortality enters twice: -1/2(1 + mu_v tau_v^E) = -1.10. Doubling mortality cuts R0 to 1.01; halving the biting rate, to 1.30. A sensitivity does not show cost-effectiveness. | Vector mortality (about -1.1) is the most sensitive parameter, then the biting rate. A sensitivity to the incubation period (about -0.6) is added. The cost-effectiveness claim is removed. |
| RG-231.2 | Section 13.4.1 | "All four quantities cross the threshold 1 together." | At the case study the stage numbers are 15.0 and 0.452: one is below 1 while R0 = 2.6. | R0 and the cycle number cross together; the stage numbers need not. |
| RG-231.3 | Sections 13.4.3 and 13.5.3 | Said that reducing the susceptible and infected exposure weights by the same factor recovers unit sensitivity. | The weights are relative. Halving both leaves R0 unchanged; protecting susceptibles alone raises it by a factor of 1.414. | Only preventing bites, which lowers the biting rate, has unit sensitivity; redirecting bites changes the weights. |
| RG-231.4 | Section 13.7, Ex. 4; Section 13.3 | Asked the reader to show that the explicit incubation compartment and the effective transmission probability give the same R0. | They agree only with exponential-sojourn survival. At the case study they give 3.196 and 2.602. | Ex. 4 states the condition and asks for the difference. Section 13.3 names the survival form it uses. |
| RG-231.5 | Section 13.7, Ex. 11(b) | Said that omitting incubation survival overestimates R0 by 1/p_EIP, about 2. | R0 scales as the square root of p_EIP, so the factor is 1.65. 1/p_EIP = 2.72 applies to the cycle number. | About 1.6 for R0, about 2.7 for the cycle number. |
| RG-231.6 | Section 13.6.2 | Said the case study's per-cycle value of about 6.75 matches published estimates of 5 to 10 for African malaria, without a source. | Smith et al. (2007, PLoS Biology) report estimates from about 1 to over 3,000. | Cites Smith et al. (2007) for that range; the case study sits at its low end. |
| RG-231.7 | Section 13.3, Ex. 1 | Wrote the vector incidence without the probability b_v, and called the rates forces "from" infection. | The section's own equations include b_v and call them forces "of" infection. | b_v added; "force of infection". |
| RG-231.8 | Ch 13 introduction | "MacDonald's refinement". | The name is Macdonald (George Macdonald). | "Macdonald's refinement". |

## Printed Chapter 14 (RG-233, landed v2_96_6)

| ID | Where | What the earlier draft said or did | What the check found | Correction (as ruled) |
|---|---|---|---|---|
| RG-233.1 | Section 14.3; Section 14.4, Ex. 2 hint | The vertical term counted births to mothers infectious at delivery. The hint gave Zika's short infection as the reason its vertical contribution is small. | For a transplacental route the opportunity is being pregnant when infected. That form does not depend on the infectious period and, for Zika, is 39 times the scalar form (0.0014 against 3.5 x 10^-5). Both stay small next to horizontal R0 = 2. | New paragraph on transplacental routes. The hint compares the two forms and says the contribution is small because few infected people are pregnant. |
| RG-233.2 | Section 14.1, Table 14.1, Section 14.4.3, Section 14.4 Ex. 2 | Gave Zika's vertical transmission as 5 to 10 percent; the exercise used 0.30, 0.10 and 0.05. | The chapter's own source, Ades et al. (2021), gives 47, 28 and 25 percent by trimester of exposure, with congenital Zika syndrome in 9, 3 and 1 percent. | About 25 to 47 percent by trimester, cited, and checked against the source. The exercise uses 0.47, 0.28 and 0.25. |
| RG-233.3 | Section 14.6, Ex. 5 (rubella) | Used 0.80 as the transmission probability, which the chapter's note warns against, assumed zero transmission after the first trimester, and gave no birth rate or infectious period. | Inconsistent with the chapter's note and with the late-pregnancy rise it cites. | Restated with its inputs given, both forms of the vertical term, and a question on the note's caveat. |
| RG-233.4 | Section 14.3 | Said tau_R* goes to infinity for chronic carriers. | With background mortality it tends to 1/nu_m = tau_m, as Section 14.6 Ex. 2 uses. | "tau_R* tends to tau_m = 1/nu_m for chronic carriers". |

## Printed Chapter 15 (RG-235, landed v2_96_7)

| ID | Where | What the earlier draft said or did | What the check found | Correction (as ruled) |
|---|---|---|---|---|
| RG-235.1 | Sections 15.4 and 15.5; Eqs. 15.11, 15.12, 15.14 and 15.17 | Wrote the Kermack-McKendrick equation three ways; the form said to reduce to the SIR model had no depletion factor. | Without the factor, incidence grows without limit: in a test case S falls below zero by day 130. With it the final size is 0.4220, against 0.4232 for the SIR model. | The kernel is defined at full susceptibility and the factor S(t)/N added. Section 15.5 gives the linear form as valid while S is close to N. |
| RG-235.2 | Section 15.5, AI box, structural verification | Said a units test and two limit tests each catch a wrong answer. | The integral of the infectiousness A alone passes the units test and both stated limits. | Units catch the integral of the survival F; the fast-recovery limit catches the integral of A. |
| RG-235.3 | Section 15.2, Ex. 1 | Said total population is preserved when there is no mortality. | The total changes at the birth rate B(t); it is constant only with no births as well. | Restated. |
| RG-235.4 | Section 15.2.2 | A cross-reference printed "Exercise 4". | The derivation it points to is Section 15.8, Ex. 1. | Reference corrected. |
| RG-235.5 | Section 15.8, Ex. 3 | "The SARS-CoV-2-like kernel of Section 15.7". | Section 15.7 calibrates the kernel to seasonal influenza. | "The influenza-like kernel". |
| RG-235.6 | Section 15.5, opening | Said the autoregressive coefficients sum to exactly R0, and reused the kernel's symbol for the memory length. | The sum is a Riemann sum of the kernel (1.2997 at a half-day step, against 1.3). | "Approximates R0"; memory length L. |
| RG-235.7 | Section 15.8, Ex. 6 | Left the interval in (c) open, and asked when incidence reaches 100 times its initial value. | (b) starts at zero incidence, so the question is undefined. | (c) is specified; the target is 100 cumulative infections from one index case. |
| RG-235.8 | Section 15.3, Ex. 1 | Asked for Eq. 15.9, which the next section derives. | The answer is printed on the next page. | Asks for the solution by characteristics in both cases. |
| RG-235.9 | Section 15.8, Ex. 2 | Asked for the growth rate as a formula in the birth and death rates. | The rate is fixed only implicitly. At the given values the population shrinks (-0.0051 per year). | Asks for the equation, and whether the population grows or shrinks. |
| RG-235.10 | Section 15.8, Ex. 4(b) | "Deterministic infection at day 5". | Reads as a deterministic infectious period. | "All transmission at day 5". |
| RG-235.11 | Section 15.4.2 | Said the kernel is integrated over the population's distribution of times since infection. | The kernel is per index case; nothing is integrated over a population. | Clause deleted. |
| RG-235.12 | Section 15.8, Ex. 8 | "Vaccination as a boundary term". | Vaccination at age 1 is a jump across age 1, not a condition at age 0. | Restated as a jump across age 1. |
| RG-235.13 | Section 15.8, Ex. 7 | Said the model reduces to the multigroup framework. | Integrating over age bands adds aging between groups, which that chapter does not have. | "With aging between groups as an added flow". |

## Printed Chapter 17 (RG-237, landed v2_96_8)

| ID | Where | What the earlier draft said or did | What the check found | Correction (as ruled) |
|---|---|---|---|---|
| RG-237.1 | Section 17.2, Ex. 1 | Asked why splitting symptomatic and asymptomatic infection matters for R0 in a way averaging would not capture. | At the baseline a single class with the weighted mean contact rate gives the same R0 (2.449 against 2.444). | The reader shows this, then explains why the split still matters for the isolation scenario. |
| RG-237.2 | Section 17.2 | Gave the asymptomatic share as 30 to 50 percent, citing Oran and Topol (2021). | The review concludes that at least a third of infections are asymptomatic; the 50 percent is not theirs. | "At least a third", checked against the paper. |
| RG-237.3 | Section 17.4, delta method | Called the input ranges 95 percent intervals, but divided each half-width by 2; gave tau_R's variance share as 32 percent. | The reading must be stated; the share is 31.3 percent. | States that each half-width is read as two standard deviations; 31 percent. |
| RG-237.4 | End-of-chapter Ex. 3 | Asked the reader to show that p and a are not jointly identifiable from case counts. | True only when the contact rates are fitted too; otherwise p is identifiable in principle. | Adds that condition. |
| RG-237.5 | Section 17.6, Ex. 1 | Did not say whether the scenario changes are relative or absolute. | The two readings give 0.699 and 0.437; both are below 1, so the answer stands. | States the changes as factors. |

## Printed Chapter 18 (RG-239, landed v2_96_9)

| ID | Where | What the earlier draft said or did | What the check found | Correction (as ruled) |
|---|---|---|---|---|
| RG-239.1 | Section 18.5, Scenario 2; Fig. 18.3 caption; Sections 18.4 and 18.6; summary | Said insecticide alone is insufficient and that the biting rate dominates. | The model replaces every mosquito that dies. If emergence is set by larval habitat, abundance falls too: the sensitivity to vector mortality is -1.26, and doubling mortality alone gives R0 = 0.84. | New paragraph on fixed or compensating emergence. The caption, summary and Section 18.4 are qualified: "when emergence replaces killed adults", "when m is held fixed". |
| RG-239.2 | Sections 18.5 and 18.6; summary | Called biting-rate interventions uniquely cost-effective. | Section 18.4 itself says an elasticity does not measure cost. | Largest proportional effect per percent of parameter change, with m held fixed; cost is a separate question. |
| RG-239.3 | Section 18.3, delta method | Labelled the vector-to-host ratio's range one standard deviation but entered it as two; listed the incubation period without a term and used the recovery rate without listing it; upper end 2.95; for a factor-2 range, [0.62, 3.48]. | Upper end 2.96. The section's own reading gives [0.90, 3.35] for a factor-2 range. The conclusion holds. | Inputs relabelled; [1.29, 2.96] and [0.90, 3.35]. |
| RG-239.4 | Section 18.3, Ex. (b) | The back-calculation counted incubation survival twice and equated the force of infection with the per-case ratio. | Section 18.3 gives a different relation. | Uses the section's quasi-equilibrium relation. |
| RG-239.5 | Section 18.3, Ex. (b) and (e) | Referred to "the companion repository's Chapter 16 notebook". | Dengue is printed Chapter 18. | Refers to the chapter's own notebook. |

## Printed Chapter 19 (RG-241, landed v2_96_10)

| ID | Where | What the earlier draft said or did | What the check found | Correction (as ruled) |
|---|---|---|---|---|
| RG-241.1 | Section 19.4, lab (a) and (b) | Predicted that the high- and low-activity per-case ratios differ by about c_H/c_L, and recovered c_H from them. The model left the strata uncoupled. | Once the strata share a growth rate the ratios converge: the female ratio is 0.015, 0.12 and 0.79 in years 1, 5 and 20. The difference shows in prevalence, 12.4 times higher in high-activity females. | The lab predicts convergence and points to prevalence; (b) states that its formula holds for an isolated core. The strata are coupled by random mixing. |
| RG-241.2 | Section 19.2, per-act probabilities | Gave 0.001, 0.0005, and 0.01 to 0.03 for receptive anal exposure, citing Patel et al. (2014). | The paper gives 8, 4 and 138 per 10,000 exposures (95 percent CI 102 to 186 for the last); 0.03 lies outside it. | 0.0008, 0.0004 and about 0.014 (CI 0.010 to 0.019), checked against the paper. |
| RG-241.3 | Section 19.2 | About 39 million people living with HIV in 2023. | The UNAIDS fact sheet gives 39.9 million. | "About 40 million (39.9 million)". |
| RG-241.4 | Section 19.2 | Wrote the infectious lifetime as the sum of two times. | Competing exits add rates: 1/(nu_m + mu_d) is about 9 years, not 61. | 1/(nu_m + mu_d). |
| RG-241.5 | Section 19.5, Scenario 4 | Gave R0 as an additive total, 1.58 + 0.008. | The chapter reports rho(K): 1.585, the same 1.59. | R0 = rho(K), about 1.59. |
| RG-241.6 | End-of-chapter Ex. 4 (PrEP) | Applied PrEP to men's force of infection only, while asking for one threshold. | Men only gives 66.7 percent coverage; both sexes, 40.8 percent. | Applies to both sexes' forces. |

## Printed Chapter 20 (RG-243, landed v2_96_11)

| ID | Where | What the earlier draft said or did | What the check found | Correction (as ruled) |
|---|---|---|---|---|
| RG-243.1 | Section 20.1; Fig. 20.1 caption; Section 20.3 | Said every single intervention leaves R0 near but not below threshold for every pathogen, and that only combinations achieve elimination. Section 20.3 credited ART's 0.16 to a combination. | For HIV, condoms alone (0.85) and ART alone (0.16) are single interventions below threshold. Dengue insecticide alone gives 0.84 if emergence stays fixed. | Restated: the higher the baseline R0, the less one intervention can do. Single measures fall short for COVID-19 and dengue but not for HIV. |
| RG-243.2 | Section 20.3 | Called biting-rate reduction and partnership reduction disproportionately cost-effective. | Elasticities do not measure cost. For HIV, condoms move R0 as far per percent as the partnership rate (0.79 each). | Restated as effect per percent of change; cost is a separate question. |
| RG-243.3 | Section 20.2; Fig. 20.2 row and caption | Called vector mortality burden-facing and sign-dependent, and said c_H acts through a denominator. | Vector mortality is invasion-facing twice and its sign never changes. c_H sits in the numerator of both directions. | Vector mortality invasion-facing twice: -0.760 with m fixed, about -1.26 if emergence stays fixed. The row is relabelled "sign-dependent or reinforcing" and the caption corrected. |
| RG-243.4 | Section 20.5, HIV bullet | Called each estimator a per-target-susceptible force. | J/I is a per-case ratio; J/S would be the force. | "The realized rate of new infections per current case in its stratum". |
| RG-243.5 | Section 20.3, Ex. 1 | Said square-root dampening recurs across COVID-19, dengue and HIV. | The section itself says COVID-19 has no square-root structure. | Limited to dengue and HIV; the exercise asks why it is absent from COVID-19. |
| RG-243.6 | Sections 20.4 and 20.1 | Said c_H exceeds the population average by an order of magnitude, and listed pandemic influenza at R0 about 1.5 among the extremes. | The ratio is 3.6 (10 against the low-activity rate). 1.5 lies inside the stated common range. | "Three and a half times the population average and ten times the low-activity rate"; influenza sits at the low edge of the common range. |

Observations the authors are still weighing are not listed here.
