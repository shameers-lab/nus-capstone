"""Phase 1 exploratory analysis for the capstone project.

This script is a starting point for the first project section.
It reads the traffic dataset, validates the basic structure,
computes key descriptive statistics, and produces a first pass at insights.

Before running this script, place the dataset here:
    data/raw/Metro_Interstate_Traffic_Volume.csv
"""

from pathlib import Path

import pandas as pd


DATA_PATH = Path(__file__).resolve().parents[1] / 'data' / 'raw' / 'Metro_Interstate_Traffic_Volume.csv'


def load_data(path: Path) -> pd.DataFrame:
    """Load the raw CSV file into a DataFrame."""
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found at {path}. Copy the dataset into this project folder first.")

    df = pd.read_csv(path)
    return df


def basic_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return standard descriptive statistics for numeric variables."""
    return df.describe(include='all').T


def main() -> None:
    df = load_data(DATA_PATH)

    print('Dataset loaded successfully.')
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print('\nColumns:')
    print(df.columns.tolist())

    print('\nBasic summary:')
    print(basic_summary(df).head(20))

    print('\nHead of data:')
    print(df.head())

    print('\nMissing values:')
    print(df.isnull().sum())


if __name__ == '__main__':
    main()
