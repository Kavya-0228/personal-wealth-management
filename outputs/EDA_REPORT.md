# Comprehensive Exploratory Data Analysis (EDA) Report
**Project Name**: An Intelligent Personal Wealth Management Dashboard  
**Dataset**: `personal_wealth_management_dataset.csv`  
**Total Records**: 1500  
**Total Columns**: 16  

---

## 1. Dataset Overview
The dataset contains 1,500 individual financial user profiles designed to train and evaluate wealth management models.

- **Total Rows**: 1500
- **Total Features**: 15 features + 1 Target (`risk_category`)
- **Key Numeric Fields**: `age`, `monthly_income`, `monthly_expense`, `monthly_savings`, `current_savings`, `debt`, `financial_goal_amount`, `investment_horizon_years`, `risk_tolerance_score`
- **Key Derived Ratios**: `savings_rate_percent`, `debt_to_income_percent`, `goal_progress_percent`, `financial_health_score`
- **Key Categorical Targets**: `financial_health_category`, `risk_category`

---

## 2. Data Quality & Integrity Analysis
- **Duplicate Records**: 0 duplicates found.
- **Missing Values Summary**:
  - `monthly_expense`: 22 missing values (1.47%)
  - `current_savings`: 22 missing values (1.47%)
  - `debt`: 22 missing values (1.47%)
  - `risk_tolerance_score`: 22 missing values (1.47%)
  - All missing numerical values are cleanly handled via median imputation during pipeline processing without deleting valid user rows.
- **Range & Validity**: All monetary and percentage fields are non-negative and strictly bounded within valid economic ranges (no invalid or corrupt entries found).

---

## 3. Univariate Analysis Findings

### Numerical Distributions
- **Age**: Ranges from 18 to 60 years (Mean: 39.2 years).
- **Monthly Income**: Mean of $136,510.93 (Range: $18,163.00 to $249,809.00).
- **Monthly Expense**: Mean of $85,227.07.
- **Monthly Savings**: Mean of $51,241.94.
- **Debt**: Mean of $578,199.55.
- **Risk Tolerance Score**: Mean of 61.28 (out of 10).

### Categorical Distributions
- **`risk_category`**:
  - Moderate: 776 users (51.7%)
  - High: 528 users (35.2%)
  - Low: 196 users (13.1%)
- **`financial_health_category`**:
  - Moderate: High density
  - Poor / Needs Improvement: Distributed across low savings rate & high DTI profiles

---

## 4. Correlation Findings

### Top Strongest Positive Correlations
1. `savings_rate_percent` & `financial_health_score`: **r = 0.7977**
2. `monthly_income` & `monthly_savings`: **r = 0.7621**
3. `monthly_income` & `monthly_expense`: **r = 0.8775**
4. `current_savings` & `goal_progress_percent`: **r = 0.7042**

### Top Strongest Negative Correlations
1. `debt_to_income_percent` & `financial_health_score`: **r = -0.4200**
2. `monthly_expense` & `financial_health_score`: **r = -0.3174**

---

## 5. Risk Category Analysis
- **Low Risk Users**: Characterized by low risk tolerance scores (Mean: 37.84), shorter investment horizons, and lower income volatility.
- **Moderate Risk Users**: Balanced risk tolerance scores (Mean: 57.31) with steady savings and medium horizon.
- **High Risk Users**: High risk tolerance scores (Mean: 75.83), higher average income ($139,502.66), and longer investment horizons.

---

## 6. Financial Health Analysis
Financial health score is heavily governed by two core derived ratios:
1. **Positive Driver**: `savings_rate_percent` (+)
2. **Negative Driver**: `debt_to_income_percent` (-)

Users with high savings rates consistently achieve high financial health scores regardless of total income magnitude, demonstrating that relative savings behavior is more impactful than absolute earnings.

---

## 7. Outlier Analysis (IQR Method)
Using $1.5 \times IQR$:
- `monthly_income`: 0 outliers
- `monthly_expense`: 0 outliers
- `monthly_savings`: 12 outliers
- `current_savings`: 42 outliers
- `debt`: 35 outliers
- `financial_goal_amount`: 0 outliers

All data points were retained as they reflect valid financial variations across user cohorts.

---

## 8. Key Business & Data Insights

1. **Risk Tolerance Score as Primary Classifier**: Risk tolerance score exhibits the strongest association with `risk_category` classification.
2. **Income & Savings Linear Relationship**: Higher income directly facilitates greater absolute savings, though expense growth (lifestyle inflation) tracks income closely.
3. **Debt-to-Income Impact**: High DTI ratio is the single greatest detriment to a user's financial health score.
4. **Savings Rate Primacy**: High savings rate % is more strongly correlated with financial health than raw monthly income.
5. **Investment Horizon Dynamics**: Longer investment horizons align with higher risk acceptance.
6. **Goal Progress Tracking**: Accumulated current savings is the key driver of goal progress percentage.
7. **Clean Data Distribution**: Low outlier rate confirms the dataset is clean and well-structured for machine learning models.
8. **Imputation Integrity**: Imputing 22 missing values via median preserves full dataset volume (1,500 samples) without introducing bias.
