import streamlit as st
import pandas as pd
import numpy as np

# Matriz de Similaridade para "Tipo de tosse"
matriz_tosse = {
    "Seca": {"Seca": 1.0, "Com Catarro": 0.5, "Ausente": 0.0},
    "Com Catarro": {"Seca": 0.5, "Com Catarro": 1.0, "Ausente": 0.0},
    "Ausente": {"Seca": 0.0, "Com Catarro": 0.0, "Ausente": 1.0},
}

# Mapeamento de valores ordinais
ordinal_map = {"Leve": 0, "Moderada": 1, "Intensa": 2, "Forte": 2}
ordinal_dor_cabeca_map = {"Nenhuma": 0, "Frontal": 1, "Generalizada": 2}

# Funções de Similaridade
def sim_numerico(a, b, intervalo):
    return max(0, 1 - abs(a - b) / intervalo)

def sim_ordinal(a, b):
    return max(0, 1 - abs(ordinal_map[a] - ordinal_map[b]) / 2)

def sim_binario(a, b):
    return 1.0 if a == b else 0.0

def sim_tosse(a, b):
    return matriz_tosse.get(a, {}).get(b, 0.0)

def sim_ordinal_dor_cabeca(a, b):
    return max(0, 1 - abs(ordinal_dor_cabeca_map[a] - ordinal_dor_cabeca_map[b]) / 2)

# Carrega a base de dados
@st.cache_data
def carregar_base():
    return pd.read_csv("database.csv")

# Interface do Streamlit
st.title("Sistema RBC - Diagnóstico de Covid ou Dengue")

st.header("1. Configuração de Pesos")
default_pesos = {
    "Temperatura corporal": 4,
    "Fadiga": 3,
    "Tipo de tosse": 4,
    "Dor no corpo": 3,
    "Náusea/Vômito": 2,
    "Tipo de dor de cabeça": 3,
    "Idade": 1,
    "Perda de paladar/Olfato": 4
}

pesos = {}
for atributo, valor in default_pesos.items():
    pesos[atributo] = st.slider(f"Peso para {atributo}", 1, 5, valor)

st.header("2. Informações do Caso de Entrada")
entrada = {
    "Temperatura corporal": st.number_input("Temperatura corporal (°C)", 35.0, 42.0, 38.0),
    "Fadiga": st.selectbox("Fadiga", ["Leve", "Moderada", "Intensa"]),
    "Tipo de tosse": st.selectbox("Tipo de tosse", ["Seca", "Com Catarro", "Ausente"]),
    "Dor no corpo": st.selectbox("Dor no corpo", ["Leve", "Moderada", "Forte"]),
    "Náusea/Vômito": st.selectbox("Náusea/Vômito", ["Sim", "Não"]),
    "Tipo de dor de cabeça": st.selectbox("Tipo de dor de cabeça", ["Frontal", "Generalizada", "Nenhuma"]),
    "Idade": st.number_input("Idade", 0, 120, 30),
    "Perda de paladar/Olfato": st.selectbox("Perda de paladar/Olfato", ["Sim", "Não"])
}

if st.button("Calcular Similaridade"):
    df = carregar_base()

    resultados = []
    for _, row in df.iterrows():
        total_peso = sum(pesos.values())

        score = (
            sim_numerico(entrada["Temperatura corporal"], row["Temperatura corporal"], 5.0) * pesos["Temperatura corporal"] +
            sim_ordinal(entrada["Fadiga"], row["Fadiga"]) * pesos["Fadiga"] +
            sim_tosse(entrada["Tipo de tosse"], row["Tipo de tosse"]) * pesos["Tipo de tosse"] +
            sim_ordinal(entrada["Dor no corpo"], row["Dor no corpo"]) * pesos["Dor no corpo"] +
            sim_binario(entrada["Náusea/Vômito"], row["Náusea/Vômito"]) * pesos["Náusea/Vômito"] +
            sim_ordinal_dor_cabeca(entrada["Tipo de dor de cabeça"], row["Tipo de dor de cabeça"]) * pesos["Tipo de dor de cabeça"] +
            sim_numerico(entrada["Idade"], row["Idade"], 100.0) * pesos["Idade"] +
            sim_binario(entrada["Perda de paladar/Olfato"], row["Perda de paladar/Olfato"]) * pesos["Perda de paladar/Olfato"]
        ) / total_peso

        resultados.append(score * 100)  # em porcentagem

    df["Similaridade (%)"] = resultados
    df_ordenado = df.sort_values(by="Similaridade (%)", ascending=False)

    st.subheader("Ranking de Casos Mais Similares")
    st.dataframe(df_ordenado)

    csv = df_ordenado.to_csv(index=False).encode('utf-8')
    st.download_button("Baixar Resultado em CSV", data=csv, file_name="resultados_rbc.csv", mime="text/csv")
