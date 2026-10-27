# WealthSphere — Intelligent Personal Wealth Management Dashboard
## Academic Project Abstract

**Project Title**: WealthSphere: An Intelligent Personal Wealth Management and Financial Risk Intelligence Platform  
**Domain**: Data Science, Machine Learning, FinTech Analytics  
**Primary Technologies**: Python, Scikit-Learn, Streamlit, Pandas, NumPy, Plotly  
**Academic Year**: 2026  

---

### Abstract
Personal financial health management is essential for long-term economic stability, yet traditional budgeting tools remain fundamentally passive—presenting static spreadsheets and fragmented account balances without actionable, predictive intelligence. This project introduces **WealthSphere**, an intelligent personal wealth management platform designed to synthesize machine learning, quantitative financial indicators, goal feasibility modeling, and scenario simulation into a unified diagnostic system.

Using a curated dataset of 1,500 consumer financial profiles, the system implements an end-to-end data science pipeline. The pipeline begins with rigorous exploratory data analysis, followed by the domain-specific engineering of six key financial ratios: calculated savings rate, debt-to-income (DTI) ratio, emergency fund coverage months, expense-to-income ratio, monthly cash flow surplus, and goal progress percentage. A supervised machine learning classification framework was developed and evaluated across Logistic Regression, Decision Tree, and Random Forest architectures to predict consumer risk tolerance personas (`Low`, `Moderate`, and `High`). **Logistic Regression** achieved the highest overall performance with a **validation accuracy of 82.00%**, precision of 82.09%, recall of 82.00%, and an F1-score of 81.84%, demonstrating optimal calibration and probability stability.

To provide clear interpretability, WealthSphere introduces a transparent, 100-point composite **Financial Health Score** weighted across six foundational pillars (Savings 25%, Debt Burden 20%, Emergency Buffer 20%, Expense Overhead 15%, Monthly Surplus 10%, and Goal Progress 10%). Across the analyzed cohort, scores categorized users into Good (30.3%), Moderate (38.1%), Needs Improvement (21.4%), and Poor (10.2%). A companion **Financial Goal Engine** calculates capital shortfalls, required monthly contributions, and feasibility thresholds. The platform's signature capability—the **What-If Wealth Simulator**—empowers users to adjust income, expense, debt, and savings levers in real time, dynamically recomputing health scores, goal timelines, and machine learning risk classifications alongside multi-year wealth accumulation trajectories.

The end product is delivered through a modern, executive FinTech dashboard built in Streamlit and Plotly, designed to immediately answer three core consumer questions: *How am I doing? What is my risk? Am I on track?* WealthSphere bridges the gap between passive bookkeeping and automated financial intelligence, offering a robust model for educational simulation and consumer decision support.

---

> **Academic & Regulatory Notice**: WealthSphere is an educational simulation platform using synthetic consumer profiles. The insights, composite scores, and risk classifications generated are intended solely for academic demonstration and decision support and do not constitute certified financial, legal, or investment advice.
