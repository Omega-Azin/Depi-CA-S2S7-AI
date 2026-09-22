"""
preprocessing.py

Reusable, dataset-agnostic preprocessing functions.
None of these functions should hardcode anything specific to the
Titanic dataset — column names to drop, paths, etc. all come from
config.py or from the function's arguments.
"""

import os
import pandas as pd


def Read_data_file(file_path):
    """
    Reads a CSV file into a pandas DataFrame.

    Handles the common failure cases gracefully instead of letting a
    raw pandas traceback bubble up:
        - the path is empty / not a string
        - the file does not exist
        - the path points to something that isn't a file
        - the file exists but is empty or not valid CSV
        - the file can't be read due to permissions

    Returns
    -------
    pd.DataFrame on success, or None on failure (a clear message is
    printed explaining what went wrong).
    """
    if not file_path or not isinstance(file_path, str):
        print(f"Invalid file path provided: {file_path!r}")
        return None

    if not os.path.exists(file_path):
        print(f"File not found: '{file_path}'. Please check the path and try again.")
        return None

    if not os.path.isfile(file_path):
        print(f"The path '{file_path}' exists but is not a file.")
        return None

    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        print(f"The file '{file_path}' is empty.")
        return None
    except pd.errors.ParserError:
        print(f"The file '{file_path}' could not be parsed as a valid CSV.")
        return None
    except PermissionError:
        print(f"Permission denied when trying to read '{file_path}'.")
        return None
    except Exception as e:
        print(f"Unexpected error while reading '{file_path}': {e}")
        return None

    if df.empty:
        print(f"Warning: '{file_path}' was read successfully but contains no rows.")

    return df


def Drop_unnecessary_features(df, cols_to_drop):
    """
    Drops the columns listed in cols_to_drop from df.

    cols_to_drop is passed in (normally sourced from config.py) rather
    than hardcoded here, so this same function works unchanged on any
    dataset.

    Returns
    -------
    A new DataFrame with the requested columns removed. Columns that
    don't exist in df are safely skipped (with a note printed).
    """
    if df is None:
        print("Drop_unnecessary_features: received None instead of a DataFrame.")
        return df

    if not cols_to_drop:
        print("No columns specified to drop — returning DataFrame unchanged.")
        return df

    existing = [c for c in cols_to_drop if c in df.columns]
    missing = [c for c in cols_to_drop if c not in df.columns]

    if missing:
        print(f"Note: these columns were not found and were skipped: {missing}")

    return df.drop(columns=existing)


def Check_data_type(df):
    """
    Builds a small, easy-to-read data-quality report.

    For every column shows:
        - dtype
        - number of unique (non-null) values
        - number of missing values

    Returns the report transposed, so each column of the original
    DataFrame becomes a row in the report — quick to scan for
    questions like "what dtype is Age?" or "how many uniques does
    Embarked have?".
    """
    if df is None:
        print("Check_data_type: received None instead of a DataFrame.")
        return None

    report = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "n_unique": df.nunique(dropna=True),
        "n_missing": df.isna().sum(),
    })

    return report.T
