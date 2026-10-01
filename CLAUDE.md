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
