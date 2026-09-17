import numpy as np
import pandas as pd

np.random.seed(42)
n = 150

student_ids = [f"STU_{1001 + i}" for i in range(n)]

# Study hours per week: right-skewed (log-normal base + noise), mean around 18-20, a few heavy study students
study_hours = np.random.gamma(shape=4.0, scale=4.5, size=n).round(1)
# clamp realistic min
study_hours = np.clip(study_hours, 4.0, 45.0)
# inject 2 clear outliers for IQR demo
study_hours[14] = 52.5  # high outlier
study_hours[88] = 58.0  # extreme outlier

# Attendance rate: left-skewed (beta distribution), most between 75% and 98%
attendance = (np.random.beta(a=7, b=2, size=n) * 100).round(1)
attendance = np.clip(attendance, 45.0, 99.5)
attendance[42] = 32.0  # low outlier
attendance[115] = 28.5 # low outlier

# Assignments completed: discrete integers 0 to 10 with a prominent mode (e.g. 8)
assignment_probs = [0.02, 0.02, 0.03, 0.05, 0.08, 0.10, 0.14, 0.18, 0.26, 0.08, 0.04]
assignments_completed = np.random.choice(range(11), size=n, p=assignment_probs)

# Sleep hours: fairly normal distribution around 7 hours
sleep_hours = np.random.normal(loc=7.1, scale=1.1, size=n).round(1)
sleep_hours = np.clip(sleep_hours, 4.0, 10.0)

# Past exam score: roughly normal 40 to 95
past_score = (50 + 0.35 * study_hours + 0.25 * attendance + np.random.normal(0, 7, size=n)).round(1)
past_score = np.clip(past_score, 35.0, 98.0)

# Study group participation: 55% Yes, 45% No
study_group = np.random.choice(["Yes", "No"], size=n, p=[0.55, 0.45])

# Prep course taken:
prep_course = np.random.choice(["Completed", "None"], size=n, p=[0.40, 0.60])

# Final exam score: correlated with study hours, past score, attendance, and study group bonus
group_bonus = np.where(study_group == "Yes", 4.5, 0.0)
prep_bonus = np.where(prep_course == "Completed", 5.0, 0.0)

final_score = (
    15.0 
    + 0.45 * past_score 
    + 0.40 * study_hours 
    + 0.20 * attendance 
    + group_bonus 
    + prep_bonus 
    + np.random.normal(0, 5.0, size=n)
).round(1)
final_score = np.clip(final_score, 30.0, 100.0)
# Add 1 anomalous score (low outlier due to sudden illness)
final_score[73] = 25.0

df = pd.DataFrame({
    "student_id": student_ids,
    "study_hours_per_week": study_hours,
    "attendance_rate": attendance,
    "past_exam_score": past_score,
    "assignments_completed": assignments_completed,
    "sleep_hours": sleep_hours,
    "study_group": study_group,
    "prep_course": prep_course,
    "final_exam_score": final_score
})

df.to_csv("student_learning_performance_eda_150.csv", index=False)
print("Successfully generated student_learning_performance_eda_150.csv with shape:", df.shape)
print("\nQuick Describe:")
print(df.describe().T[["count", "mean", "std", "min", "50%", "max"]])
