import pandas as pd


def validate_students(df: pd.DataFrame) -> list:
    issues = []

    if "student_id" in df.columns:
        missing_ids = df["student_id"].isna().sum() + (df["student_id"] == "").sum()
        if missing_ids > 0:
            issues.append(f"Students: {missing_ids} missing student_id values found.")

        duplicate_ids = df["student_id"].duplicated().sum()
        if duplicate_ids > 0:
            issues.append(f"Students: {duplicate_ids} duplicate student_id values found.")

    return issues


def validate_enrollments(df: pd.DataFrame, students_df: pd.DataFrame = None) -> list:
    issues = []

    if "student_id" in df.columns:
        missing_ids = df["student_id"].isna().sum() + (df["student_id"] == "").sum()
        if missing_ids > 0:
            issues.append(f"Enrollments: {missing_ids} missing student_id values found.")

    if "course_id" in df.columns:
        missing_course_ids = df["course_id"].isna().sum() + (df["course_id"] == "").sum()
        if missing_course_ids > 0:
            issues.append(f"Enrollments: {missing_course_ids} missing course_id values found.")

    if {"student_id", "course_id", "semester"}.issubset(df.columns):
        duplicate_enrollments = df.duplicated(subset=["student_id", "course_id", "semester"]).sum()
        if duplicate_enrollments > 0:
            issues.append(
                f"Enrollments: {duplicate_enrollments} duplicate student-course-semester records found."
            )

    if students_df is not None and "student_id" in df.columns and "student_id" in students_df.columns:
        invalid_students = ~df["student_id"].isin(students_df["student_id"])
        invalid_count = invalid_students.sum()
        if invalid_count > 0:
            issues.append(
                f"Enrollments: {invalid_count} records reference student_id values not found in students table."
            )

    return issues


def validate_attendance(df: pd.DataFrame, students_df: pd.DataFrame = None) -> list:
    issues = []

    if "attendance_percent" in df.columns:
        invalid_attendance = ((df["attendance_percent"] < 0) | (df["attendance_percent"] > 100)).sum()
        if invalid_attendance > 0:
            issues.append(
                f"Attendance: {invalid_attendance} invalid attendance_percent values found (must be 0 to 100)."
            )

    if students_df is not None and "student_id" in df.columns and "student_id" in students_df.columns:
        invalid_students = ~df["student_id"].isin(students_df["student_id"])
        invalid_count = invalid_students.sum()
        if invalid_count > 0:
            issues.append(
                f"Attendance: {invalid_count} records reference student_id values not found in students table."
            )

    return issues


def validate_performance(df: pd.DataFrame, students_df: pd.DataFrame = None) -> list:
    issues = []

    if "gpa" in df.columns:
        invalid_gpa = ((df["gpa"] < 0) | (df["gpa"] > 4)).sum()
        if invalid_gpa > 0:
            issues.append(f"Performance: {invalid_gpa} invalid GPA values found (must be 0 to 4).")

    if "credits_completed" in df.columns:
        invalid_credits = (df["credits_completed"] < 0).sum()
        if invalid_credits > 0:
            issues.append(
                f"Performance: {invalid_credits} invalid credits_completed values found (must be non-negative)."
            )

    if students_df is not None and "student_id" in df.columns and "student_id" in students_df.columns:
        invalid_students = ~df["student_id"].isin(students_df["student_id"])
        invalid_count = invalid_students.sum()
        if invalid_count > 0:
            issues.append(
                f"Performance: {invalid_count} records reference student_id values not found in students table."
            )

    return issues


def validate_data(cleaned_data: dict) -> list:
    """
    Run automated validation checks across all cleaned datasets.
    Returns a list of validation issues.
    """
    issues = []

    students_df = cleaned_data.get("students")
    enrollments_df = cleaned_data.get("enrollments")
    attendance_df = cleaned_data.get("attendance")
    performance_df = cleaned_data.get("performance")

    if students_df is not None:
        issues.extend(validate_students(students_df))

    if enrollments_df is not None:
        issues.extend(validate_enrollments(enrollments_df, students_df))

    if attendance_df is not None:
        issues.extend(validate_attendance(attendance_df, students_df))

    if performance_df is not None:
        issues.extend(validate_performance(performance_df, students_df))

    if issues:
        print("Validation completed with issues found.")
    else:
        print("Validation completed. No issues found.")

    return issues