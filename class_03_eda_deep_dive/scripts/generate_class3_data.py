"""Generate the Class 03 'Campus Wellbeing Survey' datasets.

Outputs (in ../datasets/):
  campus_survey_raw.csv    - messy file students clean in the Data Detective task
  campus_survey_clean.csv  - cleaned version used for the live class and team missions

The data is synthetic, with deliberately planted patterns:

  * Simpson's paradox      study hours vs exam score is NEGATIVE overall but POSITIVE inside every program
  * Non-linear relation    stress vs exam score is an inverted U (Pearson r ~ 0)
  * Threshold effects      sleep < 6h and part-time job > 15h/week (now >15h/week) both hurt scores
  * Bimodal distribution   part-time job hours (many zeros + a cluster around 14h)
  * Skewed distribution    commute minutes
  * Confounding            coffee has NO effect on score, but looks harmful overall (Engineering drinks most)
  * Missing-not-at-random  sleep is missing more often for students with long job hours
  * Real outliers          a few genuine extreme students that must NOT be deleted
  * Data-entry errors      duplicates, label variants, impossible values, sentinel codes (999)
"""
import os

import numpy as np
import pandas as pd

rng = np.random.default_rng(303)
N = 520

PROGRAMS = ["Engineering", "Data Science", "Business", "Design"]
P_PROB = [0.28, 0.24, 0.30, 0.18]
STUDY_MEAN = {"Engineering": 26, "Data Science": 20, "Business": 14, "Design": 9}
BASE_SCORE = {"Engineering": 56, "Data Science": 64, "Business": 73, "Design": 80}
COFFEE_BUMP = {"Engineering": 1.6, "Data Science": 1.0, "Business": 0.3, "Design": 0.0}
WITHIN_SLOPE = 0.7  # exam points per extra study hour, inside a program

program = rng.choice(PROGRAMS, size=N, p=P_PROB)
year = rng.integers(1, 5, size=N)
age = 17 + year + rng.integers(0, 2, size=N)

residence = rng.choice(["Hostel", "Home", "Commuter"], size=N, p=[0.45, 0.25, 0.30])
commute_scale = {"Hostel": 12, "Home": 30, "Commuter": 70}
commute = np.array([rng.lognormal(np.log(commute_scale[r]), 0.45) for r in residence]).round(0)

study = np.array([rng.normal(STUDY_MEAN[p], 4.5) for p in program]).clip(1, 45).round(1)

has_job = rng.random(N) < 0.45
job = np.where(has_job, rng.normal(15, 6, size=N).clip(4, 32), 0).round(0)

sleep = (rng.normal(7.1, 0.85, size=N) - 0.5 * (residence == "Commuter") - 0.035 * job).clip(3.5, 9.5).round(1)

stress = (5.5 + 0.03 * (study - 16) + 0.03 * job + 0.25 * (7 - sleep) + rng.normal(0, 2.0, size=N)).clip(1, 10).round(1)
social = (2.6 + 0.35 * (stress - 5) + rng.normal(0, 1.0, size=N)).clip(0.3, 9).round(1)

coffee = np.array([
    rng.poisson(max(0.1, 1.0 + COFFEE_BUMP[p] + 0.12 * (7 - s) + 0.06 * (st - 5)))
    for p, s, st in zip(program, sleep, stress)
]).clip(0, 12)

# ---- exam score model ----
stress_effect = -1.2 * (stress - 5.5) ** 2
stress_effect -= stress_effect.mean()
sleep_pen = -5.0 * np.clip(6 - sleep, 0, None)
job_pen = -1.5 * np.clip(job - 15, 0, None)
base = np.array([BASE_SCORE[p] for p in program], dtype=float)
study_dev = study - np.array([STUDY_MEAN[p] for p in program])
exam = (base + WITHIN_SLOPE * study_dev + sleep_pen + job_pen + stress_effect
        + rng.normal(0, 3.5, size=N)).clip(20, 100).round(1)

df = pd.DataFrame({
    "student_id": [f"CS-{i:04d}" for i in range(1, N + 1)],
    "program": program, "year": year, "age": age, "residence": residence,
    "study_hours_week": study, "sleep_hours": sleep, "caffeine_cups_day": coffee,
    "social_media_hours_day": social, "part_time_job_hours_week": job,
    "commute_minutes": commute, "stress_score": stress, "exam_score": exam,
})

# ---- genuine outliers (REAL signal - keep them!) ----
grinders = df[df.program.isin(["Engineering", "Data Science"])].sample(3, random_state=1).index
for idx, hrs in zip(grinders, [58.0, 61.0, 55.0]):
    df.loc[idx, ["study_hours_week", "stress_score", "exam_score"]] = [hrs, 9.6, round(float(rng.normal(70, 3)), 1)]
genius = df[df.program == "Design"].sample(1, random_state=2).index[0]
df.loc[genius, ["study_hours_week", "exam_score", "stress_score"]] = [2.0, 96.5, 3.0]
real_outlier_ids = list(df.loc[list(grinders) + [genius], "student_id"])

clean = df.copy()

# ---- raw-file mess ----
raw = df.copy()

labels = {
    "Engineering": ["engineering", "ENGINEERING", " Engineering", "Eng."],
    "Data Science": ["data science", "DS", "Data Sci", "Data Science "],
    "Business": ["business", "Biz", "BUSINESS "],
    "Design": ["design", "Design "],
}
variant_rows = raw.sample(frac=0.14, random_state=3).index
for i in variant_rows:
    raw.loc[i, "program"] = rng.choice(labels[raw.loc[i, "program"]])

# impossible values / sentinels (chosen from rows that are not the real outliers)
safe = raw[~raw.student_id.isin(real_outlier_ids)].sample(9, random_state=4).index.tolist()
raw.loc[safe[0], "age"] = 250
raw.loc[safe[1], "age"] = 199
raw.loc[safe[2], "age"] = 5
raw.loc[safe[3], "study_hours_week"] = 168
raw.loc[safe[4], "study_hours_week"] = 999
raw.loc[safe[5], "sleep_hours"] = -7.5
raw.loc[safe[6], "sleep_hours"] = 25
raw.loc[safe[7], "exam_score"] = 105
raw.loc[safe[8], "exam_score"] = 999

# missing sleep depends on job hours (missing NOT at random); stress missing is random
p_missing = 0.03 + 0.012 * raw["part_time_job_hours_week"]
raw.loc[rng.random(N) < p_missing, "sleep_hours"] = np.nan
raw.loc[rng.random(N) < 0.03, "stress_score"] = np.nan

# 10 exact duplicate rows scattered through the file
dupes = raw.sample(10, random_state=5)
raw = pd.concat([raw, dupes]).sample(frac=1, random_state=6).reset_index(drop=True)

# ---- the clean file = what a careful analyst would produce from raw ----
c = raw.drop_duplicates().copy()
canon = {k.lower().strip(): k for k in PROGRAMS}
alias = {"eng.": "Engineering", "ds": "Data Science", "data sci": "Data Science", "biz": "Business"}
c["program"] = c["program"].str.strip().str.lower().map(lambda s: alias.get(s, canon.get(s)))
c.loc[(c.age < 15) | (c.age > 60), "age"] = np.nan
c.loc[(c.study_hours_week > 100), "study_hours_week"] = np.nan
c.loc[(c.sleep_hours <= 0) | (c.sleep_hours > 14), "sleep_hours"] = np.nan
c.loc[(c.exam_score > 100), "exam_score"] = np.nan
c = c.sort_values("student_id").reset_index(drop=True)

out = os.path.join(os.path.dirname(__file__), "..", "datasets")
raw.to_csv(os.path.join(out, "campus_survey_raw.csv"), index=False)
c.to_csv(os.path.join(out, "campus_survey_clean.csv"), index=False)
print("raw:", raw.shape, "clean:", c.shape)
print("real outlier ids:", real_outlier_ids)
