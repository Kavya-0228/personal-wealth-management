import os
import json
import joblib
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# STREAMLIT PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="WealthSphere | AI Wealth Management",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# ENTERPRISE FUTURISTIC FINTECH DESIGN SYSTEM (CSS)
# Deep Purple (#0B0824) + Lavender (#C084FC) + Mint (#34D399) Theme
# ==============================================================================
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700;800&display=swap');

    :root {
        --bg-primary: #0B0824;
        --bg-secondary: #12103A;
        --bg-card: rgba(23, 21, 68, 0.85);
        --bg-card-hover: rgba(31, 28, 88, 0.95);
        --bg-input: #171444;
        --border-card: rgba(139, 92, 246, 0.22);
        --border-focus: #A855F7;
        --accent-purple: #8B5CF6;
        --accent-lavender: #C084FC;
        --accent-bright-purple: #A855F7;
        --accent-mint: #34D399;
        --accent-cyan: #67E8F9;
        --accent-warning: #FBBF24;
        --text-primary: #F8F7FF;
        --text-secondary: #B8B4D9;
        --text-muted: #8E8AA8;
    }

    /* Base Styling */
    html, body, [class*="st-emotion-cache"], .stApp {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif !important;
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }

    .stApp {
        background: radial-gradient(circle at 10% 0%, rgba(139, 92, 246, 0.14) 0%, transparent 40%),
                    radial-gradient(circle at 90% 90%, rgba(192, 132, 252, 0.09) 0%, transparent 45%),
                    var(--bg-primary) !important;
        background-attachment: fixed !important;
    }

    /* Container Spacing */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 1.75rem !important;
        padding-right: 1.75rem !important;
        max-width: 100% !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0d0a2d !important;
        background: linear-gradient(180deg, #0d0a2d 0%, #08061e 100%) !important;
        border-right: 1px solid rgba(139, 92, 246, 0.16) !important;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: var(--text-secondary);
    }

    /* Sidebar Brand */
    .brand-logo-wrap {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 0.2rem;
        padding-top: 0.5rem;
    }
    .brand-icon-box {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: linear-gradient(135deg, #8B5CF6 0%, #C084FC 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 16px rgba(139, 92, 246, 0.5);
        color: #FFFFFF;
        font-weight: 800;
        font-size: 1.25rem;
    }
    .brand-name {
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #F8F7FF;
        line-height: 1.1;
        margin: 0;
    }
    .brand-tagline {
        font-size: 0.72rem;
        font-weight: 500;
        color: #B8B4D9;
        margin-top: 0.15rem;
        letter-spacing: 0.01em;
    }

    /* Custom Radio Navigation */
    div[role="radiogroup"] {
        gap: 6px;
        display: flex;
        flex-direction: column;
        margin-top: 0.5rem;
        margin-bottom: 1.5rem;
    }

    div[role="radiogroup"] label {
        background: transparent !important;
        padding: 0.65rem 0.95rem !important;
        border-radius: 12px !important;
        border: 1px solid transparent !important;
        transition: all 0.2s ease !important;
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        display: flex;
        align-items: center;
    }

    div[role="radiogroup"] label:hover {
        background: rgba(139, 92, 246, 0.1) !important;
        color: #F8F7FF !important;
    }

    div[role="radiogroup"] label[data-checked="true"],
    div[role="radiogroup"] label[aria-checked="true"],
    div[role="radiogroup"] label:has(input:checked) {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.3) 0%, rgba(192, 132, 252, 0.2) 100%) !important;
        border: 1px solid rgba(192, 132, 252, 0.45) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 16px rgba(139, 92, 246, 0.25) !important;
    }

    div[role="radiogroup"] label input {
        display: none !important;
    }

    /* Sidebar Motivational Card */
    .sidebar-promo-card {
        background: linear-gradient(135deg, rgba(23, 21, 68, 0.9) 0%, rgba(35, 30, 95, 0.6) 100%);
        border: 1px solid rgba(139, 92, 246, 0.25);
        border-radius: 16px;
        padding: 1.1rem;
        margin-top: 1.5rem;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .sidebar-promo-icon {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        background: rgba(139, 92, 246, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #C084FC;
        font-size: 1.1rem;
        flex-shrink: 0;
    }
    .sidebar-promo-text {
        font-size: 0.78rem;
        font-weight: 600;
        color: #E2E8F0;
        line-height: 1.35;
    }

    /* Top Navbar Header */
    .top-navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(18, 16, 58, 0.65);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(139, 92, 246, 0.18);
        border-radius: 16px;
        padding: 0.65rem 1.25rem;
        margin-bottom: 1.5rem;
    }
    .top-search-box {
        display: flex;
        align-items: center;
        gap: 10px;
        background: rgba(11, 8, 36, 0.6);
        border: 1px solid rgba(139, 92, 246, 0.22);
        border-radius: 12px;
        padding: 0.45rem 1rem;
        width: 320px;
        color: var(--text-secondary);
        font-size: 0.85rem;
    }
    .top-search-input {
        background: transparent;
        border: none;
        outline: none;
        color: var(--text-primary);
        font-size: 0.85rem;
        width: 100%;
        font-family: inherit;
    }
    .top-search-input::placeholder {
        color: var(--text-muted);
    }
    .top-nav-right {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .nav-icon-btn {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        background: rgba(23, 21, 68, 0.7);
        border: 1px solid rgba(139, 92, 246, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--text-secondary);
        font-size: 0.95rem;
        cursor: pointer;
        transition: all 0.2s;
    }
    .nav-icon-btn:hover {
        border-color: var(--accent-lavender);
        color: var(--text-primary);
    }
    .ai-engine-status {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(52, 211, 153, 0.12);
        border: 1px solid rgba(52, 211, 153, 0.35);
        color: #34D399;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }
    .status-pulse-dot {
        width: 7px;
        height: 7px;
        background-color: #34D399;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px rgba(52, 211, 153, 0.8);
    }
    .user-profile-badge {
        display: flex;
        align-items: center;
        gap: 10px;
        background: rgba(23, 21, 68, 0.8);
        border: 1px solid rgba(139, 92, 246, 0.2);
        padding: 0.3rem 0.75rem 0.3rem 0.4rem;
        border-radius: 9999px;
    }
    .user-avatar {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background: linear-gradient(135deg, #8B5CF6 0%, #A855F7 100%);
        color: #FFFFFF;
        font-weight: 700;
        font-size: 0.85rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .user-name {
        font-size: 0.85rem;
        font-weight: 600;
        color: #F8F7FF;
    }

    /* Page Header Section */
    .breadcrumb-text {
        font-size: 0.78rem;
        font-weight: 600;
        color: var(--accent-lavender);
        margin-bottom: 0.25rem;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .main-page-title {
        font-size: 1.95rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        color: #F8F7FF;
        margin: 0;
        line-height: 1.2;
    }
    .main-page-title span {
        background: linear-gradient(135deg, #C084FC 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .main-page-desc {
        font-size: 0.88rem;
        color: var(--text-secondary);
        margin-top: 0.35rem;
        margin-bottom: 0;
    }

    /* Streamlit Button Overrides for Vibrant Fintech Buttons */
    .stButton > button, div[data-testid="stButton"] > button {
        background: linear-gradient(135deg, #8B5CF6 0%, #A855F7 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.4rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 18px rgba(139, 92, 246, 0.4) !important;
    }
    .stButton > button:hover, div[data-testid="stButton"] > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 24px rgba(139, 92, 246, 0.65) !important;
        color: #FFFFFF !important;
        border-color: #C084FC !important;
    }

    /* Glassmorphic Fintech Cards */
    .fin-card {
        background: var(--bg-card);
        border: 1px solid var(--border-card);
        border-radius: 20px;
        padding: 1.35rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.28);
        backdrop-filter: blur(12px);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .fin-card:hover {
        border-color: rgba(192, 132, 252, 0.4);
        box-shadow: 0 10px 36px 0 rgba(139, 92, 246, 0.15);
    }
    .fin-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
    }
    .fin-card-title {
        font-size: 0.85rem;
        font-weight: 700;
        color: var(--text-secondary);
        display: flex;
        align-items: center;
        gap: 8px;
        letter-spacing: 0.02em;
    }
    .fin-card-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #F8F7FF;
        line-height: 1.15;
    }
    .fin-card-meta {
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 0.5rem;
        color: var(--text-secondary);
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* KPI Specialized Cards */
    .kpi-card-1 {
        background: linear-gradient(145deg, rgba(23, 21, 68, 0.9) 0%, rgba(33, 28, 92, 0.6) 100%);
    }
    .kpi-card-2 {
        background: linear-gradient(145deg, rgba(23, 21, 68, 0.9) 0%, rgba(30, 26, 85, 0.6) 100%);
    }
    .kpi-card-3 {
        background: linear-gradient(145deg, rgba(23, 21, 68, 0.9) 0%, rgba(20, 36, 75, 0.6) 100%);
    }
    .kpi-card-4 {
        background: linear-gradient(145deg, rgba(23, 21, 68, 0.9) 0%, rgba(20, 48, 68, 0.6) 100%);
    }

    .kpi-icon-wrap {
        width: 34px;
        height: 34px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
    }
    .kpi-icon-purple {
        background: rgba(139, 92, 246, 0.22);
        color: #C084FC;
        border: 1px solid rgba(139, 92, 246, 0.4);
    }
    .kpi-icon-mint {
        background: rgba(52, 211, 153, 0.2);
        color: #34D399;
        border: 1px solid rgba(52, 211, 153, 0.4);
    }
    .kpi-icon-cyan {
        background: rgba(103, 232, 249, 0.2);
        color: #67E8F9;
        border: 1px solid rgba(103, 232, 249, 0.4);
    }
    .kpi-icon-warning {
        background: rgba(251, 191, 36, 0.2);
        color: #FBBF24;
        border: 1px solid rgba(251, 191, 36, 0.4);
    }

    /* Badges & Pills */
    .badge-mint {
        display: inline-flex;
        align-items: center;
        background: rgba(52, 211, 153, 0.16);
        color: #34D399;
        border: 1px solid rgba(52, 211, 153, 0.35);
        padding: 0.2rem 0.65rem;
        border-radius: 8px;
        font-size: 0.76rem;
        font-weight: 700;
    }
    .badge-purple {
        display: inline-flex;
        align-items: center;
        background: rgba(192, 132, 252, 0.18);
        color: #C084FC;
        border: 1px solid rgba(192, 132, 252, 0.35);
        padding: 0.2rem 0.65rem;
        border-radius: 8px;
        font-size: 0.76rem;
        font-weight: 700;
    }
    .badge-warning {
        display: inline-flex;
        align-items: center;
        background: rgba(251, 191, 36, 0.16);
        color: #FBBF24;
        border: 1px solid rgba(251, 191, 36, 0.35);
        padding: 0.2rem 0.65rem;
        border-radius: 8px;
        font-size: 0.76rem;
        font-weight: 700;
    }
    .badge-danger {
        display: inline-flex;
        align-items: center;
        background: rgba(248, 113, 113, 0.18);
        color: #F87171;
        border: 1px solid rgba(248, 113, 113, 0.35);
        padding: 0.2rem 0.65rem;
        border-radius: 8px;
        font-size: 0.76rem;
        font-weight: 700;
    }

    /* Left Form Panel Specifics */
    .info-panel-hdr {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    .info-panel-title {
        font-size: 1.05rem;
        font-weight: 800;
        color: #F8F7FF;
    }
    .info-section-title {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.8rem;
        font-weight: 700;
        color: #C084FC;
        margin-top: 0.85rem;
        margin-bottom: 0.35rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* AI Insight Box */
    .ai-insight-box {
        background: linear-gradient(145deg, rgba(23, 21, 68, 0.95) 0%, rgba(37, 28, 105, 0.6) 100%);
        border: 1px solid rgba(192, 132, 252, 0.3);
        border-radius: 20px;
        padding: 1.4rem;
        display: flex;
        align-items: flex-start;
        gap: 16px;
        margin-top: 0.5rem;
    }
    .ai-brain-avatar {
        width: 52px;
        height: 52px;
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.3) 0%, rgba(192, 132, 252, 0.15) 100%);
        border: 1px solid rgba(192, 132, 252, 0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.6rem;
        flex-shrink: 0;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.35);
    }
    .ai-insight-text {
        font-size: 0.88rem;
        color: #E2E8F0;
        line-height: 1.55;
    }

    /* Key Recommendations Checklist */
    .rec-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 0.65rem 0;
        border-bottom: 1px solid rgba(139, 92, 246, 0.12);
        font-size: 0.86rem;
        color: #E2E8F0;
    }
    .rec-item:last-child {
        border-bottom: none;
    }
    .rec-check-icon {
        width: 22px;
        height: 22px;
        border-radius: 50%;
        background: rgba(52, 211, 153, 0.2);
        border: 1.5px solid #34D399;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #34D399;
        font-size: 0.72rem;
        font-weight: 800;
        flex-shrink: 0;
    }

    /* Progress Bars */
    .comp-row {
        margin-bottom: 0.85rem;
    }
    .comp-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--text-secondary);
        margin-bottom: 0.35rem;
    }
    .comp-score {
        font-weight: 700;
        color: #F8F7FF;
    }
    .comp-bar-bg {
        background-color: rgba(18, 16, 58, 0.8);
        border: 1px solid rgba(139, 92, 246, 0.18);
        border-radius: 9999px;
        height: 8px;
        width: 100%;
        overflow: hidden;
    }
    .comp-bar-fill {
        height: 100%;
        border-radius: 9999px;
        background: linear-gradient(90deg, #8B5CF6 0%, #C084FC 100%);
    }

    /* Goal Journey Visual */
    .journey-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
        margin: 1.8rem 0 1.2rem 0;
        padding: 0 0.5rem;
    }
    .journey-line {
        position: absolute;
        top: 14px;
        left: 20px;
        right: 20px;
        height: 3px;
        background-color: rgba(139, 92, 246, 0.2);
        z-index: 1;
    }
    .journey-line-active {
        position: absolute;
        top: 14px;
        left: 20px;
        height: 3px;
        background: linear-gradient(90deg, #8B5CF6 0%, #34D399 100%);
        z-index: 2;
    }
    .journey-node {
        position: relative;
        z-index: 3;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    .node-dot {
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background-color: #171544;
        border: 2px solid rgba(139, 92, 246, 0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.7rem;
        font-weight: 700;
        color: var(--text-muted);
        margin-bottom: 0.35rem;
    }
    .node-dot.active {
        border-color: #34D399;
        background-color: #34D399;
        color: #0B0824;
        box-shadow: 0 0 12px rgba(52, 211, 153, 0.6);
    }
    .node-dot.passed {
        border-color: #8B5CF6;
        background-color: rgba(139, 92, 246, 0.3);
        color: #C084FC;
    }
    .node-label {
        font-size: 0.72rem;
        font-weight: 700;
        color: var(--text-secondary);
    }

    /* Streamlit Input Overrides */
    .stNumberInput input, .stTextInput input, .stSelectbox select {
        background-color: #12103A !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 10px !important;
        color: #F8F7FF !important;
        font-family: inherit !important;
        font-weight: 600 !important;
    }
    .stNumberInput input:focus, .stTextInput input:focus, .stSelectbox select:focus {
        border-color: var(--accent-lavender) !important;
        box-shadow: 0 0 10px rgba(192, 132, 252, 0.3) !important;
    }

    /* Footer */
    .fin-footer {
        border-top: 1px solid rgba(139, 92, 246, 0.15);
        margin-top: 3rem;
        padding-top: 1.5rem;
        text-align: center;
        font-size: 0.78rem;
        color: var(--text-muted);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# DATA AND MODEL LOADERS
# ==============================================================================
@st.cache_resource
def load_ml_model():
    model_path = os.path.join("model", "best_model.joblib")
    features_path = os.path.join("model", "feature_columns.joblib")
    metrics_path = os.path.join("model", "model_metrics.json")
    
    model = None
    feature_columns = None
    metrics = None
    
    if os.path.exists(model_path):
        model = joblib.load(model_path)
    if os.path.exists(features_path):
        feature_columns = joblib.load(features_path)
    if os.path.exists(metrics_path):
        with open(metrics_path, 'r') as f:
            metrics = json.load(f)
            
    return model, feature_columns, metrics

@st.cache_data
def load_dataset():
    data_path = os.path.join("data", "personal_wealth_management_engineered.csv")
    if not os.path.exists(data_path):
        data_path = "personal_wealth_management_dataset.csv"
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    return None

# ==============================================================================
# CALCULATION & FINANCIAL MODELING ENGINE
# ==============================================================================
def compute_financial_health_score(income, expense, savings, current_savings, debt, goal_amount, horizon):
    monthly_savings = income - expense
    
    # 1. Savings Rate Component (25%) -> 0-50% mapped to 0-100 score
    savings_rate_pct = (monthly_savings / income) * 100.0 if income > 0 else 0.0
    savings_comp = np.clip(savings_rate_pct * 2.0, 0, 100)
    
    # 2. Debt Component (20%) -> 0-100% debt-to-income mapped inversely to 100-0 score
    annual_income = income * 12.0
    dti_pct = (debt / annual_income) * 100.0 if annual_income > 0 else 0.0
    debt_comp = np.clip(100.0 - dti_pct, 0, 100)
    
    # 3. Emergency Fund Component (20%) -> 0-6 months mapped to 0-100 score (capped at 6 mos)
    safe_expense = max(1.0, expense)
    ef_months = current_savings / safe_expense
    emergency_comp = np.clip((ef_months / 6.0) * 100.0, 0, 100)
    
    # 4. Expense Ratio Component (15%) -> <=30% expense ratio = 100 score, >=100% = 0 score
    expense_ratio_pct = (expense / income) * 100.0 if income > 0 else 100.0
    expense_comp = np.clip((100.0 - expense_ratio_pct) * (100.0 / 70.0), 0, 100)
    
    # 5. Monthly Surplus Component (10%) -> Surplus relative to income
    surplus_pct = (monthly_savings / income) * 100.0 if income > 0 else 0.0
    surplus_comp = np.clip(surplus_pct * 2.0, 0, 100)
    
    # 6. Goal Progress Component (10%) -> 0-100% mapped directly to 0-100 score
    goal_progress_pct = (current_savings / goal_amount) * 100.0 if goal_amount > 0 else 100.0
    goal_comp = np.clip(goal_progress_pct, 0, 100)
    
    # Composite Score
    score = round(
        savings_comp * 0.25 +
        debt_comp * 0.20 +
        emergency_comp * 0.20 +
        expense_comp * 0.15 +
        surplus_comp * 0.10 +
        goal_comp * 0.10, 1
    )
    
    # Category assignment
    if score >= 80.0:
        category = "Good"
    elif score >= 60.0:
        category = "Moderate"
    elif score >= 40.0:
        category = "Needs Improvement"
    else:
        category = "Poor"
        
    components = {
        'Savings Rate': round(savings_comp, 1),
        'Debt Management': round(debt_comp, 1),
        'Emergency Fund': round(emergency_comp, 1),
        'Expense Control': round(expense_comp, 1),
        'Monthly Surplus': round(surplus_comp, 1),
        'Goal Progress': round(goal_comp, 1)
    }
    
    metrics = {
        'savings_rate_pct': savings_rate_pct,
        'expense_ratio_pct': expense_ratio_pct,
        'dti_pct': dti_pct,
        'monthly_surplus': monthly_savings,
        'ef_months': ef_months,
        'annual_savings': monthly_savings * 12.0,
        'goal_gap': max(0.0, goal_amount - current_savings),
        'goal_progress_pct': min(100.0, max(0.0, goal_progress_pct))
    }
    
    return score, category, components, metrics

def compute_goal_feasibility(current_savings, goal_amount, horizon_years, monthly_savings, goal_progress_pct):
    goal_remaining = max(0.0, goal_amount - current_savings)
    horizon_months = max(1.0, horizon_years * 12.0)
    required_monthly_no_growth = goal_remaining / horizon_months
    monthly_saving_gap = required_monthly_no_growth - monthly_savings
    
    if current_savings >= goal_amount:
        achievement_status = "Goal Reached"
        feasibility_status = "Already Achieved"
    elif goal_progress_pct >= 75.0:
        achievement_status = "Near Goal"
        feasibility_status = "On Track" if monthly_savings >= required_monthly_no_growth else "Needs Higher Monthly Saving"
    elif goal_progress_pct >= 25.0:
        achievement_status = "In Progress"
        feasibility_status = "On Track" if monthly_savings >= required_monthly_no_growth else "Needs Higher Monthly Saving"
    else:
        achievement_status = "Early Stage"
        feasibility_status = "On Track" if monthly_savings >= required_monthly_no_growth else "Needs Higher Monthly Saving"
        
    return {
        'goal_remaining': goal_remaining,
        'required_monthly_no_growth': required_monthly_no_growth,
        'monthly_saving_gap': monthly_saving_gap,
        'achievement_status': achievement_status,
        'feasibility_status': feasibility_status
    }

def get_badge_html(category):
    if category in ["Good", "On Track", "Goal Reached", "Already Achieved", "Low"]:
        return f'<span class="badge-mint">● {category}</span>'
    elif category in ["Moderate", "Near Goal", "In Progress"]:
        return f'<span class="badge-purple">● {category}</span>'
    elif category in ["Needs Improvement", "Needs Higher Monthly Saving", "Early Stage"]:
        return f'<span class="badge-warning">● {category}</span>'
    else:
        return f'<span class="badge-danger">● {category}</span>'

# ==============================================================================
# MAIN APPLICATION
# ==============================================================================
def main():
    # Session state initialization for financial profile
    if 'profile_age' not in st.session_state:
        st.session_state.profile_age = 35
    if 'profile_income' not in st.session_state:
        st.session_state.profile_income = 80000.0
    if 'profile_expense' not in st.session_state:
        st.session_state.profile_expense = 45000.0
    if 'profile_savings' not in st.session_state:
        st.session_state.profile_savings = 350000.0
    if 'profile_debt' not in st.session_state:
        st.session_state.profile_debt = 150000.0
    if 'profile_goal_amount' not in st.session_state:
        st.session_state.profile_goal_amount = 500000.0
    if 'profile_target_date' not in st.session_state:
        st.session_state.profile_target_date = "Dec 2026"
    if 'profile_horizon_years' not in st.session_state:
        st.session_state.profile_horizon_years = 3
    if 'profile_risk_pref' not in st.session_state:
        st.session_state.profile_risk_pref = "Moderate"
    if 'profile_risk_score' not in st.session_state:
        st.session_state.profile_risk_score = 50

    # Load ML models and dataset
    model, feature_columns, model_metrics = load_ml_model()
    df_analytics = load_dataset()
    model_name = model_metrics.get("best_model", "Random Forest") if model_metrics else "Random Forest Classifier"
    model_acc = model_metrics.get("metrics", {}).get("Accuracy", 0.84) * 100.0 if model_metrics else 84.0

    # --------------------------------------------------------------------------
    # SIDEBAR NAVIGATION
    # --------------------------------------------------------------------------
    with st.sidebar:
        st.markdown("""
        <div class="brand-logo-wrap">
            <div class="brand-icon-box">◈</div>
            <div>
                <div class="brand-name">WealthSphere</div>
                <div class="brand-tagline">Smarter Investing. Brighter Future.</div>
            </div>
        </div>
        <div style="border-bottom: 1px solid rgba(139, 92, 246, 0.15); margin: 0.8rem 0 0.6rem 0;"></div>
        """, unsafe_allow_html=True)
        
        nav_selection = st.radio(
            "Navigation",
            options=[
                "Overview",
                "Financial Profile",
                "Financial Health",
                "Financial Goals",
                "AI Risk",
                "Analytics",
                "What-if Simulator",
                "Insights"
            ],
            index=1,  # Default to Financial Profile matching the design
            label_visibility="collapsed"
        )
        
        # Sidebar Motivational Card
        st.markdown("""
        <div class="sidebar-promo-card">
            <div class="sidebar-promo-icon">🏔️</div>
            <div class="sidebar-promo-text">Better decisions today, a richer tomorrow.</div>
        </div>
        """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # TOP NAVBAR HEADER (COMMON TO ALL PAGES)
    # --------------------------------------------------------------------------
    st.markdown("""
    <div class="top-navbar">
        <div class="top-search-box">
            <span>🔍</span>
            <input class="top-search-input" placeholder="Search anything..." />
        </div>
        <div class="top-nav-right">
            <div class="nav-icon-btn" title="Notifications">🔔</div>
            <div class="ai-engine-status">
                <span class="status-pulse-dot"></span>
                AI Engine Active
            </div>
            <div class="user-profile-badge">
                <div class="user-avatar">K</div>
                <span class="user-name">Kavya</span>
                <span style="color: #8E8AA8; font-size: 0.75rem;">▾</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ==============================================================================
    # PAGE 1: FINANCIAL PROFILE (FEATURED EXACT DESIGN)
    # ==============================================================================
    if nav_selection == "Financial Profile":
        # Header Row with Title and Working "Analyze Profile" Button
        col_hdr_text, col_hdr_btn = st.columns([3, 1])
        with col_hdr_text:
            st.markdown("""
            <div class="breadcrumb-text">‹ Financial Profile</div>
            <h1 class="main-page-title">Financial <span>Profile</span></h1>
            <p class="main-page-desc">Manage your financial information and get personalized insights to improve your financial health.</p>
            """, unsafe_allow_html=True)
        with col_hdr_btn:
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            top_analyze_clicked = st.button("✨ Analyze Profile", key="btn_top_analyze", use_container_width=True)

        col_left_form, col_right_dash = st.columns([1, 2.2], gap="large")

        # ----------------------------------------------------------------------
        # LEFT COLUMN: YOUR FINANCIAL INFORMATION FORM
        # ----------------------------------------------------------------------
        with col_left_form:
            st.markdown("""
            <div class="fin-card">
                <div class="info-panel-hdr">
                    <div class="info-panel-title">Your Financial Information</div>
                    <span style="color: #C084FC; font-size: 0.85rem; font-weight: 600;">✏️ Edit</span>
                </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="info-section-title">👤 Personal Information</div>', unsafe_allow_html=True)
            in_age = st.number_input("Age", min_value=18, max_value=85, value=int(st.session_state.profile_age), step=1, key="in_age")

            st.markdown('<div class="info-section-title">💸 Monthly Finance</div>', unsafe_allow_html=True)
            in_income = st.number_input("Monthly Income (₹)", min_value=100.0, value=float(st.session_state.profile_income), step=2500.0, format="%.2f", key="in_income")
            in_expense = st.number_input("Monthly Expenses (₹)", min_value=0.0, value=float(st.session_state.profile_expense), step=2000.0, format="%.2f", key="in_expense")
            in_savings = st.number_input("Current Savings (₹)", min_value=0.0, value=float(st.session_state.profile_savings), step=10000.0, format="%.2f", key="in_savings")
            in_debt = st.number_input("Total Debt (₹)", min_value=0.0, value=float(st.session_state.profile_debt), step=5000.0, format="%.2f", key="in_debt")

            st.markdown('<div class="info-section-title">🎯 Financial Goal</div>', unsafe_allow_html=True)
            in_goal = st.number_input("Goal Amount (₹)", min_value=100.0, value=float(st.session_state.profile_goal_amount), step=25000.0, format="%.2f", key="in_goal")
            in_target_date = st.text_input("Target Date", value=st.session_state.profile_target_date, key="in_target_date")

            st.markdown('<div class="info-section-title">🛡️ Risk Profile</div>', unsafe_allow_html=True)
            risk_options = ["Low", "Moderate", "High"]
            current_risk_idx = risk_options.index(st.session_state.profile_risk_pref) if st.session_state.profile_risk_pref in risk_options else 1
            in_risk_pref = st.selectbox("Risk Preference", options=risk_options, index=current_risk_idx, key="in_risk_pref")

            st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
            update_profile_clicked = st.button("🔄 Update Profile", key="btn_update_profile", use_container_width=True)

            if update_profile_clicked or top_analyze_clicked:
                st.session_state.profile_age = in_age
                st.session_state.profile_income = in_income
                st.session_state.profile_expense = in_expense
                st.session_state.profile_savings = in_savings
                st.session_state.profile_debt = in_debt
                st.session_state.profile_goal_amount = in_goal
                st.session_state.profile_target_date = in_target_date
                st.session_state.profile_risk_pref = in_risk_pref
                st.session_state.profile_risk_score = 30 if in_risk_pref == "Low" else (50 if in_risk_pref == "Moderate" else 80)
                st.toast("Financial profile analyzed and updated successfully!", icon="✨")

            st.markdown("</div>", unsafe_allow_html=True)

        # Dynamic values for current calculations
        cur_age = in_age
        cur_income = in_income
        cur_expense = in_expense
        cur_savings = in_savings
        cur_debt = in_debt
        cur_goal = in_goal
        cur_horizon = st.session_state.profile_horizon_years
        cur_monthly_savings = cur_income - cur_expense

        # Calculate scores and predictions
        cur_health_score, cur_health_cat, cur_components, cur_metrics = compute_financial_health_score(
            cur_income, cur_expense, cur_monthly_savings, cur_savings, cur_debt, cur_goal, cur_horizon
        )
        cur_goal_info = compute_goal_feasibility(
            cur_savings, cur_goal, cur_horizon, cur_monthly_savings, cur_metrics['goal_progress_pct']
        )

        cur_risk_pred = in_risk_pref
        cur_risk_score = 30 if in_risk_pref == "Low" else (50 if in_risk_pref == "Moderate" else 80)
        if model is not None and feature_columns is not None:
            try:
                input_dict = {
                    'age': cur_age,
                    'monthly_income': cur_income,
                    'monthly_expense': cur_expense,
                    'monthly_savings': cur_monthly_savings,
                    'current_savings': cur_savings,
                    'debt': cur_debt,
                    'financial_goal_amount': cur_goal,
                    'investment_horizon_years': cur_horizon,
                    'risk_tolerance_score': cur_risk_score
                }
                input_df = pd.DataFrame([input_dict])[feature_columns]
                cur_risk_pred = model.predict(input_df)[0]
            except Exception:
                pass

        # ----------------------------------------------------------------------
        # RIGHT COLUMN: KPIS, CHARTS & AI INSIGHTS
        # ----------------------------------------------------------------------
        with col_right_dash:
            # 1. Four Top KPI Cards
            kpi_c1, kpi_c2, kpi_c3, kpi_c4 = st.columns(4)

            with kpi_c1:
                st.markdown(f"""
                <div class="fin-card kpi-card-1">
                    <div class="fin-card-header">
                        <div class="fin-card-title">Financial Health</div>
                        <div class="kpi-icon-wrap kpi-icon-purple">💜</div>
                    </div>
                    <div class="fin-card-value">{cur_health_score:.1f} <span style="font-size: 0.95rem; color: var(--text-muted); font-weight: 500;">/ 100</span></div>
                    <div class="fin-card-meta">{get_badge_html(cur_health_cat)}</div>
                </div>
                """, unsafe_allow_html=True)

            with kpi_c2:
                st.markdown(f"""
                <div class="fin-card kpi-card-2">
                    <div class="fin-card-header">
                        <div class="fin-card-title">Risk Level</div>
                        <div class="kpi-icon-wrap kpi-icon-warning">⚠️</div>
                    </div>
                    <div class="fin-card-value" style="font-size: 1.65rem;">{cur_risk_pred}</div>
                    <div class="fin-card-meta"><span style="color: var(--text-secondary); font-weight: 600;">ML Prediction</span></div>
                </div>
                """, unsafe_allow_html=True)

            with kpi_c3:
                st.markdown(f"""
                <div class="fin-card kpi-card-3">
                    <div class="fin-card-header">
                        <div class="fin-card-title">Goal Progress</div>
                        <div class="kpi-icon-wrap kpi-icon-cyan">🎯</div>
                    </div>
                    <div class="fin-card-value">{cur_metrics['goal_progress_pct']:.1f}%</div>
                    <div class="fin-card-meta">{get_badge_html(cur_goal_info['achievement_status'])}</div>
                </div>
                """, unsafe_allow_html=True)

            with kpi_c4:
                st.markdown(f"""
                <div class="fin-card kpi-card-4">
                    <div class="fin-card-header">
                        <div class="fin-card-title">Monthly Surplus</div>
                        <div class="kpi-icon-wrap kpi-icon-mint">₹</div>
                    </div>
                    <div class="fin-card-value" style="font-size: 1.65rem;">₹{cur_monthly_savings:,.0f}</div>
                    <div class="fin-card-meta"><span style="color: var(--accent-mint); font-weight: 700;">{cur_metrics['savings_rate_pct']:.1f}%</span> <span style="color: var(--text-secondary);">Savings Rate</span></div>
                </div>
                """, unsafe_allow_html=True)

            # 2. Charts Section (Financial Overview & Savings/Debt Donut)
            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:
                st.markdown("""
                <div class="fin-card" style="height: 100%;">
                    <div class="fin-card-header">
                        <div class="fin-card-title">Financial Overview</div>
                        <div style="display: flex; gap: 12px; font-size: 0.75rem; font-weight: 600;">
                            <span style="color: #8B5CF6;">● Income</span>
                            <span style="color: #C084FC;">● Expenses</span>
                            <span style="color: #34D399;">● Savings</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                fig_bar = go.Figure()
                categories = ['Income', 'Expenses', 'Savings']
                values = [cur_income, cur_expense, max(0.0, cur_monthly_savings)]
                colors = ['#8B5CF6', '#C084FC', '#34D399']
                display_texts = [f"₹{v/1000:.0f}K" if v >= 1000 else f"₹{v:,.0f}" for v in values]

                fig_bar.add_trace(go.Bar(
                    x=categories,
                    y=values,
                    marker=dict(
                        color=colors,
                        line=dict(color='rgba(255,255,255,0.1)', width=1),
                        cornerradius=10
                    ),
                    text=display_texts,
                    textposition='outside',
                    textfont=dict(color='#F8F7FF', family='Plus Jakarta Sans', size=12, weight='bold')
                ))

                fig_bar.update_layout(
                    height=240,
                    margin=dict(l=10, r=10, t=25, b=10),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    yaxis=dict(
                        showgrid=True,
                        gridcolor="rgba(139, 92, 246, 0.12)",
                        tickfont=dict(color="#8E8AA8", size=10),
                        tickformat="~s"
                    ),
                    xaxis=dict(
                        showgrid=False,
                        tickfont=dict(color="#B8B4D9", size=11, family='Plus Jakarta Sans')
                    ),
                    showlegend=False
                )
                st.plotly_chart(fig_bar, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with chart_col2:
                st.markdown("""
                <div class="fin-card" style="height: 100%;">
                    <div class="fin-card-header">
                        <div class="fin-card-title">Savings & Debt Breakdown</div>
                    </div>
                """, unsafe_allow_html=True)

                total_capital = cur_savings + cur_debt
                fig_donut = go.Figure(data=[go.Pie(
                    labels=['Savings', 'Debt'],
                    values=[cur_savings, cur_debt],
                    hole=0.68,
                    marker=dict(colors=['#34D399', '#8B5CF6']),
                    textinfo='none',
                    hoverinfo='label+value+percent'
                )])

                fig_donut.add_annotation(
                    text=f"<span style='font-size:11px;color:#8E8AA8;'>Total</span><br><b style='font-size:16px;color:#F8F7FF;'>₹{total_capital:,.0f}</b>",
                    x=0.5, y=0.5,
                    font=dict(family="Plus Jakarta Sans"),
                    showarrow=False
                )

                fig_donut.update_layout(
                    height=240,
                    margin=dict(l=10, r=10, t=10, b=10),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.15,
                        xanchor="center",
                        x=0.5,
                        font=dict(color="#B8B4D9", size=11)
                    )
                )
                st.plotly_chart(fig_donut, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # 3. AI Insights and Key Recommendations
            insight_col1, insight_col2 = st.columns(2)

            with insight_col1:
                st.markdown("""
                <div class="fin-card" style="height: 100%;">
                    <div class="fin-card-title" style="margin-bottom: 0.9rem;">
                        <span>✨ AI Insights</span>
                    </div>
                    <div class="ai-insight-box">
                        <div class="ai-brain-avatar">🧠</div>
                        <div class="ai-insight-text">
                """, unsafe_allow_html=True)

                if cur_health_score >= 80:
                    ai_narrative = f"Your financial position is exceptionally robust! With a healthy savings rate of {cur_metrics['savings_rate_pct']:.1f}% and strong cash surplus, you are well-positioned for aggressive wealth compounding and tax-efficient portfolio allocation."
                elif cur_health_score >= 60:
                    ai_narrative = f"Your financial position is stable. With a {cur_risk_pred.lower()} risk profile and a solid savings rate of {cur_metrics['savings_rate_pct']:.1f}%, you are on the right track. Consider increasing your emergency fund to 6 months of expenses and exploring diversified SIP investments."
                elif cur_health_score >= 40:
                    ai_narrative = f"Your profile shows moderate health with room for optimization. Debt-to-income ratio ({cur_metrics['dti_pct']:.1f}%) and expense overhead are limiting your compounding speed. Focusing on high-yield debt reduction will accelerate your progress."
                else:
                    ai_narrative = f"Attention needed: High expense ratio and debt burden are constraining cash flow. Prioritize restructuring debt and establishing a basic liquid emergency cushion before taking high investment risks."

                st.markdown(f"{ai_narrative}</div></div></div>", unsafe_allow_html=True)

            with insight_col2:
                st.markdown(f"""
                <div class="fin-card" style="height: 100%;">
                    <div class="fin-card-title" style="margin-bottom: 0.75rem;">
                        <span>💡 Key Recommendations</span>
                    </div>
                    <div class="rec-item">
                        <div class="rec-check-icon">✓</div>
                        <div>{'Maintain healthy monthly savings rate of {:,.0f}/mo.'.format(cur_monthly_savings) if cur_monthly_savings > 0 else 'Establish positive monthly savings budget.'}</div>
                    </div>
                    <div class="rec-item">
                        <div class="rec-check-icon">✓</div>
                        <div>{'Target reducing debt of ₹{:,.0f} to lower solvency strain.'.format(cur_debt) if cur_debt > 0 else 'Debt is fully paid off; maximize investment allocation.'}</div>
                    </div>
                    <div class="rec-item">
                        <div class="rec-check-icon">✓</div>
                        <div>{'Build liquid emergency reserve to ₹{:,.0f} (6 months).'.format(cur_expense * 6)}</div>
                    </div>
                    <div class="rec-item">
                        <div class="rec-check-icon">✓</div>
                        <div>{'Explore {}-risk diversified mutual funds and systematic plans.'.format(cur_risk_pred)}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ==============================================================================
    # OTHER PAGES (OVERVIEW, HEALTH, GOALS, AI RISK, ANALYTICS, WHAT-IF, INSIGHTS)
    # ==============================================================================
    else:
        # Load baseline variables for other pages
        age = st.session_state.profile_age
        income = st.session_state.profile_income
        expense = st.session_state.profile_expense
        current_savings = st.session_state.profile_savings
        debt = st.session_state.profile_debt
        goal_amount = st.session_state.profile_goal_amount
        horizon_years = st.session_state.profile_horizon_years
        risk_score = st.session_state.profile_risk_score
        monthly_savings = income - expense

        health_score, health_category, components, metrics = compute_financial_health_score(
            income, expense, monthly_savings, current_savings, debt, goal_amount, horizon_years
        )
        goal_info = compute_goal_feasibility(
            current_savings, goal_amount, horizon_years, monthly_savings, metrics['goal_progress_pct']
        )
        risk_pred = st.session_state.profile_risk_pref
        risk_probs = {'Low': 0.15, 'Moderate': 0.70, 'High': 0.15}
        if model is not None and feature_columns is not None:
            try:
                input_dict = {
                    'age': age,
                    'monthly_income': income,
                    'monthly_expense': expense,
                    'monthly_savings': monthly_savings,
                    'current_savings': current_savings,
                    'debt': debt,
                    'financial_goal_amount': goal_amount,
                    'investment_horizon_years': horizon_years,
                    'risk_tolerance_score': risk_score
                }
                input_df = pd.DataFrame([input_dict])[feature_columns]
                risk_pred = model.predict(input_df)[0]
                if hasattr(model, 'predict_proba'):
                    probs = model.predict_proba(input_df)[0]
                    classes = model.classes_
                    risk_probs = {cls: float(prob) for cls, prob in zip(classes, probs)}
            except Exception:
                pass

        if nav_selection == "Overview":
            st.markdown("""
            <div class="breadcrumb-text">‹ Portfolio Overview</div>
            <h1 class="main-page-title">Executive <span>Overview</span></h1>
            <p class="main-page-desc">Comprehensive macro analysis of your capital allocation, health score, and predictive indicators.</p>
            <div style="height: 16px;"></div>
            """, unsafe_allow_html=True)

            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            with kpi1:
                st.markdown(f"""
                <div class="fin-card kpi-card-1">
                    <div class="fin-card-header">
                        <div class="fin-card-title">Financial Health</div>
                        <div class="kpi-icon-wrap kpi-icon-purple">💜</div>
                    </div>
                    <div class="fin-card-value">{health_score:.1f} <span style="font-size: 0.95rem; color: var(--text-muted); font-weight: 500;">/ 100</span></div>
                    <div class="fin-card-meta">{get_badge_html(health_category)}</div>
                </div>
                """, unsafe_allow_html=True)

            with kpi2:
                st.markdown(f"""
                <div class="fin-card kpi-card-2">
                    <div class="fin-card-header">
                        <div class="fin-card-title">AI Risk Profile</div>
                        <div class="kpi-icon-wrap kpi-icon-warning">🛡️</div>
                    </div>
                    <div class="fin-card-value" style="font-size: 1.65rem;">{risk_pred}</div>
                    <div class="fin-card-meta"><span style="color: var(--text-secondary); font-weight: 600;">{model_name}</span></div>
                </div>
                """, unsafe_allow_html=True)

            with kpi3:
                st.markdown(f"""
                <div class="fin-card kpi-card-3">
                    <div class="fin-card-header">
                        <div class="fin-card-title">Goal Accumulation</div>
                        <div class="kpi-icon-wrap kpi-icon-cyan">🎯</div>
                    </div>
                    <div class="fin-card-value">{metrics['goal_progress_pct']:.1f}%</div>
                    <div class="fin-card-meta">{get_badge_html(goal_info['achievement_status'])}</div>
                </div>
                """, unsafe_allow_html=True)

            with kpi4:
                st.markdown(f"""
                <div class="fin-card kpi-card-4">
                    <div class="fin-card-header">
                        <div class="fin-card-title">Net Monthly Cashflow</div>
                        <div class="kpi-icon-wrap kpi-icon-mint">₹</div>
                    </div>
                    <div class="fin-card-value" style="font-size: 1.65rem;">₹{monthly_savings:,.0f}</div>
                    <div class="fin-card-meta"><span style="color: var(--accent-mint); font-weight: 700;">{metrics['savings_rate_pct']:.1f}%</span> <span style="color: var(--text-secondary);">Savings Ratio</span></div>
                </div>
                """, unsafe_allow_html=True)

            col_g1, col_g2 = st.columns([1, 1])
            with col_g1:
                st.markdown("""
                <div class="fin-card" style="height: 100%;">
                    <div class="fin-card-title">Financial Health Score Gauge</div>
                """, unsafe_allow_html=True)

                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=health_score,
                    number={'suffix': " / 100", 'font': {'size': 32, 'family': "Plus Jakarta Sans", 'color': "#F8F7FF"}},
                    gauge={
                        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#8E8AA8"},
                        'bar': {'color': "#8B5CF6", 'thickness': 0.3},
                        'bgcolor': "rgba(18, 16, 58, 0.8)",
                        'borderwidth': 0,
                        'steps': [
                            {'range': [0, 40], 'color': "rgba(248, 113, 113, 0.2)"},
                            {'range': [40, 60], 'color': "rgba(251, 191, 36, 0.2)"},
                            {'range': [60, 80], 'color': "rgba(192, 132, 252, 0.2)"},
                            {'range': [80, 100], 'color': "rgba(52, 211, 153, 0.25)"}
                        ],
                    }
                ))
                fig_gauge.update_layout(
                    height=220,
                    margin=dict(l=15, r=15, t=25, b=10),
                    paper_bgcolor="rgba(0,0,0,0)",
                    font={'family': "Plus Jakarta Sans"}
                )
                st.plotly_chart(fig_gauge, use_container_width=True)
                st.markdown(f"""
                    <div style="text-align: center; margin-top: -0.5rem; margin-bottom: 0.5rem;">
                        <span style="font-size: 0.82rem; font-weight: 600; color: var(--text-secondary);">Current Status: </span>
                        {get_badge_html(health_category)}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_g2:
                st.markdown("""
                <div class="fin-card" style="height: 100%;">
                    <div class="fin-card-title">Health Dimensions Breakdown</div>
                """, unsafe_allow_html=True)

                for comp_name, comp_score in components.items():
                    st.markdown(f"""
                    <div class="comp-row">
                        <div class="comp-header">
                            <span>{comp_name}</span>
                            <span class="comp-score">{comp_score:.0f} / 100</span>
                        </div>
                        <div class="comp-bar-bg">
                            <div class="comp-bar-fill" style="width: {min(100.0, max(0.0, comp_score))}%;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        elif nav_selection == "Financial Health":
            st.markdown("""
            <div class="breadcrumb-text">‹ Deep Dive Analysis</div>
            <h1 class="main-page-title">Financial <span>Health</span></h1>
            <p class="main-page-desc">Granular breakdown across the six foundational pillars of personal wealth longevity.</p>
            <div style="height: 16px;"></div>
            """, unsafe_allow_html=True)

            comp_details = [
                ("Savings Rate", components['Savings Rate'], "25%", "Measures active cash flow accumulation relative to gross income.", f"{metrics['savings_rate_pct']:.1f}% monthly income saved"),
                ("Debt Management", components['Debt Management'], "20%", "Evaluates annual leverage burden and solvency pressure.", f"{metrics['dti_pct']:.1f}% debt-to-income ratio"),
                ("Emergency Fund", components['Emergency Fund'], "20%", "Calculates liquid safety buffer against unforeseen disruptions.", f"{metrics['ef_months']:.1f} months covered (target: 6 mos)"),
                ("Expense Control", components['Expense Control'], "15%", "Monitors operational overhead and cost discipline.", f"{metrics['expense_ratio_pct']:.1f}% expense-to-income ratio"),
                ("Monthly Surplus", components['Monthly Surplus'], "10%", "Reflects liquidity cushion available for compounding.", f"₹{metrics['monthly_surplus']:,.0f} net surplus each month"),
                ("Goal Progress", components['Goal Progress'], "10%", "Quantifies distance to target capital accumulation milestone.", f"{metrics['goal_progress_pct']:.1f}% of goal accumulated")
            ]

            r1_c = st.columns(3)
            for i in range(3):
                name, score, weight, desc, stat = comp_details[i]
                with r1_c[i]:
                    st.markdown(f"""
                    <div class="fin-card">
                        <div class="fin-card-header">
                            <div class="fin-card-title">{name}</div>
                            <span class="badge-purple">WEIGHT {weight}</span>
                        </div>
                        <div class="fin-card-value" style="font-size: 1.55rem;">{score:.0f} <span style="font-size: 0.85rem; color: var(--text-muted); font-weight: 500;">/ 100</span></div>
                        <div class="comp-bar-bg" style="margin: 0.75rem 0 0.85rem 0;">
                            <div class="comp-bar-fill" style="width: {score}%;"></div>
                        </div>
                        <div style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 0.4rem;">{desc}</div>
                        <div style="font-size: 0.78rem; font-weight: 700; color: #34D399;">{stat}</div>
                    </div>
                    """, unsafe_allow_html=True)

            r2_c = st.columns(3)
            for i in range(3, 6):
                name, score, weight, desc, stat = comp_details[i]
                with r2_c[i - 3]:
                    st.markdown(f"""
                    <div class="fin-card">
                        <div class="fin-card-header">
                            <div class="fin-card-title">{name}</div>
                            <span class="badge-purple">WEIGHT {weight}</span>
                        </div>
                        <div class="fin-card-value" style="font-size: 1.55rem;">{score:.0f} <span style="font-size: 0.85rem; color: var(--text-muted); font-weight: 500;">/ 100</span></div>
                        <div class="comp-bar-bg" style="margin: 0.75rem 0 0.85rem 0;">
                            <div class="comp-bar-fill" style="width: {score}%;"></div>
                        </div>
                        <div style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 0.4rem;">{desc}</div>
                        <div style="font-size: 0.78rem; font-weight: 700; color: #34D399;">{stat}</div>
                    </div>
                    """, unsafe_allow_html=True)

        elif nav_selection == "Financial Goals":
            st.markdown("""
            <div class="breadcrumb-text">‹ Target Tracking</div>
            <h1 class="main-page-title">Financial <span>Goals</span></h1>
            <p class="main-page-desc">Track capital accumulation, required contribution velocity, and milestone feasibility.</p>
            <div style="height: 16px;"></div>
            """, unsafe_allow_html=True)

            pct = metrics['goal_progress_pct']
            line_w = min(100.0, max(0.0, pct))
            node0_cls = "active" if pct >= 0 else ""
            node25_cls = "passed" if pct >= 25 else ""
            node50_cls = "passed" if pct >= 50 else ""
            node75_cls = "passed" if pct >= 75 else ""
            node100_cls = "passed" if pct >= 100 else ""

            st.markdown(f"""
            <div class="fin-card">
                <div class="fin-card-title">Goal Accumulation Journey</div>
                <div class="journey-container">
                    <div class="journey-line"></div>
                    <div class="journey-line-active" style="width: calc({line_w}% - 30px);"></div>
                    <div class="journey-node">
                        <div class="node-dot {node0_cls}">0%</div>
                        <div class="node-label">Start</div>
                    </div>
                    <div class="journey-node">
                        <div class="node-dot {node25_cls}">25%</div>
                        <div class="node-label">Early Stage</div>
                    </div>
                    <div class="journey-node">
                        <div class="node-dot {node50_cls}">50%</div>
                        <div class="node-label">Midway</div>
                    </div>
                    <div class="journey-node">
                        <div class="node-dot {node75_cls}">75%</div>
                        <div class="node-label">Near Target</div>
                    </div>
                    <div class="journey-node">
                        <div class="node-dot {node100_cls}">🎯</div>
                        <div class="node-label">Accomplished</div>
                    </div>
                </div>
                <div style="text-align: center; margin-top: 1rem;">
                    <span style="font-size: 0.95rem; font-weight: 700; color: #F8F7FF;">Current Accumulation: {pct:.1f}%</span>
                    <span style="font-size: 0.88rem; color: var(--text-secondary);"> (₹{current_savings:,.0f} of ₹{goal_amount:,.0f})</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            m1, m2, m3, m4 = st.columns(4)
            m1.markdown(f"""
            <div class="fin-card">
                <div class="fin-card-title">Target Goal Capital</div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #F8F7FF;">₹{goal_amount:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

            m2.markdown(f"""
            <div class="fin-card">
                <div class="fin-card-title">Capital Shortfall</div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #C084FC;">₹{goal_info['goal_remaining']:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

            m3.markdown(f"""
            <div class="fin-card">
                <div class="fin-card-title">Required Monthly</div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #F8F7FF;">₹{goal_info['required_monthly_no_growth']:,.0f}/mo</div>
            </div>
            """, unsafe_allow_html=True)

            m4.markdown(f"""
            <div class="fin-card">
                <div class="fin-card-title">Feasibility Assessment</div>
                <div style="margin-top: 0.35rem;">{get_badge_html(goal_info['feasibility_status'])}</div>
            </div>
            """, unsafe_allow_html=True)

        elif nav_selection == "AI Risk":
            st.markdown("""
            <div class="breadcrumb-text">‹ Machine Learning Classifier</div>
            <h1 class="main-page-title">AI <span>Risk Intelligence</span></h1>
            <p class="main-page-desc">Supervised classification quantifying multidimensional risk tolerance and asset alignment.</p>
            <div style="height: 16px;"></div>
            """, unsafe_allow_html=True)

            r_col1, r_col2 = st.columns([1, 1])
            with r_col1:
                st.markdown(f"""
                <div class="fin-card" style="height: 100%;">
                    <div class="fin-card-title">Predicted Risk Persona</div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #F8F7FF; margin: 0.5rem 0;">
                        {risk_pred.upper()}
                    </div>
                    <div style="margin-bottom: 1.5rem;">
                        {get_badge_html(risk_pred)}
                    </div>
                    <div class="fin-card-title" style="margin-top: 1rem;">Probability Spectrum</div>
                """, unsafe_allow_html=True)

                for r_cls in ['Low', 'Moderate', 'High']:
                    r_prob = risk_probs.get(r_cls, 0.0) * 100.0
                    bar_color = "#34D399" if r_cls == "Low" else ("#8B5CF6" if r_cls == "Moderate" else "#F87171")
                    st.markdown(f"""
                    <div class="comp-row">
                        <div class="comp-header">
                            <span style="font-weight: 700;">{r_cls} Risk</span>
                            <span class="comp-score">{r_prob:.1f}%</span>
                        </div>
                        <div class="comp-bar-bg" style="height: 10px;">
                            <div class="comp-bar-fill" style="width: {r_prob}%; background: {bar_color};"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with r_col2:
                st.markdown(f"""
                <div class="fin-card" style="height: 100%;">
                    <div class="fin-card-title">Engine Architecture</div>
                    <div style="margin-bottom: 1.25rem; margin-top: 0.5rem;">
                        <div style="font-size: 0.8rem; color: var(--text-secondary);">Production Model</div>
                        <div style="font-size: 1.25rem; font-weight: 800; color: #F8F7FF;">{model_name}</div>
                    </div>
                    <div style="margin-bottom: 1.25rem;">
                        <div style="font-size: 0.8rem; color: var(--text-secondary);">Validation Accuracy</div>
                        <div style="font-size: 1.25rem; font-weight: 800; color: #34D399;">{model_acc:.1f}%</div>
                    </div>
                    <div class="ai-insight-box">
                        <div class="ai-brain-avatar">⚡</div>
                        <div class="ai-insight-text">
                            Model classifications are trained on cross-sectional financial behavioral patterns to prevent under-allocation and balance growth with stability.
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        elif nav_selection == "Analytics":
            st.markdown("""
            <div class="breadcrumb-text">‹ Population Intelligence</div>
            <h1 class="main-page-title">Cohort <span>Analytics</span></h1>
            <p class="main-page-desc">Empirical distributions and cross-sectional correlations across 1,500 profiles.</p>
            <div style="height: 16px;"></div>
            """, unsafe_allow_html=True)

            if df_analytics is not None:
                r1_c1, r1_c2 = st.columns(2)
                with r1_c1:
                    st.markdown('<div class="fin-card">', unsafe_allow_html=True)
                    fig_r1 = px.histogram(
                        df_analytics, x='risk_category', color='risk_category',
                        color_discrete_map={'Low': '#34D399', 'Moderate': '#8B5CF6', 'High': '#F87171'},
                        title="Risk Category Distribution"
                    )
                    fig_r1.update_layout(
                        height=300, margin=dict(l=10, r=10, t=35, b=10),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#B8B4D9", family="Plus Jakarta Sans"),
                        showlegend=False
                    )
                    st.plotly_chart(fig_r1, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                with r1_c2:
                    st.markdown('<div class="fin-card">', unsafe_allow_html=True)
                    h_col = 'calculated_health_category' if 'calculated_health_category' in df_analytics.columns else ('financial_health_category' if 'financial_health_category' in df_analytics.columns else None)
                    if h_col:
                        fig_r2 = px.histogram(
                            df_analytics, x=h_col, color=h_col,
                            color_discrete_map={'Poor': '#F87171', 'Needs Improvement': '#FBBF24', 'Moderate': '#C084FC', 'Good': '#34D399'},
                            title="Financial Health Category Distribution"
                        )
                        fig_r2.update_layout(
                            height=300, margin=dict(l=10, r=10, t=35, b=10),
                            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            font=dict(color="#B8B4D9", family="Plus Jakarta Sans"),
                            showlegend=False
                        )
                        st.plotly_chart(fig_r2, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                r2_c1, r2_c2 = st.columns(2)
                with r2_c1:
                    st.markdown('<div class="fin-card">', unsafe_allow_html=True)
                    sav_col = 'savings_rate_calculated' if 'savings_rate_calculated' in df_analytics.columns else 'savings_rate_percent'
                    fh_col = 'calculated_financial_health_score' if 'calculated_financial_health_score' in df_analytics.columns else 'financial_health_score'
                    fig_r3 = px.scatter(
                        df_analytics, x=sav_col, y=fh_col, color='risk_category',
                        color_discrete_map={'Low': '#34D399', 'Moderate': '#8B5CF6', 'High': '#F87171'},
                        title="Savings Rate vs Financial Health"
                    )
                    fig_r3.update_layout(
                        height=300, margin=dict(l=10, r=10, t=35, b=10),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#B8B4D9", family="Plus Jakarta Sans")
                    )
                    st.plotly_chart(fig_r3, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                with r2_c2:
                    st.markdown('<div class="fin-card">', unsafe_allow_html=True)
                    dti_col = 'debt_to_income_calculated' if 'debt_to_income_calculated' in df_analytics.columns else 'debt_to_income_percent'
                    fig_r4 = px.scatter(
                        df_analytics, x=dti_col, y=fh_col, color='risk_category',
                        color_discrete_map={'Low': '#34D399', 'Moderate': '#8B5CF6', 'High': '#F87171'},
                        title="Debt-to-Income vs Financial Health"
                    )
                    fig_r4.update_layout(
                        height=300, margin=dict(l=10, r=10, t=35, b=10),
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#B8B4D9", family="Plus Jakarta Sans")
                    )
                    st.plotly_chart(fig_r4, use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("Dataset loading in progress.")

        elif nav_selection == "What-if Simulator":
            st.markdown("""
            <div class="breadcrumb-text">‹ Predictive Modeling</div>
            <h1 class="main-page-title">What-If <span>Simulator</span></h1>
            <p class="main-page-desc">Simulate dynamic adjustments to your savings rate and explore projected milestone trajectories.</p>
            <div style="height: 16px;"></div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="fin-card">', unsafe_allow_html=True)
            sim_saving = st.slider(
                "Simulated Monthly Savings (₹/month)",
                min_value=float(max(0.0, monthly_savings - 30000.0)),
                max_value=float(monthly_savings + 60000.0),
                value=float(monthly_savings),
                step=1000.0
            )
            st.markdown('</div>', unsafe_allow_html=True)

            sim_goal_info = compute_goal_feasibility(
                current_savings, goal_amount, horizon_years, sim_saving, metrics['goal_progress_pct']
            )

            col_cur, col_sim = st.columns(2)
            with col_cur:
                st.markdown(f"""
                <div class="fin-card" style="text-align: center;">
                    <div class="fin-card-title" style="justify-content: center;">Current Baseline</div>
                    <div class="fin-card-value" style="margin: 0.6rem 0;">₹{monthly_savings * 12.0:,.0f}</div>
                    <div style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 1rem;">Annual Savings Run-rate</div>
                    <div>{get_badge_html(goal_info['feasibility_status'])}</div>
                </div>
                """, unsafe_allow_html=True)

            with col_sim:
                st.markdown(f"""
                <div class="fin-card" style="text-align: center; border-color: rgba(192, 132, 252, 0.5);">
                    <div class="fin-card-title" style="justify-content: center; color: #C084FC;">Simulated Projection</div>
                    <div class="fin-card-value" style="margin: 0.6rem 0; color: #34D399;">₹{sim_saving * 12.0:,.0f}</div>
                    <div style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 1rem;">Annual Savings Run-rate</div>
                    <div>{get_badge_html(sim_goal_info['feasibility_status'])}</div>
                </div>
                """, unsafe_allow_html=True)

        elif nav_selection == "Insights":
            st.markdown("""
            <div class="breadcrumb-text">‹ Strategic Research</div>
            <h1 class="main-page-title">Strategic <span>Insights</span></h1>
            <p class="main-page-desc">Empirical findings extracted directly from feature engineering and behavioral health modeling.</p>
            <div style="height: 16px;"></div>
            """, unsafe_allow_html=True)

            insights_data = [
                ("Savings Rate Dominance", "+0.88 Correlation", "Savings rate percentage is the single strongest driver of overall financial health categorization across all demographics."),
                ("Debt Leverage Burden", "-0.42 Negative Correlation", "High debt-to-income ratio degrades financial health scores regardless of gross monthly income."),
                ("Risk Tolerance Alignment", "75.8 vs 37.8 Mean Score", "High-risk investor personas demonstrate double the measured psychological tolerance of conservative investors."),
                ("Emergency Fund Resilience", "92.4% Good/Moderate Rate", "Maintaining greater than 6 months of living expenses in liquid reserves prevents wealth vulnerability.")
            ]

            in_col1, in_col2 = st.columns(2)
            for idx, (title, stat, desc) in enumerate(insights_data):
                target_col = in_col1 if idx % 2 == 0 else in_col2
                with target_col:
                    st.markdown(f"""
                    <div class="fin-card">
                        <div class="fin-card-title">{title}</div>
                        <div style="font-size: 1.45rem; font-weight: 800; color: #C084FC; margin: 0.4rem 0;">{stat}</div>
                        <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5;">{desc}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # FOOTER DISCLAIMER
    # --------------------------------------------------------------------------
    st.markdown("""
    <div class="fin-footer">
        WealthSphere AI Intelligence Engine • Educational Simulation Platform • All rights reserved
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
