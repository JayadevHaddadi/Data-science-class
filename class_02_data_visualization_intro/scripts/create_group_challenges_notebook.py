import json

notebook = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 🏆 The Data Science Boardroom Challenge: Group Analytical Missions\n",
    "**Course**: Data Science Class | **Session**: Data Visualization & Chart Selection  \n",
    "**Format**: 15-minute group working sprint + 60-second Executive Pitch per team  \n",
    "\n",
    "---\n",
    "\n",
    "### 🎯 The Ground Rules\n",
    "1. **Code is cheap, insight is expensive.** Anyone can ask AI to generate a plot in 3 seconds. Your team's score is based on **how well you interpret the chart** and **the business action you propose**.\n",
    "2. Each group has a unique **Stakeholder Persona** and a specific **Decision Problem**.\n",
    "3. Use the starter code provided under your group's mission. Customize labels, colors, annotations, or thresholds.\n",
    "4. Prepare a **60-Second Executive Pitch** answering:\n",
    "   - *Why did you pick this visualization over others?*\n",
    "   - *What hidden pattern did you discover?*\n",
    "   - *What is the #1 concrete recommendation you propose to leadership?*"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 0. Shared Setup & Datasets"
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
    "# Set clean styling\n",
    "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n",
    "plt.rcParams['font.sans-serif'] = 'DejaVu Sans'\n",
    "plt.rcParams['figure.dpi'] = 110\n",
    "\n",
    "# Load both shared datasets\n",
    "df_students = pd.read_csv('datasets/student_demographics_performance.csv')\n",
    "df_weekly = pd.read_csv('datasets/student_weekly_trends.csv')\n",
    "\n",
    "print(f\"Loaded df_students: {df_students.shape[0]} students\")\n",
    "print(f\"Loaded df_weekly:   {df_weekly.shape[0]} semester weeks\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## 🚨 MISSION 1: The \"At-Risk Early Warning\" Taskforce\n",
    "**Your Stakeholder**: The University Academic Dean & Provost.  \n",
    "**The Problem**: The Dean wants an automated alert for students heading for a **'D' or 'F' grade**. At what specific threshold of weekly study hours or attendance do student grades collapse? Where is the \"danger zone\"?\n",
    "\n",
    "**Your Team's Questions to Answer in 60s**:\n",
    "1. Is low attendance or low study hours the bigger driver of failing grades?\n",
    "2. At what exact cutoff (e.g. `< X` hours or `< Y%` attendance) should the university trigger mandatory tutoring?\n",
    "3. Defend why you chose this chart type over a simple table of averages."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# =========================================================================\n",
    "# MISSION 1 STARTER CODE (Customize thresholds, styling, or annotations)\n",
    "# =========================================================================\n",
    "fig, ax = plt.subplots(figsize=(9, 5))\n",
    "\n",
    "# Scatter plot colored by grade category\n",
    "sns.scatterplot(\n",
    "    data=df_students,\n",
    "    x='study_hours_weekly',\n",
    "    y='final_score',\n",
    "    hue='grade',\n",
    "    hue_order=['A', 'B', 'C', 'D', 'F'],\n",
    "    palette={'A': '#2ca02c', 'B': '#1f77b4', 'C': '#ff7f0e', 'D': '#d62728', 'F': '#8c564b'},\n",
    "    s=65,\n",
    "    alpha=0.85,\n",
    "    ax=ax\n",
    ")\n",
    "\n",
    "# TODO: Group 1 - Adjust this vertical danger threshold and analyze what falls to the left!\n",
    "danger_hours_threshold = 15.0\n",
    "ax.axvline(danger_hours_threshold, color='crimson', linestyle='--', linewidth=2, label=f'Proposed Danger Line ({danger_hours_threshold}h)')\n",
    "ax.axhline(60, color='gray', linestyle=':', label='Passing Boundary (60 pts)')\n",
    "\n",
    "ax.set_title('Academic Dean Briefing: Identifying the Failing Grade Danger Zone', fontweight='bold', fontsize=13)\n",
    "ax.set_xlabel('Weekly Study Hours', fontweight='semibold')\n",
    "ax.set_ylabel('Final Exam Score', fontweight='semibold')\n",
    "ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## 🧠 MISSION 2: The \"Burnout & Mental Health\" Taskforce\n",
    "**Your Stakeholder**: The Director of Campus Counseling & Student Wellbeing.  \n",
    "**The Problem**: The counseling center wants to schedule wellness workshops before students reach breaking points. Using `df_weekly`, identify the exact week when stress peaks. Does heavy studying cause stress, or does intense cramming trigger right before exams?\n",
    "\n",
    "**Your Team's Questions to Answer in 60s**:\n",
    "1. Which week experiences the sharpest surge in reported stress levels?\n",
    "2. What happened to study hours immediately after Week 6 midterms? (Look at Week 7).\n",
    "3. In which week must the university launch stress-management interventions?"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# =========================================================================\n",
    "# MISSION 2 STARTER CODE (Customize shaded regions, twin axis, or lines)\n",
    "# =========================================================================\n",
    "fig, ax1 = plt.subplots(figsize=(10, 5))\n",
    "\n",
    "# Primary Axis: Study Hours & Quiz Scores\n",
    "ax1.plot(df_weekly['week'], df_weekly['study_hours_datascience'], marker='o', color='#1f77b4', linewidth=2.5, label='DS Study Hours')\n",
    "ax1.plot(df_weekly['week'], df_weekly['avg_quiz_score'], marker='s', color='#2ca02c', linewidth=2, linestyle='-.', label='Avg Quiz Score')\n",
    "ax1.set_xlabel('Semester Week', fontweight='bold', fontsize=11)\n",
    "ax1.set_ylabel('Study Hours / Score', color='#1f77b4', fontweight='bold', fontsize=11)\n",
    "ax1.set_xticks(df_weekly['week'])\n",
    "\n",
    "# Secondary Axis: Stress Level (1 to 10)\n",
    "ax2 = ax1.twinx()\n",
    "ax2.plot(df_weekly['week'], df_weekly['stress_level'], marker='^', color='#d62728', linewidth=2.5, label='Reported Stress Level (1-10)')\n",
    "ax2.set_ylabel('Stress Level (1-10)', color='#d62728', fontweight='bold', fontsize=11)\n",
    "ax2.set_ylim(1, 10)\n",
    "\n",
    "# TODO: Group 2 - Add a shaded span or annotation to highlight the critical intervention window!\n",
    "# ax1.axvspan(5.5, 7.5, color='gold', alpha=0.25, label='Crisis Window')\n",
    "\n",
    "ax1.set_title('Wellbeing Briefing: 12-Week Stress Surge vs. Study Trajectory', fontweight='bold', fontsize=13)\n",
    "ax1.legend(loc='upper left')\n",
    "ax2.legend(loc='upper right')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## ⚖️ MISSION 3: The \"Curriculum & Major Equity\" Audit\n",
    "**Your Stakeholder**: The Head of Engineering & Science Curriculum.  \n",
    "**The Problem**: Mechanical and Electrical Engineering students claim that Computer Science and Data Science courses are graded much easier. Investigate whether differences in final exam scores reflect unfair grading or simply differences in weekly study hours.\n",
    "\n",
    "**Your Team's Questions to Answer in 60s**:\n",
    "1. Does Computer Science really achieve significantly higher scores than Mechanical Engineering?\n",
    "2. When you compare study hours across majors, does the higher score make sense?\n",
    "3. **Ethical Trap**: Did your chart start the Y-axis at 0? What happens if you truncate the axis to start at 70?"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# =========================================================================\n",
    "# MISSION 3 STARTER CODE (Compare scores and study hours across majors)\n",
    "# =========================================================================\n",
    "major_comparison = df_students.groupby('major').agg(\n",
    "    avg_score=('final_score', 'mean'),\n",
    "    avg_study_hours=('study_hours_weekly', 'mean'),\n",
    "    count=('student_id', 'count')\n",
    ").reset_index()\n",
    "\n",
    "fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))\n",
    "\n",
    "# 1. Average Final Score by Major (Horizontal Bar)\n",
    "axes[0].barh(major_comparison['major'], major_comparison['avg_score'], color='#3182bd', edgecolor='black', alpha=0.85)\n",
    "axes[0].set_title('Average Final Score by Major', fontweight='bold')\n",
    "axes[0].set_xlabel('Score (0 - 100)')\n",
    "axes[0].set_xlim(0, 100)  # Always start at 0!\n",
    "\n",
    "# 2. Average Weekly Study Hours by Major\n",
    "axes[1].barh(major_comparison['major'], major_comparison['avg_study_hours'], color='#31a354', edgecolor='black', alpha=0.85)\n",
    "axes[1].set_title('Average Weekly Study Hours by Major', fontweight='bold')\n",
    "axes[1].set_xlabel('Study Hours per Week')\n",
    "axes[1].set_xlim(0, 30)\n",
    "\n",
    "# TODO: Group 3 - Add text value labels inside or beside the bars!\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## 🚌 MISSION 4: The \"Commuter Reality Check\" Taskforce\n",
    "**Your Stakeholder**: The Director of Campus Housing & Commuter Student Services.  \n",
    "**The Problem**: Commuter students claim long travel times ruin their academic success. What do students actually sacrifice when their commute is long: sleep, leisure, or self-study? Does long commute directly tank grades?\n",
    "\n",
    "**Your Team's Questions to Answer in 60s**:\n",
    "1. As `daily_commute_hrs` increases, which activity drops fastest: `daily_sleep_hrs` or `daily_study_hrs`?\n",
    "2. How strong is the correlation between commute time and final exam score?\n",
    "3. Defend why a **Stacked Bar Chart** or **Scatter Plot** is far superior to a 5-slice Pie Chart for this analysis."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# =========================================================================\n",
    "# MISSION 4 STARTER CODE (Explore commute impact on sleep and score)\n",
    "# =========================================================================\n",
    "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
    "\n",
    "# 1. Commute vs Sleep with Trendline\n",
    "sns.scatterplot(data=df_students, x='daily_commute_hrs', y='daily_sleep_hrs', color='#2b83ba', s=60, alpha=0.8, ax=axes[0])\n",
    "sns.regplot(data=df_students, x='daily_commute_hrs', y='daily_sleep_hrs', scatter=False, color='darkred', ax=axes[0])\n",
    "axes[0].set_title('Impact of Commute on Sleep Duration', fontweight='bold')\n",
    "axes[0].set_xlabel('Daily Commute (Hours)')\n",
    "axes[0].set_ylabel('Daily Sleep (Hours)')\n",
    "\n",
    "# 2. Daily 24-Hour Time Allocation by Commute Bracket (Short vs Long Commute)\n",
    "df_students['commute_bracket'] = pd.cut(df_students['daily_commute_hrs'], bins=[0, 1.5, 4.0], labels=['Short Commute (<=1.5h)', 'Long Commute (>1.5h)'])\n",
    "bracket_time = df_students.groupby('commute_bracket', observed=False)[['daily_sleep_hrs', 'daily_classes_hrs', 'daily_study_hrs', 'daily_leisure_hrs', 'daily_commute_hrs']].mean()\n",
    "\n",
    "bracket_time.plot(kind='barh', stacked=True, colormap='Spectral', edgecolor='white', ax=axes[1])\n",
    "axes[1].set_title('24-Hour Time Budget: Short vs. Long Commuters', fontweight='bold')\n",
    "axes[1].set_xlabel('Total Daily Hours (24h)')\n",
    "axes[1].set_xlim(0, 24)\n",
    "axes[1].legend(bbox_to_anchor=(1.02, 1), loc='upper left')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "---\n",
    "## 🗺️ MISSION 5: The \"Regional Talent & Admissions\" Board\n",
    "**Your Stakeholder**: The University Admissions & Scholarship Board.  \n",
    "**The Problem**: The university wants to allocate regional diversity scholarships. Are students from distant states (`Delhi`, `Maharashtra`) performing as well as local students (`Karnataka`, `Kerala`)? Where should admissions focus recruitment?\n",
    "\n",
    "**Your Team's Questions to Answer in 60s**:\n",
    "1. Which state region has the highest average final score?\n",
    "2. Which state region has the lowest student enrollment count (potential untapped talent)?\n",
    "3. **Analytical Trap**: Why is it dangerous to compare states using only the average score without showing the student count ($n$)?"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# =========================================================================\n",
    "# MISSION 5 STARTER CODE (Lollipop / Bubble Chart showing score + sample size)\n",
    "# =========================================================================\n",
    "state_summary = df_students.groupby('state_region').agg(\n",
    "    student_count=('student_id', 'count'),\n",
    "    avg_score=('final_score', 'mean'),\n",
    "    median_score=('final_score', 'median')\n",
    ").reset_index().sort_values(by='avg_score', ascending=True)\n",
    "\n",
    "fig, ax = plt.subplots(figsize=(9, 4.5))\n",
    "\n",
    "# Horizontal lollipop stems\n",
    "ax.hlines(y=state_summary['state_region'], xmin=65, xmax=state_summary['avg_score'], color='#2b83ba', linewidth=3, alpha=0.6)\n",
    "\n",
    "# Bubble dots sized by student count\n",
    "scatter = ax.scatter(\n",
    "    state_summary['avg_score'], \n",
    "    state_summary['state_region'], \n",
    "    s=state_summary['student_count'] * 12,  # Bubble size = enrollment volume\n",
    "    c=state_summary['avg_score'], \n",
    "    cmap='coolwarm', \n",
    "    edgecolors='black',\n",
    "    linewidth=1.5,\n",
    "    zorder=3\n",
    ")\n",
    "\n",
    "# Add data label with both mean score and sample size (n)\n",
    "for _, row in state_summary.iterrows():\n",
    "    ax.text(row['avg_score'] + 0.6, row['state_region'], f\"{row['avg_score']:.1f} pts (n={row['student_count']})\", va='center', fontweight='bold')\n",
    "\n",
    "ax.set_xlim(65, 88)\n",
    "ax.set_title('Admissions Board Briefing: State Performance vs. Enrollment Volume', fontweight='bold', fontsize=13)\n",
    "ax.set_xlabel('Average Final Exam Score', fontweight='semibold')\n",
    "ax.set_ylabel('State Region', fontweight='semibold')\n",
    "plt.colorbar(scatter, label='Average Score')\n",
    "\n",
    "plt.tight_layout()\n",
    "plt.show()"
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

with open("class_02_data_visualization_intro/data_visualization_group_challenges.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=1)

print("Created data_visualization_group_challenges.ipynb successfully!")
