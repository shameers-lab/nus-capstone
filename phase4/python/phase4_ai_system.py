from __future__ import annotations

import json
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

DATA_PATH = Path(r'D:\PhotonUser\Shameer\Capstone\phase2\output\cleaned_traffic_data.csv')
OUTPUT_DIR = Path(r'D:\PhotonUser\Shameer\Capstone\phase4\output')
LOG_PATH = OUTPUT_DIR / 'phase4_ai_system.log'


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
    return df


def build_explainability_summary(df: pd.DataFrame) -> dict:
    feature_cols = [
        'temp', 'rain_1h', 'snow_1h', 'clouds_all', 'holiday_flag', 'rain_flag',
        'snow_flag', 'hour', 'month', 'is_weekend', 'peak_hour', 'hour_sin', 'hour_cos', 'temperature_c'
    ]
    X = df[feature_cols]
    y = df['traffic_volume']

    selector = SelectKBest(score_func=f_regression, k=5)
    X_selected = selector.fit_transform(X, y)
    selected_features = np.array(feature_cols)[selector.get_support()]
    scores = selector.scores_[selector.get_support()]

    feature_importance = dict(zip(selected_features.tolist(), scores.tolist()))
    top_feature = max(feature_importance, key=feature_importance.get)
    return {
        'selected_features': selected_features.tolist(),
        'feature_importance': feature_importance,
        'top_feature': top_feature,
    }


def build_recommendation_logic(df: pd.DataFrame) -> dict:
    hourly = df.groupby('hour')['traffic_volume'].mean().sort_values(ascending=False)
    best_low_traffic_hours = hourly.sort_values().head(5).index.tolist()
    best_avoid_hours = hourly.sort_values(ascending=False).head(5).index.tolist()

    rain_mean = df[df['rain_flag'] == 1]['traffic_volume'].mean()
    dry_mean = df[df['rain_flag'] == 0]['traffic_volume'].mean()

    recommendation = {
        'recommended_low_traffic_hours': best_low_traffic_hours,
        'recommended_avoid_hours': best_avoid_hours,
        'rain_related_traffic_mean': float(rain_mean),
        'dry_related_traffic_mean': float(dry_mean),
        'message': 'Travel before 06:00 or after 20:00 when possible to avoid the strongest commuter congestion. Expect higher traffic during rainy peak hours.'
    }
    return recommendation


def build_deep_learning_proxy(df: pd.DataFrame) -> dict:
    feature_cols = [
        'temp', 'rain_1h', 'snow_1h', 'clouds_all', 'holiday_flag', 'rain_flag',
        'snow_flag', 'hour', 'month', 'is_weekend', 'peak_hour', 'hour_sin', 'hour_cos', 'temperature_c'
    ]
    X = df[feature_cols].values
    y = df['traffic_volume'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    rf_model = RandomForestRegressor(n_estimators=200, random_state=42)
    rf_model.fit(X_train, y_train)
    pred = rf_model.predict(X_test)

    metrics = {
        'mae': float(mean_absolute_error(y_test, pred)),
        'rmse': float(np.sqrt(mean_squared_error(y_test, pred))),
        'r2': float(r2_score(y_test, pred)),
    }
    return {
        'model_type': 'RandomForestRegressor',
        'metrics': metrics,
        'notes': 'This serves as a practical deep-learning-style ensemble baseline for traffic prediction and supports later neural network implementation if needed.'
    }


def save_outputs(explainability: dict, recommendation: dict, deep_learning: dict) -> None:
    output_data = {
        'explainability': explainability,
        'recommendation_system': recommendation,
        'deep_learning_proxy': deep_learning,
    }
    with open(OUTPUT_DIR / 'phase4_ai_summary.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)

    summary_md = '''# Phase 4 AI System Summary

## Explainability
- Selected features: {selected_features}
- Top feature by influence: {top_feature}
- Feature influence summary: {feature_importance}

## Recommendation System
- Recommended low-traffic hours: {low_hours}
- Recommended avoid hours: {avoid_hours}
- Rain-related traffic mean: {rain_mean:.2f}
- Dry-related traffic mean: {dry_mean:.2f}
- Recommendation message: {message}

## Deep Learning / AI Add-on
- Model type: {model_type}
- MAE: {mae:.2f}
- RMSE: {rmse:.2f}
- R2: {r2:.4f}
- Notes: {notes}
'''.format(
        selected_features=explainability['selected_features'],
        top_feature=explainability['top_feature'],
        feature_importance=explainability['feature_importance'],
        low_hours=recommendation['recommended_low_traffic_hours'],
        avoid_hours=recommendation['recommended_avoid_hours'],
        rain_mean=recommendation['rain_related_traffic_mean'],
        dry_mean=recommendation['dry_related_traffic_mean'],
        message=recommendation['message'],
        model_type=deep_learning['model_type'],
        mae=deep_learning['metrics']['mae'],
        rmse=deep_learning['metrics']['rmse'],
        r2=deep_learning['metrics']['r2'],
        notes=deep_learning['notes'],
    )
    (OUTPUT_DIR / 'phase4_summary.md').write_text(summary_md, encoding='utf-8')


def main() -> None:
    setup_logging()
    logging.info('Starting Phase 4 AI system workflow.')
    df = load_data()

    explainability = build_explainability_summary(df)
    recommendation = build_recommendation_logic(df)
    deep_learning = build_deep_learning_proxy(df)
    save_outputs(explainability, recommendation, deep_learning)

    logging.info('Explainability summary: %s', explainability)
    logging.info('Recommendation summary: %s', recommendation)
    logging.info('Deep learning summary: %s', deep_learning)

    print('Phase 4 complete.')
    print(json.dumps({'explainability': explainability, 'recommendation': recommendation, 'deep_learning': deep_learning}, indent=2))


if __name__ == '__main__':
    main()
