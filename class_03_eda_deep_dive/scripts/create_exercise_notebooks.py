"""Builds the exercise notebooks:

  03_STUDENT_solo_data_detective.ipynb      individual task (raw, messy data)
  03_INSTRUCTOR_solo_solutions.ipynb        same notebook with solutions + answer key
  04_STUDENT_team_mission.ipynb             5 team missions (clean data)
  04_INSTRUCTOR_team_answers.ipynb          solved missions with ground-truth numbers
"""
from nbtools import build, code, md, note, render, save, setup_cell

# ============================================================================
#  SOLO: DATA DETECTIVE
# ============================================================================
S = []
S += [
    md("""
# 🕵️ Solo Task — Data Detective
**Time: 15 minutes · Work alone · Cameras on, mics muted · Type `?` in chat if stuck**

The survey office sent us the **raw** Campus Wellbeing Survey file. Before anyone analyses it, a detective must find
**everything that is wrong** with it. Real data is *always* dirty. At least **10 problems** are hiding in this file.

**Your goals**
1. 🔍 Find as many problems as you can (a scoreboard in chat: *type your count when time is up*).
2. 🧹 Fix them in `df_clean`.
3. ✅ Run the auto-checker until it shows **8/8**.
4. 🧠 Decide what to do with *suspicious but possibly real* students (outliers are **not** the same as errors).
""", "student"),
    md("""
# 🕵️ Solo Task — Data Detective · INSTRUCTOR SOLUTIONS
This is the student notebook with the TODOs filled in, plus the **answer key** at the bottom.
Run order is identical. Students never see this copy.
""", "instr"),
    setup_cell(("raw",)),
    md("## Step 0 · Load the raw file"),
    code('''
raw = load("raw")
print(raw.shape)
raw.head()
'''),
    md("""
## Step 1 · Detective toolkit
| Question | Tool |
|---|---|
| How big? What types? What's missing? | `raw.info()` · `raw.isna().sum()` |
| Any impossible numbers? | `raw.describe()` · `raw.sort_values("col")` · `raw[raw["age"] > 60]` |
| Duplicates? | `raw.duplicated().sum()` · `raw[raw.duplicated(keep=False)]` |
| Messy categories? | `raw["program"].value_counts()` |
| Is missingness random? | `raw.groupby(raw["sleep_hours"].isna())["part_time_job_hours_week"].mean()` |
"""),
    md("## Step 2 · Hunt!  *(each cell is a workspace — edit and re-run freely)*\n### 2a. Numbers that cannot be real"),
    code('''
raw.describe().round(1)
'''),
    code('''
# Which rows have impossible values? Look at the min/max above, then filter. Examples:
raw[raw["age"] > 60]
# Try the same idea for: age < 15, study_hours_week, sleep_hours, exam_score ...
''', "student"),
    code('''
print("--- age outside 15–60 ---")
display(raw[(raw["age"] < 15) | (raw["age"] > 60)])
print("--- study hours > 100 (a week only has 168 hours!) ---")
display(raw[raw["study_hours_week"] > 100])
print("--- sleep < 0 or > 14 ---")
display(raw[(raw["sleep_hours"] < 0) | (raw["sleep_hours"] > 14)])
print("--- exam score > 100 ---")
display(raw[raw["exam_score"] > 100])
''', "instr"),
    md("### 2b. Duplicates"),
    code('''
# How many exact duplicate rows are there?
raw.duplicated().sum()
''', "student"),
    code('''
print("duplicate rows:", raw.duplicated().sum())
raw[raw.duplicated(keep=False)].sort_values("student_id").head(6)
''', "instr"),
    md("### 2c. Messy categories"),
    code('''
raw["program"].value_counts()
'''),
    md("### 2d. Missing values"),
    code('''
raw.isna().sum()
'''),
    md("""
### 2e. Is the missingness *random*? (the real detective question)
If `sleep_hours` is missing for **random** students, we can ignore it. If it's missing for a **specific kind** of student, our analysis is biased.
"""),
    code('''
# Compare the average job hours of students who skipped the sleep question vs. those who answered.
# Hint: raw.groupby(raw["sleep_hours"].isna())["part_time_job_hours_week"].mean()

''', "student"),
    code('''
print(raw.groupby(raw["sleep_hours"].isna())["part_time_job_hours_week"].agg(["count", "mean"]).round(1))
raw.groupby(raw["part_time_job_hours_week"] > 15)["sleep_hours"].apply(lambda s: s.isna().mean()).round(2).rename("share with missing sleep")
''', "instr"),
    md("### 2f. Suspicious… but are they errors?"),
    code('''
raw[raw["study_hours_week"].between(40, 100)].sort_values("study_hours_week", ascending=False)
'''),
    code('''
# Also look at the best-scoring students who barely study:
raw[raw["exam_score"].between(90, 100)].sort_values("study_hours_week").head(5)
'''),
    md("""
**Think:** a student who studies 58 h/week with stress 9.6 — a *typo*, or a real burned-out grinder?
A Design student with 2 study hours and an exam score of 96.5 — a *typo*, or a genuinely gifted student?
👉 **Write your decision and your evidence in the box below.**
"""),
    md("""
## Step 3 · Evidence board 📝
*(double-click this cell to edit)*

| # | Problem found | How I found it | My fix |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| … | | | |

**Outlier decision (keep or remove? why?):** …
""", "student"),
    md("## Step 4 · Clean it\n### 🧪 Auto-checker (run this cell, don't edit it)"),
    code('''
REAL_OUTLIERS = ["CS-0183", "CS-0477", "CS-0109", "CS-0187"]   # (a hint: the checker knows some students are real!)
PROGRAMS = {"Engineering", "Data Science", "Business", "Design"}

def check_my_work(d):
    ok = lambda c: "✅" if c else "❌"
    def within(col, lo, hi):
        s = d[col].dropna()
        return bool(s.between(lo, hi).all())
    checks = [
        ("no duplicate students", not d["student_id"].duplicated().any()),
        ("program has exactly 4 clean labels", set(d["program"].dropna().unique()) == PROGRAMS and d["program"].notna().all()),
        ("age is realistic (15–60 or blank)", within("age", 15, 60)),
        ("study_hours is realistic (0–100 or blank)", within("study_hours_week", 0, 100)),
        ("sleep_hours is realistic (0–14 or blank)", within("sleep_hours", 0, 14)),
        ("exam_score is between 0 and 100 (or blank)", within("exam_score", 0, 100)),
        ("real extreme students were KEPT", d["student_id"].isin(REAL_OUTLIERS).sum() == 4 and
            d.loc[d["student_id"].isin(REAL_OUTLIERS), ["study_hours_week", "exam_score"]].notna().all().all()),
        ("you did not delete too much (≥ 505 rows left)", len(d) >= 505),
    ]
    for name, passed in checks:
        print(ok(passed), name)
    n = sum(p for _, p in checks)
    print(f"\\n{n}/{len(checks)} checks passed" + ("  🎉 Clean!" if n == len(checks) else "  — keep going"))

print("Checker ready.")
'''),
    code('''
df_clean = raw.copy()

# 1) remove exact duplicate rows
#    hint: df_clean = df_clean.drop_duplicates()

# 2) standardise the program labels so only 4 remain.
#    Look at raw["program"].value_counts() above and add every variant you saw.
program_map = {
    "engineering": "Engineering",
    # "data science": "Data Science",
    # ...
}
df_clean["program"] = df_clean["program"].str.strip().str.lower().map(program_map)

# 3) turn impossible values into blanks (NaN). Example:
#    df_clean.loc[df_clean["age"] > 60, "age"] = np.nan

check_my_work(df_clean)
''', "student"),
    code('''
df_clean = raw.drop_duplicates().copy()

program_map = {
    "engineering": "Engineering", "eng.": "Engineering",
    "data science": "Data Science", "ds": "Data Science", "data sci": "Data Science",
    "business": "Business", "biz": "Business",
    "design": "Design",
}
df_clean["program"] = df_clean["program"].str.strip().str.lower().map(program_map)

df_clean.loc[(df_clean["age"] < 15) | (df_clean["age"] > 60), "age"] = np.nan
df_clean.loc[df_clean["study_hours_week"] > 100, "study_hours_week"] = np.nan
df_clean.loc[(df_clean["sleep_hours"] <= 0) | (df_clean["sleep_hours"] > 14), "sleep_hours"] = np.nan
df_clean.loc[df_clean["exam_score"] > 100, "exam_score"] = np.nan

check_my_work(df_clean)
''', "instr"),
    md("""
## Step 5 · 🌶️ Extra challenge (if you finish early)
1. Write a **3-sentence data-quality memo** to the survey office: what went wrong, how big is it, what should they change in the form? *(Hint: a dropdown for `program` would prevent label chaos.)*
2. Compare `df_clean.describe()` with `raw.describe()`. How did the mean of `study_hours_week` change?
3. **Why did we blank impossible values instead of deleting the whole row?**

**When time is up: type your final number of problems found in chat.** 🏁
""", "student"),
    md("""
## 🔑 INSTRUCTOR ANSWER KEY — the 14 planted problems

| # | Problem | Where | Evidence | Right fix |
|---|---|---|---|---|
| 1 | **10 exact duplicate rows** | whole file | `raw.duplicated().sum()` = 10 | drop |
| 2 | **Label chaos** in `program` (≈14 spellings: `DS`, `Biz`, `Eng.`, ` Engineering`, `data science`…) | `program` | `value_counts()` | strip/lower/map to 4 labels |
| 3 | `age` = **250** | `age` | describe max | blank (NaN) |
| 4 | `age` = **199** (typo for 19?) | `age` | filter > 60 | blank — *don't guess* |
| 5 | `age` = **5** | `age` | describe min | blank |
| 6 | `study_hours_week` = **168** (every hour of the week) | study | filter > 100 | blank |
| 7 | `study_hours_week` = **999** — a **sentinel** "missing" code | study | describe max | blank |
| 8 | `sleep_hours` = **−7.5** (sign typo?) | sleep | describe min | blank (or abs, but justify) |
| 9 | `sleep_hours` = **25** | sleep | describe max | blank |
| 10 | `exam_score` = **105** (> 100) | exam | filter | blank |
| 11 | `exam_score` = **999** — sentinel | exam | describe max | blank |
| 12 | **Missing `sleep_hours` is NOT random** — much more common for students with long job hours (busy students skip the late-night survey) | sleep | job-hours mean of missing group is much higher | **don't impute naively**; report bias |
| 13 | `stress_score` missing ≈3 % at random | stress | `isna().sum()` | leave NaN / ignore |
| 14 | **Real outliers (KEEP!)**: three students studying 55–61 h/week with stress ≈9.6; one Design student with 2 h study and 96.5 exam | study/exam | extreme but consistent with other columns | keep, flag, mention in report |

### 🎤 Talking points for the debrief
* "Everyone found the 250-year-old. The skill is the *systematic* sweep: duplicates → categories → ranges → missing → missingness *pattern*."
* "**999 is not a number, it's a missing-value code.** If you'd averaged it you'd have a mean study time of 44 hours."
* "Why blank instead of deleting the row? The rest of that student's answers are fine — deleting rows throws away good information."
* "The most senior judgement was **keeping** the 55-hour student. We checked other columns (stress 9.6, normal-ish score): coherent story → real person."
* "Problem 12 is the one a junior analyst misses: *the pattern of the missing data is itself a finding*."
""", "instr"),
]

# ============================================================================
#  TEAM MISSIONS
# ============================================================================
T = []
T += [
    md("""
# 👥 Team Missions — Class 03
**11 minutes in your breakout room · then a 45-second pitch**

### Step 1 — set your team number below, run the setup cell, and jump to *your* mission.
Roles (5 people): **🖥️ Driver** (shares screen, types) · **🤨 Skeptic** ("what else could explain this?") · **🎤 Spokesperson** · **⏱️ Timekeeper** · **📝 Scribe** (fills in the pitch box)

### The pitch (45 seconds, spoken — no screen share)
> **Headline:** one sentence, the finding. &nbsp; **Evidence:** the one chart/number that proves it. &nbsp; **Recommendation:** what should the stakeholder DO?

**Scoring:** 🔍 finding is real & correct (40%) · 🧠 you checked an alternative explanation (30%) · 🎯 concrete recommendation (30%)
""", "student"),
    md("""
# 🎤 INSTRUCTOR — Team Missions · Answer notebook
Student copy: `04_STUDENT_team_mission.ipynb`. This copy has **solved code, ground-truth numbers, and grilling questions** for each team.
""", "instr"),
    setup_cell(("clean",)),
    code('''
TEAM = 1   # 👈 change to your team number (1–5), then re-run the cell
df = load("clean")
print(f"Team {TEAM} ready — {df.shape[0]} students loaded.  Scroll down to 'Mission {TEAM}'.")
''', "student"),
    code('''
df = load("clean")
print(df.shape)
''', "instr"),
]

# ---------------------------------------------------------------- TEAM 1
T += [
    md("""
---
# 🛌 Mission 1 — The Sleep Cliff
**Stakeholder:** Head of Student Health Services
**Question:** *"Is there a minimum amount of sleep we should recommend? How many exam points are students losing if they're below it?"*
**EDA skills:** scatter plot · binning · comparing group means
"""),
    code('''
d = df.dropna(subset=["sleep_hours", "exam_score"])

fig, ax = plt.subplots(figsize=(7.5, 4.5))
sns.scatterplot(data=d, x="sleep_hours", y="exam_score", alpha=0.45, ax=ax)
ax.set_title("Sleep vs exam score"); plt.show()
print("correlation r =", round(d["sleep_hours"].corr(d["exam_score"]), 2))
'''),
    code('''
# Average score for each sleep band — where does the curve bend?
bands = pd.cut(d["sleep_hours"], bins=[0, 5, 5.5, 6, 6.5, 7, 8, 10])
table = d.groupby(bands)["exam_score"].agg(["count", "mean"]).round(1)
display(table)
table["mean"].plot(marker="o", figsize=(7, 3.5), title="Average exam score by sleep band"); plt.show()
'''),
    code('''
THRESHOLD = 6          # 👈 try other values (5, 5.5, 6.5, 7). Which one separates the groups best?
short = d["sleep_hours"] < THRESHOLD
print(f"share of students below {THRESHOLD}h: {short.mean():.0%}")
print(d.groupby(short)["exam_score"].mean().round(1).rename({True: f"< {THRESHOLD}h", False: f">= {THRESHOLD}h"}))
'''),
    md("""
**Discuss:** Where is the cliff? Is the relationship a straight line or a bend? Is `r` a good summary here?
**Skeptic:** could another variable (job hours? commute?) explain both short sleep and low scores?

**📝 Pitch box** *(double-click to write)*
**Headline:** …  **Evidence:** …  **Recommendation:** …
""", "student"),
]

# ---------------------------------------------------------------- TEAM 2
T += [
    md("""
---
# 😰 Mission 2 — The Stress Sweet Spot
**Stakeholder:** Director of Campus Counselling
**Question:** *"Students say 'stress ruins my grades'. Is that true? Is some stress good? When should we step in?"*
**EDA skills:** non-linear relationships · why a weak `r` ≠ "no relationship" · small-sample caution
"""),
    code('''
d = df.dropna(subset=["stress_score", "exam_score"])
fig, ax = plt.subplots(figsize=(7.5, 4.5))
sns.regplot(data=d, x="stress_score", y="exam_score", scatter_kws={"alpha": 0.35, "s": 25},
            line_kws={"color": "crimson"}, ax=ax)
ax.set_title("Stress vs exam score (straight-line fit)"); plt.show()
print("correlation r =", round(d["stress_score"].corr(d["exam_score"]), 2))
'''),
    code('''
# Does a straight line describe it well? Average score for each stress level:
bands = pd.cut(d["stress_score"], bins=[0, 2, 3, 4, 5, 6, 7, 8, 9, 10])
table = d.groupby(bands)["exam_score"].agg(["count", "mean"]).round(1)
display(table)
table["mean"].plot(marker="o", figsize=(7, 3.5), title="Average exam score by stress band"); plt.show()
'''),
    code('''
# Try a curve instead of a line (order=2 means a parabola):
fig, ax = plt.subplots(figsize=(7.5, 4.5))
sns.regplot(data=d, x="stress_score", y="exam_score", order=2, scatter_kws={"alpha": 0.3, "s": 25},
            line_kws={"color": "crimson"}, ax=ax)
ax.set_title("Same data, curved fit"); plt.show()
'''),
    md("""
**Discuss:** Is stress "bad"? Where is performance highest? Look at the **count** column: can you trust the lowest bands?
**Skeptic:** is low stress really *causing* low scores — or might these be disengaged students?

**📝 Pitch box:** **Headline:** …  **Evidence:** …  **Recommendation:** …
""", "student"),
]

# ---------------------------------------------------------------- TEAM 3
T += [
    md("""
---
# 💼 Mission 3 — The Working Student
**Stakeholder:** Dean of Student Finance (decides the cap on campus job hours)
**Question:** *"Does working a part-time job hurt exam scores? If so, at how many hours per week does it start to hurt?"*
**EDA skills:** bimodal variable · grouping into buckets · checking a confounder
"""),
    code('''
d = df.dropna(subset=["exam_score"]).copy()
d["job_group"] = pd.cut(d["part_time_job_hours_week"], bins=[-1, 0, 8, 15, 40],
                        labels=["none", "1-8h", "9-15h", ">15h"])
display(d.groupby("job_group")["exam_score"].agg(["count", "mean"]).round(1))
sns.boxplot(data=d, x="job_group", y="exam_score"); plt.title("Exam score by weekly job hours"); plt.show()
'''),
    code('''
# 👈 Change the cut points above (e.g. [-1, 0, 10, 12, 15, 18, 40]) to find where the drop STARTS.
# Skeptic's check: maybe the workers are all in one hard program? Compare within each program:
d.pivot_table(index="program", columns="job_group", values="exam_score", aggfunc="mean").round(1)
'''),
    code('''
# How many students are actually in the risky group?
print(d["job_group"].value_counts(normalize=True).round(2))
'''),
    md("""
**Discuss:** Is it "working vs not working" or "working *too much*"? Does the pattern hold in **every** program?
**Skeptic:** what else might overworked students lack? (hint: check `sleep_hours` for the >15h group)

**📝 Pitch box:** **Headline:** …  **Evidence:** …  **Recommendation (a number!):** …
""", "student"),
]

# ---------------------------------------------------------------- TEAM 4
T += [
    md("""
---
# ☕ Mission 4 — The Coffee Myth
**Stakeholder:** Campus Café Manager & Wellness Office
**Question:** *"Heavy coffee drinkers seem to score worse. Should we launch an anti-coffee campaign or restrict sales of espresso?"*
**EDA skills:** confounding · checking inside groups · Simpson-style thinking
"""),
    code('''
d = df.dropna(subset=["exam_score"])
fig, ax = plt.subplots(figsize=(7.5, 4.5))
sns.regplot(data=d, x="caffeine_cups_day", y="exam_score", x_jitter=0.2,
            scatter_kws={"alpha": 0.3, "s": 25}, line_kws={"color": "crimson"}, ax=ax)
ax.set_title("Coffee vs exam score — all students"); plt.show()
print("overall r =", round(d["caffeine_cups_day"].corr(d["exam_score"]), 2))
'''),
    code('''
# Who drinks the most coffee? Look at the groups:
display(d.groupby("program").agg(students=("student_id", "count"),
                                  avg_cups=("caffeine_cups_day", "mean"),
                                  avg_score=("exam_score", "mean")).round(2))
'''),
    code('''
# Same chart, coloured by program, and the correlation INSIDE each program
sns.lmplot(data=d, x="caffeine_cups_day", y="exam_score", hue="program", height=4.5, aspect=1.5,
           x_jitter=0.2, scatter_kws={"alpha": 0.35, "s": 25}); plt.show()
print({p: round(float(g["caffeine_cups_day"].corr(g["exam_score"])), 2) for p, g in d.groupby("program")})
'''),
    md("""
**Discuss:** Is coffee harming scores, or is something else going on? What changed when you looked *inside* each program?
**Skeptic:** which *other* variable could make coffee drinkers look worse? What would you need to prove causation?

**📝 Pitch box:** **Headline:** …  **Evidence:** …  **Recommendation:** …
""", "student"),
]

# ---------------------------------------------------------------- TEAM 5
T += [
    md("""
---
# 🕳️ Mission 5 — Who Didn't Answer? (and the extreme students)
**Stakeholder:** Survey Office
**Question:** *"About 10 % of students skipped the sleep question. Can we just ignore the blanks? And what should we do with the extreme students (55+ study hours; 96 % score with 2 study hours)?"*
**EDA skills:** missing-data patterns · outlier judgement
"""),
    code('''
d = df.copy()
d["sleep_missing"] = d["sleep_hours"].isna()
print("share of sleep answers missing:", round(d["sleep_missing"].mean(), 3))
d.groupby("sleep_missing")[["part_time_job_hours_week", "study_hours_week", "stress_score", "exam_score",
                            "commute_minutes"]].mean().round(1)
'''),
    code('''
# Does the missing rate change by group?
d["job_group"] = pd.cut(d["part_time_job_hours_week"], bins=[-1, 0, 15, 40], labels=["no job", "1-15h", ">15h"])
for col in ["job_group", "program", "residence"]:
    print(d.groupby(col)["sleep_missing"].mean().round(3).to_frame("share missing"), "\\n")
'''),
    code('''
# The extreme students: error or real?
extreme = d[(d["study_hours_week"] >= 50) | ((d["exam_score"] >= 93) & (d["study_hours_week"] <= 5))]
extreme[["student_id", "program", "study_hours_week", "sleep_hours", "stress_score", "exam_score"]]
'''),
    code('''
# Compare them with their own program (are they consistent with the rest of their record?)
d.groupby("program")[["study_hours_week", "stress_score", "exam_score"]].mean().round(1)
'''),
    md("""
**Discuss:** Are the blanks random? Who is under-represented in the sleep results? Keep or remove the extreme students — what evidence?
**Skeptic:** if we ignore the missing group, in which direction would our conclusions about sleep be biased?

**📝 Pitch box:** **Headline:** …  **Evidence:** …  **Recommendation:** …
""", "student"),
]

# ============================================================================
#  INSTRUCTOR-ONLY: ground truth for teams (computed live below)
# ============================================================================
T += [
    md("""
---
# 🔑 GROUND TRUTH — computed numbers for each mission
*(instructor only — values below are printed by the code, so they always match the data)*
""", "instr"),
    code('''
d = df.dropna(subset=["sleep_hours", "exam_score"])
below, above = d[d.sleep_hours < 6]["exam_score"], d[d.sleep_hours >= 6]["exam_score"]
print("=== TEAM 1 SLEEP ===")
print(f"overall r = {d.sleep_hours.corr(d.exam_score):.2f}   (weak-looking)")
print(f"<6h: n={len(below)} ({len(below)/len(d):.0%} of students) mean={below.mean():.1f}   >=6h: n={len(above)} mean={above.mean():.1f}   gap={above.mean()-below.mean():.1f} pts")
print(d.groupby(pd.cut(d.sleep_hours,[0,5,5.5,6,6.5,7,8,10]))["exam_score"].agg(["count","mean"]).round(1))
''', "instr"),
    code('''
d = df.dropna(subset=["stress_score", "exam_score"])
print("=== TEAM 2 STRESS ===")
print(f"overall r = {d.stress_score.corr(d.exam_score):.2f}   (weak — but the relationship is strong and CURVED)")
t = d.groupby(pd.cut(d.stress_score,[0,2,3,4,5,6,7,8,9,10]))["exam_score"].agg(["count","mean"]).round(1)
print(t)
print("peak band:", t["mean"].idxmax(), "->", t["mean"].max())
''', "instr"),
    code('''
d = df.dropna(subset=["exam_score"]).copy()
d["jg"] = pd.cut(d.part_time_job_hours_week, bins=[-1,0,8,15,40], labels=["none","1-8h","9-15h",">15h"])
print("=== TEAM 3 JOB ===")
print(d.groupby("jg")["exam_score"].agg(["count","mean"]).round(1))
print("share >15h:", round((d.part_time_job_hours_week>15).mean(),2))
print(d.pivot_table(index="program", columns="jg", values="exam_score", aggfunc="mean").round(1))
print("avg sleep >15h vs <=15h:", d[d.part_time_job_hours_week>15].sleep_hours.mean().round(2), d[d.part_time_job_hours_week<=15].sleep_hours.mean().round(2))
''', "instr"),
    code('''
d = df.dropna(subset=["exam_score"])
print("=== TEAM 4 COFFEE ===")
print("overall r =", round(d.caffeine_cups_day.corr(d.exam_score), 2))
print(d.groupby("program").agg(avg_cups=("caffeine_cups_day","mean"), avg_score=("exam_score","mean")).round(2))
print("within-program r:", {p: round(float(g.caffeine_cups_day.corr(g.exam_score)),2) for p, g in d.groupby("program")})
''', "instr"),
    code('''
d = df.copy(); d["miss"] = d.sleep_hours.isna()
print("=== TEAM 5 MISSING + OUTLIERS ===")
print("missing share:", round(d.miss.mean(),3))
d["jg"] = pd.cut(d.part_time_job_hours_week, bins=[-1,0,15,40], labels=["no job","1-15h",">15h"])
print(d.groupby("jg")["miss"].mean().round(3).to_dict(), "| by program:", d.groupby("program")["miss"].mean().round(3).to_dict())
print(d.groupby("residence")["miss"].mean().round(3).to_dict())
print(d[(d.study_hours_week>=50)|((d.exam_score>=93)&(d.study_hours_week<=5))][["student_id","program","study_hours_week","stress_score","exam_score"]])
''', "instr"),
    md("""
### Quick answers
| Team | Finding | Common mistake | Strong recommendation |
|---|---|---|---|
| **1 Sleep** | A *cliff* below ~6 h: students under 6 h (≈22 % of the class) average ≈5 pts lower overall, and ≈8 pts lower under 5.5 h (≈59 vs ≈66+); above 6 h extra sleep adds little. `r` (≈0.18) understates it because the relation is a threshold, not a line. | "Sleep and scores are weakly related." | "Recommend ≥ 6 h; target the ~25 % below it." |
| **2 Stress** | **Inverted U**: scores peak at moderate stress (≈5–6) and fall at both ends, steeply above ~8. Pearson r ≈ −0.17 hides it. Lowest-stress band is tiny (n≈16) → be careful. | "Stress is weakly bad." / treating low-stress as proven harmful. | "Intervene at stress ≥ 8; don't try to eliminate stress." |
| **3 Job** | No harm up to ~15 h/week; above 15 h scores drop (≈58 vs ≈67 for non-workers, ≈ −9 pts; ≈21 % of students), and it falls even more above ~22 h. Holds within each program. Overworked students also sleep less (≈6.2 h vs 6.9 h). | Comparing "works vs doesn't" and concluding any job hurts. | "Cap campus jobs at ~15 h/week." |
| **4 Coffee** | Overall r ≈ −0.34, but **inside every program ≈ 0**. Engineering drinks the most and scores lowest because of the *program*. Confounding. | "Coffee lowers scores → ban it." | "No coffee campaign; compare within program." |
| **5 Missing/outliers** | Sleep is missing ≈ 5× more often for students with a job (≈3 % of non-workers vs 15–19 % of workers) → the sleep results *under-represent* overworked students (biased, probably *understating* sleep trouble). The 3 grinders (55–61 h, stress ≈9.6) and the 96.5 Design student are coherent → **keep & flag**. | "Fill blanks with the mean." / "delete outliers." | "Follow up with job-heavy students; keep outliers; add an optional-question reminder." |
""", "instr"),
]

if __name__ == "__main__":
    for nb_name, cells, aud, do_render in [
        ("03_STUDENT_solo_data_detective.ipynb", S, "student", False),
        ("03_INSTRUCTOR_solo_solutions.ipynb", S, "instr", True),
        ("04_STUDENT_team_mission.ipynb", T, "student", False),
        ("04_INSTRUCTOR_team_answers.ipynb", T, "instr", True),
    ]:
        nb = build(cells, aud)
        if do_render:
            for p in render(nb):
                print(nb_name, "cell error:", p)
        print("Saved", save(nb, nb_name))
