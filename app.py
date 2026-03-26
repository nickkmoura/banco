import streamlit as st
import json
from datetime import datetime
import os

ARQUIVO = "financas.json"

# -------- DADOS --------
def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO, "r") as f:
            return json.load(f)
    return {"usuarios": {}}

def salvar(dados):
    with open(ARQUIVO, "w") as f:
        json.dump(dados, f, indent=4)

def data_atual():
    return datetime.now().strftime("%d/%m")

def ler_valor(valor):
    try:
        return float(valor.replace(",", "."))
    except:
        return 0

dados = carregar()

# -------- UI --------
st.set_page_config(page_title="Banco 💚", layout="centered")
st.title("Banco 💚")

# usuário
user = st.text_input("Usuário")
if user:
    user = user.lower()
    if user not in dados["usuarios"]:
        dados["usuarios"][user] = {"meses": {}}

# mês
mes = st.text_input("Mês")
if user and mes:
    mes = mes.lower()
    if mes not in dados["usuarios"][user]["meses"]:
        dados["usuarios"][user]["meses"][mes] = {
            "saldo": 0,
            "historico": [],
            "entradas": 0,
            "saidas": 0
        }

# adicionar
if user and mes:
    st.subheader("Adicionar")

    nome = st.text_input("Nome")
    valor = st.text_input("Valor")
    categoria = st.text_input("Categoria")

    col1, col2 = st.columns(2)

    if col1.button("Entrada 💰"):
        v = ler_valor(valor)
        texto = f"+ {data_atual()} | {nome} ({categoria}): {v:.2f}"
        dados["usuarios"][user]["meses"][mes]["historico"].append(texto)

    if col2.button("Gasto 💸"):
        v = ler_valor(valor)
        texto = f"- {data_atual()} | {nome} ({categoria}): {v:.2f}"
        dados["usuarios"][user]["meses"][mes]["historico"].append(texto)

    # recalcular
    saldo = 0
    entradas = 0
    saidas = 0

    for h in dados["usuarios"][user]["meses"][mes]["historico"]:
        valor = float(h.split(": ")[1])
        if h.startswith("+"):
            saldo += valor
            entradas += valor
        else:
            saldo -= valor
            saidas += valor

    dados["usuarios"][user]["meses"][mes]["saldo"] = saldo
    dados["usuarios"][user]["meses"][mes]["entradas"] = entradas
    dados["usuarios"][user]["meses"][mes]["saidas"] = saidas

    salvar(dados)

    # resumo
    st.subheader("Resumo")
    st.write(f"Saldo: R$ {saldo:.2f}")
    st.write(f"Entradas: R$ {entradas:.2f}")
    st.write(f"Saídas: R$ {saidas:.2f}")

    # histórico
    st.subheader("Histórico")
    for h in dados["usuarios"][user]["meses"][mes]["historico"]:
        st.write(h)
