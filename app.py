import streamlit as st
import pandas as pd
from datetime import date, timedelta
from io import StringIO
import calendar

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Igreja Batista de Pindorama",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# ESTADO DE TEMA
# ══════════════════════════════════════════════════════════════════════════════
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

dark = st.session_state.dark_mode

# ── Paleta de cores por tema ──────────────────────────────────────────────────
if dark:
    C = {
        "bg":          "#0f172a",
        "bg2":         "#1e293b",
        "bg3":         "#334155",
        "border":      "#334155",
        "border2":     "#475569",
        "text":        "#f1f5f9",
        "text2":       "#94a3b8",
        "text3":       "#64748b",
        "topbar":      "#020617",
        "topbar_border":"#1e293b",
        "accent":      "#3b82f6",
        "accent2":     "#1d4ed8",
        "green":       "#10b981",
        "amber":       "#f59e0b",
        "rose":        "#f43f5e",
        "panel_shadow":"rgba(0,0,0,0.3)",
        "hover":       "#1e293b",
        "input_bg":    "#1e293b",
        "export_bg":   "#1e293b",
        "cal_normal":  "#1e293b",
        "cal_bday":    "#1e3a5f",
        "cal_today_bg":"#2563eb",
        "cal_text":    "#94a3b8",
        "avatar_bg":   "#1e3a5f",
        "avatar_text": "#3b82f6",
        "kpi_bg":      "#1e293b",
        "eng_bg":      "#334155",
        "season_bar":  "#1e3a5f",
        "mini_bg":     "#1e293b",
        "tab_bg":      "#1e293b",
        "tab_active":  "#f1f5f9",
        "tab_border":  "#334155",
    }
    THEME_ICON  = "☀️"
    THEME_LABEL = "Tema Claro"
else:
    C = {
        "bg":          "#f8fafc",
        "bg2":         "#ffffff",
        "bg3":         "#f1f5f9",
        "border":      "#e2e8f0",
        "border2":     "#cbd5e1",
        "text":        "#0f172a",
        "text2":       "#475569",
        "text3":       "#94a3b8",
        "topbar":      "#0f172a",
        "topbar_border":"#1e293b",
        "accent":      "#2563eb",
        "accent2":     "#1d4ed8",
        "green":       "#059669",
        "amber":       "#d97706",
        "rose":        "#db2777",
        "panel_shadow":"rgba(0,0,0,0.04)",
        "hover":       "#f8fafc",
        "input_bg":    "#ffffff",
        "export_bg":   "#f8fafc",
        "cal_normal":  "#f1f5f9",
        "cal_bday":    "#dbeafe",
        "cal_today_bg":"#2563eb",
        "cal_text":    "#64748b",
        "avatar_bg":   "#dbeafe",
        "avatar_text": "#1d4ed8",
        "kpi_bg":      "#ffffff",
        "eng_bg":      "#f1f5f9",
        "season_bar":  "#dbeafe",
        "mini_bg":     "#f8fafc",
        "tab_bg":      "transparent",
        "tab_active":  "#0f172a",
        "tab_border":  "#e2e8f0",
    }
    THEME_ICON  = "🌙"
    THEME_LABEL = "Tema Escuro"

# ══════════════════════════════════════════════════════════════════════════════
# CSS GLOBAL
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Lora:wght@600;700&display=swap');

*, html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    box-sizing: border-box;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
[data-testid="collapsedControl"] {{ display: none; }}
section[data-testid="stSidebar"] {{ display: none; }}
.block-container {{ padding: 0 0 4rem 0 !important; max-width: 100% !important; }}

/* ── Body background ── */
body, .stApp, [data-testid="stAppViewContainer"] {{
    background: {C["bg"]} !important;
}}
[data-testid="stAppViewBlockContainer"] {{
    background: {C["bg"]} !important;
}}

/* ── TOPBAR ── */
.topbar {{
    background: {C["topbar"]};
    border-bottom: 1px solid {C["topbar_border"]};
    padding: 0 48px;
    display: flex; align-items: center; justify-content: space-between;
    height: 64px;
    position: sticky; top: 0; z-index: 999;
}}
.topbar-brand {{ display: flex; align-items: center; gap: 14px; }}
.topbar-monogram {{
    width: 36px; height: 36px; background: {C["accent"]};
    border-radius: 8px; display: flex; align-items: center;
    justify-content: center; font-weight: 700; color: white;
    font-size: 13px; letter-spacing: .03em; flex-shrink: 0;
}}
.topbar-name {{ font-family: 'Lora', serif; color: #f1f5f9; font-size: 1rem; font-weight: 600; }}
.topbar-sub  {{ color: #475569; font-size: .7rem; text-transform: uppercase; letter-spacing: .07em; }}
.topbar-right {{ display: flex; align-items: center; gap: 16px; }}
.topbar-date {{ color: #64748b; font-size: .8rem; }}

/* ── TABS ── */
.stTabs {{ padding: 0 48px; }}
.stTabs [data-baseweb="tab-list"] {{
    background: transparent;
    border-bottom: 1px solid {C["tab_border"]};
    gap: 0; padding: 0; margin-bottom: 28px;
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent; border: none;
    border-bottom: 2px solid transparent; border-radius: 0;
    padding: 16px 22px; font-size: .85rem; font-weight: 500;
    color: {C["text3"]}; margin-bottom: -1px;
}}
.stTabs [aria-selected="true"] {{
    background: transparent !important;
    color: {C["tab_active"]} !important;
    border-bottom: 2px solid {C["accent"]} !important;
}}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] {{ display: none; }}

/* ── PANELS ── */
.panel {{
    background: {C["bg2"]};
    border: 1px solid {C["border"]};
    border-radius: 14px; padding: 22px 24px; margin-bottom: 18px;
    box-shadow: 0 1px 3px {C["panel_shadow"]};
}}
.panel-title {{
    font-size: .7rem; font-weight: 600; color: {C["text3"]};
    text-transform: uppercase; letter-spacing: .08em;
    margin-bottom: 16px; padding-bottom: 12px;
    border-bottom: 1px solid {C["border"]};
}}
.panel-title span {{ color: {C["text3"]}; font-weight: 400; }}

/* ── KPI CARDS ── */
.kpi-row {{ display: grid; grid-template-columns: repeat(4,1fr); gap: 14px; margin-bottom: 22px; }}
.kpi {{
    background: {C["kpi_bg"]}; border: 1px solid {C["border"]};
    border-radius: 14px; padding: 20px 22px;
    border-top: 3px solid {C["border"]};
    box-shadow: 0 1px 3px {C["panel_shadow"]};
}}
.kpi.blue  {{ border-top-color: {C["accent"]}; }}
.kpi.green {{ border-top-color: {C["green"]}; }}
.kpi.amber {{ border-top-color: {C["amber"]}; }}
.kpi.rose  {{ border-top-color: {C["rose"]}; }}
.kpi-label {{ font-size:.7rem; font-weight:600; color:{C["text3"]}; text-transform:uppercase; letter-spacing:.08em; margin-bottom:8px; }}
.kpi-value {{ font-family:'Lora',serif; font-size:2rem; color:{C["text"]}; line-height:1; margin-bottom:4px; }}
.kpi-sub   {{ font-size:.75rem; color:{C["text3"]}; }}

/* ── URGENCY BANNER ── */
.urgency-banner {{
    background: linear-gradient(135deg, #1e3a8a 0%, {C["accent"]} 100%);
    border-radius: 14px; padding: 26px 30px; margin-bottom: 22px;
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 12px;
}}
.urgency-title {{ font-family:'Lora',serif; color:white; font-size:1.4rem; margin-bottom:4px; }}
.urgency-sub   {{ color: #93c5fd; font-size:.85rem; }}
.urgency-empty {{ color: #bfdbfe; font-size:.88rem; font-style:italic; }}

/* ── AVATAR ── */
.avatar {{
    background: {C["avatar_bg"]}; color: {C["avatar_text"]};
    border-radius: 50%; display: flex; align-items: center;
    justify-content: center; font-weight: 700; flex-shrink: 0;
}}

/* ── TODAY GRID ── */
.today-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:12px; margin-bottom:22px; }}
.today-card {{
    background:{C["bg2"]}; border:1px solid {C["border"]};
    border-radius:12px; padding:16px 18px;
    display:flex; align-items:center; gap:14px;
    box-shadow:0 1px 3px {C["panel_shadow"]};
}}
.today-name   {{ font-weight:600; color:{C["text"]}; font-size:.92rem; }}
.today-detail {{ color:{C["text2"]}; font-size:.78rem; margin-top:2px; }}
.today-phone  {{ color:{C["accent"]}; font-size:.78rem; font-weight:500; margin-top:4px; }}

/* ── GENERIC TABLE ── */
.gtable {{ width:100%; border-collapse:collapse; }}
.gtable th {{
    text-align:left; font-size:.68rem; font-weight:600; color:{C["text3"]};
    text-transform:uppercase; letter-spacing:.08em;
    padding:0 14px 10px; border-bottom:1px solid {C["border"]};
}}
.gtable td {{ padding:11px 14px; border-bottom:1px solid {C["border"]}; color:{C["text2"]}; vertical-align:middle; }}
.gtable tr:last-child td {{ border-bottom:none; }}
.gtable tr:hover td {{ background:{C["hover"]}; }}
.gt-name {{ font-weight:500; color:{C["text"]}; font-size:.875rem; }}
.gt-sub  {{ color:{C["text3"]}; font-size:.75rem; margin-top:1px; }}
.gt-phone{{ color:{C["accent"]}; font-size:.82rem; font-weight:500; }}

/* ── BADGES ── */
.badge {{ display:inline-block; padding:3px 10px; border-radius:99px; font-size:.72rem; font-weight:700; }}
.badge-today  {{ background:#fef9c3; color:#854d0e; }}
.badge-soon   {{ background:#dbeafe; color:#1e40af; }}
.badge-past   {{ background:{C["bg3"]}; color:{C["text3"]}; }}
.pill {{ display:inline-block; padding:2px 10px; border-radius:99px; font-size:.72rem; font-weight:600; }}
.pill-sim {{ background:#d1fae5; color:#065f46; }}
.pill-nao {{ background:#fee2e2; color:#991b1b; }}

/* ── CALENDAR ── */
.cal-grid {{ display:grid; grid-template-columns:repeat(7,1fr); gap:4px; }}
.cal-hdr  {{ text-align:center; font-size:.65rem; font-weight:600; color:{C["text3"]}; padding:4px 0 8px; text-transform:uppercase; }}
.cal-day  {{
    aspect-ratio:1; border-radius:8px; display:flex;
    flex-direction:column; align-items:center; justify-content:center;
    font-size:.78rem; cursor:default;
}}
.cal-empty  {{ background:transparent; }}
.cal-normal {{ background:{C["cal_normal"]}; color:{C["cal_text"]}; }}
.cal-bday   {{ background:{C["cal_bday"]}; color:{C["accent"]}; font-weight:600; }}
.cal-today  {{ background:{C["cal_today_bg"]}; color:white; font-weight:700; }}
.cal-dot    {{ width:4px; height:4px; border-radius:50%; background:{C["accent"]}; margin-top:2px; }}
.cal-today .cal-dot {{ background:white; }}

/* ── PYRAMID ── */
.pyr-row  {{ display:flex; align-items:center; gap:8px; margin-bottom:8px; }}
.pyr-lbl  {{ font-size:.72rem; color:{C["text2"]}; flex-shrink:0; padding:0 6px; }}
.pyr-m    {{ height:20px; background:{C["accent"]}; border-radius:4px 0 0 4px; }}
.pyr-f    {{ height:20px; background:{C["rose"]}; border-radius:0 4px 4px 0; }}
.pyr-sep  {{ width:1px; background:{C["border"]}; height:20px; flex-shrink:0; }}
.pyr-val  {{ font-size:.7rem; color:{C["text3"]}; width:24px; flex-shrink:0; text-align:center; }}

/* ── ENGAGEMENT ── */
.eng-row  {{ display:flex; align-items:center; gap:10px; margin-bottom:9px; }}
.eng-lbl  {{ width:120px; font-size:.78rem; color:{C["text2"]}; flex-shrink:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
.eng-bg   {{ flex:1; height:8px; background:{C["eng_bg"]}; border-radius:99px; overflow:hidden; }}
.eng-fill {{ height:100%; border-radius:99px; }}
.eng-pct  {{ font-size:.75rem; font-weight:600; color:{C["text2"]}; width:36px; text-align:right; flex-shrink:0; }}

/* ── SEASON ── */
.season-wrap {{ display:flex; align-items:flex-end; gap:5px; height:90px; margin-top:8px; }}
.season-col  {{ display:flex; flex-direction:column; align-items:center; flex:1; height:100%; justify-content:flex-end; gap:3px; }}
.season-bar  {{ width:100%; background:{C["season_bar"]}; border-radius:4px 4px 0 0; min-height:3px; }}
.season-bar.cur {{ background:{C["accent"]}; }}
.season-lbl  {{ font-size:.6rem; color:{C["text3"]}; }}
.season-cnt  {{ font-size:.65rem; font-weight:600; color:{C["text2"]}; }}

/* ── MEMBER TABLE ── */
.mtable {{ width:100%; border-collapse:collapse; font-size:.875rem; }}
.mtable th {{
    text-align:left; font-size:.68rem; font-weight:600; color:{C["text3"]};
    text-transform:uppercase; letter-spacing:.08em;
    padding:0 14px 10px; border-bottom:1px solid {C["border"]};
    background:{C["bg2"]};
}}
.mtable td {{ padding:12px 14px; border-bottom:1px solid {C["border"]}; vertical-align:middle; }}
.mtable tr:last-child td {{ border-bottom:none; }}
.mtable tr:hover td {{ background:{C["hover"]}; }}
.mt-name {{ font-weight:500; color:{C["text"]}; }}
.mt-sub  {{ color:{C["text3"]}; font-size:.75rem; margin-top:1px; }}

/* ── MINI STATS ── */
.mini-grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:12px; margin-bottom:16px; }}
.mini-card {{
    background:{C["mini_bg"]}; border-radius:10px;
    padding:14px; text-align:center;
    border:1px solid {C["border"]};
}}
.mini-val {{ font-family:'Lora',serif; font-size:1.6rem; color:{C["text"]}; }}
.mini-lbl {{ font-size:.68rem; color:{C["text3"]}; text-transform:uppercase; letter-spacing:.06em; margin-top:3px; }}

/* ── INPUTS ── */
.stTextInput input, .stSelectbox > div > div {{
    border-radius:8px !important;
    border:1px solid {C["border2"]} !important;
    background:{C["input_bg"]} !important;
    color:{C["text"]} !important;
    font-size:.875rem !important;
}}
.stTextInput input:focus {{
    border-color:{C["accent"]} !important;
    box-shadow:0 0 0 3px rgba(37,99,235,.15) !important;
}}
label {{ color:{C["text2"]} !important; font-size:.82rem !important; }}

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton button {{
    background:{C["accent"]} !important; color:white !important;
    border:none !important; border-radius:8px !important;
    font-size:.82rem !important; font-weight:500 !important;
    padding:9px 20px !important;
}}
.stDownloadButton button:hover {{ background:{C["accent2"]} !important; }}

/* ── EXPORT BOX ── */
.export-box {{
    background:{C["export_bg"]}; border:1px solid {C["border"]};
    border-radius:10px; padding:16px 20px;
    display:flex; align-items:center; justify-content:space-between;
    flex-wrap:wrap; gap:12px; margin-top:14px;
}}
.export-info {{ font-size:.82rem; color:{C["text2"]}; }}
.export-info strong {{ color:{C["text"]}; }}

/* ── EXPANDER ── */
.streamlit-expanderHeader {{
    background:{C["bg2"]} !important; border:1px solid {C["border"]} !important;
    border-radius:10px !important; font-size:.82rem !important;
    color:{C["text2"]} !important; padding:10px 20px !important;
    margin:0 48px 24px 48px !important;
}}
.streamlit-expanderContent {{
    border:1px solid {C["border"]} !important; border-top:none !important;
    border-radius:0 0 10px 10px !important;
    margin:-24px 48px 24px 48px !important; padding:20px !important;
    background:{C["bg2"]} !important;
}}

/* ── RADIO ── */
.stRadio label {{ font-size:.875rem !important; color:{C["text2"]} !important; }}

/* ══ RESPONSIVO — MOBILE ════════════════════════════════════════════════════ */
@media (max-width: 768px) {{
    .topbar {{ padding: 0 16px; height: 56px; }}
    .topbar-sub {{ display: none; }}
    .topbar-date {{ display: none; }}
    .stTabs {{ padding: 0 12px; }}
    .stTabs [data-baseweb="tab"] {{ padding: 12px 12px; font-size:.8rem; }}
    .streamlit-expanderHeader {{ margin: 0 12px 16px 12px !important; }}
    .streamlit-expanderContent {{ margin: -16px 12px 16px 12px !important; }}
    .kpi-row {{ grid-template-columns: repeat(2,1fr); gap:10px; }}
    .kpi {{ padding: 14px 16px; }}
    .kpi-value {{ font-size:1.6rem; }}
    .today-grid {{ grid-template-columns: 1fr; }}
    .panel {{ padding: 16px; }}
    .pyr-lbl {{ width: 100px; font-size:.65rem; }}
    .eng-lbl  {{ width: 90px; font-size:.72rem; }}
    .gtable th, .gtable td {{ padding: 9px 10px; font-size:.8rem; }}
    .mtable th, .mtable td {{ padding: 10px 10px; font-size:.8rem; }}
    .mini-grid {{ grid-template-columns: repeat(2,1fr); }}
    .urgency-banner {{ padding: 18px 20px; }}
    .urgency-title {{ font-size:1.1rem; }}
    .season-lbl {{ font-size:.55rem; }}
    .topbar-monogram {{ width:30px; height:30px; font-size:11px; }}
    .topbar-name {{ font-size:.88rem; }}
}}

@media (max-width: 480px) {{
    .kpi-row {{ grid-template-columns: 1fr 1fr; }}
    .pyr-row {{ flex-wrap: nowrap; }}
    .export-box {{ flex-direction: column; align-items: flex-start; }}
}}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS / ETL
# ══════════════════════════════════════════════════════════════════════════════
ORDEM_FAIXA = ["Crianças (0–12)", "Jovens (13–17)", "Jovens adultos (18–29)", "Adultos (30–59)", "Idosos (60+)"]
MESES_PT    = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
MESES_FULL  = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
               "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]

def parse_data(val):
    try:    return pd.to_datetime(val, dayfirst=True)
    except: return pd.NaT

def calcular_idade(dt):
    if pd.isna(dt): return None
    h = date.today()
    return h.year - dt.year - ((h.month, h.day) < (dt.month, dt.day))

def faixa_etaria(idade):
    if idade is None:  return "Não informado"
    if idade < 13:     return "Crianças (0–12)"
    if idade < 18:     return "Jovens (13–17)"
    if idade < 30:     return "Jovens adultos (18–29)"
    if idade < 60:     return "Adultos (30–59)"
    return "Idosos (60+)"

def dias_para_aniversario(dt):
    if pd.isna(dt): return None
    hoje = date.today()
    prox = dt.replace(year=hoje.year).date()
    if prox < hoje:
        prox = dt.replace(year=hoje.year + 1).date()
    return (prox - hoje).days

def iniciais(nome: str) -> str:
    p = str(nome).strip().split()
    return (p[0][0] + p[-1][0]).upper() if len(p) >= 2 else str(nome)[:2].upper()

@st.cache_data
def carregar_padrao():
    return pd.read_csv("dados_membros.csv", encoding="utf-8-sig")

@st.cache_data(ttl=300)
def carregar_sheets(url: str) -> pd.DataFrame:
    import requests
    url = url.strip()
    if "/pub" in url and "output=csv" in url:
        csv_url = url
    elif "/d/" in url and "/e/" not in url:
        sid = url.split("/d/")[1].split("/")[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{sid}/export?format=csv"
    else:
        csv_url = url
    resp = requests.get(csv_url, headers={"User-Agent": "Mozilla/5.0"}, allow_redirects=True, timeout=15)
    resp.raise_for_status()
    return pd.read_csv(StringIO(resp.text))

def etl(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]
    for col in ["Email", "Carimbo de data/hora", "Timestamp"]:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)
    for col, fn in [("Nome Completo", str.title), ("Bairro", str.title)]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().apply(fn)
    for col in ["Membro Ativo", "Gênero"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.capitalize()
    df["_dt"]        = df["Data de Nascimento"].apply(parse_data)
    df["Idade"]      = df["_dt"].apply(calcular_idade)
    df["Faixa Etária"] = df["Idade"].apply(faixa_etaria)
    df["_mes"]       = df["_dt"].dt.month
    df["_dia"]       = df["_dt"].dt.day
    df["_dias_aniv"] = df["_dt"].apply(dias_para_aniversario)
    df["_iniciais"]  = df["Nome Completo"].apply(iniciais)
    return df


# ══════════════════════════════════════════════════════════════════════════════
# TOPBAR + BOTÃO DE TEMA
# ══════════════════════════════════════════════════════════════════════════════
hoje = date.today()
hoje_mes_nome = MESES_FULL[hoje.month - 1]

col_top, col_btn = st.columns([10, 1])
with col_top:
    st.markdown(f"""
    <div class="topbar">
        <div class="topbar-brand">
            <div class="topbar-monogram">IBP</div>
            <div>
                <div class="topbar-name">Igreja Batista de Pindorama</div>
                <div class="topbar-sub">Painel de Gestão de Membros</div>
            </div>
        </div>
        <div class="topbar-right">
            <div class="topbar-date">{hoje.strftime("%d de %B de %Y")}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_btn:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button(THEME_ICON, help=THEME_LABEL, key="theme_toggle"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# FONTE DE DADOS
# ══════════════════════════════════════════════════════════════════════════════
with st.expander("Configurar fonte de dados", expanded=False):
    fonte = st.radio(
        "Fonte", ["Dados de demonstração", "Google Sheets (tempo real)", "Upload de CSV"],
        horizontal=True, label_visibility="collapsed",
    )
    df_raw = None
    if fonte == "Google Sheets (tempo real)":
        st.markdown(f"""
        <div style="background:{'#1e3a5f' if dark else '#eff6ff'};border:1px solid {'#1e40af' if dark else '#bfdbfe'};
        border-radius:8px;padding:12px 16px;font-size:.82rem;color:{'#93c5fd' if dark else '#1e40af'};line-height:1.6;margin-bottom:10px">
        <strong>Como conectar:</strong> Na planilha vinculada ao Forms, acesse
        <em>Arquivo &rarr; Compartilhar &rarr; Publicar na web</em>,
        selecione a aba, formato CSV, clique em Publicar e cole o link abaixo.
        Os dados atualizam automaticamente a cada 5 minutos.
        </div>""", unsafe_allow_html=True)
        url = st.text_input("Link", placeholder="https://docs.google.com/spreadsheets/d/...", label_visibility="collapsed")
        if url:
            try:
                df_raw = carregar_sheets(url)
                st.success(f"{len(df_raw)} registros carregados.")
            except Exception as e:
                st.error(f"Erro: {e}")
    elif fonte == "Upload de CSV":
        up = st.file_uploader("CSV do Google Forms", type=["csv"], label_visibility="collapsed")
        if up:
            df_raw = pd.read_csv(up, encoding="utf-8-sig")
            st.success(f"{len(df_raw)} registros carregados.")
    if df_raw is None:
        df_raw = carregar_padrao()

df = etl(df_raw)
hoje_mes = hoje.month
hoje_dia  = hoje.day


# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs(["Hoje", "Mês em Curso", "Análise da Congregação", "Membros"])


# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — HOJE
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    total     = len(df)
    ativos    = int((df["Membro Ativo"] == "Sim").sum()) if "Membro Ativo" in df.columns else total
    aniv_hoje = df[df["_dias_aniv"] == 0]
    aniv_7    = df[(df["_dias_aniv"] > 0) & (df["_dias_aniv"] <= 7)].sort_values("_dias_aniv")

    st.markdown(f"""
    <div class="kpi-row">
        <div class="kpi blue">
            <div class="kpi-label">Total de membros</div>
            <div class="kpi-value">{total}</div>
            <div class="kpi-sub">cadastros no sistema</div>
        </div>
        <div class="kpi green">
            <div class="kpi-label">Membros ativos</div>
            <div class="kpi-value">{ativos}</div>
            <div class="kpi-sub">{round(ativos/total*100) if total else 0}% do total</div>
        </div>
        <div class="kpi rose">
            <div class="kpi-label">Aniversariantes hoje</div>
            <div class="kpi-value">{len(aniv_hoje)}</div>
            <div class="kpi-sub">{hoje.strftime("%d de %B")}</div>
        </div>
        <div class="kpi amber">
            <div class="kpi-label">Próximos 7 dias</div>
            <div class="kpi-value">{len(aniv_7)}</div>
            <div class="kpi-sub">aniversariantes chegando</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Banner
    if len(aniv_hoje) == 0:
        st.markdown(f"""
        <div class="urgency-banner">
            <div>
                <div class="urgency-title">Nenhum aniversariante hoje</div>
                <div class="urgency-sub">{hoje.strftime("%A, %d de %B de %Y").capitalize()}</div>
            </div>
            <div class="urgency-empty">Confira os próximos 7 dias abaixo.</div>
        </div>""", unsafe_allow_html=True)
    else:
        cards = "".join(f"""
        <div class="today-card">
            <div class="avatar" style="width:44px;height:44px;font-size:.95rem">{r["_iniciais"]}</div>
            <div>
                <div class="today-name">{r.get("Nome Completo","—")}</div>
                <div class="today-detail">{r.get("Idade","—")} anos &middot; {r.get("Bairro","—")}</div>
                <div class="today-phone">{r.get("Telefone","—")}</div>
            </div>
        </div>""" for _, r in aniv_hoje.iterrows())
        st.markdown(f"""
        <div class="urgency-banner">
            <div>
                <div class="urgency-title">{"Feliz Aniversário!" if len(aniv_hoje)==1 else f"{len(aniv_hoje)} Aniversariantes Hoje!"}</div>
                <div class="urgency-sub">{hoje.strftime("%A, %d de %B de %Y").capitalize()}</div>
            </div>
        </div>
        <div class="today-grid">{cards}</div>""", unsafe_allow_html=True)

    # Próximos 7 dias
    st.markdown(f'<div class="panel"><div class="panel-title">Próximos 7 dias <span>— prepare as celebrações</span></div>', unsafe_allow_html=True)
    if aniv_7.empty:
        st.markdown(f'<p style="color:{C["text3"]};font-size:.88rem">Nenhum aniversariante nos próximos 7 dias.</p>', unsafe_allow_html=True)
    else:
        rows = ""
        for _, r in aniv_7.iterrows():
            dias  = int(r["_dias_aniv"])
            dt_fmt= (hoje + timedelta(days=dias)).strftime("%d/%m")
            if dias == 1:   cls, txt = "badge-today", "Amanhã"
            elif dias <= 3: cls, txt = "badge-today", f"Em {dias} dias"
            else:           cls, txt = "badge-soon",  f"Em {dias} dias"
            rows += f"""
            <tr>
                <td><span class="badge {cls}">{txt}</span></td>
                <td>
                    <div style="display:flex;align-items:center;gap:10px">
                        <div class="avatar" style="width:32px;height:32px;font-size:.75rem">{r["_iniciais"]}</div>
                        <div><div class="gt-name">{r.get("Nome Completo","—")}</div><div class="gt-sub">{r.get("Bairro","—")}</div></div>
                    </div>
                </td>
                <td style="color:{C["text2"]};font-size:.82rem">{dt_fmt} &mdash; {r.get("Idade","—")} anos</td>
                <td><span class="gt-phone">{r.get("Telefone","—")}</span></td>
            </tr>"""
        st.markdown(f"""
        <div style="overflow-x:auto">
        <table class="gtable">
            <thead><tr><th>Quando</th><th>Membro</th><th>Data / Idade</th><th>Telefone</th></tr></thead>
            <tbody>{rows}</tbody>
        </table></div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — MÊS EM CURSO
# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    aniv_mes = df[df["_mes"] == hoje_mes].sort_values("_dia")
    passados = aniv_mes[aniv_mes["_dia"] < hoje_dia]
    futuros  = aniv_mes[aniv_mes["_dia"] >= hoje_dia]

    col_cal, col_info = st.columns([1.3, 1])

    with col_cal:
        st.markdown(f'<div class="panel"><div class="panel-title">Calendário de {hoje_mes_nome}</div>', unsafe_allow_html=True)
        cal_matrix  = calendar.monthcalendar(hoje.year, hoje_mes)
        bday_dias   = set(aniv_mes["_dia"].tolist())
        dias_semana = ["Seg","Ter","Qua","Qui","Sex","Sáb","Dom"]
        hdr  = "".join(f'<div class="cal-hdr">{d}</div>' for d in dias_semana)
        cells = ""
        for week in cal_matrix:
            for d in week:
                if d == 0:
                    cells += '<div class="cal-day cal-empty"></div>'
                elif d == hoje_dia:
                    dot    = '<div class="cal-dot"></div>' if d in bday_dias else ""
                    cells += f'<div class="cal-day cal-today">{d}{dot}</div>'
                elif d in bday_dias:
                    cells += f'<div class="cal-day cal-bday">{d}<div class="cal-dot"></div></div>'
                else:
                    cells += f'<div class="cal-day cal-normal">{d}</div>'
        st.markdown(f"""
        <div class="cal-grid">{hdr}{cells}</div>
        <div style="display:flex;gap:16px;margin-top:14px;font-size:.72rem;color:{C["text3"]}">
            <span style="display:flex;align-items:center;gap:5px">
                <span style="width:10px;height:10px;background:{C["cal_bday"]};border-radius:3px;display:inline-block"></span>Aniversário
            </span>
            <span style="display:flex;align-items:center;gap:5px">
                <span style="width:10px;height:10px;background:{C["accent"]};border-radius:3px;display:inline-block"></span>Hoje
            </span>
        </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_info:
        st.markdown(f"""
        <div class="panel" style="height:100%">
            <div class="panel-title">Resumo de {hoje_mes_nome}</div>
            <div class="mini-grid">
                <div class="mini-card"><div class="mini-val">{len(aniv_mes)}</div><div class="mini-lbl">Total no mês</div></div>
                <div class="mini-card"><div class="mini-val" style="color:{C["green"]}">{len(futuros)}</div><div class="mini-lbl">Ainda virão</div></div>
                <div class="mini-card"><div class="mini-val" style="color:{C["text3"]}">{len(passados)}</div><div class="mini-lbl">Já passaram</div></div>
                <div class="mini-card"><div class="mini-val">{round(len(aniv_mes)/total*100) if total else 0}%</div><div class="mini-lbl">Da congregação</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

    # Sazonalidade
    st.markdown(f'<div class="panel"><div class="panel-title">Aniversários por Mês <span>— sazonalidade anual</span></div>', unsafe_allow_html=True)
    por_mes = df.groupby("_mes").size().reindex(range(1,13), fill_value=0)
    max_val = por_mes.max() or 1
    bars = "".join(f"""
    <div class="season-col">
        <div class="season-cnt">{cnt}</div>
        <div class="season-bar{'  cur' if m==hoje_mes else ''}" style="height:{int(cnt/max_val*100)}%"></div>
        <div class="season-lbl">{MESES_PT[m-1]}</div>
    </div>""" for m, cnt in por_mes.items())
    st.markdown(f'<div class="season-wrap">{bars}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    def bday_table(df_sub, titulo):
        if df_sub.empty:
            return f'<div class="panel"><div class="panel-title">{titulo}</div><p style="color:{C["text3"]};font-size:.85rem">Nenhum registro.</p></div>'
        rows = "".join(f"""
        <tr>
            <td style="color:{C["text3"]};font-size:.8rem">{r["_dia"]:02d}/{hoje_mes:02d}</td>
            <td>
                <div style="display:flex;align-items:center;gap:9px">
                    <div class="avatar" style="width:30px;height:30px;font-size:.72rem">{r["_iniciais"]}</div>
                    <div><div class="gt-name">{r.get("Nome Completo","—")}</div><div class="gt-sub">{r.get("Bairro","—")}</div></div>
                </div>
            </td>
            <td style="color:{C["text2"]};font-size:.8rem">{r.get("Idade","—")} anos</td>
            <td><span class="gt-phone">{r.get("Telefone","—")}</span></td>
        </tr>""" for _, r in df_sub.iterrows())
        return f"""<div class="panel"><div class="panel-title">{titulo} <span>({len(df_sub)})</span></div>
        <div style="overflow-x:auto"><table class="gtable">
            <thead><tr><th>Data</th><th>Membro</th><th>Idade</th><th>Telefone</th></tr></thead>
            <tbody>{rows}</tbody>
        </table></div></div>"""

    c1, c2 = st.columns(2)
    with c1: st.markdown(bday_table(futuros, "Ainda virão este mês"), unsafe_allow_html=True)
    with c2: st.markdown(bday_table(passados, "Já passaram este mês"), unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — ANÁLISE DA CONGREGAÇÃO
# ════════════════════════════════════════════════════════════════════════════════
with tab3:

    col_pir, col_eng = st.columns([1.2, 1])

    with col_pir:
        st.markdown(f'<div class="panel"><div class="panel-title">Pirâmide Etária <span>— masculino vs feminino</span></div>', unsafe_allow_html=True)
        if "Gênero" in df.columns:
            masc = df[df["Gênero"].str.lower() == "masculino"]
            fem  = df[df["Gênero"].str.lower() == "feminino"]
            mf   = masc["Faixa Etária"].value_counts().reindex(ORDEM_FAIXA, fill_value=0)
            ff   = fem["Faixa Etária"].value_counts().reindex(ORDEM_FAIXA, fill_value=0)
            mp   = max(mf.max(), ff.max(), 1)
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;font-size:.72rem;font-weight:600;margin-bottom:10px">
                <span style="color:{C["accent"]}">Masculino</span>
                <span style="color:{C["rose"]}">Feminino</span>
            </div>""", unsafe_allow_html=True)
            for faixa in reversed(ORDEM_FAIXA):
                mv = mf.get(faixa, 0); fv = ff.get(faixa, 0)
                mw = int(mv/mp*100);   fw = int(fv/mp*100)
                st.markdown(f"""
                <div class="pyr-row">
                    <div class="pyr-val">{mv}</div>
                    <div style="flex:1;display:flex;justify-content:flex-end">
                        <div class="pyr-m" style="width:{mw}px"></div>
                    </div>
                    <div class="pyr-sep"></div>
                    <div class="pyr-lbl" style="width:140px;text-align:center">{faixa}</div>
                    <div class="pyr-sep"></div>
                    <div style="flex:1">
                        <div class="pyr-f" style="width:{fw}px"></div>
                    </div>
                    <div class="pyr-val">{fv}</div>
                </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_eng:
        st.markdown(f'<div class="panel"><div class="panel-title">Engajamento por Bairro <span>— % de ativos</span></div>', unsafe_allow_html=True)
        if "Membro Ativo" in df.columns:
            eng = (
                df.groupby("Bairro")
                  .agg(total=("Membro Ativo","count"),
                       ativos=("Membro Ativo", lambda x: (x=="Sim").sum()))
                  .assign(pct=lambda d: (d["ativos"]/d["total"]*100).round(1))
                  .sort_values("pct", ascending=False)
            )
            for bairro, row in eng.iterrows():
                pct = row["pct"]
                cor = C["green"] if pct >= 80 else (C["amber"] if pct >= 60 else C["rose"])
                st.markdown(f"""
                <div class="eng-row">
                    <div class="eng-lbl" title="{bairro}">{bairro}</div>
                    <div class="eng-bg">
                        <div class="eng-fill" style="width:{pct}%;background:{cor}"></div>
                    </div>
                    <div class="eng-pct">{pct:.0f}%</div>
                </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    def grafico_stacked(titulo, df_cross, col_a, col_b, lbl_a, lbl_b, cor_a, cor_b):
        linhas = ""
        for faixa in ORDEM_FAIXA:
            va = int(df_cross[col_a].get(faixa, 0)) if col_a in df_cross.columns else 0
            vb = int(df_cross[col_b].get(faixa, 0)) if col_b in df_cross.columns else 0
            total_row = va + vb or 1
            pct_a = round(va / total_row * 100)
            pct_b = 100 - pct_a
            lbl_curta = faixa.split("(")[0].strip()
            r_a = "6px 0 0 6px" if pct_b > 0 else "6px"
            r_b = "0 6px 6px 0" if pct_a > 0 else "6px"
            seg_a = (f'<div style="width:{pct_a}%;background:{cor_a};height:100%;'
                     f'display:flex;align-items:center;justify-content:center;'
                     f'font-size:.68rem;font-weight:700;color:white;'
                     f'border-radius:{r_a};overflow:hidden">'
                     f'{"&nbsp;"+str(va) if pct_a >= 14 else ""}'
                     f'</div>') if pct_a > 0 else ""
            seg_b = (f'<div style="width:{pct_b}%;background:{cor_b};height:100%;'
                     f'display:flex;align-items:center;justify-content:center;'
                     f'font-size:.68rem;font-weight:700;color:white;'
                     f'border-radius:{r_b};overflow:hidden">'
                     f'{"&nbsp;"+str(vb) if pct_b >= 14 else ""}'
                     f'</div>') if pct_b > 0 else ""
            linhas += (
                f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:10px">'
                f'<div style="width:130px;font-size:.75rem;color:{C["text2"]};'
                f'flex-shrink:0;text-align:right;line-height:1.2">{lbl_curta}</div>'
                f'<div style="flex:1;height:26px;border-radius:6px;'
                f'background:{C["eng_bg"]};overflow:hidden;display:flex">'
                f'{seg_a}{seg_b}</div>'
                f'<div style="width:52px;font-size:.7rem;color:{C["text3"]};'
                f'flex-shrink:0;text-align:right">{va}&thinsp;/&thinsp;{vb}</div>'
                f'</div>'
            )
        legenda = (
            f'<div style="display:flex;gap:20px;margin-top:14px;padding-top:12px;'
            f'border-top:1px solid {C["border"]};flex-wrap:wrap">'
            f'<span style="display:flex;align-items:center;gap:6px">'
            f'<span style="width:12px;height:12px;background:{cor_a};border-radius:3px;display:inline-block"></span>'
            f'<span style="font-size:.75rem;color:{C["text2"]};font-weight:500">{lbl_a}</span></span>'
            f'<span style="display:flex;align-items:center;gap:6px">'
            f'<span style="width:12px;height:12px;background:{cor_b};border-radius:3px;display:inline-block"></span>'
            f'<span style="font-size:.75rem;color:{C["text2"]};font-weight:500">{lbl_b}</span></span>'
            f'</div>'
        )
        return f'<div class="panel"><div class="panel-title">{titulo}</div>{linhas}{legenda}</div>'

    col_fe, col_gf = st.columns(2)
    with col_fe:
        if "Membro Ativo" in df.columns:
            cross = (df.groupby(["Faixa Etária","Membro Ativo"]).size()
                       .unstack(fill_value=0).reindex(ORDEM_FAIXA).fillna(0))
            st.markdown(grafico_stacked(
                "Ativos vs Inativos por Faixa Etária",
                cross, "Sim", "Não", "Ativos", "Inativos",
                C["green"], C["rose"]
            ), unsafe_allow_html=True)

    with col_gf:
        if "Gênero" in df.columns:
            gf = (df.groupby(["Faixa Etária","Gênero"]).size()
                    .unstack(fill_value=0).reindex(ORDEM_FAIXA).fillna(0))
            fem_col  = "Feminino"  if "Feminino"  in gf.columns else gf.columns[0]
            masc_col = "Masculino" if "Masculino" in gf.columns else (gf.columns[1] if len(gf.columns) > 1 else gf.columns[0])
            st.markdown(grafico_stacked(
                "Gênero por Faixa Etária",
                gf, fem_col, masc_col, "Feminino", "Masculino",
                C["rose"], C["accent"]
            ), unsafe_allow_html=True)

    # Indicadores demográficos
    id_med = round(df["Idade"].dropna().mean(), 1) if df["Idade"].dropna().any() else "—"
    id_min = int(df["Idade"].dropna().min())       if df["Idade"].dropna().any() else "—"
    id_max = int(df["Idade"].dropna().max())       if df["Idade"].dropna().any() else "—"
    adultos     = len(df[df["Faixa Etária"].isin(["Jovens adultos (18–29)","Adultos (30–59)"])])
    dependentes = len(df[df["Faixa Etária"].isin(["Crianças (0–12)","Idosos (60+)"])])
    razao       = round(dependentes/adultos, 2) if adultos else "—"

    st.markdown(f"""
    <div class="panel">
        <div class="panel-title">Indicadores Demográficos</div>
        <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:14px">
            {"".join(f'''<div style="text-align:center;padding:12px;background:{C["bg3"]};border-radius:10px;border:1px solid {C["border"]}">
                <div style="font-family:'Lora',serif;font-size:1.5rem;color:{C["text"]}">{val}</div>
                <div style="font-size:.67rem;color:{C["text3"]};text-transform:uppercase;letter-spacing:.06em;margin-top:4px">{lbl}</div>
            </div>''' for val, lbl in [(id_med,"Idade média"),(id_min,"Mais jovem"),(id_max,"Mais velho"),(adultos,"Adultos"),(razao,"Razão depend.")])}
        </div>
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 — MEMBROS
# ════════════════════════════════════════════════════════════════════════════════
with tab4:
    f1, f2, f3, f4 = st.columns([2.5,1.5,1.8,1.2])
    with f1: busca      = st.text_input("Buscar por nome", placeholder="Digite o nome do membro...")
    with f2:
        b_opts     = ["Todos os bairros"] + sorted(df["Bairro"].dropna().unique().tolist())
        bairro_sel = st.selectbox("Bairro", b_opts)
    with f3:
        fx_opts   = ["Todas as faixas"] + ORDEM_FAIXA
        faixa_sel = st.selectbox("Faixa etária", fx_opts)
    with f4:
        st_opts    = ["Todos"] + (["Ativos","Inativos"] if "Membro Ativo" in df.columns else [])
        status_sel = st.selectbox("Status", st_opts)

    df_f = df.copy()
    if busca: df_f = df_f[df_f["Nome Completo"].str.lower().str.contains(busca.lower(), na=False)]
    if bairro_sel != "Todos os bairros": df_f = df_f[df_f["Bairro"] == bairro_sel]
    if faixa_sel  != "Todas as faixas":  df_f = df_f[df_f["Faixa Etária"] == faixa_sel]
    if status_sel == "Ativos"   and "Membro Ativo" in df_f.columns: df_f = df_f[df_f["Membro Ativo"] == "Sim"]
    elif status_sel == "Inativos" and "Membro Ativo" in df_f.columns: df_f = df_f[df_f["Membro Ativo"] == "Não"]

    st.markdown(f'<div class="panel"><div class="panel-title">Lista de Membros <span>— {len(df_f)} resultado(s)</span></div>', unsafe_allow_html=True)
    rows = ""
    for _, r in df_f.iterrows():
        ativo = r.get("Membro Ativo","—")
        pill  = (f'<span class="pill pill-sim">Ativo</span>'   if str(ativo)=="Sim" else
                 f'<span class="pill pill-nao">Inativo</span>' if str(ativo)=="Não" else "—")
        da    = r.get("_dias_aniv", None)
        extra = ""
        if da is not None:
            if da == 0:   extra = f'&nbsp;<span class="badge badge-today">Hoje!</span>'
            elif da <= 7: extra = f'&nbsp;<span class="badge badge-soon">Em {da}d</span>'
        rows += f"""
        <tr>
            <td>
                <div style="display:flex;align-items:center;gap:10px">
                    <div class="avatar" style="width:32px;height:32px;font-size:.75rem">{r["_iniciais"]}</div>
                    <div><div class="mt-name">{r.get("Nome Completo","—")}{extra}</div><div class="mt-sub">{r.get("Bairro","—")}</div></div>
                </div>
            </td>
            <td style="color:{C["text2"]};font-size:.82rem">{r.get("Data de Nascimento","—")}</td>
            <td>
                <div style="color:{C["text"]};font-size:.875rem">{r.get("Idade","—")} anos</div>
                <div class="mt-sub">{r.get("Faixa Etária","—")}</div>
            </td>
            <td style="color:{C["text2"]};font-size:.82rem">{r.get("Gênero","—")}</td>
            <td style="color:{C["accent"]};font-size:.82rem;font-weight:500">{r.get("Telefone","—")}</td>
            <td>{pill}</td>
        </tr>"""
    st.markdown(f"""
    <div style="overflow-x:auto">
    <table class="mtable">
        <thead><tr>
            <th>Membro</th><th>Nascimento</th><th>Idade / Faixa</th>
            <th>Genero</th><th>Telefone</th><th>Status</th>
        </tr></thead>
        <tbody>{rows}</tbody>
    </table></div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    COLS = ["Nome Completo","Data de Nascimento","Idade","Faixa Etária","Gênero","Bairro","Telefone","Membro Ativo"]
    cols_ok   = [c for c in COLS if c in df_f.columns]
    csv_bytes = df_f[cols_ok].to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.markdown(f"""
    <div class="export-box">
        <div class="export-info">
            <strong>{len(df_f)} membros</strong> prontos para exportação com os filtros aplicados.
            O arquivo é compatível com Excel e Google Sheets.
        </div>
    </div>""", unsafe_allow_html=True)
    st.download_button("Baixar lista em CSV", data=csv_bytes,
                       file_name=f"membros_ibp_{hoje.strftime('%Y%m%d')}.csv", mime="text/csv")

