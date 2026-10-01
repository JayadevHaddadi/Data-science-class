# 📋 Class 03 Lesson Plan: EDA Deep Dive (ONLINE)

**Time**: 10:50 – 12:30 (100 min) · **Format**: online (Teams or Meet) + Google Colab · **Students**: ~25
**Topics (from the admin's request)**: distributions · relationships · grouping · correlation · patterns & anomalies

---

## ⏱️ Timeline

| Clock | Min | Block | Notebook | Mode |
|---|---|---|---|---|
| 10:50 | 8 | **Part 0** Hook: Anscombe's quartet + mission | 01 / 02 | You talk, chat poll |
| 10:58 | 17 | **Part 1** Distributions & shape (bimodal, skew, mixtures) | 01 / 02 | Live demo + predict |
| 11:15 | 20 | **Solo: Data Detective** (15 work + 5 debrief) | 03 | Individual |
| 11:35 | 17 | **Part 2** Relationships & correlation (heatmap, causation, the study-hours cliffhanger) | 01 / 02 | Live demo + predict |
| 11:52 | 7 | ☕ Break | | |
| 11:59 | 13 | **Part 3** Grouping & **Simpson's paradox** (climax) | 01 / 02 | Live demo |
| 12:12 | 13 | **Team missions** (5 teams × 5 students, 11 min work) | 04 | Breakout rooms |
| 12:25 | 5 | **Pitches** (45 s each) + wrap-up | | Students speak |

**Never talk more than ~10 min without students doing something.**

### ✂️ If you run late, cut in this order
1. Part 1.4 (commute mixture plot)
2. Part 2.2 poll on social media causation
3. Part 3 bonus pivot table
4. Pitches become chat-only ("type headline + recommendation")

### ➕ If you run early
* Ask "which team's finding surprised you most?" and have the team show their chart.
* Bonus: have students find a *second* Simpson's paradox (e.g. `residence` vs exam score by `program`).

---

## 📁 Notebooks

| File | Who | What |
|---|---|---|
| `01_INSTRUCTOR_live_class.ipynb` | **you** (screen-share) | Talking points in blockquotes, polls, answers, pre-rendered outputs |
| `02_STUDENT_follow_along.ipynb` | students | Same code & predict boxes, no answers. They run cells as you do |
| `03_STUDENT_solo_data_detective.ipynb` | students | Individual raw-data cleaning task with auto-checker (8 checks) |
| `03_INSTRUCTOR_solo_solutions.ipynb` | **you** | Solutions + answer key of the 14 planted problems |
| `04_STUDENT_team_mission.ipynb` | students | 5 team missions; set `TEAM = n`; roles and pitch template |
| `04_INSTRUCTOR_team_answers.ipynb` | **you** | Solved missions with ground-truth numbers |
| `INSTRUCTOR_TEAM_GUIDE.md` | **you** | Pitch grilling questions and teacher summaries per team |

**No download needed**: the survey data is embedded inside each notebook (the repo is private, so Colab can't fetch it from GitHub).

---

## 🖥️ Teams or Meet?

* **Use whichever platform your school's account gives you breakout rooms in.** The team missions need breakout rooms.
* **Teams**: breakout rooms work on school/work (Microsoft 365) accounts. Organiser must *create* rooms; use the meeting's "Breakout rooms" icon (not available in some channel/ad-hoc meetings, so **schedule the meeting** beforehand).
* **Meet**: breakout rooms are available on paid Google Workspace plans (e.g. Education), not on a personal free Gmail account. Colab is Google, so Meet fits slightly better *if* breakouts are enabled for you.
* **If you have no breakout rooms**: the students create their own side calls (5 small Teams/Meet/Zoom calls, one per team, link posted in chat), or the teams work in a Google Doc and you hold 5 short rooms in chat.
* **Test it today before class**, not at 10:50.

---

## ✅ Pre-class checklist (30 min)

- [ ] Upload `02`, `03_STUDENT`, `04_STUDENT` notebooks to a shared Google Drive folder ("anyone with link → viewer"), or to a **GitHub Gist/public repo** and use "Open in Colab". Students use **File → Save a copy in Drive** (viewers can't edit the original).
- [ ] Open `02_STUDENT` once in a **fresh** Colab session and run the setup cell (confirms it works with Colab's package versions).
- [ ] Open `01_INSTRUCTOR_live_class.ipynb` in Colab (or VS Code) and **Runtime → Run all** once so outputs exist, then clear nothing: the blockquotes are your script.
- [ ] Put the three student links in a text file ready to paste in chat.
- [ ] Decide team assignments (1–5) from the roster; paste them in chat at 12:10.
- [ ] Pick a TA or two strong students to answer `?` messages during the solo task.
- [ ] Two screens ideal: one for the Teams/Meet window (chat, participants), one for the notebook.

---

## 🧑‍🏫 Online interaction toolkit

| Technique | How |
|---|---|
| **Predict-then-reveal** | Every plot is preceded by a "🔮 PREDICT" box; students type guess in chat; you read 3 aloud |
| **Everyone-answers chat** | "On 3, type your answer": prevents the same 2 students from answering every time |
| **Students share screens** | In the solo debrief, ask 2–3 to show their best finding |
| **`?` protocol** | Stuck → type `?` → TA/peer helps, you don't stop the class |
| **Cameras** | On for solo work and team rooms, optional during demos |
| **Timer** | Post "⏱ 5 min left" in chat; countdown timer shared on screen helps |
| **Rooms** | Visit 2–3 rooms; ask each "what's the one chart that proves your point?" |

---

## 🎯 Learning outcomes

By the end, students can:
1. Choose the right summary for a distribution (mean vs median; bimodal → split).
2. Systematically audit a raw dataset (duplicates, categories, ranges, sentinels, missingness patterns).
3. Distinguish *outlier* from *error*.
4. Read a correlation heatmap and state why r ≠ causation and r ≠ "no relationship".
5. Use `groupby` and colour-by-group to detect **Simpson's paradox** and confounding.
6. Defend a finding in 45 seconds with one chart and one recommendation.
