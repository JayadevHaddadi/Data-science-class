"""Builds the Class 04 instructor deck: ../slides/Class04_Probability_Foundations.pptx

All numbers are computed here, so slides and notebooks agree. Needs python-pptx, numpy, scipy.
Edit this file, not the .pptx.
"""
import os

import numpy as np
from scipy import stats

from deck_helpers import *  # noqa: F401,F403  (theme, helpers, prs)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "slides", "Class04_Probability_Foundations.pptx")
rng = np.random.default_rng(404)

# ------------------------------------------------------------------ numbers
flips = rng.integers(0, 2, 5000)
running = np.cumsum(flips) / np.arange(1, 5001)
CHECK = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
LLN = [round(float(running[n - 1]), 3) for n in CHECK]

totals = np.array([a + b for a in range(1, 7) for b in range(1, 7)])
ways = [int((totals == t).sum()) for t in range(2, 13)]

prev, sens, fpr = 0.01, 0.95, 0.05
p_pos = sens * prev + fpr * (1 - prev)
post1 = sens * prev / p_pos
post2 = sens * post1 / (sens * post1 + fpr * (1 - post1))
prevs = [0.01, 0.02, 0.05, 0.10, 0.20, 0.50]
posts = [sens * p / (sens * p + fpr * (1 - p)) * 100 for p in prevs]

n_b, p_b = 10, 0.3
k = np.arange(0, 11)
binom_pmf = stats.binom.pmf(k, n_b, p_b)
p_ge5 = 1 - stats.binom.cdf(4, n_b, p_b)

lam = 3
kp = np.arange(0, 11)
pois_pmf = stats.poisson.pmf(kp, lam)
p0 = stats.poisson.pmf(0, lam)

mu_h, sd_h = 170, 8
xs = np.arange(146, 195, 2)
norm_pdf = stats.norm.pdf(xs, mu_h, sd_h)
z185 = (185 - mu_h) / sd_h
p_gt185 = 1 - stats.norm.cdf(185, mu_h, sd_h)
q95 = stats.norm.ppf(0.95, mu_h, sd_h)

exp_means = rng.exponential(1.0, size=(20000, 30)).mean(axis=1)
edges = np.arange(0.4, 1.81, 0.05)
cnt, _ = np.histogram(exp_means, bins=edges)
cent = [f"{c:.2f}" for c in (edges[:-1] + edges[1:]) / 2]

# delivery example
dx, dp = np.array([1, 2, 3]), np.array([0.5, 0.3, 0.2])
dE = float((dx * dp).sum())
dV = float(((dx - dE) ** 2 * dp).sum())


def chart_col(s, x, y, w, h, cats, vals, cat_t, val_t, color=TEAL, gap=40, labels=False, fmt="0.00"):
    cd = CategoryChartData()
    cd.categories = cats
    cd.add_series("s", vals)
    ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(x), Inches(y), Inches(w), Inches(h), cd).chart
    style_chart(ch, cat_t, val_t)
    pl = ch.plots[0]
    pl.gap_width = gap
    pl.series[0].format.fill.solid()
    pl.series[0].format.fill.fore_color.rgb = rgb(color)
    if labels:
        pl.has_data_labels = True
        pl.data_labels.number_format = fmt
        pl.data_labels.number_format_is_linked = False
        pl.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
        pl.data_labels.font.size = Pt(12)
        pl.data_labels.font.color.rgb = rgb(DARK)
    return ch


# ================================================================== 1 TITLE
s = new_slide(dark=True, notes=(
    "TIMING (~95 min of content; the deck is built so you can cut cleanly):\n"
    "Slides 2-4 probability basics (12 min) | 5-7 conditional & independence (15 min) | 8-10 Bayes (18 min) | "
    "11-12 random variables (10 min) | 13-17 distributions & CLT (20 min) | 18-19 mistakes + hand-off (5 min).\n\n"
    "MUST TEACH if time is tight: 5, 6 (conditional), 8 (Bayes by counting), 11 (E[X]), 13/14/15 (one slide each for the three distributions). "
    "CAN CUT or just mention: 4 (addition rule), 10 (updating twice), 12 (transformations), 16 (CLT), 17 (cheat-sheet).\n\n"
    "Each slide has a PREDICT question in the notes: ask it BEFORE you reveal the answer. Companion notebooks: 01_INSTRUCTOR_concepts.ipynb for live demos."))
text(s, 0.8, 1.6, 7, 0.4, "DATA SCIENCE · CLASS 04", size=14, color=AMBER, bold=True)
text(s, 0.8, 2.1, 7.2, 2.2, "Probability\nfoundations", size=54, color="FFFFFF", font=HEAD, bold=True)
text(s, 0.8, 4.5, 6.8, 1.4,
     "Concepts · conditional probability · independence · Bayes' theorem · random variables · distributions",
     size=18, color=MINT)
r = np.random.default_rng(8)
for i in range(14 * 9):
    cx, cy = i % 14, i // 14
    circle(s, 8.2 + cx * 0.33, 1.5 + cy * 0.5, 0.2, AMBER if r.random() < 0.17 else TEAL)

# ================================================================== 2 ROADMAP
s = new_slide(notes=(
    "FRAME: probability is the language of uncertainty. Everything later (inference, machine learning) is built on these six ideas.\n"
    "SAY: 'Today we know the rules of the game and ask what data to expect. Next class we run it backwards: we see the data and ask what the rules were.'\n"
    "ASK: 'Name one decision you made this week under uncertainty.' (Weather, exam, traffic.) Take two answers."))
title(s, "Roadmap", "Six ideas, each builds on the last")
items = [("1", "Probability", "How likely, and the rules"), ("2", "Conditional", "Probability once we know something"),
         ("3", "Independence", "When knowing B changes nothing"), ("4", "Bayes", "Updating beliefs with evidence"),
         ("5", "Random variables", "Turning outcomes into numbers"), ("6", "Distributions", "Named patterns you can reuse")]
for i, (n, h_, b_) in enumerate(items):
    x = 0.6 + (i % 3) * 4.1
    y = 1.9 + (i // 3) * 2.45
    rect(s, x, y, 3.95, 2.2, fill=CARD, line=MINT)
    circle(s, x + 0.25, y + 0.25, 0.55, TEAL)
    text(s, x + 0.25, y + 0.25, 0.55, 0.55, n, size=18, bold=True, color="FFFFFF", align=PP_ALIGN.CENTER,
         anchor=MSO_ANCHOR.MIDDLE, space=0)
    text(s, x + 0.25, y + 1.0, 3.45, 0.45, h_, size=21, bold=True, color=DARK, font=HEAD)
    text(s, x + 0.25, y + 1.5, 3.45, 0.6, b_, size=15, color=MUTED)

# ================================================================== 3 PROBABILITY BASICS
s = new_slide(notes=(
    "TWO MEANINGS: classical = favourable / all equally likely outcomes (a fair die: 1/6). Frequentist = long-run proportion.\n"
    f"CHART: one simulated run of coin flips. After 10 flips the proportion was {LLN[0]:.2f}; after 5,000 flips {LLN[-1]:.3f}. It wobbles then settles near 0.5. That is the Law of Large Numbers.\n"
    "PREDICT first: 'After 10 flips will the proportion of heads be exactly 0.5? After 5,000?' Then show the chart.\n"
    "WARNING: gambler's fallacy. A coin that just landed heads five times is NOT due for tails. The law is about proportions in the long run, not about 'making up' for the past."))
title(s, "1 · Probability", "Probability = what the proportion settles to")
cd = CategoryChartData()
cd.categories = [str(n) for n in CHECK]
cd.add_series("proportion of heads", LLN)
ch = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(0.6), Inches(1.7), Inches(7.4), Inches(5.0), cd).chart
style_chart(ch, "number of coin flips", "proportion of heads")
ch.value_axis.minimum_scale, ch.value_axis.maximum_scale = 0.2, 0.8
ser = ch.plots[0].series[0]
ser.format.line.color.rgb = rgb(TEAL)
ser.format.line.width = Pt(3)
ser.smooth = False
card(s, 8.4, 1.8, 4.33, 2.2, "Classical", ["Favourable ÷ all equally likely.", "Fair die: P(6) = 1/6."], size=16)
card(s, 8.4, 4.25, 4.33, 2.45, "Long-run frequency", ["Short runs are wild, long runs settle near 0.5.",
                                                     "Past flips don’t change the next one."], head_color="B36B00", size=16)

# ================================================================== 4 SAMPLE SPACE
s = new_slide(notes=(
    "SAMPLE SPACE: list every equally likely outcome. Two dice: 36. The total 7 has 6 ways, totals 2 and 12 have 1 way each, which is why the middle is tallest.\n"
    "ADDITION RULE: P(A or B) = P(A) + P(B) - P(A and B). We subtract the overlap because (6,4), (6,5), (6,6) are in BOTH events and would be counted twice.\n"
    "EXAMPLE: A = first die is 6 (6/36), B = total at least 10 (6/36), overlap 3/36. So P(A or B) = 6/36 + 6/36 - 3/36 = 9/36 = 0.25.\n"
    "PREDICT: 'What is the most likely total of two dice? How many ways?'"))
title(s, "1 · Probability", "Count the ways: two dice")
chart_col(s, 0.6, 1.7, 7.0, 5.0, [str(t) for t in range(2, 13)], ways, "total of two dice", "ways out of 36",
          gap=25, labels=True, fmt="0")
card(s, 8.0, 1.8, 4.73, 2.35, "Addition rule", [
    "P(A or B) = P(A) + P(B) − P(A and B)",
    "Subtract the overlap so it isn’t counted twice."], size=15)
card(s, 8.0, 4.4, 4.73, 2.3, "Example", [
    "A: first die is 6 (6/36)",
    "B: total ≥ 10 (6/36), overlap 3/36",
    "P(A or B) = 9/36 = 0.25"], head_color="B36B00", size=15)

# ================================================================== 5 CONDITIONAL
s = new_slide(notes=(
    "MESSAGE: conditioning = shrinking the world to the cases where B happened, then asking how many of those also have A.\n"
    "TABLE: 400 students. 150 joined a study group (120 passed, 30 failed); 250 did not (150 passed, 100 failed). Overall pass rate 270/400 = 0.675.\n"
    "PREDICT: 'Among study-group students, is the pass rate higher, lower or the same as 0.675?' Then compute 120/150 = 0.80.\n"
    "CAUTION: this is association, not proof that study groups cause passing (callback to Class 03: confounding)."))
title(s, "2 · Conditional probability", "P(A | B): shrink the world to B")
rect(s, 0.6, 1.8, 6.4, 1.3, fill=DARK)
text(s, 0.6, 1.8, 6.4, 1.3, "P(A | B) = P(A and B) / P(B)", size=30, color="FFFFFF", font=HEAD, bold=True,
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
tbl = s.shapes.add_table(4, 4, Inches(0.6), Inches(3.45), Inches(6.4), Inches(2.6)).table
data = [["", "Pass", "Fail", "Total"], ["Study group", "120", "30", "150"], ["No group", "150", "100", "250"], ["Total", "270", "130", "400"]]
for i, row in enumerate(data):
    for j, v in enumerate(row):
        c = tbl.cell(i, j)
        c.text = v
        c.fill.solid()
        c.fill.fore_color.rgb = rgb(DARK if i == 0 else ("FFFFFF" if i % 2 else "EEF4F2"))
        for pg in c.text_frame.paragraphs:
            pg.alignment = PP_ALIGN.CENTER if j else PP_ALIGN.LEFT
            for rn in pg.runs:
                rn.font.size, rn.font.name = Pt(16), BODY
                rn.font.bold = (i == 0 or j == 0)
                rn.font.color.rgb = rgb("FFFFFF" if i == 0 else INK)
card(s, 7.4, 1.8, 5.33, 1.45, "Overall", "P(pass) = 270 / 400 = 0.675", size=19)
card(s, 7.4, 3.45, 5.33, 1.45, "Given a study group", "P(pass | group) = 120 / 150 = 0.80", size=19, head_color=TEAL)
card(s, 7.4, 5.1, 5.33, 1.45, "Given no group", "P(pass | no group) = 150 / 250 = 0.60", size=19, head_color=RED)

# ================================================================== 6 DIRECTION
s = new_slide(notes=(
    "THE MOST COMMON PROBABILITY MISTAKE: confusing P(A|B) with P(B|A).\n"
    "From the same table: 80% of study-group students pass, BUT only 44% (120/270) of passing students were in a study group. Different questions, different denominators.\n"
    "REAL EXAMPLES: 'Most car accidents happen near home' (P(near home | accident) is high) does not mean 'home is dangerous' (P(accident | near home) is tiny, because we spend most time near home). "
    "'Most successful founders dropped out' vs 'most dropouts become founders'.\n"
    "This is exactly the trap in the Bayes medical-test puzzle on the next slides."))
title(s, "2 · Conditional probability", "P(A | B) is not P(B | A)")
for x, head, big, sub, col in [
    (0.6, "Of study-group students…", "80%", "passed.   P(pass | group) = 120 / 150", TEAL),
    (6.83, "Of students who passed…", "44%", "were in a study group.   P(group | pass) = 120 / 270", RED),
]:
    rect(s, x, 1.8, 5.9, 3.0, fill=CARD, line=MINT)
    text(s, x + 0.3, 2.0, 5.3, 0.45, head, size=19, bold=True, color=DARK, font=HEAD)
    text(s, x + 0.3, 2.65, 5.3, 1.3, big, size=66, color=col, font=HEAD, bold=True)
    text(s, x + 0.3, 4.0, 5.3, 0.6, sub, size=15, color=MUTED)
rect(s, 0.6, 5.15, 12.13, 1.5, fill=DARK)
text(s, 0.95, 5.15, 11.4, 1.5,
     "Same table, different denominators. Always say which one is “given”.", size=24, color="FFFFFF", font=HEAD,
     bold=True, anchor=MSO_ANCHOR.MIDDLE)

# ================================================================== 7 INDEPENDENCE
s = new_slide(notes=(
    "DEFINITION: A and B independent if P(A and B) = P(A) x P(B), equivalently P(A|B) = P(A): learning B tells you nothing about A.\n"
    "DICE CHECK: A = first die even (1/2), B = total is 7 (1/6). P(A)P(B) = 1/12. P(A and B) = 3/36 = 1/12. Equal, so independent. Surprising: whatever the first die shows, exactly one value of the second die makes 7.\n"
    "CARDS: P(2nd ace | 1st ace) = 4/52 = 0.077 with replacement (independent), 3/51 = 0.059 without (dependent: the deck changed).\n"
    "KEY TRAP: mutually exclusive is NOT independent. If A and B cannot both happen, then knowing A happened tells you B did not: strong dependence.\n"
    "PREDICT: 'Are \"first die is 1\" and \"first die is 6\" independent?' (No: exclusive, so dependent.)"))
title(s, "3 · Independence", "Does knowing B change the chance of A?")
rect(s, 0.6, 1.8, 6.0, 1.3, fill=DARK)
text(s, 0.6, 1.8, 6.0, 1.3, "Independent ⇔ P(A and B) = P(A) × P(B)", size=20, color="FFFFFF", font=HEAD, bold=True,
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
card(s, 0.6, 3.4, 6.0, 3.3, "Dice: first die even, total is 7", [
    "P(A) = 1/2     P(B) = 1/6",
    "P(A) × P(B) = 1/12",
    "P(A and B) = 3/36 = 1/12",
    "Equal → independent ✅"], size=17)
card(s, 6.93, 1.8, 5.8, 2.4, "Cards: ace after ace", [
    "With replacement: 4/52 = 0.077 → independent",
    "Without: 3/51 = 0.059 → dependent"], size=16, head_color="B36B00")
card(s, 6.93, 4.45, 5.8, 2.25, "Exclusive ≠ independent", [
    "“First die is 1” and “first die is 6” can’t both happen.",
    "Knowing one tells you a lot about the other."], size=16, head_color=RED)

# ================================================================== 8 BAYES BY COUNTING
s = new_slide(notes=(
    "THE PUZZLE: 1% of people have a disease. The test is positive for 95% of sick people and 5% of healthy people. You test positive. How likely are you sick?\n"
    "PREDICT BEFORE THIS SLIDE: get a gut number in chat (95%? 80%? 50%? 16%?). Most say 95%. Keep the votes.\n"
    "COUNT 10,000 people: 100 sick, 9,900 healthy. Sick and positive: 0.95 x 100 = 95. Healthy and positive (false alarms): 0.05 x 9,900 = 495. All positives = 590. Of those, 95 are sick: 95/590 = 16.1%.\n"
    "WHY: the healthy group is 99 times bigger, so even a small false-alarm rate produces far more false alarms than there are real cases. IGNORING THE BASE RATE is the number one Bayes mistake."))
title(s, "4 · Bayes' theorem", "A positive test: how worried should you be?")
text(s, 0.6, 1.65, 12.1, 0.5, "10,000 people · 1% sick · test catches 95% of sick people · 5% false alarms on healthy people",
     size=17, color=MUTED)
boxes = [
    (0.6, "100 sick", "95 test positive", TEAL, "E3F1EE"),
    (4.7, "9,900 healthy", "495 test positive", RED, "FBE9E7"),
]
for x, h_, b_, col, fillc in boxes:
    rect(s, x, 2.4, 3.7, 2.2, fill=fillc)
    text(s, x + 0.25, 2.55, 3.3, 0.5, h_, size=22, bold=True, color=col, font=HEAD)
    text(s, x + 0.25, 3.3, 3.3, 1.0, b_, size=26, bold=True, color=DARK)
text(s, 4.35, 3.0, 0.4, 0.6, "+", size=36, bold=True, color=MUTED, align=PP_ALIGN.CENTER)
text(s, 8.35, 3.05, 0.5, 0.6, "→", size=36, bold=True, color=AMBER, align=PP_ALIGN.CENTER)
rect(s, 9.0, 2.4, 3.73, 2.2, fill=DARK)
text(s, 9.25, 2.55, 3.3, 0.4, "590 positives", size=18, color=MINT, bold=True)
text(s, 9.25, 3.1, 3.3, 1.0, f"{post1 * 100:.1f}%", size=50, color=AMBER, font=HEAD, bold=True)
text(s, 9.25, 4.0, 3.3, 0.5, "of them are really sick", size=15, color="FFFFFF")
rect(s, 0.6, 5.0, 12.13, 1.6, fill=CARD, line=MINT)
text(s, 0.95, 5.0, 11.4, 1.6,
     "The healthy group is 99× bigger, so a small false-alarm rate still produces far more false alarms (495) than real cases (95).",
     size=20, color=DARK, font=HEAD, bold=True, anchor=MSO_ANCHOR.MIDDLE)

# ================================================================== 9 BAYES FORMULA
s = new_slide(notes=(
    "NOW THE FORMULA: P(sick | +) = P(+ | sick) P(sick) / P(+), where P(+) = P(+|sick)P(sick) + P(+|healthy)P(healthy) = 0.95x0.01 + 0.05x0.99 = 0.059.\n"
    f"So the posterior = 0.0095 / 0.059 = {post1:.3f}. Same answer as counting: the formula is just the counting argument written as fractions.\n"
    "THE CHART: same test, different base rates. At 1% prevalence a positive means 16%; at 10% it means 68%; at 50% it means 95%. The test did not change, the prior did.\n"
    "RECIPE: (1) write the prior, (2) the likelihoods, (3) total probability of the evidence, (4) divide."))
title(s, "4 · Bayes' theorem", "Same test, different base rate")
rect(s, 0.6, 1.8, 5.9, 1.4, fill=DARK)
text(s, 0.6, 1.8, 5.9, 1.4, "P(H | E) = P(E | H) · P(H) / P(E)", size=26, color="FFFFFF", font=HEAD, bold=True,
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
steps = [("Prior", "P(sick) = 0.01"), ("Likelihoods", "0.95 if sick, 0.05 if healthy"),
         ("Total P(+)", "0.95·0.01 + 0.05·0.99 = 0.059"), ("Divide", f"0.0095 / 0.059 = {post1:.3f}")]
for i, (k_, v_) in enumerate(steps):
    y = 3.5 + i * 0.8
    circle(s, 0.6, y + 0.05, 0.45, AMBER)
    text(s, 0.6, y + 0.05, 0.45, 0.45, str(i + 1), size=15, bold=True, color=DARK, align=PP_ALIGN.CENTER,
         anchor=MSO_ANCHOR.MIDDLE, space=0)
    text(s, 1.3, y, 1.8, 0.55, k_, size=16, color=MUTED, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 3.1, y, 3.5, 0.55, v_, size=16, bold=True, color=DARK, anchor=MSO_ANCHOR.MIDDLE)
chart_col(s, 6.9, 1.7, 5.83, 5.0, [f"{p * 100:.0f}%" for p in prevs], [round(v, 1) for v in posts],
          "how common the disease is", "P(sick | positive test), %", gap=40, labels=True, fmt="0")

# ================================================================== 10 UPDATING
s = new_slide(notes=(
    f"UPDATING: yesterday's posterior becomes today's prior. After one positive: {post1 * 100:.1f}%. After a second INDEPENDENT positive test: {post2 * 100:.1f}%.\n"
    "This is how spam filters, medical diagnosis and many ML models work: every new piece of evidence nudges the belief.\n"
    "LINK: the student AI tasks include a spam-filter (naive Bayes) problem. Naive Bayes assumes the words are independent given the class: that is where independence comes back.\n"
    "ASK: 'Why must the second test be independent of the first?' (Otherwise the same error repeats and you double-count the evidence.)"))
title(s, "4 · Bayes' theorem", "Evidence accumulates")
for i, (big, lab, col) in enumerate([("1%", "before any test (prior)", MUTED),
                                      (f"{post1 * 100:.0f}%", "after one positive test", TEAL),
                                      (f"{post2 * 100:.0f}%", "after two independent positives", RED)]):
    x = 0.6 + i * 4.1
    rect(s, x, 1.9, 3.95, 3.0, fill=CARD, line=MINT)
    text(s, x + 0.3, 2.15, 3.35, 1.4, big, size=64, color=col, font=HEAD, bold=True)
    text(s, x + 0.3, 3.8, 3.35, 0.9, lab, size=17, color=INK)
    if i < 2:
        text(s, x + 3.55, 3.0, 0.7, 0.6, "→", size=32, bold=True, color=AMBER, align=PP_ALIGN.CENTER)
rect(s, 0.6, 5.3, 12.13, 1.3, fill=DARK)
text(s, 0.95, 5.3, 11.4, 1.3, "Yesterday’s posterior is today’s prior. That is how spam filters and diagnosis systems learn.",
     size=22, color="FFFFFF", font=HEAD, bold=True, anchor=MSO_ANCHOR.MIDDLE)

# ================================================================== 11 RANDOM VARIABLES
s = new_slide(notes=(
    "A RANDOM VARIABLE turns outcomes into numbers. X = number of days a delivery takes. pmf = list of P(X = x).\n"
    f"E[X] = sum of x * P(x) = 1(0.5) + 2(0.3) + 3(0.2) = {dE:.1f}. This is the long-run average, a weighted average, NOT the most likely value (that is 1 day) and not a value you must be able to see (1.7 days never happens).\n"
    f"Var(X) = sum of (x - E[X])^2 P(x) = {dV:.2f}; SD = {np.sqrt(dV):.2f} days. SD is the typical distance from the mean, in the original units.\n"
    "PREDICT: 'If you order 1,000 items, about how many total delivery days?' (1,700.)"))
title(s, "5 · Random variables", "X = days until delivery")
chart_col(s, 0.6, 1.7, 5.6, 4.3, ["1 day", "2 days", "3 days"], [0.5, 0.3, 0.2], "X", "P(X = x)", gap=60,
          labels=True, fmt="0.0")
text(s, 0.6, 6.15, 5.6, 0.5, "pmf: the probabilities add up to 1", size=15, color=MUTED)
card(s, 6.6, 1.8, 6.13, 1.7, "Expected value (long-run average)", [
    f"E[X] = 1(0.5) + 2(0.3) + 3(0.2) = {dE:.1f} days"], size=18)
card(s, 6.6, 3.7, 6.13, 1.7, "Variance and SD", [
    f"Var(X) = Σ (x − E[X])² · P(x) = {dV:.2f}",
    f"SD = {np.sqrt(dV):.2f} days"], size=17, head_color="B36B00")
card(s, 6.6, 5.6, 6.13, 1.1, "Not", "the most likely value, nor one you must see", size=16, head_color=RED)

# ================================================================== 12 E AND VAR RULES
s = new_slide(notes=(
    "RULES: E[aX + b] = a E[X] + b: the mean moves and scales. Var(aX + b) = a^2 Var(X): the spread scales by a squared; adding a constant b does not change the spread.\n"
    "EXAMPLE: delivery cost = 5 + 2X dollars. E = 5 + 2(1.7) = 8.4. Var = 4 x 0.61 = 2.44.\n"
    "These rules are what the casino-game student task needs: winnings are a function of the die roll.\n"
    "LONG-RUN: running average of many trials heads to E[X] (Law of Large Numbers again). One day can be anything; 1,000 days are predictable."))
title(s, "5 · Random variables", "Transforming X: what happens to E and Var?")
for i, (head, body, col) in enumerate([
    ("Mean", "E[aX + b] = a·E[X] + b", TEAL),
    ("Variance", "Var(aX + b) = a² · Var(X)", "B36B00"),
    ("Example: cost = 5 + 2X", f"E = 5 + 2({dE:.1f}) = {5 + 2 * dE:.1f}      Var = 4 × {dV:.2f} = {4 * dV:.2f}", RED),
]):
    y = 1.85 + i * 1.65
    rect(s, 0.6, y, 12.13, 1.45, fill=CARD, line=MINT)
    text(s, 0.95, y, 4.0, 1.45, head, size=22, bold=True, color=col, font=HEAD, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 5.0, y, 7.5, 1.45, body, size=24, color=DARK, font=HEAD, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.6, 6.85, 12.1, 0.4, "Adding a constant shifts the mean but doesn’t change the spread. Multiplying by a scales the spread by a².",
     size=15, color=MUTED)

# ================================================================== 13 BINOMIAL
s = new_slide(notes=(
    "BINOMIAL: n independent yes/no trials, each with the same success probability p; X = number of successes. Example: 10 customers, each buys with p = 0.3.\n"
    f"The bar at k is P(X = k). Tallest at 3 (= n p). Mean n p = 3, SD = sqrt(n p (1-p)) = {np.sqrt(n_b * p_b * (1 - p_b)):.2f}.\n"
    f"THE CDF TRAP: cdf(k) = P(X <= k). 'At least 5' = P(X >= 5) = 1 - cdf(4) = {p_ge5:.3f}. NOT 1 - cdf(5). This off-by-one is the classic AI mistake from the AI demo.\n"
    "ASK: 'Which bars do I add for \"at most 2\"?' (0, 1, 2 = cdf(2).)"))
title(s, "6 · Distributions", "Binomial: successes out of n tries")
chart_col(s, 0.6, 1.7, 7.0, 5.0, [str(int(v)) for v in k], [round(float(v), 3) for v in binom_pmf],
          "customers who buy (out of 10, p = 0.3)", "P(X = k)", gap=30, labels=True, fmt="0.00")
card(s, 8.0, 1.8, 4.73, 2.1, "Use when", ["Fixed n, yes/no each time,", "same p, independent."], size=16)
card(s, 8.0, 4.1, 4.73, 2.6, "“At least 5”", [
    "cdf(4) = P(X ≤ 4)",
    f"P(X ≥ 5) = 1 − cdf(4) = {p_ge5:.3f}",
    "Not 1 − cdf(5)!"], size=16, head_color=RED)

# ================================================================== 14 POISSON
s = new_slide(notes=(
    "POISSON: events at random times at a steady average rate lambda; X = how many happen in a fixed window (emails per hour, calls per minute).\n"
    f"lambda = 3 here. Bar heights: P(0) = {p0:.3f} = e^-3. Right tail is longer than the left since counts cannot go below 0.\n"
    "SIGNATURE: mean = variance = lambda. If real count data has variance far from its mean, Poisson is probably wrong.\n"
    "BINOMIAL vs POISSON: Binomial has a fixed n and a maximum; Poisson has no maximum and no n.\n"
    "ASK: 'Calls per minute: Binomial or Poisson?' (Poisson.) 'Heads in 10 flips?' (Binomial.)"))
title(s, "6 · Distributions", "Poisson: events in a window")
chart_col(s, 0.6, 1.7, 7.0, 5.0, [str(int(v)) for v in kp], [round(float(v), 3) for v in pois_pmf],
          "emails in one hour (λ = 3)", "P(X = k)", color="D98A1F", gap=30, labels=True, fmt="0.00")
card(s, 8.0, 1.8, 4.73, 2.1, "Use when", ["Random events, steady average rate,", "counted in a fixed window."], size=16)
card(s, 8.0, 4.1, 4.73, 2.6, "Signature", [
    "mean = variance = λ",
    f"P(no emails) = e⁻³ = {p0:.3f}",
    "No fixed n, no maximum."], size=16, head_color="B36B00")

# ================================================================== 15 NORMAL
s = new_slide(notes=(
    "NORMAL: continuous, symmetric bell, described by mean mu and SD sigma. Probability = AREA under the curve; P(X = exactly 170.00) is 0, so we always ask about ranges.\n"
    f"68-95-99.7: about 68% within 1 SD (162-178), 95% within 2 (154-186), 99.7% within 3.\n"
    f"Z-SCORE: z = (x - mu)/sigma = (185 - 170)/8 = {z185:.2f}. P(height > 185) = 1 - cdf = {p_gt185:.3f}, about 3%.\n"
    f"PPF is the inverse of cdf: ppf(0.95) = {q95:.1f} cm: the tallest 5% are taller than this.\n"
    "COMMON BUG: scipy.stats.norm takes the standard deviation, not the variance."))
title(s, "6 · Distributions", "Normal: area under the curve is probability")
cd = CategoryChartData()
cd.categories = [str(int(v)) for v in xs]
cd.add_series("density", [round(float(v), 4) for v in norm_pdf])
ch = s.shapes.add_chart(XL_CHART_TYPE.AREA, Inches(0.6), Inches(1.7), Inches(7.0), Inches(5.0), cd).chart
style_chart(ch, "height (cm), mean 170, SD 8", "density")
ch.plots[0].series[0].format.fill.solid()
ch.plots[0].series[0].format.fill.fore_color.rgb = rgb(TEAL)
tbl = s.shapes.add_table(4, 2, Inches(8.0), Inches(1.8), Inches(4.73), Inches(2.0)).table
for i, row in enumerate([["Within", "Share"], ["1 SD  (162–178)", "≈ 68%"], ["2 SD  (154–186)", "≈ 95%"], ["3 SD  (146–194)", "≈ 99.7%"]]):
    for j, v in enumerate(row):
        c = tbl.cell(i, j)
        c.text = v
        c.fill.solid()
        c.fill.fore_color.rgb = rgb(DARK if i == 0 else ("FFFFFF" if i % 2 else "EEF4F2"))
        for rn in c.text_frame.paragraphs[0].runs:
            rn.font.size, rn.font.name, rn.font.bold = Pt(15), BODY, (i == 0 or j == 1)
            rn.font.color.rgb = rgb("FFFFFF" if i == 0 else INK)
card(s, 8.0, 4.1, 4.73, 2.6, "Tools", [
    f"z = (185 − 170) / 8 = {z185:.2f}",
    f"P(X > 185) = 1 − cdf = {p_gt185:.3f}",
    f"ppf(0.95) = {q95:.1f} cm (top 5%)"], size=16, head_color="B36B00")

# ================================================================== 16 CLT
s = new_slide(notes=(
    "CENTRAL LIMIT THEOREM: the AVERAGE of many independent draws is approximately Normal, even when the individual draws are not.\n"
    "CHART: 20,000 averages, each the mean of 30 draws from a strongly skewed Exponential distribution (mean 1, SD 1). The histogram is a bell centred on 1.\n"
    "THE SD of an average of n draws is sigma/sqrt(n) = 1/sqrt(30) = 0.18: narrower than one draw. This is the 'use 2, not 10, for the average of 25 students' trap in the student tasks.\n"
    "WHY: averaging cancels ups and downs; there are many more ways to land in the middle than at the extremes (see the dice demo in the notebook).\n"
    "THIS is the bridge to Class 05: sampling distributions and confidence intervals."))
title(s, "6 · Distributions", "Central Limit Theorem: averages become bell-shaped")
chart_col(s, 0.6, 1.7, 7.4, 5.0, cent, [int(c) for c in cnt], "average of 30 draws", "how many of 20,000 averages",
          gap=8)
card(s, 8.4, 1.8, 4.33, 2.4, "The raw data", ["Strongly skewed (Exponential).", "Mean 1, SD 1."], size=16)
card(s, 8.4, 4.45, 4.33, 2.25, "The average of 30", ["Bell-shaped, centred on 1.", "SD = σ/√n = 0.18"], size=16,
     head_color="B36B00")

# ================================================================== 17 CHEAT SHEET
s = new_slide(notes=(
    "CLOSING TOOL: read each row, ask 'which example is this?'. Quick quiz: heights of adults? (Normal) goals in a match? (Poisson) number of correct answers when guessing 10 quiz questions? (Binomial) average of 30 exam scores? (Normal by CLT)."))
title(s, "Wrap-up", "Which distribution?")
rows = [("One yes/no trial", "Bernoulli", "p"), ("Successes in n independent trials", "Binomial", "n, p"),
        ("Events in a fixed time window", "Poisson", "λ"), ("Measurements around a mean", "Normal", "μ, σ"),
        ("Average of many draws", "≈ Normal (CLT)", "μ, σ/√n")]
tbl = s.shapes.add_table(len(rows) + 1, 3, Inches(0.6), Inches(1.8), Inches(12.13), Inches(4.7)).table
tbl.columns[0].width, tbl.columns[1].width, tbl.columns[2].width = Inches(6.5), Inches(3.5), Inches(2.13)
for j, hd in enumerate(["Situation", "Distribution", "Parameters"]):
    c = tbl.cell(0, j)
    c.text = hd
    c.fill.solid()
    c.fill.fore_color.rgb = rgb(DARK)
    for rn in c.text_frame.paragraphs[0].runs:
        rn.font.size, rn.font.bold, rn.font.name, rn.font.color.rgb = Pt(17), True, BODY, rgb("FFFFFF")
for i, row in enumerate(rows, start=1):
    for j, v in enumerate(row):
        c = tbl.cell(i, j)
        c.text = v
        c.fill.solid()
        c.fill.fore_color.rgb = rgb("FFFFFF" if i % 2 else "EEF4F2")
        for rn in c.text_frame.paragraphs[0].runs:
            rn.font.size, rn.font.name, rn.font.bold = Pt(18), BODY, (j == 1)
            rn.font.color.rgb = rgb(TEAL if j == 1 else INK)

# ================================================================== 18 MISTAKES
s = new_slide(notes=(
    "Use as a checklist: ask the class for an example of two of these. Each maps to a slide: 1 -> slide 6, 2 -> slide 7, 3 -> slide 8, 4 -> slide 13, 5 -> slide 3."))
title(s, "Wrap-up", "Five mistakes to avoid")
mist = [("“P(A|B) is the same as P(B|A).”", "Different denominators. Say which is “given”."),
        ("“Exclusive events are independent.”", "If A happens, B can’t. That is dependence."),
        ("“The test is 95% accurate, so I’m 95% likely sick.”", "Include the base rate."),
        ("“At least 5” = 1 − cdf(5).", "It is 1 − cdf(4)."),
        ("“Tails is due after five heads.”", "The coin has no memory.")]
for i, (a, b) in enumerate(mist):
    y = 1.75 + i * 1.0
    rect(s, 0.6, y, 12.13, 0.88, fill=CARD, line=MINT)
    circle(s, 0.8, y + 0.2, 0.48, RED)
    text(s, 0.8, y + 0.2, 0.48, 0.48, "✕", size=16, bold=True, color="FFFFFF", align=PP_ALIGN.CENTER,
         anchor=MSO_ANCHOR.MIDDLE, space=0)
    text(s, 1.55, y, 6.2, 0.88, a, size=17, bold=True, color=DARK, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 7.9, y, 4.7, 0.88, b, size=15, color=TEAL, anchor=MSO_ANCHOR.MIDDLE)

# ================================================================== 19 HAND-OFF
s = new_slide(dark=True, notes=(
    "HAND-OFF: use the student notebooks next. 03_STUDENT_ai_tasks.ipynb (3 tasks to solve with AI, verification mandatory) and 04_STUDENT_group_presentations.ipynb (5 groups x 5 min).\n"
    "THE AI WORKFLOW: Understand, Prompt, Run, Verify, Reflect. The verify step (simulation) is what you are grading.\n"
    "Questions to ask the groups are in 04_INSTRUCTOR_group_presentations.ipynb."))
title(s, "Your turn", "Learn it, then use AI to check it", dark=True)
flow = [("1", "Understand", "Say what’s given and asked"), ("2", "Prompt", "Give all numbers, ask for assumptions + code"),
        ("3", "Run", "Run the code yourself"), ("4", "Verify", "Simulate or use a second method"),
        ("5", "Reflect", "Log what AI got right or wrong")]
for i, (n, h_, b_) in enumerate(flow):
    x = 0.6 + i * 2.45
    rect(s, x, 1.9, 2.3, 2.9, fill="145253")
    circle(s, x + 0.2, 2.1, 0.5, AMBER)
    text(s, x + 0.2, 2.1, 0.5, 0.5, n, size=17, bold=True, color=DARK, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, space=0)
    text(s, x + 0.2, 2.85, 1.9, 0.5, h_, size=19, bold=True, color="FFFFFF", font=HEAD)
    text(s, x + 0.2, 3.4, 1.9, 1.3, b_, size=14, color=MINT)
rect(s, 0.6, 5.2, 12.13, 1.4, fill=TEAL)
text(s, 0.95, 5.2, 11.4, 1.4,
     "You are accountable for the answer, not the AI. Never trust a number you haven’t verified.",
     size=22, color="FFFFFF", font=HEAD, bold=True, anchor=MSO_ANCHOR.MIDDLE)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
prs.save(OUT)
print("Saved", OUT, "| slides:", len(prs.slides))
print(f"post1 {post1:.4f} post2 {post2:.4f} p>=5 {p_ge5:.4f} z {z185:.2f} p>185 {p_gt185:.4f} q95 {q95:.1f} dE {dE:.2f} dV {dV:.3f} p0 {p0:.4f}")
print("LLN", LLN, "ways", ways)
