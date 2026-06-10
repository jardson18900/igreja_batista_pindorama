import streamlit as st
import pandas as pd
from datetime import date
import urllib.request

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Igreja Batista de Pindorama",
    page_icon="✝️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&display=swap');

*, html, body { font-family: 'DM Sans', sans-serif; }
h1,h2,h3,h4 { font-family: 'DM Serif Display', serif; }

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="collapsedControl"] { display: none; }
.block-container { padding: 0 2rem 3rem 2rem !important; max-width: 1200px; }

/* ── TOP NAV ── */
.topnav {
    background: #0d1f3c;
    border-radius: 0 0 20px 20px;
    padding: 0 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: -1rem -2rem 2rem -2rem;
    box-shadow: 0 4px 24px rgba(13,31,60,0.15);
}
.topnav-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 18px 0;
}
.topnav-brand .cross { font-size: 1.5rem; }
.topnav-brand .name {
    font-family: 'DM Serif Display', serif;
    color: white;
    font-size: 1.1rem;
    line-height: 1.2;
}
.topnav-brand .sub {
    color: #7fa4cc;
    font-size: 0.72rem;
    font-weight: 300;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.topnav-date {
    color: #7fa4cc;
    font-size: 0.8rem;
    font-weight: 300;
}

/* ── METRIC CARDS ── */
.metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 32px; }
.mcard {
    background: white;
    border-radius: 16px;
    padding: 22px 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
    border-top: 3px solid transparent;
    transition: transform .15s;
}
.mcard:hover { transform: translateY(-2px); }
.mcard.blue  { border-top-color: #1a56db; }
.mcard.green { border-top-color: #057a55; }
.mcard.amber { border-top-color: #c27803; }
.mcard.rose  { border-top-color: #be185d; }
.mcard .ico { font-size: 1.5rem; margin-bottom: 8px; }
.mcard .val {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem;
    color: #0d1f3c;
    line-height: 1;
}
.mcard .lbl {
    font-size: 0.78rem;
    color: #6b7280;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 4px;
}

/* ── SECTION TITLE ── */
.sec-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.25rem;
    color: #0d1f3c;
    margin: 0 0 14px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid #f0f4f8;
}

/* ── CHART CARD ── */
.chart-card {
    background: white;
    border-radius: 16px;
    padding: 22px 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
    margin-bottom: 16px;
    height: 100%;
}

/* ── BIRTHDAY CARDS ── */
.bday-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
.bday-card {
    background: white;
    border-radius: 14px;
    padding: 16px 18px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    display: flex;
    align-items: center;
    gap: 14px;
    border-left: 4px solid #c27803;
}
.bday-card.today { border-left-color: #be185d; background: #fff5f9; }
.bday-card.past  { border-left-color: #d1d5db; opacity: 0.7; }
.bday-ico { font-size: 1.8rem; flex-shrink: 0; }
.bday-name { font-weight: 600; color: #0d1f3c; font-size: 0.95rem; }
.bday-detail { color: #6b7280; font-size: 0.8rem; margin-top: 2px; }

/* ── TABLE ── */
.stDataFrame { border-radius: 12px !important; overflow: hidden !important; }
.stDataFrame th {
    background: #f8fafc !important;
    color: #374151 !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.04em !important;
}

/* ── BADGE ── */
.badge-sim { background:#d1fae5; color:#065f46; padding:2px 10px; border-radius:99px; font-size:.75rem; font-weight:600; }
.badge-nao { background:#fee2e2; color:#991b1b; padding:2px 10px; border-radius:99px; font-size:.75rem; font-weight:600; }

/* ── SEARCH BAR ── */
.stTextInput input {
    border-radius: 10px !important;
    border: 1.5px solid #e5e7eb !important;
    padding: 10px 14px !important;
    font-size: 0.9rem !important;
}
.stTextInput input:focus { border-color: #1a56db !important; box-shadow: 0 0 0 3px rgba(26,86,219,0.1) !important; }

/* ── SELECTBOX ── */
.stSelectbox > div > div {
    border-radius: 10px !important;
    border: 1.5px solid #e5e7eb !important;
}

/* ── SHEETS INPUT ── */
.sheets-box {
    background: #f0f7ff;
    border: 1.5px solid #bfdbfe;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 16px;
}
.sheets-box p { color: #1e40af; font-size: 0.85rem; margin: 0 0 8px 0; }

/* ── PAGE TABS ── */
div[data-testid="stHorizontalBlock"] { gap: 0 !important; }

/* Streamlit tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #f1f5f9;
    border-radius: 12px;
    padding: 4px;
    margin-bottom: 24px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 500;
    font-size: 0.9rem;
    color: #6b7280;
}
.stTabs [aria-selected="true"] {
    background: white !important;
    color: #0d1f3c !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}
.stTabs [data-baseweb="tab-highlight"] { display: none; }
.stTabs [data-baseweb="tab-border"] { display: none; }

</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def calcular_idade(val):
    try:
        d = pd.to_datetime(val, dayfirst=True)
        h = date.today()
        return h.year - d.year - ((h.month, h.day) < (d.month, d.day))
    except Exception:
        return None

def faixa_etaria(idade):
    if idade is None: return "Não informado"
    if idade < 13:   return "Crianças (0–12)"
    if idade < 18:   return "Jovens (13–17)"
    if idade < 30:   return "Jovens adultos (18–29)"
    if idade < 60:   return "Adultos (30–59)"
    return "Idosos (60+)"

def mes_nasc(val):
    try: return pd.to_datetime(val, dayfirst=True).month
    except: return None

def dia_nasc(val):
    try: return pd.to_datetime(val, dayfirst=True).day
    except: return 99

def normalizar(df):
    df.columns = [c.strip() for c in df.columns]
    if "Email" in df.columns:
        df = df.drop(columns=["Email"])
    if "Nome Completo" in df.columns:
        df["Nome Completo"] = df["Nome Completo"].str.strip().str.title()
    if "Bairro" in df.columns:
        df["Bairro"] = df["Bairro"].str.strip().str.title()
    if "Membro Ativo" in df.columns:
        df["Membro Ativo"] = df["Membro Ativo"].str.strip().str.capitalize()
    df["Idade"]       = df["Data de Nascimento"].apply(calcular_idade)
    df["Faixa Etária"] = df["Idade"].apply(faixa_etaria)
    df["_mes"]        = df["Data de Nascimento"].apply(mes_nasc)
    df["_dia"]        = df["Data de Nascimento"].apply(dia_nasc)
    return df

@st.cache_data
def carregar_padrao():
    return pd.read_csv("dados_membros.csv", encoding="utf-8-sig")

@st.cache_data(ttl=300)  # cache 5 min
def carregar_sheets(url):
    """Lê Google Sheets publicada como CSV."""
    # converte URL de edição para exportação CSV
    if "spreadsheets/d/" in url:
        sheet_id = url.split("/d/")[1].split("/")[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    else:
        csv_url = url
    return pd.read_csv(csv_url, encoding="utf-8-sig")


# ── TOP NAV ───────────────────────────────────────────────────────────────────
hoje = date.today()
st.markdown(f"""
<div class="topnav">
    <div class="topnav-brand">
        <span class="cross">✝️</span>
        <div>
            <div class="name">Igreja Batista de Pindorama</div>
            <div class="sub">Painel de Gestão de Membros</div>
        </div>
    </div>
    <div class="topnav-date">{hoje.strftime("%d de %B de %Y")}</div>
</div>
""", unsafe_allow_html=True)


# ── DATA SOURCE (expander discreto) ──────────────────────────────────────────
with st.expander("⚙️ Fonte de dados", expanded=False):
    fonte = st.radio(
        "Fonte",
        ["📋 Dados de demonstração", "📊 Google Sheets (ao vivo)", "📂 Upload de CSV"],
        horizontal=True,
        label_visibility="collapsed",
    )

    df_raw = None

    if fonte == "📊 Google Sheets (ao vivo)":
        st.markdown("""
        <div class="sheets-box">
            <p>🔗 <strong>Como conectar:</strong> Abra sua planilha → <em>Arquivo → Compartilhar → Publicar na web</em>
            → escolha a aba → formato CSV → copie o link e cole abaixo.</p>
        </div>
        """, unsafe_allow_html=True)
        sheets_url = st.text_input("URL da planilha Google Sheets", placeholder="https://docs.google.com/spreadsheets/d/...")
        if sheets_url:
            try:
                df_raw = carregar_sheets(sheets_url)
                st.success(f"✅ {len(df_raw)} registros carregados da planilha")
            except Exception as e:
                st.error(f"Erro ao carregar planilha: {e}")

    elif fonte == "📂 Upload de CSV":
        up = st.file_uploader("Selecionar CSV exportado do Google Forms", type=["csv"], label_visibility="collapsed")
        if up:
            df_raw = pd.read_csv(up, encoding="utf-8-sig")
            st.success(f"✅ {len(df_raw)} registros carregados")

    if df_raw is None:
        df_raw = carregar_padrao()

df = normalizar(df_raw.copy())
hoje_mes = hoje.month
hoje_dia = hoje.day


# ── TABS (menu horizontal) ────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📊  Visão Geral", "🎂  Aniversariantes", "👥  Membros"])


# ════════════════════════════════════════════════════════════
# TAB 1 — VISÃO GERAL
# ════════════════════════════════════════════════════════════
with tab1:
    ativos      = len(df[df.get("Membro Ativo", pd.Series(dtype=str)) == "Sim"]) if "Membro Ativo" in df else len(df)
    aniv_mes    = int((df["_mes"] == hoje_mes).sum())
    idade_media = int(df["Idade"].dropna().mean()) if df["Idade"].dropna().any() else "—"

    # Metric cards via HTML
    st.markdown(f"""
    <div class="metric-grid">
        <div class="mcard blue">
            <div class="ico">👥</div>
            <div class="val">{len(df)}</div>
            <div class="lbl">Total de membros</div>
        </div>
        <div class="mcard green">
            <div class="ico">✅</div>
            <div class="val">{ativos}</div>
            <div class="lbl">Membros ativos</div>
        </div>
        <div class="mcard amber">
            <div class="ico">🎂</div>
            <div class="val">{aniv_mes}</div>
            <div class="lbl">Aniversários este mês</div>
        </div>
        <div class="mcard rose">
            <div class="ico">📅</div>
            <div class="val">{idade_media}</div>
            <div class="lbl">Idade média (anos)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    ORDEM_FAIXA = ["Crianças (0–12)", "Jovens (13–17)", "Jovens adultos (18–29)", "Adultos (30–59)", "Idosos (60+)"]

    with col_a:
        st.markdown('<div class="chart-card"><p class="sec-title">👤 Faixa Etária</p>', unsafe_allow_html=True)
        faixa_counts = (
            df["Faixa Etária"]
            .value_counts()
            .reindex(ORDEM_FAIXA)
            .dropna()
            .rename("Membros")
        )
        st.bar_chart(faixa_counts, color="#1a56db", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="chart-card"><p class="sec-title">🏘️ Membros por Bairro</p>', unsafe_allow_html=True)
        bairro_counts = df["Bairro"].value_counts().head(10).rename("Membros")
        st.bar_chart(bairro_counts, color="#057a55", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if "Gênero" in df.columns:
        col_c, col_d = st.columns([1, 2])
        with col_c:
            st.markdown('<div class="chart-card"><p class="sec-title">⚧ Gênero</p>', unsafe_allow_html=True)
            genero_counts = df["Gênero"].value_counts().rename("Membros")
            st.bar_chart(genero_counts, color="#c27803", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# TAB 2 — ANIVERSARIANTES
# ════════════════════════════════════════════════════════════
with tab2:
    nome_mes = hoje.strftime("%B").capitalize()
    st.markdown(f'<p class="sec-title">🎂 Aniversariantes de {nome_mes}</p>', unsafe_allow_html=True)

    aniv_df = df[df["_mes"] == hoje_mes].sort_values("_dia").copy()

    if aniv_df.empty:
        st.info("Nenhum aniversariante este mês.")
    else:
        # Renderiza cards em grid 2 colunas
        cards_html = '<div class="bday-grid">'
        for _, row in aniv_df.iterrows():
            dia    = row["_dia"]
            nome   = row.get("Nome Completo", "—")
            idade  = row.get("Idade", "—")
            bairro = row.get("Bairro", "—")
            tel    = row.get("Telefone", "—")

            if dia == hoje_dia:
                cls, ico = "today", "🎉"
            elif dia > hoje_dia:
                cls, ico = "",      "🎂"
            else:
                cls, ico = "past",  "✅"

            cards_html += f"""
            <div class="bday-card {cls}">
                <div class="bday-ico">{ico}</div>
                <div>
                    <div class="bday-name">Dia {dia:02d} · {nome}</div>
                    <div class="bday-detail">{idade} anos · {bairro}</div>
                    <div class="bday-detail">📱 {tel}</div>
                </div>
            </div>"""
        cards_html += '</div>'
        st.markdown(cards_html, unsafe_allow_html=True)

    # Próximo mês
    st.markdown("<br>", unsafe_allow_html=True)
    proximo = (hoje_mes % 12) + 1
    nome_prox = date(hoje.year, proximo, 1).strftime("%B").capitalize()
    st.markdown(f'<p class="sec-title">📅 Próximo mês — {nome_prox}</p>', unsafe_allow_html=True)

    prox_df = df[df["_mes"] == proximo].sort_values("_dia")
    if prox_df.empty:
        st.info("Nenhum aniversariante no próximo mês.")
    else:
        colunas = [c for c in ["Nome Completo", "Data de Nascimento", "Idade", "Bairro", "Telefone"] if c in prox_df.columns]
        st.dataframe(prox_df[colunas].reset_index(drop=True), use_container_width=True, hide_index=True)


# ════════════════════════════════════════════════════════════
# TAB 3 — MEMBROS
# ════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<p class="sec-title">👥 Lista de Membros</p>', unsafe_allow_html=True)

    f1, f2, f3, f4 = st.columns([2, 1.5, 1.5, 1])
    with f1:
        busca = st.text_input("Buscar por nome", placeholder="🔍  Digite o nome...", label_visibility="collapsed")
    with f2:
        bairros = ["Todos os bairros"] + sorted(df["Bairro"].dropna().unique().tolist())
        bairro_sel = st.selectbox("Bairro", bairros, label_visibility="collapsed")
    with f3:
        faixas = ["Todas as faixas"] + ORDEM_FAIXA
        faixa_sel = st.selectbox("Faixa", faixas, label_visibility="collapsed")
    with f4:
        ativo_sel = st.selectbox("Status", ["Todos", "Ativos", "Inativos"], label_visibility="collapsed")

    df_f = df.copy()
    if busca:
        df_f = df_f[df_f["Nome Completo"].str.lower().str.contains(busca.lower(), na=False)]
    if bairro_sel != "Todos os bairros":
        df_f = df_f[df_f["Bairro"] == bairro_sel]
    if faixa_sel != "Todas as faixas":
        df_f = df_f[df_f["Faixa Etária"] == faixa_sel]
    if ativo_sel == "Ativos" and "Membro Ativo" in df_f.columns:
        df_f = df_f[df_f["Membro Ativo"] == "Sim"]
    elif ativo_sel == "Inativos" and "Membro Ativo" in df_f.columns:
        df_f = df_f[df_f["Membro Ativo"] == "Não"]

    st.caption(f"{len(df_f)} membro(s) encontrado(s)")

    COLS = ["Nome Completo", "Data de Nascimento", "Idade", "Faixa Etária", "Gênero", "Bairro", "Telefone", "Membro Ativo"]
    cols_ok = [c for c in COLS if c in df_f.columns]

    st.dataframe(df_f[cols_ok].reset_index(drop=True), use_container_width=True, hide_index=True)

    csv_export = df_f[cols_ok].to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button("⬇️ Exportar lista filtrada (.csv)", csv_export, "membros_filtrados.csv", "text/csv")

