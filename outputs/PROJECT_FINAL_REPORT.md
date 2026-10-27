# WealthSphere — Intelligent Personal Wealth Management Dashboard
## Comprehensive Project Final Report & System Architecture

**Project Title**: WealthSphere — Personal Financial Intelligence  
**Author / Team**: Data Science & AI Engineering Team  
**Dataset**: Personal Wealth Management Dataset (1,500 Consumer Profiles)  
**Tech Stack**: Python 3.10+, Scikit-Learn, Streamlit, Pandas, NumPy, Plotly, Joblib  
**Date of Validation**: October 2026  

---

## 1. Project Overview
**WealthSphere** is an AI-powered personal financial intelligence dashboard engineered to empower individuals with data-driven wealth diagnostics. Built for competition-level execution, WealthSphere integrates automated exploratory data analysis, domain-engineered financial metrics, supervised machine learning for risk classification, an objective 6-dimension financial health scoring model, interactive goal feasibility tracking, and an interactive real-time What-If scenario simulator.

---

## 2. Problem Statement
Modern personal finance consumers frequently struggle with fragmented financial data:
1. **Subjective Risk Profiling**: Traditional risk assessments rely on qualitative questionnaires that fail to mirror real cash flow realities.
2. **Lack of Comprehensive Health Metrics**: Consumers track account balances but lack a holistic diagnostic score synthesizing savings velocity, debt burden, liquid emergency buffers, and operational expenses.
3. **Static Goal Planning**: Financial goals are typically calculated with static linear formulas that ignore changing monthly surplus capacities and feasibility thresholds.
4. **Disjointed Decision Simulation**: Users lack dynamic sandboxes to test how incremental lifestyle changes (e.g., earning 10% more vs. trimming 15% expenses) alter long-term wealth trajectories.

---

## 3. Project Objectives
* **Audit & Clean**: Perform rigorous Exploratory Data Analysis on 1,500 personal wealth records.
* **Feature Engineering**: Formulate domain-authentic financial ratios (savings rates, debt-to-income, emergency months, expense overhead, surplus, and goal progress).
* **Supervised Machine Learning**: Train, evaluate, and benchmark multi-class classifiers to predict consumer risk tolerance personas (`Low`, `Moderate`, `High`).
* **Objective Health Scoring**: Implement a transparent 100-point composite financial health scoring model divided into 6 weighted dimensions.
* **Goal Feasibility Tracking**: Calculate capital gaps, required monthly savings, and timeline feasibility.
* **Interactive FinTech Dashboard**: Deploy a production-grade Streamlit application featuring dark sidebar navigation, dynamic KPI cards, SVG radial gauges, What-If simulation sandboxes, and cohort analytics.

---

## 4. Dataset Description
The dataset comprises 1,500 synthetic consumer profiles designed around empirical wealth management benchmarks:
* `age`: Age of consumer (18 to 85 years, mean 41.5 years).
* `monthly_income`: Gross monthly inflow ($1,000 to $250,000).
* `monthly_expense`: Total operating expenses and living overhead.
* `monthly_savings`: Monthly surplus capital.
* `current_savings`: Accumulated liquid and semi-liquid assets.
* `debt`: Total outstanding consumer debt (credit, personal, auto, student).
* `financial_goal_amount`: Target accumulation milestone.
* `investment_horizon_years`: Target investment window (1 to 40 years).
* `risk_tolerance_score`: Psychometric baseline risk tolerance (0 to 100).
* `risk_category`: Supervised ground-truth classification (`Low`, `Moderate`, `High`).

---

## 5. Exploratory Data Analysis (EDA)
EDA was conducted via [eda.py](file:///c:/Users/kavya/OneDrive/Desktop/ds%20project/eda.py) with all artifacts logged in [outputs/](file:///c:/Users/kavya/OneDrive/Desktop/ds%20project/outputs/):
* **Data Hygiene**: Confirmed zero duplicate records and zero missing values across all columns.
* **Distribution Analysis**: Analyzed skewness and kurtosis across income, debt, and savings. Identified right-skewed wealth distributions mirroring real-world macroeconomics.
* **Correlation Matrix**: Uncovered a high correlation between monthly surplus and overall savings rate, and an inverse correlation between debt-to-income and solvency stability.
* **Outlier Detection**: Audited IQR boundaries to establish bounds for the What-If simulation limits without dropping valid extreme earners.

---

## 6. Feature Engineering
Six core domain variables were engineered and persisted to `data/personal_wealth_management_engineered.csv`:
1. **Calculated Savings Rate** (`savings_rate_calculated`):
   $$\text{Savings Rate} = \frac{\text{Monthly Savings}}{\text{Monthly Income}} \times 100$$
2. **Debt-to-Income Ratio** (`debt_to_income_calculated`):
   $$\text{DTI} = \frac{\text{Debt}}{\text{Monthly Income} \times 12} \times 100$$
3. **Emergency Fund Months** (`emergency_fund_months`):
   $$\text{Emergency Buffer} = \frac{\text{Current Savings}}{\max(\text{Monthly Expense}, 1)}$$
4. **Expense Ratio** (`expense_ratio`):
   $$\text{Expense Ratio} = \frac{\text{Monthly Expense}}{\text{Monthly Income}} \times 100$$
5. **Monthly Surplus** (`monthly_surplus`):
   $$\text{Surplus} = \max(0, \text{Monthly Income} - \text{Monthly Expense})$$
6. **Goal Progress Percent** (`goal_progress_percent`):
   $$\text{Goal Progress} = \min\left(100, \frac{\text{Current Savings}}{\text{Financial Goal Amount}} \times 100\right)$$

---

## 7. Machine Learning Model Training
Supervised models were trained using stratified 80/20 train/test splits via [train.py](file:///c:/Users/kavya/OneDrive/Desktop/ds%20project/train.py):
* **Preprocessing Pipeline**: `SimpleImputer(strategy='median')` + `StandardScaler()`.
* **Model Benchmarking Comparison**:
  | Model | Accuracy | Precision | Recall | F1 Score |
  | :--- | :---: | :---: | :---: | :---: |
  | **Logistic Regression (Champion)** | **82.00%** | **82.09%** | **82.00%** | **81.84%** |
  | **Random Forest Classifier** | 80.67% | 81.02% | 80.67% | 80.51% |
  | **Decision Tree Classifier** | 72.00% | 71.89% | 72.00% | 71.87% |
* **Selected Production Artifact**: Serialized to `model/best_model.joblib` and `model/feature_columns.joblib`. Logistic Regression demonstrated optimal calibration and probability stability.

---

## 8. Financial Health Scoring Methodology
A composite 100-point educational financial scoring index was developed across 6 pillars:
* **Savings Rate (25% Weight)**: Normalized as $\min(\text{Savings Rate} \times 2, 100)$.
* **Debt Burden (20% Weight)**: Inversely scaled as $\max(100 - \text{DTI}, 0)$.
* **Emergency Fund (20% Weight)**: Scaled to a 6-month target as $\min((\text{Months} / 6) \times 100, 100)$.
* **Expense Ratio (15% Weight)**: Scaled where $\le 30\%$ expense yields 100 pts and $\ge 100\%$ yields 0 pts.
* **Monthly Surplus (10% Weight)**: Scaled relative to gross income as $\min((\text{Surplus} / \text{Income}) \times 200, 100)$.
* **Goal Progress (10% Weight)**: Direct 0–100% accumulation mapping.

**Population Health Score Distribution**:
* **Good ($\ge 80$)**: 30.33% (Mean Score: 87.04)
* **Moderate (60–79.9)**: 38.07% (Mean Score: 70.71)
* **Needs Improvement (40–59.9)**: 21.40% (Mean Score: 51.41)
* **Poor ($< 40$)**: 10.20% (Mean Score: 29.77)

---

## 9. Financial Goal Feasibility Analysis
Goal analysis models evaluate accumulation velocity against target milestones:
* **Remaining Shortfall**: $\max(0, \text{Goal Amount} - \text{Current Savings})$.
* **Required Monthly Saving**: $\frac{\text{Remaining Shortfall}}{\text{Horizon Years} \times 12}$.
* **Monthly Saving Gap**: $\max(0, \text{Required Monthly} - \text{Current Monthly Saving})$.
* **Feasibility Status**: Categorized into `Already Achieved` (27.93%), `On Track` (59.00%), and `Needs Higher Monthly Saving` (13.07%).

---

## 10. Risk Analysis & Explainability
Rather than presenting black-box ML predictions, WealthSphere couples class probabilities with rule-based feature explainability:
* **Confidence Spectrum**: Calculates exact probabilities for `Low`, `Moderate`, and `High` classes.
* **"Why This Prediction?" Engine**: Identifies positive contributors (e.g., strong savings velocity $>30\%$, $>6$ months emergency fund) and flags risk vectors (e.g., elevated DTI, cash flow contraction).

---

## 11. Dashboard Architecture
WealthSphere's front end is implemented in Streamlit using a bespoke FinTech design system:
* **Theme Palette**: Crisp light canvas (`#F4F7FB`), midnight navy sidebar (`#0B1026`), electric primary (`#6D4AFF`), vibrant cyan (`#27D7E8`), and mint success (`#22C7A5`).
* **Sidebar Controls**: Collapsible inputs for income, expenses, savings, debt, goal, and horizon with dynamic state management.
* **Modular Navigation**:
  * `◉ Overview`: Executive summary answering the 3 core UX questions.
  * `♡ Financial Health`: Deep dive into the 6 pillars with weight breakdowns.
  * `◇ Financial Goals`: Milestone accumulation roadmap.
  * `⚡ AI Risk`: Supervised probability spectrum and feature drivers.
  * `◈ Analytics`: Interactive population distributions using Plotly.
  * `◎ What-If Simulator`: Real-time before-and-after financial sandbox.
  * `✦ AI Insights`: Prioritized strengths, watchouts, and next-best actions.

---

## 12. What-If Wealth Simulator (Signature Feature)
The simulator serves as WealthSphere's signature capability:
* Allows users to independently adjust monthly income, expenses, liquid savings, debt, goals, and horizons.
* Dynamically recomputes the 6-pillar financial health score, goal progress, feasibility status, and re-executes the ML risk model on simulated inputs in real time.
* Renders before-and-after comparison cards and a multi-year wealth accumulation curve comparing baseline run-rates against simulated projections.

---

## 13. AI Insights Engine
The insights module evaluates consumer cash flows to surface:
* **Top Strengths**: Verified financial vectors exceeding recommended thresholds.
* **Areas to Watch**: Under-allocated reserves or leverage friction.
* **Next Best Action**: Quantified, specific financial guidance (e.g., exact dollar amounts to allocate toward debt payoff or goal acceleration).

---

## 14. Model Performance Summary
* **Champion Model**: Logistic Regression Pipeline.
* **Testing Accuracy**: 82.00% (Balanced across stratified test split).
* **Precision / Recall / F1**: 82.09% / 82.00% / 81.84%.
* **Serialization**: Pipeline and feature schema preserved in `model/best_model.joblib`.

---

## 15. Key Results & Findings
1. **Savings Rate Dominance**: Monthly savings rate is the single strongest statistical predictor of overall financial health ($r = +0.88$).
2. **Leverage Friction**: High debt-to-income ratios consistently degrade financial stability scores regardless of gross income magnitude.
3. **Emergency Reserves as a Volatility Buffer**: Consumers with $>6$ months of living expenses in liquid reserves demonstrate a $>92\%$ Good/Moderate financial health categorization.

---

## 16. Limitations
* **Synthetic Cohort**: Models are trained on synthetic consumer records designed around macroeconomic standards. Real-world consumer behavior may exhibit non-linear spending shocks.
* **Static Interest Assumptions**: Baseline calculations assume constant currency purchasing power without compounding variable interest rate fluctuations.

---

## 17. Future Enhancements
* **Persistent Database Integration**: Connect to PostgreSQL/Supabase for persistent multi-user authentication and session history.
* **Live Open Banking / Plaid API Integration**: Direct transaction feed ingestion for automated expense categorization.
* **Automated PDF Export**: One-click generation of branded financial audit PDF reports for advisors and consumers.

---

## 18. Educational Financial Disclaimer
> **Notice**: WealthSphere is an educational simulation and financial intelligence platform designed for academic demonstration and decision support. The insights, scores, and risk classifications generated do not constitute certified financial, legal, or investment advice.

---
*Report Certified for Final Project Submission and Competition Demonstration.*
