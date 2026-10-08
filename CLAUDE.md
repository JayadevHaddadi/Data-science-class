# Instructions for AI agents working in this repo

## Always push after every change
This repo has a remote (`origin`, GitHub). After **every** change you make here (new/edited notebooks, datasets,
scripts, docs), do all three, without waiting to be asked:

1. `git add` the relevant files (never add stray files such as `* copy.ipynb` or scratch output)
2. `git commit` with a clear message
3. `git push origin main`

If the push fails, tell the user why instead of silently leaving work unpushed.

## Notebook conventions
- Class 03 notebooks are generated from `class_03_eda_deep_dive/scripts/` — edit the generator scripts, not the
  `.ipynb` files, then rebuild (commands in that class's README) and commit both.
- Instructor notebooks (`*INSTRUCTOR*`) contain answers and must never be shared with students.
- The repo is private; student notebooks embed their data so they run in Colab without downloads.

## Exercise design lessons (from teaching feedback)
- **Do not pre-build the analysis in student exercises.** Feedback after Class 03: the solo and especially the team notebook
  had too much already done (full working plots, tables and bucket code), so students mostly pressed "run" and then presented
  the starter output. For future solo/team notebooks: give only the mission, the dataset, a short list of *tools/hints*
  (function names, not working code), and empty cells. Students write the plots/aggregations themselves.
  Keep fully-worked code in the INSTRUCTOR copy only.
- Team notebooks may be assigned as homework, so each mission must still be completable alone from the hints.
- Always provide an instructor question bank (what to ask after each pitch) next to the guide.
