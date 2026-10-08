# 📊 Data Science Class: Interactive Labs & Lecture Notes

A structured repository containing practical curriculum, datasets, Jupyter notebooks, lesson plans, and whiteboard guides for university-level Data Science and Exploratory Data Analysis (EDA).

---

## 📂 Repository Structure

```
Data-science-class/
├── README.md                                  # Repository overview and quickstart
├── requirements.txt                           # Python dependencies
├── .gitignore                                 # Clean version control exclusions
│
├── class_01_statistical_functions_eda/        # Session 1: Statistical Functions in EDA
│   ├── README.md                              # Class overview and objectives
│   ├── student_learning_performance_eda_150.csv # 150-student dataset
│   ├── statistical_functions_eda_class.ipynb  # Interactive student lab notebook
│   ├── statistical_functions_eda_class_solutions.ipynb # Pre-rendered solutions notebook
│   ├── WHITEBOARD_LECTURE_GUIDE.md            # Whiteboard sketches, curves & layouts
│   ├── CLASS_LESSON_PLAN.md                   # 100-minute instructional timeline
│   ├── instructor_solutions_and_demo.py       # Terminal verification script
│   └── scripts/                               # Data and notebook generation scripts
│
└── class_02_data_visualization_intro/         # Session 2: Data Visualization & Chart Selection
    ├── README.md                              # Class overview and objectives
    ├── data_visualization_intro.ipynb         # Student notebook (Code included + 5 Discussions)
    ├── data_visualization_intro_solutions.ipynb # Pre-rendered reference notebook
    ├── WHITEBOARD_LECTURE_GUIDE.md            # Whiteboard visual charts & decision matrix
    ├── CLASS_LESSON_PLAN.md                   # 100-minute instructional timeline
    ├── datasets/                              # Datasets used in visualization lab
    │   ├── student_demographics_performance.csv # 250 students cross-sectional data
    │   └── student_weekly_trends.csv          # 12-week longitudinal study & stress trends
    └── scripts/                               # Data and notebook generation scripts
```

---

## 🚀 Quickstart & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Running in VS Code
1. Open this repository folder in **VS Code**.
2. Open any `.ipynb` notebook file.
3. In the top right corner of the notebook, click **"Select Kernel"** $\rightarrow$ **"Python Environments..."** $\rightarrow$ Select your Python installation.
4. Click **"Run All"** or run cells interactively with `Shift + Enter`.

---

## 📑 Syllabus & Sessions

### [Class 01: Statistical Functions in EDA](class_01_statistical_functions_eda/)
- **Summary Statistics**: `describe()`, 5-number summary
- **Central Tendency & Spread**: Mean vs. Median vs. Mode, Variance & Standard Deviation
- **Anomalies & Shape**: Percentiles, IQR, Tukey's Outlier Rule, Skewness
- **Comparative Analysis**: `groupby()` + `agg()`, Covariance & Correlation ($r$)

### [Class 02: Data Visualization Introduction](class_02_data_visualization_intro/)
- **Matplotlib Foundations**: Anatomy of a plot (`Figure` vs `Axes`), Object-Oriented interface
- **Chart Selection Framework**:
  - **Distribution**: Histogram, KDE, Boxplot (Bimodal distributions)
  - **Comparison**: Bar charts (vertical, horizontal, grouped) & Truncated Axis ethics
  - **Time Trend**: Multi-series line charts with annotations
  - **Composition**: Stacked bar charts vs. Pie charts (Perception psychophysics)
  - **Relationship & Correlation**: Scatter plots with regression lines and correlation heatmaps
  - **Multivariate**: Pair plots (`sns.pairplot`)
  - **Geographic Pattern**: Regional ranking & lollipop charts

### [Class 03: EDA Deep Dive (online)](class_03_eda_deep_dive/)
- **Distributions & Shape**: bimodal, skewed, hidden mixtures
- **Anomalies**: data-quality audit, sentinels, missingness patterns, outlier vs error
- **Relationships & Correlation**: heatmaps, causation vs association, non-linear patterns
- **Grouping**: `groupby`, Simpson's paradox, confounding
- **Format**: Colab notebooks, solo Data Detective task, 5 team missions with pitches

### [Class 04: Probability Foundations + AI-Assisted Problem Solving](class_04_probability_foundations/)
- **Probability**: concepts, conditional probability, independence, Bayes' theorem
- **Random variables & distributions**: expected value, variance, Binomial, Poisson, Normal, CLT
- **AI workflow**: Understand → Prompt → Run → Verify → Reflect; 3 live demo tasks + 3 student tasks
