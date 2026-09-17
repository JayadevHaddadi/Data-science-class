"""
INSTRUCTOR ANSWER KEY & VERIFICATION SCRIPT
Covers all exercises and calculations for Session:
Statistical functions in the context of exploratory data analysis.
"""
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv("student_learning_performance_eda_150.csv")

print("="*70)
print("1. OVERVIEW & DESCRIBE()")
print("="*70)
print(df.describe().T[["count", "mean", "std", "min", "25%", "50%", "75%", "max"]])

print("\n" + "="*70)
print("2. MEAN, MEDIAN, MODE, VARIANCE, STD (EXERCISE 1)")
print("="*70)
mean_att = df['attendance_rate'].mean()
median_att = df['attendance_rate'].median()
std_att = df['attendance_rate'].std()
mode_assign = df['assignments_completed'].mode()[0]

print(f"Attendance Rate Mean:   {mean_att:.2f}%")
print(f"Attendance Rate Median: {median_att:.2f}%")
print(f"Attendance Rate Std:    {std_att:.2f}%")
print(f"Mode Assignments Done:  {mode_assign}")
print(f"Observation: Mean ({mean_att:.2f}) < Median ({median_att:.2f}) -> Left-Skewed distribution!")

print("\n" + "="*70)
print("3. SKEWNESS VALUES")
print("="*70)
print(df.select_dtypes(include=np.number).skew().round(3))

print("\n" + "="*70)
print("4. IQR & OUTLIER DETECTION (EXERCISE 2)")
print("="*70)
# Target: attendance_rate
q1 = df['attendance_rate'].quantile(0.25)
q3 = df['attendance_rate'].quantile(0.75)
iqr = q3 - q1
lower_fence = q1 - 1.5 * iqr
upper_fence = q3 + 1.5 * iqr

print(f"Attendance Q1: {q1:.2f}, Q3: {q3:.2f}, IQR: {iqr:.2f}")
print(f"Tukey Fences: Lower = {lower_fence:.2f}, Upper = {upper_fence:.2f}")

outliers = df[(df['attendance_rate'] < lower_fence) | (df['attendance_rate'] > upper_fence)]
print(f"Identified {len(outliers)} attendance outlier(s):")
print(outliers[['student_id', 'attendance_rate', 'study_hours_per_week', 'final_exam_score']])

print("\n" + "="*70)
print("5. GROUPBY + AGG (EXERCISE 3)")
print("="*70)
prep_comparison = df.groupby('prep_course').agg(
    count=('student_id', 'count'),
    mean_hours=('study_hours_per_week', 'mean'),
    median_hours=('study_hours_per_week', 'median'),
    mean_score=('final_exam_score', 'mean'),
    median_score=('final_exam_score', 'median'),
    std_score=('final_exam_score', 'std')
).round(2)
print(prep_comparison)

print("\n" + "="*70)
print("6. COVARIANCE & CORRELATION MATRIX (EXERCISE 4 / CHALLENGE)")
print("="*70)
numeric_df = df.select_dtypes(include=np.number)
corr_matrix = numeric_df.corr().round(2)
print("Correlations with final_exam_score:")
print(corr_matrix['final_exam_score'].sort_values(ascending=False))
print("\nCovariance Matrix sample:")
print(numeric_df[['study_hours_per_week', 'past_exam_score', 'final_exam_score']].cov().round(2))
