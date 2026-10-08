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

---

# ❓ Question Bank: ask after each pitch (pick 3–4 per team)

Order: **Check** (do they understand their own chart?) → **Challenge** (alternative explanations) → **Decide** (stakeholder pushback) → **Extend** (what would you do next?). Aim the Check questions at the *non-spokesperson* so the whole team has to understand it.

## 🛌 Team 1: Sleep Cliff
- **Check:** "Where exactly does the curve bend? Show me the sleep band where scores start to drop." *(~6 h; below 5.5 h is worst)*
- **Check:** "What did you try as a threshold? Did 5, 6 and 7 hours give different answers?" *(6 separates best; 7 dilutes the gap)*
- **Challenge:** "The correlation is only 0.18. Why should the Health Director care?" *(r = straight-line fit; the damage sits in one group, ~22 % of students)*
- **Challenge:** "Could heavy job hours cause both short sleep and low scores?" *(job >15 h sleep ≈ 6.2 h; yes, a confounder)*
- **Decide:** "Short sleepers average ~5 points lower. Is that worth a campaign for 22 % of students?"
- **Extend:** "Is it sleep *causing* low scores, or is a stressed student sleeping badly *and* studying badly? How would you test it?" *(experiment / track same students over time)*

## 😰 Team 2: Stress Sweet Spot
- **Check:** "Why did you use a curved fit instead of a straight line? What does the straight line miss?"
- **Check:** "At what stress score is average performance highest, and where does it fall off?" *(peak ≈5–6; falls above ~8)*
- **Challenge:** "How many students are in your lowest stress band? Can you trust that average?" *(n ≈ 16; no)*
- **Challenge:** "Does your chart prove stress *causes* lower scores at the high end?" *(no: poor scorers may become stressed: reverse causation)*
- **Decide:** "So should the university try to *reduce everyone's stress to zero*?" *(no, moderate is fine; target ≥ 8)*
- **Extend:** "Would you expect the same curve for every program? How would you check?" *(colour/facet by program)*

## 💼 Team 3: Working Student
- **Check:** "Is the harm from having a job at all, or from working too many hours? Which numbers show that?" *(none 67 vs 9–15 h 66 vs >15 h 58)*
- **Check:** "How did you choose your bucket boundaries? What happens if you move them?"
- **Challenge:** "Did you check the pattern *within* each program, or could one hard program explain it?" *(pivot: holds in all four)*
- **Challenge:** "What else do heavy workers lack that could explain the lower scores?" *(sleep: 6.2 vs 6.9 h)*
- **Decide:** "Many students need the money. Is a 15-hour cap fair? What would you say to a student working 20 h?"
- **Extend:** "55 % of students don't work at all. How does that spike change how you'd report the *average* job hours?" *(mean ≈ 6.8 describes nobody)*

## ☕ Team 4: Coffee Myth
- **Check:** "What happened to the trend line when you coloured by program?" *(flat inside each program)*
- **Check:** "Which program drinks the most coffee, and which scores lowest? Is that a coincidence?" *(Engineering ≈ 2.9 cups, ≈ 55)*
- **Challenge:** "You found no effect inside programs. Does that prove coffee is harmless?" *(no, observational; only shows no evidence of harm)*
- **Challenge:** "Name another situation from today where an overall trend flipped inside the groups." *(Simpson's: study hours)*
- **Decide:** "Café manager: do I keep selling espresso? Should the Wellness Office run a coffee campaign?"
- **Extend:** "What data would you need to claim coffee *does* affect scores?" *(randomised trial, or the same students over time, control for sleep and program)*

## 🕳️ Team 5: Who Didn't Answer?
- **Check:** "Are the missing sleep answers random? Show me the evidence." *(≈3 % no job vs 15–19 % working students)*
- **Check:** "Which of the four extreme students did you keep, and what evidence did you use?" *(stress 9.6 + plausible scores; three similar cases)*
- **Challenge:** "Why not fill the blanks with the average sleep?" *(hides bias; shrinks variance; invents data)*
- **Challenge:** "In which direction does the missing data bias our sleep results?" *(busy students missing → sleep looks better than reality)*
- **Decide:** "Survey Office: I need one number for the board. What do I say average sleep is?"
- **Extend:** "How would you change the survey form to prevent this?" *(optional-question reminders, shorter form, daytime reminders)*

---

## 🎯 Whole-class questions (ask when a team finishes)
1. "Hands up if you **agree** with this team's recommendation. Hands up if you'd **want more evidence**." *(then ask one of the doubters why)*
2. "Which *one* number or chart convinced you most?"
3. "What would **change your mind**?"
4. "Did any team's finding connect to another team's?" *(Team 1 ↔ 3 via sleep; Team 4 ↔ live Simpson; Team 5 ↔ Team 1 via who is missing from sleep data)*

## 🔧 If a team gives a weak answer
- "Show me the chart *you* made, not the starter one."
- "What did you try that **didn't** work?" *(tests whether they explored or copied)*
- "Explain it to someone who doesn't know what a correlation is."
