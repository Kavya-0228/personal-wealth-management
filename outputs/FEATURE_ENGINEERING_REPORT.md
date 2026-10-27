# Feature Engineering Report
**Project**: An Intelligent Personal Wealth Management Dashboard  
**Engineered Dataset**: `data/personal_wealth_management_engineered.csv`  
**Total Records**: 1500  
**Total Features**: 28 (16 Original + 12 Engineered)  

---

## 1. Summary of New Features Created

| Feature Name | Type | Formula / Logic | Description |
| :--- | :---: | :--- | :--- |
| `savings_rate_calculated` | Numerical | `(monthly_savings / monthly_income) * 100` | Exact percentage of monthly income saved |
| `expense_ratio` | Numerical | `(monthly_expense / monthly_income) * 100` | Percentage of income spent on monthly expenses |
| `debt_to_income_calculated` | Numerical | `(debt / (monthly_income * 12)) * 100` | Ratio of total debt to annual income |
| `monthly_surplus` | Numerical | `monthly_income - monthly_expense` | Net unallocated cashflow available per month |
| `goal_gap` | Numerical | `max(0, financial_goal_amount - current_savings)` | Remaining target savings required |
| `emergency_fund_months` | Numerical | `current_savings / monthly_expense` | Number of months expenses covered by savings |
| `annual_savings` | Numerical | `monthly_savings * 12` | Total projected yearly savings |
| `annual_income` | Numerical | `monthly_income * 12` | Gross annual income |
| `savings_to_goal_ratio` | Numerical | `(current_savings / financial_goal_amount) * 100` | Percentage of target financial goal achieved |
| `savings_behavior` | Categorical | `<15%` (Low), `15-30%` (Moderate), `>30%` (Strong) | User saving behavior tier |
| `debt_burden_category` | Categorical | `<20%` (Low), `20-40%` (Moderate), `>40%` (High) | User debt leverage level |
| `emergency_fund_status` | Categorical | `<3 mos` (Weak), `3-6 mos` (Adequate), `>6 mos` (Strong) | Liquidity preparedness status |

---

## 2. Statistical Summary of Engineered Features

| Feature | Mean | Median | Min | Max | Std_Dev |
| --- | --- | --- | --- | --- | --- |
| savings_rate_calculated | 37.25 | 36.72 | 5.00 | 75.00 | 14.96 |
| expense_ratio | 63.13 | 63.14 | 25.00 | 298.13 | 17.76 |
| debt_to_income_calculated | 35.64 | 34.50 | 0.00 | 181.58 | 21.59 |
| monthly_surplus | 51323.27 | 44390.00 | -54854.00 | 181779.00 | 34786.80 |
| goal_gap | 719119.56 | 574088.50 | 0.00 | 2399821.00 | 692142.94 |
| emergency_fund_months | 10.04 | 7.61 | 0.00 | 73.27 | 8.83 |
| annual_savings | 614903.26 | 530886.00 | 12720.00 | 2181348.00 | 408803.49 |
| annual_income | 1638131.15 | 1666932.00 | 217956.00 | 2997708.00 | 797293.66 |
| savings_to_goal_ratio | 113.35 | 46.97 | 0.00 | 2552.95 | 213.56 |

---

## 3. Financial Behavior Category Distributions

### A. Savings Behavior (`savings_behavior`)
| Savings Behavior | Count | Percentage (%) |
| --- | --- | --- |
| Strong Saving | 1016 | 67.73 |
| Moderate Saving | 374 | 24.93 |
| Low Saving | 110 | 7.33 |

### B. Debt Burden Category (`debt_burden_category`)
| Debt Burden Category | Count | Percentage (%) |
| --- | --- | --- |
| High Debt | 635 | 42.33 |
| Moderate Debt | 474 | 31.60 |
| Low Debt | 391 | 26.07 |

### C. Emergency Fund Status (`emergency_fund_status`)
| Emergency Fund Status | Count | Percentage (%) |
| --- | --- | --- |
| Strong | 898 | 59.87 |
| Adequate | 333 | 22.20 |
| Weak | 269 | 17.93 |

---

## 4. Relationship & Correlation Analysis

| Feature_1 | Feature_2 | Pearson_Correlation |
| --- | --- | --- |
| savings_rate_calculated | financial_health_score | 0.80 |
| debt_to_income_calculated | financial_health_score | -0.40 |
| monthly_surplus | financial_health_score | 0.48 |
| emergency_fund_months | financial_health_score | 0.69 |
| goal_gap | goal_progress_percent | -0.86 |

---

## 5. Key Feature Engineering Insights

1. **Savings Rate as Primary Predictor**: `savings_rate_calculated` has an r = 0.7977 correlation with `financial_health_score`.
2. **Debt Leverage Impact**: `debt_to_income_calculated` correlates negatively (r = -0.4019) with financial health.
3. **Cashflow Surplus Buffer**: `monthly_surplus` averages $51,323.27 per user per month.
4. **Emergency Liquidity Cushion**: `emergency_fund_months` averages 10.04 months of expenses across all profiles.
5. **Capital Goal Gap**: Users have an average remaining `goal_gap` of $719,119.56.
6. **High Savings Propensity**: 67.7% of users fall into the 'Strong Saving' tier (>30% savings rate).
7. **Manageable Debt Burden**: 26.1% of users exhibit low debt to annual income ratio (<20%).
8. **Strong Liquidity Reserves**: 59.9% of users hold over 6 months of expenses in liquid savings.
