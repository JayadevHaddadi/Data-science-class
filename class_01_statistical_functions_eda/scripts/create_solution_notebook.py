import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 📊 Exploratory Data Analysis: Statistical Functions in Python (INSTRUCTOR SOLUTIONS)\n",
    "**Course**: Data Science Class | **Session**: Statistical Functions in EDA  \n",
    "**Classroom**: N209C | **Time**: 10:50 - 12:30  \n",
    "**Dataset**: `student_learning_performance_eda_150.csv` (150 students)  \n",
    "\n",
    "> 💡 **Presenter Tip**: You can run this entire notebook cell-by-cell on your projector! Each section includes **\"🗣️ What to say\"** and **\"👀 What to point out\"** notes so you never feel lost."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 0. Setup & Data Loading\n",
    "**🗣️ What to say:**  \n",
    "*\"Welcome everyone! Today we are doing exploratory data analysis (EDA). We have data for 150 students covering study hours, attendance, past exam scores, sleep, and final scores. Before we jump into math, let's load our libraries and inspect the first 5 rows.\"*"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "\n",
    "# Set clean styling for plots\n",
    "pd.set_option('display.max_columns', None)\n",
    "sns.set_theme(style=\"whitegrid\", palette=\"muted\")\n",
    "\n",
    "# Load the dataset\n",
    "df = pd.read_csv('student_learning_performance_eda_150.csv')\n",
    "print(f\"Dataset loaded: {df.shape[0]} rows and {df.shape[1]} columns.\")\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## Part 1: Quick Statistical Overview (`describe()`)\n",
    "\n",
    "**🗣️ What to say:**  \n",
    "*\"Instead of checking every student one by one, `df.describe()` gives us an instant summary. In one line, we get the count, the mean, the standard deviation, and the famous '5-number summary' (min, 25%, 50% median, 75%, max).\"*"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Transpose with .T so rows are variables, which makes it much easier to read!\n",
    "df.describe().T[['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']].round(2)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**👀 What to point at on screen:**\n",
    "1. Look at `study_hours_per_week`: **Mean is 18.3**, but **Median (50%) is 17.0**, and **Max is 58.0**!\n",
    "2. **Ask the class**: *\"Why is the mean higher than the median?\"*\n",
    "3. **Answer to give**: A couple of students studied 50+ hours. Those extreme values pull the mean upward, while the median stays steady in the middle."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## Part 2: Mean, Median, Mode, Variance & Standard Deviation\n",
    "\n",
    "**🗣️ What to say:**  \n",
    "- **Mean**: Sum divided by count. Great for symmetric bell curves, but easily tricked by extreme values.\n",
    "- **Median**: The middle value when sorted. Extremely robust against outliers.\n",
    "- **Mode**: The most frequently occurring value. Ideal for discrete counts and survey categories.\n",
    "- **Variance**: Average squared deviation from the mean. Problem: units are squared (e.g. $\\text{hours}^2$).\n",
    "- **Standard Deviation**: $\\sqrt{\\text{Variance}}$. Back in original units! Shows the typical spread of data."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Computing statistics on final_exam_score\n",
    "score_mean = df['final_exam_score'].mean()\n",
    "score_median = df['final_exam_score'].median()\n",
    "score_std = df['final_exam_score'].std()\n",
    "score_var = df['final_exam_score'].var()\n",
    "assign_mode = df['assignments_completed'].mode()[0]  # [0] picks the first mode\n",
    "\n",
    "print(f\"Final Exam Score - Mean:               {score_mean:.2f} points\")\n",
    "print(f\"Final Exam Score - Median:             {score_median:.2f} points\")\n",
    "print(f\"Final Exam Score - Standard Deviation: {score_std:.2f} points\")\n",
    "print(f\"Final Exam Score - Variance:           {score_var:.2f} points^2\")\n",
    "print(f\"Assignments Completed - Mode:          {assign_mode} assignments (most common)\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 🧪 In-Class Exercise 1 (Give students 5 minutes)\n",
    "**Prompt for students:**\n",
    "> *\"Calculate the mean, median, and standard deviation for `attendance_rate`. Is the mean higher or lower than the median? What does that tell you about how most students attend class?\"*\n",
    "\n",
    "*(While students work: walk around, see if anyone is stuck on typing `df['attendance_rate'].mean()`)*"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# ✅ SOLUTION TO EXERCISE 1:\n",
    "att_mean = df['attendance_rate'].mean()\n",
    "att_median = df['attendance_rate'].median()\n",
    "att_std = df['attendance_rate'].std()\n",
    "\n",
    "print(f\"Attendance Mean:   {att_mean:.2f}%\")\n",
    "print(f\"Attendance Median: {att_median:.2f}%\")\n",
    "print(f\"Attendance Std:    {att_std:.2f}%\")\n",
    "\n",
    "# 🗣️ Explanation to tell the class:\n",
    "# \"Notice that the Mean (77.83%) is LOWER than the Median (79.55%).\"\n",
    "# \"This means a few students with very bad attendance (e.g. 28%) are dragging the average down.\""
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## Part 3: Skewness & Distribution Shape\n",
    "\n",
    "**🗣️ What to say:**  \n",
    "- **Skewness = 0**: Perfectly symmetric (Bell curve). Mean $\\approx$ Median.\n",
    "- **Positive Skew (> 0)**: Long tail to the right. Mean $>$ Median (e.g. income, study hours).\n",
    "- **Negative Skew (< 0)**: Long tail to the left. Mean $<$ Median (e.g. attendance, retirement age)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Print skewness of all numerical columns\n",
    "print(\"--- SKEWNESS VALUES ---\")\n",
    "print(df.select_dtypes(include=np.number).skew().round(2))\n",
    "\n",
    "# Plot the two contrasting distributions\n",
    "fig, axes = plt.subplots(1, 2, figsize=(14, 4))\n",
    "\n",
    "# 1. Right Skewed\n",
    "sns.histplot(df['study_hours_per_week'], kde=True, ax=axes[0], color='teal')\n",
    "axes[0].axvline(df['study_hours_per_week'].mean(), color='red', linestyle='--', linewidth=2, label='Mean (18.3)')\n",
    "axes[0].axvline(df['study_hours_per_week'].median(), color='black', linestyle='-', linewidth=2, label='Median (17.0)')\n",
    "axes[0].set_title(\"Right-Skewed (Positive): Study Hours\")\n",
    "axes[0].legend()\n",
    "\n",
    "# 2. Left Skewed\n",
    "sns.histplot(df['attendance_rate'], kde=True, ax=axes[1], color='coral')\n",
    "axes[1].axvline(df['attendance_rate'].mean(), color='red', linestyle='--', linewidth=2, label='Mean (77.8)')\n",
    "axes[1].axvline(df['attendance_rate'].median(), color='black', linestyle='-', linewidth=2, label='Median (79.6)')\n",
    "axes[1].set_title(\"Left-Skewed (Negative): Attendance Rate\")\n",
    "axes[1].legend()\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**👀 What to point at on screen:**\n",
    "- Show the red dashed line (mean) vs black solid line (median).\n",
    "- Explain: *\"The mean is always pulled toward the tail! That's why the mean is called an 'outlier magnet'.\"*"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## Part 4: Percentiles, Quartiles & Outlier Detection (Tukey's 1.5 $\\times$ IQR Rule)\n",
    "\n",
    "**🗣️ What to say:**  \n",
    "- $Q_1$ = 25th percentile (25% of students scored below this).\n",
    "- $Q_3$ = 75th percentile (75% of students scored below this).\n",
    "- **IQR (Interquartile Range)** = $Q_3 - Q_1$ (The spread of the middle 50%).\n",
    "- **Tukey's Rule**: Anything beyond $1.5 \\times \\text{IQR}$ outside the box is statistically an outlier!"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Example: Outliers in study_hours_per_week\n",
    "q1_study = df['study_hours_per_week'].quantile(0.25)\n",
    "q3_study = df['study_hours_per_week'].quantile(0.75)\n",
    "iqr_study = q3_study - q1_study\n",
    "\n",
    "lower_study = q1_study - 1.5 * iqr_study\n",
    "upper_study = q3_study + 1.5 * iqr_study\n",
    "\n",
    "print(f\"Q1: {q1_study:.2f} hrs | Q3: {q3_study:.2f} hrs | IQR: {iqr_study:.2f} hrs\")\n",
    "print(f\"Lower Fence: {lower_study:.2f} hrs (any student below this is low outlier)\")\n",
    "print(f\"Upper Fence: {upper_study:.2f} hrs (any student above this is high outlier)\")\n",
    "\n",
    "# Filter outlier students\n",
    "study_outliers = df[(df['study_hours_per_week'] < lower_study) | (df['study_hours_per_week'] > upper_study)]\n",
    "print(f\"\\nNumber of study hour outliers: {len(study_outliers)}\")\n",
    "study_outliers[['student_id', 'study_hours_per_week', 'final_exam_score']]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Visualizing with a Boxplot\n",
    "plt.figure(figsize=(9, 3))\n",
    "sns.boxplot(x=df['study_hours_per_week'], color='skyblue', flierprops=dict(marker='o', markersize=8, markerfacecolor='crimson'))\n",
    "plt.title(\"Boxplot of Study Hours per Week (Red Dots = Outliers)\")\n",
    "plt.xlabel(\"Hours per Week\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 🧪 In-Class Exercise 2 (Give students 7 minutes)\n",
    "**Prompt for students:**\n",
    "> *\"Now find the outliers in `attendance_rate`. Compute Q1, Q3, IQR, and find any students below the lower bound. Who are these students?\"*"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# ✅ SOLUTION TO EXERCISE 2:\n",
    "q1_att = df['attendance_rate'].quantile(0.25)\n",
    "q3_att = df['attendance_rate'].quantile(0.75)\n",
    "iqr_att = q3_att - q1_att\n",
    "\n",
    "lower_att = q1_att - 1.5 * iqr_att\n",
    "upper_att = q3_att + 1.5 * iqr_att\n",
    "\n",
    "att_outliers = df[df['attendance_rate'] < lower_att]\n",
    "print(f\"Attendance Q1: {q1_att:.2f}%, Q3: {q3_att:.2f}%, IQR: {iqr_att:.2f}%\")\n",
    "print(f\"Lower Bound cutoff: {lower_att:.2f}%\")\n",
    "print(f\"Found {len(att_outliers)} attendance outliers:\")\n",
    "att_outliers[['student_id', 'attendance_rate', 'final_exam_score', 'study_hours_per_week']]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**🗣️ Question for the class:**  \n",
    "*\"Should we delete these 7 students from our dataset?\"*  \n",
    "**Answer:** *\"No! These are real students who attended < 47% of classes. An academic advisor needs to identify them, not pretend they don't exist!\"*"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## Part 5: Comparative Statistics with `groupby()` + `agg()`\n",
    "\n",
    "**🗣️ What to say:**  \n",
    "*\"Summary stats for the whole class are helpful, but what if we want to compare different groups? For instance: Do students who study in groups perform better than solo students? `groupby()` + `agg()` is the ultimate tool for this.\"*"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Compare final_exam_score between students in a study group vs not\n",
    "group_comparison = df.groupby('study_group')['final_exam_score'].agg([\n",
    "    'count',\n",
    "    'mean',\n",
    "    'median',\n",
    "    'std'\n",
    "]).round(2)\n",
    "\n",
    "group_comparison"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 🧪 In-Class Exercise 3 (Give students 5 minutes)\n",
    "**Prompt for students:**\n",
    "> *\"Group by `prep_course` (Completed vs None) and find the mean and median for BOTH `study_hours_per_week` and `final_exam_score`.\"*"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# ✅ SOLUTION TO EXERCISE 3:\n",
    "prep_comparison = df.groupby('prep_course').agg(\n",
    "    count=('student_id', 'count'),\n",
    "    mean_hours=('study_hours_per_week', 'mean'),\n",
    "    median_hours=('study_hours_per_week', 'median'),\n",
    "    mean_score=('final_exam_score', 'mean'),\n",
    "    median_score=('final_exam_score', 'median')\n",
    ").round(2)\n",
    "\n",
    "prep_comparison"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "**🗣️ Discussion to highlight:**  \n",
    "*\"Notice: Students who completed the prep course have an average final score of ~78.7 vs ~73.4 for those who did not, even though both groups studied about the same number of hours (~18 hrs)! The prep course actually helped efficiency!\"*"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## Part 6: Relationships - Covariance & Correlation\n",
    "\n",
    "**🗣️ What to say:**  \n",
    "- **Covariance**: Measures if two variables increase together ($+$) or opposite ($-$). But its value is hard to interpret because it depends on the units ($hours \\times points$).\n",
    "- **Pearson Correlation ($r$)**: Standardized covariance! It always sits strictly between $-1.0$ and $+1.0$.\n",
    "  - $+1.0$: Perfect positive line\n",
    "  - $0.0$: No linear relationship\n",
    "  - $-1.0$: Perfect negative line"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Covariance vs Correlation between study hours and final score\n",
    "cov_val = df['study_hours_per_week'].cov(df['final_exam_score'])\n",
    "corr_val = df['study_hours_per_week'].corr(df['final_exam_score'])\n",
    "\n",
    "print(f\"Covariance:  {cov_val:.2f}  (Units: hours * points - hard to interpret)\")\n",
    "print(f\"Correlation: {corr_val:.2f}  (Scale-independent between -1 and +1 - easy to interpret!)\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Correlation Heatmap across all numerical features\n",
    "numeric_df = df.select_dtypes(include=np.number)\n",
    "corr_matrix = numeric_df.corr().round(2)\n",
    "\n",
    "plt.figure(figsize=(8, 6))\n",
    "sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt=\".2f\", linewidths=0.5)\n",
    "plt.title(\"Correlation Matrix Heatmap\")\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 🧪 Final In-Class Challenge (7 minutes)\n",
    "**Prompt for students:**\n",
    "> *\"Look at the correlation heatmap:\n",
    "> 1. Which variable has the strongest correlation with final exam score?\n",
    "> 2. What is the correlation between `sleep_hours` and `final_exam_score`?\n",
    "> 3. Why does correlation NOT mean causation?\"*"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# ✅ SOLUTION TO FINAL CHALLENGE:\n",
    "print(\"Correlations with final_exam_score (highest to lowest):\")\n",
    "print(corr_matrix['final_exam_score'].sort_values(ascending=False))\n",
    "\n",
    "# 🗣️ What to conclude the class with:\n",
    "# 1. Past exam score (0.55) and study hours (0.48) are the biggest drivers.\n",
    "# 2. Sleep hours has correlation near 0 (-0.03). Sleeping 10 hours won't magically pass the exam!\n",
    "# 3. Correlation != Causation: Just because study hours correlates with score doesn't mean \n",
    "#    staring at a book for 50 hours guarantees an A. Quality of study and prior knowledge matter!"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## 🎓 Class Summary (Last 5 minutes on the whiteboard)\n",
    "1. **`describe()`**: Your first snapshot of any new dataset.\n",
    "2. **Mean vs Median**: Mean follows the tail; Median represents the middle.\n",
    "3. **IQR**: Robust measure of spread; foundation for Tukey's outlier detection.\n",
    "4. **`groupby().agg()`**: The tool for comparing subgroups.\n",
    "5. **Correlation**: Tells you how strongly two features move together, but beware of causation assumptions!"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

with open("statistical_functions_eda_class_solutions.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=1)

print("Created statistical_functions_eda_class_solutions.ipynb successfully!")
