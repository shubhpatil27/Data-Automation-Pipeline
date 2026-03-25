import os
import pandas as pd


def normalize_data(cleaned_data: dict) -> dict:
    """
    Create structured tables aligned with relational database principles
    and save them to data/processed.
    """
    os.makedirs("data/processed", exist_ok=True)

    normalized_data = {}

    students_df = cleaned_data.get("students")
    enrollments_df = cleaned_data.get("enrollments")
    attendance_df = cleaned_data.get("attendance")
    performance_df = cleaned_data.get("performance")

    if students_df is not None:
        students_table = students_df.copy()
        normalized_data["students"] = students_table
        students_table.to_csv("data/processed/students.csv", index=False)

    if enrollments_df is not None:
        enrollments_table = enrollments_df.copy()
        normalized_data["enrollments"] = enrollments_table
        enrollments_table.to_csv("data/processed/enrollments.csv", index=False)

        if "course_id" in enrollments_table.columns:
            course_columns = [col for col in ["course_id", "course_name", "department", "credits"] if col in enrollments_table.columns]

            if course_columns:
                courses_table = enrollments_table[course_columns].drop_duplicates().reset_index(drop=True)
                normalized_data["courses"] = courses_table
                courses_table.to_csv("data/processed/courses.csv", index=False)

    if attendance_df is not None:
        attendance_table = attendance_df.copy()
        normalized_data["attendance"] = attendance_table
        attendance_table.to_csv("data/processed/attendance.csv", index=False)

    if performance_df is not None:
        performance_table = performance_df.copy()
        normalized_data["performance"] = performance_table
        performance_table.to_csv("data/processed/performance.csv", index=False)

    cleaned_master_parts = []

    for name, df in normalized_data.items():
        temp_df = df.copy()
        temp_df["source_table"] = name
        cleaned_master_parts.append(temp_df)

    if cleaned_master_parts:
        cleaned_master_dataset = pd.concat(cleaned_master_parts, ignore_index=True, sort=False)
        normalized_data["cleaned_master_dataset"] = cleaned_master_dataset
        cleaned_master_dataset.to_csv("data/processed/cleaned_master_dataset.csv", index=False)

    print("Normalized tables created and saved successfully.")
    return normalized_data