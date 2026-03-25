import pandas as pd
import os

def load_data():
    """
    Load all raw datasets from the data/raw directory
    and return them as a dictionary of DataFrames.
    """

    base_path = "data/raw"

    files = {
        "students": "student_master.csv",
        "enrollments": "course_enrollments.csv",
        "attendance": "attendance_records.csv",
        "performance": "academic_performance.csv"
    }

    data = {}

    for key, filename in files.items():
        file_path = os.path.join(base_path, filename)

        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                data[key] = df
                print(f"Loaded {filename} successfully.")
            except Exception as e:
                print(f"Error loading {filename}: {e}")
        else:
            print(f"File not found: {filename}")

    return data