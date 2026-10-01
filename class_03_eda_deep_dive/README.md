# Class 03: EDA Deep Dive — "Campus Wellbeing Survey" (Online)

An interactive, online-friendly session on **distributions, anomalies, relationships, grouping and correlation**,
built around one synthetic dataset (520 students, 4 programs) with deliberately planted patterns.

## 🎯 Topics Covered
- Anscombe's quartet: why summary numbers lie
- Distribution shape: bimodal (job hours), right-skewed (commute), mixtures hidden in a skew
- Anomaly detection: duplicates, label chaos, impossible values, sentinel codes (999), missingness patterns, real vs fake outliers
- Relationships: correlation heatmap, scatter plots, correlation ≠ causation, non-linear patterns
- Grouping: `groupby`, colour-by-group, **Simpson's paradox**, confounding

## 📂 Files
| Path | Purpose |
|---|---|
| `CLASS_LESSON_PLAN.md` | Minute-by-minute online plan, platform advice, checklist, cut list |
| `INSTRUCTOR_TEAM_GUIDE.md` | Pitch grilling guide for the 5 team missions |
| `notebooks/01_INSTRUCTOR_live_class.ipynb` | **Your master notebook** (talking points inside, pre-rendered) |
| `notebooks/02_STUDENT_follow_along.ipynb` | Students' copy of the live session |
| `notebooks/03_STUDENT_solo_data_detective.ipynb` + `03_INSTRUCTOR_solo_solutions.ipynb` | Individual raw-data cleaning exercise + answer key |
| `notebooks/04_STUDENT_team_mission.ipynb` + `04_INSTRUCTOR_team_answers.ipynb` | 5 team missions + ground-truth answers |
| `datasets/campus_survey_raw.csv` | Messy file (530 rows) |
| `datasets/campus_survey_clean.csv` | Cleaned file (520 rows) |
| `scripts/` | Generators (`generate_class3_data.py`, `create_live_notebooks.py`, `create_exercise_notebooks.py`, `nbtools.py`) |

All notebooks have the data **embedded** — they run in Colab with zero setup (the repo is private).

## 🔧 Rebuilding
```bash
cd class_03_eda_deep_dive/scripts
python generate_class3_data.py            # regenerate CSVs
python create_live_notebooks.py           # notebooks 01 + 02
python create_exercise_notebooks.py       # notebooks 03 + 04
```
Edit the `*.py` generators, not the `.ipynb` files, and rebuild.

## 🧬 Planted patterns (answer key)
| Pattern | Where |
|---|---|
| Simpson's paradox: study vs exam is negative overall (r ≈ −0.38), positive within each program | Live Part 3 |
| Stress vs exam is an inverted U (r ≈ −0.17) | Team 2 |
| Sleep < 6 h and job > 15 h/week hurt exam score | Teams 1 and 3 |
| Coffee has no effect, but looks harmful because Engineering drinks most | Team 4 |
| Sleep missing far more for working students; 4 real outliers | Team 5 |
| 14 data-quality problems in the raw file | Solo task |
