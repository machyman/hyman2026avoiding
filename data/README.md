# Data

Empirical datasets used in the book's case studies, with provenance. Each data file keeps its own licence, which
may differ from the MIT License that covers this repository's code.

## U.S. mpox, 2022 (Chapter 8)

- [`us_mpox_2022_weekly_cdc.txt`](us_mpox_2022_weekly_cdc.txt): weekly U.S. mpox cases reported to CDC during the
  2022 outbreak, 32 weeks. Two tab-separated columns: the week (week 0 is the first week in the series) and the
  case count. The Windows (CRLF) line endings are kept as in the source.

**Licence: GPL-3.0.** The file is copied unchanged from the GrowthPredict toolbox (Chowell et al. 2024,
*Sci. Rep.* 14, 1630), file `input/Most_Recent_Timeseries_US-CDC.txt` of
<https://github.com/gchowell/forecasting_growthmodels>, which is distributed under the
[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html). It is not covered by this
repository's MIT License. The book's Section 8.8 and the bootstrap lab of Section 8.2.1 use it, through
[`../figs_src/ch9_benchmarks.py`](../figs_src/ch9_benchmarks.py).

## WSU 2009 H1N1 (Chapters 7–8)

The Washington State University 2009 H1N1 outbreak dataset is **freely available
from the MIDAS Network data catalog** at <https://catalog.midasnetwork.us>. It is
not redistributed here — please download it from the original source, which
carries the authoritative provenance and terms of use.

Additional case-study datasets will be added as the corresponding chapters are
finalized. The book is currently under review.
