import os
import pandas as pd


def generate_data_quality_report(validation_issues: list) -> None:
    """
    Write validation issues to a text report.
    """
    os.makedirs("reports", exist_ok=True)

    report_path = "reports/data_quality_report.txt"

    with open(report_path, "w", encoding="utf-8") as file:
        file.write("DATA QUALITY REPORT\n")
        file.write("=" * 50 + "\n\n")

        if validation_issues:
            file.write("Validation issues found:\n\n")
            for idx, issue in enumerate(validation_issues, start=1):
                file.write(f"{idx}. {issue}\n")
        else:
            file.write("No validation issues found.\n")

    print(f"Data quality report saved to {report_path}")


def generate_summary_metrics(normalized_data: dict) -> None:
    """
    Generate summary metrics and save them to an Excel workbook.
    """
    os.makedirs("reports", exist_ok=True)

    output_path = "reports/summary_metrics.xlsx"

    students_df = normalized_data.get("students")
    enrollments_df = normalized_data.get("enrollments")
    attendance_df = normalized_data.get("attendance")
    performance_df = normalized_data.get("performance")

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        summary_overview = []

        if students_df is not None:
            summary_overview.append(["Total Students", len(students_df)])

            if "major" in students_df.columns:
                students_by_major = (
                    students_df["major"]
                    .value_counts(dropna=False)
                    .reset_index()
                )
                students_by_major.columns = ["major", "student_count"]
                students_by_major.to_excel(
                    writer,
                    sheet_name="Students by Major",
                    index=False
                )

        if enrollments_df is not None:
            summary_overview.append(["Total Enrollments", len(enrollments_df)])

            if "semester" in enrollments_df.columns:
                enrollments_by_semester = (
                    enrollments_df["semester"]
                    .value_counts(dropna=False)
                    .reset_index()
                )
                enrollments_by_semester.columns = ["semester", "enrollment_count"]
                enrollments_by_semester.to_excel(
                    writer,
                    sheet_name="Enrollments by Semester",
                    index=False
                )

        if attendance_df is not None and "attendance_percent" in attendance_df.columns:
            avg_attendance = attendance_df["attendance_percent"].mean()
            summary_overview.append(["Average Attendance", round(avg_attendance, 2)])

        if performance_df is not None:
            if "gpa" in performance_df.columns:
                avg_gpa = performance_df["gpa"].mean()
                summary_overview.append(["Average GPA", round(avg_gpa, 2)])

            if "credits_completed" in performance_df.columns:
                avg_credits = performance_df["credits_completed"].mean()
                summary_overview.append(["Average Credits Completed", round(avg_credits, 2)])

        overview_df = pd.DataFrame(summary_overview, columns=["metric", "value"])
        overview_df.to_excel(writer, sheet_name="Overview", index=False)

    print(f"Summary metrics saved to {output_path}")


def generate_reports(normalized_data: dict, validation_issues: list) -> None:
    """
    Generate all project reports.
    """
    generate_data_quality_report(validation_issues)
    generate_summary_metrics(normalized_data)
    print("All reports generated successfully.")