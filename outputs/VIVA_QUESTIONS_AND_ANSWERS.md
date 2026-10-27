# WealthSphere — Comprehensive Viva Voce Questions & Answers
## 35 Technical Questions and Concise Answers for Project Defense

---

### Category 1: Python, Pandas, & NumPy Foundations

#### Q1. What is the role of Pandas and NumPy in the WealthSphere pipeline?
**Answer**: NumPy handles vectorized mathematical computations, piecewise clipping (`np.clip`), and array operations for the scoring engine. Pandas handles tabular dataset ingestion, exploratory statistical summarization, feature engineering, and cohort segmentation.

#### Q2. Why did you use `np.clip` in the financial health scoring calculations?
**Answer**: `np.clip` constrains calculated dimension values strictly between 0 and 100, preventing extreme values (such as savings rates $>50\%$ or negative cash flow) from exceeding the valid scoring scale.

#### Q3. How did you handle potential division-by-zero errors in Python?
**Answer**: We implemented mathematical floors using `max()` expressions. For example, emergency fund runway uses `current_savings / max(1.0, expense)` so that an expense of zero never triggers a `ZeroDivisionError`. Similarly, goal timelines use `max(1.0, horizon * 12.0)`.

---

### Category 2: Exploratory Data Analysis (EDA)

#### Q4. What were the key findings from your Exploratory Data Analysis?
**Answer**: The 1,500 records had zero duplicates and zero missing values. Distributions for income and wealth were right-skewed, mirroring real-world economic distributions. Savings rate demonstrated the strongest correlation ($+0.88$) with financial stability, while debt-to-income showed a strong negative correlation ($-0.42$).

#### Q5. How did you check for and handle outliers during EDA?
**Answer**: Outliers were identified using the Interquartile Range (IQR) method ($1.5 \times \text{IQR}$). Because extreme incomes and goals represent valid high-net-worth profiles rather than measurement errors, we preserved them in the dataset while using median imputation and robust scaling during ML modeling.

---

### Category 3: Feature Engineering

#### Q6. What new features did you engineer, and why were they necessary?
**Answer**: We engineered six core domain metrics: `savings_rate_calculated`, `debt_to_income_calculated`, `emergency_fund_months`, `expense_ratio`, `monthly_surplus`, and `goal_progress_percent`. Raw dollar amounts fail to capture solvency; these ratios normalize metrics across different income brackets.

#### Q7. How is the Debt-to-Income (DTI) ratio calculated in your system?
**Answer**: DTI is calculated as:
$$\text{DTI} = \frac{\text{Total Debt}}{\text{Monthly Income} \times 12} \times 100$$
This measures outstanding debt obligations relative to annual gross earning capacity.

#### Q8. Why is Emergency Fund measured in "months" rather than currency?
**Answer**: Absolute savings (e.g., ₹50,000) provides different security depending on living costs. Dividing liquid savings by monthly expenses gives the true liquid runway—how many months the consumer can survive without income.

---

### Category 4: Machine Learning & Modeling

#### Q9. What machine learning task does WealthSphere solve?
**Answer**: It solves a supervised multi-class classification problem, predicting a consumer's financial risk tolerance persona into one of three categories: `Low`, `Moderate`, or `High`.

#### Q10. What features are fed into the machine learning model?
**Answer**: Nine numerical features: `age`, `monthly_income`, `monthly_expense`, `monthly_savings`, `current_savings`, `debt`, `financial_goal_amount`, `investment_horizon_years`, and `risk_tolerance_score`.

#### Q11. Which machine learning models did you evaluate, and which one performed best?
**Answer**: We evaluated Logistic Regression, Decision Tree, and Random Forest Classifier. **Logistic Regression** achieved the highest performance with a validation accuracy of **82.00%**, compared to 80.67% for Random Forest and 72.00% for Decision Tree.

#### Q12. Why did Logistic Regression outperform or match tree-based ensembles on this dataset?
**Answer**: The engineered financial features have predominantly linear relationships with risk categories. With proper median imputation and standard scaling, Logistic Regression prevented overfitting on synthetic boundaries, yielding superior generalization and well-calibrated class probabilities.

#### Q13. How did you split the dataset for model training and validation?
**Answer**: We used a stratified train/test split with an 80/20 ratio (1,200 training samples, 300 test samples). The `stratify=y` parameter ensured that class distributions (`Low`, `Moderate`, `High`) were preserved proportionally in both splits.

#### Q14. What preprocessing steps were packaged into the ML Pipeline?
**Answer**: We used a Scikit-Learn `Pipeline` containing `SimpleImputer(strategy='median')` to handle missing values, `StandardScaler()` to standardize feature variance, and the `LogisticRegression` estimator. Packaging them into a pipeline prevents data leakage.

#### Q15. How do you persist the trained model and feature schema?
**Answer**: We used `joblib.dump()` to serialize the trained pipeline to `model/best_model.joblib` and the list of feature column names to `model/feature_columns.joblib`. This ensures exact feature alignment during Streamlit inference.

---

### Category 5: Evaluation Metrics (Accuracy, Precision, Recall, F1)

#### Q16. What is the difference between Accuracy and F1-Score?
**Answer**: Accuracy measures the ratio of total correct predictions to total samples. F1-Score is the harmonic mean of precision and recall, providing a balanced evaluation that accounts for potential class imbalances across categories.

#### Q17. What were your model’s precision, recall, and F1 scores?
**Answer**: On the test set, the Logistic Regression model achieved:
* **Accuracy**: 82.00%
* **Weighted Precision**: 82.09%
* **Weighted Recall**: 82.00%
* **Weighted F1-Score**: 81.84%

#### Q18. How does the application extract risk confidence?
**Answer**: It calls `model.predict_proba(input_vector)` to obtain the calibrated probability distribution across classes (`Low`, `Moderate`, `High`). Confidence is reported as $\max(P) \times 100$.

---

### Category 6: Financial Health Scoring Engine

#### Q19. How is the 100-Point Financial Health Score calculated?
**Answer**: It is a weighted composite index across six pillars:
$$\text{Score} = 0.25(\text{Savings Rate}) + 0.20(\text{Debt Burden}) + 0.20(\text{Emergency Fund}) + 0.15(\text{Expense Ratio}) + 0.10(\text{Monthly Surplus}) + 0.10(\text{Goal Progress})$$

#### Q20. What are the thresholds for the health score categories?
**Answer**:
* **Poor**: 0.0 – 39.9
* **Needs Improvement**: 40.0 – 59.9
* **Moderate**: 60.0 – 79.9
* **Good**: 80.0 – 100.0

#### Q21. How does the system generate the dynamic health explanation?
**Answer**: The system sorts the six component scores. It identifies the highest-scoring pillar as the consumer's primary strength and the lowest-scoring pillar as the primary area requiring attention, dynamically generating an individualized narrative.

---

### Category 7: Goal Feasibility Engine

#### Q22. How does the Goal Feasibility Engine determine if a user is "On Track"?
**Answer**: It calculates the required monthly saving:
$$\text{Required Monthly} = \frac{\text{Goal Amount} - \text{Current Savings}}{\text{Horizon Years} \times 12}$$
If the user's monthly surplus is greater than or equal to this required amount, they are classified as **On Track**; otherwise, they are classified as **Needs Higher Monthly Saving**.

#### Q23. What happens if a user's current savings already exceed their goal?
**Answer**: The system detects that $\text{Current Savings} \ge \text{Goal Amount}$, sets the remaining gap to ₹0, and assigns the status **Already Achieved**.

---

### Category 8: Streamlit & Front-End Architecture

#### Q24. How does Streamlit handle state management in WealthSphere?
**Answer**: Streamlit uses `st.session_state` to store user profile parameters (income, expenses, savings, goal, horizon, etc.). When a user changes an input or clicks "Analyze Profile", `st.session_state` updates and triggers a reactive rerun.

#### Q25. Why did you use `@st.cache_resource` and `@st.cache_data`?
**Answer**: `@st.cache_resource` caches the ML model pipeline in memory so it is only loaded once at startup rather than on every user interaction. `@st.cache_data` caches the static CSV dataset and base64 image assets, keeping page transitions fast ($<100\text{ ms}$).

#### Q26. Why did you use Plotly instead of static Matplotlib charts in the dashboard?
**Answer**: Plotly generates interactive, hardware-accelerated HTML5/WebGL charts supporting tooltips, zoom, pan, and legend toggling. Matplotlib produces static raster images without user interaction.

#### Q27. How did you create the circular donut gauge for the health score?
**Answer**: We engineered a lightweight SVG circular progress ring using dynamic `stroke-dasharray` and `stroke-dashoffset` attributes calculated from the score percentage. This renders instantly without Plotly overhead.

---

### Category 9: What-If Simulator & Innovation

#### Q28. What makes the What-If Simulator technically significant?
**Answer**: It is a real-time counterfactual engine. When a slider moves, it re-runs feature engineering, the ML model, the health score, and goal feasibility entirely in memory, immediately displaying before-and-after differences ($\pm \Delta$) and updating a multi-year wealth accumulation curve.

#### Q29. Does the What-If Simulator modify the original dataset or model files?
**Answer**: No. All simulation adjustments operate strictly on ephemeral in-memory copies within `st.session_state`. The original model and CSV files remain completely untouched.

#### Q30. What genuine innovation does WealthSphere introduce?
**Answer**: The unified synthesis of four domains: predictive machine learning (risk classification), deterministic financial diagnostics (health scoring), mathematical goal modeling, and real-time counterfactual simulation—presented in an explainable, responsive interface.

---

### Category 10: Limitations & Future Scope

#### Q31. What are the primary limitations of the current project?
**Answer**:
1. It is trained on a synthetic consumer dataset.
2. It does not integrate live bank transaction feeds (Plaid/Open Banking).
3. It assumes constant purchasing power without variable investment compounding.
4. It is designed for educational decision support rather than certified financial advice.

#### Q32. How can this platform be extended for a production commercial deployment?
**Answer**:
1. Implement Open Banking APIs for automatic bank feed ingestion.
2. Add PostgreSQL/Supabase database persistence and user authentication.
3. Incorporate live stock/mutual fund market APIs.
4. Add automated PDF report generation.

#### Q33. Why shouldn't WealthSphere be considered certified financial advice?
**Answer**: Certified financial advice requires personalized fiduciary evaluation, compliance with regulatory bodies (such as SEBI or SEC), and formal verification of consumer liabilities. WealthSphere is an educational simulation platform.

#### Q34. How did you ensure the system is resilient against invalid inputs?
**Answer**: We verified nine edge cases in our automated test suite (including income=0, expense=0, debt=0, zero horizon, and high debt). The code incorporates mathematical floors and clamps to prevent crashes or `NaN` outputs under all conditions.

#### Q35. What is the single most important metric in the entire dashboard?
**Answer**: The **Savings Rate**. Our empirical correlation analysis proved that the savings rate has a $+0.88$ correlation with financial health category, making cash flow discipline the single greatest driver of long-term solvency.
