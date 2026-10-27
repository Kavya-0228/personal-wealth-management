# -*- coding: utf-8 -*-
import os
import json
import base64
import joblib
import textwrap
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# STREAMLIT PAGE CONFIGURATION & SYSTEM CLEANUP
# ==============================================================================
st.set_page_config(
    page_title="WealthSphere | Personal Financial Intelligence",
    page_icon="W",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper function to convert local image to base64 data URI
@st.cache_data
def get_image_base64(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            return f"data:image/jpeg;base64,{data}"
    return ""

banner_base64 = get_image_base64(os.path.join("assets", "banner.jpg"))

# ==============================================================================
# WEALTHSPHERE COMPETITION FINTECH DESIGN SYSTEM
# Palette: #F0F4FA (Bg), #24163D (Sidebar), #6D28D9 (Primary), #A78BFA (Lavender Accent),
# #059669 (Success), #D97706 (Warning), #DC2626 (Danger), #24183B (Text)
# ==============================================================================
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --bg-main: #F0F4FA;
        --sidebar-bg: #24163D;
        --primary: #6D28D9;
        --primary-light: #F3EBFF;
        --secondary: #A78BFA;
        --secondary-light: #EDE4FF;
        --success: #059669;
        --success-light: #EAFBF5;
        --warning: #D97706;
        --warning-light: #FFF4E5;
        --danger: #DC2626;
        --danger-light: #FEECEC;
        --text-dark: #24183B;
        --text-muted: #6B6480;
        --text-subtle: #8A7E9D;
        --card-bg: #FFFFFF;
        --border-color: #DDD0FF;
        --radius-lg: 16px;
        --radius-md: 12px;
        --radius-sm: 8px;
        --card-shadow: 0 1px 3px rgba(36, 24, 59, 0.04), 0 6px 16px rgba(36, 24, 59, 0.03);
        --card-shadow-hover: 0 8px 24px rgba(167, 139, 250, 0.12);
    }

    /* Hide default Streamlit clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}
    [data-testid="stDecoration"] {visibility: hidden;}
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stSidebar"],
    [data-testid="stSidebarHeader"] {
        border-top: none !important;
        box-shadow: none !important;
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    [data-testid="stAppViewContainer"]::before,
    [data-testid="stAppViewContainer"]::after,
    [data-testid="stHeader"]::before,
    [data-testid="stHeader"]::after,
    [data-testid="stSidebar"]::before,
    [data-testid="stSidebar"]::after,
    [data-testid="stSidebarHeader"]::before,
    [data-testid="stSidebarHeader"]::after {
        content: none !important;
        display: none !important;
    }

    [data-testid="stExpandSidebarButton"] {
        position: fixed !important;
        top: 0.5rem !important;
        left: 0.5rem !important;
        z-index: 1001 !important;
        visibility: visible !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 2rem !important;
        height: 2rem !important;
        padding: 0 !important;
        border: 0 !important;
        background: transparent !important;
        box-shadow: none !important;
        cursor: pointer !important;
    }
    [data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"] {
        position: relative;
        width: 16px;
        height: 16px;
        font-size: 0 !important;
        color: transparent !important;
    }
    [data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"]::after {
        content: "";
        position: absolute;
        top: 4px;
        left: 3px;
        width: 7px;
        height: 7px;
        border-top: 2px solid #6B6480;
        border-right: 2px solid #6B6480;
        transform: rotate(45deg);
    }

    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div:first-child {
        background: #24163D !important;
    }
    [data-testid="stSidebarHeader"],
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarUserContent"] {
        background: #24163D !important;
    }
    [data-testid="stSidebar"] {
        width: 250px !important;
        min-width: 250px !important;
        max-width: 250px !important;
        border-right: 1px solid rgba(167, 139, 250, 0.16);
        overflow-x: hidden !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding: 1rem 0.75rem 0.75rem !important;
    }
    [data-testid="stSidebarHeader"] {
        height: 40px !important;
        min-height: 40px !important;
        padding: 0 0.5rem !important;
    }
    [data-testid="stSidebarHeader"] button,
    [data-testid="stSidebarHeader"] [data-testid="stIconMaterial"] {
        visibility: visible !important;
    }
    [data-testid="stSidebarHeader"] button {
        color: #B9AECF !important;
    }
    [data-testid="stSidebarHeader"] [data-testid="stIconMaterial"] {
        color: #B9AECF !important;
    }
    .ws-sidebar-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.25rem 0.25rem 1rem;
    }
    .ws-sidebar-mark {
        display: grid;
        place-items: center;
        width: 42px;
        height: 42px;
        flex: 0 0 42px;
        border-radius: 13px;
        background: #332454;
        color: #A78BFA;
        font-size: 1.45rem;
        font-weight: 700;
        box-shadow: inset 0 0 0 1px rgba(167, 139, 250, 0.2);
    }
    .ws-sidebar-name {
        color: #FFFFFF;
        font-size: 1.05rem;
        font-weight: 800;
        line-height: 1.2;
    }
    .ws-sidebar-caption {
        margin-top: 0.2rem;
        color: #B9AECF;
        font-size: 0.68rem;
        font-weight: 600;
    }
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #B9AECF !important;
        font-size: 0.68rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.06em;
    }
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: #B9AECF !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] > label {
        display: none;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] {
        display: flex !important;
        flex-direction: column !important;
        gap: 0.2rem !important;
        padding: 0 !important;
        border: 0 !important;
        background: transparent !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label {
        display: flex !important;
        align-items: center !important;
        box-sizing: border-box !important;
        width: 100% !important;
        min-width: 0 !important;
        min-height: 40px;
        flex: 0 0 auto !important;
        padding: 0.45rem 0.65rem !important;
        border: 1px solid transparent !important;
        border-radius: 9px !important;
        background: transparent !important;
        color: #E8E2F2 !important;
        white-space: nowrap !important;
        text-align: left !important;
        transition: background 150ms ease, border-color 150ms ease, color 150ms ease;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:hover {
        background: rgba(167, 139, 250, 0.12) !important;
        border-color: rgba(167, 139, 250, 0.18) !important;
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label[data-checked="true"],
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label[aria-checked="true"],
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label:has(input:checked) {
        background: linear-gradient(100deg, #6D28D9 0%, #8B5CF6 100%) !important;
        border-color: rgba(255, 255, 255, 0.12) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(17, 10, 36, 0.2) !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label p {
        margin: 0 !important;
        color: #E8E2F2 !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadioOption"]:has(input:checked) p {
        color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadioOption"] > div > div > div:first-child {
        display: none !important;
    }

    /* Base Styling */
    html, body, .stApp {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif !important;
        color: var(--text-dark) !important;
    }

    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background-color: var(--bg-main) !important;
    }

    /* Spacing */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 100% !important;
    }

    .status-pulse-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        display: inline-block;
        background-color: #A78BFA;
        box-shadow: 0 0 8px #A78BFA;
    }

    /* -------------------------------------------------------------------------
       TOP HEADER
       ------------------------------------------------------------------------- */
    .top-header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #FFFFFF;
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 0.75rem 1.4rem;
        margin-bottom: 1.2rem;
        box-shadow: var(--card-shadow);
    }
    .top-header-left {
        display: flex;
        flex-direction: column;
    }
    .greeting-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: var(--text-dark);
        margin: 0;
        letter-spacing: -0.02em;
    }
    .greeting-sub {
        font-size: 0.8rem;
        color: var(--text-muted);
        margin-top: 2px;
    }
    .top-header-right {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .ai-engine-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #EDE4FF;
        border: 1px solid #A78BFA;
        color: #6D28D9;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.03em;
    }
    .profile-avatar-circle {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background-color: #24163D;
        color: #FFFFFF;
        font-weight: 800;
        font-size: 0.88rem;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 8px rgba(11, 16, 38, 0.2);
    }

    /* -------------------------------------------------------------------------
       HERO SECTION
       ------------------------------------------------------------------------- */
    .hero-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F0F4FA 100%);
        border: 1px solid rgba(167, 139, 250, 0.2);
        border-radius: var(--radius-lg);
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.3rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: var(--card-shadow);
        position: relative;
        overflow: hidden;
    }
    .hero-card::after {
        content: "";
        position: absolute;
        right: -30px;
        top: -30px;
        width: 180px;
        height: 180px;
        background: radial-gradient(circle, rgba(167, 139, 250, 0.12) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .hero-title {
        font-size: 1.65rem;
        font-weight: 800;
        color: var(--text-dark);
        letter-spacing: -0.03em;
        margin: 0;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 0.88rem;
        color: var(--text-muted);
        margin-top: 0.4rem;
        margin-bottom: 0;
        max-width: 600px;
        line-height: 1.45;
    }
    .hero-graph-graphic {
        display: flex;
        align-items: center;
        gap: 8px;
        background: #F3EBFF;
        border: 1px solid rgba(109, 74, 255, 0.2);
        padding: 0.6rem 1rem;
        border-radius: 12px;
        color: #6D28D9;
        font-weight: 700;
        font-size: 0.82rem;
    }

    /* -------------------------------------------------------------------------
       CARD SYSTEM & 4 TOP KPI CARDS
       ------------------------------------------------------------------------- */
    .fin-card {
        background: #FFFFFF;
        border: 1px solid var(--border-color);
        border-radius: var(--radius-lg);
        padding: 1.25rem 1.35rem;
        box-shadow: var(--card-shadow);
        transition: all 0.2s ease;
    }
    .fin-card:hover {
        border-color: #DDD0FF;
        box-shadow: var(--card-shadow-hover);
    }
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.1rem;
        margin-bottom: 1.3rem;
    }
    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.6rem;
    }
    .kpi-label {
        font-size: 0.74rem;
        font-weight: 700;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-badge {
        font-size: 0.72rem;
        font-weight: 700;
        padding: 0.2rem 0.55rem;
        border-radius: 6px;
    }
    .kpi-value-lg {
        font-size: 1.85rem;
        font-weight: 800;
        color: var(--text-dark);
        letter-spacing: -0.03em;
        line-height: 1.15;
    }
    .kpi-footer-sub {
        font-size: 0.78rem;
        color: var(--text-muted);
        margin-top: 0.35rem;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    /* Badges */
    .badge-success {
        background: #EAFBF5;
        color: #059669;
        border: 1px solid #C8F3DC;
    }
    .badge-primary {
        background: #F3EBFF;
        color: #6D28D9;
        border: 1px solid #DDD0FF;
    }
    .badge-warning {
        background: #FFF4E5;
        color: #D97706;
        border: 1px solid #F8D7A8;
    }
    .badge-danger {
        background: #FEECEC;
        color: #DC2626;
        border: 1px solid #FCCACA;
    }
    .badge-secondary {
        background: #E9D8FF;
        color: #6D28D9;
        border: 1px solid #DDD0FF;
    }

    /* -------------------------------------------------------------------------
       FINANCIAL HEALTH GAUGE & DIMENSIONS
       ------------------------------------------------------------------------- */
    .health-gauge-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 0.8rem;
    }
    .dim-bar-wrap {
        margin-bottom: 0.75rem;
    }
    .dim-bar-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.78rem;
        font-weight: 700;
        color: var(--text-dark);
        margin-bottom: 0.3rem;
    }
    .dim-track {
        height: 7px;
        background: #F5F0FF;
        border-radius: 9999px;
        overflow: hidden;
        width: 100%;
    }
    .dim-fill {
        height: 100%;
        border-radius: 9999px;
        transition: width 0.3s ease;
    }
    .health-narrative-callout {
        background: #F3EBFF;
        border: 1px solid rgba(109, 74, 255, 0.2);
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-size: 0.8rem;
        color: #6D28D9;
        line-height: 1.45;
        margin-top: 1rem;
    }

    /* -------------------------------------------------------------------------
       GOAL JOURNEY VISUALIZATION
       ------------------------------------------------------------------------- */
    .journey-nodes-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
        margin: 1.2rem 0;
        padding: 0 1rem;
    }
    .journey-bg-line {
        position: absolute;
        top: 15px;
        left: 2rem;
        right: 2rem;
        height: 4px;
        background: #DDD0FF;
        z-index: 1;
    }
    .journey-fill-line {
        position: absolute;
        top: 15px;
        left: 2rem;
        height: 4px;
        background: linear-gradient(90deg, #6D28D9 0%, #8B5CF6 100%);
        z-index: 2;
    }
    .journey-node-dot {
        position: relative;
        z-index: 3;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: #FFFFFF;
        border: 3px solid #6D28D9;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.72rem;
        font-weight: 800;
        color: #6D28D9;
    }
    .journey-node-dot.passed {
        background: #6D28D9;
        color: #FFFFFF;
    }
    .journey-node-dot.active {
        background: #8B5CF6;
        border-color: #8B5CF6;
        color: #FFFFFF;
        box-shadow: 0 0 12px rgba(34, 199, 165, 0.6);
    }
    .goal-metrics-grid-3 {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.8rem;
        margin-top: 1rem;
        padding-top: 0.8rem;
        border-top: 1px solid #F5F0FF;
    }
    .goal-metric-col {
        display: flex;
        flex-direction: column;
    }
    .goal-metric-lbl {
        font-size: 0.72rem;
        color: var(--text-muted);
        font-weight: 600;
    }
    .goal-metric-num {
        font-size: 1.1rem;
        font-weight: 800;
        color: var(--text-dark);
        margin-top: 2px;
    }

    /* -------------------------------------------------------------------------
       WHAT-IF SIMULATOR CARDS
       ------------------------------------------------------------------------- */
    .sim-compare-card {
        background: #FFFFFF;
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: 1.1rem;
        text-align: center;
        box-shadow: var(--card-shadow);
    }
    .sim-diff-badge {
        font-size: 0.78rem;
        font-weight: 800;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        display: inline-block;
        margin-top: 0.4rem;
    }

    /* -------------------------------------------------------------------------
       AI RISK SPECIFIC
       ------------------------------------------------------------------------- */
    .why-reason-item {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.8rem;
        color: var(--text-dark);
        padding: 0.35rem 0;
    }
    .why-reason-icon {
        font-weight: 800;
        font-size: 0.85rem;
    }

    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        padding: 1rem 1.25rem;
        background: #FFFFFF;
        border: 1px solid #DDD0FF;
        border-radius: 12px;
        box-shadow: 0 5px 18px rgba(20, 33, 61, 0.05);
    }
    .app-brand { display: flex; align-items: center; gap: 0.8rem; min-width: 0; }
    .app-brand-mark {
        display: grid;
        place-items: center;
        width: 42px;
        height: 42px;
        flex: 0 0 42px;
        border-radius: 13px;
        background: #332454;
        color: #A78BFA;
        font-size: 1.45rem;
        font-weight: 700;
        box-shadow: inset 0 0 0 1px rgba(167, 139, 250, 0.2);
    }
    .app-brand-name { color: #24183B; font-size: 1.12rem; font-weight: 800; }
    .app-brand-subtitle { color: #6B6480; font-size: 0.82rem; }
    .header-status {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #059669;
        font-size: 0.78rem;
        font-weight: 700;
        white-space: nowrap;
    }
    .education-note { margin: 0.55rem 0 0.9rem; color: #6B6480; font-size: 0.78rem; }
    .status-pulse-dot { background-color: #A78BFA; box-shadow: 0 0 7px rgba(167,139,250,.35); }
    [data-testid="stExpander"] {
        margin: 0.7rem 0 1rem;
        border: 1px solid #DDD0FF !important;
        border-radius: 10px !important;
        background: #FFFFFF !important;
        box-shadow: 0 3px 12px rgba(36,24,59,.04);
    }
    [data-testid="stExpander"] details {
        border: 0 !important;
        border-radius: 10px !important;
        background: #FFFFFF !important;
    }
    [data-testid="stExpander"] summary {
        color: #24183B !important;
        background: #FFFFFF !important;
        font-weight: 700 !important;
        border-radius: 9px !important;
        transition: background 150ms ease;
    }
    [data-testid="stExpander"] summary:hover { background: #F3EBFF !important; }
    [data-testid="stExpander"] details[open] summary {
        border-bottom: 1px solid #DDD0FF;
        border-radius: 9px 9px 0 0 !important;
    }
    [data-testid="stExpander"] summary:focus-visible {
        outline: 2px solid #A78BFA !important;
        outline-offset: 2px !important;
    }
    [data-testid="stExpander"] [data-testid="stIconMaterial"] {
        position: relative;
        display: inline-flex;
        width: 14px;
        height: 14px;
        flex: 0 0 14px;
        font-size: 0 !important;
        color: transparent !important;
    }
    [data-testid="stExpander"] [data-testid="stIconMaterial"]::after {
        content: "";
        width: 6px;
        height: 6px;
        border-right: 1.5px solid #6B6480;
        border-bottom: 1.5px solid #6B6480;
        transform: rotate(-45deg);
        transition: transform 0.18s ease;
    }
    [data-testid="stExpander"] details[open] [data-testid="stIconMaterial"]::after {
        transform: rotate(45deg);
        border-color: #6D28D9;
    }
    [data-testid="stExpander"] [data-testid="stForm"] {
        padding: 1rem !important;
        border: 1px solid #DDD0FF !important;
        border-radius: 10px !important;
        background: #FFFFFF !important;
    }
    [data-testid="stForm"] [data-testid="stWidgetLabel"],
    [data-testid="stForm"] [data-testid="stWidgetLabel"] p,
    [data-testid="stForm"] [data-testid="stCaptionContainer"],
    [data-testid="stForm"] [data-testid="stCaptionContainer"] p {
        color: #24183B !important;
    }
    [data-testid="stForm"] [data-testid="stWidgetLabel"] {
        font-weight: 600 !important;
    }
    [data-testid="stForm"] [data-testid="stNumberInputContainer"],
    [data-testid="stForm"] [data-testid="stSelectbox"] [role="group"] {
        box-sizing: border-box !important;
        background: #FFFFFF !important;
        border: 1px solid #DDD0FF !important;
        border-radius: 8px !important;
        box-shadow: none !important;
        transition: border-color 150ms ease, box-shadow 150ms ease;
    }
    [data-testid="stForm"] [data-testid="stNumberInputContainer"]:hover,
    [data-testid="stForm"] [data-testid="stSelectbox"] [role="group"]:hover {
        border-color: #A78BFA !important;
    }
    [data-testid="stForm"] [data-testid="stNumberInputContainer"]:focus-within,
    [data-testid="stForm"] [data-testid="stSelectbox"] [role="group"]:focus-within {
        border-color: #A78BFA !important;
        box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.2) !important;
    }
    [data-testid="stForm"] [data-testid="stNumberInputField"],
    [data-testid="stForm"] [data-testid="stSelectbox"] input[role="combobox"] {
        color: #24183B !important;
        background: transparent !important;
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
    }
    [data-testid="stForm"] [data-testid="stNumberInputField"] {
        padding: 6px 4px 6px 8px !important;
        font-size: 0.82rem !important;
    }
    [data-testid="stForm"] [data-testid="stNumberInputContainer"] button,
    [data-testid="stForm"] [data-testid="stSelectbox"] button {
        border-radius: 6px !important;
        background: transparent !important;
        color: #6D28D9 !important;
    }
    [data-testid="stForm"] [data-testid="stNumberInputContainer"] button:hover,
    [data-testid="stForm"] [data-testid="stSelectbox"] button:hover {
        background: #F3EBFF !important;
        color: #6D28D9 !important;
    }
    [role="listbox"] {
        background: #FFFFFF !important;
        border: 1px solid #DDD0FF !important;
        border-radius: 8px !important;
        color: #24183B !important;
    }
    [role="option"] { color: #24183B !important; }
    [role="option"][data-focused="true"],
    [role="option"][aria-selected="true"] {
        background: #F3EBFF !important;
        color: #24183B !important;
    }
    .stButton > button, [data-testid="stFormSubmitButton"] button {
        border-radius: 8px !important;
        font-weight: 700 !important;
    }
    [data-testid="stFormSubmitButton"] button {
        border: 1px solid #6D28D9 !important;
        background: #6D28D9 !important;
        color: #FFFFFF !important;
        transition: background 150ms ease, border-color 150ms ease, box-shadow 150ms ease, transform 150ms ease;
    }
    [data-testid="stFormSubmitButton"] button:hover {
        border-color: #5B21B6 !important;
        background: #5B21B6 !important;
        box-shadow: 0 4px 12px rgba(109, 40, 217, 0.22) !important;
        transform: translateY(-1px);
    }
    [data-testid="stFormSubmitButton"] button:focus-visible {
        outline: 3px solid rgba(167, 139, 250, 0.55) !important;
        outline-offset: 2px !important;
        box-shadow: none !important;
    }
    [data-testid="stMetricValue"] { color: #211638 !important; }
    div[data-testid="stVerticalBlock"]:has(.simulator-controls-heading) [data-testid="stWidgetLabel"],
    div[data-testid="stVerticalBlock"]:has(.simulator-controls-heading) [data-testid="stWidgetLabel"] p,
    div[data-testid="stVerticalBlock"]:has(.simulator-controls-heading) [data-testid="stCaptionContainer"],
    div[data-testid="stVerticalBlock"]:has(.simulator-controls-heading) [data-testid="stCaptionContainer"] p {
        color: #24183B !important;
    }
    div[data-testid="stVerticalBlock"]:has(.simulator-controls-heading) [data-testid="stWidgetLabel"] {
        font-weight: 600 !important;
    }
    div[data-testid="stVerticalBlock"]:has(.simulator-controls-heading) [data-testid="stSliderThumbValue"],
    div[data-testid="stVerticalBlock"]:has(.simulator-controls-heading) [data-testid="stSliderThumbValue"] p {
        color: #6D28D9 !important;
        font-weight: 700 !important;
    }
    div[data-testid="stVerticalBlock"]:has(.simulator-controls-heading) [data-testid="stSliderTickBar"],
    div[data-testid="stVerticalBlock"]:has(.simulator-controls-heading) [data-testid="stSliderTickBar"] p {
        color: #6B6480 !important;
        font-size: 0.72rem !important;
    }
    div[data-testid="stVerticalBlock"]:has(.simulator-controls-heading) [data-testid="stSlider"] [role="group"] > div > div:first-child {
        isolation: isolate;
    }
    div[data-testid="stVerticalBlock"]:has(.simulator-controls-heading) [data-testid="stSlider"] [role="group"] > div > div:first-child::after {
        content: "";
        position: absolute;
        inset: 0;
        background: #6D28D9;
        mix-blend-mode: color;
        pointer-events: none;
    }
    div[data-testid="stVerticalBlock"]:has(.simulator-controls-heading) [data-testid="stSlider"] [role="group"] > div > div:has([data-testid="stSliderThumbValue"]) {
        background-color: #6D28D9 !important;
    }
    div[data-testid="stVerticalBlock"]:has(.simulator-controls-heading) [data-testid="stNumberInputContainer"] {
        box-sizing: border-box !important;
        background: #FFFFFF !important;
        border: 1px solid #DDD0FF !important;
        border-radius: 8px !important;
        box-shadow: none !important;
        transition: border-color 150ms ease, box-shadow 150ms ease;
    }
    div[data-testid="stVerticalBlock"]:has(.simulator-controls-heading) [data-testid="stNumberInputContainer"]:focus-within {
        border-color: #A78BFA !important;
        box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.2) !important;
    }
    div[data-testid="stVerticalBlock"]:has(.simulator-controls-heading) [data-testid="stNumberInputField"] {
        color: #24183B !important;
        background: transparent !important;
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
    }
    div[data-testid="stVerticalBlock"]:has(.simulator-controls-heading) .stButton > button {
        border: 1px solid #6D28D9 !important;
        border-radius: 8px !important;
        background: #6D28D9 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        transition: background 150ms ease, border-color 150ms ease, box-shadow 150ms ease, transform 150ms ease;
    }
    div[data-testid="stVerticalBlock"]:has(.simulator-controls-heading) .stButton > button:hover {
        border-color: #5B21B6 !important;
        background: #5B21B6 !important;
        box-shadow: 0 4px 12px rgba(109, 40, 217, 0.22) !important;
        transform: translateY(-1px);
    }
    div[data-testid="stVerticalBlock"]:has(.simulator-page-heading) [data-testid="stMetricLabel"],
    div[data-testid="stVerticalBlock"]:has(.simulator-page-heading) [data-testid="stMetricLabel"] p {
        color: #6B6480 !important;
        white-space: normal !important;
        overflow: visible !important;
    }
    div[data-testid="stVerticalBlock"]:has(.simulator-page-heading) [data-testid="stMetricValue"] {
        color: #24183B !important;
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
        overflow-wrap: anywhere;
        line-height: 1.2;
    }
    div[data-testid="stVerticalBlock"]:has(.simulator-page-heading) [data-testid="stMetricDelta"] {
        color: #6B6480 !important;
        background: #F3EBFF !important;
        border-radius: 6px;
        font-size: 0.7rem !important;
        white-space: normal !important;
    }
    div[data-testid="stVerticalBlock"]:has(.simulator-page-heading) [data-testid="stMetric"] div:has(> [data-testid="stMetricDelta"]) {
        overflow: visible !important;
        height: auto !important;
    }
    div[data-testid="stVerticalBlock"]:has(.simulator-page-heading) [data-testid="stMetricDelta"] [data-testid="stMarkdownContainer"],
    div[data-testid="stVerticalBlock"]:has(.simulator-page-heading) [data-testid="stMetricDelta"] p {
        max-width: 100% !important;
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
        overflow-wrap: anywhere;
    }
    div[data-testid="stVerticalBlock"]:has(.analytics-page-heading) [data-testid="stCaptionContainer"],
    div[data-testid="stVerticalBlock"]:has(.analytics-page-heading) [data-testid="stCaptionContainer"] p {
        color: #6B6480 !important;
    }
    div[data-testid="stVerticalBlock"]:has(.analytics-page-heading) div[data-testid="stElementContainer"]:has(.js-plotly-plot) {
        padding: 0.35rem !important;
        border: 1px solid #DDD0FF !important;
        border-radius: 12px !important;
        background: #FFFFFF !important;
        box-shadow: 0 1px 3px rgba(36, 24, 59, 0.04), 0 6px 16px rgba(36, 24, 59, 0.04);
    }
    div[data-testid="stVerticalBlock"]:has(.ai-chat-page-heading) [data-testid="stChatMessage"] {
        padding: 0.8rem 1rem !important;
        border: 1px solid #DDD0FF !important;
        border-radius: 10px !important;
        background: #FFFFFF !important;
    }
    div[data-testid="stVerticalBlock"]:has(.ai-chat-page-heading) [data-testid="stChatMessageContent"],
    div[data-testid="stVerticalBlock"]:has(.ai-chat-page-heading) [data-testid="stChatMessageContent"] p {
        color: #24183B !important;
    }
    div[data-testid="stVerticalBlock"]:has(.ai-chat-page-heading) [data-testid="stChatMessageAvatarUser"] {
        background: #6D28D9 !important;
        color: #FFFFFF !important;
    }
    div[data-testid="stVerticalBlock"]:has(.ai-chat-page-heading) [data-testid="stChatMessageAvatarAssistant"] {
        background: #A78BFA !important;
        color: #24183B !important;
    }
    div[data-testid="stVerticalBlock"]:has(.ai-chat-page-heading) [data-testid="stForm"] {
        padding: 0.75rem !important;
        border: 1px solid #DDD0FF !important;
        border-radius: 10px !important;
        background: #FFFFFF !important;
    }
    div[data-testid="stVerticalBlock"]:has(.ai-chat-page-heading) [data-testid="stWidgetLabel"],
    div[data-testid="stVerticalBlock"]:has(.ai-chat-page-heading) [data-testid="stWidgetLabel"] p {
        color: #24183B !important;
    }
    div[data-testid="stVerticalBlock"]:has(.ai-chat-page-heading) [data-testid="stTextInputRootElement"] {
        background: #FFFFFF !important;
        border: 1px solid #DDD0FF !important;
        border-radius: 8px !important;
    }
    div[data-testid="stVerticalBlock"]:has(.ai-chat-page-heading) [data-testid="stTextInput"] input {
        color: #24183B !important;
        background: transparent !important;
    }
    div[data-testid="stVerticalBlock"]:has(.ai-chat-page-heading) [data-testid="stTextInputRootElement"]:focus-within {
        border-color: #A78BFA !important;
        box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.2) !important;
    }
    div[data-testid="stVerticalBlock"]:has(.ai-chat-page-heading) .stButton > button {
        min-height: 48px;
        border: 1px solid #DDD0FF !important;
        border-radius: 8px !important;
        background: #FFFFFF !important;
        color: #24183B !important;
        white-space: normal !important;
        text-align: left !important;
    }
    div[data-testid="stVerticalBlock"]:has(.ai-chat-page-heading) .stButton > button:hover {
        border-color: #A78BFA !important;
        background: #F3EBFF !important;
    }
    @media (max-width: 1100px) {
        div[data-testid="stVerticalBlock"]:has(.simulator-page-heading) [data-testid="stMetricValue"] {
            font-size: 1.1rem !important;
        }
        div[data-testid="stVerticalBlock"]:has(.simulator-page-heading) [data-testid="stMetricDelta"] {
            font-size: 0.64rem !important;
        }
    }
    @media (max-width: 1100px) {
        div[data-testid="stHorizontalBlock"]:has(.overview-kpi-card),
        div[data-testid="stHorizontalBlock"]:has([data-testid="stMetricValue"]) {
            display: flex !important;
            flex-wrap: wrap !important;
            gap: 0.75rem !important;
        }
        div[data-testid="stHorizontalBlock"]:has(.overview-kpi-card) > div[data-testid="stColumn"],
        div[data-testid="stHorizontalBlock"]:has([data-testid="stMetricValue"]) > div[data-testid="stColumn"] {
            flex: 1 1 calc(50% - 0.4rem) !important;
            width: calc(50% - 0.4rem) !important;
            max-width: calc(50% - 0.4rem) !important;
            min-width: 0 !important;
        }
    }
    @media (max-width: 700px) {
        div[data-testid="stHorizontalBlock"]:has(.overview-kpi-card) > div[data-testid="stColumn"],
        div[data-testid="stHorizontalBlock"]:has([data-testid="stMetricValue"]) > div[data-testid="stColumn"] {
            flex-basis: 100% !important;
            width: 100% !important;
            max-width: 100% !important;
        }
    }
    @media (max-width: 700px) {
        .block-container { padding: 0.65rem 0.75rem 1.5rem !important; }
        .app-header { align-items: flex-start; padding: 0.8rem; }
        .app-brand-mark { width: 36px; height: 36px; flex-basis: 36px; }
        .app-brand-name { font-size: 1rem; }
        .app-brand-subtitle { font-size: 0.72rem; }
        .header-status { font-size: 0.68rem; }
    }
    @media (max-height: 700px) {
        [data-testid="stSidebar"] > div:first-child { padding-top: 0.75rem !important; }
        [data-testid="stSidebarHeader"] { height: 32px !important; min-height: 32px !important; }
        .ws-sidebar-brand { padding-bottom: 0.55rem; }
        .ws-sidebar-mark { width: 36px; height: 36px; flex-basis: 36px; }
        [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] { gap: 0.1rem !important; }
        [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] label {
            min-height: 34px;
            padding: 0.3rem 0.55rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# DATA AND MODEL LOADERS (PRESERVED)
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
# FINANCIAL COMPUTATIONS ENGINE (PRESERVED)
# ==============================================================================
def compute_financial_health_score(income, expense, monthly_savings, current_savings, debt, goal_amount, horizon):
    income = max(0.0, float(income))
    expense = max(0.0, float(expense))
    current_savings = max(0.0, float(current_savings))
    debt = max(0.0, float(debt))
    goal_amount = max(0.0, float(goal_amount))
    horizon = max(0.08, float(horizon))

    # 1. Savings Rate Component (25%) -> 0-50% mapped to 0-100 score
    savings_rate_pct = (monthly_savings / income) * 100.0 if income > 0 else 0.0
    savings_comp = np.clip(savings_rate_pct * 2.0, 0, 100)
    
    # 2. Debt Component (20%) -> 0-100% debt-to-income mapped inversely to 100-0 score
    annual_income = income * 12.0
    dti_pct = (debt / annual_income) * 100.0 if annual_income > 0 else (100.0 if debt > 0 else 0.0)
    debt_comp = np.clip(100.0 - dti_pct, 0, 100)
    
    # 3. Emergency Fund Component (20%) -> 0-6 months mapped to 0-100 score (capped at 6 mos)
    safe_expense = max(1.0, expense)
    ef_months = current_savings / safe_expense
    emergency_comp = np.clip((ef_months / 6.0) * 100.0, 0, 100)
    
    # 4. Expense Ratio Component (15%) -> <=30% expense ratio = 100 score, >=100% = 0 score
    expense_ratio_pct = (expense / income) * 100.0 if income > 0 else (0.0 if expense == 0 else 100.0)
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
    
    if score >= 80.0:
        category = "Good"
    elif score >= 60.0:
        category = "Moderate"
    elif score >= 40.0:
        category = "Needs Improvement"
    else:
        category = "Poor"
        
    components = {
        'Savings Rate': round(savings_comp),
        'Debt Burden': round(debt_comp),
        'Emergency Fund': round(emergency_comp),
        'Expense Ratio': round(expense_comp),
        'Monthly Surplus': round(surplus_comp),
        'Goal Progress': round(goal_comp)
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

def combine_horizon_months(years, months):
    years = int(years)
    months = int(months)
    if years < 0:
        raise ValueError("Horizon years must be zero or greater.")
    if months < 0 or months > 11:
        raise ValueError("Horizon months must be between 0 and 11.")
    return years * 12 + months


def format_horizon_months(total_horizon_months):
    total_horizon_months = max(0, int(total_horizon_months))
    years, months = divmod(total_horizon_months, 12)
    parts = []
    if years:
        parts.append(f"{years} year{'s' if years != 1 else ''}")
    if months or not parts:
        parts.append(f"{months} month{'s' if months != 1 else ''}")
    return ", ".join(parts)


def format_inr(amount, decimals=0):
    value = f"{abs(float(amount)):,.{decimals}f}"
    whole, dot, fraction = value.partition(".")
    if len(whole) > 3:
        whole = whole[:-3].replace(",", "")
        last_three = f"{abs(float(amount)):,.{decimals}f}".split(".")[0][-3:]
        groups = []
        while len(whole) > 2:
            groups.insert(0, whole[-2:])
            whole = whole[:-2]
        if whole:
            groups.insert(0, whole)
        whole = ",".join(groups + [last_three])
    return f"{'-' if float(amount) < 0 else ''}₹{whole}{dot}{fraction}" if dot else f"{'-' if float(amount) < 0 else ''}₹{whole}"


def reset_simulator_to_profile():
    profile_values = {
        "sim_income_input": "profile_income",
        "sim_expense_input": "profile_expense",
        "sim_savings_input": "profile_savings",
        "sim_debt_input": "profile_debt",
        "sim_goal_input": "profile_goal_amount",
        "sim_horizon_years": "profile_horizon_years_input",
        "sim_horizon_months": "profile_horizon_months_input",
    }
    for simulator_key, profile_key in profile_values.items():
        st.session_state[simulator_key] = st.session_state[profile_key]


def compute_goal_feasibility(current_savings, goal_amount, horizon_years, monthly_savings, goal_progress_pct, total_horizon_months=None):
    goal_amount = max(0.0, float(goal_amount))
    current_savings = max(0.0, float(current_savings))
    goal_remaining = max(0.0, goal_amount - current_savings) if goal_amount > 0 else 0.0

    if total_horizon_months is None:
        horizon_months = max(1, int(round(float(horizon_years) * 12.0)))
    else:
        horizon_months = max(0, int(total_horizon_months))

    achieved = (goal_amount > 0 and current_savings >= goal_amount) or (goal_amount == 0 and current_savings >= 0)
    if achieved:
        required_monthly = 0.0
        monthly_saving_gap = 0.0
    elif horizon_months > 0:
        required_monthly = goal_remaining / horizon_months
        monthly_saving_gap = max(0.0, required_monthly - monthly_savings)
    else:
        required_monthly = None
        monthly_saving_gap = goal_remaining
    
    if achieved:
        achievement_status = "Goal Accomplished"
        feasibility_status = "Already Achieved"
    elif horizon_months == 0:
        achievement_status = "Needs Attention"
        feasibility_status = "No Time Remaining"
    elif monthly_savings >= required_monthly:
        achievement_status = "On Track"
        feasibility_status = "On Track"
    else:
        achievement_status = "Needs Attention"
        feasibility_status = "Needs Higher Monthly Saving"
        
    return {
        'goal_remaining': goal_remaining,
        'required_monthly_saving': required_monthly,
        'monthly_saving_gap': monthly_saving_gap,
        'achievement_status': achievement_status,
        'feasibility_status': feasibility_status
    }

# Circular SVG Gauge Chart Generator — fully inline, no CSS class dependency
def generate_health_donut_svg(score_val, category_label):
    radius = 64
    circumference = 2 * np.pi * radius
    dash_offset = circumference * (1.0 - (min(100.0, max(0.0, score_val)) / 100.0))
    stroke_color = "#8B5CF6" if score_val >= 80 else ("#6D28D9" if score_val >= 60 else ("#D97706" if score_val >= 40 else "#DC2626"))
    badge_bg  = "#E9D8FF" if score_val >= 80 else ("#F3EBFF" if score_val >= 60 else ("#FFF4E5" if score_val >= 40 else "#FEECEC"))
    badge_clr = "#8B5CF6" if score_val >= 80 else ("#6D28D9" if score_val >= 60 else ("#D97706" if score_val >= 40 else "#DC2626"))
    badge_brd = "#DDD0FF" if score_val >= 80 else ("#DDD0FF" if score_val >= 60 else ("#F8D7A8" if score_val >= 40 else "#FCCACA"))

    return f'<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0.5rem;"><div style="position:relative;width:160px;height:160px;"><svg viewBox="0 0 160 160" width="160" height="160"><circle cx="80" cy="80" r="{radius}" fill="none" stroke="#F5F0FF" stroke-width="12"/><circle cx="80" cy="80" r="{radius}" fill="none" stroke="{stroke_color}" stroke-width="12" stroke-dasharray="{circumference:.2f}" stroke-dashoffset="{dash_offset:.2f}" stroke-linecap="round" transform="rotate(-90 80 80)"/><text x="80" y="73" text-anchor="middle" dominant-baseline="middle" font-size="30" font-weight="800" fill="#24183B" font-family="Plus Jakarta Sans,Inter,sans-serif">{score_val:.0f}%</text></svg><div style="position:absolute;bottom:-10px;left:50%;transform:translateX(-50%);white-space:nowrap;"><span style="font-size:0.68rem;font-weight:700;padding:0.18rem 0.5rem;border-radius:5px;background:{badge_bg};color:{badge_clr};border:1px solid {badge_brd};">{category_label.upper()}</span></div></div></div>'

# ==============================================================================
# MAIN APPLICATION
def build_rule_based_financial_answer(question, profile):
    question_text = question.casefold()
    income = profile["income"]
    expense = profile["expense"]
    monthly_savings = profile["monthly_savings"]
    current_savings = profile["current_savings"]
    debt = profile["debt"]
    goal_amount = profile["goal_amount"]
    horizon_months = profile["horizon_months"]
    metrics = profile["metrics"]
    goal_info = profile["goal_info"]

    if any(word in question_text for word in ("goal", "target", "timeline", "horizon", "deadline")):
        remaining = goal_info["goal_remaining"]
        required = goal_info["required_monthly_saving"]
        if remaining <= 0:
            return f"Your entered savings of {format_inr(current_savings)} meet or exceed your {format_inr(goal_amount)} goal. The goal is already achieved by the dashboard calculation."
        if required is None:
            return f"Your goal is {format_inr(goal_amount)} and current savings are {format_inr(current_savings)}, leaving {format_inr(remaining)}. No time remains in the selected horizon, so a monthly amount cannot be calculated."
        monthly_margin = monthly_savings - required
        margin_text = (
            f"Your entry is about {format_inr(monthly_margin)} above that simple monthly amount."
            if monthly_margin >= 0
            else f"Your entry is about {format_inr(abs(monthly_margin))} below that simple monthly amount."
        )
        return (
            f"Your goal is {format_inr(goal_amount)}. After {format_inr(current_savings)} in current savings, "
            f"{format_inr(remaining)} remains over {horizon_months} months. Dividing the remaining amount "
            f"by the months gives about {format_inr(required)} per month. You entered {format_inr(monthly_savings)} "
            f"as monthly savings. {margin_text} This estimate assumes no growth, interest, or fees."
        )

    if any(word in question_text for word in ("debt", "loan", "repay", "repayment", "interest")):
        annual_income = income * 12.0
        return (
            f"Your entered total debt is {format_inr(debt)}. The dashboard's debt indicator is total debt divided by "
            f"annual income ({format_inr(debt)} / {format_inr(annual_income)}), or {metrics['dti_pct']:.1f}%. "
            "This is not a payment-to-income ratio. Your interest rates, minimum payments, and fees are not in the profile, "
            "so I cannot compare payoff options or estimate interest savings."
        )

    if any(word in question_text for word in ("risk", "tolerance", "prediction", "category")):
        predicted = profile["predicted_risk"]
        prediction_text = (
            f"The existing model classifies the profile as {predicted}. This is a model output, not a guarantee or investment recommendation."
            if predicted != "Unavailable"
            else "The existing model prediction is unavailable for this profile."
        )
        return f"Your selected risk tolerance is {profile['risk_tolerance']}. {prediction_text} Risk tolerance and a model category do not remove the possibility of loss."

    if any(word in question_text for word in ("expense", "spend", "budget", "cash flow", "cashflow", "left over", "leftover")) and not any(word in question_text for word in ("saving", "save", "emergency", "fund")):
        expense_ratio = metrics["expense_ratio_pct"]
        return (
            f"Your entered monthly expenses are {format_inr(expense)} against income of {format_inr(income)}. "
            f"That is {expense_ratio:.1f}% of income (expenses / income). Income minus expenses is "
            f"{format_inr(income - expense)} per month. Your monthly savings entry, {format_inr(monthly_savings)}, "
            "is separate and can differ from that arithmetic remainder."
        )

    if any(word in question_text for word in ("saving", "savings", "save", "emergency", "fund")):
        return (
            f"You entered {format_inr(monthly_savings)} in monthly savings and {format_inr(current_savings)} in current savings. "
            f"Monthly savings are {metrics['savings_rate_pct']:.1f}% of income. At your entered expense level of "
            f"{format_inr(expense)}, current savings cover about {metrics['ef_months']:.1f} months "
            "(current savings / monthly expenses). These are profile-based estimates, not a savings target."
        )

    if any(word in question_text for word in ("health", "score", "financial")):
        parts = (
            f"savings rate {metrics['savings_rate_pct']:.1f}% (component {profile['components']['Savings Rate']}/100), "
            f"debt / yearly income {metrics['dti_pct']:.1f}% (component {profile['components']['Debt Burden']}/100), "
            f"emergency coverage {metrics['ef_months']:.1f} months (component {profile['components']['Emergency Fund']}/100), "
            f"expense ratio {metrics['expense_ratio_pct']:.1f}% (component {profile['components']['Expense Ratio']}/100), "
            f"monthly surplus component {profile['components']['Monthly Surplus']}/100, "
            f"and goal progress {metrics['goal_progress_pct']:.1f}% (component {profile['components']['Goal Progress']}/100)"
        )
        return (
            f"Your dashboard health score is {profile['score']:.1f}/100 ({profile['category']}). It combines six weighted "
            "components: savings rate 25%, debt burden 20%, emergency fund 20%, expense ratio 15%, monthly surplus 10%, "
            f"and goal progress 10%. Your current profile measures include {parts}. It is an educational dashboard score, not a credit rating."
        )

    return (
        f"I can explain your health score ({profile['score']:.1f}/100), savings, expenses, debt, risk tolerance, or goal. "
        f"For context, your entered income is {format_inr(income)} per month and income minus expenses is {format_inr(income - expense)}."
    )


def build_financial_product_guidance(profile):
    metrics = profile["metrics"]
    monthly_savings = profile["monthly_savings"]
    income = profile["income"]
    expense = profile["expense"]
    current_savings = profile["current_savings"]
    debt = profile["debt"]
    goal_amount = profile["goal_amount"]
    horizon_months = profile["horizon_months"]
    risk_tolerance = profile["risk_tolerance"]
    cash_remaining = income - expense
    horizon_text = profile["horizon_display"]

    if monthly_savings > 0 and cash_remaining > 0:
        recurring_fit = (
            f"You entered {format_inr(monthly_savings)} in monthly savings, while income minus expenses is "
            f"{format_inr(cash_remaining)}. A recurring deposit may be worth researching only if its scheduled contribution "
            f"fits your cash flow and {horizon_text} goal horizon."
        )
    else:
        recurring_fit = (
            f"Your entered monthly savings are {format_inr(monthly_savings)} and income minus expenses is "
            f"{format_inr(cash_remaining)}. A fixed recurring contribution may not fit until your cash flow is reviewed."
        )

    if "Low" in risk_tolerance or horizon_months < 36:
        mutual_fund_fit = (
            f"Your selected tolerance is {risk_tolerance} and your goal horizon is {horizon_text}. "
            "Market-linked funds can lose value, so they may be a poor match for money needed soon or when losses would be difficult to accept."
        )
    else:
        mutual_fund_fit = (
            f"Your selected tolerance is {risk_tolerance} and your goal horizon is {horizon_text}. "
            "That context may support researching long-term market-linked options, but it does not establish suitability and losses remain possible."
        )

    debt_fit = (
        f"Your profile lists {format_inr(debt)} in total debt and a dashboard debt / annual-income indicator of "
        f"{metrics['dti_pct']:.1f}%. Compare actual APRs, required payments, and any early-payment fees before deciding whether extra repayment fits."
        if debt > 0
        else "No debt is entered in the profile, so debt repayment options are not currently matched to a listed balance."
    )

    return [
        {
            "name": "Savings Accounts",
            "purpose": "Hold cash for everyday access, near-term needs, and reserves.",
            "benefits": "Convenient access and a clear place to separate cash from longer-term goals.",
            "risks": "Fees, minimum-balance rules, and inflation can affect the value of cash over time.",
            "liquidity": "Typically high; account terms and transfer limits vary.",
            "time_horizon": "Immediate to short term.",
            "considerations": "Check fees, access rules, deposit-protection rules in your jurisdiction, and account terms. No current rates are assumed.",
            "profile_match": (
                f"Your current savings of {format_inr(current_savings)} cover about {metrics['ef_months']:.1f} months "
                f"of entered expenses ({format_inr(expense)} per month). Accessible cash may be relevant for near-term needs; "
                f"your goal is {format_inr(goal_amount)} over {horizon_text}."
            ),
        },
        {
            "name": "Recurring Deposits",
            "purpose": "Build savings through scheduled, repeated deposits over a chosen term.",
            "benefits": "Can support a regular saving habit and planned contributions.",
            "risks": "Missed-contribution rules, early-closure terms, and inflation may matter; availability varies.",
            "liquidity": "Usually lower than an on-demand savings account; verify withdrawal terms.",
            "time_horizon": "Term-based; compare the term with your goal date.",
            "considerations": "Confirm contribution flexibility, penalties, taxes, and whether deposits fit after essential expenses. No rates are assumed.",
            "profile_match": recurring_fit,
        },
        {
            "name": "Fixed Deposits",
            "purpose": "Place a lump sum for a specified term under stated institution terms.",
            "benefits": "The term and stated conditions can make the commitment easier to understand in advance.",
            "risks": "Early withdrawal restrictions or penalties, tax treatment, and inflation can reduce suitability.",
            "liquidity": "Limited during the term; depends on the specific terms.",
            "time_horizon": "Months to years, matched to when the money may be needed.",
            "considerations": "Keep near-term and emergency money accessible; verify maturity, early-exit, tax, and protection terms. No return is assumed.",
            "profile_match": (
                f"Your current savings are {format_inr(current_savings)} and your goal is {format_inr(goal_amount)} "
                f"in {horizon_text}. A fixed term may only suit a portion you do not expect to need before maturity."
            ),
        },
        {
            "name": "Mutual Funds",
            "purpose": "Pool investments into market-linked assets according to a fund's mandate.",
            "benefits": "Some funds provide diversification and access to multiple securities through one investment.",
            "risks": "Values can fall; fees, taxes, market risk, and fund-specific risks apply. Returns are not guaranteed.",
            "liquidity": "Redemption and settlement depend on fund type and terms; some products have restrictions.",
            "time_horizon": "Depends on the fund and goal; market risk can persist over long periods.",
            "considerations": "Review the fund documents, risk level, fees, tax treatment, and whether a loss is affordable. No returns are forecast.",
            "profile_match": mutual_fund_fit,
        },
        {
            "name": "Debt Repayment Options",
            "purpose": "Pay required amounts and evaluate whether additional payments should reduce outstanding balances.",
            "benefits": "Extra repayment may reduce interest costs when allowed; the effect depends on the debt's APR and terms.",
            "risks": "Using liquid savings can leave less cash available; prepayment fees and other terms may apply.",
            "liquidity": "Money used for repayment is generally no longer available as cash.",
            "time_horizon": "Based on each balance, rate, required payment, and repayment terms.",
            "considerations": "List balances, APRs, minimum payments, fees, and due dates. Keep required payments current; compare options using actual terms.",
            "profile_match": debt_fit,
        },
    ]

# MAIN APPLICATION
# ==============================================================================
def main():
    # Session state initialization
    if 'profile_age' not in st.session_state:
        st.session_state.profile_age = 35
    if 'profile_income' not in st.session_state:
        st.session_state.profile_income = 80000.0
    if 'profile_expense' not in st.session_state:
        st.session_state.profile_expense = 45000.0
    if 'profile_monthly_savings' not in st.session_state:
        st.session_state.profile_monthly_savings = max(0.0, st.session_state.profile_income - st.session_state.profile_expense)
    if 'profile_savings' not in st.session_state:
        st.session_state.profile_savings = 35000.0
    if 'profile_debt' not in st.session_state:
        st.session_state.profile_debt = 15000.0
    if 'profile_goal_amount' not in st.session_state:
        st.session_state.profile_goal_amount = 200000.0
    if 'profile_horizon_years' not in st.session_state:
        st.session_state.profile_horizon_years = 10
    if 'profile_horizon_years_input' not in st.session_state or 'profile_horizon_months_input' not in st.session_state:
        legacy_horizon_months = max(0, int(round(float(st.session_state.profile_horizon_years) * 12)))
        st.session_state.profile_horizon_years_input = legacy_horizon_months // 12
        st.session_state.profile_horizon_months_input = legacy_horizon_months % 12
    if 'profile_risk_score' not in st.session_state:
        st.session_state.profile_risk_score = 50
    if 'profile_risk_pref' not in st.session_state:
        st.session_state.profile_risk_pref = "50 (Moderate)"
    if 'nav_tab' not in st.session_state:
        st.session_state.nav_tab = "Overview"
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Load ML models and dataset
    model, feature_columns, model_metrics = load_ml_model()
    df_analytics = load_dataset()
    model_name = model_metrics.get("best_model") if model_metrics else None
    accuracy = model_metrics.get("metrics", {}).get("Accuracy") if model_metrics else None
    model_acc = float(accuracy) * 100.0 if accuracy is not None else None
    model_name_display = model_name or "Unavailable"
    model_acc_display = f"{model_acc:.1f}%" if model_acc is not None else "Unavailable"
    model_accuracy_explanation = (
        f"On separate test examples, the model classified {model_acc:.1f}% correctly. This is not a guarantee for an individual profile."
        if model_acc is not None
        else "Validation accuracy is unavailable because the model's test results were not loaded."
    )

    nav_options = [
        "Overview",
        "Financial Health",
        "Financial Goals",
        "AI Risk Analysis",
        "Analytics",
        "What-If Simulator",
        "AI Insights",
        "AI Chatbot",
        "Financial Products"
    ]
    if st.session_state.nav_tab not in nav_options:
        st.session_state.nav_tab = "Overview"

    # Full-width product header and compact application status.
    st.markdown(textwrap.dedent("""
    <div class="app-header">
        <div class="app-brand">
            <div class="app-brand-mark">₹</div>
            <div>
                <div class="app-brand-name">WealthSphere</div>
                <div class="app-brand-subtitle">Personal Financial Intelligence</div>
            </div>
        </div>
        <div class="header-status">
            <span class="status-pulse-dot"></span>
            <span>AI ENGINE ACTIVE</span>
        </div>
    </div>
    <div class="education-note">Educational decision-support tool. Not certified financial, investment, or legal advice.</div>
    """), unsafe_allow_html=True)

    with st.expander("Profile Settings", expanded=False):
        with st.form("profile_settings_form"):
            profile_col_1, profile_col_2, profile_col_3 = st.columns(3, gap="medium")
            with profile_col_1:
                in_age = st.number_input("Age", min_value=18, max_value=100, value=int(st.session_state.profile_age), step=1, key="profile_form_age")
                in_income = st.number_input("Monthly Income (₹)", min_value=100.0, value=float(st.session_state.profile_income), step=5000.0, key="profile_form_income")
                in_expense = st.number_input("Monthly Expenses (₹)", min_value=0.0, value=float(st.session_state.profile_expense), step=2500.0, key="profile_form_expense")
            with profile_col_2:
                in_savings = st.number_input("Monthly Savings (₹)", min_value=0.0, value=float(st.session_state.profile_monthly_savings), step=2500.0, key="profile_form_monthly_savings")
                in_current_savings = st.number_input("Current Savings (₹)", min_value=0.0, value=float(st.session_state.profile_savings), step=5000.0, key="profile_form_current_savings")
                in_debt = st.number_input("Total Debt (₹)", min_value=0.0, value=float(st.session_state.profile_debt), step=2500.0, key="profile_form_debt")
            with profile_col_3:
                in_goal = st.number_input("Goal Amount (₹)", min_value=100.0, value=float(st.session_state.profile_goal_amount), step=10000.0, key="profile_form_goal")
                horizon_years_input, horizon_months_input = st.columns(2, gap="small")
                with horizon_years_input:
                    in_horizon_years = st.number_input("Years", min_value=0, value=int(st.session_state.profile_horizon_years_input), step=1, key="profile_form_horizon_years")
                with horizon_months_input:
                    in_horizon_months = st.number_input("Months", min_value=0, max_value=11, value=int(st.session_state.profile_horizon_months_input), step=1, key="profile_form_horizon_months")
                st.caption(f"Total horizon: {format_horizon_months(combine_horizon_months(in_horizon_years, in_horizon_months))}")
                risk_options = ["25 (Low)", "50 (Moderate)", "75 (High)"]
                current_risk_index = 0 if "Low" in st.session_state.profile_risk_pref else (2 if "High" in st.session_state.profile_risk_pref else 1)
                in_risk = st.selectbox("Risk Tolerance", options=risk_options, index=current_risk_index, key="profile_form_risk")
            analyze_profile = st.form_submit_button("Analyze Profile", type="primary", use_container_width=True)

        if analyze_profile:
            st.session_state.profile_age = in_age
            st.session_state.profile_income = in_income
            st.session_state.profile_expense = in_expense
            st.session_state.profile_monthly_savings = in_savings
            st.session_state.profile_savings = in_current_savings
            st.session_state.profile_debt = in_debt
            st.session_state.profile_goal_amount = in_goal
            st.session_state.profile_horizon_years_input = in_horizon_years
            st.session_state.profile_horizon_months_input = in_horizon_months
            total_horizon_months = combine_horizon_months(in_horizon_years, in_horizon_months)
            st.session_state.profile_horizon_years = total_horizon_months / 12.0
            st.session_state.profile_risk_pref = in_risk
            st.session_state.profile_risk_score = 25 if "Low" in in_risk else (75 if "High" in in_risk else 50)
            st.success("Profile analyzed. Dashboard results have been updated.")

    nav_icons = {
        "Overview": "▦",
        "Financial Health": "◉",
        "Financial Goals": "◎",
        "AI Risk Analysis": "⌁",
        "Analytics": "▥",
        "What-If Simulator": "⟳",
        "AI Insights": "✧",
        "AI Chatbot": "◌",
        "Financial Products": "▤",
    }
    with st.sidebar:
        st.markdown(textwrap.dedent("""
        <div class="ws-sidebar-brand">
            <div class="ws-sidebar-mark">₹</div>
            <div>
                <div class="ws-sidebar-name">WealthSphere</div>
                <div class="ws-sidebar-caption">FINANCIAL INTELLIGENCE</div>
            </div>
        </div>
        """), unsafe_allow_html=True)
        st.caption("WORKSPACE")
        nav_selection = st.radio(
            "Main navigation",
            options=nav_options,
            format_func=lambda page: f"{nav_icons[page]}　{page}",
            label_visibility="collapsed",
            key="nav_tab"
        )

    # --------------------------------------------------------------------------
    # CORE PROFILE METRICS
    # --------------------------------------------------------------------------
    u_income = st.session_state.profile_income
    u_expense = st.session_state.profile_expense
    u_savings = st.session_state.profile_savings
    u_debt = st.session_state.profile_debt
    u_goal = st.session_state.profile_goal_amount
    u_horizon_months = combine_horizon_months(
        st.session_state.profile_horizon_years_input,
        st.session_state.profile_horizon_months_input
    )
    u_horizon = u_horizon_months / 12.0
    u_surplus = float(st.session_state.profile_monthly_savings)
    u_cash_remaining = u_income - u_expense
    u_savings_rate = (u_surplus / u_income) * 100.0 if u_income > 0 else 0.0

    score_val, cat_val, components, metrics = compute_financial_health_score(
        u_income, u_expense, u_surplus, u_savings, u_debt, u_goal, u_horizon
    )
    goal_info = compute_goal_feasibility(
        u_savings, u_goal, u_horizon, u_surplus, metrics['goal_progress_pct'],
        total_horizon_months=u_horizon_months
    )
    horizon_display = format_horizon_months(u_horizon_months)
    required_monthly_display = (
        f"₹{goal_info['required_monthly_saving']:,.0f}"
        if goal_info['required_monthly_saving'] is not None
        else "No time remaining"
    )

    # ML Risk Inference with actual probabilities
    risk_pred = None
    risk_confidence = None
    risk_probs = None

    if model is not None and feature_columns is not None:
        try:
            in_df = pd.DataFrame([{
                'age': st.session_state.profile_age,
                'monthly_income': u_income,
                'monthly_expense': u_expense,
                'monthly_savings': u_surplus,
                'current_savings': u_savings,
                'debt': u_debt,
                'financial_goal_amount': u_goal,
                'investment_horizon_years': u_horizon,
                'risk_tolerance_score': st.session_state.profile_risk_score
            }])[feature_columns]
            pred_class = model.predict(in_df)[0]
            risk_pred = str(pred_class)
            if hasattr(model, 'predict_proba'):
                probs = model.predict_proba(in_df)[0]
                classes = model.classes_
                prob_dict = {str(c): float(p) * 100.0 for c, p in zip(classes, probs)}
                risk_probs = prob_dict
                risk_confidence = max(probs) * 100.0
        except Exception:
            risk_pred = None

    risk_pred_display = str(risk_pred) if risk_pred is not None else "Unavailable"
    risk_confidence_display = f"{risk_confidence:.1f}%" if risk_confidence is not None else "Unavailable"

    # ==============================================================================
    # 4. OVERVIEW PAGE
    # ==============================================================================
    if nav_selection == "Overview":

        # ------------------------------------------------------------------
        # Pre-compute badge colours (used throughout, no CSS class needed)
        # ------------------------------------------------------------------
        def badge_style(bg, clr, brd):
            return f"font-size:0.72rem;font-weight:700;padding:0.2rem 0.55rem;border-radius:6px;background:{bg};color:{clr};border:1px solid {brd};"

        h_bg  = "#E9D8FF" if score_val >= 80 else ("#F3EBFF" if score_val >= 60 else ("#FFF4E5" if score_val >= 40 else "#FEECEC"))
        h_clr = "#8B5CF6" if score_val >= 80 else ("#6D28D9" if score_val >= 60 else ("#D97706" if score_val >= 40 else "#DC2626"))
        h_brd = "#E9D8FF" if score_val >= 80 else ("#DDD0FF" if score_val >= 60 else ("#F8D7A8" if score_val >= 40 else "#FECACA"))

        r_bg  = "#F5F0FF" if risk_pred is None else ("#E9D8FF" if risk_pred == "Low" else ("#F3EBFF" if risk_pred == "Moderate" else "#FEECEC"))
        r_clr = "#6B6480" if risk_pred_display == "Unavailable" else ("#8B5CF6" if risk_pred == "Low" else ("#6D28D9" if risk_pred == "Moderate" else "#DC2626"))
        r_brd = "#DDD0FF" if risk_pred is None else ("#E9D8FF" if risk_pred == "Low" else ("#DDD0FF" if risk_pred == "Moderate" else "#FECACA"))

        g_bg  = "#E9D8FF" if "Track" in goal_info['feasibility_status'] else "#FFF4E5"
        g_clr = "#8B5CF6" if "Track" in goal_info['feasibility_status'] else "#D97706"
        g_brd = "#E9D8FF" if "Track" in goal_info['feasibility_status'] else "#F8D7A8"

        s_bg  = "#E9D8FF" if u_surplus >= 15000 else "#E9D8FF"
        s_clr = "#8B5CF6" if u_surplus >= 15000 else "#059669"
        s_brd = "#E9D8FF" if u_surplus >= 15000 else "#E9D8FF"

        CARD = "background:#FFFFFF;border:1px solid #DDD0FF;border-radius:16px;padding:1.25rem 1.35rem;box-shadow:0 1px 3px rgba(36,24,59,0.04),0 6px 16px rgba(36,24,59,0.04);"

        # ------------------------------------------------------------------
        # HERO SECTION
        # ------------------------------------------------------------------
        st.markdown(textwrap.dedent(f"""
        <div style="background:linear-gradient(135deg,#FFFFFF 0%,#F5F0FF 100%);border:1px solid rgba(109,40,217,0.16);border-radius:16px;padding:1.5rem 1.8rem;margin-bottom:1.3rem;display:flex;justify-content:space-between;align-items:center;box-shadow:0 1px 3px rgba(36,24,59,0.04);position:relative;overflow:hidden;">
            <div>
                <h1 style="font-size:1.65rem;font-weight:800;color:#24183B;margin:0;line-height:1.2;">Your Money at a Glance</h1>
                <p style="font-size:0.88rem;color:#6B6480;margin-top:0.4rem;margin-bottom:0;max-width:650px;line-height:1.45;">A plain-language snapshot of your financial health, model result, monthly cash flow, and savings goal.</p>
            </div>
            <div style="display:flex;align-items:center;gap:8px;background:#F3EBFF;border:1px solid rgba(56,103,246,0.2);padding:0.6rem 1rem;border-radius:12px;color:#6D28D9;font-weight:700;font-size:0.82rem;white-space:nowrap;">
                Educational estimate
            </div>
        </div>
        """), unsafe_allow_html=True)

        # ------------------------------------------------------------------
        # KPI CARDS — 4 columns, 100% inline styles
        # ------------------------------------------------------------------
        c1, c2, c3, c4 = st.columns(4, gap="small")
        with c1:
            st.markdown(textwrap.dedent(f"""
            <div class="overview-kpi-card" style="{CARD}">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;">
                    <span style="font-size:0.74rem;font-weight:700;color:#6B6480;text-transform:uppercase;letter-spacing:0.05em;">Financial Health</span>
                    <span style="{badge_style(h_bg,h_clr,h_brd)}">{cat_val.upper()}</span>
                </div>
                <div style="font-size:1.85rem;font-weight:800;color:#24183B;letter-spacing:-0.03em;line-height:1.15;">{score_val:.1f}&thinsp;<span style="font-size:0.95rem;color:#6B6480;font-weight:500;">/&nbsp;100</span></div>
                <div style="font-size:0.78rem;color:#6B6480;margin-top:0.35rem;">Based on the profile you entered</div>
            </div>"""), unsafe_allow_html=True)
        with c2:
            st.markdown(textwrap.dedent(f"""
            <div class="overview-kpi-card" style="{CARD}">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;">
                    <span style="font-size:0.74rem;font-weight:700;color:#6B6480;text-transform:uppercase;letter-spacing:0.05em;">AI Risk Profile</span>
                    <span style="{badge_style(r_bg,r_clr,r_brd)}">{risk_pred_display.upper()}</span>
                </div>
                <div style="font-size:1.85rem;font-weight:800;color:#24183B;letter-spacing:-0.03em;line-height:1.15;">{risk_pred_display}</div>
                <div style="font-size:0.78rem;color:#6B6480;margin-top:0.35rem;">Top category match: {risk_confidence_display}</div>
            </div>"""), unsafe_allow_html=True)
        with c3:
            st.markdown(textwrap.dedent(f"""
            <div class="overview-kpi-card" style="{CARD}">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;">
                    <span style="font-size:0.74rem;font-weight:700;color:#6B6480;text-transform:uppercase;letter-spacing:0.05em;">Goal Progress</span>
                    <span style="{badge_style(g_bg,g_clr,g_brd)}">{goal_info['feasibility_status']}</span>
                </div>
                <div style="font-size:1.85rem;font-weight:800;color:#24183B;letter-spacing:-0.03em;line-height:1.15;">{metrics['goal_progress_pct']:.1f}%</div>
                <div style="font-size:0.78rem;color:#6B6480;margin-top:0.35rem;">₹{u_savings:,.0f} of ₹{u_goal:,.0f}</div>
            </div>"""), unsafe_allow_html=True)
        with c4:
            st.markdown(textwrap.dedent(f"""
            <div class="overview-kpi-card" style="{CARD}">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;">
                    <span style="font-size:0.74rem;font-weight:700;color:#6B6480;text-transform:uppercase;letter-spacing:0.05em;">Income left after expenses</span>
                    <span style="{badge_style(s_bg,s_clr,s_brd)}">Calculated</span>
                </div>
                <div style="font-size:1.85rem;font-weight:800;color:#24183B;letter-spacing:-0.03em;line-height:1.15;">{format_inr(u_cash_remaining)}</div>
                <div style="font-size:0.78rem;color:#6B6480;margin-top:0.35rem;">Monthly income minus monthly expenses</div>
            </div>"""), unsafe_allow_html=True)

        cash_metrics = st.columns(4, gap="small")
        cash_values = [
            ("Monthly income", format_inr(u_income)),
            ("Monthly expenses", format_inr(u_expense)),
            ("Monthly savings entered", format_inr(u_surplus)),
            ("Current savings", format_inr(u_savings)),
        ]
        for metric_column, (label, value) in zip(cash_metrics, cash_values):
            with metric_column:
                st.metric(label, value)
        st.caption(
            f"After monthly expenses, income leaves {format_inr(u_cash_remaining)}. "
            f"You entered {format_inr(u_surplus)} as monthly savings for the score and goal estimate. "
            f"You spend {metrics['expense_ratio_pct']:.1f}% of monthly income. "
            f"Your current savings would cover about {metrics['ef_months']:.1f} months of expenses "
            "if income stopped and spending stayed the same. This is a simple estimate."
        )

        st.markdown("<div style='height:1.1rem'></div>", unsafe_allow_html=True)

        # ------------------------------------------------------------------
        # FINANCIAL HEALTH SCORE + GOAL JOURNEY
        # ------------------------------------------------------------------
        col_health, col_goal = st.columns([1.2, 1], gap="medium")

        with col_health:
            sorted_dims = sorted(components.items(), key=lambda x: x[1], reverse=True)
            strongest_dim = sorted_dims[0][0]
            weakest_dim   = sorted_dims[-1][0]
            plain_dimension_names = {
                "Savings Rate": "monthly savings",
                "Debt Burden": "debt compared with yearly income",
                "Emergency Fund": "emergency savings",
                "Expense Ratio": "monthly spending compared with income",
                "Monthly Surplus": "money left after expenses",
                "Goal Progress": "progress toward your goal",
            }
            explanation_text = (
                f"Your strongest area is <strong>{plain_dimension_names[strongest_dim]}</strong> "
                f"({sorted_dims[0][1]}%). Your lowest area is "
                f"<strong>{plain_dimension_names[weakest_dim]}</strong> ({sorted_dims[-1][1]}%)."
            )

            DIM_COLORS = {
                'Savings Rate': '#6D28D9', 'Debt Burden': '#8B5CF6',
                'Emergency Fund': '#8B5CF6', 'Expense Ratio': '#D97706',
                'Monthly Surplus': '#6D28D9', 'Goal Progress': '#DC2626'
            }
            dim_html = "".join([
                f'<div style="margin-bottom:0.62rem;"><div style="display:flex;justify-content:space-between;font-size:0.77rem;font-weight:700;color:#24183B;margin-bottom:0.22rem;"><span>{dname}</span><span>{dscore}%</span></div><div style="height:7px;background:#F5F0FF;border-radius:9999px;overflow:hidden;"><div style="height:7px;width:{dscore}%;background:{DIM_COLORS.get(dname, "#6D28D9")};border-radius:9999px;"></div></div></div>'
                for dname, dscore in components.items()
            ])

            st.markdown(textwrap.dedent(f"""
            <div style="{CARD}">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.9rem;">
                    <span style="font-size:0.82rem;font-weight:800;text-transform:uppercase;letter-spacing:0.05em;color:#24183B;">Financial Health Score</span>
                    <span style="{badge_style(h_bg,h_clr,h_brd)}">{cat_val.upper()}</span>
                </div>
                <div style="display:grid;grid-template-columns:170px 1fr;gap:1rem;align-items:center;">
                    {generate_health_donut_svg(score_val, cat_val)}
                    <div style="padding-top:0.5rem;">{dim_html}</div>
                </div>
                <div style="background:#F3EBFF;border:1px solid rgba(56,103,246,0.2);border-radius:10px;padding:0.75rem 1rem;font-size:0.8rem;color:#6D28D9;line-height:1.45;margin-top:0.9rem;">
                    💡 {explanation_text}
                </div>
                <div style="font-size:0.72rem;color:#6B6480;line-height:1.45;margin-top:0.65rem;">
                    Note: These percentages are dashboard-generated educational scores, not actual percentages of money saved or credit ratings.
                </div>
            </div>
            """), unsafe_allow_html=True)

        with col_goal:
            pct = metrics['goal_progress_pct']

            # Node states
            def _node_style(cls):
                if cls == "passed":
                    return "background:#6D28D9;border-color:#6D28D9;color:#FFFFFF;"
                elif cls == "active":
                    return "background:#8B5CF6;border-color:#8B5CF6;color:#FFFFFF;box-shadow:0 0 12px rgba(139,92,246,0.5);"
                return "background:#FFFFFF;border-color:#6D28D9;color:#6D28D9;"

            n0  = "passed" if pct > 0   else "active"
            n33 = "passed" if pct >= 33 else ("active" if pct > 0  else "")
            n66 = "passed" if pct >= 66 else ("active" if pct >= 33 else "")
            n100= "active" if pct >= 100 else ""

            # Fill line: correct CSS calc spanning the track (100% - 4rem)
            fill_fraction = min(pct / 100.0, 1.0)

            goal_callout_text = (
                "🎯 GOAL ON TRACK — You are mathematically on track to reach your target within the selected horizon."
                if "Track" in goal_info['feasibility_status']
                else (
                    "⚠️ NO TIME REMAINING — Increase savings or extend the investment horizon to fund this goal."
                    if u_horizon_months == 0
                    else f"⚠️ ATTENTION NEEDED — Monthly savings gap of ₹{goal_info['monthly_saving_gap']:,.0f} detected against timeline."
                )
            )
            gc_bg  = "#E9D8FF" if "Track" in goal_info['feasibility_status'] else "#FFF4E5"
            gc_brd = "#E9D8FF" if "Track" in goal_info['feasibility_status'] else "#F8D7A8"
            gc_clr = "#059669" if "Track" in goal_info['feasibility_status'] else "#D97706"

            st.markdown(textwrap.dedent(f"""
            <div style="{CARD}">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.8rem;">
                    <span style="font-size:0.82rem;font-weight:800;text-transform:uppercase;letter-spacing:0.05em;color:#24183B;">🎯 Financial Goal Journey</span>
                    <span style="{badge_style(g_bg,g_clr,g_brd)}">{goal_info['feasibility_status']}</span>
                </div>
                <div style="position:relative;margin:1.2rem 0 0.4rem 0;padding:0 1rem;height:34px;">
                    <div style="position:absolute;top:15px;left:2rem;right:2rem;height:4px;background:#DDD0FF;border-radius:2px;z-index:1;"></div>
                    <div style="position:absolute;top:15px;left:2rem;height:4px;width:calc((100% - 4rem) * {fill_fraction:.4f});background:linear-gradient(90deg,#6D28D9 0%,#8B5CF6 100%);border-radius:2px;z-index:2;"></div>
                    <div style="position:relative;display:flex;justify-content:space-between;align-items:center;z-index:3;">
                        <div style="width:32px;height:32px;border-radius:50%;border:3px solid;display:flex;align-items:center;justify-content:center;font-size:0.70rem;font-weight:800;{_node_style(n0)}">0%</div>
                        <div style="width:32px;height:32px;border-radius:50%;border:3px solid;display:flex;align-items:center;justify-content:center;font-size:0.70rem;font-weight:800;{_node_style(n33)}">33%</div>
                        <div style="width:32px;height:32px;border-radius:50%;border:3px solid;display:flex;align-items:center;justify-content:center;font-size:0.70rem;font-weight:800;{_node_style(n66)}">66%</div>
                        <div style="width:32px;height:32px;border-radius:50%;border:3px solid;display:flex;align-items:center;justify-content:center;font-size:0.78rem;font-weight:800;{_node_style(n100)}">🎯</div>
                    </div>
                </div>
                <div style="display:flex;justify-content:space-between;font-size:0.70rem;color:#6B6480;font-weight:700;padding:0 0.4rem;margin-bottom:0.2rem;">
                    <span>START</span><span>CURRENT ({pct:.1f}%)</span><span>MILESTONE</span><span>TARGET</span>
                </div>
                <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.7rem;margin-top:0.9rem;padding-top:0.8rem;border-top:1px solid #F5F0FF;">
                    <div>
                        <div style="font-size:0.71rem;color:#6B6480;font-weight:600;">Goal target</div>
                        <div style="font-size:1.05rem;font-weight:800;color:#24183B;margin-top:2px;">₹{u_goal:,.0f}</div>
                    </div>
                    <div>
                        <div style="font-size:0.71rem;color:#6B6480;font-weight:600;">Saved so far</div>
                        <div style="font-size:1.05rem;font-weight:800;color:#6D28D9;margin-top:2px;">₹{u_savings:,.0f}</div>
                    </div>
                    <div>
                        <div style="font-size:0.71rem;color:#6B6480;font-weight:600;">Still needed</div>
                        <div style="font-size:1.05rem;font-weight:800;color:#DC2626;margin-top:2px;">₹{goal_info['goal_remaining']:,.0f}</div>
                    </div>
                    <div>
                        <div style="font-size:0.71rem;color:#6B6480;font-weight:600;">Needed each month</div>
                        <div style="font-size:0.92rem;font-weight:800;color:#24183B;margin-top:2px;">{required_monthly_display}</div>
                    </div>
                    <div>
                        <div style="font-size:0.71rem;color:#6B6480;font-weight:600;">Current Monthly</div>
                        <div style="font-size:1.05rem;font-weight:800;color:#8B5CF6;margin-top:2px;">₹{u_surplus:,.0f}</div>
                    </div>
                    <div>
                        <div style="font-size:0.71rem;color:#6B6480;font-weight:600;">Monthly Gap</div>
                        <div style="font-size:1.05rem;font-weight:800;color:#24183B;margin-top:2px;">₹{goal_info['monthly_saving_gap']:,.0f}</div>
                    </div>
                </div>
                <div style="background:{gc_bg};border:1px solid {gc_brd};border-radius:10px;padding:0.75rem 1rem;font-size:0.8rem;color:{gc_clr};line-height:1.45;margin-top:0.9rem;">
                    {goal_callout_text}
                </div>
            </div>
            """), unsafe_allow_html=True)
            st.caption(f"For {horizon_display}, this simple estimate divides the amount still needed by the months available. It assumes no investment growth, interest, fees, or changes in monthly savings.")

        st.markdown("<div style='height:1.1rem'></div>", unsafe_allow_html=True)

        # ------------------------------------------------------------------
        # AI RISK INTELLIGENCE — 2 columns, 100% inline styles
        # ------------------------------------------------------------------
        col_risk_left, col_risk_right = st.columns([1, 1], gap="medium")

        # Dynamic Reason Generator
        reasons = []
        if u_savings_rate >= 30:
            reasons.append(("<span style='color:#8B5CF6;font-weight:800;'>✓</span>", f"Monthly savings are {u_savings_rate:.1f}% of income"))
        else:
            reasons.append(("<span style='color:#D97706;font-weight:800;'>⚠️</span>", f"Monthly savings are {u_savings_rate:.1f}% of income"))
        if metrics['ef_months'] >= 6:
            reasons.append(("<span style='color:#8B5CF6;font-weight:800;'>✓</span>", f"Current savings cover about {metrics['ef_months']:.1f} months of expenses"))
        else:
            reasons.append(("<span style='color:#DC2626;font-weight:800;'>⚠️</span>", f"Current savings cover about {metrics['ef_months']:.1f} months of expenses"))
        if u_surplus > 0:
            reasons.append(("<span style='color:#8B5CF6;font-weight:800;'>✓</span>", f"Monthly savings entered: {format_inr(u_surplus)}"))
        else:
            reasons.append(("<span style='color:#DC2626;font-weight:800;'>⚠️</span>", "No monthly savings amount was entered"))
        if metrics['dti_pct'] <= 25:
            reasons.append(("<span style='color:#8B5CF6;font-weight:800;'>✓</span>", f"Debt is {metrics['dti_pct']:.1f}% of yearly income"))
        else:
            reasons.append(("<span style='color:#D97706;font-weight:800;'>⚠️</span>", f"Debt is {metrics['dti_pct']:.1f}% of yearly income"))

        overview_probability_rows = []
        if risk_probs is not None:
            overview_probability_rows = [
                (label, color, risk_probs[class_name])
                for class_name, label, color in [
                    ("Low", "LOW", "#8B5CF6"),
                    ("Moderate", "MODERATE", "#6D28D9"),
                    ("High", "HIGH", "#DC2626"),
                ]
                if class_name in risk_probs
            ]
        risk_bars_html = "".join([
            f'<div style="margin-bottom:0.7rem;"><div style="display:flex;justify-content:space-between;font-size:0.76rem;font-weight:700;color:#24183B;margin-bottom:0.22rem;"><span>{label}</span><span>{prob:.1f}%</span></div><div style="height:7px;background:#F5F0FF;border-radius:9999px;overflow:hidden;"><div style="height:7px;width:{min(prob,100):.1f}%;background:{clr};border-radius:9999px;"></div></div></div>'
            for label, clr, prob in overview_probability_rows
        ]) or "<p>Category match percentages are unavailable from the saved model.</p>"

        with col_risk_left:
            st.markdown(textwrap.dedent(f"""
            <div style="{CARD}">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.8rem;">
                    <span style="font-size:0.82rem;font-weight:800;text-transform:uppercase;letter-spacing:0.05em;color:#24183B;">⚡ AI Risk Intelligence</span>
                    <span style="{badge_style(r_bg,r_clr,r_brd)}">{model_name_display}</span>
                </div>
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:1.1rem;flex-wrap:wrap;">
                    <div style="font-size:2rem;font-weight:800;color:#6D28D9;">{risk_pred_display}</div>
                    <span style="{badge_style(r_bg,r_clr,r_brd)}">Top category match: {risk_confidence_display}</span>
                </div>
                <div style="font-size:0.76rem;font-weight:800;color:#6B6480;margin-bottom:0.5rem;letter-spacing:0.04em;">CATEGORY MATCH STRENGTH</div>
                {risk_bars_html}
            </div>
            """), unsafe_allow_html=True)

        reasons_rows = "".join([
            f"""<div style='display:flex;align-items:flex-start;gap:8px;font-size:0.8rem;color:#24183B;padding:0.35rem 0;border-bottom:1px solid #F5F0FF;'>{icon}<span>{text}</span></div>"""
            for icon, text in reasons
        ])
        with col_risk_right:
            st.markdown(textwrap.dedent(f"""
            <div style="{CARD}">
                <div style="font-size:0.82rem;font-weight:800;text-transform:uppercase;letter-spacing:0.05em;color:#24183B;margin-bottom:0.8rem;">What in your profile matters here?</div>
                <p style="font-size:0.8rem;color:#6B6480;margin-bottom:0.8rem;">These parts of your profile are included in its analysis. Category: <strong>{risk_pred_display}</strong>.</p>
                <div>{reasons_rows}</div>
                <div style="margin-top:1rem;padding-top:0.8rem;border-top:1px solid #F5F0FF;font-size:0.74rem;color:#6B6480;">
                    {model_accuracy_explanation}
                </div>
            </div>
            """), unsafe_allow_html=True)
        # Overview Wealth Forecast Area Chart
        st.markdown("<div style='height:1.1rem'></div>", unsafe_allow_html=True)
        ov_years = np.linspace(0, u_horizon, num=max(2, int(np.ceil(u_horizon)) + 1))
        ov_proj = [u_savings + (u_surplus * 12 * y) for y in ov_years]

        fig_ov = go.Figure()
        fig_ov.add_trace(go.Scatter(
            x=ov_years, y=ov_proj, mode='lines+markers', name='Projected Savings (₹)',
            line=dict(color='#6D28D9', width=3.5),
            fill='tozeroy', fillcolor='rgba(56,103,246,0.06)'
        ))
        fig_ov.add_hline(y=u_goal, line_dash="dot", line_color="#8B5CF6", annotation_text=f"Target Goal: ₹{u_goal:,.0f}", annotation_position="top left")

        fig_ov.update_layout(
            title=f"Projected Wealth Growth Trajectory over {horizon_display}",
            xaxis_title="Horizon Timeline (Years)",
            yaxis_title="Accumulated Capital (₹)",
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#F5F0FF",
            height=330,
            margin=dict(l=10, r=10, t=40, b=10),
            font=dict(family="Plus Jakarta Sans", color="#24183B")
        )
        st.plotly_chart(fig_ov, use_container_width=True)

    # ==============================================================================
    # 8. AI RISK DEEP DIVE PAGE
    # ==============================================================================
    elif nav_selection == "AI Risk Analysis":
        st.markdown("""
<div style="margin-bottom: 1.2rem;">
    <h1 style="font-size: 1.75rem; font-weight: 800; color: #24183B; margin: 0;">
    What Does the Model Say About Your Financial Profile?
    </h1>
    <p style="font-size: 0.88rem; color: #6B6480; margin-top: 0.2rem;">
    This is a model prediction based on the profile you entered, not a measure of the chance you will lose money.
    </p>
</div>
""", unsafe_allow_html=True)

        CARD = "background:#FFFFFF;border:1px solid #DDD0FF;border-radius:16px;padding:1.25rem 1.35rem;box-shadow:0 1px 3px rgba(36,24,59,0.04),0 6px 16px rgba(36,24,59,0.04);"

        def badge_style(bg, clr, brd):
            return f"font-size:0.72rem;font-weight:700;padding:0.2rem 0.55rem;border-radius:6px;background:{bg};color:{clr};border:1px solid {brd};"

        r_bg  = "#F5F0FF" if risk_pred is None else ("#E9D8FF" if risk_pred == "Low" else ("#F3EBFF" if risk_pred == "Moderate" else "#FEECEC"))
        r_clr = "#6B6480" if risk_pred is None else ("#8B5CF6" if risk_pred == "Low" else ("#6D28D9" if risk_pred == "Moderate" else "#DC2626"))
        r_brd = "#DDD0FF" if risk_pred is None else ("#E9D8FF" if risk_pred == "Low" else ("#DDD0FF" if risk_pred == "Moderate" else "#FECACA"))

        # ── Row 1: Prediction Card + Confidence Card + Accuracy Card ──────────
        k1, k2, k3 = st.columns(3, gap="medium")
        with k1:
            st.markdown(f"""
<div style="{CARD}">
    <div style="font-size:0.74rem;font-weight:700;color:#6B6480;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.5rem;">Predicted profile category</div>
    <div style="font-size:2rem;font-weight:800;color:#6D28D9;">{risk_pred_display}</div>
    <div style="margin-top:0.4rem;"><span style="{badge_style(r_bg, r_clr, r_brd)}">Top category match: {risk_confidence_display}</span></div>
</div>""", unsafe_allow_html=True)

        with k2:
            st.markdown(f"""
<div style="{CARD}">
    <div style="font-size:0.74rem;font-weight:700;color:#6B6480;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.5rem;">Validation accuracy</div>
    <div style="font-size:2rem;font-weight:800;color:#8B5CF6;letter-spacing:-0.02em;">{model_acc_display}</div>
    <div style="font-size:0.78rem;color:#6B6480;margin-top:0.4rem;">Share of test examples classified correctly</div>
</div>""", unsafe_allow_html=True)

        with k3:
            st.markdown(f"""
<div style="{CARD}">
    <div style="font-size:0.74rem;font-weight:700;color:#6B6480;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.5rem;">Prediction method</div>
    <div style="font-size:1.15rem;font-weight:800;color:#24183B;letter-spacing:-0.01em;margin-top:0.3rem;">{model_name_display}</div>
    <div style="font-size:0.78rem;color:#6B6480;margin-top:0.4rem;">Trained using labeled examples</div>
</div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        # ── Row 2: Probability Spectrum + Risk Reasons ─────────────────────────
        col_prob, col_why = st.columns([1, 1.2], gap="medium")

        probability_rows = []
        if risk_probs is not None:
            probability_rows = [
                (label, color, risk_probs[class_name])
                for class_name, label, color in [
                    ("Low", "LOW", "#8B5CF6"),
                    ("Moderate", "MODERATE", "#6D28D9"),
                    ("High", "HIGH", "#DC2626"),
                ]
                if class_name in risk_probs
            ]
        risk_bars_html = "".join([
            f'<div style="margin-bottom:0.85rem;"><div style="display:flex;justify-content:space-between;font-size:0.78rem;font-weight:700;color:#24183B;margin-bottom:0.28rem;"><span>{label}</span><span>{prob:.1f}%</span></div><div style="height:10px;background:#F5F0FF;border-radius:9999px;overflow:hidden;"><div style="height:10px;width:{min(prob,100):.1f}%;background:{clr};border-radius:9999px;"></div></div></div>'
            for label, clr, prob in probability_rows
        ]) or "<p>Category match percentages are unavailable because the saved model did not provide them.</p>"
        with col_prob:
            st.markdown(f"""
<div style="{CARD}">
    <div style="font-size:0.82rem;font-weight:800;text-transform:uppercase;letter-spacing:0.05em;color:#24183B;margin-bottom:1rem;">How strongly each category matches</div>
    {risk_bars_html}
    <div style="margin-top:0.9rem;padding-top:0.75rem;border-top:1px solid #F5F0FF;font-size:0.75rem;color:#6B6480;">
        These percentages compare profile categories. They are not probabilities of financial loss or a guarantee about what will happen.
    </div>
</div>""", unsafe_allow_html=True)

        # Dynamic risk reasons
        reasons = []
        if u_savings_rate >= 30:
            reasons.append(("✓", "#8B5CF6", f"Monthly savings entered are {u_savings_rate:.1f}% of income"))
        else:
            reasons.append(("⚠", "#D97706", f"Monthly savings entered are {u_savings_rate:.1f}% of income"))
        if metrics['ef_months'] >= 6:
            reasons.append(("✓", "#8B5CF6", f"Current savings cover about {metrics['ef_months']:.1f} months of expenses"))
        else:
            reasons.append(("⚠", "#DC2626", f"Current savings cover about {metrics['ef_months']:.1f} months of expenses"))
        if u_surplus > 0:
            reasons.append(("✓", "#8B5CF6", f"Monthly savings entered: {format_inr(u_surplus)}"))
        else:
            reasons.append(("⚠", "#DC2626", "No monthly savings amount was entered"))
        if metrics['dti_pct'] <= 25:
                reasons.append(("✓", "#8B5CF6", f"Debt is {metrics['dti_pct']:.1f}% of yearly income, a lower share by this dashboard's measure"))
        else:
                reasons.append(("⚠", "#D97706", f"Debt is {metrics['dti_pct']:.1f}% of yearly income; review your balances and required payments"))

        reasons_html = "".join([
            f'<div style="display:flex;align-items:flex-start;gap:10px;padding:0.45rem 0;border-bottom:1px solid #F5F0FF;font-size:0.8rem;color:#24183B;"><span style="color:{clr};font-weight:800;font-size:0.9rem;flex-shrink:0;">{icon}</span><span>{text}</span></div>'
            for icon, clr, text in reasons
        ])

        with col_why:
            st.markdown(f"""
<div style="{CARD}">
    <div style="font-size:0.82rem;font-weight:800;text-transform:uppercase;letter-spacing:0.05em;color:#24183B;margin-bottom:0.3rem;">What in your profile matters here?</div>
    <p style="font-size:0.8rem;color:#6B6480;margin-bottom:0.8rem;">These parts of your profile help explain the <strong>{risk_pred_display}</strong> category:</p>
    <div>{reasons_html}</div>
    <div style="margin-top:1rem;padding-top:0.8rem;border-top:1px solid #F5F0FF;font-size:0.74rem;color:#6B6480;">
        {model_accuracy_explanation}
    </div>
</div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        # ── Row 3: Risk Radar Chart ────────────────────────────────────────────
        radar_categories = ['Monthly savings', 'Debt vs yearly income', 'Emergency savings', 'Spending vs income', 'Money left monthly', 'Goal progress']
        radar_component_keys = ['Savings Rate', 'Debt Burden', 'Emergency Fund', 'Expense Ratio', 'Monthly Surplus', 'Goal Progress']
        radar_values = [components[key] for key in radar_component_keys]
        radar_values_closed = radar_values + [radar_values[0]]
        radar_cats_closed = radar_categories + [radar_categories[0]]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=radar_values_closed,
            theta=radar_cats_closed,
            fill='toself',
            name='Your Profile',
            fillcolor='rgba(56,103,246,0.12)',
            line=dict(color='#6D28D9', width=2.5)
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=[75] * (len(radar_categories) + 1),
            theta=radar_cats_closed,
            fill='toself',
            name='Benchmark (75)',
            fillcolor='rgba(19,184,166,0.05)',
            line=dict(color='#8B5CF6', width=1.5, dash='dot')
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=10), gridcolor='#F5F0FF'),
                angularaxis=dict(tickfont=dict(size=11, color='#24183B'))
            ),
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            height=380,
            margin=dict(l=40, r=40, t=40, b=60),
            title=dict(text="Your profile compared with a reference score", font=dict(size=14, color='#24183B', family='Plus Jakarta Sans')),
            font=dict(family="Plus Jakarta Sans", color="#24183B")
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        st.caption("The shape compares six parts of your financial profile with a reference score of 75. It is a profile comparison, not a forecast of loss.")

    # ==============================================================================
    # 9. WHAT-IF WEALTH SIMULATOR (SIGNATURE FEATURE)
    # ==============================================================================
    elif nav_selection == "What-If Simulator":
        st.markdown("""
        <div class="simulator-page-heading" style="margin-bottom: 1.2rem;">
            <h1 style="font-size: 1.75rem; font-weight: 800; color: #24183B; margin: 0;">
                Try Different Money Scenarios
            </h1>
            <p style="font-size: 0.88rem; color: #6B6480; margin-top: 0.2rem;">
                Change these temporary scenario values to see how the estimates compare with your saved profile. Scenario changes do not edit Profile Settings.
            </p>
        </div>
        """, unsafe_allow_html=True)

        simulator_defaults = {
            "sim_income_input": u_income,
            "sim_expense_input": u_expense,
            "sim_savings_input": u_savings,
            "sim_debt_input": u_debt,
            "sim_goal_input": u_goal,
            "sim_horizon_years": st.session_state.profile_horizon_years_input,
            "sim_horizon_months": st.session_state.profile_horizon_months_input,
        }
        for simulator_key, default_value in simulator_defaults.items():
            if simulator_key not in st.session_state:
                st.session_state[simulator_key] = default_value

        col_controls, col_display = st.columns([1.1, 2], gap="large")

        with col_controls:
            st.markdown('<div class="simulator-controls-heading" style="font-size:0.82rem;font-weight:800;color:#6D28D9;text-transform:uppercase;margin-bottom:0.5rem;">Scenario values</div>', unsafe_allow_html=True)

            sim_income = st.slider("Monthly income (₹)", min_value=20000.0, max_value=250000.0, value=float(st.session_state.sim_income_input), step=5000.0, key="sim_income_input")
            sim_expense = st.slider("Monthly expenses (₹)", min_value=0.0, max_value=float(sim_income), value=float(min(st.session_state.sim_expense_input, sim_income)), step=2500.0, key="sim_expense_input")
            sim_savings = st.slider("Current savings (₹)", min_value=0.0, max_value=2000000.0, value=float(st.session_state.sim_savings_input), step=25000.0, key="sim_savings_input")
            sim_debt = st.slider("Total debt (₹)", min_value=0.0, max_value=500000.0, value=float(st.session_state.sim_debt_input), step=5000.0, key="sim_debt_input")
            sim_goal = st.slider("Savings goal (₹)", min_value=0.0, max_value=3000000.0, value=float(st.session_state.sim_goal_input), step=50000.0, key="sim_goal_input")
            sim_horizon_col_years, sim_horizon_col_months = st.columns(2, gap="small")
            with sim_horizon_col_years:
                sim_horizon_years = st.number_input("Years", min_value=0, max_value=30, value=int(st.session_state.sim_horizon_years), step=1, key="sim_horizon_years")
            with sim_horizon_col_months:
                sim_horizon_months = st.number_input("Months", min_value=0, max_value=11, value=int(st.session_state.sim_horizon_months), step=1, key="sim_horizon_months")
            sim_total_horizon_months = combine_horizon_months(sim_horizon_years, sim_horizon_months)
            sim_horizon = sim_total_horizon_months / 12.0
            sim_horizon_display = format_horizon_months(sim_total_horizon_months)
            st.caption(f"Scenario goal horizon: {sim_horizon_display}")
            st.button("Reset to saved profile", on_click=reset_simulator_to_profile, use_container_width=True)

        # Compute Simulated Results
        sim_surplus = max(0.0, sim_income - sim_expense)
        sim_score, sim_cat, sim_comps, sim_metrics = compute_financial_health_score(
            sim_income, sim_expense, sim_surplus, sim_savings, sim_debt, sim_goal, sim_horizon
        )
        sim_goal_info = compute_goal_feasibility(
            sim_savings, sim_goal, sim_horizon, sim_surplus, sim_metrics['goal_progress_pct'],
            total_horizon_months=sim_total_horizon_months
        )

        sim_risk = None
        if model is not None and feature_columns is not None:
            try:
                sim_in_df = pd.DataFrame([{
                    'age': st.session_state.profile_age,
                    'monthly_income': sim_income,
                    'monthly_expense': sim_expense,
                    'monthly_savings': sim_surplus,
                    'current_savings': sim_savings,
                    'debt': sim_debt,
                    'financial_goal_amount': sim_goal,
                    'investment_horizon_years': sim_horizon,
                    'risk_tolerance_score': st.session_state.profile_risk_score
                }])[feature_columns]
                sim_risk = str(model.predict(sim_in_df)[0])
            except Exception:
                sim_risk = None

        score_diff = sim_score - score_val
        goal_diff = sim_metrics['goal_progress_pct'] - metrics['goal_progress_pct']

        with col_display:
            st.markdown(textwrap.dedent("""
            <div style="font-size: 0.84rem; font-weight: 800; color: #24183B; text-transform: uppercase; margin-bottom: 0.75rem;">
                Saved profile compared with this scenario
            </div>
            """), unsafe_allow_html=True)

            comparison_rows = [
                ("Monthly income", u_income, sim_income),
                ("Monthly expenses", u_expense, sim_expense),
                ("Money left after expenses", u_cash_remaining, sim_surplus),
                ("Monthly savings entered", u_surplus, sim_surplus),
                ("Current savings", u_savings, sim_savings),
                ("Total debt", u_debt, sim_debt),
            ]
            for row_start in range(0, len(comparison_rows), 3):
                comparison_columns = st.columns(3, gap="small")
                for comparison_column, (label, base_value, scenario_value) in zip(comparison_columns, comparison_rows[row_start:row_start + 3]):
                    with comparison_column:
                        st.metric(
                            label,
                            f"₹{scenario_value:,.0f}",
                            delta=f"vs saved profile ₹{base_value:,.0f}",
                            delta_color="off"
                        )

            badge1_cls = "badge-success" if score_diff >= 0 else "badge-danger"
            diff1_sign = "+" if score_diff >= 0 else ""
            badge2_cls = "badge-success" if goal_diff >= 0 else "badge-danger"
            diff2_sign = "+" if goal_diff >= 0 else ""

            h_change_str = f"{score_val:.0f}" + " &rarr; <span style='color: #6D28D9;'>" + f"{sim_score:.0f}" + "</span>"
            g_change_str = f"{metrics['goal_progress_pct']:.1f}%" + " &rarr; <span style='color: #8B5CF6;'>" + f"{sim_metrics['goal_progress_pct']:.1f}%" + "</span>"
            scenario_risk_display = str(sim_risk) if sim_risk is not None else "Unavailable"
            r_change_str = f"{risk_pred_display} &rarr; <span style='color: #6D28D9;'>{scenario_risk_display}</span>"
            diff1_text = f"{diff1_sign}{score_diff:.1f} pts"
            diff2_text = f"{diff2_sign}{goal_diff:.1f}%"

            r1, r2, r3 = st.columns(3, gap="medium")
            with r1:
                st.markdown(textwrap.dedent(f"""
                <div class="sim-compare-card">
                    <div style="font-size: 0.74rem; font-weight: 700; color: #6B6480;">HEALTH SCORE</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #24183B; margin: 0.3rem 0;">
                        {h_change_str}
                    </div>
                    <span class="sim-diff-badge {badge1_cls}">
                        {diff1_text}
                    </span>
                </div>
                """), unsafe_allow_html=True)

            with r2:
                st.markdown(textwrap.dedent(f"""
                <div class="sim-compare-card">
                    <div style="font-size: 0.74rem; font-weight: 700; color: #6B6480;">GOAL PROGRESS</div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #24183B; margin: 0.3rem 0;">
                        {g_change_str}
                    </div>
                    <span class="sim-diff-badge {badge2_cls}">
                        {diff2_text}
                    </span>
                </div>
                """), unsafe_allow_html=True)

            with r3:
                st.markdown(textwrap.dedent(f"""
                <div class="sim-compare-card">
                    <div style="font-size: 0.74rem; font-weight: 700; color: #6B6480;">PREDICTED PROFILE CATEGORY</div>
                    <div style="font-size: 1.3rem; font-weight: 800; color: #24183B; margin: 0.45rem 0;">
                        {r_change_str}
                    </div>
                    <span class="sim-diff-badge badge-primary">
                        Status: {sim_goal_info['feasibility_status']}
                    </span>
                </div>
                """), unsafe_allow_html=True)

            # Wealth Trajectory Projection Chart
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            years = np.linspace(0, sim_horizon, num=max(2, int(np.ceil(sim_horizon)) + 1))
            baseline_trajectory = [u_savings + (u_surplus * 12 * y) for y in years]
            simulated_trajectory = [sim_savings + (sim_surplus * 12 * y) for y in years]

            fig_sim = go.Figure()
            fig_sim.add_trace(go.Scatter(
                x=years, y=baseline_trajectory, mode='lines', name='Current Baseline',
                line=dict(color='#6B6480', width=2.5, dash='dash')
            ))
            fig_sim.add_trace(go.Scatter(
                x=years, y=simulated_trajectory, mode='lines+markers', name='Simulated Trajectory',
                line=dict(color='#6D28D9', width=3.5)
            ))
            fig_sim.add_hline(y=sim_goal, line_dash="dot", line_color="#8B5CF6", annotation_text="Goal Target", annotation_position="top left")

            fig_sim.update_layout(
                title=dict(
                    text=f"Wealth Accumulation Forecast ({sim_horizon_display})",
                    font=dict(size=15, color="#24183B", family="Plus Jakarta Sans"),
                    x=0.03,
                    xanchor="left"
                ),
                xaxis_title="Years ahead",
                yaxis_title="Estimated savings (₹)",
                xaxis=dict(
                    title_font=dict(size=12, color="#24183B"),
                    tickfont=dict(size=10, color="#6B6480"),
                    gridcolor="#DDD0FF",
                    zerolinecolor="#B9A6E5"
                ),
                yaxis=dict(
                    title_font=dict(size=12, color="#24183B"),
                    tickfont=dict(size=10, color="#6B6480"),
                    gridcolor="#DDD0FF",
                    zerolinecolor="#B9A6E5"
                ),
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#F5F0FF",
                height=320,
                margin=dict(l=58, r=18, t=58, b=50),
                font=dict(family="Plus Jakarta Sans", color="#24183B", size=11),
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(family="Plus Jakarta Sans", color="#24183B", size=10),
                    bgcolor="rgba(255,255,255,0.85)"
                ),
                hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#DDD0FF", font=dict(color="#24183B"))
            )
            fig_sim.update_annotations(font=dict(color="#6B6480", size=10))
            st.plotly_chart(fig_sim, use_container_width=True)

    # ==============================================================================
    # 10. ANALYTICS PAGE
    # ==============================================================================
    elif nav_selection == "Analytics":
        st.title("Explore the Financial Dataset")
        st.markdown("""
        <div class="analytics-page-heading" style="margin-bottom: 1.2rem;">
            <p style="font-size: 0.88rem; color: #6B6480; margin-top: 0.2rem;">
                These charts describe patterns in the available example profiles. They do not predict your personal future.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if df_analytics is not None:
            def style_analytics_figure(fig, pie=False):
                fig.update_layout(
                    paper_bgcolor="#FFFFFF",
                    plot_bgcolor="#F5F0FF",
                    font=dict(family="Plus Jakarta Sans", color="#24183B", size=11),
                    title=dict(
                        font=dict(family="Plus Jakarta Sans", size=14, color="#24183B"),
                        x=0.04,
                        xanchor="left"
                    ),
                    legend=dict(
                        font=dict(family="Plus Jakarta Sans", size=10, color="#24183B"),
                        bgcolor="rgba(255,255,255,0.9)",
                        bordercolor="#DDD0FF",
                        borderwidth=0
                    ),
                    hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#DDD0FF", font=dict(color="#24183B")),
                    margin=dict(l=42, r=24, t=48, b=42),
                    uniformtext=dict(minsize=9, mode="show") if pie else None
                )
                axis_style = dict(
                    title_font=dict(family="Plus Jakarta Sans", size=11, color="#24183B"),
                    tickfont=dict(family="Plus Jakarta Sans", size=10, color="#6B6480"),
                    gridcolor="#DDD0FF",
                    zerolinecolor="#B9A6E5",
                    showgrid=True,
                    automargin=True
                )
                fig.update_xaxes(**axis_style)
                fig.update_yaxes(**axis_style)
                if pie:
                    fig.update_traces(
                        textinfo="label+percent",
                        textposition="inside",
                        insidetextfont=dict(family="Plus Jakarta Sans", size=10, color="#FFFFFF"),
                        marker=dict(line=dict(color="#FFFFFF", width=1))
                    )

            st.caption(f"Dataset shown: {len(df_analytics):,} profiles. A relationship between two measures does not prove that one causes the other.")
            c1, c2 = st.columns(2, gap="medium")

            with c1:
                # Financial Health Distribution
                h_col = 'calculated_financial_health_score' if 'calculated_financial_health_score' in df_analytics.columns else 'financial_health_score'
                fig_h = px.histogram(
                    df_analytics, x=h_col, nbins=25,
                    title="How financial health scores are spread",
                    color_discrete_sequence=['#6D28D9'],
                    labels={h_col: "Financial health score"}
                )
                fig_h.update_layout(
                    height=280, margin=dict(l=10, r=10, t=35, b=10),
                    paper_bgcolor="#FFFFFF", plot_bgcolor="#F5F0FF",
                    font=dict(color="#24183B", family="Plus Jakarta Sans")
                )
                style_analytics_figure(fig_h)
                st.plotly_chart(fig_h, use_container_width=True)
                st.caption("Each bar counts profiles within a score range. This shows how common each score range is in the dataset.")

            with c2:
                # Risk Category Distribution
                fig_r = px.pie(
                    df_analytics, names='risk_category',
                    title="Profiles in each predicted category",
                    color='risk_category',
                    labels={'risk_category': 'Profile category'},
                    color_discrete_map={'Low': '#8B5CF6', 'Moderate': '#6D28D9', 'High': '#A78BFA'}
                )
                fig_r.update_layout(
                    height=280, margin=dict(l=10, r=10, t=35, b=10),
                    paper_bgcolor="#FFFFFF",
                    font=dict(color="#24183B", family="Plus Jakarta Sans")
                )
                style_analytics_figure(fig_r, pie=True)
                st.plotly_chart(fig_r, use_container_width=True)
                st.caption("The slices show the share of dataset profiles labeled Low, Moderate, or High risk.")

            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

            c3, c4 = st.columns(2, gap="medium")
            with c3:
                # Savings Rate vs Health Score
                sav_col = 'savings_rate_calculated' if 'savings_rate_calculated' in df_analytics.columns else 'savings_rate_percent'
                fig_s = px.scatter(
                    df_analytics, x=sav_col, y=h_col, color='risk_category',
                    color_discrete_map={'Low': '#8B5CF6', 'Moderate': '#6D28D9', 'High': '#A78BFA'},
                    title="Monthly savings compared with health score",
                    labels={sav_col: "Share of income saved (%)", h_col: "Financial health score", 'risk_category': 'Profile category'}
                )
                fig_s.update_layout(
                    height=280, margin=dict(l=10, r=10, t=35, b=10),
                    paper_bgcolor="#FFFFFF", plot_bgcolor="#F5F0FF",
                    font=dict(color="#24183B", family="Plus Jakarta Sans")
                )
                style_analytics_figure(fig_s)
                st.plotly_chart(fig_s, use_container_width=True)
                st.caption("Each dot is one profile. The chart shows whether higher savings shares tend to appear alongside higher scores in this dataset; it does not establish cause and effect.")

            with c4:
                # Debt to Income vs Health Score
                dti_col = 'debt_to_income_calculated' if 'debt_to_income_calculated' in df_analytics.columns else 'debt_to_income_percent'
                fig_d = px.scatter(
                    df_analytics, x=dti_col, y=h_col, color='risk_category',
                    color_discrete_map={'Low': '#8B5CF6', 'Moderate': '#6D28D9', 'High': '#A78BFA'},
                    title="Debt compared with yearly income and health score",
                    labels={dti_col: "Debt as a share of yearly income (%)", h_col: "Financial health score", 'risk_category': 'Profile category'}
                )
                fig_d.update_layout(
                    height=280, margin=dict(l=10, r=10, t=35, b=10),
                    paper_bgcolor="#FFFFFF", plot_bgcolor="#F5F0FF",
                    font=dict(color="#24183B", family="Plus Jakarta Sans")
                )
                style_analytics_figure(fig_d)
                st.plotly_chart(fig_d, use_container_width=True)
                st.caption("Each dot is one profile. This compares debt as a share of yearly income with its health score; it is a dataset pattern, not a forecast for you.")
        else:
            st.info("Dataset loading in progress.")

    # ==============================================================================
    # 11. AI INSIGHTS PAGE
    # ==============================================================================
    elif nav_selection == "AI Insights":
        st.title("Your Financial Insights")
        st.caption("These observations come from the income, expenses, savings, debt, and goal details in your profile. They are educational prompts, not personal investment advice.")

        strengths = []
        if u_savings_rate >= 25:
            strengths.append(f"You entered monthly savings of ₹{u_surplus:,.0f}, equal to {u_savings_rate:.1f}% of income.")
        if metrics['ef_months'] >= 4:
            strengths.append(f"Your current savings could cover about {metrics['ef_months']:.1f} months of expenses at today's spending level.")
        if u_savings >= u_goal and u_goal > 0:
            strengths.append(f"Your current savings of ₹{u_savings:,.0f} meet or exceed your ₹{u_goal:,.0f} goal.")
        if not strengths:
            strengths.append("No strength threshold is met in the measures shown yet. The figures below show where to start reviewing.")

        watchouts = []
        if u_expense > u_income:
            watchouts.append(f"Monthly expenses exceed income by ₹{u_expense - u_income:,.0f}.")
        if metrics['dti_pct'] > 25:
            watchouts.append(f"Debt is {metrics['dti_pct']:.1f}% of yearly income. Review the repayments and rates that apply to your debt.")
        if metrics['ef_months'] < 6:
            watchouts.append(f"Current savings cover about {metrics['ef_months']:.1f} months of expenses; the dashboard's six-month score target is not yet met.")
        if goal_info['goal_remaining'] > 0 and goal_info['monthly_saving_gap'] > 0:
            watchouts.append(f"At the current monthly saving amount, the goal is short by about ₹{goal_info['monthly_saving_gap']:,.0f} per month for the selected date.")
        if not watchouts:
            watchouts.append("None of the attention checks on this page were triggered by the current profile. This does not guarantee future financial security.")

        next_steps = []
        if goal_info['monthly_saving_gap'] > 0 and u_horizon_months == 0:
            next_steps.append(f"Choose a later goal date or review whether you can set aside the remaining ₹{goal_info['goal_remaining']:,.0f}; no time remains in the current plan.")
        elif goal_info['monthly_saving_gap'] > 0:
            next_steps.append(f"To meet the goal in {horizon_display}, the simple estimate calls for about ₹{goal_info['required_monthly_saving']:,.0f} per month, around ₹{goal_info['monthly_saving_gap']:,.0f} more than your monthly savings entry.")
        if metrics['ef_months'] < 6:
            emergency_target = max(0.0, (6 * u_expense) - u_savings)
            next_steps.append(f"Review an emergency-savings target. Six months of current expenses would be about ₹{6 * u_expense:,.0f}; the difference from current savings is about ₹{emergency_target:,.0f}.")
        if u_debt > 0:
            next_steps.append(f"Review your debt balances, interest rates, and required payments alongside your entered monthly savings of ₹{u_surplus:,.0f}.")
        if not next_steps:
            next_steps.append("Review your profile inputs and goal date periodically so these estimates continue to reflect your situation.")

        review_items = [
            f"Monthly income: ₹{u_income:,.0f}; monthly expenses: ₹{u_expense:,.0f}.",
            f"Current savings: ₹{u_savings:,.0f}; emergency coverage at current spending: {metrics['ef_months']:.1f} months.",
            f"Goal: ₹{u_goal:,.0f}; remaining amount: ₹{goal_info['goal_remaining']:,.0f}; time available: {horizon_display}.",
            f"Overall financial health score: {score_val:.1f} out of 100; predicted profile category: {risk_pred_display} (model result).",
        ]

        insight_sections = [
            ("What You Are Doing Well", strengths),
            ("What Needs Attention", watchouts),
            ("Suggested Next Steps", next_steps),
            ("Progress to Review Later", review_items),
        ]
        for section_index in range(0, len(insight_sections), 2):
            insight_columns = st.columns(2, gap="medium")
            for insight_column, (section_title, section_items) in zip(insight_columns, insight_sections[section_index:section_index + 2]):
                with insight_column:
                    st.subheader(section_title)
                    for item in section_items:
                        st.markdown(f"- {item}")

        st.info("Goal-saving estimates divide the amount remaining by the months available and assume no investment growth, interest, fees, or changes in contributions.")

    # ==============================================================================
    # 12. FINANCIAL HEALTH DEEP DIVE PAGE
    # ==============================================================================
    elif nav_selection == "Financial Health":
        st.title("How Healthy Are Your Finances?")
        st.markdown(textwrap.dedent("""
        <div style="margin-bottom: 1.2rem;">
            <p style="font-size: 0.88rem; color: #6B6480; margin-top: 0.2rem;">
                Your overall score combines six parts of your profile. Each part is scored from 0 to 100; higher means stronger by this dashboard's rules.
            </p>
        </div>
        """), unsafe_allow_html=True)

        st.metric("Overall financial health", f"{score_val:.1f}%", cat_val)
        st.caption("The category is based on the displayed score: Good (80+), Moderate (60–79.9), Needs Improvement (40–59.9), or Poor (below 40). This percentage is a dashboard-generated educational score, not an actual percentage of money saved or a credit rating.")

        health_descriptions = {
            "Savings Rate": ("Monthly savings", f"You save {metrics['savings_rate_pct']:.1f}% of monthly income. The score reaches its maximum at 50% savings."),
            "Debt Burden": ("Debt compared with yearly income", f"Your debt is {metrics['dti_pct']:.1f}% of one year's income. A lower share receives a stronger score."),
            "Emergency Fund": ("Emergency savings", f"Your current savings cover about {metrics['ef_months']:.1f} months of expenses. The score reaches its maximum at six months."),
            "Expense Ratio": ("Monthly spending", f"Your expenses use {metrics['expense_ratio_pct']:.1f}% of monthly income. Lower spending relative to income scores higher."),
            "Monthly Surplus": ("Monthly savings amount", f"You entered {format_inr(metrics['monthly_surplus'])} as the amount saved each month; the score compares it with your income. The overview shows income minus expenses separately."),
            "Goal Progress": ("Progress toward your goal", f"You have saved {metrics['goal_progress_pct']:.1f}% of the goal amount."),
        }

        comp_list = [
            ("Savings Rate", components['Savings Rate'], "25%", "#6D28D9"),
            ("Debt Burden", components['Debt Burden'], "20%", "#8B5CF6"),
            ("Emergency Fund", components['Emergency Fund'], "20%", "#8B5CF6"),
            ("Expense Ratio", components['Expense Ratio'], "15%", "#D97706"),
            ("Monthly Surplus", components['Monthly Surplus'], "10%", "#6D28D9"),
            ("Goal Progress", components['Goal Progress'], "10%", "#DC2626")
        ]

        r1 = st.columns(3, gap="medium")
        for idx in range(3):
            name, score, weight, color = comp_list[idx]
            simple_name, explanation = health_descriptions[name]
            status = "Strong" if score >= 80 else ("On track" if score >= 60 else ("Needs attention" if score >= 40 else "Low"))
            with r1[idx]:
                st.markdown(textwrap.dedent(f"""
                <div class="fin-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-size: 0.82rem; font-weight: 800; color: #24183B;">{simple_name}</span>
                        <span class="kpi-badge badge-primary">Share {weight}</span>
                    </div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #24183B;">{score:.0f}%</div>
                    <div class="dim-track" style="margin: 0.6rem 0;"><div class="dim-fill" style="width: {score}%; background: {color};"></div></div>
                    <div style="font-size: 0.78rem; font-weight: 700; color: #8B5CF6;">{status}</div>
                    <div style="font-size: 0.82rem; color: #6B6480; line-height: 1.45; margin-top: 0.45rem;">{explanation}</div>
                </div>
                """), unsafe_allow_html=True)

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        r2 = st.columns(3, gap="medium")
        for idx in range(3, 6):
            name, score, weight, color = comp_list[idx]
            simple_name, explanation = health_descriptions[name]
            status = "Strong" if score >= 80 else ("On track" if score >= 60 else ("Needs attention" if score >= 40 else "Low"))
            with r2[idx - 3]:
                st.markdown(textwrap.dedent(f"""
                <div class="fin-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-size: 0.82rem; font-weight: 800; color: #24183B;">{simple_name}</span>
                        <span class="kpi-badge badge-primary">Share {weight}</span>
                    </div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #24183B;">{score:.0f}%</div>
                    <div class="dim-track" style="margin: 0.6rem 0;"><div class="dim-fill" style="width: {score}%; background: {color};"></div></div>
                    <div style="font-size: 0.78rem; font-weight: 700; color: #8B5CF6;">{status}</div>
                    <div style="font-size: 0.82rem; color: #6B6480; line-height: 1.45; margin-top: 0.45rem;">{explanation}</div>
                </div>
                """), unsafe_allow_html=True)

    # ==============================================================================
    # 13. FINANCIAL GOALS DEEP DIVE PAGE
    # ==============================================================================
    elif nav_selection == "Financial Goals":
        st.title("Plan Your Savings Goal")
        st.markdown(textwrap.dedent("""
        <div style="margin-bottom: 1.2rem;">
            <p style="font-size: 0.88rem; color: #6B6480; margin-top: 0.2rem;">
                See what you have saved, what remains, and the monthly amount needed to reach your target by your chosen date.
            </p>
        </div>
        """), unsafe_allow_html=True)

        st.markdown(textwrap.dedent(f"""
        <div class="fin-card" style="margin-bottom: 1.2rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                <span style="font-size: 0.84rem; font-weight: 800; text-transform: uppercase; color: #24183B;">Goal progress</span>
                <span class="kpi-badge badge-success">● {goal_info['feasibility_status']}</span>
            </div>
            <div style="font-size: 1.75rem; font-weight: 800; color: #24183B; margin-bottom: 0.4rem;">
                {metrics['goal_progress_pct']:.1f}% saved
            </div>
            <div class="dim-track" style="height: 10px; margin-bottom: 0.6rem;">
                <div class="dim-fill" style="width: {metrics['goal_progress_pct']}%; background: #8B5CF6;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #6B6480; font-weight: 600;">
                <span>Saved: ₹{u_savings:,.0f}</span>
                <span>Goal: ₹{u_goal:,.0f}</span>
            </div>
        </div>
        """), unsafe_allow_html=True)
        st.caption(f"Time available: {horizon_display}")

        g1, g2, g3 = st.columns(3, gap="medium")
        with g1:
            st.markdown(textwrap.dedent(f"""
            <div class="fin-card">
                <div class="kpi-label">Amount still needed</div>
                <div class="kpi-value-lg" style="color: #6D28D9; margin-top: 4px;">₹{goal_info['goal_remaining']:,.0f}</div>
            </div>
            """), unsafe_allow_html=True)
        with g2:
            st.markdown(textwrap.dedent(f"""
            <div class="fin-card">
                <div class="kpi-label">Save each month to stay on time</div>
                <div class="kpi-value-lg" style="margin-top: 4px;">{required_monthly_display}</div>
            </div>
            """), unsafe_allow_html=True)
        with g3:
            st.markdown(textwrap.dedent(f"""
            <div class="fin-card">
                <div class="kpi-label">Extra monthly saving needed</div>
                <div class="kpi-value-lg" style="color: {'#8B5CF6' if goal_info['monthly_saving_gap'] == 0 else '#DC2626'}; margin-top: 4px;">
                    ₹{goal_info['monthly_saving_gap']:,.0f}
                </div>
            </div>
            """), unsafe_allow_html=True)

        st.info(
            "Estimate assumes no investment growth, interest, fees, or changes in your monthly savings. "
            "The monthly amount is the amount still needed divided by the number of months left. "
            "If no time remains, extend the goal date; the app does not divide by zero."
        )

    elif nav_selection == "AI Chatbot":
        st.markdown("""
        <div class="ai-chat-page-heading" style="margin-bottom:1rem;">
            <h1 style="font-size:1.75rem;font-weight:800;color:#24183B;margin:0;">AI Chatbot</h1>
            <p style="font-size:0.88rem;color:#6B6480;margin-top:0.25rem;">Ask about the figures already in your WealthSphere profile.</p>
        </div>
        """, unsafe_allow_html=True)
        st.info("Rule-based assistant. No conversational AI model or external API is connected; the existing risk prediction model is separate. Answers use simple calculations from this session's profile. Chat history stays in session memory and is not sent to a third-party AI service.")

        chat_profile = {
            "income": u_income,
            "expense": u_expense,
            "monthly_savings": u_surplus,
            "current_savings": u_savings,
            "debt": u_debt,
            "goal_amount": u_goal,
            "horizon_months": u_horizon_months,
            "horizon_display": horizon_display,
            "risk_tolerance": st.session_state.profile_risk_pref,
            "metrics": metrics,
            "goal_info": goal_info,
            "score": score_val,
            "category": cat_val,
            "components": components,
            "predicted_risk": risk_pred_display,
        }

        if not st.session_state.chat_history:
            with st.chat_message("assistant"):
                st.write("Hello. I can explain your health score, savings, expenses, debt indicator, risk tolerance, or goal timeline using the numbers in your current profile.")
        else:
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

        with st.form("financial_chat_form", clear_on_submit=True):
            chat_question = st.text_input("Your question", placeholder="For example: How much should I save monthly to reach my goal?")
            send_chat_question = st.form_submit_button("Send", type="primary")

        def submit_chat_question(question):
            question = question.strip()
            if question:
                st.session_state.chat_history.extend([
                    {"role": "user", "content": question},
                    {"role": "assistant", "content": build_rule_based_financial_answer(question, chat_profile)},
                ])
                st.rerun()

        if send_chat_question:
            submit_chat_question(chat_question)

        st.markdown("#### Suggested questions")
        suggested_questions = [
            "How is my financial health score calculated?",
            "How much should I save monthly to meet my goal?",
            "What share of my income goes to expenses?",
            "What does my debt indicator mean?",
            "What does my risk tolerance mean?",
            "How many months of expenses do my savings cover?",
        ]
        suggestion_columns = st.columns(2, gap="small")
        for question_index, suggested_question in enumerate(suggested_questions):
            with suggestion_columns[question_index % 2]:
                if st.button(suggested_question, key=f"chat_suggestion_{question_index}", use_container_width=True):
                    submit_chat_question(suggested_question)

    elif nav_selection == "Financial Products":
        st.markdown("""
        <div style="margin-bottom:1rem;">
            <h1 style="font-size:1.75rem;font-weight:800;color:#24183B;margin:0;">Financial Products</h1>
            <p style="font-size:0.88rem;color:#6B6480;margin-top:0.25rem;">Educational product categories to research, compared with your current profile.</p>
        </div>
        """, unsafe_allow_html=True)
        st.warning("Educational information only, not personalized financial, tax, or investment advice. Product terms and availability vary. No live rates, returns, or offers are shown, and WealthSphere will never purchase or apply for a product for you.")

        product_profile = {
            "income": u_income,
            "expense": u_expense,
            "monthly_savings": u_surplus,
            "current_savings": u_savings,
            "debt": u_debt,
            "goal_amount": u_goal,
            "horizon_months": u_horizon_months,
            "horizon_display": horizon_display,
            "risk_tolerance": st.session_state.profile_risk_pref,
            "metrics": metrics,
        }
        st.markdown(
            f"<div class='fin-card' style='margin-bottom:1rem;'><strong style='color:#24183B;'>Profile context</strong><br>"
            f"Monthly income: {format_inr(u_income)} · Expenses: {format_inr(u_expense)} · Monthly savings entered: {format_inr(u_surplus)} · "
            f"Current savings: {format_inr(u_savings)} · Debt: {format_inr(u_debt)}<br>"
            f"Goal: {format_inr(u_goal)} · Horizon: {horizon_display} · Risk tolerance: {st.session_state.profile_risk_pref}</div>",
            unsafe_allow_html=True
        )

        product_cards = build_financial_product_guidance(product_profile)
        for row_start in range(0, len(product_cards), 2):
            product_columns = st.columns(2, gap="medium")
            for product_column, product in zip(product_columns, product_cards[row_start:row_start + 2]):
                with product_column:
                    st.markdown(textwrap.dedent(f"""
                    <div class="fin-card" style="height:100%;">
                        <h3 style="font-size:1.05rem;font-weight:800;color:#24183B;margin:0 0 0.65rem;">{product['name']}</h3>
                        <p style="font-size:0.82rem;color:#6B6480;line-height:1.45;margin:0 0 0.8rem;"><strong style="color:#24183B;">Purpose:</strong> {product['purpose']}</p>
                        <div style="font-size:0.78rem;color:#24183B;line-height:1.5;">
                            <p><strong>Potential benefits:</strong> {product['benefits']}</p>
                            <p><strong>Risks:</strong> {product['risks']}</p>
                            <p><strong>Liquidity:</strong> {product['liquidity']}</p>
                            <p><strong>Time horizon:</strong> {product['time_horizon']}</p>
                            <p><strong>Considerations:</strong> {product['considerations']}</p>
                        </div>
                        <div style="background:#F3EBFF;border:1px solid #DDD0FF;border-radius:8px;padding:0.75rem;margin-top:0.8rem;font-size:0.8rem;color:#24183B;line-height:1.45;">
                            <strong>Why it may or may not match:</strong> {product['profile_match']}
                        </div>
                    </div>
                    """), unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------------------------
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #DDD0FF; padding-top: 1.5rem; margin-top: 2rem; font-size: 0.75rem; color: #6B6480;">
        <span>WealthSphere AI Financial Intelligence • Educational Simulation Engine</span>
        <span>Version 2.0 • Competition Edition</span>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
