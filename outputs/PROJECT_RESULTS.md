# WealthSphere — Validated Empirical Project Results
## Official Verification and Empirical Benchmark Data

All results detailed in this report represent verified, reproducible outputs generated directly by the platform's analytical scripts ([train.py](file:///c:/Users/kavya/OneDrive/Desktop/ds%20project/train.py), [financial_health_goal_analysis.py](file:///c:/Users/kavya/OneDrive/Desktop/ds%20project/financial_health_goal_analysis.py), and `test_validation.py`).

---

## 1. Machine Learning Benchmark Results

Supervised multi-class classification predicting consumer risk tolerance (`Low`, `Moderate`, `High`) across stratified 80/20 train/test splits (1,200 training records, 300 testing records):

| Model Architecture | Accuracy | Precision (Weighted) | Recall (Weighted) | F1 Score (Weighted) | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression Pipeline** | **82.00%** | **82.09%** | **82.00%** | **81.84%** | **Champion Model (Deployed)** |
| **Random Forest Classifier** | 80.67% | 81.02% | 80.67% | 80.51% | Benchmark Comparison |
| **Decision Tree Classifier** | 72.00% | 71.89% | 72.00% | 71.87% | Baseline Comparison |

### Deployed Model Pipeline Specification:
* **Preprocessing**: `SimpleImputer(strategy='median')` followed by `StandardScaler()`.
* **Classifier**: `LogisticRegression(multi_class='auto', max_iter=1000, random_state=42)`.
* **Serialization**: Exported to `model/best_model.joblib` (2,657 bytes) and `model/feature_columns.joblib` (174 bytes).

---

## 2. Comprehensive Test Suite Validation

| Test Suite Category | Total Tests | Passed | Failed | Verification Status |
| :--- | :---: | :---: | :---: | :---: |
| **System Structure & Artifacts** | 12 | 12 | 0 | **100% PASS** |
| **Mathematical Formulas (Calculations)** | 12 | 12 | 0 | **100% PASS** |
| **Edge-Case Fault Tolerance** | 9 | 9 | 0 | **100% PASS** |
| **Demo Profile Archetypes** | 5 | 5 | 0 | **100% PASS** |
| **Total Automated Tests** | **38** | **38** | **0** | **100% PASS** |

---

## 3. Financial Health Score Cohort Distribution (1,500 Records)

Derived from the 100-point composite scoring model across the engineered dataset:

| Health Category | Score Range | Population Count | Cohort % | Mean Score | Median Score |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Good** | 80.0 – 100.0 | 455 | 30.33% | 87.04 | 86.68 |
| **Moderate** | 60.0 – 79.9 | 571 | 38.07% | 70.71 | 71.01 |
| **Needs Improvement** | 40.0 – 59.9 | 321 | 21.40% | 51.41 | 51.67 |
| **Poor** | 0.0 – 39.9 | 153 | 10.20% | 29.77 | 30.24 |
| **Overall Cohort** | **0.0 – 100.0** | **1,500** | **100.0%** | **67.36** | **70.72** |

---

## 4. Financial Goal Feasibility Distribution (1,500 Records)

Evaluation of capital accumulation velocity against target milestones:

| Feasibility Classification | Definition Criteria | Record Count | Percentage (%) |
| :--- | :--- | :---: | :---: |
| **Already Achieved** | Current Savings $\ge$ Goal Amount | 419 | 27.93% |
| **On Track** | Monthly Surplus $\ge$ Required Monthly Saving | 885 | 59.00% |
| **Needs Higher Monthly Saving** | Monthly Surplus $<$ Required Monthly Saving | 196 | 13.07% |

*Average Cohort Goal Amount*: $1,264,552.16  
*Average Current Savings*: $716,115.49  
*Average Goal Progress*: 54.36%  
*Average Required Monthly Contribution*: $11,457.47  

---

## 5. Statistical Correlations & Feature Drivers

* **Savings Rate Dominance**: $r = +0.88$ correlation with overall financial health categorization across all demographic segments.
* **Debt Leverage Drag**: $r = -0.42$ negative correlation between debt-to-income and solvency score.
* **Emergency Reserve Resilience**: Consumers maintaining $\ge 6$ months of living expenses in liquid accounts demonstrated a $92.4\%$ Good/Moderate health rating.
