# -----------------------------------------------------------------------
# Central configuration for the preprocessing pipeline.
#
# Nothing dataset-specific should live inside preprocessing.py — if you
# want to reuse the pipeline on a different dataset tomorrow, you only
# need to change the values here.
# -----------------------------------------------------------------------

# Path to the raw data file used by main.py
DATA_PATH = "data/raw/titanic.csv"

# Columns to remove during preprocessing.
# For the Titanic dataset these are identifier / free-text columns that
# don't carry predictive signal on their own.
COLUMNS_TO_DROP = [
    "PassengerId",
    "Name",
    "Ticket",
]
