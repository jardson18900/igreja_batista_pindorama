import streamlit as st
import pandas as pd
from datetime import date
import io

# ── Configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Igreja Batista de Pindorama",
    page_icon="✝️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS personalizado ───────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(160deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
    }
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #c8d6e5 !important;
    }

    /* Cards de métricas */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        border-radius: 16px;
        padding: 24px 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(15, 52, 96, 0.08);
        border-left: 4px solid #0f3460;
        margin-bottom: 8px;
    }
    .metric-card .value {
        font-size: 2.4rem;
        font-weight: 700;
        color: #0f3460;
        font-family: 'Playfair Display', serif;
        line-height: 1;
    }
    .metric-card .label {
        font-size: 0.8rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 6px;
    }

    /* Aniversariante card */
    .birthday-card {
        background: linear-gradient(135deg, #fff9f0 0%, #fff3e0 100%);
        border-radius: 12px;
        padding: 14px 18px;
        border-left: 4px solid #e67e22;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .birthday-card .name {
        font-weight: 600;
        color: #1a1a2e;
        font-size: 0.95rem;
    }
    .birthday-card .detail {
        color: #888;
        font-size: 0.8rem;
    }

    /* Header */
    .app-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
        color: white;
    }
    .app-header h1 {
        color: white !important;
        margin: 0;
        font-size: 1.9rem;
    }
    .app-header p {
        color: #a0b4cc;
        margin: 4px 0 0 0;
        font-size: 0.9rem;
    }

    /* Upload box */
    .upload-hint {
        background: #f0f4ff;
        border: 2px dashed #0f3460;
        border-radius: 12px;
        padding: 16px;
        color: #0f3460;
        font-size: 0.85rem;
        text-align: center;
        margin-bottom: 16px;
    }

    /* Tabela */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Divider */
    hr { border-color: #e8ecf0; }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 99px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-sim { background:#d4edda; color:#155724; }
    .badge-nao { background:#f8d7da; color:#721c24; }
</style>
""", unsafe_allow_html=True)


# ── Funções utilitárias ─────────────────────────────────────────────────────
def calcular_idade(data_nasc_str: str) -> int:
    try:
        d = pd.to_datetime(data_nasc_str, dayfirst=True)
        hoje = date.today()
        return hoje.year - d.year - ((hoje.month, hoje.day) < (d.month, d.day))
    except Exception:
        return None

def faixa_etaria(idade):
    if idade is None:
        return "Não informado"
    if idade < 13:
        return "Crianças (0–12)"
    if idade < 18:
        return "Jovens (13–17)"
    if idade < 30:
        return "Jovens adultos (18–29)"
    if idade < 60:
        return "Adultos (30–59)"
    return "Idosos (60+)"

def eh_aniversariante_mes(data_nasc_str: str) -> bool:
    try:
        d = pd.to_datetime(data_nasc_str, dayfirst=True)
        return d.month == date.today().month
    except Exception:
        return False

def dia_nascimento(data_nasc_str: str) -> int:
    try:
        return pd.to_datetime(data_nasc_str, dayfirst=True).day
    except Exception:
        return 99

def normalizar_df(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza colunas: strip, title case em nomes, upper em bairro."""
    col_map = {c: c.strip() for c in df.columns}
    df = df.rename(columns=col_map)
    if "Nome Completo" in df.columns:
        df["Nome Completo"] = df["Nome Completo"].str.strip().str.title()
    if "Bairro" in df.columns:
        df["Bairro"] = df["Bairro"].str.strip().str.title()
    if "Membro Ativo" in df.columns:
        df["Membro Ativo"] = df["Membro Ativo"].str.strip().str.capitalize()
    df["Idade"] = df["Data de Nascimento"].apply(calcular_idade)
    df["Faixa Etária"] = df["Idade"].apply(faixa_etaria)
    df["Aniversário Mês"] = df["Data de Nascimento"].apply(eh_aniversariante_mes)
    return df

@st.cache_data
def carregar_dados_padrao():
    return pd.read_csv("dados_membros.csv", encoding="utf-8-sig")


# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ✝️ Igreja Batista\nde Pindorama")
    st.markdown("---")

    pagina = st.radio(
        "Navegação",
        ["📊 Visão Geral", "🎂 Aniversariantes", "👥 Membros"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### 📂 Dados")

    modo = st.radio(
        "Fonte dos dados",
        ["Dados de demonstração", "Carregar CSV próprio"],
        label_visibility="collapsed",
    )

    df_raw = None
    if modo == "Carregar CSV próprio":
        st.markdown(
            '<div class="upload-hint">📥 Exporte o CSV do Google Forms e faça upload aqui</div>',
            unsafe_allow_html=True,
        )
        uploaded = st.file_uploader("Selecionar arquivo CSV", type=["csv"], label_visibility="collapsed")
        if uploaded:
            df_raw = pd.read_csv(uploaded, encoding="utf-8-sig")
            st.success(f"✅ {len(df_raw)} registros carregados")

    if df_raw is None:
        df_raw = carregar_dados_padrao()

    df = normalizar_df(df_raw.copy())

    # Filtro rápido de ativos
    mostrar = st.radio("Exibir membros", ["Todos", "Apenas ativos", "Apenas inativos"])
    if mostrar == "Apenas ativos":
        df = df[df["Membro Ativo"] == "Sim"]
    elif mostrar == "Apenas inativos":
        df = df[df["Membro Ativo"] == "Não"]

    st.markdown("---")
    st.caption(f"Total carregado: **{len(df)}** membros")


# ── Header ──────────────────────────────────────────────────────────────────
mes_nome = date.today().strftime("%B de %Y").capitalize()
st.markdown(f"""
<div class="app-header">
    <h1>✝️ Igreja Batista de Pindorama</h1>
    <p>Painel de Gestão de Membros · {mes_nome}</p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 1 — VISÃO GERAL
# ══════════════════════════════════════════════════════════════════════════════
if pagina == "📊 Visão Geral":
    ativos = len(df[df["Membro Ativo"] == "Sim"])
    inativos = len(df[df["Membro Ativo"] == "Não"])
    aniversariantes = df["Aniversário Mês"].sum()
    idade_media = int(df["Idade"].dropna().mean()) if df["Idade"].dropna().any() else "—"

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><div class="value">{len(df)}</div><div class="label">Total de Membros</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><div class="value">{ativos}</div><div class="label">Membros Ativos</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><div class="value">{aniversariantes}</div><div class="label">Aniversários este mês</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><div class="value">{idade_media}</div><div class="label">Idade média (anos)</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("### 👥 Distribuição por Faixa Etária")
        ordem_faixa = ["Crianças (0–12)", "Jovens (13–17)", "Jovens adultos (18–29)", "Adultos (30–59)", "Idosos (60+)"]
        faixa_counts = df["Faixa Etária"].value_counts().reindex(ordem_faixa).dropna()
        st.bar_chart(faixa_counts, color="#0f3460")

    with col_b:
        st.markdown("### 🏘️ Membros por Bairro")
        bairro_counts = df["Bairro"].value_counts().head(10)
        st.bar_chart(bairro_counts, color="#e67e22")

    st.markdown("### ⚧ Distribuição por Gênero")
    if "Gênero" in df.columns:
        genero_counts = df["Gênero"].value_counts()
        col_g1, col_g2, col_g3 = st.columns([1, 2, 1])
        with col_g2:
            st.bar_chart(genero_counts, color="#27ae60")


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 2 — ANIVERSARIANTES
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "🎂 Aniversariantes":
    st.markdown(f"### 🎂 Aniversariantes de {date.today().strftime('%B')}")

    aniv = df[df["Aniversário Mês"]].copy()
    aniv["_dia"] = aniv["Data de Nascimento"].apply(dia_nascimento)
    aniv = aniv.sort_values("_dia")

    if aniv.empty:
        st.info("Nenhum aniversariante encontrado para este mês.")
    else:
        st.caption(f"🎉 {len(aniv)} aniversariante(s) este mês")
        st.markdown("<br>", unsafe_allow_html=True)

        cols = st.columns(2)
        for i, (_, row) in enumerate(aniv.iterrows()):
            col = cols[i % 2]
            with col:
                dia = row["_dia"]
                hoje_dia = date.today().day
                icone = "🎂" if dia == hoje_dia else ("🎈" if dia > hoje_dia else "✅")
                nome = row.get("Nome Completo", "—")
                bairro = row.get("Bairro", "—")
                idade = row.get("Idade", "—")
                tel = row.get("Telefone", "—")

                st.markdown(f"""
                <div class="birthday-card">
                    <div style="font-size:2rem">{icone}</div>
                    <div>
                        <div class="name">{nome}</div>
                        <div class="detail">Dia {dia} · {idade} anos · {bairro}</div>
                        <div class="detail">📱 {tel}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Próximos meses (preview)
    st.markdown("---")
    st.markdown("### 📅 Próximo mês")
    proximo_mes = (date.today().month % 12) + 1

    def eh_proximo_mes(data_nasc_str):
        try:
            return pd.to_datetime(data_nasc_str, dayfirst=True).month == proximo_mes
        except Exception:
            return False

    prox = df[df["Data de Nascimento"].apply(eh_proximo_mes)]
    if prox.empty:
        st.info("Nenhum aniversariante no próximo mês.")
    else:
        st.caption(f"{len(prox)} aniversariante(s) no próximo mês")
        st.dataframe(
            prox[["Nome Completo", "Data de Nascimento", "Idade", "Bairro", "Telefone"]].reset_index(drop=True),
            use_container_width=True,
            hide_index=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
# PÁGINA 3 — MEMBROS
# ══════════════════════════════════════════════════════════════════════════════
elif pagina == "👥 Membros":
    st.markdown("### 👥 Lista de Membros")

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        busca = st.text_input("🔍 Buscar por nome", placeholder="Digite o nome...")
    with col_f2:
        bairros = ["Todos"] + sorted(df["Bairro"].dropna().unique().tolist())
        bairro_sel = st.selectbox("🏘️ Filtrar por bairro", bairros)
    with col_f3:
        faixas = ["Todas"] + ["Crianças (0–12)", "Jovens (13–17)", "Jovens adultos (18–29)", "Adultos (30–59)", "Idosos (60+)"]
        faixa_sel = st.selectbox("👤 Filtrar por faixa etária", faixas)

    df_filtrado = df.copy()
    if busca:
        df_filtrado = df_filtrado[df_filtrado["Nome Completo"].str.lower().str.contains(busca.lower(), na=False)]
    if bairro_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Bairro"] == bairro_sel]
    if faixa_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Faixa Etária"] == faixa_sel]

    st.caption(f"{len(df_filtrado)} resultado(s) encontrado(s)")

    colunas_exibir = ["Nome Completo", "Data de Nascimento", "Idade", "Faixa Etária", "Gênero", "Bairro", "Telefone", "Membro Ativo"]
    colunas_existentes = [c for c in colunas_exibir if c in df_filtrado.columns]

    st.dataframe(
        df_filtrado[colunas_existentes].reset_index(drop=True),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")
    # Download
    csv_export = df_filtrado[colunas_existentes].to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button(
        label="⬇️ Exportar lista filtrada (.csv)",
        data=csv_export,
        file_name="membros_filtrados.csv",
        mime="text/csv",
    )
