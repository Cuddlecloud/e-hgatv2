# Equation Context Files

These files transcribe the displayed equations from the three local PDFs provided for the E-HGATv2 literature context.

## Files

- `2023_FSMJ_AGVinCT_equations.md` - full 2023 FSMJ MILP, crowding distance, GD+, spread, normalization, and deviation formulas.
- `2022_Book_Chapter_ContainerTransport_equations.md` - loading, unloading, dual-cycling MILP variants and GAP formulas from the 2022 book chapter.
- `Homayouni_XAI_MOO_equations.md` - confirms the 2-page XAI+MOO note has no displayed equations; lists symbolic objects mentioned in text.
- `overleaf_equations.tex` - combined Overleaf-ready LaTeX document.

## Precision Notes

- The 2023 FSMJ paper had extractable text and rendered pages; equations were cross-checked with both.
- The 2022 book chapter had no extractable text layer; equations were transcribed from rendered page images.
- The 2022 book chapter prints constraint (15) with `e_{ij} \ge 0`, although the model defines total energy as `\mathcal{E}`. The Markdown preserves the printed form and also records the likely intended version.
- A local TeX compiler was not available, but `overleaf_equations.tex` passed a brace-balance check.
