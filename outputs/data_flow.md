# Data Flow Architecture & Pipeline Movement
## WealthSphere: End-to-End Data Pipeline Specification

This document details the movement of data throughout the WealthSphere platform, tracing how raw financial data transitions from ingestion to machine learning inference, diagnostic scoring, and front-end interaction.

---

## 1. Data Flow Diagram (DFD Level 1)

```
[ Raw Financial Profile ]
          │
          ▼
[ STEP 1: Preprocessing & Validation ]
   • Guard against division-by-zero (max(1, expense))
   • Ensure non-negative bounds
          │
          ▼
[ STEP 2: Feature Engineering Engine ]
   • savings_rate_calculated = (surplus / income) * 100
   • debt_to_income_calculated = (debt / (income * 12)) * 100
   • emergency_fund_months = current_savings / expense
   • expense_ratio = (expense / income) * 100
   • monthly_surplus = max(0, income - expense)
   • goal_progress_percent = (savings / goal) * 100
          │
          ├──────────────────────────┬──────────────────────────┐
          ▼                          ▼                          ▼
[ STEP 3: ML Risk Model ]  [ STEP 4: Scoring Engine ]  [ STEP 5: Goal Engine ]
 • Load best_model.joblib   • Savings Rate (25%)       • Remaining Shortfall
 • 9-feature vector input   • Debt Burden (20%)        • Required Monthly
 • Inference & Proba        • Emergency Fund (20%)     • Monthly Deficit Gap
 • Low / Mod / High         • Expense Ratio (15%)      • Feasibility Status
 • Confidence %             • Monthly Surplus (10%)    • Milestone Progress
                            • Goal Progress (10%)
                            • Health Category
          │                          │                          │
          └──────────────────────────┼──────────────────────────┘
                                     ▼
                     [ STEP 6: AI Insights Engine ]
                      • Identify strongest pillar
                      • Identify primary watchout
                      • Quantify next best action
                                     ▼
                [ STEP 7: What-If Simulation Sandbox ]
                 • Accepts real-time parameter changes
                 • Recomputes Steps 2–6 in-memory
                 • Renders Before vs After comparison
                                     ▼
             [ STEP 8: Visualization & Presentation Layer ]
              • 4 Top KPI Cards
              • Radial SVG Donut Gauge Chart
              • Milestone Journey Track
              • Interactive Plotly Cohort Curves
              • Executive Streamlit Interface
```

---

## 2. Pipeline Stage Details

### Stage 1: Ingestion & Input Normalization
* **Inputs**: Inflow amounts, outflow amounts, existing asset base, liabilities, target milestone amount, and investment time window.
* **Safeguards**: Employs mathematical floors: `safe_expense = max(1.0, expense)` to prevent division-by-zero during emergency coverage calculation; `safe_horizon = max(0.08, horizon)` to prevent division-by-zero during run-rate calculation.

### Stage 2: Feature Transformation
* Raw values are mapped into normalized financial ratios that eliminate scaling discrepancies between high-income earners and early-career savers.
* Features match the structure stored in `model/feature_columns.joblib`.

### Stage 3: Supervised Classification (ML Pipeline)
* The input vector passes through the serialized `scikit-learn` pipeline:
  1. `SimpleImputer(strategy='median')`: Ensures missing fields are imputed consistently with training medians.
  2. `StandardScaler()`: Standardizes features to zero mean and unit variance.
  3. `LogisticRegression()`: Computes multi-class log-odds and outputs calibrated posterior probabilities `predict_proba()`.

### Stage 4: Financial Health Scoring
* Transforms domain metrics into 0–100 sub-scores using piecewise continuous normalization.
* Computes the linear composite score:
  $$\text{Score} = 0.25(\text{Savings}) + 0.20(\text{Debt}) + 0.20(\text{Emergency}) + 0.15(\text{Expense}) + 0.10(\text{Surplus}) + 0.10(\text{Goal})$$

### Stage 5: Goal Accumulation Modeling
* Evaluates dynamic monthly contribution requirements without assumed compounding to present conservative accumulation velocity.
* Compares current monthly surplus against required monthly savings to assign explicit feasibility classifications.

### Stage 6: Visualization & UI State Synchronization
* Streamlit maintains session state (`st.session_state`). When a user triggers "Analyze Profile" or adjusts What-If sliders, Streamlit executes a reactive rerun, refreshing all visual components in $< 100$ milliseconds.
