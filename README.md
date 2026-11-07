# Traffic Volume Forecasting and Pattern Analysis for Interstate 94

## Project overview
This capstone project analyses hourly traffic volume on westbound I-94 near Minneapolis–St Paul using weather, time, and holiday information. The project follows a connected end-to-end workflow across SQL analysis, descriptive statistics, probability, Python data preparation, machine learning, explainability, recommendation logic, and responsible AI.

## Business problem
Traffic congestion is strongly influenced by commuter behaviour, weather conditions, and occasional holiday effects. A deeper understanding of traffic patterns can support better planning, travel guidance, and operational decision-making.

## Dataset
The project uses the approved dataset provided for this capstone:

- data/raw/Metro_Interstate_Traffic_Volume.csv

The dataset contains hourly traffic records including:
- holiday
- temperature
- rain and snow depth
- cloud coverage
- weather condition
- date and time
- traffic volume

## Repository structure

- data/
  - raw/
- phase1/
  - README.md
  - sql/
  - python/
  - output/
- phase2/
  - README.md
  - python/
  - output/
- phase3/
  - README.md
  - python/
  - output/
- phase4/
  - README.md
  - python/
  - output/
- final/
  - capstone_final_report.md
  - responsible_ai_and_mlops.md
  - project_submission_checklist.md
- README.md
- requirements.txt

## Project phases

### Phase 1: SQL, statistics, probability, and dashboard foundations
- SQLite import and SQL analysis
- descriptive statistics and correlation
- probability and conditional probability
- dashboard-ready findings and visual narrative

### Phase 2: Data pipeline and feature engineering
- schema validation
- missing value and duplicate handling
- outlier checks
- feature engineering for modelling and analysis
- cleaned dataset generation

### Phase 3: Machine learning and AI models
- supervised learning for regression and classification
- unsupervised clustering
- model evaluation and interpretation
- practical performance review

### Phase 4: Explainability, recommendation, and advanced AI system design
- explainability and feature importance
- recommendation logic for lower-traffic travel windows
- advanced AI-style model evaluation
- responsible AI and MLOps framing

### Final integration
- final capstone report
- responsible AI and sustainability discussion
- deployment simulation notes
- final submission checklist

## Environment and setup
This project was completed using Python 3.12 with a minimal set of packages:

- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- sqlite-utils

## Execution flow
1. Place the raw dataset in the data/raw folder.
2. Run the project scripts in sequence by phase.
3. Review outputs under each phase folder.
4. Use the final folder for submission-ready material.

## Key findings
- Traffic volume follows strong time-of-day patterns.
- Weather conditions influence traffic intensity, especially during rain conditions.
- Time-based features are highly important for prediction and interpretation.
- A recommendation layer can suggest lower-congestion travel windows.
- The project demonstrates both analytical insight and practical AI decision support.

## Submission guidance
This repository is organised for grading and can be submitted as a public GitHub repository. If a private repository is used, ensure the evaluator has access before submission.

## Notes
- All analysis is based on the provided capstone dataset.
- The phases are intentionally connected so the project reads as one coherent capstone rather than separate assignments.
- All outputs are saved in their relevant phase folders to maintain reproducibility and traceability.
