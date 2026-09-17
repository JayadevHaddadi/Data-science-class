# 🖍️ Whiteboard Masterclass: Data Visualization & Chart Selection

**Session**: Data Visualization Introduction & Chart Selection Framework  
**Classroom**: N209C (100% Whiteboard Friendly — Zero Projector Dependency)  
**Laptop Setup**: Keep your laptop open on your teacher desk showing `data_visualization_intro_solutions.ipynb` as your private teleprompter.

---

## 🧭 Board Layout Strategy

```
┌─────────────────────────┬──────────────────────────────────────┬───────────────────────────┐
│     LEFT COLUMN (25%)   │          CENTER STAGE (50%)          │    RIGHT COLUMN (25%)     │
│  "Matplotlib Code Rule" │       "Draw Charts & Comparisons"    │ "The 5 Analytic Puzzles"  │
└─────────────────────────┴──────────────────────────────────────┴───────────────────────────┘
```

---

## 🎨 Board 1: Anatomy of Matplotlib (10:50 – 11:10)

### 1. What to Draw in Center Stage:
Draw a big rectangular picture frame inside an outer canvas:

```text
┌─────────────────────────────────────────────────────────────┐
│ FIGURE (The Canvas / Window)                                │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ AXES (The Actual Subplot / Coordinate Space)        │   │
│   │                                                     │   │
│   │  Y-Axis Label     Title: "Weekly Scores"            │   │
│   │      ▲                                              │   │
│   │  100 ┼               *  (Data Point)                │   │
│   │      │              / \                             │   │
│   │   50 ┼─────────────*───*──────────── (Grid line)    │   │
│   │      │                                              │   │
│   │    0 ┴─────┼─────┼─────┼─────┼─────►                │   │
│   │            1     2     3     4     (X-Ticks)        │   │
│   │                   X-Axis Label                      │   │
│   │                                      [Legend]       │   │
│   └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 2. What to Write on the Left:
```text
The OO Pattern (Standard in Data Science):

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y, label='Scores')
ax.set_title("...")
ax.set_xlabel("...")
ax.set_ylabel("...")
ax.grid(True)
ax.legend()
plt.show()
```

### 3. What to Say Out Loud:
> *"Think of `Figure` as the picture frame hanging on your wall, and `Axes` as the actual painting inside the frame. In professional data science, we always use the Object-Oriented (`fig, ax`) style because it allows us to put multiple paintings inside one frame without getting confused."*

---

## 🎨 Board 2: Distribution — Histogram vs. Boxplot (11:10 – 11:30)

### 1. What to Draw (The Bimodal Trap):
Draw a Histogram with 2 distinct bumps on top, and draw a Boxplot right underneath it sharing the same X-axis:

```text
HISTOGRAM:
       Frequency
          ▲       Peak 1 (~12h)         Peak 2 (~25h)
          │         ┌─┐                   ┌─┐
          │        ┌┘ └┐                 ┌┘ └┐
          │      ┌─┘   └─┐             ┌─┘   └─┐
          └──────┴───────┴─────────────┴───────┴──────► Study Hours
                (Casual Cohort)       (Dedicated Cohort)

BOXPLOT (Directly underneath):
          ├─────────────┬──────────────────────────────┤
         Min           Q1             Q2              Q3            Max
                 (Notice: The valley in the middle is INVISIBLE!)
```

### 2. 💬 Analytic Discussion 1 to Ask the Room:
> **Question to the Class**: *"Look at the boxplot. Can you tell there are two completely different student cohorts? Why or why not?"*  
> **Answer to give**: *"No! Boxplots only show Q1, Median, and Q3. They completely flatten valleys and clusters. If you only look at a boxplot, you miss the multimodality of your audience. Always use Histograms/KDE alongside boxplots!"*

---

## 🎨 Board 3: Comparison & The "Truncated Axis" Lie (11:30 – 11:50)

### 1. What to Draw on the Board:
Draw two bar charts comparing CS (79%) vs Mechanical (74%):

```text
    CHART A (Misleading / Truncated)             CHART B (Honest Baseline)
    Y-Axis starts at 70:                         Y-Axis starts at 0:
    85 ┼                                        100 ┼
       │   ┌───┐                                    │   ┌───┐   ┌───┐
    80 ┼   │   │                                    │   │   │   │   │
       │   │   │   ┌───┐                         50 ┼   │   │   │   │
    75 ┼───│───│───│───│                            │   │   │   │   │
    70 ┴───┴───┴───┴───┴──                       0  ┴───┴───┴───┴───┴──
            CS     Mech                                  CS     Mech
    "CS looks 4x bigger!"                        "Real difference is < 5%!"
```

### 2. 💬 Analytic Discussion 2 to Ask the Room:
> **Question to the Class**: *"Why do news channels and marketing agencies truncate bar chart axes?"*  
> **Golden Rule of Data Ethics**:  
> *"The human brain judges a bar by its height and surface area. When you truncate the axis, you artificially magnify small differences. Bar charts MUST ALWAYS start at zero. (Line charts can start higher to show trends, but never bar charts!)."*

---

## 🎨 Board 4: Composition — Why Pie Charts Fail (11:50 – 12:10)

### 1. What to Draw:
Draw a 5-slice pie chart next to a stacked horizontal bar:

```text
PIE CHART (Hard to compare angles):           STACKED BAR (Easy to compare lengths):
           ┌─────────┐                         0h                 12h                24h
        .             .                        ┌──────┬────┬────┬──────┬───┐
      /    Sleep 29%    \                      │Sleep │Cls │Stdy│Leisur│Com│
     │ ────────┼───────  │                     └──────┴────┴────┴──────┴───┘
      \ Leisure \ Class /                       7.0h   5.5h 3.5h  6.2h  1.8h
        .  26%   \ 23%/
           └─────────┘
```

### 2. 💬 Analytic Discussion 3 to Ask the Room:
> **Question to the Class**: *"Looking at the pie chart slices, can your eye instantly tell if Leisure is larger than Class? Now look at the stacked bar. Which is faster to read?"*  
> **Rule of Thumb**:  
> *"Human vision is optimized for comparing linear position on a common scale. We struggle to evaluate angles and curved areas. Limit pie charts to 2 or 3 extreme slices (e.g., Yes 80% / No 20%). For anything else, use bars."*

---

## 🎨 Board 5: The Master Chart Selection Matrix (12:10 – 12:30)

Write this comprehensive summary on the board as students' permanent takeaway:

```text
╔════════════════════════════════════════════════════════════════════════════════╗
║                  📊 CHART SELECTION DECISION MATRIX                            ║
╠════════════════════════╦══════════════════════╦════════════════════════════════╣
║ WHAT ARE YOU ASKING?   ║ DATA TYPES           ║ WHAT CHART TO DRAW?            ║
╠════════════════════════╬══════════════════════╬════════════════════════════════╣
║ 1. Distribution        ║ 1 Continuous         ║ Histogram, KDE, Boxplot        ║
║ 2. Comparison          ║ 1 Category + 1 Num   ║ Bar Chart (bar / barh)         ║
║ 3. Time Trend          ║ Date/Time + Num      ║ Line Chart (with markers)      ║
║ 4. Composition         ║ Parts of 100%        ║ Stacked Bar (Avoid Pie >3)     ║
║ 5. Relationship        ║ 2 Continuous         ║ Scatter Plot (add hue for 3rd) ║
║ 6. Correlation         ║ Many Continuous      ║ Correlation Heatmap            ║
║ 7. Multi-Variable      ║ 3+ Continuous        ║ Pair Plot (sns.pairplot)       ║
╚════════════════════════╩══════════════════════╩════════════════════════════════╝
```
