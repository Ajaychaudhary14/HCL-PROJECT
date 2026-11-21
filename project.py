import pandas as pd
import numpy as np

# Read the original CSV file
df = pd.read_csv("college_student_management_data.csv")

# 1. Clean column names
df.columns = df.columns.str.strip()

# 2. Clean student IDs
df["student_id"] = df["student_id"].astype("string").str.strip()

df = df.dropna(subset=["student_id"])
df = df[df["student_id"] != ""]

# Remove duplicate student IDs
df = df.drop_duplicates(subset=["student_id"], keep="first")

# 3. Define valid ranges for numeric columns
numeric_ranges = {
    "age": (16, 100),
    "GPA": (0, 4),
    "course_load": (0, 10),
    "avg_course_grade": (0, 100),
    "attendance_rate": (0, 1),
    "lms_logins_past_month": (0, 1000),
    "avg_session_duration_minutes": (0, 1440),
    "assignment_submission_rate": (0, 1),
    "forum_participation_count": (0, 1000),
    "video_completion_rate": (0, 1)
}

# 4. Convert numeric columns and handle invalid values
for column, (minimum, maximum) in numeric_ranges.items():

    df[column] = pd.to_numeric(
        df[column], errors="coerce"
    )

    # Replace out-of-range values with missing values
    invalid = ~df[column].between(minimum, maximum)
    df.loc[invalid, column] = np.nan

    # Fill missing values using median
    df[column] = df[column].fillna(
        df[column].median()
    )

# 5. Convert whole-number columns to integers
integer_columns = [
    "age",
    "course_load",
    "lms_logins_past_month",
    "avg_session_duration_minutes",
    "forum_participation_count"
]

for column in integer_columns:
    df[column] = df[column].round().astype(int)

# 6. Clean categorical/text columns
text_columns = [
    "gender",
    "major",
    "enrollment_status",
    "risk_level"
]

for column in text_columns:
    df[column] = (
        df[column]
        .astype("string")
        .str.strip()
    )

# Standardize text formatting
df["gender"] = df["gender"].str.title()
df["major"] = df["major"].str.title()
df["enrollment_status"] = df["enrollment_status"].str.title()
df["risk_level"] = df["risk_level"].str.title()

# 7. Remove remaining duplicate rows
df = df.drop_duplicates()

# 8. Reset index
df = df.reset_index(drop=True)

# 9. Save cleaned CSV file
df.to_csv(
    "cleaned_college_student_management_data.csv",
    index=False
)

# 10. Display cleaning results
print("Data Cleaning Completed Successfully!")

print("Total rows:", len(df))
print("Total columns:", len(df.columns))

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

print("\nCleaned data preview:")
print(df.head())

print("\nCleaned CSV file saved successfully!")

