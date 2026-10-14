import os
import urllib.parse
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pydeck as pdk
import streamlit.components.v1 as components

# ---------------------------------------------------------
# Configuración general de la página
# ---------------------------------------------------------
st.set_page_config(
    page_title="Cuenca Golfo San Jorge - Transición Energética",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para diseño responsivo y optimización de espacio vertical en 1080p
st.markdown("""
<style>
    /* 0. Fijación obligatoria de Modo Oscuro permanente */
    .stApp, [data-testid="stAppViewContainer"], body {
        background-color: #0e1117 !important;
        color: #f8fafc !important;
    }
    section[data-testid="stSidebar"], [data-testid="stSidebarContent"] {
        background-color: #111827 !important;
    }

    /* 1. Ocultar el gatito de GitHub, botón Fork/Deploy y menú de tres puntos (manteniendo la barra de herramientas activa) */
    #MainMenu, 
    [data-testid="stMainMenu"],
    [data-testid="stAppDeployButton"], 
    .stAppDeployButton,
    [data-testid="stHeaderActionElements"],
    [data-testid="stToolbarActions"],
    div[class*="e1yxiy6j6"],
    [data-testid="stToolbar"] a,
    [data-testid="stToolbar"] button:not([data-testid="stExpandSidebarButton"]) {
        display: none !important;
    }

    /* Header y toolbar transparentes que no bloquean clics en la app */
    header[data-testid="stHeader"] {
        background: transparent !important;
        pointer-events: none !important;
        z-index: 99999 !important;
    }
    [data-testid="stToolbar"] {
        background: transparent !important;
        pointer-events: none !important;
    }

    /* 2. Botón para colapsar filtros (cuando la barra lateral está abierta) */
    [data-testid="stSidebarCollapseButton"] {
        display: inline-flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        color: #38bdf8 !important;
    }
    [data-testid="stSidebarCollapseButton"] svg {
        fill: #38bdf8 !important;
        stroke: #38bdf8 !important;
    }

    /* 3. Botón para expandir y traer de vuelta los filtros (cuando la barra lateral está oculta) */
    [data-testid="stExpandSidebarButton"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {
        display: inline-flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        position: fixed !important;
        top: 0.65rem !important;
        left: 0.65rem !important;
        z-index: 9999999 !important;
        background-color: #0f172a !important;
        border: 1.5px solid #38bdf8 !important;
        border-radius: 8px !important;
        color: #38bdf8 !important;
        width: 2.3rem !important;
        height: 2.3rem !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.6) !important;
        transition: all 0.2s ease-in-out !important;
    }
    [data-testid="stExpandSidebarButton"]:hover,
    [data-testid="stSidebarCollapsedControl"]:hover,
    [data-testid="collapsedControl"]:hover {
        background-color: #1e293b !important;
        border-color: #7dd3fc !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.6) !important;
        transform: scale(1.05) !important;
    }
    [data-testid="stExpandSidebarButton"] svg,
    [data-testid="stExpandSidebarButton"] span,
    [data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="collapsedControl"] svg {
        fill: #38bdf8 !important;
        stroke: #38bdf8 !important;
        color: #38bdf8 !important;
        visibility: visible !important;
        display: inline-block !important;
    }

    /* 3. Ocultar el pie de página de Streamlit */
    footer {
        display: none !important;
    }

    /* 4. Ocultar la insignia flotante inferior derecha (el avatar de usuario y la coronita de Streamlit) */
    div[class*="viewerBadge"],
    div[class*="Profile"],
    div[class*="manage-app"],
    div[class*="floating-buttons"],
    .viewerBadge_container__r5tak,
    [data-testid="stDecoration"] {
        display: none !important;
    }
    .block-container {
        max-width: 98% !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        padding-top: 3.2rem !important;
        padding-bottom: 1rem !important;
    }
    [data-testid="stSidebarContent"] {
        padding-top: 1.2rem !important;
    }
    [data-testid="stSidebarHeader"] {
        height: auto !important;
        min-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    [data-testid="stSidebarUserContent"] {
        padding-top: 0 !important;
        padding-bottom: 1rem !important;
    }
    .block-container h1,
    .block-container h1 span,
    .main-header-title {
        font-size: clamp(1.5rem, 1.85vw, 1.95rem) !important;
        font-weight: 700 !important;
        color: #f8fafc !important;
        line-height: 1.15 !important;
        margin: 0 0 0.25rem 0 !important;
        padding: 0 !important;
    }
    [data-testid="stSidebarContent"] h1,
    [data-testid="stSidebarContent"] h1 span,
    [data-testid="stSidebarContent"] h2,
    [data-testid="stSidebarContent"] h2 span,
    [data-testid="stSidebarContent"] h3,
    [data-testid="stSidebarContent"] h3 span {
        text-align: center !important;
    }
    [data-testid="stSidebarContent"] h1,
    [data-testid="stSidebarContent"] h1 span {
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        color: #f8fafc !important;
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    h2, h2 span, h3, h3 span, h4, h4 span, h5, h5 span {
        color: #f8fafc !important;
    }
    h2 span, h3 span, h4 span, h5 span {
        font-size: inherit !important;
    }

    /* 2. Barra lateral espaciada y uniforme */
    [data-testid="stSidebarUserContent"],
    [data-testid="stSidebarUserContent"] > div > div[data-testid="stVerticalBlock"],
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
        display: flex !important;
        flex-direction: column !important;
        gap: 0.45rem !important;
    }
    [data-testid="stSidebarUserContent"] .stSelectbox,
    [data-testid="stSidebarUserContent"] .stSlider,
    [data-testid="stSidebarUserContent"] .stButton {
        margin-bottom: 0.95rem !important;
    }
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
        margin-bottom: 0.3rem !important;
    }
    .sidebar-section-title,
    [data-testid="stSidebar"] .sidebar-section-title {
        margin-top: 1.1rem !important;
        margin-bottom: 0.6rem !important;
    }
    .sidebar-footer,
    .sidebar-footer div {
        white-space: nowrap !important;
        font-size: 13px !important;
        text-align: center !important;
        color: #cbd5e1 !important;
        line-height: 1.4 !important;
    }

    /* 3. Textos descriptivos con margen inferior reducido */
    .main-subtitle {
        font-size: 15px !important;
        line-height: 1.4 !important;
        color: #cbd5e1 !important;
        margin-bottom: 0.25rem !important;
    }
    [data-testid="stTooltipContent"],
    [data-testid="stTooltipContent"] p,
    [data-testid="stTooltipContent"] span,
    [data-testid="stTooltipContent"] div,
    div[data-baseweb="tooltip"] {
        font-size: 14.5px !important;
        line-height: 1.4 !important;
    }
    p, span, .stCaption, [data-testid="stCaptionContainer"] p {
        font-size: 14.5px !important;
        color: #cbd5e1 !important;
    }
    .stTabs [data-baseweb="tab"] p {
        font-size: 15.5px !important;
        font-weight: 600 !important;
    }
    .streamlit-expanderHeader p {
        font-size: 15px !important;
        font-weight: 600 !important;
    }
    code, .stMarkdown code {
        color: #34d399 !important;
        background-color: rgba(16, 185, 129, 0.12) !important;
        border: 1px solid rgba(16, 185, 129, 0.35) !important;
        padding: 0.12rem 0.38rem !important;
        border-radius: 4px !important;
        font-size: 0.88em !important;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
    }

    /* 4. Tarjetas de KPIs Cyber-Dark con Fondos Tintados y Bordes Temáticos */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 0.65rem;
        width: 100%;
        margin-bottom: 0.45rem;
    }
    .kpi-container {
        border-radius: 10px !important;
        padding: 0.55rem 0.75rem !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        height: 100%;
        min-width: 0;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        gap: 6px !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .kpi-container:hover {
        transform: translateY(-2px);
    }
    .kpi-card-petroleo {
        background: linear-gradient(135deg, rgba(40, 48, 65, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
        border: 1.5px solid #475569 !important;
    }
    .kpi-card-agua {
        background: linear-gradient(135deg, rgba(14, 116, 144, 0.35) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
        border: 1.5px solid #0284c7 !important;
        box-shadow: 0 4px 14px -2px rgba(2, 132, 199, 0.28) !important;
    }
    .kpi-card-demanda {
        background: linear-gradient(135deg, rgba(194, 65, 12, 0.35) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
        border: 1.5px solid #ea580c !important;
        box-shadow: 0 4px 14px -2px rgba(234, 88, 12, 0.28) !important;
    }
    .kpi-card-eolica {
        background: linear-gradient(135deg, rgba(13, 148, 136, 0.35) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
        border: 1.5px solid #0d9488 !important;
        box-shadow: 0 4px 14px -2px rgba(13, 148, 136, 0.28) !important;
    }
    .kpi-card-co2 {
        background: linear-gradient(135deg, rgba(22, 163, 74, 0.30) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
        border: 1.5px solid #16a34a !important;
        box-shadow: 0 4px 14px -2px rgba(22, 163, 74, 0.28) !important;
    }
    .kpi-content-left {
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-width: 0;
        flex: 1;
    }
    .kpi-title, .kpi-label {
        font-size: clamp(0.70rem, 0.76vw, 0.82rem) !important;
        font-weight: 600;
        color: #94a3b8 !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 2px;
        white-space: normal !important;
        line-height: 1.2;
    }
    .kpi-value {
        font-size: clamp(1rem, 1.35vw, 1.6rem) !important;
        white-space: nowrap !important;
        font-weight: 700;
        color: #f8fafc !important;
        line-height: 1.15;
        margin: 0.12rem 0 !important;
    }
    .kpi-value span {
        font-size: clamp(0.70rem, 0.85vw, 0.90rem) !important;
        font-weight: 400;
        color: #94a3b8 !important;
        white-space: nowrap !important;
    }
    .kpi-subtext, .kpi-subtext span, .kpi-subtext b {
        font-size: clamp(0.68rem, 0.74vw, 0.80rem) !important;
        color: #cbd5e1 !important;
        margin-top: 1px;
        line-height: 1.25;
    }
    .kpi-subtext b {
        color: #f8fafc !important;
    }
    .kpi-icon-right {
        width: clamp(1.4rem, 1.8vw, 2.2rem) !important;
        height: clamp(1.4rem, 1.8vw, 2.2rem) !important;
        flex-shrink: 0 !important;
        font-size: clamp(1.4rem, 1.8vw, 2.2rem) !important;
        line-height: 1 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        user-select: none !important;
        margin: 0 !important;
    }
    .kpi-icon-right svg {
        width: 100% !important;
        height: 100% !important;
        max-width: clamp(1.4rem, 1.8vw, 2.2rem) !important;
        max-height: clamp(1.4rem, 1.8vw, 2.2rem) !important;
        flex-shrink: 0 !important;
    }
    .kpi-badge {
        display: inline-block;
        padding: 1px 7px;
        border-radius: 9999px;
        font-size: clamp(0.68rem, 0.74vw, 0.80rem) !important;
        font-weight: 700;
    }
    .badge-green { background-color: rgba(22, 163, 74, 0.25) !important; color: #4ade80 !important; border: 1px solid #16a34a !important; }
    .badge-blue { background-color: rgba(2, 132, 199, 0.25) !important; color: #38bdf8 !important; border: 1px solid #0284c7 !important; }
    .badge-amber { background-color: rgba(180, 83, 9, 0.25) !important; color: #fbbf24 !important; border: 1px solid #b45309 !important; }
    .badge-red { background-color: rgba(185, 28, 28, 0.25) !important; color: #f87171 !important; border: 1px solid #b91c1c !important; }
    .trace-op { color: #38bdf8 !important; font-weight: 600; }
    .trace-pe { color: #34d399 !important; font-weight: 700; }

    /* 5. Franja de Balance Económico (Fondos Tintados y Bordes a Juego) */
    .econ-bar {
        display: grid;
        grid-template-columns: repeat(6, minmax(0, 1fr));
        gap: 0.5rem;
        margin-top: 4px;
        margin-bottom: 0.45rem;
        width: 100%;
    }
    .econ-item {
        border-radius: 8px;
        padding: 0.35rem 0.6rem !important;
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-width: 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.35);
        transition: transform 0.15s ease;
    }
    .econ-item:hover {
        transform: translateY(-1px);
    }
    .econ-item-demanda { 
        background-color: rgba(30, 41, 59, 0.7) !important;
        border: 1px solid #475569 !important; 
    }
    .econ-item-gas { 
        background-color: rgba(194, 65, 12, 0.2) !important;
        border: 1px solid #c2410c !important; 
    }
    .econ-item-valor-gas { 
        background-color: rgba(180, 83, 9, 0.2) !important;
        border: 1px solid #d97706 !important; 
    }
    .econ-item-costo { 
        background-color: rgba(109, 40, 217, 0.2) !important;
        border: 1px solid #7c3aed !important; 
    }
    .econ-item-creditos { 
        background-color: rgba(8, 145, 178, 0.2) !important;
        border: 1px solid #06b6d4 !important; 
    }
    .econ-item-beneficio { 
        background-color: rgba(21, 128, 61, 0.25) !important;
        border: 1px solid #22c55e !important; 
        box-shadow: 0 0 10px rgba(34, 197, 94, 0.25) !important;
    }
    .econ-label {
        font-size: 0.82rem !important;
        font-weight: 600;
        color: #94a3b8 !important;
        margin-bottom: 2px;
        line-height: 1.15;
        white-space: normal !important;
    }
    .econ-val {
        font-size: 0.82rem !important;
        font-weight: 700;
        color: #f8fafc !important;
        white-space: nowrap;
        line-height: 1.15;
    }

    /* 6. Banner de Contexto Territorial y Diagnóstico Cyber-Dark */
    .unified-context-box {
        background-color: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-left: 4px solid #38bdf8 !important;
        border-radius: 8px;
        padding: 0.5rem 0.95rem !important;
        margin-top: 4px;
        margin-bottom: 0.55rem;
        font-size: clamp(0.80rem, 0.88vw, 0.92rem) !important;
        color: #f8fafc !important;
        line-height: 1.45;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    .unified-context-box b {
        color: #f8fafc !important;
    }

    /* 7. Altura del mapa 3D para ganar visibilidad sin scroll */
    .stPydeckChart, div[data-testid="stDeckGlJsonChart"] {
        height: 540px !important;
        min-height: 540px !important;
    }

    /* 8. Sliders corporativos FAZE en color cian (#38bdf8) */
    div[data-testid="stSlider"] [role="slider"] {
        background-color: #38bdf8 !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.6) !important;
    }
    div[data-testid="stSlider"] [role="slider"]:focus,
    div[data-testid="stSlider"] [role="slider"]:hover {
        box-shadow: 0 0 14px rgba(56, 189, 248, 0.9) !important;
        transform: scale(1.1);
    }
    div[data-testid="stSlider"] [data-baseweb="slider"] > div > div:first-child,
    div[data-testid="stSlider"] [data-baseweb="slider"] div[style*="rgb(255, 75, 75)"],
    div[data-testid="stSlider"] [data-baseweb="slider"] div[style*="background-color: rgb(255, 75, 75)"],
    div[data-testid="stSlider"] [data-baseweb="slider"] div[style*="#ff4b4b"],
    div[data-testid="stSlider"] [data-baseweb="slider"] div[style*="background: rgb(255, 75, 75)"] {
        background-color: #38bdf8 !important;
        background: #38bdf8 !important;
    }
    div[data-testid="stSlider"] [data-testid="stTickBarMin"],
    div[data-testid="stSlider"] [data-testid="stTickBarMax"] {
        color: #94a3b8 !important;
    }
    div[data-testid="stSlider"] [data-baseweb="slider"] div[aria-hidden="true"] {
        color: #38bdf8 !important;
    }

    /* 9. Media Queries para pantallas medianas (Notebooks <= 1400px) */
    @media (max-width: 1400px) {
        .stMetric label, .kpi-label, .kpi-title { font-size: 0.74rem !important; }
        .kpi-value { font-size: clamp(1rem, 1.35vw, 1.6rem) !important; white-space: nowrap !important; }
        .kpi-subtext, .kpi-subtext span, .kpi-subtext b { font-size: 0.70rem !important; }
        .kpi-icon-right {
            width: clamp(1.4rem, 1.8vw, 2.2rem) !important;
            height: clamp(1.4rem, 1.8vw, 2.2rem) !important;
            font-size: clamp(1.4rem, 1.8vw, 2.2rem) !important;
        }
        .econ-bar { grid-template-columns: repeat(3, minmax(0, 1fr)); }
        section[data-testid="stSidebar"],
        [data-testid="stSidebarContent"] { width: 300px !important; min-width: 300px !important; }
        .stPydeckChart, div[data-testid="stDeckGlJsonChart"] { height: 480px !important; min-height: 480px !important; }
    }

    /* 9.1. Media Query Responsive para Celulares y Pantallas Móviles (<= 768px) */
    @media (max-width: 768px) {
        /* Permitir que los contenedores flexibles hagan salto de línea en celular */
        div[data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
        }
        
        /* Si las tarjetas están en columnas de Streamlit o divs con clase específica */
        div[data-testid="column"] {
            min-width: 100% !important;
            margin-bottom: 0.5rem !important;
        }

        /* En caso de que uses un contenedor CSS Grid personalizado para las tarjetas */
        .kpi-grid, .econ-bar, .kpi-container, .metric-grid, .cards-container {
            grid-template-columns: 1fr !important;
            display: flex !important;
            flex-direction: column !important;
        }

        .kpi-container {
            margin-bottom: 0.5rem !important;
            padding: 0.75rem 1rem !important;
        }
        .econ-item {
            margin-bottom: 0.35rem !important;
            padding: 0.5rem 0.75rem !important;
        }
    }

    /* 10. Orientación y contención del Tooltip nativo de Pydeck */
    .deck-tooltip {
        max-height: 380px !important;
        overflow-y: auto !important;
        z-index: 99999 !important;
        pointer-events: none !important;
        transition: opacity 0.08s ease-out;
    }
    .deck-tooltip > div {
        max-height: 380px !important;
        overflow-y: auto !important;
    }
    div[data-testid="stDeckGlJsonChart"],
    .stPydeckChart {
        overflow: visible !important;
    }
    iframe[data-testid="stCustomComponentV1"] {
        position: absolute !important;
        width: 0 !important;
        height: 0 !important;
        border: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Ícono Vectorial Eólico y Funciones Auxiliares
# ---------------------------------------------------------
ICON_TURBINA_SVG = (
    '<svg style="vertical-align: -2.5px; display: inline-block; margin-right: 4px;" '
    'width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2.2" '
    'stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M12 12v9"/>'
    '<path d="m14 12 5-8.5a1 1 0 0 0-1.7-1L12 7"/>'
    '<path d="M12 12 3.5 14a1 1 0 0 0-1 1.7L7 18"/>'
    '<path d="M12 12l3 7.5a1 1 0 0 0 1.9.4L18 15"/>'
    '<circle cx="12" cy="12" r="2" fill="#38bdf8"/>'
    '</svg>'
)

def fmt_num(valor, decimales=0):
    """Formatea números al estándar Español/Argentina: punto (.) para miles y coma (,) para decimales."""
    if valor is None or pd.isna(valor):
        return "0" if decimales == 0 else "0," + ("0" * decimales)
    formato = f"{float(valor):,.{decimales}f}"
    return formato.replace(",", "X").replace(".", ",").replace("X", ".")


def haversine_km(lat1, lon1, lat2, lon2):
    """Calcula la distancia geodésica en kilómetros entre dos coordenadas (fórmula de Haversine)."""
    R = 6371.0  # Radio medio terrestre en km
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2.0) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda / 2.0) ** 2
    c = 2.0 * np.arctan2(np.sqrt(a), np.sqrt(1.0 - a))
    return float(R * c)


# ---------------------------------------------------------
# Coordenadas y operadores de referencia para Parques Eólicos CGSJ
# ---------------------------------------------------------
COORDS_PARQUES = {
    'MANAEO': (-45.72, -67.75, 'YPF Luz', 'PE Manantiales Behr'),
    'DIADEO': (-45.78, -67.65, 'Hychico (CAPSA)', 'PE Diadema'),
    'DIA2EO': (-45.78, -67.65, 'Hychico (CAPSA)', 'PE Diadema II'),
    'TORDEO': (-45.88, -67.90, 'Tecpetrol', 'PE El Tordillo'),
    'KOSTEO': (-45.75, -67.55, 'Kosten S.A.', 'PE Kosten'),
    'MAL1EO': (-45.05, -66.85, 'Total Eren', 'PE Malaspina I'),
    'GARAEO': (-44.75, -66.65, 'Pan American Energy', 'PE Garayalde'),
    'BICEEO': (-46.75, -68.30, 'PCR', 'PE Bicentenario'),
    'BIC2EO': (-46.75, -68.30, 'PCR', 'PE Bicentenario II'),
    'LEONEO': (-46.55, -67.85, 'YPF Luz', 'PE Cañadón León (RenovAr)'),
    'LEO1EO': (-46.55, -67.85, 'YPF Luz', 'PE Cañadón León (MATER)'),
    'LHEREO': (-46.50, -68.90, 'Total Eren', 'PE Hércules')
}

# ---------------------------------------------------------
# 1. Carga de datos con @st.cache_data
# ---------------------------------------------------------
@st.cache_data
def cargar_datos():
    archivo_excel = "Base_Datos_CGSJ_Transicion_Energetica_CORREGIDO.xlsx"
    with pd.ExcelFile(archivo_excel, engine="openpyxl") as xl:
        df_yac = xl.parse("Yacimientos")
        df_pe = xl.parse("Parque_Eolico")
        df_params = xl.parse("Parametros")
        
    # Asegurar formato datetime en las fechas
    df_yac["fecha"] = pd.to_datetime(df_yac["fecha"])
    df_pe["fecha"] = pd.to_datetime(df_pe["fecha"])
    
    # Normalización de texto y provincias en mayúsculas
    df_yac["provincia_norm"] = df_yac["provincia"].astype(str).str.strip().str.upper()
    df_pe["provincia_norm"] = df_pe["provincia"].astype(str).str.strip().str.upper()
    df_yac["yacimiento"] = df_yac["yacimiento"].astype(str).str.strip()
    df_yac["operador"] = df_yac["operador"].astype(str).str.strip()
    
    return df_yac, df_pe, df_params

try:
    df_yac_raw, df_pe_raw, df_params = cargar_datos()
except Exception as e:
    st.error(f"Error al cargar la base de datos: {e}")
    st.stop()

# Parámetros por defecto de la hoja 'Parametros'
params_map = dict(zip(df_params['parametro'], df_params['valor']))
def_consumo = float(params_map.get('consumo_esp_bes', 7.5))
def_precio_gas = float(params_map.get('precio_gas_boca_pozo', params_map.get('precio_gas_boca_poz', 3.5)))
def_lcoe = float(params_map.get('lcoe_eolico', 42.0))
def_factor_emision = float(params_map.get('factor_emision_red', 0.42))

# Mapeo unívoco de cada yacimiento a su provincia predominante
mapa_yac_a_provincia = (
    df_yac_raw.groupby(['yacimiento', 'provincia_norm'])['prod_liquido_m3']
    .sum()
    .reset_index()
    .sort_values(['yacimiento', 'prod_liquido_m3'], ascending=[True, False])
    .drop_duplicates('yacimiento')
    .set_index('yacimiento')['provincia_norm']
    .to_dict()
)

# ---------------------------------------------------------
# 2. Barra Lateral (Sidebar con espaciado uniforme y limpio)
# ---------------------------------------------------------
st.sidebar.markdown("""
<div style="text-align: center; margin-top: 0.2rem; margin-bottom: 1rem;">
    <span style="font-size: 1.8rem; font-weight: 800; letter-spacing: 3px; color: #38bdf8;">FAZE</span>
</div>
<div class="sidebar-section-title" style="text-align: center; font-size: 1.15rem; font-weight: 600; color: #f8fafc; margin-bottom: 0.6rem;">
    📍 Filtro Geográfico y Bloque
</div>
""", unsafe_allow_html=True)

# Callbacks para sincronización automática bidireccional Provincia <-> Yacimiento
if 'filtro_provincia' not in st.session_state:
    st.session_state['filtro_provincia'] = 'Todas'
if 'filtro_yacimiento' not in st.session_state:
    st.session_state['filtro_yacimiento'] = 'Todos los Yacimientos'

def _on_yacimiento_change():
    yac = st.session_state.get('filtro_yacimiento', 'Todos los Yacimientos')
    if yac != 'Todos los Yacimientos':
        prov_asoc = mapa_yac_a_provincia.get(yac)
        if prov_asoc in ['CHUBUT', 'SANTA CRUZ']:
            st.session_state['filtro_provincia'] = prov_asoc

def _on_provincia_change():
    prov = st.session_state.get('filtro_provincia', 'Todas')
    curr_yac = st.session_state.get('filtro_yacimiento', 'Todos los Yacimientos')
    if curr_yac != 'Todos los Yacimientos' and prov != 'Todas':
        prov_actual = mapa_yac_a_provincia.get(curr_yac)
        if prov_actual != prov:
            st.session_state['filtro_yacimiento'] = 'Todos los Yacimientos'

provincia_sel = st.sidebar.selectbox(
    "Provincia",
    options=['Todas', 'CHUBUT', 'SANTA CRUZ'],
    key='filtro_provincia',
    on_change=_on_provincia_change
)

# Lista de yacimientos disponibles según provincia seleccionada
if provincia_sel != 'Todas':
    yacimientos_disp = sorted(df_yac_raw[df_yac_raw['provincia_norm'] == provincia_sel]['yacimiento'].dropna().unique().tolist())
else:
    yacimientos_disp = sorted(df_yac_raw['yacimiento'].dropna().unique().tolist())

opciones_yacimientos = ["Todos los Yacimientos"] + yacimientos_disp

if st.session_state.get('filtro_yacimiento') not in opciones_yacimientos:
    st.session_state['filtro_yacimiento'] = 'Todos los Yacimientos'

yacimiento_sel_unico = st.sidebar.selectbox(
    "Yacimiento",
    options=opciones_yacimientos,
    key='filtro_yacimiento',
    on_change=_on_yacimiento_change,
    help="Seleccioná un yacimiento para analizar su serie histórica consolidada (2019-2026) sin fragmentar por cambios de operador y evaluar parques eólicos dentro del radio de cercanía."
)
yacimientos_sel = [] if yacimiento_sel_unico == "Todos los Yacimientos" else [yacimiento_sel_unico]

# Control de Radio de Cobertura Eólica
radio_cobertura_km = st.sidebar.slider(
    "Radio de Cobertura Eólica (km)",
    min_value=10,
    max_value=120,
    value=40,
    step=5,
    help="Distancia máxima geodésica (Haversine) desde el yacimiento seleccionado para vincular parques eólicos cercanos."
)

# Filtro Temporal Mensual
meses_disponibles = pd.date_range(start='2019-01-01', end='2026-08-01', freq='MS').strftime('%Y-%m').tolist()
rango_meses = st.sidebar.select_slider(
    "📅 Período Mensual (2019 - 2026)",
    options=meses_disponibles,
    value=(meses_disponibles[0], meses_disponibles[-1])
)
fecha_min = pd.to_datetime(rango_meses[0] + "-01")
fecha_max = pd.to_datetime(rango_meses[1] + "-01")

# Parámetros Dinámicos con inicialización y botón de restablecimiento en st.session_state
VALORES_DEFECTO_PARAMS = {
    "param_consumo": 1.2,
    "param_precio_gas": 3.50,
    "param_lcoe": 42.0,
    "param_factor_emision": 0.42,
    "param_precio_bono": 5.0,
}
for k_param, v_def in VALORES_DEFECTO_PARAMS.items():
    if k_param not in st.session_state:
        st.session_state[k_param] = v_def

def restablecer_parametros():
    for k_param, v_def in VALORES_DEFECTO_PARAMS.items():
        st.session_state[k_param] = v_def

st.sidebar.markdown("""
<div class="sidebar-section-title" style="text-align: center; font-size: 1.15rem; font-weight: 600; color: #f8fafc; margin-top: 1.1rem; margin-bottom: 0.6rem;">
    ⚙️ Parámetros Dinámicos
</div>
""", unsafe_allow_html=True)
st.sidebar.button(
    "🔄 Restablecer Valores por Defecto",
    on_click=restablecer_parametros,
    use_container_width=True
)

consumo_esp_extraccion = st.sidebar.slider(
    "Consumo Específico de Extracción (kWh/m³ liq)",
    min_value=0.5,
    max_value=12.0,
    step=0.1,
    format="%.1f",
    key="param_consumo",
    help="Consumo eléctrico promedio requerido para levantamiento artificial e inyección por cada m³ de fluido producido."
)

precio_gas_boca_pozo = st.sidebar.slider(
    "Precio Gas Boca de Pozo (USD/MMBtu)",
    min_value=0.5,
    max_value=10.0,
    step=0.1,
    format="%.2f",
    key="param_precio_gas",
    help="Precio de costo de oportunidad del gas natural desplazado."
)

lcoe_eolico = st.sidebar.slider(
    "LCOE Eólico Regional (USD/MWh)",
    min_value=30.0,
    max_value=65.0,
    step=0.5,
    format="%.1f",
    key="param_lcoe",
    help="Costo nivelado promedio de generación eólica en la cuenca."
)

factor_emision_red = st.sidebar.slider(
    "Factor Emisión de Red (tCO₂/MWh)",
    min_value=0.1,
    max_value=0.7,
    step=0.01,
    format="%.2f",
    key="param_factor_emision",
    help="Factor de emisión de generación térmica desplazada."
)

precio_bono_co2 = st.sidebar.slider(
    "Precio Bono de Carbono (USD/tCO₂)",
    min_value=0.0,
    max_value=30.0,
    step=0.5,
    format="%.1f",
    key="param_precio_bono",
    help="Valor del crédito o bono de carbono por tonelada de CO₂ evitada."
)

with st.sidebar.expander("📐 Memoria de Cálculo y Ecuaciones", expanded=False):
    st.markdown("""
* **Demanda Eléctrica:**  
  `E [MWh] = Líquido [m³] × Consumo Específico [kWh/m³] ÷ 1.000`
* **Vínculo Geodésico:**  
  Distancia pozo-parque mediante fórmula de Haversine (`R = 6.371 km`)
* **Gas Evitado:**  
  `Gas [MMBtu] = Demanda Cubierta [MWh] × 9,5 MMBtu/MWh` *(Heat Rate motogeneración)*
* **Emisiones:**  
  `CO₂ [t] = Demanda Cubierta [MWh] × Factor de Emisión Red [tCO₂/MWh]`
* **Beneficio Neto:**  
  `Valor Gas Liberado + Ingreso Bonos CO₂ - Costo LCOE`
    """)

st.sidebar.markdown("""
<div class="sidebar-footer" style="white-space: nowrap; font-size: 13px; text-align: center; margin-top: 8px;">
    <div>Cuenca Golfo San Jorge — Transición Energética</div>
    <div>Fuentes: Secretaría de Energía / CAMMESA</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Filtrado de Datos y Lógica de Proximidad (Haversine)
# ---------------------------------------------------------
# 1. Filtro temporal
df_yac = df_yac_raw[(df_yac_raw['fecha'] >= fecha_min) & (df_yac_raw['fecha'] <= fecha_max)].copy()
df_pe_periodo = df_pe_raw[(df_pe_raw['fecha'] >= fecha_min) & (df_pe_raw['fecha'] <= fecha_max)].copy()

# 2. Filtro provincia para yacimientos
if provincia_sel != 'Todas':
    df_yac = df_yac[df_yac['provincia_norm'] == provincia_sel]

# 3. Filtro por Yacimiento seleccionado (consolidando operadores en toda la serie)
if yacimientos_sel:
    df_yac = df_yac[df_yac['yacimiento'].isin(yacimientos_sel)]

# Cantidad de meses en el período para cálculo de potencia media (MW)
n_meses_periodo = max(1, (fecha_max.year - fecha_min.year) * 12 + (fecha_max.month - fecha_min.month) + 1)
horas_periodo = n_meses_periodo * 730.0

# 4. Determinación de Parques Eólicos Activos según Proximidad Geográfica (Haversine)
parques_cercanos_info = {}  # {central_nemo: (dist_min_km, yac_referencia)}

if yacimientos_sel and not df_yac.empty:
    # Obtener coordenadas únicas de los yacimientos seleccionados
    coords_yac_sel = df_yac[['yacimiento', 'latitud', 'longitud']].drop_duplicates()
    for nemo, (p_lat, p_lon, p_op, p_nom) in COORDS_PARQUES.items():
        dist_min = float('inf')
        yac_ref = ""
        for _, r_yac in coords_yac_sel.iterrows():
            d = haversine_km(r_yac['latitud'], r_yac['longitud'], p_lat, p_lon)
            if d < dist_min:
                dist_min = d
                yac_ref = r_yac['yacimiento']
        if dist_min <= radio_cobertura_km:
            parques_cercanos_info[nemo] = (dist_min, yac_ref)
            
    # Filtrar generación eólica ÚNICAMENTE a los parques dentro del radio de cercanía
    df_pe = df_pe_periodo[df_pe_periodo['central_nemo'].isin(list(parques_cercanos_info.keys()))].copy()
else:
    # Sin filtro de yacimiento ("Todos"): total regional según provincia seleccionada
    if provincia_sel != 'Todas':
        df_pe = df_pe_periodo[df_pe_periodo['provincia_norm'] == provincia_sel].copy()
    else:
        df_pe = df_pe_periodo.copy()

# ---------------------------------------------------------
# Encabezado Principal y Panel de Trazabilidad Histórica
# ---------------------------------------------------------
st.title("⚡ Cuenca Golfo San Jorge: Transición Energética")

if not yacimientos_sel:
    alcance_txt = "Todos los yacimientos (Escala Regional)"
    jurisdiccion_txt = provincia_sel
else:
    alcance_txt = yacimientos_sel[0]
    jurisdiccion_txt = mapa_yac_a_provincia.get(yacimientos_sel[0], provincia_sel)

st.markdown(f"""
<div class="main-subtitle">
    Simulador geoespacial para evaluar la demanda eléctrica de yacimientos maduros y su descarbonización con energía eólica regional.<br/>
    <b>Período activo:</b> <code>{rango_meses[0]}</code> a <code>{rango_meses[1]}</code> ({n_meses_periodo} meses) &nbsp;|&nbsp;
    <b>Jurisdicción:</b> <code>{jurisdiccion_txt}</code> &nbsp;|&nbsp;
    <b>Yacimiento:</b> <code>{alcance_txt}</code>
</div>
""", unsafe_allow_html=True)

with st.expander("📘 Guía Rápida: ¿Cómo operar este simulador y qué representa cada métrica?"):
    st.markdown("""
    ### 🎯 1. Propósito del Simulador
    La Cuenca del Golfo San Jorge (CGSJ) es una cuenca petrolera madura donde para extraer 1 m³ de petróleo es necesario bombear entre 15 y 25 m³ de agua (el 93% a 96% del fluido extraído es agua). Levantar ese volumen desde 1.500–2.200 m de profundidad demanda una enorme cantidad de energía eléctrica. 

    Esta plataforma cruza los datos oficiales de 153 yacimientos (Capítulo IV - Secretaría de Energía) con la generación real de los 12 parques eólicos de la región (CAMMESA) entre 2019 y 2026 para responder cuatro preguntas estratégicas:
    1. **¿Cuánta electricidad demandan los yacimientos** para extraer y bombear semejante volumen de agua?
    2. **¿Qué proporción de esa demanda puede abastecerse** con los parques eólicos dentro del radio territorial operativo?
    3. **¿Cuántas emisiones de CO₂ se neutralizan** al reemplazar la quema de gas en motogeneración térmica?
    4. **¿Cuál es el beneficio económico neto** al liberar gas comercializable al sistema frente al costo LCOE de la energía eólica?

    ---
    ### 📊 2. Significado de las 5 Tarjetas Superiores (KPIs) y Balance Económico
    - **🛢️ Petróleo Producido (m³):** Volumen acumulado de crudo neto extraído (también expresado en millones de metros cúbicos, Mm³).
    - **💧 Agua Bruta / WOR (m³):** Volumen total de agua producida. WOR (*Water-Oil Ratio*) indica cuántos m³ de agua salen por cada 1 m³ de petróleo; BSW (%) es el porcentaje de agua sobre el líquido total extraído.
    - **⚡ Demanda Eléctrica de Extracción (MWh):** Energía eléctrica consumida para elevar el fluido total (`Líquido Total × Consumo Específico ÷ 1.000`), junto con su Potencia Media continua (MW) requerida las 24 h.
    - **🌀 Generación Eólica (MWh) y Cobertura Renovable (%):** Electricidad limpia generada y qué porcentaje de la demanda de extracción logra cubrir (`Generación Eólica ÷ Demanda de Extracción`).
    - **🌱 CO₂ Evitado y Balance Económico Neto:**
      - **CO₂ Evitado (tCO₂):** Toneladas de dióxido de carbono no emitidas al desplazar generación térmica fósil.
      - **Gas Evitado de Quemado (MMBtu):** `Demanda Eólica Cubierta [MWh] × 9,5 [MMBtu/MWh]`.
      - **Valor del Gas Liberado (USD):** `Gas Evitado [MMBtu] × Precio Gas Boca de Pozo [USD/MMBtu]`.
      - **Ingreso Créditos CO₂ (USD):** `CO₂ Evitado [tCO₂] × Precio Bono de Carbono [USD/tCO₂]`.
      - **Costo Eólico Asociado (USD):** `Demanda Eólica Cubierta [MWh] × LCOE Eólico [USD/MWh]`.
      - **Beneficio Neto Estimado (USD):** `Valor Gas Liberado + Ingreso Créditos CO₂ − Costo Eólico`.

    ---
    ### 🗺️ 3. Cómo interpretar el Mapa 3D y la Simulación
    - **Columnas 3D (Yacimientos):** Su altura indica el volumen de líquido total extraído y su color el nivel de criticidad acuífera:
      - 🟠 **Naranja (#f59e0b):** Operación convencional con WOR < 9 (BSW < 90%).
      - 🔵 **Azul Eléctrico (#0ea5e9):** Yacimientos maduros hiper-acuíferos con WOR ≥ 9 (BSW ≥ 90%), principales candidatos para electrificación.
    - **Aerogeneradores y Halos Cian (Parques Eólicos):** Su ubicación muestra las fuentes de generación limpia de la cuenca. Al modificar el deslizador de *Radio de Cobertura Eólica*, el simulador recalcula dinámicamente qué yacimientos quedan bajo el área de influencia renovable y actualiza al instante el balance técnico-económico.
    """)

if df_yac.empty and df_pe.empty:
    st.warning("⚠️ No se encontraron registros para los filtros seleccionados.")
    st.stop()


# ---------------------------------------------------------
# 3. KPIs de Cabecera y Modelo Económico (Formato AR)
# ---------------------------------------------------------
petroleo_acum_m3 = df_yac['prod_petroleo_m3'].sum() if not df_yac.empty else 0.0
agua_acum_m3 = df_yac['prod_agua_m3'].sum() if not df_yac.empty else 0.0
liquido_acum_m3 = df_yac['prod_liquido_m3'].sum() if not df_yac.empty else (petroleo_acum_m3 + agua_acum_m3)
wor_medio_ponderado = (agua_acum_m3 / petroleo_acum_m3) if petroleo_acum_m3 > 0 else 0.0
corte_agua_ponderado = (agua_acum_m3 / liquido_acum_m3 * 100.0) if liquido_acum_m3 > 0 else 0.0

# Demanda Eléctrica de Extracción estimada en MWh: (prod_liquido_m3 * consumo_esp_extraccion) / 1000
demanda_extraccion_mwh = (liquido_acum_m3 * consumo_esp_extraccion) / 1000.0
potencia_media_demanda_mw = demanda_extraccion_mwh / horas_periodo

# Generación Eólica Total en el período (MWh) y Tasa de Cobertura Renovable
gen_eolica_total_mwh = df_pe['generacion_mwh'].sum() if not df_pe.empty else 0.0
potencia_media_eolica_mw = gen_eolica_total_mwh / horas_periodo
tasa_cobertura_pct = (gen_eolica_total_mwh / demanda_extraccion_mwh * 100.0) if demanda_extraccion_mwh > 0 else 0.0

# Emisiones de CO2 evitadas (tCO2)
emisiones_evitadas_tco2 = gen_eolica_total_mwh * factor_emision_red

# Cálculo de Beneficio Económico / Gas Liberado + Créditos de Carbono:
# - Demanda eólica cubierta [MWh]: energía eólica efectivamente aplicada a cubrir la demanda de extracción
demanda_eolica_cubierta_mwh = min(gen_eolica_total_mwh, demanda_extraccion_mwh) if demanda_extraccion_mwh > 0 else gen_eolica_total_mwh
# - Gas evitado de quemado: Demanda eólica cubierta [MWh] * 9.5 [MMBtu/MWh]
HEAT_RATE_MMBTU_MWH = 9.5
gas_evitado_mmbtu = demanda_eolica_cubierta_mwh * HEAT_RATE_MMBTU_MWH
# - Valor del gas liberado: Gas evitado [MMBtu] * precio_gas_boca_pozo [USD/MMBtu]
valor_gas_liberado_usd = gas_evitado_mmbtu * precio_gas_boca_pozo
# - Ingreso por Créditos de CO2: Emisiones evitadas [tCO2] * precio_bono_co2 [USD/tCO2]
ingreso_creditos_co2_usd = emisiones_evitadas_tco2 * precio_bono_co2
# - Costo eólico asociado: Demanda eólica cubierta [MWh] * lcoe_eolico [USD/MWh]
costo_eolico_usd = demanda_eolica_cubierta_mwh * lcoe_eolico
# - Beneficio Neto Estimado [USD] = Valor del gas liberado + Ingreso Créditos CO2 - Costo eólico
beneficio_neto_usd = valor_gas_liberado_usd + ingreso_creditos_co2_usd - costo_eolico_usd

signo_ben = "+" if beneficio_neto_usd >= 0 else "-"
beneficio_neto_fmt = f"{signo_ben} {fmt_num(abs(beneficio_neto_usd), 0)} USD"
badge_ben_class = "badge-green" if beneficio_neto_usd >= 0 else "badge-amber"

# Renderizado de las 5 Tarjetas de Métricas en un Grid Responsivo Fluido (5 columnas elásticas)
if yacimientos_sel and not parques_cercanos_info:
    badge_class = "badge-red"
    sub_cobertura = f'Cobertura Renovable: <span class="kpi-badge {badge_class}">0,0%</span> (Sin parques a &le;{radio_cobertura_km} km)'
else:
    badge_class = "badge-green" if tasa_cobertura_pct >= 80 else ("badge-amber" if tasa_cobertura_pct >= 35 else "badge-blue")
    sub_cobertura = f'Tasa de Cobertura Renovable: <span class="kpi-badge {badge_class}">{fmt_num(tasa_cobertura_pct, 1)}%</span>'

autos_equivalentes = int(emisiones_evitadas_tco2 / 4.6)

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-container kpi-card-petroleo">
        <div class="kpi-content-left">
            <div class="kpi-title kpi-label">Petróleo Producido</div>
            <div class="kpi-value">{fmt_num(petroleo_acum_m3, 0)} <span>m³</span></div>
            <div class="kpi-subtext">Acumulado ({fmt_num(petroleo_acum_m3/1e6, 2)} Mm³)</div>
        </div>
        <div class="kpi-icon-right" style="opacity: 0.8;">🛢️</div>
    </div>
    <div class="kpi-container kpi-card-agua">
        <div class="kpi-content-left">
            <div class="kpi-title kpi-label">Agua Bruta / WOR</div>
            <div class="kpi-value">{fmt_num(agua_acum_m3, 0)} <span>m³</span></div>
            <div class="kpi-subtext">WOR: <b>{fmt_num(wor_medio_ponderado, 2)}</b> | BSW: <b>{fmt_num(corte_agua_ponderado, 1)}%</b></div>
        </div>
        <div class="kpi-icon-right" style="opacity: 0.85; filter: drop-shadow(0 0 8px rgba(2, 132, 199, 0.45));">💧</div>
    </div>
    <div class="kpi-container kpi-card-demanda">
        <div class="kpi-content-left">
            <div class="kpi-title kpi-label">Demanda de Extracción</div>
            <div class="kpi-value">{fmt_num(demanda_extraccion_mwh, 0)} <span>MWh</span></div>
            <div class="kpi-subtext">Pot. media: <b>{fmt_num(potencia_media_demanda_mw, 1)} MW</b> ({fmt_num(consumo_esp_extraccion, 1)} kWh/m³)</div>
        </div>
        <div class="kpi-icon-right" style="opacity: 0.9;">⚡</div>
    </div>
    <div class="kpi-container kpi-card-eolica">
        <div class="kpi-content-left">
            <div class="kpi-title kpi-label">Generación Eólica</div>
            <div class="kpi-value">{fmt_num(gen_eolica_total_mwh, 0)} <span>MWh</span></div>
            <div class="kpi-subtext">{sub_cobertura}</div>
        </div>
        <div class="kpi-icon-right" style="opacity: 0.9;">
            <svg viewBox="0 0 24 24" fill="none" stroke="#2dd4bf" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 12v9"/>
                <path d="m14 12 5-8.5a1 1 0 0 0-1.7-1L12 7"/>
                <path d="M12 12 3.5 14a1 1 0 0 0-1 1.7L7 18"/>
                <path d="M12 12l3 7.5a1 1 0 0 0 1.9.4L18 15"/>
                <circle cx="12" cy="12" r="2" fill="#2dd4bf"/>
            </svg>
        </div>
    </div>
    <div class="kpi-container kpi-card-co2">
        <div class="kpi-content-left">
            <div class="kpi-title kpi-label">CO₂ Evitado / Beneficio</div>
            <div class="kpi-value">{fmt_num(emisiones_evitadas_tco2, 0)} <span>tCO₂</span></div>
            <div class="kpi-subtext">
                Beneficio: <span class="kpi-badge {badge_ben_class}">{beneficio_neto_fmt}</span><br/>
                <span>🚗 ~<b>{fmt_num(autos_equivalentes, 0)}</b> autos evitados/año.</span>
            </div>
        </div>
        <div class="kpi-icon-right" style="opacity: 0.9;">🌱</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Franja de Balance Económico en 6 micro-tarjetas con contorno neón estilizado
st.markdown(f"""
<div class="econ-bar">
    <div class="econ-item econ-item-demanda">
        <div class="econ-label">⚡ Demanda Cubierta</div>
        <div class="econ-val">{fmt_num(demanda_eolica_cubierta_mwh, 0)} MWh</div>
    </div>
    <div class="econ-item econ-item-gas">
        <div class="econ-label">🔥 Gas Evitado</div>
        <div class="econ-val" style="color:#fb923c !important;">{fmt_num(gas_evitado_mmbtu, 0)} MMBtu</div>
    </div>
    <div class="econ-item econ-item-valor-gas">
        <div class="econ-label">💵 Valor Gas Liberado</div>
        <div class="econ-val" style="color:#4ade80 !important;">+ {fmt_num(valor_gas_liberado_usd, 0)} USD</div>
    </div>
    <div class="econ-item econ-item-costo">
        <div class="econ-label">📉 Costo Eólico LCOE</div>
        <div class="econ-val" style="color:#c084fc !important;">- {fmt_num(costo_eolico_usd, 0)} USD</div>
    </div>
    <div class="econ-item econ-item-creditos">
        <div class="econ-label">🌐 Ingreso Créditos CO₂</div>
        <div class="econ-val" style="color:#38bdf8 !important;">+ {fmt_num(ingreso_creditos_co2_usd, 0)} USD</div>
    </div>
    <div class="econ-item econ-item-beneficio">
        <div class="econ-label" style="color:#86efac !important;">💰 Beneficio Neto Estimado</div>
        <div class="econ-val" style="color:#4ade80 !important;"><span class="kpi-badge {badge_ben_class}">{beneficio_neto_fmt}</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Recuadro unificado de contexto, cercanía eólica y diagnóstico (2 líneas compactas)
if len(yacimientos_sel) == 1 and not df_yac.empty:
    y_nom = yacimientos_sel[0]
    sub_y = df_yac[df_yac['yacimiento'] == y_nom]
    ops_detalle = []
    for op_nom, grp_op in sub_y.groupby('operador'):
        a_min = grp_op['fecha'].dt.year.min()
        a_max = grp_op['fecha'].dt.year.max()
        rango_str = f"{a_min}" if a_min == a_max else f"{a_min}-{a_max}"
        ops_detalle.append(
            f"<span class='trace-op'>{op_nom}</span> <span style='color:#cbd5e1;'>({rango_str})</span>"
        )
    ops_str = " / ".join(ops_detalle) if ops_detalle else "N/A"

    if parques_cercanos_info:
        parques_str = ", ".join([
            f"<span class='trace-pe'>{COORDS_PARQUES[k][3]}</span> <span style='color:#cbd5e1;'>({fmt_num(v[0], 1)} km)</span>"
            for k, v in sorted(parques_cercanos_info.items(), key=lambda x: x[1][0])
        ])
    else:
        parques_str = f"<span style='color:#fbbf24;'>Sin parques a &le;{radio_cobertura_km} km</span>"

    linea_1 = (
        f"📍 <b>{y_nom}</b> &nbsp;|&nbsp; 🏢 <b>Operadores:</b> {ops_str} &nbsp;|&nbsp; "
        f"🌀 <b>Parques en radio ({len(parques_cercanos_info)}):</b> {parques_str}"
    )
    linea_2 = (
        f"💡 <b>Diagnóstico de Bloque:</b> Demanda <b>{fmt_num(potencia_media_demanda_mw, 2)} MW</b> continuos "
        f"(<b>{fmt_num(corte_agua_ponderado, 1)}%</b> agua bruta / WOR <b>{fmt_num(wor_medio_ponderado, 2)}</b>). "
        f"Cobertura eólica: <b>{fmt_num(tasa_cobertura_pct, 1)}%</b> &nbsp;|&nbsp; "
        f"Potencial liberación: <b>{fmt_num(gas_evitado_mmbtu, 0)} MMBtu</b> de gas ({beneficio_neto_fmt})."
    )
else:
    n_parques_activos = df_pe['central_nemo'].nunique() if not df_pe.empty else 12
    linea_1 = (
        f"🌐 <b>Cuenca Golfo San Jorge</b> &nbsp;|&nbsp; "
        f"🌀 <b>{n_parques_activos} Parques eólicos activos</b> &nbsp;|&nbsp; "
        f"📡 <b>Radio operativo regional:</b> {radio_cobertura_km} km"
    )
    linea_2 = (
        f"💡 <b>Diagnóstico Regional:</b> Demanda <b>{fmt_num(potencia_media_demanda_mw, 1)} MW</b> continuos "
        f"(<b>{fmt_num(corte_agua_ponderado, 1)}%</b> agua bruta / WOR <b>{fmt_num(wor_medio_ponderado, 2)}</b>). "
        f"Cobertura eólica: <b>{fmt_num(tasa_cobertura_pct, 1)}%</b> &nbsp;|&nbsp; "
        f"Potencial liberación: <b>{fmt_num(gas_evitado_mmbtu, 0)} MMBtu</b> de gas ({beneficio_neto_fmt})."
    )

st.markdown(f"""
<div class="unified-context-box">
    <div>{linea_1}</div>
    <div style="margin-top: 3px;">{linea_2}</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Preprocesamiento consolidado para Mapa y Tablas de Detalle
# ---------------------------------------------------------
gen_por_nemo = df_pe_periodo.groupby('central_nemo')['generacion_mwh'].sum().to_dict() if not df_pe_periodo.empty else {}

if not df_yac.empty:
    yac_map = df_yac.groupby(
        ['yacimiento', 'provincia', 'latitud', 'longitud'], 
        as_index=False
    ).agg(
        prod_petroleo_m3=('prod_petroleo_m3', 'sum'),
        prod_agua_m3=('prod_agua_m3', 'sum'),
        prod_liquido_m3=('prod_liquido_m3', 'sum'),
        operador=('operador', lambda s: " / ".join(sorted(s.dropna().unique())))
    )
    yac_map = yac_map[(yac_map['latitud'].notna()) & (yac_map['longitud'].notna()) & (yac_map['latitud'] != 0)].copy()
    yac_map['wor'] = (yac_map['prod_agua_m3'] / yac_map['prod_petroleo_m3'].replace(0, float('nan'))).round(2).fillna(0.0)
    yac_map['bsw_pct'] = ((yac_map['prod_agua_m3'] / yac_map['prod_liquido_m3'].replace(0, float('nan'))) * 100.0).round(1).fillna(0.0)
    
    # Escala de elevación proporcionada (entre 400m y 12.000m para no desproporcionar frente a parques)
    max_liq = yac_map['prod_liquido_m3'].max() if len(yac_map) > 0 and yac_map['prod_liquido_m3'].max() > 0 else 1.0
    yac_map['elevacion'] = (yac_map['prod_liquido_m3'] / max_liq) * 11500.0 + 400.0
    
    # Asignación de color según WOR y severidad de corte de agua
    def calcular_color_yac(row):
        # WOR moderado (<90% de agua / WOR < 9): Ámbar/naranja [245, 158, 11, 230]
        # WOR severo (>=90% de agua / WOR >= 9): Azul eléctrico [14, 165, 233, 230]
        if row['bsw_pct'] >= 90.0 or row['wor'] >= 9.0:
            return [14, 165, 233, 230]
        else:
            return [245, 158, 11, 230]

    yac_map['color'] = yac_map.apply(calcular_color_yac, axis=1)
    yac_map['tipo'] = '🛢️ Yacimiento Hidrocarburífero'
    yac_map['tipo_objeto'] = 'yacimiento'
    yac_map['nombre'] = yac_map['yacimiento']
    yac_map['nombre_yacimiento'] = yac_map['yacimiento']
    yac_map['nombre_parque'] = ''
    yac_map['header_badge'] = '🛢️ Yacimiento Hidrocarburífero'
    yac_map['titulo_nombre'] = yac_map['yacimiento']
    yac_map['subtitulo_meta'] = "Operador: " + yac_map['operador'].astype(str) + " (" + yac_map['provincia'].astype(str) + ")"
    
    # Calcular parque eólico más cercano y balance energético local para cada yacimiento
    info_1_list, info_2_list, info_3_list, info_4_list = [], [], [], []
    m1_list, m2_list, m3_list, m4_list = [], [], [], []
    for _, r_y in yac_map.iterrows():
        y_lat, y_lon = r_y['latitud'], r_y['longitud']
        demanda_y_mwh = (r_y['prod_liquido_m3'] * consumo_esp_extraccion) / 1000.0
        demanda_y_mw = demanda_y_mwh / horas_periodo
        
        # Buscar parque más cercano y sumar generación eólica dentro del radio_cobertura_km
        min_d = float('inf')
        min_p_nom = "N/A"
        gen_local_mwh = 0.0
        n_parques_radio = 0
        for nemo, (p_lat, p_lon, p_op, p_nom) in COORDS_PARQUES.items():
            d = haversine_km(y_lat, y_lon, p_lat, p_lon)
            if d < min_d:
                min_d = d
                min_p_nom = p_nom
            if d <= radio_cobertura_km:
                gen_local_mwh += gen_por_nemo.get(nemo, 0.0)
                n_parques_radio += 1
                
        oferta_local_mw = gen_local_mwh / horas_periodo
        cob_local_pct = (gen_local_mwh / demanda_y_mwh * 100.0) if demanda_y_mwh > 0 else 0.0
        
        info_1_list.append(
            f"Líquido: {fmt_num(r_y['prod_liquido_m3'], 0)} m³ (Petróleo: {fmt_num(r_y['prod_petroleo_m3'], 0)} m³ | Agua: {fmt_num(r_y['prod_agua_m3'], 0)} m³)"
        )
        info_2_list.append(
            f"Corte de Agua (BSW): {fmt_num(r_y['bsw_pct'], 1)}% | WOR: {fmt_num(r_y['wor'], 2)}"
        )
        info_3_list.append(
            f"Parque más cercano: {min_p_nom} a {fmt_num(min_d, 1)} km ({n_parques_radio} parque(s) a ≤{radio_cobertura_km} km)"
        )
        info_4_list.append(
            f"Balance Local ({radio_cobertura_km} km): Demanda {fmt_num(demanda_y_mw, 2)} MW vs. Oferta Eólica {fmt_num(oferta_local_mw, 2)} MW (Cob: {fmt_num(cob_local_pct, 1)}%)"
        )
        
        # Métricas limpias para tooltip sin etiquetas crudas
        m1_list.append(f"{fmt_num(r_y['prod_petroleo_m3'], 0)} m³")
        m2_list.append(f"{fmt_num(r_y['prod_agua_m3'], 0)} m³ (Líq: {fmt_num(r_y['prod_liquido_m3'], 0)} m³)")
        m3_list.append(f"{fmt_num(r_y['bsw_pct'], 1)}% (WOR: {fmt_num(r_y['wor'], 2)})")
        if min_p_nom != "N/A":
            m4_list.append(f"{min_p_nom} a {fmt_num(min_d, 1)} km ({n_parques_radio} en radio)")
        else:
            m4_list.append("Sin parques en radio")
        
    yac_map['info_1'] = info_1_list
    yac_map['info_2'] = info_2_list
    yac_map['info_3'] = info_3_list
    yac_map['info_4'] = info_4_list
    
    yac_map['metrica_1_label'] = "Petróleo Producido:"
    yac_map['metrica_1_val'] = m1_list
    yac_map['metrica_2_label'] = "Agua Bruta (Líquido):"
    yac_map['metrica_2_val'] = m2_list
    yac_map['metrica_3_label'] = "Corte de Agua (BSW / WOR):"
    yac_map['metrica_3_val'] = m3_list
    yac_map['metrica_4_label'] = f"Parque Eólico Cercano (≤{radio_cobertura_km} km):"
    yac_map['metrica_4_val'] = m4_list
else:
    yac_map = pd.DataFrame()

# ---------------------------------------------------------
# 4 y 5. Pestañas Principales: Mapa 3D vs. Análisis Temporal
# ---------------------------------------------------------
tab_mapa, tab_graficos = st.tabs(["🗺️ Mapa Geoespacial 3D", "📈 Análisis Temporal y Detalle"])

with tab_mapa:

    # Preparar datos de Parques Eólicos para el mapa (mostrando activos y contexto regional)
    df_pe_mapa_base = df_pe_periodo.copy()
    if provincia_sel != 'Todas' and not yacimientos_sel:
        df_pe_mapa_base = df_pe_mapa_base[df_pe_mapa_base['provincia_norm'] == provincia_sel]

    if not df_pe_mapa_base.empty:
        pe_map = df_pe_mapa_base.groupby(['parque', 'central_nemo', 'provincia'], as_index=False).agg({
            'generacion_mwh': 'sum'
        })
        pe_map['latitud'] = pe_map['central_nemo'].map(lambda c: COORDS_PARQUES[c][0] if c in COORDS_PARQUES else -45.80)
        pe_map['longitud'] = pe_map['central_nemo'].map(lambda c: COORDS_PARQUES[c][1] if c in COORDS_PARQUES else -67.50)
        pe_map['operador'] = pe_map['central_nemo'].map(lambda c: COORDS_PARQUES[c][2] if c in COORDS_PARQUES else 'Generador Eólico')
        
        max_gen = pe_map['generacion_mwh'].max() if len(pe_map) > 0 and pe_map['generacion_mwh'].max() > 0 else 1.0
        
        # Diferenciación de parques activos (en radio) vs fuera de radio
        pe_map['en_radio'] = pe_map['central_nemo'].apply(
            lambda c: True if not yacimientos_sel else (c in parques_cercanos_info)
        )
        
        # Radio de cobertura definido por el slider dinámico (en metros)
        pe_map['radio_metros'] = float(radio_cobertura_km * 1000.0)
        
        pe_map['color_base'] = pe_map['en_radio'].apply(
            lambda act: [45, 212, 191, 230] if act else [100, 116, 139, 140]
        )
        pe_map['color_halo_fill'] = pe_map['en_radio'].apply(
            lambda act: [30, 41, 59, 30] if act else [15, 23, 42, 15]
        )
        pe_map['color_halo_line'] = pe_map['en_radio'].apply(
            lambda act: [56, 189, 248, 200] if act else [148, 163, 184, 90]
        )
        
        # Offset visual de coordenadas para que el molino no quede solapado con columnas de yacimientos
        pe_map["lon_display"] = pe_map["longitud"] + 0.018  # Desplaza ligeramente al este
        pe_map["lat_display"] = pe_map["latitud"] + 0.008   # Desplaza ligeramente al norte
        
        # Descriptor de ícono para IconLayer (Aerogenerador vertical con mástil cónico y aspas aerodinámicas en SVG Data-URI)
        svg_turbine = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 220" width="140" height="220">
  <!-- Mástil / Torre con base cónica ancha y visible -->
  <polygon points="66,80 74,80 77,215 63,215" fill="#38bdf8" opacity="0.95"/>
  
  <!-- Buje central / Rotor -->
  <circle cx="70" cy="80" r="8" fill="#ffffff"/>
  <circle cx="70" cy="80" r="10" stroke="#38bdf8" stroke-width="2" fill="none"/>

  <!-- Aspa superior vertical (ancha y con forma aerodinámica) -->
  <path d="M70,72 Q64,35 68,8 Q70,4 72,8 Q76,35 70,72 Z" fill="#38bdf8"/>
  
  <!-- Aspa inferior izquierda -->
  <path d="M63,84 Q32,102 8,118 Q4,120 7,116 Q36,92 63,84 Z" fill="#38bdf8"/>
  
  <!-- Aspa inferior derecha -->
  <path d="M77,84 Q108,102 132,118 Q136,120 133,116 Q104,92 77,84 Z" fill="#38bdf8"/>
</svg>"""

        ICON_TURBINA = {
            "url": f"data:image/svg+xml;utf8,{urllib.parse.quote(svg_turbine)}",
            "width": 140,
            "height": 220,
            "anchorY": 215,  # Base inferior de la torre apoyada sobre el pedestal
            "anchorX": 70,   # Centro del mástil
            "mask": False
        }
        pe_map["icon_data"] = [ICON_TURBINA] * len(pe_map)
        
        pe_map['tipo'] = '💨 Parque Eólico'
        pe_map['tipo_objeto'] = 'molino'
        pe_map['nombre'] = pe_map['parque']
        pe_map['nombre_parque'] = pe_map['parque']
        pe_map['nombre_yacimiento'] = ''
        pe_map['header_badge'] = '💨 Parque Eólico'
        pe_map['titulo_nombre'] = pe_map['parque']
        pe_map['subtitulo_meta'] = "Titular: " + pe_map['operador'].astype(str) + " (" + pe_map['provincia'].astype(str) + ")"
        
        # Calcular distancia al yacimiento más cercano para el tooltip del parque
        p_info_1, p_info_2, p_info_3, p_info_4 = [], [], [], []
        pe_m1, pe_m2, pe_m3, pe_m4 = [], [], [], []
        coords_yac_todos = df_yac_raw[['yacimiento', 'latitud', 'longitud']].drop_duplicates()
        for _, r_p in pe_map.iterrows():
            p_lat, p_lon = r_p['latitud'], r_p['longitud']
            pot_mw = r_p['generacion_mwh'] / horas_periodo
            
            if yacimientos_sel and r_p['central_nemo'] in parques_cercanos_info:
                d_min, y_nom_min = parques_cercanos_info[r_p['central_nemo']]
                estado_txt = f"En radio de {radio_cobertura_km} km ({fmt_num(d_min, 1)} km a {y_nom_min})"
            else:
                # Buscar yacimiento más cercano en la cuenca
                d_min = float('inf')
                y_nom_min = "N/A"
                for _, ry in coords_yac_todos.iterrows():
                    if pd.notna(ry['latitud']) and ry['latitud'] != 0:
                        d = haversine_km(p_lat, p_lon, ry['latitud'], ry['longitud'])
                        if d < d_min:
                            d_min = d
                            y_nom_min = ry['yacimiento']
                if yacimientos_sel:
                    estado_txt = f"Fuera de radio (más cercano: {y_nom_min} a {fmt_num(d_min, 1)} km)"
                else:
                    estado_txt = f"Yac. más cercano: {y_nom_min} a {fmt_num(d_min, 1)} km"
                    
            p_info_1.append(f"Generación Acumulada: {fmt_num(r_p['generacion_mwh'], 0)} MWh")
            p_info_2.append(f"Potencia Media: {fmt_num(pot_mw, 2)} MW | Cobertura: {radio_cobertura_km} km ({r_p['central_nemo']})")
            p_info_3.append(estado_txt)
            p_info_4.append(f"Emisiones desplazadas: {fmt_num(r_p['generacion_mwh'] * factor_emision_red, 0)} tCO₂")
            
            pe_m1.append(f"{fmt_num(pot_mw, 2)} MW")
            pe_m2.append(f"{radio_cobertura_km} km ({r_p['central_nemo']})")
            pe_m3.append(f"{fmt_num(r_p['generacion_mwh'], 0)} MWh")
            pe_m4.append(f"{fmt_num(r_p['generacion_mwh'] * factor_emision_red, 0)} tCO₂ ({estado_txt})")
            
        pe_map['info_1'] = p_info_1
        pe_map['info_2'] = p_info_2
        pe_map['info_3'] = p_info_3
        pe_map['info_4'] = p_info_4
        
        pe_map['metrica_1_label'] = "Potencia Media Estimada:"
        pe_map['metrica_1_val'] = pe_m1
        pe_map['metrica_2_label'] = "Radio de Cobertura Eólica:"
        pe_map['metrica_2_val'] = pe_m2
        pe_map['metrica_3_label'] = "Generación Acumulada:"
        pe_map['metrica_3_val'] = pe_m3
        pe_map['metrica_4_label'] = "Emisiones Desplazadas:"
        pe_map['metrica_4_val'] = pe_m4
    else:
        pe_map = pd.DataFrame()

    # Construcción de capas Pydeck con prioridad de renderizado (Render Priority):
    # 1. Halos de cobertura eólica (siempre visibles en el suelo con borde nítido y hover oscuro)
    # 2. Columnas 3D de yacimientos (cilindros esbeltos semi-translúcidos)
    # 3. Pedestal eólico en el suelo (base iluminada sobrepuesta)
    # 4. Iconos de turbinas eólicas (al frente de todo, mástil y 3 aspas aerodinámicas)
    capas = []

    # 1. Capa de Cobertura / Halos Eólicos (Siempre visibles en el suelo con borde nítido y hover oscuro contrastante)
    if not pe_map.empty:
        layer_pe_halo = pdk.Layer(
            "ScatterplotLayer",
            id="wind-halo-layer",
            data=pe_map,
            get_position=["longitud", "latitud"],
            get_radius="radio_metros",
            radius_scale=1,
            stroked=True,
            filled=True,
            line_width_min_pixels=1.5,
            get_line_color="color_halo_line",
            get_fill_color="color_halo_fill",
            pickable=True,
            auto_highlight=True,
            highlight_color=[12, 35, 60, 220]  # Azul petróleo oscuro contrastante con alta opacidad (~86%)
        )
        capas.append(layer_pe_halo)

    # 2. Capa de Yacimientos Hidrocarburíferos (ColumnLayer 3D esbelta)
    if not yac_map.empty:
        layer_yac = pdk.Layer(
            "ColumnLayer",
            id="yacimientos-layer",
            data=yac_map,
            get_position=["longitud", "latitud"],
            get_elevation="elevacion",
            elevation_scale=1,
            radius=650,
            disk_resolution=16,
            get_fill_color="color",
            opacity=0.85,
            pickable=True,
            auto_highlight=True,
            extruded=True
        )
        capas.append(layer_yac)

    # 3. Capa de Pedestal / Base luminosa en el suelo (ScatterplotLayer)
    if not pe_map.empty:
        layer_pe_base = pdk.Layer(
            "ScatterplotLayer",
            id="wind-base-layer",
            data=pe_map,
            get_position=["lon_display", "lat_display"],
            get_radius=1500,
            radius_scale=1,
            get_fill_color="color_base",
            get_line_color=[255, 255, 255, 180],
            stroked=True,
            filled=True,
            line_width_min_pixels=1,
            pickable=True,
            auto_highlight=True,
            highlight_color=[255, 255, 255, 255]
        )
        capas.append(layer_pe_base)

    # 4. Capa de la Turbina Eólica (IconLayer con mástil y 3 aspas en billboard 3D)
    if not pe_map.empty:
        layer_pe_turbines = pdk.Layer(
            "IconLayer",
            id="wind-turbines-layer",
            data=pe_map,
            get_position=["lon_display", "lat_display"],
            get_icon="icon_data",
            get_size=55,
            size_scale=1,
            size_min_pixels=55,
            size_max_pixels=115,
            billboard=True,
            pickable=True
        )
        capas.append(layer_pe_turbines)

    # 5. Capa Soberana de rotulado TextLayer para Islas Malvinas y Puerto Argentino
    df_soberania = pd.DataFrame([
        # Etiqueta central: Un poco más al sur y al este para tapar exactamente el texto en inglés
        {
            "nombre": "ISLAS MALVINAS",
            "lat": -51.84,
            "lon": -59.48,
            "font_size": 13,
            "padding_x": 16,
            "padding_y": 8
        },
        # Etiqueta en la capital: Tapa por completo "Stanley" en el este
        {
            "nombre": "PUERTO ARGENTINO",
            "lat": -51.69,
            "lon": -57.85,
            "font_size": 11,
            "padding_x": 14,
            "padding_y": 6
        }
    ])

    soberania_layer = pdk.Layer(
        "TextLayer",
        id="soberania-layer",
        data=df_soberania,
        get_position=["lon", "lat"],
        get_text="nombre",
        get_color=[255, 255, 255, 240], # Letras blancas nítidas
        get_size="font_size",
        get_alignment_baseline=pdk.types.String("center"),
        get_text_anchor=pdk.types.String("middle"),
        background=True,
        get_background_color=[15, 23, 42, 255], # 255 es fully opaque (tapa todo lo que está abajo)
        background_padding=[16, 8],
        get_background_padding_x="padding_x",
        get_background_padding_y="padding_y",
        billboard=True,
        pickable=False
    )
    capas.append(soberania_layer)

    # Vista inicial 3D centrada en Cuenca Golfo San Jorge (o enfocada en el yacimiento seleccionado)
    if yacimientos_sel and not yac_map.empty:
        lat_centro = float(yac_map['latitud'].mean())
        lon_centro = float(yac_map['longitud'].mean())
        zoom_inicial = 9.2 if len(yacimientos_sel) <= 2 else 8.5
        pitch_inicial = 45
        bearing_inicial = -15
    else:
        lat_centro = -46.15
        lon_centro = -67.80
        zoom_inicial = 7.3
        pitch_inicial = 42
        bearing_inicial = 0

    view_state = pdk.ViewState(
        latitude=lat_centro,
        longitude=lon_centro,
        zoom=zoom_inicial,
        min_zoom=6.0,   # Evita zoom out excesivo
        max_zoom=12.0,
        pitch=pitch_inicial,
        bearing=bearing_inicial,
        drag_pan=True,
        scroll_zoom=True
    )

    # Tooltip interactivo limpio sin escapes de etiquetas ni caracteres crudos
    tooltip = {
        "html": """
        <div style="background-color: #0f172a; padding: 12px 16px; border-radius: 8px; border: 1.5px solid #38bdf8; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.65); color: #f8fafc; min-width: 250px; max-width: 440px; line-height: 1.5;">
            <div style="color: #38bdf8; font-weight: 700; font-size: 11.5px; text-transform: uppercase; letter-spacing: 0.5px;">{header_badge}</div>
            <div style="color: #ffffff; font-weight: 700; font-size: 16px; margin: 2px 0 3px 0;">{titulo_nombre}</div>
            <div style="color: #94a3b8; font-size: 12.5px; margin-bottom: 8px;">{subtitulo_meta}</div>
            <hr style="margin: 6px 0 8px 0; border: 0; border-top: 1px solid rgba(56, 189, 248, 0.25);"/>
            <div style="margin-bottom: 4px; font-size: 13px;">
                <span style="color: #94a3b8;">{metrica_1_label}</span>
                <span style="color: #f1f5f9; font-weight: 600; float: right; margin-left: 14px;">{metrica_1_val}</span>
            </div>
            <div style="margin-bottom: 4px; font-size: 13px;">
                <span style="color: #94a3b8;">{metrica_2_label}</span>
                <span style="color: #38bdf8; font-weight: 600; float: right; margin-left: 14px;">{metrica_2_val}</span>
            </div>
            <div style="margin-bottom: 4px; font-size: 13px;">
                <span style="color: #94a3b8;">{metrica_3_label}</span>
                <span style="color: #fbbf24; font-weight: 600; float: right; margin-left: 14px;">{metrica_3_val}</span>
            </div>
            <div style="margin-top: 6px; padding-top: 5px; border-top: 1px dashed rgba(148, 163, 184, 0.2); font-size: 12.5px;">
                <span style="color: #94a3b8;">{metrica_4_label}</span>
                <span style="color: #4ade80; font-weight: 600; float: right; margin-left: 14px;">{metrica_4_val}</span>
            </div>
            <div style="clear: both;"></div>
        </div>
        """,
        "style": {
            "backgroundColor": "transparent",
            "color": "#f8fafc"
        }
    }

    mapbox_token = os.environ.get("MAPBOX_API_KEY", "")
    if mapbox_token:
        map_style = "mapbox://styles/mapbox/dark-v11"
        map_provider = "mapbox"
    else:
        map_style = pdk.map_styles.CARTO_DARK
        map_provider = "carto"

    r = pdk.Deck(
        layers=capas,
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style=map_style,
        map_provider=map_provider
    )

    st.pydeck_chart(r, use_container_width=True, height=540)

    # Inyector de posicionamiento inteligente adaptativo para el Tooltip (auto-flip 4 cuadrantes)
    components.html(
        """
        <script>
        (function() {
            function initSmartTooltip() {
                try {
                    const parentDoc = window.parent ? window.parent.document : document;
                    if (!parentDoc) return;

                    function autoPositionTooltip() {
                        const tooltip = parentDoc.querySelector('.deck-tooltip');
                        if (!tooltip || tooltip.style.display === 'none') return;

                        const mapBox = parentDoc.querySelector('[data-testid="stDeckGlJsonChart"]') || 
                                       parentDoc.querySelector('.stPydeckChart') || 
                                       tooltip.parentElement;
                        if (!mapBox) return;

                        const boxRect = mapBox.getBoundingClientRect();
                        const transform = tooltip.style.transform || '';
                        const match = transform.match(/translate\(([-\d.]+)px,\s*([-\d.]+)px\)/);

                        if (match) {
                            const x = parseFloat(match[1]);
                            const y = parseFloat(match[2]);
                            const h = boxRect.height || 540;
                            const w = boxRect.width || 800;

                            // Si el punto está en la parte superior (arriba) -> proyectar hacia abajo
                            // Si el punto está en la parte inferior (abajo) -> proyectar hacia arriba
                            const isTop = y < (h * 0.48);
                            const translateY = isTop ? '14px' : 'calc(-100% - 14px)';

                            // Si el punto está muy a la derecha del mapa -> proyectar hacia la izquierda
                            // Caso general -> al lado derecho del cursor
                            const isRightEdge = x > (w - 380);
                            const translateX = isRightEdge ? 'calc(-100% - 20px)' : '20px';

                            tooltip.style.setProperty('translate', `${translateX} ${translateY}`, 'important');
                        }
                    }

                    if (!parentDoc.__smartTooltipAttached) {
                        parentDoc.__smartTooltipAttached = true;
                        
                        const observer = new MutationObserver(autoPositionTooltip);
                        observer.observe(parentDoc.body, {
                            attributes: true,
                            subtree: true,
                            attributeFilter: ['style', 'class']
                        });

                        parentDoc.addEventListener('mousemove', function() {
                            requestAnimationFrame(autoPositionTooltip);
                        }, { passive: true });
                    }
                    autoPositionTooltip();
                } catch(e) {
                    console.error('Smart tooltip error:', e);
                }
            }

            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', initSmartTooltip);
            } else {
                initSmartTooltip();
            }
            setTimeout(initSmartTooltip, 300);
            setTimeout(initSmartTooltip, 1000);
        })();
        </script>
        """,
        height=0,
        width=0
    )

    # Leyenda visual explicativa debajo del mapa
    col_leg1, col_leg2, col_leg3, col_leg4 = st.columns(4)
    with col_leg1:
        st.markdown(f":material/wind_power: **Parques Eólicos**: Turbina cian con halo continuo ({radio_cobertura_km} km); resalta en azul petróleo al interactuar.")
    with col_leg2:
        st.markdown("🟠 **Yacimientos WOR Moderado (<90% / WOR < 9)**: Ámbar/naranja. Menor corte relativo de agua.")
    with col_leg3:
        st.markdown("🔵 **Yacimientos WOR Severo (≥90% / WOR ≥ 9)**: Azul eléctrico. Alto BSW y electrointensividad.")
    with col_leg4:
        st.markdown("📏 **Altura Columnas 3D**: Volumen consolidado de fluido extraído ($m^3$).")

with tab_graficos:
    # Fila de Títulos, Controles y Gráficos Nivelados
    col_graf1, col_graf2 = st.columns(2)

    # Columna izquierda: Petróleo vs. Agua Bruta
    with col_graf1:
        st.markdown("##### 🛢️ Petróleo vs. 💧 Agua Bruta (Serie Consolidada)")
        st.caption("Evolución mensual consolidada: extracción de petróleo vs. corte de agua")
        if not df_yac.empty:
            df_yac_mes = df_yac.groupby('fecha', as_index=False).agg({
                'prod_petroleo_m3': 'sum',
                'prod_agua_m3': 'sum'
            }).sort_values('fecha')
            
            fig1 = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Área de Petróleo (Eje Izquierdo)
            fig1.add_trace(
                go.Scatter(
                    x=df_yac_mes['fecha'],
                    y=df_yac_mes['prod_petroleo_m3'],
                    name="Petróleo (m³)",
                    mode='lines',
                    line=dict(color='#d97706', width=2.5),
                    fill='tozeroy',
                    fillcolor='rgba(217, 119, 6, 0.15)',
                    hovertemplate="<b>%{x|%Y-%m}</b><br>Petróleo: %{y:,.0f} m³<extra></extra>"
                ),
                secondary_y=False
            )
            
            # Curva de Agua Bruta (Eje Derecho)
            fig1.add_trace(
                go.Scatter(
                    x=df_yac_mes['fecha'],
                    y=df_yac_mes['prod_agua_m3'],
                    name="Agua Bruta (m³)",
                    mode='lines',
                    line=dict(color='#0284c7', width=2.5),
                    hovertemplate="<b>%{x|%Y-%m}</b><br>Agua Bruta: %{y:,.0f} m³<extra></extra>"
                ),
                secondary_y=True
            )
            
            fig1.update_layout(
                separators=",.",
                height=350,
                font=dict(size=13),
                margin=dict(t=15, b=30, l=40, r=40),
                legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5, font=dict(size=12)),
                hovermode="x unified",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )
            # Calibración de rangos verticales para reflejar fielmente la dominancia de agua (BSW > 90%)
            max_petroleo = float(df_yac_mes['prod_petroleo_m3'].max()) if len(df_yac_mes) > 0 and df_yac_mes['prod_petroleo_m3'].max() > 0 else 1.0
            max_agua = float(df_yac_mes['prod_agua_m3'].max()) if len(df_yac_mes) > 0 and df_yac_mes['prod_agua_m3'].max() > 0 else 1.0

            fig1.update_xaxes(showgrid=True, gridcolor="#334155")
            fig1.update_yaxes(
                title_text="Petróleo [m³]", 
                secondary_y=False, 
                showgrid=True, 
                gridcolor="#334155", 
                tickformat=",.0f",
                range=[0, max_petroleo * 2.8]
            )
            fig1.update_yaxes(
                title_text="Agua Bruta [m³]", 
                secondary_y=True, 
                showgrid=False, 
                tickformat=",.0f",
                range=[0, max_agua * 1.15]
            )
            
            st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': 'hover', 'displaylogo': False})
        else:
            st.info("No hay datos de yacimientos para los filtros aplicados.")

    # Columna derecha: Generación Eólica Mensual
    with col_graf2:
        st.markdown("##### :material/wind_power: Generación Eólica Mensual Agregada y Tendencia")
        modo_grafico_eolico = st.radio(
            "Visualización Eólica:",
            options=["Total Mensual + Tendencia", "Líneas por Parque (Estacionalidad)"],
            index=0,
            horizontal=True,
            label_visibility="collapsed"
        )

        if not df_pe.empty:
            if modo_grafico_eolico == "Total Mensual + Tendencia":
                df_pe_tot = df_pe.groupby('fecha', as_index=False).agg({
                    'generacion_mwh': 'sum'
                }).sort_values('fecha')
                df_pe_tot['tendencia_ma6'] = df_pe_tot['generacion_mwh'].rolling(window=6, min_periods=1).mean()
                
                fig2 = go.Figure()
                fig2.add_trace(
                    go.Bar(
                        x=df_pe_tot['fecha'],
                        y=df_pe_tot['generacion_mwh'],
                        name="Generación Mensual (MWh)",
                        marker_color="rgba(16, 185, 129, 0.65)",
                        marker_line_color="rgba(5, 150, 105, 1.0)",
                        marker_line_width=1,
                        hovertemplate="<b>%{x|%Y-%m}</b><br>Generación Total: %{y:,.0f} MWh<extra></extra>"
                    )
                )
                fig2.add_trace(
                    go.Scatter(
                        x=df_pe_tot['fecha'],
                        y=df_pe_tot['tendencia_ma6'],
                        name="Tendencia (Media Móvil 6m)",
                        mode="lines",
                        line=dict(color="#0f766e", width=3),
                        hovertemplate="<b>%{x|%Y-%m}</b><br>Tendencia 6m: %{y:,.0f} MWh<extra></extra>"
                    )
                )
                
                # Si hay datos de yacimientos, agregar línea de referencia de demanda eléctrica mensual
                if not df_yac.empty:
                    df_dem_mes = df_yac.groupby('fecha', as_index=False)['prod_liquido_m3'].sum().sort_values('fecha')
                    df_dem_mes['demanda_mwh'] = (df_dem_mes['prod_liquido_m3'] * consumo_esp_extraccion) / 1000.0
                    fig2.add_trace(
                        go.Scatter(
                            x=df_dem_mes['fecha'],
                            y=df_dem_mes['demanda_mwh'],
                            name="Demanda Extracción (MWh)",
                            mode="lines",
                            line=dict(color="#e11d48", width=2, dash="dot"),
                            hovertemplate="<b>%{x|%Y-%m}</b><br>Demanda Extracción: %{y:,.0f} MWh<extra></extra>"
                        )
                    )
                    
                fig2.update_layout(
                    separators=",.",
                    height=350,
                    font=dict(size=13),
                    margin=dict(t=15, b=30, l=40, r=40),
                    legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5, font=dict(size=12)),
                    hovermode="x unified",
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)"
                )
                fig2.update_xaxes(showgrid=True, gridcolor="#334155")
                fig2.update_yaxes(title_text="Energía [MWh]", showgrid=True, gridcolor="#334155", tickformat=",.0f")
                st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': 'hover', 'displaylogo': False})
                
            else:
                df_pe_mes = df_pe.groupby(['fecha', 'parque'], as_index=False).agg({
                    'generacion_mwh': 'sum'
                }).sort_values('fecha')
                
                fig2 = px.line(
                    df_pe_mes,
                    x='fecha',
                    y='generacion_mwh',
                    color='parque',
                    color_discrete_sequence=px.colors.qualitative.Bold,
                    labels={'generacion_mwh': 'Generación [MWh]', 'fecha': 'Fecha', 'parque': 'Parque Eólico'}
                )
                fig2.update_traces(
                    line=dict(width=2.2),
                    hovertemplate="<b>%{fullData.name}</b>: %{y:,.0f} MWh<extra></extra>"
                )
                fig2.update_layout(
                    separators=",.",
                    height=350,
                    font=dict(size=13),
                    margin=dict(t=15, b=30, l=40, r=40),
                    legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5, font=dict(size=11)),
                    hovermode="x unified",
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)"
                )
                fig2.update_xaxes(showgrid=True, gridcolor="#334155")
                fig2.update_yaxes(title_text="Energía Eólica [MWh]", showgrid=True, gridcolor="#334155", tickformat=",.0f")
                st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': 'hover', 'displaylogo': False})
        else:
            if yacimientos_sel:
                st.warning(f"Sin generación eólica cercana dentro del radio de {radio_cobertura_km} km para los yacimientos seleccionados.")
            else:
                st.info("No hay datos de parques eólicos para los filtros aplicados.")

    # Fila 3: Dos tablas desplegables niveladas exactamente a la misma altura horizontal
    col_izq, col_der = st.columns(2)

    with col_izq:
        with st.expander("Ver Trazabilidad y Balance por Yacimiento", icon="🛢️"):
            if not yac_map.empty:
                yac_tabla = yac_map.sort_values('prod_liquido_m3', ascending=False).head(30).copy()
                yac_tabla['Petróleo (m³)'] = yac_tabla['prod_petroleo_m3'].apply(lambda x: fmt_num(x, 0))
                yac_tabla['Agua (m³)'] = yac_tabla['prod_agua_m3'].apply(lambda x: fmt_num(x, 0))
                yac_tabla['BSW (%)'] = yac_tabla['bsw_pct'].apply(lambda x: fmt_num(x, 1) + "%")
                yac_tabla['WOR'] = yac_tabla['wor'].apply(lambda x: fmt_num(x, 2))
                
                yac_mostrar = yac_tabla[['yacimiento', 'operador', 'provincia', 'Petróleo (m³)', 'Agua (m³)', 'BSW (%)', 'WOR']].copy()
                yac_mostrar.columns = ['Yacimiento', 'Operadores en el Período', 'Provincia', 'Petróleo (m³)', 'Agua (m³)', 'BSW (%)', 'WOR']
                st.dataframe(yac_mostrar, width="stretch", hide_index=True)
            else:
                st.write("Sin datos de yacimientos disponibles.")

    with col_der:
        with st.expander("Ver Detalle de Parques Eólicos Activos", icon=":material/wind_power:"):
            if not df_pe.empty:
                pe_resumen = df_pe.groupby(['central_nemo', 'parque', 'provincia'], as_index=False).agg(
                    total_mwh=('generacion_mwh', 'sum'),
                    prom_mwh=('generacion_mwh', 'mean'),
                    meses=('generacion_mwh', 'count')
                ).sort_values('total_mwh', ascending=False)
                
                if yacimientos_sel:
                    pe_resumen['Distancia (km)'] = pe_resumen['central_nemo'].apply(
                        lambda c: fmt_num(parques_cercanos_info[c][0], 1) if c in parques_cercanos_info else "-"
                    )
                pe_resumen['Total MWh'] = pe_resumen['total_mwh'].apply(lambda x: fmt_num(x, 2))
                pe_resumen['Promedio Mensual MWh'] = pe_resumen['prom_mwh'].apply(lambda x: fmt_num(x, 2))
                
                cols_mostrar = ['central_nemo', 'parque', 'provincia', 'Total MWh', 'Promedio Mensual MWh', 'meses']
                nombres_cols = ['Código', 'Parque Eólico', 'Provincia', 'Total MWh', 'Promedio Mensual MWh', 'Meses']
                if yacimientos_sel:
                    cols_mostrar.insert(3, 'Distancia (km)')
                    nombres_cols.insert(3, 'Distancia (km)')
                    
                pe_mostrar = pe_resumen[cols_mostrar].copy()
                pe_mostrar.columns = nombres_cols
                st.dataframe(pe_mostrar, width="stretch", hide_index=True)
            else:
                st.write("Sin parques eólicos activos en el radio seleccionado.")


