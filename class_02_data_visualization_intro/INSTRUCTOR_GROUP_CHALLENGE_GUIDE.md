# 🎤 Instructor Master Playbook: Group Presentation Grilling Guide

**Session**: Data Science Boardroom Challenge — Chart Selection & Analytical Defense  
**Location**: Room N209C  
**Format**: 5 Teams $\times$ (60s Student Pitch + 60s Instructor Grilling) = ~12-15 Minutes Total  
**Your Role**: You play the **Executive / Boardroom Chair**. Your goal is to test if students truly understand the analytical story or if they just generated code with AI without thinking.

---

## 🧭 Rapid Grading Scorecard (Keep in Mind)
* **35% - Visual Integrity**: Did they choose the right chart? Did they start bar axes at zero? Are labels clear?
* **35% - Analytical Depth**: Did they spot the actual pattern or just state obvious averages?
* **30% - Executive Delivery**: Did they propose a concrete business decision in their 60-second pitch?

---

## 🚨 GROUP 1: The "At-Risk Early Warning" Taskforce

* **Their Stakeholder**: The University Academic Dean & Provost.
* **Their Mission**: Find the exact tipping point where students collapse into D or F grades.

### 🔍 Ground Truth (What the Data Actually Shows):
* The critical cliff edge is **15 hours of study per week**.
* Students below 15 hours have an **>80% failure rate (D or F)**.
* **The Nuance**: High attendance alone cannot save a student who studies <10 hours (you can sit in class passively and still fail). But high study hours almost always guarantees a C or better even with mediocre attendance.

### 🎯 2 Sharp Questions to Ask Them:
1. *"You identified 15 hours as the threshold. What about attendance? If a student attends 95% of classes but only studies 8 hours a week, will they pass according to your chart?"*
2. *"Why did your team use a scatter plot with color hue instead of just showing the average score for each grade in a bar chart?"*
   * *Ideal Answer*: *"A bar chart of averages hides individual student variance. The scatter plot lets the Dean see every student and identify exact boundary clusters."*

### 😈 Devil's Advocate Objection:
> *"Provost speaking: Hiring tutors costs our university $50,000. If we set the alert threshold at 15 hours, how many false alarms (students who study <15h but still passed) are you going to force into tutoring?"*

### 🎓 Teacher's 30-Second Summary to the Class:
> *"Notice what Group 1 did: They didn't just show data; they identified a **decision boundary**. In machine learning, this scatter plot is the foundation of classification algorithms like Logistic Regression and Support Vector Machines (SVM). Great job."*

---

## 🧠 GROUP 2: The "Burnout & Mental Health" Taskforce

* **Their Stakeholder**: The Director of Campus Counseling & Student Wellbeing.
* **The Mission**: Map student stress across 12 weeks and schedule timely interventions.

### 🔍 Ground Truth (What the Data Actually Shows):
* **Week 6**: Stress surges to **7.5/10** (Midterm week).
* **Week 7**: Immediate crash—study hours drop from **18h down to 11h** (post-exam exhaustion/burnout).
* **Week 11–12**: Desperation cramming—study hours rocket to **30h+** while stress spikes to an alarming **9.4/10**.
* **Best Intervention Timing**: **Week 5** (preventative coping strategies before midterms) and **Week 10** (time management before finals). Intervening in Week 12 is too late!

### 🎯 2 Sharp Questions to Ask Them:
1. *"Look at Week 7 where study hours plummet to 11 hours. Did students suddenly get lazy, or is this psychological burnout? How does your chart support your claim?"*
2. *"You used a dual-axis chart (left axis for hours/score, right axis for stress). Dual-axis charts are often criticized in data science. What is the risk of having two different scales on one plot?"*
   * *Ideal Answer*: *"If the scales are manipulated, it can create a false visual illusion that two unrelated lines are crossing or identical in magnitude."*

### 😈 Devil's Advocate Objection:
> *"Director speaking: If stress peaks in Week 12, why shouldn't I just put all my counselors in the library during Week 12 finals?"*
> *(Push them to argue that Week 12 is reactive; preventative workshops must happen in Week 5 or 10).*

### 🎓 Teacher's 30-Second Summary to the Class:
> *"Time series is about **lead indicators vs. lag indicators**. Stress leads; burnout lags. When you design line charts, adding shaded zones (`axvspan`) turns a boring line into a human narrative."*

---

## ⚖️ GROUP 3: The "Curriculum & Major Equity" Audit

* **Their Stakeholder**: The Head of the Engineering Curriculum Committee.
* **The Mission**: Determine if Computer Science courses are graded easier than Mechanical Engineering.

### 🔍 Ground Truth (What the Data Actually Shows):
* CS students average **79.5 pts** vs Mechanical at **74.2 pts** (~5.3 point difference).
* However, CS students average **~24 hours of study/week** vs Mechanical at **~14 hours/week**!
* When adjusted for study effort, Mechanical students actually get more "points per hour studied". Grading is completely fair.

### 🎯 2 Sharp Questions to Ask Them:
1. *"Did your horizontal bar chart start its horizontal axis at 0? If you started the axis at 70, how would that distort the Dean's perception?"*
   * *Ideal Answer*: *"If we started at 70, a 5-point difference would look 4 times longer, falsely suggesting CS is wildly superior or inflated."*
2. *"Why did your team use a Horizontal Bar Chart (`barh`) instead of a Vertical Bar Chart?"*
   * *Ideal Answer*: *"Major names like 'Business Analytics' and 'Computer Science' are long. Horizontal bars keep labels readable without awkward 45-degree neck-tilting."*

### 😈 Devil's Advocate Objection:
> *"Curriculum Chair speaking: A 5-point difference is half a letter grade! Shouldn't I force the Computer Science faculty to curve down their exam scores by 5%?"*
> *(Push them to explain that CS students study 10 more hours per week on average).*

### 🎓 Teacher's 30-Second Summary to the Class:
> *"Rule #1 of comparison charts: **Never compare outputs without showing the inputs**. Group 3 showed both final score and study hours side-by-side, preventing an unfair curriculum penalty."*

---

## 🚌 GROUP 4: The "Commuter Student Reality Check"

* **Their Stakeholder**: The Campus Housing & Commuter Student Services Director.
* **The Mission**: Discover what students actually sacrifice when commute times are long.

### 🔍 Ground Truth (What the Data Actually Shows):
* Commute time has a strong negative correlation with **sleep** ($r \approx -0.45$).
* Short commuters ($\le 1.5$h) sleep **~7.2 hours**; long commuters ($>1.5$h) sleep only **~5.5 hours**.
* Study hours remain relatively constant (~2.5h daily). Commuters don't stop studying; **they sacrifice their sleep to keep up!**

### 🎯 2 Sharp Questions to Ask Them:
1. *"Looking at your stacked bar chart of the 24-hour day, why is a Stacked Bar Chart scientifically better than a 5-slice Pie Chart here?"*
   * *Ideal Answer*: *"Human eyes compare lengths along a straight baseline much more accurately than 2D slice angles. On a pie chart, distinguishing 5.5h of classes from 6.2h of leisure is nearly impossible."*
2. *"If long commuters study the same amount of hours as non-commuters, why do their exam scores still drop by 7 points?"*
   * *Answer*: *"Cognitive fatigue and sleep deprivation."*

### 😈 Devil's Advocate Objection:
> *"Housing Director speaking: Dorm rooms cost millions to build. If commuters are still studying their 2.5 hours a day, why should the university invest in commuter sleep pods or transit shuttles?"*

### 🎓 Teacher's 30-Second Summary to the Class:
> *"Composition data (summing to 100% or 24 hours) is easy to bungle. Avoid pie charts for complex budgets. Group 4 proved that 'hidden tradeoffs' are often where the real data science story lives."*

---

## 🗺️ GROUP 5: The "Regional Talent & Admissions" Board

* **Their Stakeholder**: The University Admissions & Scholarship Board.
* **The Mission**: Evaluate regional state performance and spot untapped geographic talent.

### 🔍 Ground Truth (What the Data Actually Shows):
* Out-of-state cohorts (e.g. `Delhi`, `Maharashtra`) often have high average scores (~81–82).
* **The Catch**: Their sample size is tiny ($n \approx 20\text{--}25$ students) compared to local states like `Karnataka` ($n \approx 88$, avg ~76).
* The high average could be **survivorship / selection bias** (only the most ambitious students move across the country).

### 🎯 2 Sharp Questions to Ask Them:
1. *"Delhi has a higher average score than Karnataka on your chart. Does this prove students from Delhi are smarter, or is there a sample size bias?"*
   * *Ideal Answer*: *"Sample size bias. Delhi only has 25 students (likely self-selected top applicants), whereas Karnataka has 88 students covering all performance tiers."*
2. *"How did your lollipop/bubble chart communicate BOTH the average score and the sample size at the same time?"*
   * *Answer*: *"Horizontal position showed score; bubble size or text labels showed student count ($n$)."*

### 😈 Devil's Advocate Objection:
> *"Admissions Dean speaking: Should we cut recruiting in Karnataka and spend our entire marketing budget in Delhi since their average score is 5 points higher?"*
> *(Push them to explain why abandoning your 88-student local pipeline based on a 25-student sample is reckless).*

### 🎓 Teacher's 30-Second Summary to the Class:
> *"Never show an aggregate metric (like mean) without showing the sample weight ($n$). A bubble or lollipop chart solves the 2-variable trap in regional comparisons."*

---

## 🏆 Final Wrap-Up for the Whole Room (Last 2 Minutes):
1. Pick 1 winner: *"The most persuasive analytical pitch today was Group [X] because they connected their visual directly to a budget decision."*
2. Remind them: *"In your future jobs, nobody pays you to write `plt.plot()`. You are paid to convince human beings to make smart decisions using visual evidence. Class dismissed!"*
