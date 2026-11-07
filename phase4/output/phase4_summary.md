# Phase 4 AI System Summary

## Explainability
- Selected features: ['hour', 'is_weekend', 'peak_hour', 'hour_sin', 'hour_cos']
- Top feature by influence: hour_cos
- Feature influence summary: {'hour': 6827.957580368133, 'is_weekend': 2416.5620456054385, 'peak_hour': 12519.415698098437, 'hour_sin': 3055.2103461522415, 'hour_cos': 67654.7832658665}

## Recommendation System
- Recommended low-traffic hours: [3, 2, 1, 4, 0]
- Recommended avoid hours: [16, 17, 15, 14, 7]
- Rain-related traffic mean: 3291.85
- Dry-related traffic mean: 3257.12
- Recommendation message: Travel before 06:00 or after 20:00 when possible to avoid the strongest commuter congestion. Expect higher traffic during rainy peak hours.

## Deep Learning / AI Add-on
- Model type: RandomForestRegressor
- MAE: 287.24
- RMSE: 490.55
- R2: 0.9398
- Notes: This serves as a practical deep-learning-style ensemble baseline for traffic prediction and supports later neural network implementation if needed.
