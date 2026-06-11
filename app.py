import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
from io import StringIO

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURAÇÃO
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Igreja Batista de Pindorama",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Lora:wght@600;700&display=swap');

*, html, body, [class*="css"] { font-family: 'Inter', sans-serif; box-sizing: border-box; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="collapsedControl"] { display: none; }
section[data-testid="stSidebar"] { display: none; }
.block-container { padding: 0 0 4rem 0 !important; max-width: 100% !important; }

/* ── TOPBAR ── */
.topbar {
    background: #0f172a;
    padding: 0 48px;
    display: flex; align-items: center; justify-content: space-between;
    height: 64px;
    border-bottom: 1px solid #1e293b;
}
.topbar-brand { display: flex; align-items: center; gap: 14px; }
.topbar-monogram {
    width: 36px; height: 36px; background: #2563eb;
    border-radius: 8px; display: flex; align-items: center;
    justify-content: center; font-weight: 700; color: white; font-size: 13px;
    letter-spacing: .03em;
}
.topbar-name { font-family: 'Lora', serif; color: #f1f5f9; font-size: 1rem; font-weight: 600; }
.topbar-sub  { color: #475569; font-size: .7rem; text-transform: uppercase; letter-spacing: .07em; }
.topbar-date { color: #475569; font-size: .8rem; }

/* ── TABS ── */
.stTabs { padding: 0 48px; }
.stTabs [data-baseweb="tab-list"] {
    background: transparent; border-bottom: 1px solid #e2e8f0;
    gap: 0; padding: 0; margin-bottom: 32px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent; border: none;
    border-bottom: 2px solid transparent; border-radius: 0;
    padding: 16px 24px; font-size: .85rem; font-weight: 500; color: #64748b;
    margin-bottom: -1px;
}
.stTabs [aria-selected="true"] {
    background: transparent !important; color: #0f172a !important;
    border-bottom: 2px solid #2563eb !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none; }

/* ── PANELS ── */
.panel {
    background: white; border: 1px solid #e2e8f0;
    border-radius: 14px; padding: 24px 26px; margin-bottom: 18px;
}
.panel-title {
    font-size: .72rem; font-weight: 600; color: #94a3b8;
    text-transform: uppercase; letter-spacing: .08em;
    margin-bottom: 18px; padding-bottom: 14px;
    border-bottom: 1px solid #f1f5f9;
}
.panel-title span { color: #94a3b8; font-weight: 400; }

/* ── KPI CARDS ── */
.kpi-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-bottom: 24px; }
.kpi {
    background: white; border: 1px solid #e2e8f0;
    border-radius: 14px; padding: 22px 24px;
    border-top: 3px solid #e2e8f0;
}
.kpi.blue  { border-top-color: #2563eb; }
.kpi.green { border-top-color: #059669; }
.kpi.amber { border-top-color: #d97706; }
.kpi.rose  { border-top-color: #db2777; }
.kpi-label { font-size:.7rem; font-weight:600; color:#94a3b8; text-transform:uppercase; letter-spacing:.08em; margin-bottom:10px; }
.kpi-value { font-family:'Lora',serif; font-size:2.1rem; color:#0f172a; line-height:1; margin-bottom:5px; }
.kpi-sub   { font-size:.75rem; color:#94a3b8; }

/* ── URGENCY BANNER ── */
.urgency-banner {
    background: linear-gradient(135deg, #1e3a8a 0%, #1d4ed8 100%);
    border-radius: 14px; padding: 28px 32px; margin-bottom: 24px;
    display: flex; align-items: center; justify-content: space-between;
}
.urgency-title { font-family:'Lora',serif; color:white; font-size:1.5rem; margin-bottom:4px; }
.urgency-sub { color: #93c5fd; font-size:.85rem; }
.urgency-empty { color: #bfdbfe; font-size:.9rem; font-style:italic; }

/* ── TODAY CARDS ── */
.today-grid { display:grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap:14px; }
.today-card {
    background: white; border-radius: 12px; padding: 18px 20px;
    display: flex; align-items: center; gap: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,.06), 0 4px 16px rgba(0,0,0,.04);
}
.today-avatar {
    width: 46px; height: 46px; border-radius: 50%;
    background: #dbeafe; color: #1d4ed8;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 1rem; flex-shrink: 0;
}
.today-name  { font-weight:600; color:#0f172a; font-size:.95rem; }
.today-detail{ color:#64748b; font-size:.8rem; margin-top:2px; }
.today-phone { color:#2563eb; font-size:.8rem; font-weight:500; margin-top:4px; }

/* ── WEEK TABLE ── */
.week-table { width:100%; border-collapse:collapse; }
.week-table th {
    text-align:left; font-size:.68rem; font-weight:600; color:#94a3b8;
    text-transform:uppercase; letter-spacing:.08em;
    padding:0 14px 10px; border-bottom:1px solid #f1f5f9;
}
.week-table td { padding:11px 14px; border-bottom:1px solid #f8fafc; vertical-align:middle; }
.week-table tr:last-child td { border-bottom:none; }
.week-table tr:hover td { background:#fafafa; }
.wt-name  { font-weight:500; color:#0f172a; font-size:.875rem; }
.wt-sub   { color:#94a3b8; font-size:.75rem; margin-top:1px; }
.wt-phone { color:#2563eb; font-size:.82rem; font-weight:500; }
.days-badge {
    display:inline-block; padding:3px 12px; border-radius:99px;
    font-size:.72rem; font-weight:700;
}
.days-1  { background:#fef9c3; color:#854d0e; }
.days-3  { background:#dbeafe; color:#1e40af; }
.days-7  { background:#f0fdf4; color:#166534; }

/* ── CALENDAR GRID ── */
.cal-grid {
    display:grid; grid-template-columns: repeat(7,1fr);
    gap:4px; margin-top:8px;
}
.cal-header { text-align:center; font-size:.68rem; font-weight:600; color:#94a3b8; padding:4px 0 8px; text-transform:uppercase; }
.cal-day {
    aspect-ratio:1; border-radius:8px; display:flex;
    flex-direction:column; align-items:center; justify-content:center;
    font-size:.8rem; position:relative; cursor:default;
}
.cal-day.empty   { background:transparent; }
.cal-day.normal  { background:#f8fafc; color:#64748b; }
.cal-day.has-bday{ background:#dbeafe; color:#1e40af; font-weight:600; }
.cal-day.today   { background:#2563eb; color:white; font-weight:700; }
.cal-dot { width:5px; height:5px; background:#2563eb; border-radius:50%; margin-top:2px; }
.cal-day.today .cal-dot { background:white; }

/* ── PYRAMID ── */
.pyramid-row { display:flex; align-items:center; gap:10px; margin-bottom:8px; }
.pyramid-label { width:150px; font-size:.78rem; color:#475569; text-align:right; flex-shrink:0; }
.pyramid-bar-left  { height:22px; background:#2563eb; border-radius:4px 0 0 4px; transition:.3s; }
.pyramid-bar-right { height:22px; background:#db2777; border-radius:0 4px 4px 0; transition:.3s; }
.pyramid-center { width:2px; background:#e2e8f0; height:22px; flex-shrink:0; }
.pyramid-val { font-size:.72rem; color:#94a3b8; width:32px; flex-shrink:0; }

/* ── ENGAGEMENT ── */
.eng-row { display:flex; align-items:center; gap:12px; margin-bottom:10px; }
.eng-label { width:130px; font-size:.8rem; color:#475569; flex-shrink:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.eng-bar-bg { flex:1; height:10px; background:#f1f5f9; border-radius:99px; overflow:hidden; }
.eng-bar-fill { height:100%; border-radius:99px; background:#059669; }
.eng-bar-fill.low { background:#ef4444; }
.eng-bar-fill.mid { background:#d97706; }
.eng-pct { font-size:.75rem; font-weight:600; color:#475569; width:36px; text-align:right; flex-shrink:0; }

/* ── SEASON CHART ── */
.season-row { display:flex; align-items:flex-end; gap:6px; height:80px; margin-top:8px; }
.season-bar-wrap { display:flex; flex-direction:column; align-items:center; flex:1; height:100%; justify-content:flex-end; gap:4px; }
.season-bar { width:100%; background:#dbeafe; border-radius:4px 4px 0 0; min-height:4px; }
.season-bar.current { background:#2563eb; }
.season-label { font-size:.62rem; color:#94a3b8; }
.season-count { font-size:.68rem; font-weight:600; color:#475569; }

/* ── MEMBER TABLE ── */
.mtable { width:100%; border-collapse:collapse; font-size:.875rem; }
.mtable th {
    text-align:left; font-size:.68rem; font-weight:600; color:#94a3b8;
    text-transform:uppercase; letter-spacing:.08em;
    padding:0 16px 10px; border-bottom:1px solid #e2e8f0;
}
.mtable td { padding:12px 16px; border-bottom:1px solid #f8fafc; vertical-align:middle; }
.mtable tr:last-child td { border-bottom:none; }
.mtable tr:hover td { background:#fafafa; }
.mt-name  { font-weight:500; color:#0f172a; }
.mt-sub   { color:#94a3b8; font-size:.75rem; margin-top:1px; }
.pill { display:inline-block; padding:2px 10px; border-radius:99px; font-size:.72rem; font-weight:600; }
.pill-sim { background:#d1fae5; color:#065f46; }
.pill-nao { background:#fee2e2; color:#991b1b; }

/* ── EXPANDER FONTE ── */
.streamlit-expanderHeader {
    background:#f8fafc !important; border:1px solid #e2e8f0 !important;
    border-radius:10px !important; font-size:.82rem !important;
    color:#475569 !important; padding:10px 20px !important;
    margin:0 48px 28px 48px !important;
}
.streamlit-expanderContent {
    border:1px solid #e2e8f0 !important; border-top:none !important;
    border-radius:0 0 10px 10px !important;
    margin:-28px 48px 28px 48px !important; padding:20px !important;
}

/* Inputs */
.stTextInput input, .stSelectbox > div > div {
    border-radius:8px !important; border:1px solid #d1d5db !important; font-size:.875rem !important;
}
.stTextInput input:focus { border-color:#2563eb !important; box-shadow:0 0 0 3px rgba(37,99,235,.1) !important; }

/* Download button */
.stDownloadButton button {
    background:#2563eb !important; color:white !important; border:none !important;
    border-radius:8px !important; font-size:.82rem !important; font-weight:500 !important; padding:9px 20px !important;
}
.stDownloadButton button:hover { background:#1d4ed8 !important; }
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
    """Dias até o próximo aniversário a partir de hoje."""
    if pd.isna(dt): return None
    hoje = date.today()
    prox = dt.replace(year=hoje.year).date()
    if prox < hoje:
        prox = dt.replace(year=hoje.year + 1).date()
    return (prox - hoje).days

def iniciais(nome: str) -> str:
    partes = nome.strip().split()
    if len(partes) >= 2:
        return (partes[0][0] + partes[-1][0]).upper()
    return nome[:2].upper()

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
    resp = requests.get(csv_url, headers={"User-Agent":"Mozilla/5.0"}, allow_redirects=True, timeout=15)
    resp.raise_for_status()
    return pd.read_csv(StringIO(resp.text))

def etl(df: pd.DataFrame) -> pd.DataFrame:
    """Pipeline ETL completo com Pandas."""
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]

    # Remove colunas irrelevantes
    for col in ["Email", "Carimbo de data/hora", "Timestamp"]:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)

    # Normaliza strings
    for col, fn in [("Nome Completo", str.title), ("Bairro", str.title)]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().apply(fn)
    for col in ["Membro Ativo", "Gênero"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.capitalize()

    # Parsing de datas
    df["_dt_nasc"] = df["Data de Nascimento"].apply(parse_data)

    # Colunas derivadas via Pandas/NumPy
    df["Idade"]           = df["_dt_nasc"].apply(calcular_idade)
    df["Faixa Etária"]    = df["Idade"].apply(faixa_etaria)
    df["_mes"]            = df["_dt_nasc"].dt.month
    df["_dia"]            = df["_dt_nasc"].dt.day
    df["_dias_aniv"]      = df["_dt_nasc"].apply(dias_para_aniversario)
    df["_iniciais"]       = df["Nome Completo"].apply(iniciais)

    return df


# ══════════════════════════════════════════════════════════════════════════════
# TOPBAR
# ══════════════════════════════════════════════════════════════════════════════
hoje = date.today()
hoje_mes_nome = MESES_FULL[hoje.month - 1]

st.markdown(f"""
<div class="topbar">
    <div class="topbar-brand">
        <div class="topbar-monogram">IBP</div>
        <div>
            <div class="topbar-name">Igreja Batista de Pindorama</div>
            <div class="topbar-sub">Painel de Gestão de Membros</div>
        </div>
    </div>
    <div class="topbar-date">{hoje.strftime("%d de %B de %Y")}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)


# ── Fonte de dados ────────────────────────────────────────────────────────────
with st.expander("Configurar fonte de dados", expanded=False):
    fonte = st.radio("Fonte", ["Dados de demonstração","Google Sheets (tempo real)","Upload de CSV"],
                     horizontal=True, label_visibility="collapsed")
    df_raw = None
    if fonte == "Google Sheets (tempo real)":
        st.markdown("""<div style='background:#eff6ff;border:1px solid #bfdbfe;border-radius:8px;
        padding:12px 16px;font-size:.82rem;color:#1e40af;line-height:1.6'>
        <strong>Como conectar:</strong> Na planilha vinculada ao Forms, acesse
        <em>Arquivo &rarr; Compartilhar &rarr; Publicar na web</em>,
        selecione a aba, formato CSV, clique em Publicar e cole o link abaixo.
        Os dados atualizam automaticamente a cada 5 minutos.</div>""", unsafe_allow_html=True)
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        url = st.text_input("Link da planilha", placeholder="https://docs.google.com/spreadsheets/d/...", label_visibility="collapsed")
        if url:
            try:
                df_raw = carregar_sheets(url)
                st.success(f"{len(df_raw)} registros carregados.")
            except Exception as e:
                st.error(f"Erro: {e}")
    elif fonte == "Upload de CSV":
        up = st.file_uploader("CSV exportado do Google Forms", type=["csv"], label_visibility="collapsed")
        if up:
            df_raw = pd.read_csv(up, encoding="utf-8-sig")
            st.success(f"{len(df_raw)} registros carregados.")
    if df_raw is None:
        df_raw = carregar_padrao()

# Pipeline ETL
df = etl(df_raw)


# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs(["Hoje", "Mês em Curso", "Análise da Congregação", "Membros"])


# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — HOJE
# ════════════════════════════════════════════════════════════════════════════════
with tab1:

    # KPIs rápidos
    total  = len(df)
    ativos = int((df["Membro Ativo"] == "Sim").sum()) if "Membro Ativo" in df.columns else total
    inat   = total - ativos
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

    # Banner de aniversariantes de hoje
    if len(aniv_hoje) == 0:
        st.markdown(f"""
        <div class="urgency-banner">
            <div>
                <div class="urgency-title">Nenhum aniversariante hoje</div>
                <div class="urgency-sub">{hoje.strftime("%A, %d de %B de %Y").capitalize()}</div>
            </div>
            <div class="urgency-empty">Aproveite para preparar as celebrações dos próximos dias.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        cards = ""
        for _, r in aniv_hoje.iterrows():
            nome   = r.get("Nome Completo","—")
            idade  = r.get("Idade","—")
            bairro = r.get("Bairro","—")
            tel    = r.get("Telefone","—")
            ini    = r.get("_iniciais","??")
            cards += f"""
            <div class="today-card">
                <div class="today-avatar">{ini}</div>
                <div>
                    <div class="today-name">{nome}</div>
                    <div class="today-detail">{idade} anos &middot; {bairro}</div>
                    <div class="today-phone">{tel}</div>
                </div>
            </div>"""
        st.markdown(f"""
        <div class="urgency-banner">
            <div>
                <div class="urgency-title">{"Feliz Aniversário!" if len(aniv_hoje)==1 else f"{len(aniv_hoje)} Aniversariantes Hoje!"}</div>
                <div class="urgency-sub">{hoje.strftime("%A, %d de %B de %Y").capitalize()}</div>
            </div>
        </div>
        <div class="today-grid" style="margin-bottom:24px">{cards}</div>
        """, unsafe_allow_html=True)

    # Próximos 7 dias
    st.markdown(f'<div class="panel"><div class="panel-title">Próximos 7 dias <span>— quem está chegando</span></div>', unsafe_allow_html=True)
    if aniv_7.empty:
        st.info("Nenhum aniversariante nos próximos 7 dias.")
    else:
        rows = ""
        for _, r in aniv_7.iterrows():
            dias   = int(r["_dias_aniv"])
            nome   = r.get("Nome Completo","—")
            idade  = r.get("Idade","—")
            bairro = r.get("Bairro","—")
            tel    = r.get("Telefone","—")
            ini    = r.get("_iniciais","??")
            dt_aniv = (hoje + timedelta(days=dias)).strftime("%d/%m")

            if dias == 1:   pill_cls = "days-1"; pill_txt = "Amanhã"
            elif dias <= 3: pill_cls = "days-1"; pill_txt = f"Em {dias} dias"
            else:           pill_cls = "days-7"; pill_txt = f"Em {dias} dias"

            rows += f"""
            <tr>
                <td><span class="days-badge {pill_cls}">{pill_txt}</span></td>
                <td>
                    <div style="display:flex;align-items:center;gap:10px">
                        <div class="today-avatar" style="width:34px;height:34px;font-size:.8rem">{ini}</div>
                        <div>
                            <div class="wt-name">{nome}</div>
                            <div class="wt-sub">{bairro}</div>
                        </div>
                    </div>
                </td>
                <td style="color:#475569;font-size:.85rem">{dt_aniv} &mdash; {idade} anos</td>
                <td><span class="wt-phone">{tel}</span></td>
            </tr>"""
        st.markdown(f"""
        <table class="week-table">
            <thead><tr><th>Quando</th><th>Membro</th><th>Data / Idade</th><th>Telefone</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — MÊS EM CURSO
# ════════════════════════════════════════════════════════════════════════════════
with tab2:

    aniv_mes = df[df["_mes"] == hoje.month].sort_values("_dia").copy()
    passados = aniv_mes[aniv_mes["_dia"] < hoje.day]
    futuros  = aniv_mes[aniv_mes["_dia"] >= hoje.day]

    col_cal, col_info = st.columns([1.2, 1])

    # Calendário visual
    with col_cal:
        st.markdown(f'<div class="panel"><div class="panel-title">Calendário de {hoje_mes_nome}</div>', unsafe_allow_html=True)

        import calendar
        cal = calendar.monthcalendar(hoje.year, hoje.month)
        dias_com_aniv = set(aniv_mes["_dia"].tolist())
        dias_semana   = ["Seg","Ter","Qua","Qui","Sex","Sab","Dom"]

        header_html = "".join(f'<div class="cal-header">{d}</div>' for d in dias_semana)
        cells_html  = ""
        for semana in cal:
            for d in semana:
                if d == 0:
                    cells_html += '<div class="cal-day empty"></div>'
                elif d == hoje.day:
                    dot = '<div class="cal-dot"></div>' if d in dias_com_aniv else ""
                    cells_html += f'<div class="cal-day today">{d}{dot}</div>'
                elif d in dias_com_aniv:
                    cells_html += f'<div class="cal-day has-bday">{d}<div class="cal-dot"></div></div>'
                else:
                    cells_html += f'<div class="cal-day normal">{d}</div>'

        st.markdown(f"""
        <div class="cal-grid">{header_html}{cells_html}</div>
        <div style="display:flex;gap:16px;margin-top:16px;font-size:.75rem;color:#64748b">
            <div style="display:flex;align-items:center;gap:6px"><div style="width:12px;height:12px;background:#dbeafe;border-radius:3px"></div>Aniversário</div>
            <div style="display:flex;align-items:center;gap:6px"><div style="width:12px;height:12px;background:#2563eb;border-radius:3px"></div>Hoje</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Info do mês
    with col_info:
        st.markdown(f"""
        <div class="panel" style="height:100%">
            <div class="panel-title">Resumo de {hoje_mes_nome}</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:20px">
                <div style="background:#f8fafc;border-radius:10px;padding:16px;text-align:center">
                    <div style="font-size:1.8rem;font-family:'Lora',serif;color:#0f172a">{len(aniv_mes)}</div>
                    <div style="font-size:.72rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em;margin-top:3px">Total no mês</div>
                </div>
                <div style="background:#f8fafc;border-radius:10px;padding:16px;text-align:center">
                    <div style="font-size:1.8rem;font-family:'Lora',serif;color:#059669">{len(futuros)}</div>
                    <div style="font-size:.72rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em;margin-top:3px">Ainda virão</div>
                </div>
                <div style="background:#f8fafc;border-radius:10px;padding:16px;text-align:center">
                    <div style="font-size:1.8rem;font-family:'Lora',serif;color:#94a3b8">{len(passados)}</div>
                    <div style="font-size:.72rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em;margin-top:3px">Já passaram</div>
                </div>
                <div style="background:#f8fafc;border-radius:10px;padding:16px;text-align:center">
                    <div style="font-size:1.8rem;font-family:'Lora',serif;color:#0f172a">{round(len(aniv_mes)/total*100) if total else 0}%</div>
                    <div style="font-size:.72rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em;margin-top:3px">Da congregação</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Sazonalidade anual
    st.markdown('<div class="panel"><div class="panel-title">Aniversários por Mês do Ano <span>— sazonalidade</span></div>', unsafe_allow_html=True)
    por_mes = df.groupby("_mes").size().reindex(range(1,13), fill_value=0)
    max_val = por_mes.max() or 1
    bars    = ""
    for m, cnt in por_mes.items():
        h_pct    = int((cnt / max_val) * 100)
        is_atual = "current" if m == hoje.month else ""
        bars    += f"""
        <div class="season-bar-wrap">
            <div class="season-count">{cnt}</div>
            <div class="season-bar {is_atual}" style="height:{h_pct}%"></div>
            <div class="season-label">{MESES_PT[m-1]}</div>
        </div>"""
    st.markdown(f'<div class="season-row">{bars}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Tabela do mês — dois painéis
    col_fut, col_pas = st.columns(2)

    def render_bday_table(df_sub, titulo):
        if df_sub.empty:
            return f'<div class="panel"><div class="panel-title">{titulo}</div><p style="color:#94a3b8;font-size:.85rem">Nenhum registro.</p></div>'
        rows = ""
        for _, r in df_sub.iterrows():
            ini    = r.get("_iniciais","??")
            nome   = r.get("Nome Completo","—")
            bairro = r.get("Bairro","—")
            idade  = r.get("Idade","—")
            tel    = r.get("Telefone","—")
            dia    = r.get("_dia","—")
            rows  += f"""
            <tr>
                <td style="color:#94a3b8;font-size:.82rem">{dia:02d}/{hoje.month:02d}</td>
                <td>
                    <div style="display:flex;align-items:center;gap:10px">
                        <div class="today-avatar" style="width:32px;height:32px;font-size:.75rem">{ini}</div>
                        <div><div class="wt-name">{nome}</div><div class="wt-sub">{bairro}</div></div>
                    </div>
                </td>
                <td style="color:#475569;font-size:.82rem">{idade} anos</td>
                <td><span class="wt-phone">{tel}</span></td>
            </tr>"""
        return f"""
        <div class="panel"><div class="panel-title">{titulo} <span>({len(df_sub)})</span></div>
        <table class="week-table">
            <thead><tr><th>Data</th><th>Membro</th><th>Idade</th><th>Telefone</th></tr></thead>
            <tbody>{rows}</tbody>
        </table></div>"""

    with col_fut:
        st.markdown(render_bday_table(futuros, "Ainda virão este mês"), unsafe_allow_html=True)
    with col_pas:
        st.markdown(render_bday_table(passados, "Já passaram este mês"), unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — ANÁLISE DA CONGREGAÇÃO
# ════════════════════════════════════════════════════════════════════════════════
with tab3:

    col_pir, col_eng = st.columns([1.2, 1])

    # Pirâmide Etária
    with col_pir:
        st.markdown('<div class="panel"><div class="panel-title">Pirâmide Etária <span>— masculino vs feminino</span></div>', unsafe_allow_html=True)

        if "Gênero" in df.columns:
            masc = df[df["Gênero"].str.lower() == "masculino"]
            fem  = df[df["Gênero"].str.lower() == "feminino"]

            masc_faixa = masc["Faixa Etária"].value_counts().reindex(ORDEM_FAIXA, fill_value=0)
            fem_faixa  = fem["Faixa Etária"].value_counts().reindex(ORDEM_FAIXA, fill_value=0)
            max_pyr    = max(masc_faixa.max(), fem_faixa.max(), 1)

            st.markdown("""
            <div style="display:flex;justify-content:center;gap:40px;margin-bottom:12px;font-size:.75rem;font-weight:600">
                <div style="color:#2563eb">Masculino</div>
                <div style="width:150px"></div>
                <div style="color:#db2777">Feminino</div>
            </div>""", unsafe_allow_html=True)

            for faixa in reversed(ORDEM_FAIXA):
                m_val  = masc_faixa.get(faixa, 0)
                f_val  = fem_faixa.get(faixa, 0)
                m_pct  = int((m_val / max_pyr) * 120)
                f_pct  = int((f_val / max_pyr) * 120)
                st.markdown(f"""
                <div class="pyramid-row">
                    <div class="pyramid-val" style="text-align:right">{m_val}</div>
                    <div style="flex:1;display:flex;justify-content:flex-end">
                        <div class="pyramid-bar-left" style="width:{m_pct}px"></div>
                    </div>
                    <div class="pyramid-center"></div>
                    <div class="pyramid-label" style="width:150px;text-align:left;font-size:.72rem;color:#475569;padding:0 8px">{faixa}</div>
                    <div style="flex:1;display:flex;justify-content:flex-start">
                        <div class="pyramid-bar-right" style="width:{f_pct}px"></div>
                    </div>
                    <div class="pyramid-val">{f_val}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Coluna 'Gênero' não encontrada nos dados.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Engajamento por Bairro
    with col_eng:
        st.markdown('<div class="panel"><div class="panel-title">Engajamento por Bairro <span>— % de ativos</span></div>', unsafe_allow_html=True)

        if "Membro Ativo" in df.columns and "Bairro" in df.columns:
            eng = (
                df.groupby("Bairro")
                  .agg(total=("Membro Ativo","count"),
                       ativos=("Membro Ativo", lambda x: (x=="Sim").sum()))
                  .assign(pct=lambda d: (d["ativos"]/d["total"]*100).round(1))
                  .sort_values("pct", ascending=False)
            )
            max_pct = eng["pct"].max() or 1
            for bairro, row in eng.iterrows():
                pct      = row["pct"]
                cor_cls  = "low" if pct < 60 else ("mid" if pct < 80 else "")
                st.markdown(f"""
                <div class="eng-row">
                    <div class="eng-label" title="{bairro}">{bairro}</div>
                    <div class="eng-bar-bg">
                        <div class="eng-bar-fill {cor_cls}" style="width:{pct}%"></div>
                    </div>
                    <div class="eng-pct">{pct:.0f}%</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Dados de bairro ou status não disponíveis.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Linha 2 — Faixa etária por status + Distribuição de gênero por faixa
    col_fe, col_gf = st.columns(2)

    with col_fe:
        st.markdown('<div class="panel"><div class="panel-title">Ativos vs Inativos por Faixa Etária</div>', unsafe_allow_html=True)
        if "Membro Ativo" in df.columns:
            cross = (
                df.groupby(["Faixa Etária","Membro Ativo"])
                  .size()
                  .unstack(fill_value=0)
                  .reindex(ORDEM_FAIXA)
                  .dropna(how="all")
            )
            cross.columns.name = None
            st.bar_chart(cross, color=["#059669","#ef4444"] if "Sim" in cross.columns and "Não" in cross.columns else ["#2563eb"],
                         use_container_width=True, height=220)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_gf:
        st.markdown('<div class="panel"><div class="panel-title">Gênero por Faixa Etária</div>', unsafe_allow_html=True)
        if "Gênero" in df.columns:
            gf = (
                df.groupby(["Faixa Etária","Gênero"])
                  .size()
                  .unstack(fill_value=0)
                  .reindex(ORDEM_FAIXA)
                  .dropna(how="all")
            )
            gf.columns.name = None
            st.bar_chart(gf, color=["#2563eb","#db2777"] if len(gf.columns)==2 else ["#2563eb"],
                         use_container_width=True, height=220)
        st.markdown("</div>", unsafe_allow_html=True)

    # Indicadores gerais
    idade_media = round(df["Idade"].dropna().mean(), 1) if df["Idade"].dropna().any() else "—"
    idade_min   = int(df["Idade"].dropna().min()) if df["Idade"].dropna().any() else "—"
    idade_max   = int(df["Idade"].dropna().max()) if df["Idade"].dropna().any() else "—"
    adultos     = len(df[df["Faixa Etária"].isin(["Jovens adultos (18–29)","Adultos (30–59)"])])
    dependentes = len(df[df["Faixa Etária"].isin(["Crianças (0–12)","Idosos (60+)"])])
    razao       = round(dependentes/adultos, 2) if adultos else "—"

    st.markdown(f"""
    <div class="panel">
        <div class="panel-title">Indicadores Demográficos</div>
        <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:16px">
            <div style="text-align:center">
                <div style="font-family:'Lora',serif;font-size:1.6rem;color:#0f172a">{idade_media}</div>
                <div style="font-size:.7rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em;margin-top:4px">Idade média</div>
            </div>
            <div style="text-align:center">
                <div style="font-family:'Lora',serif;font-size:1.6rem;color:#0f172a">{idade_min}</div>
                <div style="font-size:.7rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em;margin-top:4px">Mais jovem</div>
            </div>
            <div style="text-align:center">
                <div style="font-family:'Lora',serif;font-size:1.6rem;color:#0f172a">{idade_max}</div>
                <div style="font-size:.7rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em;margin-top:4px">Mais velho</div>
            </div>
            <div style="text-align:center">
                <div style="font-family:'Lora',serif;font-size:1.6rem;color:#0f172a">{adultos}</div>
                <div style="font-size:.7rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em;margin-top:4px">Adultos ativos</div>
            </div>
            <div style="text-align:center">
                <div style="font-family:'Lora',serif;font-size:1.6rem;color:#0f172a">{razao}</div>
                <div style="font-size:.7rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em;margin-top:4px">Razão dependência</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 — MEMBROS
# ════════════════════════════════════════════════════════════════════════════════
with tab4:

    f1, f2, f3, f4 = st.columns([2.5,1.5,1.8,1.2])
    with f1:
        busca = st.text_input("Buscar por nome", placeholder="Digite o nome do membro...")
    with f2:
        bairros_opts = ["Todos os bairros"] + sorted(df["Bairro"].dropna().unique().tolist())
        bairro_sel   = st.selectbox("Bairro", bairros_opts)
    with f3:
        faixa_opts = ["Todas as faixas"] + ORDEM_FAIXA
        faixa_sel  = st.selectbox("Faixa etária", faixa_opts)
    with f4:
        status_opts = ["Todos"] + (["Ativos","Inativos"] if "Membro Ativo" in df.columns else [])
        status_sel  = st.selectbox("Status", status_opts)

    df_f = df.copy()
    if busca:
        df_f = df_f[df_f["Nome Completo"].str.lower().str.contains(busca.lower(), na=False)]
    if bairro_sel != "Todos os bairros":
        df_f = df_f[df_f["Bairro"] == bairro_sel]
    if faixa_sel != "Todas as faixas":
        df_f = df_f[df_f["Faixa Etária"] == faixa_sel]
    if status_sel == "Ativos" and "Membro Ativo" in df_f.columns:
        df_f = df_f[df_f["Membro Ativo"] == "Sim"]
    elif status_sel == "Inativos" and "Membro Ativo" in df_f.columns:
        df_f = df_f[df_f["Membro Ativo"] == "Não"]

    st.markdown(f'<div class="panel"><div class="panel-title">Lista de Membros <span>— {len(df_f)} resultado(s)</span></div>', unsafe_allow_html=True)

    rows = ""
    for _, r in df_f.iterrows():
        ini    = r.get("_iniciais","??")
        nome   = r.get("Nome Completo","—")
        nasc   = r.get("Data de Nascimento","—")
        idade  = r.get("Idade","—")
        faixa  = r.get("Faixa Etária","—")
        genero = r.get("Gênero","—")
        bairro = r.get("Bairro","—")
        tel    = r.get("Telefone","—")
        ativo  = r.get("Membro Ativo","—")
        dias_a = r.get("_dias_aniv", None)

        pill = (
            '<span class="pill pill-sim">Ativo</span>'   if str(ativo) == "Sim" else
            '<span class="pill pill-nao">Inativo</span>' if str(ativo) == "Não" else "—"
        )
        aniv_badge = ""
        if dias_a is not None:
            if dias_a == 0:   aniv_badge = '&nbsp;<span class="pill" style="background:#fef9c3;color:#854d0e">Hoje!</span>'
            elif dias_a <= 7: aniv_badge = f'&nbsp;<span class="pill" style="background:#dbeafe;color:#1e40af">Em {dias_a}d</span>'

        rows += f"""
        <tr>
            <td>
                <div style="display:flex;align-items:center;gap:10px">
                    <div class="today-avatar" style="width:34px;height:34px;font-size:.78rem">{ini}</div>
                    <div>
                        <div class="mt-name">{nome}{aniv_badge}</div>
                        <div class="mt-sub">{bairro}</div>
                    </div>
                </div>
            </td>
            <td style="color:#475569;font-size:.82rem">{nasc}</td>
            <td>
                <div style="color:#0f172a;font-size:.875rem">{idade} anos</div>
                <div class="mt-sub">{faixa}</div>
            </td>
            <td style="color:#475569;font-size:.82rem">{genero}</td>
            <td style="color:#2563eb;font-size:.82rem;font-weight:500">{tel}</td>
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
    </table>
    </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Exportação
    COLS_EXPORT = ["Nome Completo","Data de Nascimento","Idade","Faixa Etária","Gênero","Bairro","Telefone","Membro Ativo"]
    cols_ok = [c for c in COLS_EXPORT if c in df_f.columns]
    csv_bytes = df_f[cols_ok].to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")

    st.markdown(f"""
    <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;
        padding:16px 22px;display:flex;align-items:center;justify-content:space-between;margin-top:16px">
        <div>
            <div style="font-size:.85rem;font-weight:600;color:#0f172a">{len(df_f)} membros prontos para exportação</div>
            <div style="font-size:.78rem;color:#94a3b8;margin-top:2px">Com os filtros aplicados &mdash; arquivo CSV compativel com Excel</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.download_button(
        "Baixar lista em CSV",
        data=csv_bytes,
        file_name=f"membros_ibp_{hoje.strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )

