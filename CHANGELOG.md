# Changelog

Notable changes to this companion repository. This is a reader-facing log; it
does not track the book manuscript.

## [2026-08-15]

### Added
- `capstone-projects/` — the book's nine chapter capstone projects, one
  directory per project with the six-step workflow specification skeleton;
  detailed materials follow as they are finalized.
- `code/python/ch10_sensitivity/` — the Chapter 10 sensitivity module
  (`ch10_index_divergence.py`, `ch10_sobol_panel.py`).
- `notebooks/README.md` (per-chapter code index) and `notebooks/ch03/` (the
  Chapter 3 transmission-comparison script, moved from `notebooks/ch02/`).
- `.gitattributes` (release-archive hygiene).

### Changed
- All per-chapter scripts and `src/sir_i_model.py` refreshed to the book's
  current baseline (contact-rate parameterization c_S=20, c_I=4, beta=0.040);
  the previous copies predated it and reproduced superseded numbers.
- Chapter directories now follow the book's current chapter numbering
  (`notebooks/ch02/` → `notebooks/ch03/`; a pointer README remains at `ch02/`).
- Entry pages: capstone and module links, reproducibility-conventions link,
  repository-history link, and an absolute issues link.

## [Unreleased]

### Added
- Initial repository: per-chapter figure-reproduction scripts
  (`notebooks/ch06`–`ch11`), the shared `src/sir_i_model.py` model, and the
  companion site.
- Data provenance and pointers (`data/`), including the WSU 2009 H1N1 dataset via
  the MIDAS Network catalog.
- Citation metadata (`CITATION.cff`) and issue templates for corrections,
  questions, and suggestions.

### Pending
- Narrated teaching notebooks and the guided lab set (`labs/`).
- ISBN and a Zenodo DOI for this repository.
- Link to the published book (pending permission from Springer).
