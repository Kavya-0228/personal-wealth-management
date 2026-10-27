import os
import sys
sys.path.insert(0, os.path.abspath("."))
import json
import joblib
import pandas as pd
import numpy as np
from app import compute_financial_health_score, compute_goal_feasibility

print("=== WEALTHSPHERE COMPREHENSIVE VALIDATION SUITE ===")

# PART 1: Project Structure Check
required_paths = [
    "data/personal_wealth_management_dataset.csv",
    "data/personal_wealth_management_engineered.csv",
    "model/best_model.joblib",
    "model/feature_columns.joblib",
    "model/model_metrics.json",
    "outputs/financial_health_goal_plots",
    "app.py",
    "train.py",
    "eda.py",
    "feature_engineering.py",
    "financial_health_goal_analysis.py",
    "requirements.txt"
]

structure_results = {}
for path in required_paths:
    exists = os.path.exists(path)
    structure_results[path] = "PASS" if exists else "FAIL"
    print(f"Path Check: {path:45s} -> {structure_results[path]}")

# PART 4: Model Integrity Check
model = joblib.load("model/best_model.joblib")
features = joblib.load("model/feature_columns.joblib")
with open("model/model_metrics.json", "r") as f:
    metrics_json = json.load(f)

print("\n--- MODEL INTEGRITY ---")
print(f"Model Type: {type(model).__name__}")
print(f"Features ({len(features)}): {features}")
print(f"Best Model: {metrics_json.get('best_model')}")
print(f"Accuracy: {metrics_json.get('metrics', {}).get('Accuracy', 0):.4f}")
print(f"Precision: {metrics_json.get('metrics', {}).get('Precision', 0):.4f}")
print(f"Recall: {metrics_json.get('metrics', {}).get('Recall', 0):.4f}")
print(f"F1-Score: {metrics_json.get('metrics', {}).get('F1 Score', 0):.4f}")

# PART 2: 5 Financial Profiles
profiles = {
    "Profile A (Financially Strong)": {
        'age': 38, 'income': 120000.0, 'expense': 40000.0, 'savings': 300000.0,
        'debt': 10000.0, 'goal': 500000.0, 'horizon': 5, 'risk_score': 70
    },
    "Profile B (Debt Heavy)": {
        'age': 29, 'income': 45000.0, 'expense': 40000.0, 'savings': 5000.0,
        'debt': 80000.0, 'goal': 200000.0, 'horizon': 3, 'risk_score': 30
    },
    "Profile C (Moderate Profile)": {
        'age': 35, 'income': 80000.0, 'expense': 45000.0, 'savings': 35000.0,
        'debt': 15000.0, 'goal': 200000.0, 'horizon': 10, 'risk_score': 50
    },
    "Profile D (High Income & Expense)": {
        'age': 45, 'income': 250000.0, 'expense': 200000.0, 'savings': 150000.0,
        'debt': 50000.0, 'goal': 1000000.0, 'horizon': 7, 'risk_score': 65
    },
    "Profile E (Goal Already Achieved)": {
        'age': 50, 'income': 90000.0, 'expense': 35000.0, 'savings': 600000.0,
        'debt': 5000.0, 'goal': 500000.0, 'horizon': 5, 'risk_score': 55
    }
}

print("\n--- 5 PROFILE TESTS ---")
for name, p in profiles.items():
    surplus = p['income'] - p['expense']
    score, cat, comps, mets = compute_financial_health_score(
        p['income'], p['expense'], surplus, p['savings'], p['debt'], p['goal'], p['horizon']
    )
    g_info = compute_goal_feasibility(p['savings'], p['goal'], p['horizon'], surplus, mets['goal_progress_pct'])
    
    in_df = pd.DataFrame([{
        'age': p['age'], 'monthly_income': p['income'], 'monthly_expense': p['expense'],
        'monthly_savings': surplus, 'current_savings': p['savings'], 'debt': p['debt'],
        'financial_goal_amount': p['goal'], 'investment_horizon_years': p['horizon'],
        'risk_tolerance_score': p['risk_score']
    }])[features]
    pred = model.predict(in_df)[0]
    probs = model.predict_proba(in_df)[0]
    conf = max(probs) * 100.0
    print(f"{name:35s} | Score: {score:5.1f} ({cat:16s}) | Goal: {g_info['feasibility_status']:15s} | Risk: {pred} ({conf:4.1f}%)")

# PART 3: Edge Case Testing
edge_cases = {
    "Income = 0": (0.0, 30000.0, -30000.0, 50000.0, 10000.0, 200000.0, 5),
    "Expense = 0": (50000.0, 0.0, 50000.0, 100000.0, 0.0, 200000.0, 5),
    "Savings = 0": (60000.0, 35000.0, 25000.0, 0.0, 10000.0, 200000.0, 5),
    "Debt = 0": (70000.0, 30000.0, 40000.0, 80000.0, 0.0, 200000.0, 5),
    "Goal = 0": (60000.0, 30000.0, 30000.0, 50000.0, 5000.0, 0.0, 5),
    "Horizon = 0": (60000.0, 30000.0, 30000.0, 50000.0, 5000.0, 200000.0, 0),
    "Very High Debt (1M)": (50000.0, 40000.0, 10000.0, 10000.0, 1000000.0, 200000.0, 5),
    "Negative Surplus": (40000.0, 55000.0, -15000.0, 20000.0, 10000.0, 200000.0, 5),
    "Goal Already Reached": (80000.0, 30000.0, 50000.0, 300000.0, 0.0, 200000.0, 5)
}

print("\n--- EDGE CASE TESTING ---")
edge_passed = True
for c_name, (inc, exp, surp, sav, dbt, gol, hor) in edge_cases.items():
    try:
        sc, ct, cp, mt = compute_financial_health_score(inc, exp, surp, sav, dbt, gol, hor)
        gi = compute_goal_feasibility(sav, gol, hor, surp, mt['goal_progress_pct'])
        assert not np.isnan(sc), "Score is NaN"
        assert not np.isnan(gi['required_monthly_saving']), "Required monthly is NaN"
        print(f"Edge Case: {c_name:25s} -> PASS (Score: {sc:.1f}, Goal: {gi['feasibility_status']})")
    except Exception as e:
        print(f"Edge Case: {c_name:25s} -> FAIL ({e})")
        edge_passed = False

# PART 5: Mathematical Independent Verification
print("\n--- INDEPENDENT CALCULATION VALIDATION ---")
# Case benchmark: Income 80,000, Expense 45,000, Savings 35,000, Debt 15,000, Goal 200,000, Horizon 10
inc, exp, sav, dbt, gol, hor = 80000.0, 45000.0, 35000.0, 15000.0, 200000.0, 10.0
surp = inc - exp

# Manual reference formulas
m_savings_rate = (surp / inc) * 100.0 # 43.75%
m_expense_ratio = (exp / inc) * 100.0 # 56.25%
m_dti = (dbt / (inc * 12.0)) * 100.0 # 1.5625%
m_monthly_surplus = surp # 35,000
m_ef_months = sav / exp # 0.7777 mos
m_goal_progress_pct = (sav / gol) * 100.0 # 17.5%

m_sav_comp = min(m_savings_rate * 2.0, 100.0) # 87.5
m_debt_comp = max(100.0 - m_dti, 0.0) # 98.4375
m_ef_comp = min((m_ef_months / 6.0) * 100.0, 100.0) # 12.9629
m_exp_comp = max((100.0 - m_expense_ratio) * (100.0 / 70.0), 0.0) # 62.5
m_surplus_comp = min((surp / inc) * 200.0, 100.0) # 87.5
m_goal_comp = min(m_goal_progress_pct, 100.0) # 17.5

m_calc_score = round(
    m_sav_comp * 0.25 + m_debt_comp * 0.20 + m_ef_comp * 0.20 +
    m_exp_comp * 0.15 + m_surplus_comp * 0.10 + m_goal_comp * 0.10, 1
)

m_goal_remaining = gol - sav # 165,000
m_req_monthly = m_goal_remaining / (hor * 12.0) # 1375
m_saving_gap = max(0.0, m_req_monthly - surp) # 0.0

app_sc, app_ct, app_cp, app_mt = compute_financial_health_score(inc, exp, surp, sav, dbt, gol, hor)
app_gi = compute_goal_feasibility(sav, gol, hor, surp, app_mt['goal_progress_pct'])

calc_checks = [
    ("savings_rate_calculated", abs(app_mt['savings_rate_pct'] - m_savings_rate) < 0.01),
    ("expense_ratio", abs(app_mt['expense_ratio_pct'] - m_expense_ratio) < 0.01),
    ("debt_to_income_calculated", abs(app_mt['dti_pct'] - m_dti) < 0.01),
    ("monthly_surplus", abs(app_mt['monthly_surplus'] - m_monthly_surplus) < 0.01),
    ("emergency_fund_months", abs(app_mt['ef_months'] - m_ef_months) < 0.01),
    ("goal_progress_percent", abs(app_mt['goal_progress_pct'] - m_goal_progress_pct) < 0.01),
    ("calculated_financial_health_score", abs(app_sc - m_calc_score) < 0.2),
    ("goal_remaining_amount", abs(app_gi['goal_remaining'] - m_goal_remaining) < 0.01),
    ("required_monthly_saving_no_growth", abs(app_gi['required_monthly_saving'] - m_req_monthly) < 0.01),
    ("monthly_saving_gap", abs(app_gi['monthly_saving_gap'] - m_saving_gap) < 0.01),
    ("goal_achievement_status", app_gi['achievement_status'] in ["On Track", "Needs Attention", "Goal Accomplished"]),
    ("goal_feasibility_status", app_gi['feasibility_status'] in ["On Track", "Needs Higher Monthly Saving", "Already Achieved"])
]

for metric_name, is_pass in calc_checks:
    print(f"Calc Check: {metric_name:35s} -> {'PASS' if is_pass else 'FAIL'}")

# PART 9: Generate demo_profiles.csv
demo_df = pd.DataFrame([
    {
        "Profile_ID": "DEMO-01",
        "Profile_Name": "Financially Strong",
        "Archetype": "High Saver & Conservative",
        "Age": 38,
        "Monthly_Income": 120000,
        "Monthly_Expense": 40000,
        "Current_Savings": 300000,
        "Debt": 10000,
        "Financial_Goal": 500000,
        "Horizon_Years": 5,
        "Risk_Score": 70,
        "Target_Health_Category": "Good",
        "Description": "High savings rate (>60%), low leverage, and well-funded emergency cushion."
    },
    {
        "Profile_ID": "DEMO-02",
        "Profile_Name": "Debt Heavy",
        "Archetype": "High Leverage & Vulnerable",
        "Age": 29,
        "Monthly_Income": 45000,
        "Monthly_Expense": 40000,
        "Current_Savings": 5000,
        "Debt": 80000,
        "Financial_Goal": 200000,
        "Horizon_Years": 3,
        "Risk_Score": 30,
        "Target_Health_Category": "Needs Improvement",
        "Description": "Constrained cash flow, negative liquidity cushion, and elevated debt burden."
    },
    {
        "Profile_ID": "DEMO-03",
        "Profile_Name": "Goal Focused",
        "Archetype": "Aggressive Capital Accumulator",
        "Age": 32,
        "Monthly_Income": 95000,
        "Monthly_Expense": 42000,
        "Current_Savings": 120000,
        "Debt": 18000,
        "Financial_Goal": 400000,
        "Horizon_Years": 4,
        "Risk_Score": 60,
        "Target_Health_Category": "Good",
        "Description": "Disciplined saver allocating >50% surplus towards a specific capital purchase."
    },
    {
        "Profile_ID": "DEMO-04",
        "Profile_Name": "Moderate Investor",
        "Archetype": "Balanced Mainstream Earner",
        "Age": 35,
        "Monthly_Income": 80000,
        "Monthly_Expense": 45000,
        "Current_Savings": 35000,
        "Debt": 15000,
        "Financial_Goal": 200000,
        "Horizon_Years": 10,
        "Risk_Score": 50,
        "Target_Health_Category": "Moderate",
        "Description": "Standard fintech user baseline with moderate health and stable cash flow."
    },
    {
        "Profile_ID": "DEMO-05",
        "Profile_Name": "Early Saver",
        "Archetype": "Young Career Starter",
        "Age": 24,
        "Monthly_Income": 38000,
        "Monthly_Expense": 26000,
        "Current_Savings": 15000,
        "Debt": 0,
        "Financial_Goal": 150000,
        "Horizon_Years": 5,
        "Risk_Score": 45,
        "Target_Health_Category": "Moderate",
        "Description": "Entry-level professional with zero debt, developing systematic savings habits."
    }
])

demo_csv_path = os.path.join("outputs", "demo_profiles.csv")
demo_df.to_csv(demo_csv_path, index=False)
print(f"\n[PART 9] demo_profiles.csv written to {demo_csv_path} with {len(demo_df)} profiles.")
