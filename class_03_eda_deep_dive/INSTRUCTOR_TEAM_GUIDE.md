# 🎤 Instructor Guide: Team Missions (Class 03)

**Format**: 5 teams × (11 min work + 45 s pitch). You are the **stakeholder**; push back like a real one.
**Exact numbers**: see `notebooks/04_INSTRUCTOR_team_answers.ipynb` (computed live from the data).
**Scoring**: 🔍 finding correct (40 %) · 🧠 checked an alternative explanation (30 %) · 🎯 concrete recommendation (30 %)

---

## 🛌 Team 1 — The Sleep Cliff (Head of Student Health)
**Truth**: a *cliff* below ~6 h. Students under 6 h (~22 %) average ~61 vs ~66 for the rest; under 5.5 h the gap is ~8 pts. More than 6 h adds almost nothing. Overall r ≈ 0.18 *understates* it because it's a threshold, not a line.
**Ask them**
1. "r is only 0.18, why do you call this important?" → *r measures straight-line fit; the damage is concentrated in one group.*
2. "Could job hours or commuting explain both bad sleep and low scores?" → *Yes, short-sleepers include overworked students; association, not proof.*
**Stakeholder objection**: "A campaign costs money. How many students would it actually reach?" → ~22 %.
**Teacher summary**: *"A weak correlation can hide a strong threshold effect. Bin the variable and look."*

## 😰 Team 2 — The Stress Sweet Spot (Counselling Director)
**Truth**: **inverted U.** Scores peak at stress ≈5–6 (≈70), fall to ≈55 at 8–9 and ≈47 above 9. Lowest-stress band (≤2) is also low (≈50) but **n = 16**. Pearson r ≈ −0.17 hides the shape.
**Ask them**
1. "Pearson says weak. Why isn't stress irrelevant?" → *non-linear, r only sees straight lines (Anscombe II!).*
2. "Does your chart prove low stress *causes* low scores?" → *No; tiny n, maybe disengaged students.*
**Stakeholder objection**: "So I should *raise* students' stress?" → *No — moderate stress is normal; intervene at ≥ 8.*
**Teacher summary**: *"Plot before you correlate. And look at the counts behind every average."*

## 💼 Team 3 — The Working Student (Dean of Student Finance)
**Truth**: no real harm up to ~15 h/week; above 15 h scores fall ≈9 pts (≈58 vs ≈67), more above ~22 h. ~21 % of students are in the >15 h group. Pattern holds in **every** program. Heavy workers also sleep less (≈6.2 vs 6.9 h).
**Ask them**
1. "Is it 'having a job' or 'too many hours'?" → *hours; 1–15 h looks fine.*
2. "Did you check the pattern within each program?" → *yes, pivot table; holds in all four.*
**Stakeholder objection**: "Many students need the money. Cap at what number?" → *~15 h, and why.*
**Teacher summary**: *"A bimodal variable (0 vs working) hides a threshold. Bucket it and compare."*

## ☕ Team 4 — The Coffee Myth (Café Manager & Wellness)
**Truth**: overall r ≈ −0.34, but inside each program r ≈ −0.03 ≈ 0. Engineering drinks the most (≈2.9 cups) and scores lowest (≈55) because of the **program**, not coffee. A **confounder**.
**Ask them**
1. "What changed when you coloured by program?" → *slopes went flat.*
2. "Does that prove coffee is harmless?" → *No — observational data; it shows no *evidence* of harm after accounting for program.*
**Stakeholder objection**: "So I keep selling espresso?" → *Yes; don't run an anti-coffee campaign; maybe study sleep instead.*
**Teacher summary**: *"Same trick as Simpson in Part 3 — always compare **within** groups before blaming a variable."*

## 🕳️ Team 5 — Who Didn't Answer? (Survey Office)
**Truth**: 9–10 % of sleep answers are missing, but **not randomly**: ≈3 % for non-workers vs 15–19 % for working students → sleep results under-represent busy students (likely **understating** sleep problems). The 3 "grinders" (55–61 h, stress 9.6, mid-70s scores) and the Design student (2 h, 96.5) are internally consistent → **keep and flag**.
**Ask them**
1. "Why not fill the blanks with the average?" → *it hides the bias and shrinks variance.*
2. "How do you know the 58-hour student isn't a typo?" → *stress 9.6, other columns coherent, three similar cases.*
**Stakeholder objection**: "I need one number for the board — what is average sleep?" → *Report it with the caveat that busy students are missing.*
**Teacher summary**: *"The pattern of missing data is itself a finding. Outliers are questions, not verdicts."*

---

## 🏆 Closing script (≈60 s)
1. Pick a winner: "the team that tied their chart to a decision."
2. Four laws of EDA: **look first · outlier ≠ error · correlation isn't causation · always ask 'who are the groups?'**
3. "Nobody pays you to write `sns.histplot`. They pay you to find what's weird and tell humans what to do."
