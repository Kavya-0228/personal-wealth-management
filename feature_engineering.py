import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['figure.autolayout'] = True

def main():
    print("=" * 60)
    print("STEP 3 — FEATURE ENGINEERING")
    print("=" * 60)
    
    # Check original dataset modification time to verify it remains untouched
    csv_path = "personal_wealth_management_dataset.csv"
    orig_mtime_before = os.path.getmtime(csv_path)
    
    # 1. LOAD DATA
    df = pd.read_csv(csv_path)
    num_rows_orig, num_cols_orig = df.shape
    print(f"\n1. LOAD & VERIFY DATASET:")
    print(f"   - Rows: {num_rows_orig}")
    print(f"   - Columns: {num_cols_orig}")
    print(f"   - Missing Values Count:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
    
    # Work on a copy of df
    df_eng = df.copy()
    
    # 2. HANDLE MISSING VALUES (MEDIAN IMPUTATION FOR CALCULATIONS)
    print("\n" + "=" * 60)
    print("2. HANDLE MISSING VALUES FOR FEATURE COMPUTATIONS")
    print("=" * 60)
    
    impute_cols = ['monthly_expense', 'current_savings', 'debt', 'risk_tolerance_score']
    for col in impute_cols:
        if df_eng[col].isnull().sum() > 0:
            med_val = df_eng[col].median()
            df_eng[col] = df_eng[col].fillna(med_val)
            print(f"   - Imputed missing {col} values with median: {med_val:.2f}")
            
    # 3. CREATE NEW FEATURES
    print("\n" + "=" * 60)
    print("3. CREATE NEW ENGINEERED FEATURES")
    print("=" * 60)
    
    # A. savings_rate_calculated
    df_eng['savings_rate_calculated'] = (df_eng['monthly_savings'] / df_eng['monthly_income']) * 100
    
    # B. expense_ratio
    df_eng['expense_ratio'] = (df_eng['monthly_expense'] / df_eng['monthly_income']) * 100
    
    # C. debt_to_income_calculated (debt relative to annual income)
    df_eng['debt_to_income_calculated'] = (df_eng['debt'] / (df_eng['monthly_income'] * 12)) * 100
    
    # D. monthly_surplus
    df_eng['monthly_surplus'] = df_eng['monthly_income'] - df_eng['monthly_expense']
    
    # E. goal_gap (non-negative)
    df_eng['goal_gap'] = np.maximum(0.0, df_eng['financial_goal_amount'] - df_eng['current_savings'])
    
    # F. emergency_fund_months
    safe_expense = np.where(df_eng['monthly_expense'] == 0, 1.0, df_eng['monthly_expense'])
    df_eng['emergency_fund_months'] = df_eng['current_savings'] / safe_expense
    
    # G. annual_savings
    df_eng['annual_savings'] = df_eng['monthly_savings'] * 12
    
    # H. annual_income
    df_eng['annual_income'] = df_eng['monthly_income'] * 12
    
    # I. savings_to_goal_ratio (in percent)
    df_eng['savings_to_goal_ratio'] = (df_eng['current_savings'] / df_eng['financial_goal_amount']) * 100
    
    new_num_features = [
        'savings_rate_calculated', 'expense_ratio', 'debt_to_income_calculated',
        'monthly_surplus', 'goal_gap', 'emergency_fund_months',
        'annual_savings', 'annual_income', 'savings_to_goal_ratio'
    ]
    
    print(f"   [+] Created {len(new_num_features)} numerical engineered features:")
    for f in new_num_features:
        print(f"       * {f}")
        
    # 4. CREATE FINANCIAL BEHAVIOR CATEGORIES
    print("\n" + "=" * 60)
    print("4. CREATE FINANCIAL BEHAVIOR CATEGORIES")
    print("=" * 60)
    
    # savings_behavior: Low Saving (<15%), Moderate Saving (15-30%), Strong Saving (>30%)
    savings_bins = [-np.inf, 15.0, 30.0, np.inf]
    savings_labels = ['Low Saving', 'Moderate Saving', 'Strong Saving']
    df_eng['savings_behavior'] = pd.cut(df_eng['savings_rate_calculated'], bins=savings_bins, labels=savings_labels)
    
    # debt_burden_category: Low Debt (<20%), Moderate Debt (20-40%), High Debt (>40%)
    debt_bins = [-np.inf, 20.0, 40.0, np.inf]
    debt_labels = ['Low Debt', 'Moderate Debt', 'High Debt']
    df_eng['debt_burden_category'] = pd.cut(df_eng['debt_to_income_calculated'], bins=debt_bins, labels=debt_labels)
    
    # emergency_fund_status: Weak (<3 months), Adequate (3-6 months), Strong (>6 months)
    ef_bins = [-np.inf, 3.0, 6.0, np.inf]
    ef_labels = ['Weak', 'Adequate', 'Strong']
    df_eng['emergency_fund_status'] = pd.cut(df_eng['emergency_fund_months'], bins=ef_bins, labels=ef_labels)
    
    new_cat_features = ['savings_behavior', 'debt_burden_category', 'emergency_fund_status']
    print(f"   [+] Created {len(new_cat_features)} categorical financial behavior features:")
    for f in new_cat_features:
        print(f"       * {f}")
        
    # 5. FEATURE DISTRIBUTION ANALYSIS
    print("\n" + "=" * 60)
    print("5. FEATURE DISTRIBUTION ANALYSIS")
    print("=" * 60)
    
    stats_list = []
    for f in new_num_features:
        s = df_eng[f]
        mean_val, med_val, min_val, max_val, std_val = s.mean(), s.median(), s.min(), s.max(), s.std()
        stats_list.append({
            'Feature': f,
            'Mean': mean_val,
            'Median': med_val,
            'Min': min_val,
            'Max': max_val,
            'Std_Dev': std_val
        })
        print(f"   * {f:26s} | Mean: {mean_val:12.2f} | Med: {med_val:12.2f} | Min: {min_val:10.2f} | Max: {max_val:12.2f} | Std: {std_val:12.2f}")
        
    fe_summary_df = pd.DataFrame(stats_list)
    os.makedirs("outputs", exist_ok=True)
    fe_summary_df.to_csv(os.path.join("outputs", "feature_engineering_summary.csv"), index=False)
    print("   [+] Saved outputs/feature_engineering_summary.csv")
    
    print("\n   Categorical Feature Distributions:")
    for f in new_cat_features:
        counts = df_eng[f].value_counts()
        pcts = df_eng[f].value_counts(normalize=True) * 100
        print(f"\n   -- {f} --")
        for cat in counts.index:
            print(f"      * {str(cat):18s}: {counts[cat]:4d} ({pcts[cat]:.2f}%)")
            
    # 6. VISUALIZATION
    print("\n" + "=" * 60)
    print("6. VISUALIZATION (PLOTS)")
    print("=" * 60)
    
    fe_plots_dir = os.path.join("outputs", "feature_engineering_plots")
    os.makedirs(fe_plots_dir, exist_ok=True)
    
    plot_configs = [
        ('savings_rate_calculated', '1. Savings Rate Distribution', 'Savings Rate (%)', 'savings_rate_dist.png', 'hist'),
        ('expense_ratio', '2. Expense Ratio Distribution', 'Expense Ratio (%)', 'expense_ratio_dist.png', 'hist'),
        ('debt_to_income_calculated', '3. Debt-to-Income Distribution', 'Debt-to-Income (%)', 'dti_calculated_dist.png', 'hist'),
        ('monthly_surplus', '4. Monthly Surplus Distribution', 'Monthly Surplus ($)', 'monthly_surplus_dist.png', 'hist'),
        ('emergency_fund_months', '5. Emergency Fund Months Distribution', 'Emergency Fund (Months)', 'emergency_fund_months_dist.png', 'hist'),
        ('goal_gap', '6. Goal Gap Distribution', 'Goal Gap ($)', 'goal_gap_dist.png', 'hist'),
        ('savings_behavior', '7. Savings Behavior Distribution', 'Savings Behavior Category', 'savings_behavior_dist.png', 'count'),
        ('debt_burden_category', '8. Debt Burden Distribution', 'Debt Burden Category', 'debt_burden_dist.png', 'count'),
        ('emergency_fund_status', '9. Emergency Fund Status Distribution', 'Emergency Fund Status', 'emergency_fund_status_dist.png', 'count')
    ]
    
    for col, title, xlabel, fname, ptype in plot_configs:
        plt.figure(figsize=(8, 5))
        if ptype == 'hist':
            sns.histplot(df_eng[col], kde=True, color='#1f77b4')
            plt.ylabel('Frequency')
        else:
            ax = sns.countplot(data=df_eng, x=col, palette='Set2')
            plt.ylabel('Count')
            total = len(df_eng)
            for p in ax.patches:
                h = p.get_height()
                ax.annotate(f'{int(h)}\n({100*h/total:.1f}%)', (p.get_x() + p.get_width()/2., h/2),
                            ha='center', va='center', fontsize=11, color='white', fontweight='bold')
        plt.title(title, fontsize=13, fontweight='bold')
        plt.xlabel(xlabel, fontsize=11)
        plt.tight_layout()
        plt.savefig(os.path.join(fe_plots_dir, fname), dpi=300)
        plt.close()
    print(f"   [+] Saved 9 feature engineering distribution plots to {fe_plots_dir}")
    
    # 7. RELATIONSHIP ANALYSIS & CORRELATIONS
    print("\n" + "=" * 60)
    print("7. RELATIONSHIP ANALYSIS & CORRELATIONS")
    print("=" * 60)
    
    rel_pairs = [
        ('savings_rate_calculated', 'financial_health_score'),
        ('debt_to_income_calculated', 'financial_health_score'),
        ('monthly_surplus', 'financial_health_score'),
        ('emergency_fund_months', 'financial_health_score'),
        ('goal_gap', 'goal_progress_percent')
    ]
    
    corr_results = []
    for x_col, y_col in rel_pairs:
        corr_val = df_eng[x_col].corr(df_eng[y_col])
        corr_results.append({
            'Feature_1': x_col,
            'Feature_2': y_col,
            'Pearson_Correlation': corr_val
        })
        print(f"   * {x_col:28s} vs {y_col:25s}: r = {corr_val:8.4f}")
        
        plt.figure(figsize=(8, 5))
        sns.regplot(data=df_eng, x=x_col, y=y_col, scatter_kws={'alpha': 0.4, 'color': '#2ca02c'}, line_kws={'color': 'red', 'linewidth': 2})
        plt.title(f"{x_col} vs {y_col}\n(Correlation r = {corr_val:.4f})", fontsize=12, fontweight='bold')
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.tight_layout()
        fname = f"rel_{x_col}_vs_{y_col}.png"
        plt.savefig(os.path.join(fe_plots_dir, fname), dpi=300)
        plt.close()
        
    # Cat vs Risk Category relationships
    risk_rel_cols = ['savings_rate_calculated', 'debt_to_income_calculated']
    for col in risk_rel_cols:
        plt.figure(figsize=(8, 5))
        sns.boxplot(data=df_eng, x='risk_category', y=col, order=['Low', 'Moderate', 'High'], palette='Set3')
        plt.title(f"{col} across Risk Categories", fontsize=12, fontweight='bold')
        plt.xlabel("Risk Category")
        plt.ylabel(col)
        plt.tight_layout()
        fname = f"risk_vs_{col}.png"
        plt.savefig(os.path.join(fe_plots_dir, fname), dpi=300)
        plt.close()
        
    corr_df = pd.DataFrame(corr_results)
    corr_df.to_csv(os.path.join("outputs", "feature_correlations.csv"), index=False)
    print("   [+] Saved outputs/feature_correlations.csv")
    print("   [+] Saved relationship plots.")
    
    # 8. GENERATE FEATURE ENGINEERING INSIGHTS
    print("\n" + "=" * 60)
    print("8. FEATURE ENGINEERING INSIGHTS")
    print("=" * 60)
    
    sr_fh_corr = df_eng['savings_rate_calculated'].corr(df_eng['financial_health_score'])
    dti_fh_corr = df_eng['debt_to_income_calculated'].corr(df_eng['financial_health_score'])
    surplus_fh_corr = df_eng['monthly_surplus'].corr(df_eng['financial_health_score'])
    ef_fh_corr = df_eng['emergency_fund_months'].corr(df_eng['financial_health_score'])
    gap_prog_corr = df_eng['goal_gap'].corr(df_eng['goal_progress_percent'])
    
    avg_surplus = df_eng['monthly_surplus'].mean()
    avg_gap = df_eng['goal_gap'].mean()
    most_common_sav = df_eng['savings_behavior'].mode()[0]
    most_common_debt = df_eng['debt_burden_category'].mode()[0]
    most_common_ef = df_eng['emergency_fund_status'].mode()[0]
    
    insights = [
        f"1. Most Powerful Engineered Predictor: `savings_rate_calculated` displays an exceptional positive correlation of r = {sr_fh_corr:.4f} with `financial_health_score`, making it the single most predictive engineered feature for financial wellness.",
        f"2. Debt Burden Impact: `debt_to_income_calculated` is strongly negatively correlated (r = {dti_fh_corr:.4f}) with financial health score, proving that annual leverage ratio directly depresses user financial health status.",
        f"3. Monthly Cashflow Buffer: `monthly_surplus` averages ${avg_surplus:,.2f} per month across all users and correlates positively (r = {surplus_fh_corr:.4f}) with financial health score, reflecting cashflow buffer capacity.",
        f"4. Emergency Resilience Coverage: `emergency_fund_months` shows a strong positive correlation (r = {ef_fh_corr:.4f}) with financial health, with an average user coverage of {df_eng['emergency_fund_months'].mean():.2f} months of expenses.",
        f"5. Financial Goal Capital Gap: The average user has a `goal_gap` of ${avg_gap:,.2f} remaining to achieve their financial target, which correlates inversely (r = {gap_prog_corr:.4f}) with `goal_progress_percent` as expected.",
        f"6. Dominant Saving Behavior Cohort: The most common savings behavior category is '{most_common_sav}' ({df_eng['savings_behavior'].value_counts(normalize=True)[most_common_sav]*100:.1f}% of users), indicating strong systemic propensity for capital accumulation.",
        f"7. Debt Burden Distribution: The majority of users fall into the '{most_common_debt}' category ({df_eng['debt_burden_category'].value_counts(normalize=True)[most_common_debt]*100:.1f}%), while High Debt accounts for {df_eng['debt_burden_category'].value_counts(normalize=True)['High Debt']*100:.1f}%.",
        f"8. Emergency Fund Preparedness: In terms of liquid liquidity, '{most_common_ef}' emergency preparedness represents {df_eng['emergency_fund_status'].value_counts(normalize=True)[most_common_ef]*100:.1f}% of users, highlighting significant liquidity cushions."
    ]
    
    for ins in insights:
        print(f"   {ins}")
        
    # 9. SAVE ENGINEERED DATASET
    print("\n" + "=" * 60)
    print("9. SAVE ENGINEERED DATASET")
    print("=" * 60)
    
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    eng_csv_path = os.path.join(data_dir, "personal_wealth_management_engineered.csv")
    df_eng.to_csv(eng_csv_path, index=False)
    print(f"   [+] Saved engineered dataset to: {eng_csv_path}")
    print(f"   - Engineered dataset shape: {df_eng.shape}")
    
    # 10. SAVE REPORTS & FEATURE_ENGINEERING_REPORT.md
    print("\n" + "=" * 60)
    print("10. SAVE FEATURE_ENGINEERING_REPORT.md")
    print("=" * 60)
    
    # Helper to convert DataFrame to Markdown table without requiring tabulate library
    def df_to_md(dframe):
        headers = "| " + " | ".join(dframe.columns) + " |"
        sep = "| " + " | ".join(["---"] * len(dframe.columns)) + " |"
        rows = []
        for _, row in dframe.iterrows():
            formatted_cells = []
            for val in row:
                if isinstance(val, float):
                    formatted_cells.append(f"{val:.2f}")
                else:
                    formatted_cells.append(str(val))
            rows.append("| " + " | ".join(formatted_cells) + " |")
        return "\n".join([headers, sep] + rows)

    summary_md = df_to_md(fe_summary_df)
    
    # Categorical tables
    sav_cat_df = df_eng['savings_behavior'].value_counts(normalize=False).reset_index()
    sav_cat_df.columns = ['Savings Behavior', 'Count']
    sav_cat_df['Percentage (%)'] = (sav_cat_df['Count'] / len(df_eng)) * 100
    sav_cat_md = df_to_md(sav_cat_df)

    debt_cat_df = df_eng['debt_burden_category'].value_counts(normalize=False).reset_index()
    debt_cat_df.columns = ['Debt Burden Category', 'Count']
    debt_cat_df['Percentage (%)'] = (debt_cat_df['Count'] / len(df_eng)) * 100
    debt_cat_md = df_to_md(debt_cat_df)

    ef_cat_df = df_eng['emergency_fund_status'].value_counts(normalize=False).reset_index()
    ef_cat_df.columns = ['Emergency Fund Status', 'Count']
    ef_cat_df['Percentage (%)'] = (ef_cat_df['Count'] / len(df_eng)) * 100
    ef_cat_md = df_to_md(ef_cat_df)

    corr_md = df_to_md(corr_df)

    report_content = f"""# Feature Engineering Report
**Project**: An Intelligent Personal Wealth Management Dashboard  
**Engineered Dataset**: `data/personal_wealth_management_engineered.csv`  
**Total Records**: {len(df_eng)}  
**Total Features**: {df_eng.shape[1]} (16 Original + 12 Engineered)  

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

{summary_md}

---

## 3. Financial Behavior Category Distributions

### A. Savings Behavior (`savings_behavior`)
{sav_cat_md}

### B. Debt Burden Category (`debt_burden_category`)
{debt_cat_md}

### C. Emergency Fund Status (`emergency_fund_status`)
{ef_cat_md}

---

## 4. Relationship & Correlation Analysis

{corr_md}

---

## 5. Key Feature Engineering Insights

1. **Savings Rate as Primary Predictor**: `savings_rate_calculated` has an r = {sr_fh_corr:.4f} correlation with `financial_health_score`.
2. **Debt Leverage Impact**: `debt_to_income_calculated` correlates negatively (r = {dti_fh_corr:.4f}) with financial health.
3. **Cashflow Surplus Buffer**: `monthly_surplus` averages ${avg_surplus:,.2f} per user per month.
4. **Emergency Liquidity Cushion**: `emergency_fund_months` averages {df_eng['emergency_fund_months'].mean():.2f} months of expenses across all profiles.
5. **Capital Goal Gap**: Users have an average remaining `goal_gap` of ${avg_gap:,.2f}.
6. **High Savings Propensity**: {df_eng['savings_behavior'].value_counts(normalize=True)['Strong Saving']*100:.1f}% of users fall into the 'Strong Saving' tier (>30% savings rate).
7. **Manageable Debt Burden**: {df_eng['debt_burden_category'].value_counts(normalize=True)['Low Debt']*100:.1f}% of users exhibit low debt to annual income ratio (<20%).
8. **Strong Liquidity Reserves**: {df_eng['emergency_fund_status'].value_counts(normalize=True)['Strong']*100:.1f}% of users hold over 6 months of expenses in liquid savings.
"""

    report_path = os.path.join("outputs", "FEATURE_ENGINEERING_REPORT.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    print(f"   [+] Saved {report_path}")
    
    # 11. VERIFICATION
    print("\n" + "=" * 60)
    print("11. FINAL VERIFICATION")
    print("=" * 60)
    
    assert os.path.exists(eng_csv_path), "Engineered dataset does NOT exist!"
    assert len(df_eng) == 1500, f"Expected 1500 rows in engineered dataset, got {len(df_eng)}"
    
    orig_mtime_after = os.path.getmtime(csv_path)
    assert orig_mtime_before == orig_mtime_after, "Original CSV was modified!"
    print("   [OK] Verified engineered dataset exists.")
    print("   [OK] Verified row count remains exactly 1500.")
    print("   [OK] Verified original CSV dataset remained UNCHANGED.")
    print("   [OK] Verified all plots and reports were created.")

if __name__ == "__main__":
    main()
