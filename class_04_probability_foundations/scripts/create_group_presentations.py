"""Builds the Class 04 group-presentation notebooks (5 groups x 5 minutes).

  04_STUDENT_group_presentations.ipynb     - cards for 5 groups, 5-minute plan, scoring, checklist
  04_INSTRUCTOR_group_presentations.ipynb  - same + what to listen for and questions to ask

Reuses the cell DSL and the setup cell from create_class4_notebooks.py. Edit this file, not the .ipynb files.
"""
from create_class4_notebooks import OUT, SETUP, build, code, md, note, save  # noqa: F401

G = []
G += [
    md("""
# 🎤 Group Presentations — Probability Foundations
**5 groups · 5 minutes each · one concept per group · explain it so a classmate could use it tomorrow**

### How this works
1. Find **your group number** below and read your card.
2. **Prepare (about 25 min)** in this notebook: fill your cells, make *one* chart, write your notes.
3. **Present (max 5 min)** by sharing your screen. No slides needed: this notebook *is* your presentation.
4. **Everyone in the group speaks**, and one person drives the screen.

### ⏱️ The 5-minute plan (use this for every group)
| Time | What |
|---|---|
| 0:00 – 0:30 | **Hook:** ask the class one question (they answer in chat) |
| 0:30 – 1:30 | **The idea in plain words** (no formulas first!) |
| 1:30 – 3:30 | **Live demo** with *your own* example (not the one from class) |
| 3:30 – 4:15 | **The common mistake** people make |
| 4:15 – 5:00 | **One question for the class** + answer |

### 🏆 How you're scored
| | |
|---|---|
| **Correct** (35 %) | numbers and statements are right |
| **Clear** (30 %) | a classmate who missed class would understand |
| **Own example + verification** (20 %) | your own scenario; you checked the answer with a simulation or a second method |
| **Delivery** (15 %) | within 5 min, everyone speaks, one good chart |

> **You may use AI** to help you prepare, but you must be able to explain every number. Expect a follow-up question from me or from the class. Keep a one-line **AI log** at the end of your section (what you asked, what you changed or corrected).

> **Toolbox (names only, you write the code):** `numpy.random.default_rng`, `rng.random`, `rng.choice`, `rng.binomial`, `rng.poisson`, `pandas.crosstab`, `scipy.stats` (`.pmf`, `.cdf`, `.ppf`), `matplotlib`.
""", "student"),
    md("""
# 🎤 INSTRUCTOR — Group Presentations
Student copy: `04_STUDENT_group_presentations.ipynb`. This copy adds, for each group: **what a strong presentation contains, the mistakes to listen for, and questions you can ask.**

**Suggested flow (about 45–50 min):** 20–25 min prep in breakout rooms or pairs → 5 × (5 min talk + 1–2 min questions) → 2 min wrap-up.
**While they prepare:** visit each room once and ask "show me your own example and the check you ran".
**Timekeeping:** put a countdown on screen; say "1 minute left" at 4:00.
**After each talk:** one praise sentence, one probing question (below), then ask the class "who disagrees with anything?".
""", "instr"),
    SETUP,
]


def group_card(n, title, concept, must, ideas, tools, hook):
    return [
        md(f"---\n# 👥 Group {n} · {title}"),
        md(f"""
**Your concept:** {concept}

**Your presentation must include**
{must}

**Ideas for your own example (pick one or invent):** {ideas}

**Tools you may need:** {tools}

**Hook question for the class (suggestion):** *{hook}*
"""),
        md("**📝 Plan (who says what, which chart, your one question for the class):**\n\n*(double-click to write)*"),
        code("# your example / calculation\n"),
        code("# your simulation or second method that CHECKS the answer, and your chart\n"),
        md("**🧾 AI log (one line each):** prompt I used → what I corrected or double-checked →\n\n*(double-click to write)*"),
    ]


G += group_card(
    1, "Conditional Probability",
    "**P(A | B)**: the probability of A *once we know B has happened*. And why **P(A | B) is not the same as P(B | A)**.",
    """1. A plain-words explanation of "given that".
2. **Your own** small table of counts (for example 200 people: did they do X, did Y happen?), built in pandas.
3. Compute **both** P(A | B) and P(B | A) from the table and show they are **different**.
4. One real-life mistake that comes from mixing them up.""",
    "phone use vs passing a test · umbrella vs rain · gym members vs fitness · players on a team vs scoring",
    "`pd.crosstab`, boolean filtering, `.mean()`",
    "Out of people who carry umbrellas, what fraction are in rain? Out of people in rain, what fraction carry umbrellas? Same number?",
)
G += [note("""
**Strong talk:** shrinks the table to the "given" row/column; two *different* numbers on screen; names the mistake (e.g. "most accidents happen near home, so home is dangerous").
**Listen for:** dividing by the wrong total; saying P(A|B) when they computed P(A and B).
**Questions to ask:**
1. "What is the denominator for P(A|B)? For P(B|A)?"
2. "Could both numbers be equal? When?" *(only if P(A) = P(B))*
3. "How would you check your table numbers by simulation?"
""")]

G += group_card(
    2, "Independence",
    "Two events are **independent** if knowing one doesn't change the chance of the other: **P(A and B) = P(A) × P(B)**. And why **mutually exclusive ≠ independent**.",
    """1. A plain-words explanation, with one example of independent events and one of **dependent** events (e.g. cards with and without replacement).
2. A **numeric test** of independence on your own pair of events (dice, coins or cards), showing P(A)·P(B) versus P(A and B).
3. One example of events that are **mutually exclusive**, and why they are *not* independent.
4. A simulation that confirms your test.""",
    "two coins · die and coin · drawing two cards · weather on two different days · 'first die even' and 'total is 7'",
    "boolean arrays, `.mean()`, `rng.integers`, `rng.choice`",
    "I flip a coin and get heads 5 times in a row. Is tails now more likely? Why or why not?",
)
G += [note("""
**Strong talk:** shows the equation with real numbers for both an "independent" and a "dependent" case; mentions the gambler's fallacy; explains exclusive events *can't* be independent (if A happens, B can't).
**Listen for:** "independent means they don't affect each other" without a number; confusing "exclusive" with "independent".
**Questions to ask:**
1. "A and B are exclusive and both have positive probability: are they independent? Why not?"
2. "Does drawing without replacement break independence? Give me the two numbers."
3. "In the class example, 'first die even' and 'total 7' were independent. Does that surprise you?"
""")]

G += group_card(
    3, "Bayes' Theorem & the Base Rate",
    "**Bayes' theorem** updates a belief with evidence: *prior → evidence → posterior*. And the **base-rate trap**: a good test can still give mostly false alarms when the thing is rare.",
    """1. Your own scenario with 3 numbers: how common something is, how often the test catches it, how often it gives a false alarm.
2. The answer computed **two ways**: with *natural frequencies* (imagine 10,000 people) **and** the formula.
3. A simulation that confirms it.
4. Re-run with **three different base rates** and show how the answer changes (a small table or chart).""",
    "airport scanner · fraud alert on a card · spam filter · plagiarism checker · rapid medical test",
    "`rng.random`, `np.where`, boolean masks, `matplotlib`",
    "A test is 95% accurate and you test positive for a rare condition. Are you 95% likely to have it? Vote in chat.",
)
G += [note("""
**Strong talk:** starts with the surprising result, then explains with the 10,000-people picture; chart of posterior vs base rate; says "the false alarms from the big healthy group outnumber the true positives".
**Listen for:** confusing sensitivity with P(sick | positive); forgetting the false-positive term in the denominator; numbers that don't match their stated inputs.
**Questions to ask:**
1. "What happens to your answer if the false-positive rate halves?"
2. "A second independent positive result: what's the new probability?"
3. "Who should care about this: a doctor, a bank, a security agency? Why?"
""")]

G += group_card(
    4, "Random Variables, Expected Value & Variance",
    "A **random variable** turns outcomes into numbers. **E[X]** is its long-run average; **Var(X)** (and SD) says how much it jumps around.",
    """1. A **game or situation of your own** (not a plain die sum) turned into a random variable X, with its probability table (pmf).
2. **E[X]** and **Var(X) / SD** computed with weighted sums in code.
3. A simulation with a **running-average plot** showing the average heading toward E[X].
4. A plain-words statement of what E[X] does **not** mean (you may never see that value on a single trial).""",
    "raffle ticket · a delivery that takes 1, 2 or 3 days with different probabilities · a game with different prizes · goals in a match",
    "`np.array`, `(x * p).sum()`, `rng.choice(..., p=...)`, `np.cumsum`",
    "I offer a game that costs ₹10 and pays ₹6 on average. Do you play once? 1000 times? What changes?",
)
G += [note("""
**Strong talk:** shows the table of x and P(x) summing to 1; multiplies out E[X] visibly; explains SD as "typical distance from E[X]"; the running-average chart settles.
**Listen for:** probabilities that don't sum to 1; E[X] given as the "most likely value"; variance without squaring.
**Questions to ask:**
1. "Two games have the same E[X] but different SD. Which would you rather play, and when?"
2. "If every prize doubles, what happens to E[X] and the variance?" *(E ×2, Var ×4)*
3. "Why does the running average wobble at the start?"
""")]

G += group_card(
    5, "Which Distribution? Binomial, Poisson & Normal",
    "Picking the right model: **Binomial** (successes out of n tries), **Poisson** (events in a time window), **Normal** (measurements around a mean). *Bonus: why averages look Normal (Central Limit Theorem).*",
    """1. **One real situation each** for Binomial, Poisson and Normal, and a sentence saying *why* that distribution fits (what is fixed, what is counted).
2. A plot of each, with its parameters labelled.
3. **One probability for each, computed with `cdf`/`pmf`**, including one "**at least**" question done correctly (watch the off-by-one!).
4. A simulation that confirms at least one of the three.""",
    "Binomial: free throws, quiz guesses · Poisson: calls per minute, goals per match · Normal: heights, exam scores, delivery times",
    "`scipy.stats.binom / poisson / norm`, `.pmf`, `.cdf`, `.ppf`, `rng.binomial`, `rng.poisson`, `rng.normal`",
    "A shop gets 4 customers per hour on average. Is 'number of customers in an hour' Binomial, Poisson or Normal? Why?",
)
G += [
    note("""
**Strong talk:** each distribution tied to a *story*; states the "fixed n" vs "no maximum" vs "continuous" difference; does `1 - cdf(k-1)` for "at least k" and explains it.
**Listen for:** off-by-one with `cdf`; passing variance instead of SD to `norm`; using Normal for counts.
**Questions to ask:**
1. "Your Poisson example has mean 4. What is its variance? How could you spot a bad Poisson fit from data?" *(variance close to the mean)*
2. "Why can't you ask for P(X = exactly 170.0) for a Normal?" *(continuous: the area under a single point is 0)*
3. "When can a Binomial be approximated by a Normal?" *(n large, p not extreme)*
4. *Bonus:* "What does the CLT say about the average of 30 exam scores?"
"""),
    md("""
---
## ✅ Final checklist (every group)
- [ ] My example is **my own**, not copied from the class notebook
- [ ] I have **one chart** and I can explain what the axes mean
- [ ] I **checked** my answer by simulation or a second method
- [ ] We finished a practice run in **under 5 minutes**
- [ ] Everyone knows their part and one question for the class is ready

## 🤝 Peer feedback (fill in while others present)
| Group | One thing I understood better | One thing that was unclear |
|---|---|---|
| 1 Conditional | | |
| 2 Independence | | |
| 3 Bayes | | |
| 4 Random variables | | |
| 5 Distributions | | |
"""),
]

if __name__ == "__main__":
    save(build(G, "student"), "04_STUDENT_group_presentations.ipynb")
    save(build(G, "instr"), "04_INSTRUCTOR_group_presentations.ipynb")
