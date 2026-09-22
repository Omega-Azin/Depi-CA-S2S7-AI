"""
main.py

Runs the preprocessing pipeline:
    1. Load the raw CSV.
    2. Optionally drop unnecessary features (columns come from config.py).
    3. Optionally print a data-quality / dtype report.
"""

from config.config import DATA_PATH, COLUMNS_TO_DROP
from preprocessing import Read_data_file, Drop_unnecessary_features, Check_data_type


def main():
    df = Read_data_file(DATA_PATH)
    if df is None:
        print("Could not load the dataset. Exiting.")
        return

    print(f"\nLoaded dataset with shape: {df.shape}\n")

    choice = input(
        "What would you like to do?\n"
        "  [1] Remove unnecessary features (columns from config.py)\n"
        "  [2] Check data types / data-quality report\n"
        "  [3] Both\n"
        "Enter 1, 2, or 3: "
    ).strip()

    if choice in ("1", "3"):
        df = Drop_unnecessary_features(df, COLUMNS_TO_DROP)
        print(f"\nColumns after dropping: {list(df.columns)}\n")

    if choice in ("2", "3"):
        report = Check_data_type(df)
        print("\nData-quality report:\n")
        print(report)

    if choice not in ("1", "2", "3"):
        print("Invalid choice — please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
