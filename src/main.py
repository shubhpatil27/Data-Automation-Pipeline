from ingest import load_data
from clean import clean_data
from validate import validate_data
from normalize import normalize_data
from report import generate_reports


def main():
    print("Starting data automation pipeline...")

    data = load_data()

    if not data:
        print("No input files were loaded. Please check the data/raw folder.")
        return

    cleaned_data = clean_data(data)
    validation_issues = validate_data(cleaned_data)
    normalized_data = normalize_data(cleaned_data)
    generate_reports(normalized_data, validation_issues)

    print("Pipeline completed successfully.")


if __name__ == "__main__":
    main()