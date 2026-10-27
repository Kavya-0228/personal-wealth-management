# Problem Statement & System Comparison
## WealthSphere: Existing Systems vs. Proposed Platform Architecture

---

## 1. Problem Statement

Traditional personal finance tracking tools (e.g., standard budgeting apps, spreadsheet templates, and basic banking dashboards) suffer from systemic structural limitations:

1. **Passive Data Presentation**: Traditional platforms present raw financial balances and retrospective transaction logs without synthesizing what the numbers indicate regarding overall solvency and longevity.
2. **Opaque and Subjective Risk Understanding**: Consumer risk tolerance is typically estimated through subjective qualitative surveys rather than calibrated against concrete empirical financial indicators such as debt-to-income, cash flow buffers, and investment horizons.
3. **Absence of Unified Health Diagnostics**: While users receive credit scores to quantify lending risk from a bank's perspective, they lack an objective, consumer-centric **Financial Health Score** that balances savings velocity, debt burdens, and liquid emergency safety nets.
4. **Static and Fragmented Goal Planning**: Goal calculators assume rigid linear accumulation and fail to dynamically evaluate whether target milestones are mathematically feasible given changing monthly surpluses.
5. **Lack of Dynamic Scenario Simulation**: Users are unable to simulate financial decisions before making them (e.g., *"How will taking on ₹20,000 in debt or reducing expenses by ₹5,000 impact my goal date, health score, and risk profile?"*).

---

## 2. Existing vs. Proposed System Comparative Matrix

| Feature / Dimension | Existing Systems (Traditional Trackers) | Proposed System (WealthSphere Platform) |
| :--- | :--- | :--- |
| **Data Nature** | Static retrospective expense logs | Dynamic diagnostic and forward-looking intelligence |
| **Risk Assessment** | Subjective static questionnaires or absent | **Supervised ML Classification (82.00% Accuracy)** with confidence spectrum |
| **Health Metric** | Single external credit score (lender-biased) | **Composite 100-Point Financial Health Score** across 6 weighted behavioral pillars |
| **Goal Tracking** | Linear balance accumulation meters | **Mathematical Goal Feasibility Engine** calculating run-rate deficits and timelines |
| **Decision Testing** | None; requires manual spreadsheet modeling | **Interactive What-If Wealth Simulator** with real-time before/after parameter testing |
| **Insights Delivery** | Generic canned savings tips | **Dynamic Contextual AI Insights** (Top Strengths, Watchouts, Next Best Actions) |
| **Visual Architecture** | Basic tables or generic administrative UI | **Executive FinTech Interface** with SVG radial progress gauges and Plotly cohort analytics |
| **Mathematical Transparency** | Black-box calculations or simple sums | Fully transparent, reproducible formulas with zero hidden heuristics |

---

## 3. Project Objectives

WealthSphere was architected around seven explicit, measurable milestones:

1. **Analyze Financial Consumer Behavior**: Conduct rigorous Exploratory Data Analysis (EDA) on 1,500 consumer profiles to quantify distributions, leverage skewness, and liquidity characteristics.
2. **Engineer Domain-Specific Financial Indicators**: Formulate and validate six foundational ratios: calculated savings rate, debt-to-income ratio, emergency coverage months, expense ratio, monthly surplus, and goal progress.
3. **Predict Financial Risk Profiles Using Supervised ML**: Train, benchmark, and deploy a supervised machine learning model capable of classifying consumer risk personas (`Low`, `Moderate`, `High`) with high validation accuracy ($\ge 80\%$).
4. **Calculate an Interpretable Financial Health Score**: Develop a transparent, 100-point composite scoring model synthesizing six financial pillars with objective category thresholds (`Poor`, `Needs Improvement`, `Moderate`, `Good`).
5. **Evaluate Mathematical Financial Goal Feasibility**: Create a dynamic goal engine that accurately computes remaining shortfalls, required monthly velocity, saving gaps, and feasibility classifications.
6. **Provide Interactive What-If Scenario Simulations**: Implement a real-time sandbox allowing consumers to adjust financial levers and visualize immediate changes to their health scores, goals, and multi-year wealth accumulation curves.
7. **Present Financial Intelligence Through a Competition-Grade Dashboard**: Deliver a cohesive, responsive Streamlit dashboard that immediately answers three core questions: *How am I doing? What is my risk? Am I on track?*
