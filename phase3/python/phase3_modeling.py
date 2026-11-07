from __future__ import annotations

import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

DATA_PATH = Path(r'D:\PhotonUser\Shameer\Capstone\phase2\output\cleaned_traffic_data.csv')
OUTPUT_DIR = Path(r'D:\PhotonUser\Shameer\Capstone\phase3\output')
LOG_PATH = OUTPUT_DIR / 'phase3_modeling.log'


def setup_logging() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[
            logging.FileHandler(LOG_PATH, mode='w', encoding='utf-8'),
            logging.StreamHandler(),
        ],
    )


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    logging.info('Loaded data with %s rows', len(df))
    return df


def prepare_regression_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    feature_cols = [
        'temp', 'rain_1h', 'snow_1h', 'clouds_all', 'holiday_flag', 'rain_flag',
        'snow_flag', 'hour', 'month', 'is_weekend', 'peak_hour', 'hour_sin', 'hour_cos', 'temperature_c'
    ]
    X = df[feature_cols]
    y = df['traffic_volume']
    return X, y


def prepare_classification_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    feature_cols = [
        'temp', 'rain_1h', 'snow_1h', 'clouds_all', 'holiday_flag', 'rain_flag',
        'snow_flag', 'hour', 'month', 'is_weekend', 'peak_hour', 'hour_sin', 'hour_cos', 'temperature_c'
    ]
    X = df[feature_cols]
    y = (df['traffic_volume'] >= df['traffic_volume'].quantile(0.75)).astype(int)
    return X, y


def build_regression_model(X: pd.DataFrame, y: pd.Series) -> dict:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    metrics = {
        'model': 'LinearRegression',
        'mae': mean_absolute_error(y_test, pred),
        'rmse': float(np.sqrt(mean_squared_error(y_test, pred))),
        'r2': r2_score(y_test, pred),
    }
    return metrics


def build_classification_model(X: pd.DataFrame, y: pd.Series) -> dict:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    metrics = {
        'model': 'LogisticRegression',
        'accuracy': accuracy_score(y_test, pred),
        'f1': f1_score(y_test, pred),
        'confusion_matrix': confusion_matrix(y_test, pred).tolist(),
    }
    return metrics


def run_clustering(df: pd.DataFrame) -> dict:
    features = df[['temp', 'rain_1h', 'snow_1h', 'clouds_all', 'traffic_volume', 'hour']]
    model = KMeans(n_clusters=4, random_state=42, n_init=10)
    labels = model.fit_predict(features)
    df_cluster = df.copy()
    df_cluster['cluster'] = labels

    cluster_summary = (
        df_cluster.groupby('cluster')['traffic_volume']
        .mean().sort_values(ascending=False)
        .to_dict()
    )

    result = {
        'n_clusters': 4,
        'cluster_summary': cluster_summary,
        'cluster_counts': df_cluster['cluster'].value_counts().to_dict(),
    }
    return result


def save_outputs(regression_metrics: dict, classification_metrics: dict, clustering_summary: dict) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_DIR / 'phase3_metrics.json', 'w', encoding='utf-8') as f:
        json.dump({
            'regression': regression_metrics,
            'classification': classification_metrics,
            'clustering': clustering_summary,
        }, f, indent=2)

    summary_md = '''# Phase 3 Modeling Summary

## Regression
- Model: LinearRegression
- MAE: {mae:.4f}
- RMSE: {rmse:.4f}
- R2: {r2:.4f}

## Classification
- Model: LogisticRegression
- Accuracy: {accuracy:.4f}
- F1: {f1:.4f}

## Clustering
- KMeans with 4 clusters
- Average traffic by cluster: {cluster_summary}
'''.format(
        mae=regression_metrics['mae'],
        rmse=regression_metrics['rmse'],
        r2=regression_metrics['r2'],
        accuracy=classification_metrics['accuracy'],
        f1=classification_metrics['f1'],
        cluster_summary=clustering_summary['cluster_summary'],
    )
    (OUTPUT_DIR / 'phase3_summary.md').write_text(summary_md, encoding='utf-8')


def main() -> None:
    setup_logging()
    logging.info('Starting Phase 3 modeling workflow.')
    df = load_data()

    X_reg, y_reg = prepare_regression_data(df)
    X_cls, y_cls = prepare_classification_data(df)

    regression_metrics = build_regression_model(X_reg, y_reg)
    classification_metrics = build_classification_model(X_cls, y_cls)
    clustering_summary = run_clustering(df)

    save_outputs(regression_metrics, classification_metrics, clustering_summary)

    logging.info('Regression metrics: %s', regression_metrics)
    logging.info('Classification metrics: %s', classification_metrics)
    logging.info('Clustering summary: %s', clustering_summary)

    print('Phase 3 complete.')
    print(json.dumps({'regression': regression_metrics, 'classification': classification_metrics, 'clustering': clustering_summary}, indent=2))


if __name__ == '__main__':
    main()
