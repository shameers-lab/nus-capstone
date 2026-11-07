# Final Capstone Report

## Project title
Traffic Volume Forecasting and Pattern Analysis for Interstate 94

## 1. Project overview
This capstone analyses hourly traffic patterns on westbound I-94 near Minneapolis–St Paul using traffic volume data combined with weather, date/time, and holiday information. The project follows a connected three-part structure: SQL and statistics analysis, Python-based data preprocessing and feature engineering, and machine learning and AI solution development.

## 2. Problem statement
Traffic conditions are heavily influenced by time of day, weather, and occasional holiday effects. A better understanding of these patterns can support traffic congestion planning, travel recommendations, and operational decision-making.

## 3. Dataset and context
The dataset contains approximately 48,000 hourly records and includes the following features:
- holiday
- temp
- rain_1h
- snow_1h
- clouds_all
- weather_main
- weather_description
- date_time
- traffic_volume

This dataset is the key analytical foundation for all work in the capstone.

## 4. Part 1: SQL, statistics, and probability
### SQL analysis
The SQL analysis focused on the relationship between traffic volume and factors such as hour of day, weekday, month, weather condition, and holiday status. The queries show that traffic volume changes strongly across hours and weekdays, which mirrors commuter travel behaviour.

### Descriptive statistics
The initial analysis found that the average traffic volume is approximately 3,259.82 vehicles per hour, with a maximum near 7,280. This indicates substantial variability and congestion during peak periods.

### Correlation highlights
Traffic volume shows a weak positive correlation with temperature and a measurable relationship with rain-related conditions. The dataset suggests that time-of-day and congestion patterns are the dominant drivers.

### Probability and conditional probability
The probability of high traffic is approximately 25.0%. When rainfall is present, the probability rises to around 27.0%, showing that weather conditions can meaningfully change congestion risk.

### Power BI/dashboard insight
The dashboard narrative emphasises time-of-day congestion, weather effects, and weekday concentration. These findings provide the foundation for later data preparation and predictive modeling.

## 5. Part 2: Data pipeline and feature engineering
The Python pipeline validates the schema, removes duplicate records, and handles missing values and outlier checks. Additional features were engineered to support downstream analytics and AI tasks, including:
- holiday_flag
- rain_flag
- snow_flag
- hour
- day_of_week
- month
- is_weekend
- peak_hour
- hour_sin
- hour_cos
- temperature_c

These features transform the raw dataset into a clean, model-ready structure.

## 6. Part 3: Machine learning and AI
### Supervised learning
A simple regression model and a classification model were trained on the cleaned dataset. The classification task performed well in separating high-traffic vs lower-traffic periods, while the regression model showed the limits of a simple linear model for this problem.

### Unsupervised learning
K-means clustering identified multiple traffic intensity groups. This helped show that the data contains distinct traffic conditions rather than a single uniform pattern.

### Explainability and recommendation
The explainability analysis identified time-based features as highly influential, especially the cyclical time encoding. This is consistent with commuter traffic patterns. A recommendation layer suggested lower-traffic travel windows and highlighted specific peak hours to avoid.

### Advanced AI / deep learning-like ensemble baseline
A stronger ensemble-based model improved prediction quality significantly compared with the basic linear model. This demonstrates that temporal and operational features are highly predictive when modeled appropriately.

## 7. Responsible AI and governance
The capstone also considers the responsible use of AI. The project acknowledges that:
- the model is for decision support rather than fully autonomous traffic control
- weather and time features may be incomplete proxies for other real-world causes of congestion
- bias risk may arise if the model is applied beyond the same setting or geography
- governance, transparency, and human review are important before deployment in real operational settings

## 8. MLOps and deployment simulation
A practical MLOps view of the project includes:
- model training and evaluation logs
- reproducible data pipeline steps
- model versioning and tracking concepts
- structured deployment notes
- monitoring suggestions for retraining and drift detection

This approach connects the project to a realistic AI system lifecycle beyond a one-off notebook analysis.

## 9. Final conclusion
The project demonstrates a coherent end-to-end data science and AI workflow using a real-world transportation dataset. It shows that traffic volume is shaped primarily by temporal patterns, with meaningful effects from weather conditions and occasional holiday variation. The final solution combines traditional analytics, reproducible Python pipelines, machine learning, explainability, and operational recommendations in a way that fits the course learning outcomes.

## 10. Submission notes
This capstone uses a connected workflow across all three parts and keeps the project reproducible and organised through:
- dataset-based analysis using the provided raw data
- Python data processing and feature engineering
- model development and evaluation
- clear documentation and logging
- a structured project folder layout

This final report should be used with the project files, outputs, and repository documentation as the final submission package.
