import numpy as np
import pandas as pd

np.random.seed(101)

# ==========================================
# DATASET 1: student_weekly_trends.csv (Time Trends / Line Charts)
# ==========================================
weeks = np.arange(1, 13)
# Base study hours by subject across 12 weeks
# Week 1-5 steady rise, Week 6-7 Midterms/break dip, Week 8-10 steady, Week 11-12 Pre-finals cramming spike!
study_ds = np.array([12, 14, 16, 17, 18, 14, 11, 16, 19, 21, 28, 30]) + np.random.normal(0, 0.8, 12)
study_math = np.array([10, 11, 12, 14, 15, 12, 9, 13, 15, 17, 24, 25]) + np.random.normal(0, 0.7, 12)
study_cs = np.array([14, 15, 17, 19, 20, 16, 12, 18, 22, 23, 31, 33]) + np.random.normal(0, 0.9, 12)

avg_quiz = np.array([72, 74, 76, 75, 78, 68, 65, 76, 79, 81, 85, 87]) + np.random.normal(0, 1.0, 12)
stress_level = np.array([3.2, 3.8, 4.5, 5.0, 5.8, 7.5, 4.0, 5.2, 6.1, 7.0, 8.9, 9.4]).round(1)

df_weekly = pd.DataFrame({
    "week": weeks,
    "study_hours_datascience": study_ds.round(1),
    "study_hours_math": study_math.round(1),
    "study_hours_cs": study_cs.round(1),
    "avg_quiz_score": avg_quiz.round(1),
    "stress_level": stress_level
})
df_weekly.to_csv("class_02_data_visualization_intro/datasets/student_weekly_trends.csv", index=False)
print("Saved student_weekly_trends.csv:", df_weekly.shape)

# ==========================================
# DATASET 2: student_demographics_performance.csv (Distribution, Comparison, Relationship, Composition, Correlation, Multi-variable, Geo)
# ==========================================
n = 250
student_ids = [f"STU_{2001 + i}" for i in range(n)]

majors = np.random.choice(
    ["Computer Science", "Data Science", "Electrical Eng", "Mechanical Eng", "Business Analytics"],
    size=n, p=[0.30, 0.25, 0.18, 0.15, 0.12]
)

genders = np.random.choice(["Female", "Male", "Other/Prefer not to say"], size=n, p=[0.46, 0.50, 0.04])

# Study hours: Bimodal mixture! Peak at 12 hrs (casual) and peak at 25 hrs (dedicated)
# This makes the histogram vs boxplot discussion mind-blowing!
cluster = np.random.choice([1, 2], size=n, p=[0.45, 0.55])
study_hours = np.where(
    cluster == 1,
    np.random.normal(12.0, 2.5, size=n),
    np.random.normal(25.0, 4.0, size=n)
).round(1)
study_hours = np.clip(study_hours, 5.0, 45.0)

attendance = np.random.beta(a=6, b=2, size=n) * 100
attendance = np.clip(attendance.round(1), 40.0, 99.0)

# Midterm and Final scores (with correlation, plus a few interesting outliers)
midterm = (45 + 0.5 * study_hours + 0.3 * attendance + np.random.normal(0, 6, size=n)).round(1)
midterm = np.clip(midterm, 35.0, 98.0)

final_score = (38 + 0.55 * study_hours + 0.35 * midterm + np.random.normal(0, 5, size=n)).round(1)
final_score = np.clip(final_score, 30.0, 100.0)

# Grades based on final score
def assign_grade(s):
    if s >= 85: return "A"
    elif s >= 75: return "B"
    elif s >= 65: return "C"
    elif s >= 50: return "D"
    else: return "F"

grades = [assign_grade(s) for s in final_score]

# 24-hour Daily Time Composition (Sleep, Classes, Study, Leisure, Commute)
sleep = np.random.normal(7.0, 0.9, size=n).round(1)
classes = np.random.normal(5.5, 0.5, size=n).round(1)
daily_study = (study_hours / 7.0).round(1)
commute = np.random.normal(1.8, 0.6, size=n).round(1)
leisure = np.maximum(1.0, 24.0 - (sleep + classes + daily_study + commute)).round(1)

# Geographic State Regions
states = np.random.choice(
    ["Karnataka", "Kerala", "Tamil Nadu", "Maharashtra", "Delhi"],
    size=n, p=[0.35, 0.22, 0.20, 0.13, 0.10]
)

df_students = pd.DataFrame({
    "student_id": student_ids,
    "major": majors,
    "gender": genders,
    "state_region": states,
    "study_hours_weekly": study_hours,
    "attendance_rate": attendance,
    "midterm_score": midterm,
    "final_score": final_score,
    "grade": grades,
    "daily_sleep_hrs": sleep,
    "daily_classes_hrs": classes,
    "daily_study_hrs": daily_study,
    "daily_leisure_hrs": leisure,
    "daily_commute_hrs": commute
})

df_students.to_csv("class_02_data_visualization_intro/datasets/student_demographics_performance.csv", index=False)
print("Saved student_demographics_performance.csv:", df_students.shape)
