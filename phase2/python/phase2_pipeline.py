from __future__ import annotations

import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd

RAW_PATH = Path(r'D:\PhotonUser\Shameer\Capstone\data\raw\Metro_Interstate_Traffic_Volume.csv')
OUTPUT_DIR = Path(r'D:\PhotonUser\Shameer\Capstone\phase2\output')
LOG_PATH = OUTPUT_DIR / 'phase2_pipeline.log'


def setup_logging() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[
            logging.FileHandler(LOG_PATH, mode='w', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )


def validate_schema(df: pd.DataFrame) -> None:
    required = {
        'holiday', 'temp', 'rain_1h', 'snow_1h', 'clouds_all',
        'weather_main', 'weather_description', 'date_time', 'traffic_volume'
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f'Missing required columns: {sorted(missing)}')
    logging.info('Schema validation passed. Found %s columns.', len(df.columns))


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    initial_rows = len(df)
    logging.info('Initial rows: %s', initial_rows)

    df = df.copy()
    df['holiday'] = df['holiday'].replace(['', ' ', 'nan', 'NaN'], 'None')
    df['holiday'] = df['holiday'].fillna('None')
    df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')
    df = df.dropna(subset=['date_time']).copy()
    logging.info('Removed rows with invalid date_time: %s', initial_rows - len(df))

    df = df.drop_duplicates().copy()
    logging.info('Removed duplicate rows: %s', initial_rows - len(df))

    q1 = df['traffic_volume'].quantile(0.25)
    q3 = df['traffic_volume'].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outlier_count = int(((df['traffic_volume'] < lower_bound) | (df['traffic_volume'] > upper_bound)).sum())
    df = df[(df['traffic_volume'] >= lower_bound) & (df['traffic_volume'] <= upper_bound)].copy()
    logging.info('Removed outliers based on IQR: %s', outlier_count)

    for col in ['temp', 'rain_1h', 'snow_1h', 'clouds_all']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=['temp', 'rain_1h', 'snow_1h', 'clouds_all', 'traffic_volume']).copy()
    logging.info('Removed rows with missing values in required numeric fields.')

    df['temperature_c'] = df['temp'] - 273.15
    df['holiday_flag'] = (df['holiday'] != 'None').astype(int)
    df['rain_flag'] = (df['rain_1h'] > 0).astype(int)
    df['snow_flag'] = (df['snow_1h'] > 0).astype(int)
    df['hour'] = df['date_time'].dt.hour
    df['day_of_week'] = df['date_time'].dt.day_name()
    df['month'] = df['date_time'].dt.month
    df['is_weekend'] = df['day_of_week'].isin(['Saturday', 'Sunday']).astype(int)
    df['peak_hour'] = df['hour'].isin([7, 8, 9, 16, 17, 18]).astype(int)

    hour = df['hour']
    df['hour_sin'] = np.sin(2 * np.pi * hour / 24)
    df['hour_cos'] = np.cos(2 * np.pi * hour / 24)

    df = df.sort_values('date_time').reset_index(drop=True)
    logging.info('Cleaning complete. Final rows: %s', len(df))
    return df


def create_summary(df: pd.DataFrame) -> dict:
    summary = {
        'rows': int(len(df)),
        'columns': list(df.columns),
        'mean_traffic_volume': float(df['traffic_volume'].mean()),
        'median_traffic_volume': float(df['traffic_volume'].median()),
        'max_traffic_volume': float(df['traffic_volume'].max()),
        'min_traffic_volume': float(df['traffic_volume'].min()),
        'mean_temp_k': float(df['temp'].mean()),
        'holiday_flag_rate': float(df['holiday_flag'].mean()),
        'rain_flag_rate': float(df['rain_flag'].mean()),
    }
    return summary


def main() -> None:
    setup_logging()
    logging.info('Starting Phase 2 pipeline for Metro traffic dataset.')

    df = pd.read_csv(RAW_PATH)
    validate_schema(df)
    cleaned_df = clean_dataset(df)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(OUTPUT_DIR / 'cleaned_traffic_data.csv', index=False)

    summary = create_summary(cleaned_df)
    with open(OUTPUT_DIR / 'feature_summary.json', 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    summary_md = '''# Phase 2 Summary

## Data Cleaning Outcome
- Raw rows processed: {}\n- Cleaned rows retained: {}\n- Missing or invalid date rows removed\n- Duplicate rows removed\n- IQR-based outliers removed\n
## Feature Engineering
- holiday_flag\n- rain_flag\n- snow_flag\n- hour\n- day_of_week\n- month\n- is_weekend\n- peak_hour\n- hour_sin\n- hour_cos\n- temperature_c\n
## Model-readiness
This cleaned dataset is ready for classification, regression, clustering, and deep learning work in later phases.
'''.format(len(pd.read_csv(RAW_PATH)), len(cleaned_df))
    (OUTPUT_DIR / 'phase2_summary.md').write_text(summary_md, encoding='utf-8')

    logging.info('Phase 2 pipeline complete.')
    logging.info('Saved dataset to %s', OUTPUT_DIR / 'cleaned_traffic_data.csv')
    print('Phase 2 pipeline complete.')
    print('Cleaned rows:', len(cleaned_df))
    print('Mean traffic volume:', round(cleaned_df['traffic_volume'].mean(), 2))


if __name__ == '__main__':
    main()
