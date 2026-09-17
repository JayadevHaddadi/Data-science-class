# 📋 Complete Classroom Teaching Guide & Lesson Plan

**Session**: Statistical Functions in the Context of Exploratory Data Analysis (EDA)  
**Date & Time**: Thursday, Sept 17 | 10:50 AM – 12:30 PM (100 minutes)  
**Room**: N209C  
**Dataset**: `student_learning_performance_eda_150.csv` (150 students, 9 features)  
**Files Prepared**:
- `student_learning_performance_eda_150.csv`: Ready dataset.
- `statistical_functions_eda_class.ipynb`: Ready-to-use interactive Jupyter Notebook.
- `instructor_solutions_and_demo.py`: Answer key with exact computations.

---

## ⏱️ Recommended 100-Minute Timeline & Class Architecture

```
10:50 - 11:00 (10m) | Warm-up & Motivation: "Why Stats in EDA?"
11:00 - 11:25 (25m) | Block 1: describe(), Mean vs Median vs Mode, Std Dev, & Skewness
11:25 - 11:50 (25m) | Block 2: Percentiles, Quartiles, IQR & Outlier Detection (Tukey's Rule)
11:50 - 12:15 (25m) | Block 3: Comparative Grouping (groupby + agg) & Relationships (corr vs cov)
12:15 - 12:30 (15m) | Debrief, Mini-Challenge & Real-World Takeaway
```

---

## 🎬 Section-by-Section Teaching Guide

### 1. Warm-Up & Motivation (10:50 – 11:00 | 10 mins)
* **Goal**: Shift students from seeing statistics as "dry math formulas" to seeing it as "detective forensic tools".
* **What to Say**:
  > *"When you open a dataset with 50,000 rows, you can't read every row. You need summary statistics to act as your eyes. But summary statistics can also lie to you if you don't know their quirks. Today, we learn how to uncover the true shape of our data, spot anomalies, and avoid common traps."*
* **Quick Action**:
  - Have everyone open `statistical_functions_eda_class.ipynb` or load `student_learning_performance_eda_150.csv`.
  - Run `df.head()` and `df.info()`. Briefly explain the variables (hours studied, past score, attendance, sleep, final exam score).

---

### 2. Block 1: Overview, Central Tendency, Spread & Skewness (11:00 – 11:25 | 25 mins)

#### A. What to Show & Talk About (15 mins)
1. **`df.describe()`**:
   - Run `df.describe().T`.
   - Point out that it gives the **5-number summary** (min, 25%, 50%, 75%, max) plus `count`, `mean`, and `std`.
2. **Mean vs. Median vs. Mode**:
   - Draw the classic intuition on the board:
     - *If 9 students earn $50k and 1 billionaire walks in, what happens to the mean? (Skyrockets). What happens to the median? (Stays the same).*
   - **Mean**: Great for symmetric, bell-shaped data; heavily distorted by outliers.
   - **Median**: Robust to extreme values; the actual "middle student".
   - **Mode**: Best for discrete/categorical counts (e.g., `assignments_completed.mode()[0] = 8`).
3. **Variance & Standard Deviation**:
   - Explain why we take the square root of variance: *Variance is in "squared points" ($\text{pts}^2$). Standard deviation is in the same units as the data (points)!*
4. **Skewness & Distribution Shape**:
   - **Right (Positive) Skew**: Tail pulls right $\rightarrow$ $\text{Mean} > \text{Median}$ (e.g., `study_hours_per_week`: mean 18.3 > median 17.0).
   - **Left (Negative) Skew**: Tail pulls left $\rightarrow$ $\text{Mean} < \text{Median}$ (e.g., `attendance_rate`: mean 77.8 < median 79.6).
   - Rule of thumb: $|Skew| < 0.5$ (symmetric), $0.5 \le |Skew| \le 1$ (moderately skewed), $|Skew| > 1$ (highly skewed).

#### B. Quick Class Poll / Question to Ask
- *"Look at `sleep_hours`: Mean is 7.18, Median is 7.10. Skewness is 0.20. Is this skewed or symmetric?"*
  - *Answer: Symmetric / approximately normal.*

#### C. Student Hands-on Micro-Exercise 1 (10 mins)
* **Prompt**:
  1. Calculate the mean, median, and standard deviation for `attendance_rate`.
  2. Compare mean vs median. Which direction is it skewed?
  3. Compute `df['assignments_completed'].mode()[0]`.
* **Instructor Walk-around**: Ensure students use `.mean()`, `.median()`, `.std()`, and `.mode()[0]`.

---

### 3. Block 2: Percentiles, Quartiles, IQR & Outlier Detection (11:25 – 11:50 | 25 mins)

#### A. What to Show & Talk About (15 mins)
1. **Percentiles & Quartiles**:
   - $Q_1$ = 25th percentile, $Q_2$ = Median (50th percentile), $Q_3$ = 75th percentile.
   - $\text{IQR} = Q_3 - Q_1$: The range of the "middle 50%" of students.
2. **Tukey's 1.5 $\times$ IQR Rule**:
   - Why 1.5? (John Tukey chose 1.5 as the sweet spot for capturing ~99.3% of normal distribution data).
   - $\text{Lower Bound} = Q_1 - 1.5 \times \text{IQR}$
   - $\text{Upper Bound} = Q_3 + 1.5 \times \text{IQR}$
3. **Connecting Numbers to Boxplots**:
   - Project a `sns.boxplot(x=df['study_hours_per_week'])`.
   - Show students the box (IQR), the line in the middle (median), the whiskers ($1.5 \times \text{IQR}$), and the points beyond (outliers!).
4. **Critical Thinking Discussion: "What should we do with outliers?"**
   - *Never blindly delete outliers!*
   - Is it a data entry error (e.g. 500 hours/week)? Fix or drop.
   - Is it a real student with unique behavior (e.g. studying 58 hours/week)? Keep and analyze!

#### B. Student Hands-on Micro-Exercise 2 (10 mins)
* **Prompt**:
  1. Calculate $Q_1$, $Q_3$, and $\text{IQR}$ for `attendance_rate`.
  2. Calculate the lower threshold ($Q_1 - 1.5 \times \text{IQR}$).
  3. Filter the dataframe to isolate students with outlier attendance:
     `df[df['attendance_rate'] < lower_bound]`
  4. How many students are outliers, and did low attendance crash their final score?

---

### 4. Block 3: Group Aggregation & Relationships (11:50 – 12:15 | 25 mins)

#### A. What to Show & Talk About (15 mins)
1. **`groupby()` + `agg()`**:
   - Why simple averages mislead: Show how grouping reveals hidden patterns (Simpson's Paradox concept).
   - Show syntax:
     ```python
     df.groupby('study_group')['final_exam_score'].agg(['count', 'mean', 'median', 'std'])
     ```
   - Multi-column aggregation: Group by both `study_group` and `prep_course`.
2. **Covariance vs. Pearson Correlation**:
   - **Covariance ($Cov(X, Y)$)**: Measures if two variables increase or decrease together.
     - *Flaw*: Its magnitude depends on units ($hours \times points$). A covariance of 40.4 is hard to interpret.
   - **Pearson Correlation ($r$)**: Covariance divided by the product of both standard deviations.
     - Normalized strictly to $[-1.0, +1.0]$.
     - Scale-free, universally comparable.
3. **Visualizing with Heatmap**:
   - Run `sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')`.
4. **Golden Rule: Correlation $\neq$ Causation**:
   - Just because $r > 0$, does changing $X$ cause $Y$? Discuss lurking/confounding variables!

#### B. Student Hands-on Micro-Exercise 3 (10 mins)
* **Prompt**:
  1. Group by `prep_course` and compute `count`, `mean`, and `std` of `final_exam_score`.
  2. Compute the correlation between `past_exam_score` and `final_exam_score`.
  3. Check the correlation between `sleep_hours` and `final_exam_score`. Is more sleep correlated with higher scores?

---

### 5. Debrief & Synthesis Challenge (12:15 – 12:30 | 15 mins)

* **The 5-Minute Class Challenge**:
  > *"Imagine you are an academic advisor. Using the statistical tools from today (outliers, group metrics, correlations), write 2 bullet points on how to identify a student who needs academic intervention before the final exam."*
* **Ask 2 students to share their answers aloud**.
* **Wrap-up Summary on the Board**:
  1. `describe()` gives you the baseline radar.
  2. Always compare Mean vs Median to test for Skew.
  3. Use IQR & Boxplots to catch extreme behaviors.
  4. Use `groupby().agg()` to slice comparisons across categories.
  5. Use Correlation matrices to spot candidate features for machine learning.
