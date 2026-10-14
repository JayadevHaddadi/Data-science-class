# Class 05: Statistical Inference

**Topics:** population vs sample · sampling and sampling distributions · confidence intervals · hypothesis testing · p-values · effect sizes

Everything uses one idea: treat the **518 exam scores** of the Class 03 campus survey as the *whole population*. Because the truth is known, every estimate, interval and test can be checked against it.

## 📂 Files
| Path | Who | Purpose |
|---|---|---|
| `slides/Class05_Statistical_Inference.pptx` | **you** | 16-slide instructor deck, speaker notes on every slide (timing, what to say, questions to ask) |
| `slides/Class05_Whiteboard_Pictures.pptx` | **you** | 8 picture slides to show or redraw on the whiteboard: circles-in-circles, biased vs random dots, narrow vs wide bells, nets, tail areas, a Venn of the two error types, overlapping bells for effect size. Built by `scripts/build_whiteboard_deck.py` |
| `notebooks/05_STUDENT_group_activity.ipynb` | students | 5 groups, task + data + hints only. Students write the code themselves |
| `notebooks/05_INSTRUCTOR_group_activity.ipynb` | **you** | Same + worked solutions (pre-rendered) and questions to ask each group |
| `scripts/build_deck.py` | | Builds the deck (python-pptx). All numbers are computed from the data |
| `scripts/create_activity_notebook.py` | | Builds both activity notebooks (reuses `nbtools.py` from Class 03) |

## ⏱️ Using the deck
Slides stand alone, so you can stop anywhere.

| Slides | Topic | ≈ min |
|---|---|---|
| 2–4 | Population vs sample, sampling bias | 8 |
| 5–6 | Sampling distribution, standard error | 12 |
| 7–8 | Confidence intervals | 12 |
| 9–12 | Hypothesis tests, p-values, error types | 15 |
| 13–15 | Effect sizes, reporting, mistakes | 10 |
| 16 | Hand out the group activity | 5 |

**Only ~20 min left after the presentations?** Do slides 2, 5, 7 and 9, then hand out the activity.

## 🔧 Rebuild
```bash
cd class_05_statistical_inference/scripts
python build_deck.py                   # deck
python create_activity_notebook.py     # notebooks
```
Edit the scripts, not the generated files.

## 🎯 Planted facts (answer key)
| Fact | Where |
|---|---|
| μ = 64.9, σ = 12.2 (518 scores) | everywhere |
| SE at n = 5 / 30 / 100 / 400 ≈ 5.5 / 2.2 / 1.2 / 0.6 | slide 6, group 2 |
| Heavy job (> 15 h) vs none: 58.4 vs 67.2, gap 8.8, t ≈ 5.9, p ≈ 1.6e-8, d ≈ 0.73 | slides 10, 13, 14, group 4 and 5 |
| Hostel vs Home: gap 0.2, p ≈ 0.85, d ≈ 0.02 | slide 13, group 4 and 5 |
| Keenest 40 students average ≈ 60 vs truth 64.9 (biased sample) | group 1 |
