import pandas as pd


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names:
    - lowercase
    - strip spaces
    - replace spaces with underscores
    """
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )
    return df


def clean_students(df: pd.DataFrame) -> pd.DataFrame:
    df = standardize_column_names(df)

    if "student_id" in df.columns:
        df["student_id"] = df["student_id"].astype(str).str.strip()

    if "full_name" in df.columns:
        df["full_name"] = df["full_name"].astype(str).str.strip().str.title()

    if "major" in df.columns:
        df["major"] = df["major"].astype(str).str.strip().replace({
            "Comp Sci": "Computer Science",
            "CSE": "Computer Science",
            "Data Sci": "Data Science"
        })

    if "semester" in df.columns:
        df["semester"] = df["semester"].astype(str).str.strip().str.title()

    df = df.drop_duplicates()
    return df


def clean_enrollments(df: pd.DataFrame) -> pd.DataFrame:
    df = standardize_column_names(df)

    if "student_id" in df.columns:
        df["student_id"] = df["student_id"].astype(str).str.strip()

    if "course_id" in df.columns:
        df["course_id"] = df["course_id"].astype(str).str.strip().str.upper()

    if "semester" in df.columns:
        df["semester"] = df["semester"].astype(str).str.strip().str.title()

    if "grade" in df.columns:
        df["grade"] = df["grade"].astype(str).str.strip().str.upper()

    df = df.drop_duplicates()
    return df


def clean_attendance(df: pd.DataFrame) -> pd.DataFrame:
    df = standardize_column_names(df)

    if "student_id" in df.columns:
        df["student_id"] = df["student_id"].astype(str).str.strip()

    if "course_id" in df.columns:
        df["course_id"] = df["course_id"].astype(str).str.strip().str.upper()

    if "attendance_percent" in df.columns:
        df["attendance_percent"] = pd.to_numeric(
            df["attendance_percent"], errors="coerce"
        )

    df = df.drop_duplicates()
    return df


def clean_performance(df: pd.DataFrame) -> pd.DataFrame:
    df = standardize_column_names(df)

    if "student_id" in df.columns:
        df["student_id"] = df["student_id"].astype(str).str.strip()

    if "gpa" in df.columns:
        df["gpa"] = pd.to_numeric(df["gpa"], errors="coerce")

    if "credits_completed" in df.columns:
        df["credits_completed"] = pd.to_numeric(
            df["credits_completed"], errors="coerce"
        )

    df = df.drop_duplicates()
    return df


def clean_data(data: dict) -> dict:
    """
    Clean and standardize all loaded datasets.
    """
    cleaned_data = {}

    if "students" in data:
        cleaned_data["students"] = clean_students(data["students"])

    if "enrollments" in data:
        cleaned_data["enrollments"] = clean_enrollments(data["enrollments"])

    if "attendance" in data:
        cleaned_data["attendance"] = clean_attendance(data["attendance"])

    if "performance" in data:
        cleaned_data["performance"] = clean_performance(data["performance"])

    print("Data cleaning and standardization completed.")
    return cleaned_data