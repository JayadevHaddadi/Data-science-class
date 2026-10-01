"""Builds the two 'live class' notebooks from ONE source:

  01_INSTRUCTOR_live_class.ipynb   - what you screen-share (talking points, polls, answers, pre-rendered outputs)
  02_STUDENT_follow_along.ipynb    - what students open in Colab (same code, predict boxes, no answers)
"""
from nbtools import build, code, md, note, predict, render, save, setup_cell

C = []  # cell list

# =====================================================================  COVER
C += [
    md("""
# 🔎 Class 03 — Exploratory Data Analysis Deep Dive
**Distributions · Anomalies · Relationships · Grouping · Correlation**

Today you are a **data detective** working on the *Campus Wellbeing Survey* (520 students, 4 programs).
The Dean's question: **"What really drives exam performance?"**

| Rule | Why |
|---|---|
| 🔮 **Predict before you run** | Guessing first is what makes the lesson stick |
| 💬 **Type `?` in chat when stuck** | Don't suffer silently — a TA / classmate will help |
| 🧠 **Insight > code** | Anyone can generate a plot. Your value is *what it means* |
""", "student"),
    md("""
# 🎤 INSTRUCTOR MASTER NOTEBOOK — Class 03: EDA Deep Dive
**Online · 25 students · Colab · 10:50–12:30 (100 min)**
Blockquotes like this one are **for you** — they are not in the student copy (`02_STUDENT_follow_along.ipynb`).

| Clock | Min | Block | Mode |
|---|---|---|---|
| 10:50 | 8 | **Part 0** Hook: Anscombe + mission | You talk, chat poll |
| 10:58 | 17 | **Part 1** Distributions & shape | Live demo + predict |
| 11:15 | 20 | **Solo: Data Detective** (notebook 03) | Individual, 15 min work + 5 debrief |
| 11:35 | 17 | **Part 2** Relationships & correlation | Live demo + predict |
| 11:52 | 7 | ☕ **Break** | Cameras off, stretch |
| 11:59 | 13 | **Part 3** Grouping & Simpson's paradox | Live demo — the climax |
| 12:12 | 13 | **Team missions** (notebook 04) | 5 breakout rooms × 5 students |
| 12:25 | 5 | **Pitches + wrap-up** | 45 s per team |

**Rhythm rule:** never talk more than ~10 min without students *doing* something (type, vote, run, share, present).

**Running late? Cut in this order:** (1) Part 1.4 mixture plot → (2) Part 2 poll on social media → (3) Part 3 bonus pivot → (4) shorten pitches to chat-only.

**Before class (see CLASS_LESSON_PLAN.md for the full checklist):** upload notebooks 02/03/04 to a shared Google Drive folder (or Colab links), test the setup cell once in a fresh Colab, create breakout rooms.
""", "instr"),
]

# =====================================================================  PART 0
C += [
    md("---\n## Part 0 · Hook: why we never trust summary numbers"),
    note("""
**🕙 10:50 — Welcome (2 min)**
🎤 SAY: "Welcome. Today is the most *detective* class of the course. Last time you learned to draw charts. Today you learn to *interrogate* data — find the weird stuff, find the real patterns, and avoid being fooled."
👩‍💻 DO: Put the Colab link in chat. Ask everyone to open notebook **02**, run the setup cell, and type ✅ in chat when it prints "Setup complete".
🛟 Tell them: "Stuck? Type `?` in chat. Don't wait."
"""),
    setup_cell(("raw", "clean")),
    md("### 🧪 Four mystery datasets (Anscombe's quartet)"),
    code('''
x123 = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
anscombe = pd.DataFrame({
    "set": np.repeat(["I", "II", "III", "IV"], 11),
    "x": x123 * 3 + [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8],
    "y": [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68,
          9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74,
          7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73,
          6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89],
})
summary = anscombe.groupby("set").agg(
    mean_x=("x", "mean"), mean_y=("y", "mean"), std_y=("y", "std"))
summary["correlation"] = [g["x"].corr(g["y"]) for _, g in anscombe.groupby("set")]
summary.round(2)
'''),
    predict("""
The table says all four datasets have the **same mean, same spread, same correlation (≈0.82)**.

**Vote in chat:** will the four scatter plots look **A)** basically the same, or **B)** completely different?""",
            """
🎤 Wait for ~10 votes in chat. Read a few out loud.
"""),
    code('''
g = sns.lmplot(data=anscombe, x="x", y="y", col="set", col_wrap=2, height=3, ci=None,
               scatter_kws={"s": 50}, line_kws={"color": "crimson"})
g.fig.suptitle("Same numbers, four different stories", y=1.02)
plt.show()
'''),
    note("""
🎤 SAY: "Same mean, same SD, same correlation, same regression line — and four totally different realities.
I: fine. II: a *curve* — a straight-line correlation is the wrong tool. III: one outlier is dragging the line. IV: one single point creates the whole correlation."
🎤 SAY: "**Summary numbers lie. EDA means LOOKING.** Today's four questions: What is the *shape*? What is *weird*? What is *related*? And *who are the groups*?"
⏱️ Keep this to ~3 min. It's a hook, not a lecture.
"""),
    md("""
### 🎯 Today's mission
**Campus Wellbeing Survey** — 520 students, 4 programs. The Dean asks: *"What really drives exam performance?"*
We'll answer with 4 EDA moves: **shape → anomalies → relationships → groups.**
"""),
    code('''
df = load("raw")        # the raw file, straight from the survey system
print(df.shape)
df.head(8)
'''),
    md("""
| Column | Meaning |
|---|---|
| `program`, `year`, `age`, `residence` | who the student is |
| `study_hours_week`, `part_time_job_hours_week`, `commute_minutes` | how they spend time |
| `sleep_hours`, `caffeine_cups_day`, `social_media_hours_day`, `stress_score` (1–10) | habits & wellbeing |
| `exam_score` (0–100) | the outcome we care about |
"""),
]

# =====================================================================  PART 1
C += [
    md("---\n## Part 1 · Distributions: what does each variable look like?"),
    note("""
**🕙 10:58 (17 min)**
Goal: students learn to ask "what SHAPE is this?" before computing any average, and that a mean can describe nobody.
"""),
    md("### 1.1 First look: `info()` and `describe()`"),
    code('''
df.info()
'''),
    code('''
df.describe().round(1)
'''),
    note("""
🎤 SAY: "Take 20 seconds. Look at the **min** and **max** rows. Don't say anything yet — just *notice*. Write 2 suspicious things in your notes."
(Wait 20 s.) 🎤 "Keep your list. In a few minutes you'll get 15 minutes alone with this raw file to hunt every problem. For now we'll look only at columns that look healthy."
👀 What they should have noticed: age max 250, study_hours max 999, sleep min -7.5 / max 25, exam max 999.
"""),
    md("### 1.2 Shape: part-time job hours"),
    predict("""
`part_time_job_hours_week` = hours per week a student works a paid job.

**What shape will the histogram have?** &nbsp; A) bell curve &nbsp; B) long right tail &nbsp; C) two humps""",
            "🎤 Take votes. Most will say A. That's the point."),
    code('''
fig, ax = plt.subplots(figsize=(8, 4))
sns.histplot(df["part_time_job_hours_week"], bins=32, ax=ax, color="steelblue")
mean, median = df["part_time_job_hours_week"].mean(), df["part_time_job_hours_week"].median()
ax.axvline(mean, color="crimson", ls="--", lw=2, label=f"mean = {mean:.1f}")
ax.axvline(median, color="darkgreen", ls="--", lw=2, label=f"median = {median:.1f}")
ax.set_title("Weekly part-time job hours"); ax.set_xlabel("hours per week"); ax.legend()
plt.show()
print("Share of students who do NOT work:", round((df["part_time_job_hours_week"] == 0).mean() * 100), "%")
'''),
    note("""
🎤 SAY: "**Two humps** — a giant spike at zero (students who don't work) and a second cluster around 15 hours. This is a *bimodal* distribution — really **two populations** glued together."
🎤 SAY: "The mean is about 6.8 hours. **Is there a single student who works 6.8 hours?** Barely. The mean describes *nobody*. The median is 0, which is also misleading. Lesson: when you see two humps, **don't summarise — split**."
❓ Ask chat: "How would you report this to the Dean in one sentence?" (Expect: "about 55% don't work; those who do work ~15 hours".)
"""),
    md("### 1.3 Shape: commute time (skew)"),
    code('''
fig, axes = plt.subplots(1, 2, figsize=(11, 4))
sns.histplot(df["commute_minutes"], bins=30, ax=axes[0], color="darkorange")
axes[0].axvline(df["commute_minutes"].mean(), color="crimson", ls="--", label="mean")
axes[0].axvline(df["commute_minutes"].median(), color="darkgreen", ls="--", label="median")
axes[0].set_title("Commute (minutes)"); axes[0].legend()
sns.boxplot(x=df["commute_minutes"], ax=axes[1], color="darkorange")
axes[1].set_title("Same data as a boxplot")
plt.show()
print(f"mean = {df['commute_minutes'].mean():.1f}   median = {df['commute_minutes'].median():.1f}   skew = {df['commute_minutes'].skew():.2f}")
'''),
    note("""
🎤 SAY: "Right-skewed: most commutes are short, a few are very long, so the **mean (37) is pulled above the median (25)**. For skewed data, report the **median**."
🎤 SAY: "The dots on the boxplot are Tukey outliers (beyond 1.5×IQR) from Class 1. **Are they errors?** A 3-hour commute is painful — but possible. *An outlier is a question, not a verdict.*"
"""),
    md("### 1.4 Is the skew hiding a *mixture*?"),
    code('''
fig, ax = plt.subplots(figsize=(8, 4))
sns.kdeplot(data=df, x="commute_minutes", hue="residence", common_norm=False, fill=True, alpha=0.35, ax=ax)
ax.set_title("Commute time by residence"); ax.set_xlim(0, 200)
plt.show()
df.groupby("residence")["commute_minutes"].agg(["count", "median", "mean"]).round(1)
'''),
    note("""
🎤 SAY: "Same trick as the job hours: the skewed shape is a **mixture of groups**. Hostel students walk 10 minutes, commuters travel over an hour. *Splitting by a category often explains a weird shape.* Remember this — it's the main idea of Part 3."
(✂️ Cut this section if you are behind.)
"""),
    md("### 🙋 Your turn (90 seconds)"),
    md("Make a histogram of `social_media_hours_day`. **In chat, type 3 words describing its shape** (symmetric? skewed? two humps?)."),
    code('''
sns.histplot(df["social_media_hours_day"], bins=25)
plt.title("Social media hours per day")
plt.show()
''', "instr"),
    code('''
# Your turn: histogram of social_media_hours_day (use sns.histplot), then describe the shape in chat

''', "student"),
    note("""
🎤 Expect: "roughly symmetric / bell-shaped / centred around 3 hours". Call on two students to say it aloud. Quick win: *not every variable is weird.*
➡️ **Transition (11:13):** "Now it's your turn. Open **notebook 03 — Data Detective**. You have 15 minutes, alone. Cameras on, mics muted, `?` in chat if stuck."
"""),
]

# =====================================================================  SOLO
C += [
    md("---\n## 🕵️ Solo task: Data Detective\n\n👉 Open **`03_STUDENT_solo_data_detective.ipynb`** (link in chat). 15 minutes, individual. We'll continue here afterwards."),
    note("""
**🕙 11:15–11:35 (15 min work + 5 debrief)** — see `03_INSTRUCTOR_solo_solutions.ipynb` for the answer key.
👩‍💻 While they work: stay on camera, answer chat, and ask a TA / strong student to help with `?` messages. Post a timer in chat at the 10-min and 2-min marks.
🏁 **Debrief (5 min):**
1. Ask: "How many problems did you find? Type the number in chat." (Anyone ≥ 8 gets a shout-out.)
2. Ask **2–3 volunteers to share their screen** and show their best finding.
3. Reveal the full list from notebook 03-INSTRUCTOR.
4. 🎤 SAY: "The most important decision wasn't deleting the bad rows — it was deciding to **KEEP** the students who study 55+ hours. An outlier is not an error. Check before you delete."
"""),
]

# =====================================================================  PART 2
C += [
    md("---\n## Part 2 · Relationships & Correlation"),
    note("""
**🕙 11:35 (17 min)** — From now on we use the **clean** file so everybody is looking at the same numbers.
"""),
    code('''
df = load("clean")
print(df.shape, "→ duplicates removed, labels fixed, impossible values blanked (NaN)")
df.isna().sum()[lambda s: s > 0]
'''),
    md("""
### 2.1 Correlation vocabulary
| \\|r\\| | Say |
|---|---|
| < 0.2 | very weak / none |
| 0.2 – 0.4 | weak–moderate |
| 0.4 – 0.7 | moderate–strong |
| > 0.7 | strong |

**Pearson r only measures *straight-line* association** (remember Anscombe II!).
"""),
    predict("""
We'll draw a **correlation heatmap** of all numeric columns, and `exam_score` is the outcome we care about.

**Chat:** which ONE variable do you think has the *strongest positive* link with exam score?""",
            "🎤 Expect: study hours (most), sleep. Don't reveal."),
    code('''
corr = df.corr(numeric_only=True)
fig, ax = plt.subplots(figsize=(9, 7))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, vmin=-1, vmax=1,
            square=True, linewidths=0.5, ax=ax)
ax.set_title("Correlation heatmap — Campus Wellbeing Survey")
plt.show()
'''),
    note("""
🎤 SAY: "Read the heatmap like a map: **red = move together, blue = move opposite, white = unrelated.** Look at the `exam_score` row."
Walk through, ~3 min:
• `age`–`year` = 0.91 → obvious/trivial (don't get excited about it).
• `social_media_hours_day`–`stress_score` ≈ 0.56 → the strongest *interesting* link.
• `exam_score` vs `study_hours_week` = **−0.38**. 😱 Pause here. "Negative?! Studying *lowers* scores?" Park it: "Hold that thought, we'll solve it after the break."
• `exam_score` vs `caffeine_cups_day` = −0.34. (Team 4 will investigate.)
• `exam_score` vs `sleep` +0.18 and vs `job hours` −0.27.
"""),
    md("### 2.2 Correlation ≠ causation"),
    code('''
fig, ax = plt.subplots(figsize=(7, 5))
sns.regplot(data=df, x="social_media_hours_day", y="stress_score",
            scatter_kws={"alpha": 0.35, "s": 25}, line_kws={"color": "crimson"}, ax=ax)
r = df["social_media_hours_day"].corr(df["stress_score"])
ax.set_title(f"Social media vs stress   (r = {r:.2f})")
plt.show()
'''),
    predict("""
Social media and stress clearly move together (r ≈ 0.56).

**Vote:** A) social media causes stress &nbsp; B) stress makes students scroll more &nbsp; C) something else drives both &nbsp; D) can't tell from this data""",
            "🎤 Answer: D (and A, B, C are all plausible). Correlation gives **association, not direction.** Use the words 'is associated with', never 'causes'."),
    note("""
🎤 SAY: "Three reasons two things correlate: **(1) A causes B, (2) B causes A, (3) a hidden C causes both** — or (4) pure coincidence. A scatter plot can't tell them apart. Experiments or careful design can."
(✂️ Cut the poll if you are behind — just say it.)
"""),
    md("### 2.3 The cliffhanger: study hours vs exam score"),
    predict("""
Students who study **more** should score **higher**, right?

**Chat:** will the scatter plot slope **up**, **down**, or be **flat**?""",
            "🎤 Everyone says 'up'. You already saw −0.38 on the heatmap, so say nothing — let them commit."),
    code('''
fig, ax = plt.subplots(figsize=(7.5, 5))
sns.regplot(data=df, x="study_hours_week", y="exam_score",
            scatter_kws={"alpha": 0.35, "s": 25}, line_kws={"color": "crimson"}, ax=ax)
r = df["study_hours_week"].corr(df["exam_score"])
ax.set_title(f"Study hours vs exam score   (r = {r:.2f})")
plt.show()
'''),
    note("""
🎤 SAY: "**Down.** The more students study, the *lower* they score. So — should the Dean tell students to study less?"
(Let them react in chat for 20 seconds.)
🎤 SAY: "Something is off. Write down ONE hypothesis for why this might be wrong. We'll test it right after the break."
☕ **Break at ~11:52** — "7 minutes. Be back at 11:59 sharp. Cameras off, stretch."
"""),
    md("---\n## ☕ Break — 7 minutes\n*While you're away, think: what could make studying look harmful when it isn't?*"),
]

# =====================================================================  PART 3
C += [
    md("---\n## Part 3 · Grouping: *who* is in the data?"),
    note("""
**🕙 11:59 (13 min) — the climax of the class.** Welcome them back; ask 2 students for their hypothesis from before the break.
"""),
    md("### 3.1 Split the data with `groupby`"),
    code('''
by_program = df.groupby("program").agg(
    students=("student_id", "count"),
    avg_study_hours=("study_hours_week", "mean"),
    avg_exam_score=("exam_score", "mean"),
).round(1).sort_values("avg_study_hours", ascending=False)
by_program
'''),
    note("""
🎤 SAY: "Look carefully. Engineering studies the most (≈26 h) and scores the lowest (≈55). Design studies the least (≈9 h) and scores the highest (≈78). **The programs differ in *both* study time and score.** What if programs, not study hours, are driving the negative line?"
"""),
    md("### 3.2 Same scatter plot — now coloured by program"),
    code('''
fig, ax = plt.subplots(figsize=(8.5, 5.5))
palette = dict(zip(sorted(df["program"].unique()), sns.color_palette("Set2", 4)))
for prog, g in df.dropna(subset=["study_hours_week", "exam_score"]).groupby("program"):
    ax.scatter(g["study_hours_week"], g["exam_score"], s=22, alpha=0.55, color=palette[prog], label=prog)
    slope, intercept = np.polyfit(g["study_hours_week"], g["exam_score"], 1)
    xs = np.linspace(g["study_hours_week"].min(), g["study_hours_week"].max(), 10)
    ax.plot(xs, intercept + slope * xs, color=palette[prog], lw=3)
all_ = df.dropna(subset=["study_hours_week", "exam_score"])
slope, intercept = np.polyfit(all_["study_hours_week"], all_["exam_score"], 1)
xs = np.linspace(all_["study_hours_week"].min(), all_["study_hours_week"].max(), 10)
ax.plot(xs, intercept + slope * xs, color="black", ls="--", lw=2.5, label="ALL students combined")
ax.set_xlabel("study hours per week"); ax.set_ylabel("exam score")
ax.set_title("Simpson's paradox: down overall, UP inside every program")
ax.legend()
plt.show()
'''),
    note("""
🎤 SAY (pause for effect): "**Inside every single program, more study = higher score.** The black dashed line — all students combined — points the *opposite way*. That's **Simpson's paradox**."
🎤 SAY: "Why: the programs are *different* (harder grading, more demanding), so they sit at different heights. Engineering students study the most and score the lowest *because of the program*, not because studying is harmful."
Famous real example: the 1973 UC Berkeley admissions data — overall it looked like women were admitted less; department by department, women were admitted at equal or higher rates.
"""),
    md("### 3.3 The numbers behind the picture"),
    code('''
rows = {"ALL students": df["study_hours_week"].corr(df["exam_score"])}
for prog, g in df.groupby("program"):
    rows[prog] = g["study_hours_week"].corr(g["exam_score"])
pd.Series(rows, name="correlation (study vs exam)").round(2).to_frame()
'''),
    predict("""
**Final question for the Dean.** Based on what you now know, vote:

A) "Tell students to study less." &nbsp; B) "Keep encouraging study — the negative trend is an illusion." &nbsp; C) "Compare students only *within* the same program."

(You can pick more than one.)""",
            "🎤 Best answers: B and C. 🎤 SAY: **Rule #1 of EDA: always ask 'who are the groups?' before believing an overall trend.** An average across different groups can say the opposite of every group."),
    md("### 🎁 Bonus (if time): program × year heatmap"),
    code('''
pivot = df.pivot_table(index="program", columns="year", values="exam_score", aggfunc="mean").round(1)
fig, ax = plt.subplots(figsize=(6, 3.5))
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlGnBu", ax=ax)
ax.set_title("Average exam score by program and year")
plt.show()
'''),
    note("""
✂️ Skip if behind. 🎤 "A pivot table is `groupby` with two keys. Notice: **year barely matters; program matters a lot** — consistent with our story."
**➡️ Transition (12:12):** "Now YOU become the detectives in teams. Open notebook **04**. Your team number is in chat. I'm opening breakout rooms."
"""),
]

# =====================================================================  TEAMS
C += [
    md("---\n## 👥 Team missions\n\n👉 Open **`04_STUDENT_team_mission.ipynb`**, set `TEAM = <your number>`, and follow your mission card. **11 minutes** in your breakout room, then a **45-second pitch**."),
    note("""
**🕙 12:12–12:25 (13 min)** — see `INSTRUCTOR_TEAM_GUIDE.md` + `04_INSTRUCTOR_team_answers.ipynb`.
1. *(before 12:12)* Post the notebook link and team assignment in chat. Pre-create 5 breakout rooms with 5 students each.
2. Read the roles out loud: **Driver** (shares screen, types) · **Skeptic** ("what else could explain this?") · **Spokesperson** (45-sec pitch) · **Timekeeper** · **Scribe** (writes pitch in the notebook).
3. Open rooms. At 4 min and 8 min broadcast: "Chart done? Now write the recommendation." Visit 2–3 rooms; each visit ask: "What's the one chart that proves your point?"
4. At 12:23 close rooms with a 60-second warning.
"""),
]

# =====================================================================  WRAP
C += [
    md("---\n## 🏁 Wrap-up: the 4 laws of EDA"),
    md("""
1. **Look before you summarise** — means and correlations can hide the real shape (Anscombe).
2. **An outlier is a question, not a verdict** — investigate before deleting (error vs real signal).
3. **Correlation is linear and not causal** — check shape, direction, and hidden third variables.
4. **Always ask "who are the groups?"** — overall trends can reverse inside the groups (Simpson).

**Exit ticket (type in chat):** *What was your biggest surprise today?*
"""),
    note("""
**🕙 12:25 (5 min)** — Pitches: each team gets 45 s — *"Headline · one piece of evidence · one recommendation."* Don't screen share; speak. After each: one sentence of praise + one pushback question from `INSTRUCTOR_TEAM_GUIDE.md`.
🏆 Pick the winner: "the team that connected their chart to a *decision*".
🎤 Close: "Nobody pays you to write `sns.histplot`. They pay you to look at data, find what's weird, and tell humans what to do about it. Great class."
**Optional homework:** pick any dataset you like (Kaggle, your own life) and write **5 EDA findings**, each with one chart and one sentence starting with "This is associated with…".
"""),
]

if __name__ == "__main__":
    instr = build(C, "instr")
    problems = render(instr)
    for p in problems:
        print("INSTRUCTOR cell error:", p)
    print("Saved", save(instr, "01_INSTRUCTOR_live_class.ipynb"))
    print("Saved", save(build(C, "student"), "02_STUDENT_follow_along.ipynb"))
