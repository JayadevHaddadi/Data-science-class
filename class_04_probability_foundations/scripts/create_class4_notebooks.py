"""Builds the Class 04 notebooks (Probability Foundations).

  01_INSTRUCTOR_concepts.ipynb        - concept demo you screen-share (notes inside, pre-rendered)
  01_STUDENT_concepts.ipynb           - students' follow-along copy (same code, no notes)
  02_INSTRUCTOR_ai_demo.ipynb         - 3 tasks YOU solve live with AI to teach the workflow (answers inside)
  02_STUDENT_ai_demo_followalong.ipynb- students watch/follow; empty cells + AI log template
  03_STUDENT_ai_tasks.ipynb           - 3 tasks students solve themselves WITH AI (little pre-built code)
  03_INSTRUCTOR_ai_tasks_solutions.ipynb - solutions, common AI traps, rubric

Reuses the cell DSL/renderer from Class 03 (nbtools.py). Edit this file, not the .ipynb files.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "class_03_eda_deep_dive", "scripts"))
from nbtools import build, code, md, note, predict, render  # noqa: E402

OUT = os.path.join(HERE, "..", "notebooks")


def save(nb, name):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("Saved", name)


SETUP = code('''
#@title ▶️ Setup — run this cell first { display-mode: "form" }
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams["figure.dpi"] = 110
rng = np.random.default_rng(42)     # fixed seed → everyone sees the same random numbers
print("✅ Setup complete")
''')

# ============================================================================
#  01  CONCEPTS
# ============================================================================
A = []
A += [
    md("""
# 🎲 Class 04 — Probability Foundations
**Probability · Conditional probability · Independence · Bayes' theorem · Random variables · Distributions**

**Our superpower today:** if you can't solve a probability problem with a formula, you can **simulate it** — run the experiment 100,000 times on the computer and count. We will use *both* (formula = exact, simulation = sanity check).
""", "student"),
    md("""
# 🎤 INSTRUCTOR — Concepts notebook (screen-share this one)
Blockquotes are **your notes** (not in the student copy). Suggested pacing for ~100 min *(adjust to your slot)*:

| Min | Part | Key idea |
|---|---|---|
| 0–15 | 1 · Probability concepts | long-run frequency, sample space, events, rules |
| 15–30 | 2 · Conditional probability | "probability *given*"; P(A\\|B) ≠ P(B\\|A) |
| 30–42 | 3 · Independence | P(A∩B)=P(A)P(B); exclusive ≠ independent |
| 42–62 | 4 · **Bayes' theorem** | the base-rate trap — the climax |
| 62–72 | ☕ Break | |
| 72–85 | 5 · Random variables | pmf, E[X], Var(X) |
| 85–100 | 6 · Distributions | Binomial, Poisson, Normal, CLT |

**Rhythm:** every part has a 🔮 PREDICT box → students type guesses in chat *before* you run the cell.
**Next notebooks:** `02_INSTRUCTOR_ai_demo` (you teach the AI workflow) and `03_STUDENT_ai_tasks` (they practise).
""", "instr"),
    SETUP,
]

# ---------------------------------------------------------------- Part 1
A += [
    md("---\n## Part 1 · Probability concepts"),
    md("""
**Probability** = a number between 0 and 1 for how likely an event is. Two ways to think about it:
* **Classical:** (favourable outcomes) ÷ (all equally likely outcomes)
* **Frequentist:** the proportion of times it happens in the *long run*

| Rule | Formula |
|---|---|
| Complement | $P(\\text{not }A) = 1 - P(A)$ |
| Addition | $P(A \\cup B) = P(A) + P(B) - P(A \\cap B)$ |
""", ),
    predict("""
I flip a fair coin 10 times. Will the proportion of heads be *exactly* 0.5? And after 5,000 flips?
**Chat:** "10 flips: ___ , 5000 flips: ___" (always / often / rarely exactly 0.5)""",
            "🎤 The honest answer: even at 5000 flips it's almost never *exactly* 0.5, but it gets very **close**. That is the Law of Large Numbers."),
    code('''
flips = rng.integers(0, 2, size=5000)                  # 1 = heads
running = np.cumsum(flips) / np.arange(1, 5001)        # proportion of heads so far

fig, ax = plt.subplots(figsize=(8, 3.8))
ax.plot(np.arange(1, 5001), running, lw=1.5)
ax.axhline(0.5, color="crimson", ls="--", label="true P(heads) = 0.5")
ax.set_xscale("log"); ax.set_xlabel("number of flips (log scale)"); ax.set_ylabel("proportion of heads")
ax.set_title("Law of Large Numbers: the proportion settles down"); ax.legend()
plt.show()
print("after 10 flips  :", running[9].round(3))
print("after 5000 flips:", running[-1].round(4))
'''),
    note("""
🎤 SAY: "Short runs are wild; long runs are calm. A *probability* is what the proportion converges to. It says nothing certain about the next flip."
⚠️ Gambler's fallacy: a coin that landed heads 5 times is *not* "due" for tails.
"""),
    md("### Sample space: two dice"),
    code('''
die = np.arange(1, 7)
outcomes = pd.DataFrame([(a, b, a + b) for a in die for b in die], columns=["die1", "die2", "total"])
print("number of equally likely outcomes:", len(outcomes))

exact = outcomes["total"].value_counts(normalize=True).sort_index()
sim_totals = rng.integers(1, 7, 100_000) + rng.integers(1, 7, 100_000)
simulated = pd.Series(sim_totals).value_counts(normalize=True).sort_index()
table = pd.DataFrame({"exact": exact, "simulated": simulated}).round(3)

ax = table.plot.bar(figsize=(8, 3.8), rot=0, width=0.8)
ax.set_title("P(total of two dice): formula vs 100,000 simulated rolls"); ax.set_xlabel("total")
plt.show()
table.T
'''),
    md("### Addition rule: 'A or B'"),
    code('''
A_ = outcomes["die1"] == 6          # event A: first die is 6
B_ = outcomes["total"] >= 10        # event B: total is 10 or more
pA, pB, pAB = A_.mean(), B_.mean(), (A_ & B_).mean()
print(f"P(A) = {pA:.3f}   P(B) = {pB:.3f}   P(A and B) = {pAB:.3f}")
print(f"P(A or B) = P(A)+P(B)-P(A and B) = {pA + pB - pAB:.3f}")
print(f"counted directly            = {(A_ | B_).mean():.3f}")
'''),
    note("""
🎤 SAY: "Why subtract P(A and B)? Because the outcomes (6,4), (6,5), (6,6) are in *both* events — adding would count them twice."
"""),
]

# ---------------------------------------------------------------- Part 2
A += [
    md("---\n## Part 2 · Conditional probability\n**P(A | B)** = probability of A *given that we know B happened* — we shrink the world to only the B cases."),
    md("$$P(A\\mid B)=\\frac{P(A\\cap B)}{P(B)}$$"),
    code('''
# 400 students: did they join a study group, and did they pass?
students = pd.DataFrame({
    "study_group": ["Yes"] * 150 + ["No"] * 250,
    "result": ["Pass"] * 120 + ["Fail"] * 30 + ["Pass"] * 150 + ["Fail"] * 100,
})
counts = pd.crosstab(students["study_group"], students["result"], margins=True)
display(counts)
display(pd.crosstab(students["study_group"], students["result"], normalize="all").round(3))
'''),
    predict("""
From the table: P(pass) overall is 270/400 = 0.675.

**Chat:** is P(pass | joined a study group) **higher, lower, or the same**? Roughly what number?""",
            "🎤 Expect 'higher'. Compute: 120/150 = 0.80."),
    code('''
p_pass = (students["result"] == "Pass").mean()
p_pass_given_group = (students[students["study_group"] == "Yes"]["result"] == "Pass").mean()
p_pass_given_none = (students[students["study_group"] == "No"]["result"] == "Pass").mean()
p_group_given_pass = (students[students["result"] == "Pass"]["study_group"] == "Yes").mean()

print(f"P(pass)                  = {p_pass:.3f}")
print(f"P(pass | study group)    = {p_pass_given_group:.3f}")
print(f"P(pass | no study group) = {p_pass_given_none:.3f}")
print(f"P(study group | pass)    = {p_group_given_pass:.3f}   ← NOT the same as P(pass | study group)!")
'''),
    note("""
🎤 SAY: "Look at the last two lines. 80% of study-group students pass. But only 44% of *passing* students were in a study group. **P(A|B) is not P(B|A).** Confusing these is the single most common probability mistake — and it's exactly what trips people up in Bayes later."
(This is *association*, not proof that study groups cause passing — callback to Class 03.)
"""),
    md("### Same idea with dice"),
    code('''
cond = outcomes[outcomes["die1"] % 2 == 0]               # shrink the world: first die is even
print("P(total = 8)                 =", round((outcomes["total"] == 8).mean(), 4), "  (= 5/36)")
print("P(total = 8 | first die even) =", round((cond["total"] == 8).mean(), 4), "  (= 3/18)")
'''),
    md("""
**Multiplication rule** (rearranged): $P(A\\cap B)=P(A\\mid B)\\,P(B)$ — used for chains of events, e.g. drawing cards one after another.
"""),
]

# ---------------------------------------------------------------- Part 3
A += [
    md("---\n## Part 3 · Independence\n**A and B are independent** if knowing B doesn't change the probability of A: $P(A\\cap B)=P(A)\\,P(B)$ (equivalently $P(A\\mid B)=P(A)$)."),
    code('''
def check_independence(A, B, label):
    pA, pB, pAB = A.mean(), B.mean(), (A & B).mean()
    verdict = "INDEPENDENT ✅" if np.isclose(pAB, pA * pB) else "DEPENDENT ❌"
    print(f"{label}\\n   P(A)={pA:.3f}  P(B)={pB:.3f}  P(A)P(B)={pA*pB:.3f}  P(A and B)={pAB:.3f}  →  {verdict}\\n")

check_independence(outcomes["die1"] % 2 == 0, outcomes["total"] == 7,
                   "A: first die even   B: total is 7")
check_independence(outcomes["die1"] == 6, outcomes["total"] >= 10,
                   "A: first die is 6   B: total ≥ 10")
check_independence(outcomes["die1"] == 1, outcomes["die1"] == 6,
                   "A: first die is 1   B: first die is 6  (mutually exclusive)")
'''),
    predict("""
Before the output above: do you think **'first die is even'** and **'total is 7'** are independent?""",
            "🎤 Most say 'no'. The check says yes: whatever the first die shows, exactly one second-die value makes 7, so P(7) = 1/6 regardless."),
    note("""
🎤 SAY: "**Mutually exclusive is NOT independent.** If A happens, B *can't* — so knowing A tells you a lot about B. Exclusive events with positive probability are always dependent."
"""),
    md("### Cards: with vs without replacement"),
    code('''
p_ace = 4 / 52
print("P(2nd card is ace | 1st was ace), WITH replacement    :", round(4 / 52, 4), "(same as P(ace) → independent)")
print("P(2nd card is ace | 1st was ace), WITHOUT replacement :", round(3 / 51, 4), "(deck changed → dependent)")

deck = np.array([1] * 4 + [0] * 48)                      # 1 = ace
draws = np.array([rng.permutation(deck)[:2] for _ in range(100_000)])
first_ace = draws[:, 0] == 1
print("simulated, without replacement:", round(draws[first_ace, 1].mean(), 4))
'''),
]

# ---------------------------------------------------------------- Part 4
A += [
    md("---\n## Part 4 · Bayes' theorem — updating beliefs with evidence"),
    md("""
$$P(H\\mid E)=\\frac{P(E\\mid H)\\,P(H)}{P(E)} \\qquad P(E)=P(E\\mid H)P(H)+P(E\\mid \\neg H)P(\\neg H)$$

*prior* $P(H)$ → see evidence $E$ → *posterior* $P(H\\mid E)$
""", ),
    md("""
### 🩺 The medical test puzzle
A disease affects **1 %** of people. A test is **95 % sensitive** (positive for 95 % of sick people) and has a **5 % false-positive rate** (positive for 5 % of healthy people).
**You test positive.** What's the probability you actually have the disease?
"""),
    predict("**Gut answer in chat — don't calculate!** A) ~95 % &nbsp; B) ~80 % &nbsp; C) ~50 % &nbsp; D) ~16 % &nbsp; E) ~5 %",
            "🎤 Most say 95%. Many doctors do too. Collect the votes and keep them visible."),
    code('''
prevalence, sensitivity, false_pos = 0.01, 0.95, 0.05

p_positive = sensitivity * prevalence + false_pos * (1 - prevalence)
posterior = sensitivity * prevalence / p_positive
print(f"P(positive test)           = {p_positive:.4f}")
print(f"P(disease | positive test) = {posterior:.3f}   ← about {posterior:.0%}")
'''),
    md("### Why? Think in *natural frequencies*: 10,000 people"),
    code('''
N = 10_000
sick = int(N * prevalence)
healthy = N - sick
tp = round(sick * sensitivity)           # sick & positive
fp = round(healthy * false_pos)          # healthy & positive
print(f"sick: {sick}  → {tp} test positive, {sick - tp} test negative")
print(f"healthy: {healthy} → {fp} test positive (FALSE alarms), {healthy - fp} test negative")
print(f"\\nAmong all {tp + fp} positive tests, only {tp} are truly sick  →  {tp / (tp + fp):.1%}")

fig, ax = plt.subplots(figsize=(7, 3.2))
ax.barh(["positive tests"], [tp], color="crimson", label=f"truly sick ({tp})")
ax.barh(["positive tests"], [fp], left=[tp], color="lightgray", label=f"healthy — false alarms ({fp})")
ax.set_title("Who is in the 'positive' group?"); ax.legend(loc="lower right")
plt.show()
'''),
    note("""
🎤 SAY: "The healthy group is **99 times bigger**, so even a small 5% false-positive rate produces ~495 false alarms — far more than the 95 true positives. **Ignoring the base rate (prior) is the #1 Bayes mistake.**"
🎤 Reveal the poll: "If you said 95%, you're in excellent company."
"""),
    md("### Check it by simulation (1,000,000 people)"),
    code('''
n = 1_000_000
is_sick = rng.random(n) < prevalence
test_pos = np.where(is_sick, rng.random(n) < sensitivity, rng.random(n) < false_pos)
print("simulated P(disease | positive) =", round(is_sick[test_pos].mean(), 3))
'''),
    md("### How much does the prior matter?"),
    code('''
prev = np.linspace(0.001, 0.5, 300)
post = sensitivity * prev / (sensitivity * prev + false_pos * (1 - prev))
fig, ax = plt.subplots(figsize=(7.5, 4))
ax.plot(prev * 100, post * 100)
ax.scatter([1], [posterior * 100], color="crimson", zorder=3, label="our case: 1% prevalence → 16%")
ax.set_xlabel("how common the disease is (%)"); ax.set_ylabel("P(disease | positive test) %")
ax.set_title("Same test, different base rates"); ax.legend()
plt.show()
'''),
    md("### Updating again: a second independent positive test"),
    code('''
prior_2 = posterior                         # yesterday's posterior is today's prior
post_2 = sensitivity * prior_2 / (sensitivity * prior_2 + false_pos * (1 - prior_2))
print(f"after 1 positive test : {posterior:.1%}")
print(f"after 2 positive tests: {post_2:.1%}")
'''),
    note("""
🎤 SAY: "**Bayes = a machine for updating.** Each new piece of evidence turns the old posterior into the new prior. This is how spam filters, medical diagnosis and many ML models work. *(Spam filters are one of the tasks in the student AI homework.)*"
☕ Break after this part.
"""),
    md("---\n## ☕ Break"),
]

# ---------------------------------------------------------------- Part 5
A += [
    md("---\n## Part 5 · Random variables\nA **random variable** $X$ turns outcomes into numbers (e.g. *total of two dice*). A **pmf** lists $P(X=x)$ for each value."),
    code('''
pmf = outcomes["total"].value_counts(normalize=True).sort_index()
x = pmf.index.to_numpy(); p = pmf.to_numpy()

mean = (x * p).sum()                       # E[X]
var = ((x - mean) ** 2 * p).sum()          # Var(X) = E[(X - mu)^2]
print(f"E[X]   = {mean:.2f}")
print(f"Var(X) = {var:.3f}    SD = {np.sqrt(var):.3f}")

fig, ax = plt.subplots(figsize=(7.5, 3.6))
ax.bar(x, p, color="steelblue"); ax.axvline(mean, color="crimson", ls="--", label=f"E[X] = {mean:.0f}")
ax.set_title("pmf of X = total of two dice"); ax.set_xlabel("x"); ax.set_ylabel("P(X = x)"); ax.legend()
plt.show()
'''),
    note("""
🎤 SAY: "E[X] is the **long-run average**, not a value you expect to see on any single roll. Here you *can* roll a 7, but for a fair die the expected value 3.5 can never occur."
"""),
    md("### Expected value = what the sample average converges to"),
    code('''
rolls = rng.integers(1, 7, 20_000) + rng.integers(1, 7, 20_000)
running_mean = np.cumsum(rolls) / np.arange(1, len(rolls) + 1)
fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(running_mean); ax.axhline(7, color="crimson", ls="--", label="E[X] = 7")
ax.set_xscale("log"); ax.set_xlabel("number of rolls"); ax.set_ylabel("average total"); ax.legend()
ax.set_title("Running average → E[X]")
plt.show()
print("E[2X + 1] =", round(2 * mean + 1, 3), "   Var(2X + 1) =", round(4 * var, 3), "  (linear transformations: E scales, Var scales by 4)")
'''),
]

# ---------------------------------------------------------------- Part 6
A += [
    md("---\n## Part 6 · Probability distributions\nA **distribution** is the pmf/pdf pattern a random variable follows. Three workhorses today."),
    md("### 6.1 Binomial — number of successes in *n* independent yes/no trials"),
    code('''
n, p = 10, 0.3          # e.g. 10 customers, each buys with probability 0.3
k = np.arange(0, n + 1)
fig, ax = plt.subplots(figsize=(7.5, 3.6))
ax.bar(k, stats.binom.pmf(k, n, p), color="steelblue")
ax.set_title(f"Binomial(n={n}, p={p}): customers who buy"); ax.set_xlabel("number of buyers")
plt.show()
print("mean = n·p =", n * p, "   SD =", round(np.sqrt(n * p * (1 - p)), 3))
print("P(exactly 3)   =", round(stats.binom.pmf(3, n, p), 4))
print("P(at least 5)  =", round(1 - stats.binom.cdf(4, n, p), 4), "  ← 'at least 5' = 1 - P(X ≤ 4)")
print("simulated P(at least 5):", round((rng.binomial(n, p, 200_000) >= 5).mean(), 4))
'''),
    note("""
⚠️ Point out the **cdf trap**: `cdf(4)` is P(X ≤ 4), so P(X ≥ 5) = 1 − cdf(**4**), not cdf(5). Off-by-one errors with ≥ / > are a favourite AI mistake — we'll see one in the AI demo.
"""),
    md("### 6.2 Poisson — number of events in a fixed time window"),
    code('''
lam = 3                 # e.g. emails per hour
k = np.arange(0, 12)
fig, ax = plt.subplots(figsize=(7.5, 3.6))
ax.bar(k, stats.poisson.pmf(k, lam), color="darkorange")
ax.set_title(f"Poisson(λ={lam}): emails in one hour"); ax.set_xlabel("number of emails")
plt.show()
print("mean = variance = λ =", lam)
print("P(no emails in an hour) =", round(stats.poisson.pmf(0, lam), 4), "  (= e^-3)")
'''),
    md("### 6.3 Normal — the bell curve"),
    code('''
mu, sigma = 170, 8       # heights in cm
dist = stats.norm(mu, sigma)
xs = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 400)
fig, ax = plt.subplots(figsize=(8, 3.8))
ax.plot(xs, dist.pdf(xs), color="black")
for k_, c in zip([1, 2, 3], ["#2a9d8f", "#e9c46a", "#e76f51"]):
    ax.fill_between(xs, dist.pdf(xs), where=(xs > mu - k_ * sigma) & (xs < mu + k_ * sigma), alpha=0.35, color=c,
                    label=f"within {k_} SD: {dist.cdf(mu + k_ * sigma) - dist.cdf(mu - k_ * sigma):.1%}")
ax.set_title("Normal(170, 8): the 68–95–99.7 rule"); ax.set_xlabel("height (cm)"); ax.legend()
plt.show()

z = (185 - mu) / sigma
print(f"z-score of 185 cm = {z:.2f}   P(height > 185) = {1 - dist.cdf(185):.4f}")
print(f"the tallest 5% are taller than {dist.ppf(0.95):.1f} cm   (ppf = inverse of cdf)")
'''),
    md("### 6.4 Why the bell curve is everywhere: the Central Limit Theorem"),
    predict("""
Individual draws from an **Exponential** distribution are very skewed (lots of small values, a long tail).

**What will the histogram of the *average of 30 draws* look like?** A) still skewed &nbsp; B) bell-shaped &nbsp; C) flat""",
            "🎤 Answer: bell-shaped."),
    code('''
fig, axes = plt.subplots(1, 3, figsize=(12, 3.2), sharex=True)
for ax, size in zip(axes, [1, 5, 30]):
    means = rng.exponential(1.0, size=(20_000, size)).mean(axis=1)
    ax.hist(means, bins=50, color="steelblue", density=True)
    ax.set_title(f"average of {size} draw{'s' if size > 1 else ''}")
axes[0].set_xlim(0, 4)
fig.suptitle("Central Limit Theorem: averages become bell-shaped", y=1.03)
plt.show()
'''),
    note("""
🎤 SAY: "No matter how weird the original distribution, the **average** of many independent draws is approximately Normal. That's why the bell curve is the default for sample means — and why statistics works."
"""),
    md("""
### Cheat-sheet: which distribution?
| Situation | Distribution | Parameters |
|---|---|---|
| One yes/no trial | Bernoulli | p |
| # successes in *n* independent yes/no trials | **Binomial** | n, p |
| # events in a fixed time/space window | **Poisson** | λ |
| Measurements clustered around a mean | **Normal** | μ, σ |
| Averages of many draws | ≈ Normal (CLT) | |
"""),
    md("""
---
## 🏁 Wrap-up
1. **P(A|B) ≠ P(B|A)** — always say which is which.
2. **Independent ≠ mutually exclusive.**
3. **Bayes: don't forget the base rate.**
4. **If the formula scares you, simulate it.**

➡️ Next: you will learn how to use **AI** to solve probability problems — *and how to catch it when it's wrong.*
"""),
]

# ============================================================================
#  02  AI DEMO  (instructor solves 3 tasks live, teaching the workflow)
# ============================================================================
B = []
B += [
    md("""
# 🤖 Using AI to Solve Probability Problems — Live Demo
**Today you learn a *workflow*, not a trick.** AI is a very fast but sometimes confidently wrong assistant. Your job: **steer it, then verify it.**
""", "student"),
    md("""
# 🎤 INSTRUCTOR — AI Demo notebook
**Goal:** model the full workflow on 3 tasks while students watch (and follow along in their copy `02_STUDENT_ai_demo_followalong`).

**How to run it (~35–40 min):**
1. Read the workflow (5 steps) — 3 min.
2. For each task: read the task → students predict → paste the **weak prompt** into your AI tool of choice and show the answer → paste the **strong prompt** → run the **verification** cell → name the lesson.
3. Use whatever AI you like (Claude, ChatGPT, Gemini…). **Answers differ from run to run** — the "what to look for" boxes tell you what to check, and the verification cells hold the ground truth.

> I deliberately did *not* paste fake AI transcripts: do it live; it's more convincing, and real mistakes are the best teacher. If the AI gets a task right, that's fine: the lesson is *"how do I know?"*
""", "instr"),
    SETUP,
    md("""
## The 5-step AI workflow  **U-P-R-V-R**
| Step | What you do | Why |
|---|---|---|
| **1 · Understand** | Restate the problem in your own words. List what's *given* and what's *asked*. | If you can't say it, you can't check it |
| **2 · Prompt** | Give context + all numbers + the exact question. Ask for: assumptions, steps, formula **and** Python code | Vague in → vague out |
| **3 · Run** | Run the code yourself. Never copy results you didn't execute | AI can describe code that doesn't work |
| **4 · Verify** | Simulation · sanity bounds (is 0 ≤ p ≤ 1? plausible size?) · try a simpler case · ask the AI to *attack its own answer* | The step that makes you a data scientist |
| **5 · Reflect** | Log: what did AI get right/wrong? What did you change? | You learn the failure patterns |

### ✍️ Anatomy of a strong prompt
```
ROLE/CONTEXT : I'm a data science student learning probability.
PROBLEM      : <paste the full problem with ALL numbers>
CONSTRAINTS  : Use Python (numpy/scipy). State your assumptions.
DELIVERABLE  : 1) the formula  2) the numeric answer  3) code  4) a simulation that checks it
CHECK        : Tell me one way your answer could be wrong.
```
"""),
]

# ------------------------------------------------ D1
B += [
    md("---\n# Demo Task 1 · The false-alarm test (Bayes)"),
    md("""
> **Task:** A factory machine is faulty **2 %** of the time. A sensor flags 90 % of faulty runs, and also wrongly flags **8 %** of healthy runs.
> The sensor flags a run. **What's the probability the machine is actually faulty?**
"""),
    predict("**Gut check in chat** — a number between 0 and 100 %. *(Don't compute.)*"),
    md("""
### ❌ Weak prompt
```
what is the chance the machine is faulty if the sensor flags it
```
### ✅ Strong prompt *(copy → AI)*
```
I'm learning Bayes' theorem. A machine is faulty 2% of the time. A sensor flags 90% of faulty runs
and wrongly flags 8% of healthy runs. The sensor flags a run.
1) Write the quantities as P(...) notation (prior, likelihood, false positive rate).
2) Compute P(faulty | flagged) with Bayes' theorem, showing P(flagged).
3) Give Python code, and a simulation of 1,000,000 runs that checks the result.
4) Tell me one common mistake people make on this kind of problem.
```
""", ),
    note("""
👀 **What to look for:** AI almost always gets Bayes problems right, so the lesson here is the *prompt structure* and the *verification*: the AI should mention that P(flagged) must include the false alarms from the 98 % healthy runs. Ask it: "what would your answer be if the machine were faulty 20 % of the time?" → shows the base-rate effect.
"""),
    code('''
# ---- our verification (ground truth) ----
prior, sens, fpr = 0.02, 0.90, 0.08
p_flag = sens * prior + fpr * (1 - prior)
exact = sens * prior / p_flag

n = 1_000_000
faulty = rng.random(n) < prior
flagged = np.where(faulty, rng.random(n) < sens, rng.random(n) < fpr)
print(f"exact (Bayes)  : {exact:.4f}")
print(f"simulation     : {faulty[flagged].mean():.4f}")
'''),
    note("""
🎤 LESSON: "The AI's formula and our simulation agree → now I **trust** it. Agreement of two independent methods is the cheapest quality check you have." (Exact ≈ 0.186.)
"""),
]

# ------------------------------------------------ D2
B += [
    md("---\n# Demo Task 2 · The call centre (choosing the distribution)"),
    md("""
> **Task:** A call centre receives on average **4 calls per minute**, at random times. **What's the probability of getting *at least 7* calls in a given minute?**
"""),
    predict("Which **distribution** would you use (Binomial / Poisson / Normal)? And do you expect the answer to be closer to 1 %, 10 % or 40 %?"),
    md("""
### ✅ Strong prompt *(copy → AI)*
```
A call centre gets an average of 4 calls per minute at random times.
1) Which probability distribution models the number of calls in a minute, and WHY (state the assumptions)?
2) Compute P(X >= 7) with scipy. Be explicit about whether you use cdf(6) or cdf(7) and why.
3) Verify with a simulation of 500,000 minutes.
```
""", ),
    note("""
👀 **What to look for (common AI traps):**
• Off-by-one: P(X ≥ 7) = 1 − cdf(**6**). Some answers use cdf(7), which computes P(X > 7).
• Wrong distribution (Binomial without an n; Normal approximation giving a slightly different answer).
👉 If the AI got it right, ask: "Now P(X > 7)?" and ask students whether the number should change — it should.
"""),
    code('''
lam = 4
right = 1 - stats.poisson.cdf(6, lam)       # P(X >= 7)
wrong = 1 - stats.poisson.cdf(7, lam)       # P(X >= 8)  <- the classic off-by-one
sim = (rng.poisson(lam, 500_000) >= 7).mean()
print(f"P(X >= 7) exact      : {right:.4f}")
print(f"P(X >= 7) simulation : {sim:.4f}")
print(f"(off-by-one version) : {wrong:.4f}   <- this is actually P(X >= 8)")
'''),
    note("""
🎤 LESSON: "Same code, one number different, a wrong answer that *looks* just as confident. A simulation caught it — **always verify the boundary (≥ vs >).**"
"""),
]

# ------------------------------------------------ D3
B += [
    md("---\n# Demo Task 3 · Monty Hall with a twist (read the problem carefully!)"),
    md("""
> **Task:** There are 3 doors: 1 car, 2 goats. You pick door 1. The host **does not know** where the car is. He opens one of the other doors **at random** — and it happens to show a **goat**. You may switch to the remaining door.
> **What is the probability of winning the car if you switch?**
"""),
    predict("Classic Monty Hall says 'switch → 2/3'. **Does the answer change here?** A) still 2/3 &nbsp; B) 1/2 &nbsp; C) 1/3"),
    md("""
### ❌ Weak prompt → AI pattern-matches the famous version
```
monty hall problem, should I switch?
```
### ✅ Strong prompt *(copy → AI)*
```
3 doors, one car. I pick door 1. The host does NOT know where the car is and opens one of the other
two doors at random. He opens door 3 and it shows a goat.
1) Is this the same as the classic Monty Hall problem? Explain precisely what differs.
2) Compute P(car behind door 2 | host randomly opened door 3 and showed a goat) using Bayes.
3) Simulate it: simulate many games, KEEP ONLY the games where the host's random door shows a goat,
   and estimate the win rate of switching.
```
""", ),
    note("""
👀 **What to look for:** a *weak* prompt usually gets the classic answer, 2/3 — right for the classic problem, wrong here. The strong prompt forces the AI to notice "host does not know".
"""),
    code('''
n = 1_000_000
car = rng.integers(1, 4, n)                         # door hiding the car (you always pick door 1)
# --- classic: host KNOWS and always opens a goat door ---
switch_classic_win = (car != 1)                     # switching wins iff your first pick was wrong
print("classic Monty Hall, switch wins:", round(switch_classic_win.mean(), 4))

# --- twist: host opens door 2 or 3 at random, may reveal the car ---
opened = rng.integers(2, 4, n)
shows_goat = opened != car                          # keep only games where he happened to reveal a goat
other_door = np.where(opened == 2, 3, 2)
switch_win = (car == other_door)
print("twist (host doesn't know), switch wins | goat shown:", round(switch_win[shows_goat].mean(), 4))
print("share of games discarded because the car was revealed:", round(1 - shows_goat.mean(), 3))
'''),
    note("""
🎤 LESSON: "The *information-generating process* matters. Same picture, different rules → different probability. AI answers the famous problem it recognises, not necessarily the one you asked. **Precise problem statements + verification** beat any magic prompt." (Twist answer: 1/2.)
"""),
    md("""
---
## 🧾 Your AI log (every task, every time)
| Field | Example |
|---|---|
| **Prompt I used** | (paste) |
| **What the AI answered** | (summary + number) |
| **How I verified** | simulation / simpler case / second method |
| **What was wrong or missing** | e.g. off-by-one, wrong distribution |
| **What I changed** | |
"""),
    md("""
## 🎓 Take-aways
1. **Give AI the whole problem with numbers**, ask for assumptions, formula, code *and* a simulation.
2. **Never trust a number you haven't verified** — simulation is your best friend in probability.
3. **Watch the usual suspects:** P(A|B) vs P(B|A), ≥ vs >, wrong distribution, the base rate, the *exact* wording.
4. **You are accountable for the answer, not the AI.** Log what you checked.

➡️ Now it's your turn: open **`03_STUDENT_ai_tasks`**.
"""),
]

# ============================================================================
#  03  STUDENT AI TASKS
# ============================================================================
C = []
C += [
    md("""
# 🧠 AI-Assisted Probability Tasks — Your Turn
**3 tasks · use any AI tool you like · you are graded on *verification and judgement*, not just the answer**

### Rules of the game
1. ✅ **You may (and should) use AI** to help — ChatGPT, Claude, Gemini, Copilot, anything.
2. 🔁 Follow the workflow from the demo: **Understand → Prompt → Run → Verify → Reflect**.
3. 🧪 For **every** task you must *verify the AI's answer yourself in code* — a simulation or a second method. An unverified answer gets no marks for verification.
4. 🧾 Fill in the **AI log** for every task (prompt, what the AI said, how you verified, what was wrong).
5. ✍️ Final answers must be **in your own words** (one sentence a non-expert would understand).

### Scoring per task
| Criterion | Points |
|---|---|
| Correct final answer | 40 % |
| Verification (simulation / second method that really checks the answer) | 30 % |
| AI log + critical thinking (you found/considered where AI could be wrong) | 30 % |

> **Hint toolbox (names only, you write the code):** `numpy.random.default_rng`, `rng.random`, `rng.choice`, `rng.binomial`, `scipy.stats.norm`, `.cdf()`, `.ppf()`, `.pmf()`, `np.mean`, `matplotlib`.
"""),
    SETUP,
]

TASK_LOG = """
### 🧾 AI log — Task {n}
| Field | Your entry |
|---|---|
| **Prompt I used** | |
| **What the AI answered (number + method)** | |
| **How I verified it** | |
| **Where AI was wrong / could be wrong** | |
| **What I changed** | |
"""

C += [
    md("---\n# Task 1 · The spam filter (Bayes + independence)"),
    md("""
**Scenario.** 40 % of incoming emails are spam. The word **"free"** appears in 60 % of spam emails and in 5 % of legitimate ("ham") emails.
The word **"winner"** appears in 30 % of spam and 2 % of ham.

**Questions**
1. An email contains **"free"**. What is the probability it is spam?
2. An email contains **both "free" and "winner"**. What is the probability it is spam? *(Assume the words appear independently **within** each class — this is the "naive Bayes" assumption.)*
3. In **one sentence**: what could go wrong if "free" and "winner" tend to appear together in the same spam emails?
"""),
    md("**Your understanding (own words — what's given, what's asked):**\n\n*(double-click to write)*"),
    code("# your code / verification here\n"),
    code("# your simulation here\n"),
    md("**Final answers (own words):**\n\n1. …\n2. …\n3. …"),
    md(TASK_LOG.format(n=1)),

    md("---\n# Task 2 · The casino game (random variables)"),
    md("""
**Scenario.** You pay **₹5** to play. You roll one fair six-sided die:
* roll a **6** → you win **₹10**
* roll a **4 or 5** → you win **₹3**
* anything else → you win **₹0**

**Questions**
1. What is the **expected winnings** per play (before paying), and the **expected profit** after paying ₹5?
2. What are the **variance and standard deviation** of the winnings?
3. What is the **probability you make a profit** in a single play?
4. What **entry price** would make the game fair?
5. Plot the **running average profit** over 10,000 simulated plays. What does it converge to?
"""),
    md("**Your understanding (own words):**\n\n*(double-click to write)*"),
    code("# your code / verification here\n"),
    code("# your simulation + plot here\n"),
    md("**Final answers (own words):**\n\n1. …\n2. …\n3. …\n4. …\n5. …"),
    md(TASK_LOG.format(n=2)),

    md("---\n# Task 3 · The exam curve (Normal distribution)"),
    md("""
**Scenario.** Scores on a big exam are approximately **Normal with mean 65 and standard deviation 10**.

**Questions**
1. What fraction of students score **above 80**?
2. What fraction score **between 55 and 75**? (How does it compare with the 68 % rule?)
3. The top **10 %** receive an A. What is the **minimum score** for an A?
4. A student scored 52. What is their **z-score** and approximate **percentile**?
5. **Draw** the bell curve and shade the region for question 1.
6. *Bonus:* if you pick **25 students** at random, what is the probability that their **average** score is above 68? *(Hint: what is the distribution of an average?)*
"""),
    md("**Your understanding (own words):**\n\n*(double-click to write)*"),
    code("# your code / verification here\n"),
    code("# your simulation + plot here\n"),
    md("**Final answers (own words):**\n\n1. …\n2. …\n3. …\n4. …\n5. (plot above)\n6. …"),
    md(TASK_LOG.format(n=3)),
    md("""
---
## 📤 Before you submit
- [ ] Every task has a **simulation or second method** I ran myself
- [ ] Every task has a filled **AI log**
- [ ] I wrote final answers in **my own words**
- [ ] Notebook runs from top to bottom (**Runtime → Run all**)
"""),
]

# ============================================================================
#  03  INSTRUCTOR SOLUTIONS
# ============================================================================
D = []
D += [
    md("""
# 🎤 INSTRUCTOR — Solutions & Rubric for `03_STUDENT_ai_tasks`
Everything below is **instructor only**. Run all cells for exact numbers.
""", "instr"),
    SETUP,
    md("## Task 1 · Spam filter — solution", "instr"),
    code('''
p_spam = 0.40
free_s, free_h = 0.60, 0.05
win_s, win_h = 0.30, 0.02

# Q1
num = free_s * p_spam
den = num + free_h * (1 - p_spam)
print(f"Q1  P(spam | free)           = {num / den:.4f}")

# Q2 (naive Bayes: words independent within each class)
num2 = free_s * win_s * p_spam
den2 = num2 + free_h * win_h * (1 - p_spam)
print(f"Q2  P(spam | free & winner)  = {num2 / den2:.4f}")

# simulation of Q1 and Q2
n = 2_000_000
spam = rng.random(n) < p_spam
free = np.where(spam, rng.random(n) < free_s, rng.random(n) < free_h)
winner = np.where(spam, rng.random(n) < win_s, rng.random(n) < win_h)
print(f"sim Q1 = {spam[free].mean():.4f}    sim Q2 = {spam[free & winner].mean():.4f}")
''', "instr"),
    md("""
**Answers:** Q1 ≈ **0.889** · Q2 ≈ **0.992**.
**Q3:** if the words are positively correlated *within* spam, then seeing "winner" after "free" is less surprising than the independence assumption claims, so naive Bayes **double-counts evidence** and is **over-confident** (the true probability would be lower than 0.992).

**Likely AI traps:** (a) confusing P(free | spam) = 0.6 with P(spam | free); (b) forgetting the ham term in the denominator; (c) multiplying probabilities without noting the independence assumption; (d) giving Q2 by multiplying the two *posteriors*.
""", "instr"),

    md("## Task 2 · Casino game — solution", "instr"),
    code('''
x = np.array([10, 3, 0]); p = np.array([1/6, 2/6, 3/6])
E = (x * p).sum(); EX2 = (x**2 * p).sum(); V = EX2 - E**2
print(f"E[winnings] = {E:.4f}   expected profit at price 5 = {E - 5:.4f}")
print(f"Var = {V:.4f}   SD = {np.sqrt(V):.4f}")
print(f"P(profit) = P(win > 5) = P(roll a 6) = {1/6:.4f}    (fair price = {E:.4f})")

rolls = rng.integers(1, 7, 10_000)
win = np.where(rolls == 6, 10, np.where(rolls >= 4, 3, 0))
profit = win - 5
running = np.cumsum(profit) / np.arange(1, 10_001)
fig, ax = plt.subplots(figsize=(8, 3.6))
ax.plot(running); ax.axhline(E - 5, color="crimson", ls="--", label=f"expected profit {E - 5:.2f}")
ax.set_xscale("log"); ax.set_xlabel("plays"); ax.set_ylabel("average profit"); ax.legend()
plt.show()
print("simulated mean profit:", profit.mean().round(3), "  simulated P(profit):", (profit > 0).mean().round(3))
''', "instr"),
    md("""
**Answers:** E[winnings] = **2.667**, expected profit = **−2.333** per play · Var ≈ **12.56**, SD ≈ **3.54** · P(profit) = **1/6 ≈ 0.167** (only a 6 pays more than ₹5) · fair price ≈ **₹2.67** · running average → **−2.33**.

**Likely AI traps:** (a) forgetting to subtract the ₹5 for "profit"; (b) computing the variance of the *profit* vs the *winnings* — same number, but check they say which; (c) counting a ₹3 win as a "profit" (it's still a loss at ₹5); (d) using 4 and 5 as *one* outcome probability 1/6 instead of 2/6.
""", "instr"),

    md("## Task 3 · Exam curve — solution", "instr"),
    code('''
d = stats.norm(65, 10)
print(f"Q1  P(X > 80)        = {1 - d.cdf(80):.4f}")
print(f"Q2  P(55 < X < 75)   = {d.cdf(75) - d.cdf(55):.4f}   (68-95-99.7 rule says ≈0.68)")
print(f"Q3  A cut-off (top 10%) = {d.ppf(0.90):.2f}")
z = (52 - 65) / 10
print(f"Q4  z(52) = {z:.2f}   percentile = {d.cdf(52) * 100:.1f}%")

# Q6: average of 25 students ~ Normal(65, 10/sqrt(25) = 2)
avg = stats.norm(65, 10 / np.sqrt(25))
print(f"Q6  P(mean of 25 > 68) = {1 - avg.cdf(68):.4f}")

sim = rng.normal(65, 10, size=(200_000, 25))
print(f"    simulated Q6        = {(sim.mean(axis=1) > 68).mean():.4f}")
print(f"    simulated Q1 / Q3   = {(sim[:, 0] > 80).mean():.4f} / {np.quantile(sim[:, 0], 0.9):.2f}")

xs = np.linspace(30, 100, 400)
fig, ax = plt.subplots(figsize=(8, 3.6))
ax.plot(xs, d.pdf(xs), color="black"); ax.fill_between(xs, d.pdf(xs), where=xs > 80, color="crimson", alpha=0.4)
ax.set_title("P(score > 80) shaded"); ax.set_xlabel("exam score")
plt.show()
''', "instr"),
    md("""
**Answers:** Q1 ≈ **0.067** · Q2 ≈ **0.683** (55 and 75 are exactly ±1 SD from the mean, so it matches the 68 % rule; if a student's number differs from 0.68 they probably mixed up σ and σ²) · Q3 ≈ **77.8** · Q4 z = **−1.3**, ≈ **9.7th percentile** · Q6 ≈ **0.067** (average has SD 10/√25 = **2**, so 68 is 1.5 SD above the mean).

**Likely AI traps:** (a) using `norm.ppf(0.10)` instead of 0.90 for "top 10 %"; (b) using SD 10 instead of 2 for the *average* in Q6 (the classic!); (c) writing the 68 % rule answer for Q2 without computing; (d) passing variance instead of standard deviation to `scipy.stats.norm`.

*(Notice Q1 and Q6 give the same ≈0.067 — a coincidence of the numbers: 80 is 1.5 SD above for individuals; 68 is 1.5 SD above for averages. Nice discussion point.)*
""", "instr"),
    md("""
---
## 📊 Grading rubric (per task, 100 pts)
| Criterion | 0 | Partial | Full |
|---|---|---|---|
| **Correct answer** (40) | wrong / missing | right method, arithmetic or boundary slip | all numbers correct |
| **Verification** (30) | none or copied AI sim without running | simulation present but doesn't test the stated question | simulation / second method that independently confirms the answer |
| **AI log & judgement** (30) | blank or generic | prompt + answer logged, no critique | names a *specific* place AI could/did go wrong and what they changed |

### 🔎 Spot-check questions for the next class (ask 2–3 students)
* "Show me the prompt you used for Task 3. Did the AI use σ = 10 for the average of 25 students?"
* "How do you know your answer to Task 1 is right if the AI's code had a bug?"
* "What did you change from the AI's answer?" *(if nothing — did you check?)*
* "Which task was AI worst at, and why do you think so?"

### ⚠️ Red flags of un-verified AI use
* Simulation numbers match the exact answer to **every** decimal (probably pasted, not run).
* Log says "AI was correct, no changes" for all three tasks.
* Final answers in the AI's phrasing, not the student's.
""", "instr"),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, cells, aud, do_render in [
        ("01_INSTRUCTOR_concepts.ipynb", A, "instr", True),
        ("01_STUDENT_concepts.ipynb", A, "student", False),
        ("02_INSTRUCTOR_ai_demo.ipynb", B, "instr", True),
        ("02_STUDENT_ai_demo_followalong.ipynb", B, "student", False),
        ("03_STUDENT_ai_tasks.ipynb", C, "student", False),
        ("03_INSTRUCTOR_ai_tasks_solutions.ipynb", D, "instr", True),
    ]:
        nb = build(cells, aud)
        if do_render:
            for p in render(nb):
                print("  ❗", name, "cell error:", p)
        save(nb, name)
