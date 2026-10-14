# Class 04 · Presenter guide: what to show and say on each slide

Companion to `slides/Class04_Probability_Foundations.pptx` (19 slides). The same notes are in the speaker notes of each slide.
Whiteboard diagrams are in `slides/Class04_Whiteboard_Venn.pptx` (see the end of this file).

**Rule for the whole class:** on almost every slide, ask the question first, wait for answers in chat, then reveal. Students remember what they guessed.

---

## Slide 1 · Title
**Show:** the title slide.
**Say:** "Today we learn how to talk about uncertainty with numbers. Six ideas, each builds on the one before. By the end you'll be able to check an AI's probability answer."
**Know:** the speaker notes on this slide hold the timing and the cut list.

## Slide 2 · Roadmap
**Show:** the six cards.
**Say:** "Probability, then conditional probability, independence, Bayes, random variables, distributions."
**Ask:** "Name one decision you made this week under uncertainty." (Weather, traffic, exam.) Take two answers.
**Simple version:** probability is a number between 0 and 1 for how likely something is. 0 means impossible, 1 means certain.

## Slide 3 · Probability = what the proportion settles to
**Show:** the line chart of coin flips.
**Ask first:** "I flip 10 times. Will heads be exactly half?" Then "What about 5,000 flips?"
**Say:** "After 10 flips the proportion jumps around. By 5,000 it sits very close to 0.5. That's the Law of Large Numbers. A probability is what the proportion settles to in the long run."
**Key point:** short runs are random and messy. Long runs are stable.
**If asked "so is tails due after 5 heads?":** No. The coin has no memory. The law is about the long-run proportion, not about making up for the past.

## Slide 4 · Count the ways: two dice
**Show:** the bar chart of dice totals.
**Ask first:** "What's the most likely total of two dice?" (7.)
**Say:** "There are 36 equally likely outcomes. 7 can happen 6 ways, 2 and 12 only 1 way. More ways means more likely."
**Addition rule (right card):** "P(A or B) = P(A) + P(B) − P(A and B). We subtract the overlap because it was counted in both."
**Example:** A = first die is 6 (6 outcomes). B = total ≥ 10 (6 outcomes). Three outcomes are in both: (6,4), (6,5), (6,6). So 6 + 6 − 3 = 9 out of 36 = 0.25.
**Can cut:** this slide, if short on time.

## Slide 5 · P(A | B): shrink the world to B
**Show:** the 400-student table.
**Say:** "'Given' means we throw away everyone who isn't in B and look only at who's left. Of 400 students, 150 joined a study group."
**Ask first:** "The overall pass rate is 67.5%. Among study-group students, is it higher or lower?"
**Walk it:** 120 of the 150 in a group passed, so 120 ÷ 150 = **0.80**. Without a group: 150 ÷ 250 = **0.60**.
**Key point:** to condition, change the denominator to only the "given" group.
**Careful:** this shows association, not that study groups cause passing. Maybe keener students join groups.

## Slide 6 · P(A | B) is not P(B | A)
**Show:** the two big numbers, 80% and 44%.
**Say:** "Same table, two different questions. Of study-group students, 80% passed. Of students who passed, only 44% were in a study group, because most students aren't in groups at all."
**Walk it:** 120 ÷ 150 vs 120 ÷ 270. Same top number, different bottom numbers.
**Real example:** "Most accidents happen near home" doesn't mean home is dangerous. We just spend most of our time near home.
**This is the most common probability mistake, and it sets up Bayes.**

## Slide 7 · Independence
**Show:** the formula box and the three cards.
**Say:** "Two events are independent if knowing one tells you nothing about the other."
**Test:** multiply P(A) × P(B). If it equals P(A and B), they're independent.
**Dice example:** A = first die is even (1/2). B = total is 7 (1/6). 1/2 × 1/6 = 1/12. P(both) = 3/36 = 1/12. Same, so independent. (Surprising, because for any first die there's exactly one second value that makes 7.)
**Cards:** with replacement, an ace then an ace is 4/52 either time. Without replacement, the second is 3/51. The deck changed, so they're dependent.
**Trap card:** "mutually exclusive means can't both happen." If A happens, B can't, so knowing A tells you a lot. Exclusive events are dependent.
**Ask:** "Are 'first die is 1' and 'first die is 6' independent?" (No.)

## Slide 8 · A positive test: how worried should you be?
**Show:** the three boxes.
**Ask first, before showing the slide:** "A disease affects 1% of people. The test catches 95% of sick people and gives a false alarm for 5% of healthy people. You test positive. How likely are you sick?" Collect guesses in chat. Most will say 95%.
**Say:** "Imagine 10,000 people. 100 are sick. 9,900 are healthy."
- Of 100 sick, 95 test positive.
- Of 9,900 healthy, 5% test positive: 495 false alarms.
- Total positives: 590. Only 95 of them are sick.
- 95 ÷ 590 = **16.1%**.

**Key point:** the healthy group is 99 times bigger, so even a small false-alarm rate gives a lot of false alarms. This is called ignoring the base rate.
**Tip:** do the counting out loud, slowly. Don't mention the formula yet.

## Slide 9 · Same test, different base rate
**Show:** the formula and the bar chart.
**Say:** "Now the same thing as a formula. P(sick | positive) = P(positive | sick) × P(sick) ÷ P(positive)."
**Walk the four steps:**
1. Prior: P(sick) = 0.01.
2. Likelihoods: 0.95 if sick, 0.05 if healthy.
3. Total P(positive) = 0.95 × 0.01 + 0.05 × 0.99 = 0.059.
4. Divide: 0.0095 ÷ 0.059 = 0.161.

**The chart:** the test is the same, but at 1% prevalence a positive means 16%, at 10% it means 68%, at 50% it means 95%. How common the thing is matters as much as how good the test is.
**Say:** "The formula is just the counting from the last slide written as fractions."

## Slide 10 · Evidence accumulates
**Show:** 1% → 16% → 78%.
**Say:** "Yesterday's posterior is today's prior. After a first positive, you're at 16%. A second independent positive takes you to 78%."
**Why independent:** otherwise the same error repeats and you count the same evidence twice.
**Link:** spam filters and diagnosis systems work this way. The spam task in the student notebook uses it.
**Can cut:** this slide, if short.

## Slide 11 · X = days until delivery
**Show:** the bar chart and the cards.
**Say:** "A random variable turns outcomes into numbers. X is how many days a delivery takes. Half the time 1 day, 30% 2 days, 20% 3 days. The bars add up to 1."
**Walk E[X]:** 1×0.5 + 2×0.3 + 3×0.2 = **1.7 days**. A weighted average.
**Variance:** how far values are from 1.7, squared, weighted. = 0.61. SD = 0.78 days, the typical distance from the mean.
**Ask:** "If I order 1,000 items, about how many total delivery days?" (1,700.)
**Careful:** 1.7 isn't the most likely value (that's 1 day), and no single delivery takes 1.7 days.

## Slide 12 · Transforming X
**Show:** the three rows.
**Say:** "If every delivery gets a fixed fee of 5 plus 2 per day, cost = 5 + 2X."
- Mean: E[aX + b] = a·E[X] + b. So 5 + 2×1.7 = 8.4.
- Variance: Var(aX + b) = a²·Var(X). So 4 × 0.61 = 2.44.

**Simple version:** adding 5 shifts everything but doesn't change how spread out it is. Multiplying by 2 doubles the spread, so the variance goes up 4 times.
**Link:** this is what the casino-game student task needs.
**Can cut** if short.

## Slide 13 · Binomial
**Show:** the bar chart.
**Say:** "10 customers walk in. Each buys with probability 0.3. X is how many buy. The bars are P(exactly k buyers). The tallest is 3, which is n × p."
**Use it when:** a fixed number of tries, yes/no each time, same chance each time, independent.
**The trap (right card):** `cdf(4)` means P(X ≤ 4), the running total up to and including 4. For "at least 5", you want everything to the right of 4, which is 1 − cdf(**4**) = 0.150. Not cdf(5).
**Ask:** "Which bars do I add for 'at most 2'?" (0, 1, 2.)

## Slide 14 · Poisson
**Show:** the orange bar chart.
**Say:** "Emails arrive at random, 3 per hour on average. X is how many in one hour. There's no fixed number of tries, and no maximum."
**Signature:** mean = variance = λ (here 3).
**P(no emails)** = e⁻³ = 0.05. A 5% chance of a completely quiet hour.
**Binomial vs Poisson:** Binomial has a fixed n and a maximum. Poisson counts events with no maximum.
**Ask:** "Calls per minute: Binomial or Poisson?" (Poisson.) "Heads in 10 flips?" (Binomial.)

## Slide 15 · Normal
**Show:** the bell curve and the table.
**Say:** "Heights: mean 170, SD 8. Most people are near 170, very tall or short are rare. Probability is the area under the curve. The chance of exactly 170.0000 is zero, so we always ask about ranges."
**68–95–99.7 rule:** about 68% within 1 SD (162 to 178), 95% within 2 (154 to 186), 99.7% within 3.
**Tools (bottom card):**
- z-score = (185 − 170) ÷ 8 = 1.88. How many SDs above average.
- P(X > 185) = 1 − cdf = 0.030, about 3%.
- ppf(0.95) = 183.2 cm. The height that 95% of people are below.

**Simple version:** `cdf` takes a value and gives a share. `ppf` takes a share and gives a value.

## Slide 16 · Central Limit Theorem
**Show:** the histogram.
**Ask first:** "Raw data is very skewed. What will the average of 30 draws look like?"
**Say:** "Each bar counts averages of 30 draws from a strongly skewed distribution. The result is a bell centred on 1. Averages are bell-shaped even when the data isn't."
**Why:** averaging cancels the ups and downs. There are many more ways to land in the middle than at the extremes.
**Also:** the average is narrower. SD of an average = σ ÷ √n = 1 ÷ √30 = 0.18.
**Why it matters:** this is the bridge to statistical inference next class.
**Can cut** to one sentence if short.

## Slide 17 · Which distribution?
**Show:** the table.
**Say:** "One yes/no trial: Bernoulli. Successes out of n tries: Binomial. Events in a time window: Poisson. Measurements around a mean: Normal. Averages: roughly Normal."
**Quick quiz:** heights? (Normal.) Goals in a match? (Poisson.) Correct answers when guessing 10 quiz questions? (Binomial.)

## Slide 18 · Five mistakes
**Show:** the list.
**Say:** "Which of these have we seen today?" Pick two and ask for an example.
**Map:** mistake 1 → slide 6, 2 → slide 7, 3 → slide 8, 4 → slide 13, 5 → slide 3.

## Slide 19 · Learn it, then use AI to check it
**Show:** the five steps.
**Say:** "Understand, Prompt, Run, Verify, Reflect. The step that matters is Verify. If an AI gives you a probability, simulate it and see if the numbers agree. You are accountable for the answer, not the AI."
**Then:** hand out `03_STUDENT_ai_tasks.ipynb` and the group presentation notebook.

---

## If you only remember 5 things
1. **Conditional probability** = change the denominator to the "given" group.
2. **P(A|B) ≠ P(B|A)**: different bottom numbers.
3. **Bayes:** imagine 10,000 people and count. Don't start with the formula.
4. **E[X]** is a long-run average, not a value you'll necessarily see.
5. **"At least k" = 1 − cdf(k−1).**

## If you freeze mid-class
- Say: "Let me show it with numbers" and go to a count of 10,000 people or a table.
- Ask the class a question. It buys time and gets them thinking.
- Say: "Good question, let's simulate it," and run a short loop in the notebook. Simulation always works.

## Preparation tip
Practise slides 5, 6 and 8 out loud once, with the calculator in hand. Those three are where most of the confusion happens, and where you'll feel most confident if they land.

---

## Whiteboard deck: `slides/Class04_Whiteboard_Venn.pptx`
Six slides to redraw on the board (each has a "draw it like this" note). Use them next to slides 4–9:

| Slide | Draws | Goes with |
|---|---|---|
| 1 | Sample space as a rectangle, an event as a circle | slide 4 |
| 2 | Two overlapping circles: the addition rule | slide 4 |
| 3 | Conditional probability: the world shrinks to one circle | slides 5–6 |
| 4 | Independence as a box split into strips | slide 7 |
| 5 | Bayes with two overlapping circles (sick, positive) | slides 8–9 |
| 6 | All the formulas on one page | any time |
