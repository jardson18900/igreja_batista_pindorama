# ✝️ Igreja Batista de Pindorama — Painel de Gestão de Membros

Projeto de extensão desenvolvido para a disciplina **Tópicos de Big Data em Python**  
Universidade Estácio de Sá — Semestre 2026.1

**Alunos:** Jardson Gabriel de Lima Silva · Juan Jorge de Melo Marques  
**Professora:** Fabiana Azevedo

---

## 📦 Como rodar localmente

### 1. Pré-requisitos
- Python 3.9 ou superior instalado
- pip atualizado

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Gerar os dados de demonstração (primeira vez)
```bash
python gerar_dados.py
```

### 4. Rodar o app
```bash
streamlit run app.py
```

O navegador abre automaticamente em `http://localhost:8501`

---

## ☁️ Deploy gratuito no Streamlit Cloud

1. Suba o projeto para um repositório público no GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte o repositório e selecione `app.py` como arquivo principal
4. Clique em **Deploy** — pronto, o link funciona no celular!

---

## 📁 Estrutura do projeto

```
igreja_app/
├── app.py              # Dashboard principal (Streamlit)
├── gerar_dados.py      # Gerador de dados fake para demonstração
├── dados_membros.csv   # CSV com 100 membros fictícios
├── requirements.txt    # Dependências Python
└── README.md           # Este arquivo
```

---

## 🔄 Fluxo de dados

```
Google Forms (coleta)
        ↓
   CSV exportado
        ↓
 Python + Pandas (ETL: limpeza, normalização, cálculo de idade/faixa)
        ↓
  Streamlit (dashboard interativo)
```

---

## 📊 Funcionalidades

| Tela | Funcionalidades |
|------|----------------|
| Visão Geral | Total de membros, membros ativos, aniversários do mês, idade média, gráficos de faixa etária, bairro e gênero |
| Aniversariantes | Lista do mês atual ordenada por dia, preview do próximo mês |
| Membros | Busca por nome, filtros por bairro e faixa etária, exportação CSV |

---

## 📋 Campos do formulário (Google Forms)

Para compatibilidade total com o sistema, o formulário deve coletar:

| Campo | Tipo |
|-------|------|
| Nome Completo | Texto curto |
| Data de Nascimento | Data (DD/MM/AAAA) |
| Gênero | Múltipla escolha |
| Bairro | Texto curto |
| Telefone | Texto curto |
| Email | Email |
| Membro Ativo | Múltipla escolha (Sim / Não) |

> O CSV exportado do Google Forms deve ter esses nomes **exatamente** como cabeçalho das colunas.
