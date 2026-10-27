# Paper workspace

This directory freezes the paper-preparation state of the project. It is venue-neutral so the
scientific content can be reviewed before adapting it to a publisher template.

## Files

- `manuscript.md` — editable manuscript, with methods/evidence revisions dated 2026-10-27.
- `manuscript.tex` — generated LaTeX version of the same scientific argument.
- `references.bib` — BibTeX records for every citation used in the draft.
- `related_work_evidence.md` — full-text claim audit and corrections to the earlier shortlist.
- `result_inventory.md` — frozen tables, figures, methods, and claim boundaries.
- `manuscript_review_2026-10-27.md` — corrections, evidence pointers, decisions, limitations, and open submission gates.

## Build

From the repository root:

```bash
python scripts/validate_manuscript_evidence.py
python scripts/build_manuscript.py --compile
```

The build requires Pandoc, pdflatex, BibTeX, and standard LaTeX packages. Figures are referenced
directly from accepted result directories. Edit Markdown and regenerate LaTeX, rather than editing
both versions. `python scripts/build_manuscript.py --check` detects version drift.
The evidence checker recomputes seed summaries and verifies six delimited manuscript tables;
`--write-tables` refreshes those tables from the frozen CSVs. It never retrains a model.

## Draft status

- Scientific narrative: methods/evidence revision complete; contribution and literature review remain open.
- Results: frozen to accepted Experiments 06, 08, and 09.
- Related work: verified against the full texts and official publication pages listed in
  `related_work_evidence.md`.
- Author: Kazi Md. Tawsif Rahman. Affiliation, declarations, target venue, page limit, and
  publisher style remain for author confirmation.
- New experiments: not required by the frozen roadmap.

## Non-negotiable claim boundary

The paper may report a formal `(epsilon, delta)` DP-SGD guarantee conditional on fixed,
non-private preprocessing. It may not claim that DP-SGD reduced measured overall membership
leakage, that epsilon about 4 is optimal, that the models are immune to stronger attacks, or that
the single-seed UNSW-NB15 result establishes universal generalisation.

