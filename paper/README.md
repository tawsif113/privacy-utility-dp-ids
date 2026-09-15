# Paper workspace

This directory freezes the paper-preparation state of the project. It is venue-neutral so the
scientific content can be reviewed before adapting it to a publisher template.

## Files

- `manuscript.md` — complete, readable first draft with citation keys.
- `manuscript.tex` — LaTeX version of the same scientific argument.
- `references.bib` — BibTeX records for every citation used in the draft.
- `related_work_evidence.md` — full-text claim audit and corrections to the earlier shortlist.
- `result_inventory.md` — frozen tables, figures, methods, and claim boundaries.

## Build

From this directory:

```bash
pdflatex manuscript.tex
bibtex manuscript
pdflatex manuscript.tex
pdflatex manuscript.tex
```

The draft uses only standard LaTeX packages. Figures are referenced directly from the accepted
result directories; they are not duplicated here.

## Draft status

- Scientific narrative: first complete pass.
- Results: frozen to accepted Experiments 06, 08, and 09.
- Related work: verified against the full texts and official publication pages listed in
  `related_work_evidence.md`.
- Authorship, affiliations, acknowledgements, target venue, page limit, and publisher style:
  intentionally left for author decision.
- New experiments: not required by the frozen roadmap.

## Non-negotiable claim boundary

The paper may report a formal `(epsilon, delta)` DP-SGD guarantee conditional on fixed,
non-private preprocessing. It may not claim that DP-SGD reduced measured overall membership
leakage, that epsilon about 4 is optimal, that the models are immune to stronger attacks, or that
the single-seed UNSW-NB15 result establishes universal generalisation.
