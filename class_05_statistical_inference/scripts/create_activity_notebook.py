"""Builds the Class 05 group-activity notebooks (5 groups, statistical inference).

  05_STUDENT_group_activity.ipynb     - task + data + hints only. Students must work out the code themselves.
  05_INSTRUCTOR_group_activity.ipynb  - same, plus worked solutions (pre-rendered) and questions to ask.

Population = the 518 exam scores of the Class 03 campus survey, so every group can compare its
estimates with the known truth.  Edit this file, not the .ipynb files.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "class_03_eda_deep_dive", "scripts"))
from nbtools import build, code, md, note, render, setup_cell  # noqa: E402

OUT = os.path.join(HERE, "..", "notebooks")


def save(nb, name):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("Saved", name)


C = []
C += [
    md("""
# 🔬 Statistical Inference — Group Activity
**5 groups · about 25 min to work · 5 min to present · one topic per group**

### The setting
Pretend the **518 exam scores** in the campus survey are **every student at the university**. That is our *population*, and because we have all of it, **we know the true answer**. Your job is to practise the tools of inference and *check* them against the truth.

### How this works
1. Find **your group** below. Read the task.
2. Work out the code **yourselves**. The notebook only gives you the data and function names to look up. (AI is allowed. Keep a short AI log, and you must be able to explain every number.)
3. Make **one chart** and write **one reporting sentence**.
4. Present in **5 minutes**: *question → what we did → chart → what it means → one thing that surprised us*.

### Scoring
| | |
|---|---|
| **Correct** (35 %) | numbers and statements are right |
| **Clear** (30 %) | a classmate who missed the lecture would understand |
| **Checked against the truth** (20 %) | you compared with the known population value |
| **Delivery** (15 %) | within 5 min, everyone speaks |
""", "student"),
    md("""
# 🎤 INSTRUCTOR — Group Activity (Class 05)
Student copy: `05_STUDENT_group_activity.ipynb`. This copy adds, per group: **a worked solution (pre-rendered, so you can read the numbers without running it) and questions to ask after the presentation.**

**Flow (≈ 45 min):** 25 min work → 5 × (5 min talk + 1–2 min questions) → 2 min wrap-up.
**While they work:** visit each group and ask "what is the population value you are comparing against?" Many groups forget to check against the truth.
**Pitfall to watch:** groups pasting AI output without running it. Ask them to change one number and re-run.
""", "instr"),
    setup_cell(("clean",)),
    code('''
from scipy import stats

df = load("clean")
population = df["exam_score"].dropna().reset_index(drop=True)   # our "whole population" of exam scores
mu, sigma = population.mean(), population.std(ddof=0)            # the TRUE mean and SD (parameters)
rng = np.random.default_rng(2026)

print(f"{len(population)} students | true mean mu = {mu:.2f} | true SD sigma = {sigma:.2f}")
df.head(3)
'''),
]

# ---------------------------------------------------------------- cards
def card(n, title, question, must, hints):
    return [
        md(f"---\n# 👥 Group {n} · {title}"),
        md(f"""
**Question:** {question}

**You must produce**
{must}

**Look up (function names, not code):** {hints}
"""),
        md("**📝 Plan / notes (who says what):**\n\n*(double-click to write)*"),
        code("# your code\n", "student"),
        code("# your chart\n", "student"),
        md("**✍️ Reporting sentence:**\n\n*(double-click to write)*"),
        md("**🧾 AI log:** prompt → what I corrected or double-checked →\n\n*(double-click to write)*"),
    ]


# ============================ GROUP 1 ============================
C += card(
    1, "Population vs Sample",
    "If we survey only the keenest students instead of a random group, how wrong is our estimate of the average exam score, and does a bigger sample fix it?",
    """1. The true mean μ of all exam scores.
2. The distribution of the mean over **1,000 random samples of 40** students (histogram).
3. The mean of a **convenience sample**: the **40 students with the highest `study_hours_week`** (those who answer surveys first). Mark it on the same histogram.
4. Repeat with **n = 200** for both kinds of sample. What happens to the random one? To the biased one?
5. One sentence explaining why more data does not rescue a biased sample.""",
    "`rng.choice(..., replace=False)`, `df.sort_values`, `.head`, `.dropna`, `plt.hist`, `plt.axvline`",
)
C += [
    code('''
random_means_40 = np.array([rng.choice(population, 40, replace=False).mean() for _ in range(1000)])
valid = df.dropna(subset=["exam_score", "study_hours_week"]).sort_values("study_hours_week", ascending=False)
keen_40 = valid["exam_score"].head(40).mean()
keen_200 = valid["exam_score"].head(200).mean()
random_means_200 = np.array([rng.choice(population, 200, replace=False).mean() for _ in range(1000)])

fig, ax = plt.subplots(figsize=(8, 3.8))
ax.hist(random_means_40, bins=30, color="steelblue", alpha=0.8, label="1,000 random samples (n = 40)")
ax.axvline(mu, color="black", ls="--", label=f"true mean {mu:.1f}")
ax.axvline(keen_40, color="crimson", lw=3, label=f"keenest 40 students: {keen_40:.1f}")
ax.set_xlabel("sample mean exam score"); ax.legend(); plt.show()
print(f"random n=40 : mean of means {random_means_40.mean():.1f}, SD {random_means_40.std():.2f}")
print(f"random n=200: mean of means {random_means_200.mean():.1f}, SD {random_means_200.std():.2f}")
print(f"keenest 40 : {keen_40:.1f}   keenest 200: {keen_200:.1f}   (truth {mu:.1f})")
''', "instr"),
    note("""
**Expected:** random means centre on μ ≈ 64.9 (SD ≈ 1.8 at n=40, ≈ 0.7 at n=200). The keenest 40 average ≈ 60.0 and the keenest 200 ≈ 59.3, well below the truth (the top studiers are mostly Engineering, who score lowest: Simpson's paradox again). A bigger biased sample is still off, just more precisely wrong.
**Questions to ask:**
1. "Which sample gave a more *precise* answer at n = 200? Which was more *accurate*?" *(precision vs accuracy)*
2. "In real life you don't know μ. How could you tell the sample was biased?" *(compare to known population facts, check who is missing)*
3. "Where have we seen non-random missingness before?" *(the missing sleep answers in Class 03)*
"""),
]

# ============================ GROUP 2 ============================
C += card(
    2, "Sampling Distribution & Standard Error",
    "How does the typical error of a sample mean shrink as the sample size grows, and does it match the formula σ/√n?",
    """1. For **n = 10, 30, 100**: draw **2,000 random samples**, compute each sample mean, and the **SD of those means**.
2. Compare each SD with the formula **σ / √n**. Make a small table.
3. One chart that overlays (or places side by side) the three distributions of sample means.
4. **Bonus:** repeat for `commute_minutes` (very skewed). Is the distribution of the *sample means* still skewed at n = 30?
5. One sentence: how much extra data do you need to cut the error in half?""",
    "`rng.choice`, `.std()`, `np.sqrt`, `sns.kdeplot` or `plt.hist`, `.skew()`",
)
C += [
    code('''
sizes = [10, 30, 100]
means = {n: np.array([rng.choice(population, n).mean() for _ in range(2000)]) for n in sizes}
table = pd.DataFrame({"n": sizes,
                      "SD of sample means": [means[n].std() for n in sizes],
                      "sigma / sqrt(n)": [sigma / np.sqrt(n) for n in sizes]}).round(2)
display(table)

fig, ax = plt.subplots(figsize=(8, 3.8))
for n in sizes:
    sns.kdeplot(means[n], fill=True, alpha=0.3, label=f"n = {n}", ax=ax)
ax.axvline(mu, color="black", ls="--"); ax.set_xlabel("sample mean"); ax.legend(); plt.show()

commute = df["commute_minutes"].dropna()
commute_means = np.array([rng.choice(commute, 30).mean() for _ in range(2000)])
print(f"commute raw skew = {commute.skew():.2f}   skew of means (n=30) = {pd.Series(commute_means).skew():.2f}")
''', "instr"),
    note("""
**Expected:** SDs ≈ 4.0, 2.2, 1.2, matching σ/√n (3.9, 2.2, 1.2). Skew of commute drops from ≈ 1.9 to ≈ 0.35.
**Questions to ask:**
1. "Why do the three curves have the same centre but different widths?"
2. "You need to halve the error. How much more data?" *(4×)* "Is it worth going from 100 to 400 students?"
3. "What is the difference between the SD of the *data* and the SE?" *(spread of individuals vs precision of the mean)*
"""),
]

# ============================ GROUP 3 ============================
C += card(
    3, "Confidence Intervals",
    "What does '95% confident' really mean? Build many intervals and count how often they catch the truth.",
    """1. Draw **one random sample of 30** and build its 95% confidence interval **by hand** (mean ± t* × SE). Does it contain μ?
2. Repeat **1,000 times**. What share of intervals contain μ?
3. Repeat with **90%** and **99%**. Make a small table of coverage and **average width**.
4. Repeat 95% with **n = 100**. What happens to the width?
5. One chart: the first 30 intervals as horizontal lines, μ as a vertical line, misses in a different colour.""",
    "`stats.t.ppf`, `.std(ddof=1)`, `np.sqrt`, `plt.hlines`, `plt.axvline`",
)
C += [
    code('''
def ci(sample, level=0.95):
    m, se = sample.mean(), sample.std(ddof=1) / np.sqrt(len(sample))
    t = stats.t.ppf((1 + level) / 2, len(sample) - 1)
    return m - t * se, m + t * se

rows = []
for level in (0.90, 0.95, 0.99):
    for n in (30, 100):
        cis = [ci(rng.choice(population, n, replace=False), level) for _ in range(1000)]
        cover = np.mean([lo <= mu <= hi for lo, hi in cis])
        width = np.mean([hi - lo for lo, hi in cis])
        rows.append({"level": f"{level:.0%}", "n": n, "coverage": f"{cover:.1%}", "avg width": round(width, 1)})
display(pd.DataFrame(rows))

demo = [ci(rng.choice(population, 30, replace=False)) for _ in range(30)]
fig, ax = plt.subplots(figsize=(7.5, 5))
for i, (lo, hi) in enumerate(demo):
    ax.hlines(i, lo, hi, color="crimson" if not (lo <= mu <= hi) else "steelblue", lw=3)
ax.axvline(mu, color="black", ls="--", label=f"true mean {mu:.1f}")
ax.set_yticks([]); ax.set_xlabel("exam score"); ax.legend(); plt.show()
''', "instr"),
    note("""
**Expected:** coverage ≈ 91 / 96 / 99 % (close to nominal; small deviations are simulation noise); average width at n = 30 is ≈ 7.5 / 9.0 / 12.3 and at n = 100 ≈ 4.1 / 4.8 / 6.4, about 1.8–1.9× narrower (√(100/30) ≈ 1.8).
**Questions to ask:**
1. "After you computed one interval, what is the probability it contains μ?" *(it either does or doesn't; 95% describes the method)*
2. "Why would you ever choose 90% over 99%?" *(precision, narrower interval)*
3. "To halve the width of the interval, what must you change?" *(4× n)*
"""),
]

# ============================ GROUP 4 ============================
C += card(
    4, "Hypothesis Test & p-value",
    "Do students with a heavy part-time job (more than 15 h/week) score differently from students with no job? Is that gap plausible by luck alone?",
    """1. State **H₀ and H₁** in words.
2. The two group means, the difference, and **n** in each group.
3. A **Welch t-test** with scipy. Report t and p.
4. A **permutation test** that you write yourself: shuffle the group labels **10,000 times**, record the difference each time, and find how often the shuffled difference is at least as extreme as the real one. Compare with the t-test p.
5. Repeat step 3 for **Hostel vs Home** residents. What is different about the result?
6. One sentence on what p does *and does not* mean here.""",
    "`stats.ttest_ind(..., equal_var=False)`, `rng.permutation`, `np.abs`, `np.mean`",
)
C += [
    code('''
job = df[df.part_time_job_hours_week > 15]["exam_score"].dropna().to_numpy()
nojob = df[df.part_time_job_hours_week == 0]["exam_score"].dropna().to_numpy()
real_diff = nojob.mean() - job.mean()
t = stats.ttest_ind(nojob, job, equal_var=False)
print(f"no job {nojob.mean():.1f} (n={len(nojob)}) | job>15h {job.mean():.1f} (n={len(job)}) | gap {real_diff:.1f}")
print(f"Welch t = {t.statistic:.2f}, p = {t.pvalue:.2e}")

pooled = np.concatenate([nojob, job])
shuffled = np.empty(10_000)
for i in range(10_000):
    perm = rng.permutation(pooled)
    shuffled[i] = perm[:len(nojob)].mean() - perm[len(nojob):].mean()
p_perm = (np.abs(shuffled) >= abs(real_diff)).mean()
print(f"permutation p = {p_perm:.4f}  (largest shuffled gap = {np.abs(shuffled).max():.1f}, real gap = {real_diff:.1f})")

fig, ax = plt.subplots(figsize=(8, 3.6))
ax.hist(shuffled, bins=60, color="lightgray"); ax.axvline(real_diff, color="crimson", lw=3, label=f"real gap {real_diff:.1f}")
ax.axvline(-real_diff, color="crimson", lw=3); ax.set_xlabel("gap when labels are shuffled"); ax.legend(); plt.show()

hostel = df[df.residence == "Hostel"]["exam_score"].dropna()
home = df[df.residence == "Home"]["exam_score"].dropna()
t2 = stats.ttest_ind(hostel, home, equal_var=False)
print(f"hostel {hostel.mean():.1f} vs home {home.mean():.1f}: t = {t2.statistic:.2f}, p = {t2.pvalue:.2f}")
''', "instr"),
    note("""
**Expected:** gap ≈ 8.8 points, t ≈ 5.9, p ≈ 1.6e-8; the permutation p prints 0.0000 (the largest of 10,000 shuffled gaps was ≈ 5.7, far below 8.8, so say "p < 1/10,000"). Hostel vs Home: gap ≈ 0.2, p ≈ 0.85.
**Questions to ask:**
1. "The permutation p says 0.0000. Is the probability *really* zero?" *(no: fewer than 1 in 10,000; report p < 0.0001)*
2. "Does p tell you that heavy jobs *cause* lower scores?" *(no: association; heavy workers also sleep less)*
3. "Hostel vs Home gave p = 0.85. Does that prove residence has no effect?" *(no: absence of evidence; look at the CI)*
4. "Is 'p = 0.03' the chance that H₀ is true?" *(no)*
"""),
]

# ============================ GROUP 5 ============================
C += card(
    5, "Effect Size",
    "A small p-value says an effect is detectable. Does it say the effect is *big*? Compare several differences by p-value and by Cohen's d.",
    """1. Make a table with these comparisons on `exam_score`: **job > 15 h vs no job**, **Hostel vs Home**, **Engineering vs Data Science**, **sleep < 6 h vs ≥ 6 h**.
   For each: the difference in means, the **Welch p-value** and **Cohen's d**.
2. Rank the rows by p and then by d. Do the rankings agree?
3. **Simulation:** make two Normal groups with means 63 and 60 and SD 10 (so d = 0.30). Test them with **n = 20, 100 and 1,000 per group**. What happens to p? To d?
4. Write a **rule of thumb** in your own words for how to read p and d together.""",
    "`stats.ttest_ind`, `.var(ddof=1)`, pooled SD, `rng.normal`, `pd.DataFrame`",
)
C += [
    code('''
def cohens_d(a, b):
    a, b = np.asarray(a), np.asarray(b)
    pooled = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    return (a.mean() - b.mean()) / pooled

score = df.dropna(subset=["exam_score"])
groups = {
    "job > 15 h vs no job (higher = no job)": (score[score.part_time_job_hours_week == 0].exam_score,
                                              score[score.part_time_job_hours_week > 15].exam_score),
    "Hostel vs Home": (score[score.residence == "Hostel"].exam_score, score[score.residence == "Home"].exam_score),
    "Engineering vs Data Science": (score[score.program == "Engineering"].exam_score,
                                    score[score.program == "Data Science"].exam_score),
    "sleep >= 6 h vs < 6 h": (score[score.sleep_hours >= 6].exam_score, score[score.sleep_hours < 6].exam_score),
}
rows = []
for name, (a, b) in groups.items():
    rows.append({"comparison": name, "mean diff": round(a.mean() - b.mean(), 1),
                 "p (Welch)": f"{stats.ttest_ind(a, b, equal_var=False).pvalue:.1e}",
                 "Cohen d": round(cohens_d(a, b), 2)})
display(pd.DataFrame(rows))

sim = []
for n in (20, 100, 1000):
    a, b = rng.normal(63, 10, n), rng.normal(60, 10, n)
    sim.append({"n per group": n, "p": f"{stats.ttest_ind(a, b).pvalue:.3g}", "Cohen d (sample)": round(cohens_d(a, b), 2)})
display(pd.DataFrame(sim))
''', "instr"),
    note("""
**Expected:** job gap 8.8 points, d ≈ 0.73, p ≈ 2e-8; Hostel vs Home d ≈ 0.02, p ≈ 0.85; Engineering vs Data Science gap −6.8, d ≈ −0.77, p ≈ 5e-10; sleep ≥ 6 h vs < 6 h gap 5.3, d ≈ 0.45, p ≈ 3e-4. The ranking by p and by d can differ (compare sleep with Engineering). Simulation: with a true d of 0.30, p can be non-significant at n = 20 and 100 and tiny (≈ 1e-9) at n = 1,000, while the sample d stays around 0.3 (noisy at small n; exact numbers change with the seed).
**Questions to ask:**
1. "Two results are both 'significant'. How do you decide which matters more?" *(d, and the practical context)*
2. "A company reports a significant improvement from 10 million users. What do you ask?" *(how big is it?)*
3. "What is a 3-point difference worth in *exam* terms? Is d = 0.3 important?" *(context decides)*
4. "Which of today's comparisons would you act on, and why?"
"""),
    md("""
---
## ✅ Checklist (every group)
- [ ] I compared my estimate with the **known population value**
- [ ] I have **one chart** and can explain the axes
- [ ] I wrote **one reporting sentence** (estimate, interval or p, and size)
- [ ] Everyone knows their part. We practised under **5 minutes**
"""),
]

if __name__ == "__main__":
    instr = build(C, "instr")
    for p in render(instr):
        print("  ❗ instructor cell error:", p)
    save(instr, "05_INSTRUCTOR_group_activity.ipynb")
    stu = build(C, "student")
    save(stu, "05_STUDENT_group_activity.ipynb")
    leaked = any("Expected" in "".join(c["source"]) or "INSTRUCTOR" in "".join(c["source"]) for c in stu["cells"])
    print("instructor material in student copy:", leaked)
