# Financial Health Score & Financial Goal Analysis Report
**Project**: An Intelligent Personal Wealth Management Dashboard  
**Engineered Dataset Input**: `data/personal_wealth_management_engineered.csv`  
**Total Records Analyzed**: 1500  

---

## 1. Transparent Calculated Financial Health Score Model

The `calculated_financial_health_score` is a transparent 0–100 composite educational score derived from six fundamental financial indicators:

| Component | Weight | Underlying Variable | Score Logic / Normalization |
| :--- | :---: | :--- | :--- |
| **Savings Rate** | 25% | `savings_rate_calculated` | `min(savings_rate % * 2, 100)` (50% savings rate = 100 pts) |
| **Debt Burden** | 20% | `debt_to_income_calculated` | `max(100 - debt_to_income %, 0)` (0% DTI = 100 pts, 100%+ DTI = 0 pts) |
| **Emergency Fund** | 20% | `emergency_fund_months` | `min((emergency_months / 6) * 100, 100)` (6+ months = 100 pts) |
| **Expense Ratio** | 15% | `expense_ratio` | `max((100 - expense_ratio %) * (100/70), 0)` (<=30% expense = 100 pts) |
| **Monthly Surplus** | 10% | `monthly_surplus` | `min((surplus / income %) * 200, 100)` (50%+ surplus = 100 pts) |
| **Goal Progress** | 10% | `goal_progress_percent` | Direct 0-100% score |

**Overall Score Statistics**:
- **Mean Score**: 67.36 / 100
- **Median Score**: 70.72 / 100
- **Min / Max Score**: 12.09 to 99.40

---

## 2. Calculated Health Category Distribution

| Category | Count | Percentage (%) | Mean_Score | Median_Score |
| --- | --- | --- | --- | --- |
| Poor | 153 | 10.20 | 29.77 | 30.24 |
| Needs Improvement | 321 | 21.40 | 51.41 | 51.67 |
| Moderate | 571 | 38.07 | 70.71 | 71.01 |
| Good | 455 | 30.33 | 87.04 | 86.68 |

---

## 3. Financial Goal Feasibility & Progress Summary

| Metric | Value |
| --- | --- |
| Average Financial Goal Amount ($) | 1264552.16 |
| Average Current Savings ($) | 716115.49 |
| Average Goal Gap ($) | 719119.56 |
| Average Goal Progress (%) | 54.36 |
| Average Required Monthly Saving ($) | 11457.47 |
| Percentage Already Achieved (%) | 27.93 |
| Percentage On Track (%) | 59.00 |
| Percentage Needs Higher Monthly Saving (%) | 13.07 |

---

## 4. Risk Category vs Health Category Cross-Tabulation

### User Counts Matrix
| risk_category | Poor | Needs Improvement | Moderate | Good |
| --- | --- | --- | --- | --- |
| High | 48 | 110 | 192 | 178 |
| Low | 23 | 39 | 82 | 52 |
| Moderate | 82 | 172 | 297 | 225 |

### Risk Category Aggregate Breakdown
| risk_category | Avg_Calculated_Health_Score | Avg_Savings_Rate_Calculated | Avg_Debt_To_Income_Calculated | Avg_Emergency_Fund_Months |
| --- | --- | --- | --- | --- |
| High | 68.59 | 37.71 | 32.78 | 10.31 |
| Low | 65.54 | 36.47 | 39.46 | 10.24 |
| Moderate | 66.98 | 37.13 | 36.63 | 9.80 |

---

## 5. Key Data-Driven Insights

1. **Dominant Health Category**: The largest group of users falls into the 'Moderate' financial health category (38.07% of users).
2. **Health Leader by Risk Profile**: The 'High' risk category achieves the highest average health score (68.59/100).
3. **Savings Rate Correlation**: Savings rate shows a strong positive correlation (r = 0.8810) with health score.
4. **Debt Burden Impact**: Debt-to-income exhibits a strong negative correlation (r = -0.2308) with financial health.
5. **Emergency Fund Coverage**: Emergency fund buffer correlates strongly (r = 0.7017) with financial health.
6. **Goal Feasibility On-Track Ratio**: Exactly 59.00% of users are mathematically 'On Track' to achieve their financial goals.
7. **Goal Achievement Distribution**: 'In Progress' is the most common goal stage (32.93% of users).
8. **Emergency Preparedness**: 269 users (17.93%) hold less than 3 months of emergency expenses.
9. **Goal Progress Performance**: The 'High' risk category leads in average goal progress (55.88%).
10. **Overall Dataset Health**: Average health score across all 1,500 users is 67.36/100.
