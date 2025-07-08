import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Análise de Sortido - Areas", layout="wide")
st.title("🌟 Análise de Rentabilidade do Sortido - Areas")

uploaded_file = st.file_uploader("Carrega o ficheiro CSV com os dados do sortido:", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Visão Geral dos Dados")
    st.dataframe(df)

    if "Margem Unitária (€)" not in df.columns:
        df["Margem Unitária (€)"] = df["Preço de Venda (€)"] - df["Preço de Custo (€)"]
    if "Margem (%)" not in df.columns:
        df["Margem (%)"] = (df["Margem Unitária (€)"] / df["Preço de Venda (€)"]) * 100
    if "Rentabilidade Total (€)" not in df.columns:
        df["Rentabilidade Total (€)"] = df["Margem Unitária (€)"] * df["Vendas Últimos 12 Meses (Unidades)"]

    df["Ranking Rentabilidade"] = df["Rentabilidade Total (€)"].rank(ascending=False).astype(int)

    st.subheader("🔄 Indicadores")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Vendas (Unidades)", int(df["Vendas Últimos 12 Meses (Unidades)"].sum()))
    col2.metric("Rentabilidade Total (€)", f"{df['Rentabilidade Total (€)'].sum():,.2f} €")
    col3.metric("Margem Média (%)", f"{df['Margem (%)'].mean():.1f}%")

    st.subheader("📈 Rentabilidade por Categoria")
    fig_bar = px.bar(df, x="Categoria", y="Rentabilidade Total (€)", color="Categoria",
                     title="Rentabilidade Total por Categoria",
                     labels={"Rentabilidade Total (€)": "Rentabilidade (€)"},
                     height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("🔍 Produtos Estrela e Críticos")
    col4, col5 = st.columns(2)
    with col4:
        st.markdown("**Top 5 Produtos Estrela (Alta Margem + Altas Vendas)**")
        estrelas = df[(df["Margem (%)"] > 60) & (df["Vendas Últimos 12 Meses (Unidades)"] > 800)]
        st.dataframe(estrelas.sort_values("Rentabilidade Total (€)", ascending=False).head(5))
    with col5:
        st.markdown("**Top 5 Produtos Críticos (Baixa Margem + Baixas Vendas)**")
        criticos = df[(df["Margem (%)"] < 30) & (df["Vendas Últimos 12 Meses (Unidades)"] < 500)]
        st.dataframe(criticos.sort_values("Rentabilidade Total (€)").head(5))

    st.subheader("🔹 Dispersão: Vendas vs Margem")
    fig_scatter = px.scatter(df, x="Vendas Últimos 12 Meses (Unidades)", y="Margem (%)",
                             color="Categoria", size="Rentabilidade Total (€)",
                             hover_name="Nome do Produto",
                             title="Dispersão entre Vendas e Margem",
                             height=500)
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.subheader("🔢 Ranking Completo de Rentabilidade")
    st.dataframe(df.sort_values("Rentabilidade Total (€)", ascending=False))

else:
    st.info("Por favor, carrega um ficheiro CSV para iniciar a análise.")
