# WealthSphere — Project Presentation Slide Deck Outline
## 15 Slide Presentation Structure for Academic & Competition Review

---

### Slide 1: Title Slide
* **Slide Title**: WealthSphere: Personal Financial Intelligence Platform
* **Subtitle**: An AI-Powered Personal Wealth Diagnostic, Risk Classification & Scenario Simulation Engine
* **Bullet Points**:
  * Combining Machine Learning, Financial Diagnostics, and Counterfactual Simulation.
  * Designed for actionable, data-driven consumer decision support.
  * Developed with Python, Scikit-Learn, Streamlit, and Plotly.
* **Recommended Visual**: High-resolution screenshot of the WealthSphere Overview Dashboard showing the KPI cards, SVG donut gauge, and midnight navy sidebar.

---

### Slide 2: Introduction
* **Slide Title**: The Personal Wealth Management Challenge
* **Bullet Points**:
  * Personal financial decisions are increasingly complex across modern economic environments.
  * Consumers manage multiple accounts, debt streams, and milestones without unified visibility.
  * The transition from passive bookkeeping to automated financial intelligence is essential.
  * WealthSphere provides an end-to-end diagnostic ecosystem tailored for individual consumers.
* **Recommended Visual**: Diagram contrasting fragmented spreadsheets with WealthSphere’s unified single pane of glass.

---

### Slide 3: Problem Statement
* **Slide Title**: Limitations of Existing Financial Tools
* **Bullet Points**:
  * **Raw Numbers Without Context**: Users see account balances but not overall solvency health.
  * **Opaque Risk Assessment**: Risk tolerance is measured via subjective questionnaires rather than financial data.
  * **Absence of Unified Diagnostic Score**: Credit scores measure lending risk for banks, not consumer prosperity.
  * **No Real-Time Scenario Modeling**: Consumers cannot test the long-term impact of life decisions before committing.
* **Recommended Visual**: Comparison graphic illustrating the "Information Gap" in current budgeting applications.

---

### Slide 4: Project Objectives
* **Slide Title**: Core Project Objectives
* **Bullet Points**:
  * Conduct comprehensive EDA and domain-specific feature engineering on 1,500 financial records.
  * Train and benchmark supervised ML models to predict risk tolerance personas with $\ge 80\%$ accuracy.
  * Develop a transparent 100-point Financial Health Score synthesizing 6 core financial pillars.
  * Implement an automated goal feasibility engine calculating concrete monthly run-rates and deficits.
  * Deliver an interactive "What-If" wealth simulation sandbox and executive FinTech front end.
* **Recommended Visual**: Checklist graphic showing the 5 technical milestones completed.

---

### Slide 5: Existing vs. Proposed System
* **Slide Title**: Existing Systems vs. Proposed WealthSphere
* **Bullet Points**:
  * **Existing**: Retrospective transaction logging, static charts, subjective risk questionnaires, no simulation.
  * **Proposed**: Predictive supervised ML classification, 100-point composite diagnostic health index.
  * **Proposed**: Deterministic goal velocity modeling and real-time counterfactual What-If sandbox.
  * **Advantage**: Bridges passive expense tracking with proactive financial intelligence.
* **Recommended Visual**: Side-by-side comparative table highlighting key architectural differentiators.

---

### Slide 6: System Architecture
* **Slide Title**: High-Level System Architecture
* **Bullet Points**:
  * **Layered Decoupled Pipeline**: Ingestion Layer $\rightarrow$ Feature Engine $\rightarrow$ Analytical Core $\rightarrow$ UI.
  * **Dual Engine Core**: Machine Learning Classification Pipeline + Deterministic Scoring Engine.
  * **In-Memory Simulation Sandbox**: Recomputes health scores and ML predictions dynamically.
  * **Modern Presentation**: Streamlit application with custom SVG gauges and Plotly cohort curves.
* **Recommended Visual**: The complete WealthSphere Mermaid architecture flowchart.

---

### Slide 7: Dataset & Exploratory Data Analysis
* **Slide Title**: Dataset Profile & Data Hygiene
* **Bullet Points**:
  * **Cohort Profile**: 1,500 consumer financial records across 10 fundamental attributes.
  * **Data Integrity**: Verified 0 duplicate rows and 0 missing values across all features.
  * **Distribution Characteristics**: Right-skewed wealth distributions reflecting macroeconomic realities.
  * **Key Findings**: Strong positive correlation ($+0.88$) between monthly surplus and savings velocity.
* **Recommended Visual**: Plotly correlation matrix heatmap and income distribution histogram.

---

### Slide 8: Domain Feature Engineering
* **Slide Title**: Domain Financial Indicators
* **Bullet Points**:
  * **Calculated Savings Rate**: $\text{Monthly Savings} / \text{Gross Income} \times 100$.
  * **Debt-to-Income (DTI)**: $\text{Total Debt} / \text{Annual Gross Income} \times 100$.
  * **Emergency Fund Runway**: $\text{Liquid Savings} / \max(1, \text{Monthly Expenses})$ (Months covered).
  * **Expense Ratio**: Operating overhead relative to monthly inflow.
  * **Monthly Surplus & Goal Progress**: Discretionary cash flow and percentage of milestone achieved.
* **Recommended Visual**: Diagram displaying the mathematical formulas and their normalization curves.

---

### Slide 9: Machine Learning Risk Classification
* **Slide Title**: Machine Learning Model Benchmark
* **Bullet Points**:
  * **Task**: Multi-class supervised classification predicting risk tolerance (`Low`, `Moderate`, `High`).
  * **Pipeline**: Median Imputer + Standard Scaler + Multi-class Logistic Regression.
  * **Evaluation Benchmark**:
    * Logistic Regression: **82.00% Accuracy** | 82.09% Precision | 81.84% F1-Score.
    * Random Forest: 80.67% Accuracy | Decision Tree: 72.00% Accuracy.
  * **Selection Rationale**: Logistic Regression demonstrated optimal probability calibration and generalization.
* **Recommended Visual**: Model benchmark bar chart and confusion matrix graphic.

---

### Slide 10: The 100-Point Financial Health Score
* **Slide Title**: Objective Financial Health Scoring Engine
* **Bullet Points**:
  * **Transparent 6-Pillar Composite Index**:
    * Savings Rate (25%), Debt Burden (20%), Emergency Buffer (20%).
    * Expense Ratio (15%), Monthly Surplus (10%), Goal Progress (10%).
  * **Cohort Health Breakdown**:
    * Good (30.3%), Moderate (38.1%), Needs Improvement (21.4%), Poor (10.2%).
  * **Explainability**: Surfaces strongest asset vector and primary improvement area dynamically.
* **Recommended Visual**: The custom SVG circular donut gauge chart alongside the 6 dimension progress bars.

---

### Slide 11: Financial Goal Feasibility Engine
* **Slide Title**: Deterministic Goal Feasibility Analysis
* **Bullet Points**:
  * **Milestone Analytics**: Calculates remaining shortfall amount and monthly required contribution velocity.
  * **Surplus Gap Detection**: Identifies whether monthly surplus covers required savings without debt drag.
  * **Feasibility Classifications**:
    * Already Achieved (27.9%), On Track (59.0%), Needs Higher Monthly Saving (13.1%).
  * **Clear Roadmap**: Visualizes progress along a multi-stage journey (`Start → Current → Milestone → Target`).
* **Recommended Visual**: Screenshot of the Financial Goal Journey card and metric grid.

---

### Slide 12: Signature Feature: What-If Wealth Simulator
* **Slide Title**: Interactive What-If Wealth Simulator
* **Bullet Points**:
  * **Counterfactual Sandbox**: Real-time interactive sliders for Income, Expense, Savings, Debt, and Horizon.
  * **Reactive Execution**: Re-runs analytical equations and ML inference in $< 100$ milliseconds.
  * **Before vs. After Delta Cards**: Instantly displays changes in Health Score, Goal Progress, and Risk Persona.
  * **Visual Multi-Year Forecast**: Dynamic Plotly curve contrasting baseline run-rates with simulated trajectories.
* **Recommended Visual**: Screenshot of the What-If Simulator interface displaying slider controls and projection curve.

---

### Slide 13: Empirical Results & System Verification
* **Slide Title**: Final Verification & Test Suite Results
* **Bullet Points**:
  * **100% Test Pass Rate**: 38 out of 38 automated tests executed successfully.
  * **Mathematical Exactness**: 12/12 financial calculations verified against manual ground-truth formulas.
  * **Edge-Case Resilience**: 9/9 edge scenarios validated (Income=0, Expense=0, Debt=0, 1M Debt, Zero Horizon).
  * **Demo Profiles Validated**: 5 realistic archetypes (Financially Strong, Debt Heavy, Goal Focused, etc.).
* **Recommended Visual**: Summary verification scorecard showing green PASS badges across all modules.

---

### Slide 14: System Limitations
* **Slide Title**: Academic Limitations & Boundaries
* **Bullet Points**:
  * **Synthetic Cohort**: Built on 1,500 modeled profiles; real consumer behavior may reflect spending shocks.
  * **Linear Projections**: Baseline goal calculations assume steady purchasing power without market volatility.
  * **Offline Execution**: Currently operates on user-provided inputs rather than direct bank API feeds.
  * **Educational Boundaries**: Platform outputs serve as decision support and do not constitute certified financial advice.
* **Recommended Visual**: Clean callout card highlighting educational and synthetic scope.

---

### Slide 15: Conclusion & Future Scope
* **Slide Title**: Conclusion & Future Roadmap
* **Bullet Points**:
  * **Project Conclusion**: WealthSphere successfully proves that machine learning and transparent financial scoring can be integrated into an intuitive, actionable FinTech platform.
  * **Future Integration**: Connect live open banking APIs (Plaid) for automated transaction categorization.
  * **Persistent Storage**: Implement secure multi-user authentication with PostgreSQL/Supabase.
  * **Automated Reporting**: One-click generation of branded financial audit PDF summaries.
* **Recommended Visual**: Final logo, project links, and live demonstration URL: [http://localhost:8501](http://localhost:8501).
