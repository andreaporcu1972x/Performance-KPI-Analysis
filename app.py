
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Cliniche Dentali",
    page_icon="🦷",
    layout="wide"
)

# ---------------------------------------------------------
# 1. LETTURA FILE EXCEL
# ---------------------------------------------------------
@st.cache_data
def load_data(file):
    df = pd.read_excel(file, sheet_name="Data_finale")

    # Pulizia nomi colonne
    df.columns = df.columns.str.strip()

    # Ordine corretto dei mesi
    ordine_mesi = ["GENNAIO", "FEBBRAIO", "MARZO", "APRILE", "MAGGIO", "GIUGNO"]
    df["Periodo"] = pd.Categorical(df["Periodo"], categories=ordine_mesi, ordered=True)

    # Margine percentuale
    df["Margine_%"] = df["Margine"] / df["Ricavi"]

    return df


st.title("🦷 Dashboard KPI - Rete Cliniche Dentali")
st.caption("Analisi interattiva di ricavi, costi, pazienti, marginalità e cancellazioni per sede.")

uploaded_file = st.file_uploader(
    "Carica il file Excel",
    type=["xlsx"]
)

if uploaded_file is None:
    st.info("Carica il file Excel `Analisi_KPI_Rete_Cliniche.xlsx` per avviare la dashboard.")
    st.stop()

df = load_data(uploaded_file)

# ---------------------------------------------------------
# 2. FILTRI
# ---------------------------------------------------------
st.sidebar.header("Filtri")

sedi = st.sidebar.multiselect(
    "Sede",
    options=sorted(df["Sede"].dropna().unique()),
    default=sorted(df["Sede"].dropna().unique())
)

prestazioni = st.sidebar.multiselect(
    "Prestazione",
    options=sorted(df["Prestazione"].dropna().unique()),
    default=sorted(df["Prestazione"].dropna().unique())
)

periodi = st.sidebar.multiselect(
    "Periodo",
    options=list(df["Periodo"].cat.categories),
    default=list(df["Periodo"].cat.categories)
)

df_filtrato = df[
    (df["Sede"].isin(sedi)) &
    (df["Prestazione"].isin(prestazioni)) &
    (df["Periodo"].isin(periodi))
].copy()

if df_filtrato.empty:
    st.warning("Nessun dato disponibile con i filtri selezionati.")
    st.stop()

# ---------------------------------------------------------
# 3. KPI PRINCIPALI
# ---------------------------------------------------------
ricavi_totali = df_filtrato["Ricavi"].sum()
costi_totali = df_filtrato["Costi"].sum()
margine_totale = df_filtrato["Margine"].sum()
pazienti_totali = df_filtrato["Pazienti"].sum()
cancellazioni_totali = df_filtrato["Cancellazioni"].sum()
margine_percentuale = margine_totale / ricavi_totali if ricavi_totali else 0
arpu = ricavi_totali / pazienti_totali if pazienti_totali else 0

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Ricavi", f"€ {ricavi_totali:,.0f}")
col2.metric("Costi", f"€ {costi_totali:,.0f}")
col3.metric("Margine", f"€ {margine_totale:,.0f}")
col4.metric("Margine %", f"{margine_percentuale:.1%}")
col5.metric("ARPU", f"€ {arpu:,.0f}")

st.divider()

# ---------------------------------------------------------
# 4. GRAFICI
# ---------------------------------------------------------
ricavi_sede = (
    df_filtrato
    .groupby("Sede", as_index=False)
    .agg(
        Ricavi=("Ricavi", "sum"),
        Costi=("Costi", "sum"),
        Margine=("Margine", "sum"),
        Pazienti=("Pazienti", "sum"),
        Cancellazioni=("Cancellazioni", "sum")
    )
    .sort_values("Ricavi", ascending=False)
)

trend_mese = (
    df_filtrato
    .groupby("Periodo", as_index=False, observed=False)
    .agg(
        Ricavi=("Ricavi", "sum"),
        Costi=("Costi", "sum"),
        Margine=("Margine", "sum"),
        Pazienti=("Pazienti", "sum")
    )
    .dropna(subset=["Periodo"])
)

prestazione = (
    df_filtrato
    .groupby("Prestazione", as_index=False)
    .agg(
        Ricavi=("Ricavi", "sum"),
        Margine=("Margine", "sum"),
        Pazienti=("Pazienti", "sum")
    )
    .sort_values("Ricavi", ascending=False)
)

c1, c2 = st.columns(2)

with c1:
    st.subheader("Ricavi e Margine per sede")
    fig = px.bar(
        ricavi_sede,
        x="Sede",
        y=["Ricavi", "Margine"],
        barmode="group",
        text_auto=".2s"
    )
    fig.update_layout(xaxis_title="", yaxis_title="Valore €", legend_title="")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Trend mensile Ricavi / Costi / Margine")
    fig = px.line(
        trend_mese,
        x="Periodo",
        y=["Ricavi", "Costi", "Margine"],
        markers=True
    )
    fig.update_layout(xaxis_title="", yaxis_title="Valore €", legend_title="")
    st.plotly_chart(fig, use_container_width=True)

c3, c4 = st.columns(2)

with c3:
    st.subheader("Ricavi per prestazione")
    fig = px.bar(
        prestazione,
        x="Prestazione",
        y="Ricavi",
        text_auto=".2s"
    )
    fig.update_layout(xaxis_title="", yaxis_title="Ricavi €")
    st.plotly_chart(fig, use_container_width=True)

with c4:
    st.subheader("Cancellazioni per sede")
    fig = px.bar(
        ricavi_sede.sort_values("Cancellazioni", ascending=False),
        x="Sede",
        y="Cancellazioni",
        text_auto=True
    )
    fig.update_layout(xaxis_title="", yaxis_title="Numero cancellazioni")
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# 5. TABELLA DI DETTAGLIO
# ---------------------------------------------------------
st.divider()
st.subheader("Dettaglio dati")

df_view = df_filtrato.copy()
df_view["Margine_%"] = df_view["Margine_%"].map(lambda x: f"{x:.1%}")

st.dataframe(
    df_view.sort_values(["Sede", "Periodo"]),
    use_container_width=True,
    hide_index=True
)

# ---------------------------------------------------------
# 6. LETTURA CONSULENZIALE
# ---------------------------------------------------------
st.divider()
st.subheader("Lettura business")

top_sede = ricavi_sede.iloc[0]["Sede"]
top_ricavi = ricavi_sede.iloc[0]["Ricavi"]
best_margine = ricavi_sede.sort_values("Margine", ascending=False).iloc[0]["Sede"]

st.write(
    f"""
    La sede con il maggior volume di ricavi è **{top_sede}**, con circa **€ {top_ricavi:,.0f}**.
    La sede con il margine più alto è **{best_margine}**.

    Questa vista aiuta il management a capire:
    - quali sedi generano più fatturato;
    - quali sedi hanno migliore marginalità;
    - dove le cancellazioni possono impattare sulle performance;
    - quali prestazioni contribuiscono maggiormente ai ricavi.
    """
)
