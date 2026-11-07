from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import sqlite3

DATA_PATH = Path(r'D:\PhotonUser\Shameer\Capstone\data\raw\Metro_Interstate_Traffic_Volume.csv')
OUTPUT_DIR = Path(r'D:\PhotonUser\Shameer\Capstone\phase1\output')
DB_PATH = OUTPUT_DIR / 'traffic_analysis.db'


def load_dataset() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')
    df['holiday_flag'] = df['holiday'].fillna('None').astype(str).ne('None').astype(int)
    df['rain_flag'] = (df['rain_1h'] > 0).astype(int)
    df['snow_flag'] = (df['snow_1h'] > 0).astype(int)
    df['hour'] = df['date_time'].dt.hour
    df['day_of_week'] = df['date_time'].dt.day_name()
    df['month'] = df['date_time'].dt.month
    return df


def compute_descriptive_stats(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = ['temp', 'rain_1h', 'snow_1h', 'clouds_all', 'traffic_volume']
    stats = df[numeric_cols].describe().T
    stats['median'] = df[numeric_cols].median()
    stats['std'] = df[numeric_cols].std(ddof=1)
    stats['variance'] = df[numeric_cols].var(ddof=1)
    return stats.reset_index().rename(columns={'index': 'variable'})


def compute_correlations(df: pd.DataFrame) -> pd.DataFrame:
    corr = df[['temp', 'rain_1h', 'snow_1h', 'clouds_all', 'traffic_volume']].corr(method='pearson')
    corr = corr.reset_index().rename(columns={'index': 'variable'})
    return corr


def compute_probability_summary(df: pd.DataFrame) -> dict:
    q75 = df['traffic_volume'].quantile(0.75)
    df['high_traffic'] = (df['traffic_volume'] >= q75).astype(int)

    total = len(df)
    p_high = df['high_traffic'].mean()
    p_rain = df['rain_flag'].mean()
    p_holiday = df['holiday_flag'].mean()

    p_high_given_rain = df.loc[df['rain_flag'] == 1, 'high_traffic'].mean() if (df['rain_flag'] == 1).any() else 0.0
    p_high_given_no_rain = df.loc[df['rain_flag'] == 0, 'high_traffic'].mean() if (df['rain_flag'] == 0).any() else 0.0
    p_high_given_holiday = df.loc[df['holiday_flag'] == 1, 'high_traffic'].mean() if (df['holiday_flag'] == 1).any() else 0.0
    p_high_given_no_holiday = df.loc[df['holiday_flag'] == 0, 'high_traffic'].mean() if (df['holiday_flag'] == 0).any() else 0.0

    odds_ratio = (p_high_given_rain / (1 - p_high_given_rain)) / (p_high_given_no_rain / (1 - p_high_given_no_rain)) if p_high_given_no_rain not in (0, 1) and p_high_given_rain not in (0, 1) else None

    summary = {
        'total_records': int(total),
        'high_traffic_threshold': float(q75),
        'p_high_traffic': float(p_high),
        'p_high_traffic_given_rain': float(p_high_given_rain),
        'p_high_traffic_given_no_rain': float(p_high_given_no_rain),
        'p_high_traffic_given_holiday': float(p_high_given_holiday),
        'p_high_traffic_given_no_holiday': float(p_high_given_no_holiday),
        'p_rain': float(p_rain),
        'p_holiday': float(p_holiday),
        'odds_ratio_rain_vs_no_rain': odds_ratio,
    }
    return summary


def save_outputs(df: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    stats = compute_descriptive_stats(df)
    corr = compute_correlations(df)
    prob = compute_probability_summary(df)

    hourly = (
        df.groupby('hour')['traffic_volume']
        .agg(['count', 'mean', 'median', 'min', 'max'])
        .reset_index()
        .rename(columns={'mean': 'avg_traffic_volume', 'median': 'median_traffic_volume'})
    )

    stats.to_csv(OUTPUT_DIR / 'descriptive_statistics.csv', index=False)
    corr.to_csv(OUTPUT_DIR / 'correlation_matrix.csv', index=False)
    hourly.to_csv(OUTPUT_DIR / 'hourly_traffic_summary.csv', index=False)
    with open(OUTPUT_DIR / 'probability_summary.json', 'w', encoding='utf-8') as f:
        json.dump(prob, f, indent=2)

    summary_md = f'''# Phase 1 summary

## Dataset overview
- Records: {len(df):,}
- Date range: {df['date_time'].min()} to {df['date_time'].max()}
- Variables: {list(df.columns)}

## Descriptive statistics highlights
- Mean traffic volume: {df['traffic_volume'].mean():.2f}
- Median traffic volume: {df['traffic_volume'].median():.2f}
- Max traffic volume: {df['traffic_volume'].max():.2f}
- Mean temperature: {df['temp'].mean():.2f} K
- Mean rain_1h: {df['rain_1h'].mean():.2f}

## Correlation highlights
- Traffic vs temperature: {df['traffic_volume'].corr(df['temp']):.4f}
- Traffic vs rain_1h: {df['traffic_volume'].corr(df['rain_1h']):.4f}
- Traffic vs snow_1h: {df['traffic_volume'].corr(df['snow_1h']):.4f}
- Traffic vs clouds_all: {df['traffic_volume'].corr(df['clouds_all']):.4f}

## Probability highlights
- High traffic threshold (75th percentile): {prob['high_traffic_threshold']:.2f}
- P(high traffic): {prob['p_high_traffic']:.4f}
- P(high traffic | rain): {prob['p_high_traffic_given_rain']:.4f}
- P(high traffic | no rain): {prob['p_high_traffic_given_no_rain']:.4f}
- P(high traffic | holiday): {prob['p_high_traffic_given_holiday']:.4f}
- P(high traffic | no holiday): {prob['p_high_traffic_given_no_holiday']:.4f}
- Odds ratio (rain vs no rain): {prob['odds_ratio_rain_vs_no_rain']}

## Interpretation
This dataset shows the expected hourly commuter pattern, with the strongest traffic concentration during peak periods and sensitivity to weather or holiday-related travel effects. Detailed relationship checks should be interpreted alongside time-of-day effects because traffic volume is strongly influenced by both temporal and environmental conditions.
'''
    (OUTPUT_DIR / 'phase1_summary.md').write_text(summary_md, encoding='utf-8')

    conn = sqlite3.connect(DB_PATH)
    df.to_sql('traffic_volume', conn, if_exists='replace', index=False)
    conn.close()


if __name__ == '__main__':
    df = load_dataset()
    save_outputs(df)
    print('Phase 1 outputs saved to:', OUTPUT_DIR)
    print('Records:', len(df))
    print('Traffic mean:', round(df['traffic_volume'].mean(), 2))
    print('Traffic max:', round(df['traffic_volume'].max(), 2))
    print('Corr traffic-temp:', round(df['traffic_volume'].corr(df['temp']), 4))
    print('Probability summary:')
    print(json.dumps(compute_probability_summary(df), indent=2))
