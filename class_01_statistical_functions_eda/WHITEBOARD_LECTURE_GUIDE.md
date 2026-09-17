# 🖍️ Whiteboard Masterclass: EDA & Statistical Functions

**Classroom**: N209C (No Projector / HDMI — 100% Whiteboard Driven)  
**Time**: 10:50 – 12:30 (100 Minutes)  
**Strategy**: Keep your laptop open on the teacher desk running `instructor_solutions_and_demo.py` or this guide as your private monitor. Write these diagrams and clean toy examples on the whiteboard.

---

## 🧭 Board Layout Strategy

Divide the whiteboard into 3 physical columns or sections:

| Column 1 (Left: 25%) | Column 2 (Center: 50%) | Column 3 (Right: 25%) |
|---|---|---|
| **Formulas & Python Code**<br>(Keep this static as reference) | **Visual Diagrams & Curves**<br>(Draw shapes, boxplots, curves) | **Student Activity & Data**<br>(Toy examples & numbers) |

---

## 🎨 Board 1: The Detective's Overview & Central Tendency (11:00 – 11:20)

### 1. What to Write on the Board:
```text
[TOPIC 1: OVERVIEW & CENTRAL TENDENCY]

df.describe()  --> The 8-Number Summary:
  1. count
  2. mean      (Average)
  3. std       (Spread)
  4. min   \
  5. 25%    \
  6. 50%     --> "5-Number Summary" (Tukey)
  7. 75%    /
  8. max   /

CENTRAL TENDENCY: "Where is the center?"
1. MEAN   = Sum(X) / N                     --> Sensitive to outliers!
2. MEDIAN = Middle value (when sorted)      --> Robust to outliers!
3. MODE   = Most frequent value            --> Great for discrete counts
```

### 2. The Killer Whiteboard Example to Draw:
Draw this simple number line with 5 students' quiz scores:
```text
Scores: [ 60,  70,  75,  80,  90 ]
        Mean = 75,  Median = 75  (Balanced!)

Now an outlier arrives (score of 0 or a genius score of 1000):
Scores: [ 60,  70,  75,  80,  1000 ]
        Median = 75   (STILL 75! Unfazed)
        Mean   = 257  (Completely broken!)
```

### 3. What to Say Out Loud:
> *"If Jeff Bezos walks into this classroom, the average wealth of this room jumps to $500 million. Did any of us get richer? No. That’s why Mean alone is dangerous. Whenever you see a mean, always check the median!"*

### 4. Code to Write in Corner of Board:
```python
df['final_exam_score'].mean()
df['final_exam_score'].median()
df['assignments_completed'].mode()[0]
```

---

## 🎨 Board 2: Spread (Variance/Std) & Skewness Curves (11:20 – 11:40)

### 1. What to Write on the Board:
```text
[TOPIC 2: SPREAD & SHAPE]

Variance (s^2) = sum(x - mean)^2 / (N - 1)   --> units are squared (pts^2)
Std Dev  (s)   = sqrt(Variance)              --> original units (pts)

Intuition:
Small Std Dev = Students clustered closely around the mean.
Large Std Dev = Massive gap between top and bottom performers.
```

### 2. The 3 Curves to Draw on the Board:
Draw these three smooth hill curves:

```text
1. SYMMETRIC (Normal)          2. RIGHT-SKEWED (Positive)        3. LEFT-SKEWED (Negative)
   "Bell Curve"                   "Tail stretches Right"           "Tail stretches Left"

        ▲                                ▲                                ▲
       / \                              / \                              / \
      /   \                            /   \                            /   \
     /     \                          /     \______                    ______/     \
    /       \                        /             \                  /             \
   ───────────                      ─────────────────                ─────────────────
   Mean = Median                    Median < Mean                    Mean < Median
   (Skew ≈ 0)                       (Skew > 0)                       (Skew < 0)
   Example: sleep_hours             Example: study_hours             Example: attendance_rate
```

### 3. What to Say Out Loud:
> *"The mean is an outlier magnet! Wherever the long tail goes, the mean gets dragged along with it. If the tail is on the right, Mean > Median. If the tail is on the left, Mean < Median."*

### 4. Code to Write on Board:
```python
df['study_hours_per_week'].skew()    # returns > 0 (Right Skewed)
df['attendance_rate'].skew()          # returns < 0 (Left Skewed)
```

---

## 🎨 Board 3: The Boxplot & Outlier Detection (11:40 – 12:00)

This is the most visually satisfying part of the lecture. Draw a large, clear horizontal boxplot.

### 1. The Anatomy of a Boxplot to Draw:

```text
       Lower Fence                                                  Upper Fence
     Q1 - 1.5 * IQR                                               Q3 + 1.5 * IQR
           │                                                            │
    *  *   ├─────────────┬───────────────────┬──────────────────────────┤     *
  Outlier  │             │                   │                          │  Outlier
 (< Fence) Min           Q1             Q2 (Median)                    Max (> Fence)
                      (25th %)            (50th %)                   (75th %)

                         └────────┬──────────┘
                                 IQR
                           (Middle 50%)
```

### 2. Write Tukey's Formulas on Board:
```text
1. IQR = Q3 - Q1
2. Lower Fence = Q1 - (1.5 * IQR)
3. Upper Fence = Q3 + (1.5 * IQR)
Rule: Any point outside the fences is an OUTLIER.
```

### 3. Quick Board Calculation (Using real dataset numbers):
Write these numbers on the board:
```text
Dataset: study_hours_per_week
  Q1 = 12.0 hrs
  Q3 = 22.2 hrs
  IQR = 22.2 - 12.0 = 10.2 hrs

  Upper Fence = 22.2 + (1.5 * 10.2)
              = 22.2 + 15.3 = 37.5 hrs

  Student STU_1089 studied 58.0 hrs!
  Since 58.0 > 37.5 --> OUTLIER!
```

### 4. Python Code for Students to Write:
```python
q1 = df['study_hours_per_week'].quantile(0.25)
q3 = df['study_hours_per_week'].quantile(0.75)
iqr = q3 - q1
upper_fence = q3 + 1.5 * iqr
df[df['study_hours_per_week'] > upper_fence]
```

---

## 🎨 Board 4: Grouping (groupby + agg) & Correlation (12:00 – 12:20)

### 1. The "Split-Apply-Combine" Diagram:
Draw 3 boxes with arrows:

```text
   [ Raw Data: 150 Students ]
               │
      SPLIT by 'prep_course'
        ┌──────┴──────┐
        ▼             ▼
   [Completed]     [None]
   (64 students) (86 students)
        │             │
      APPLY mean(), std()
        │             │
      COMBINE into 1 Table
        ▼
┌────────────┬───────┬────────────┬───────────┐
│ prep_course│ count │ mean_score │ std_score │
├────────────┼───────┼────────────┼───────────┤
│ Completed  │   64  │   78.6     │   10.4    │
│ None       │   86  │   73.4     │    7.9    │
└────────────┴───────┴────────────┴───────────┘
```

### 2. Covariance vs. Correlation (Draw this table):
```text
                       COVARIANCE                CORRELATION (r)
Formula:               Cov(X, Y)                 Cov(X, Y) / (std_X * std_Y)
Range:                 -∞ to +∞                  -1.0 to +1.0
Units:                 hrs * points (confusing)  Unitless (standardized)
Interpretation:        Only shows direction      Shows DIRECTION + STRENGTH
```

### 3. Draw the 4 Mini Scatterplots:
```text
   r = +1.0                  r = -0.8                   r = 0.0                   Non-linear (r ≈ 0)
      ▲                         ▲                         ▲                         ▲
      │       /                 │   \                     │   .  .  .               │      .  .
      │     /                   │     \                   │  .  .  .  .             │    .      .
      │   /                     │       \                 │   .  .  .               │   .        .
      └──────►                  └──────►                  └──────►                  └──────►
  (Strong Positive)         (Strong Negative)           (No Relation)             (Curved - trap!)
```

### 4. The Golden Rule to Write in Big Letters:
```text
⚠️ CORRELATION ≠ CAUSATION!
Example: As ice cream sales rise, drowning deaths rise.
Does ice cream cause drowning? NO! Confounding factor: Summer heat!
```

---

## 🎯 Wrap-Up & Exit Ticket (12:20 – 12:30 | 10 mins)

Write this single prompt on the board for the whole class:

```text
╔══════════════════════════════════════════════════════════════════════╗
║                    🎓 5-MINUTE EXIT CHALLENGE                         ║
║                                                                      ║
║  You are an academic advisor. Write down:                            ║
║  1. Which 2 metrics would you use to flag an "at-risk" student?      ║
║  2. Why would you use MEDIAN instead of MEAN for class attendance?   ║
╚══════════════════════════════════════════════════════════════════════╝
```
Ask 2 students to shout out their answers before dismissing the class!
