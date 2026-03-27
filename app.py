import streamlit as st
import json
from datetime import datetime
import os

ARQUIVO = "financas.json"

# ---------- DADOS ----------
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

def recalcular(dados, user, mes):
    saldo = 0
    entradas = 0
    saidas = 0

    historico = dados["usuarios"][user]["meses"][mes]["historico"]

    for h in historico:
        try:
            valor = float(h.split(": ")[1])
            if h.startswith("+"):
                saldo += valor
                entradas += valor
            else:
                saldo -= valor
                saidas += valor
        except:
            pass

    dados["usuarios"][user]["meses"][mes]["saldo"] = saldo
    dados["usuarios"][user]["meses"][mes]["entradas"] = entradas
    dados["usuarios"][user]["meses"][mes]["saidas"] = saidas

# ---------- INICIO ----------
dados = carregar()

st.set_page_config(page_title="Banco 💚", layout="centered")
st.title("Banco 💚")

# usuário e mês
user = st.text_input("Usuário")
mes = st.text_input("Mês")

if user and mes:
    user = user.lower()
    mes = mes.lower()

    if user not in dados["usuarios"]:
        dados["usuarios"][user] = {"meses": {}}

    if mes not in dados["usuarios"][user]["meses"]:
        dados["usuarios"][user]["meses"][mes] = {
            "saldo": 0,
            "historico": [],
            "entradas": 0,
            "saidas": 0
        }

    info = dados["usuarios"][user]["meses"][mes]

    # ---------- RESUMO ----------
    recalcular(dados, user, mes)
    st.subheader("Resumo")
    st.metric("Saldo", f"R$ {info['saldo']:.2f}")
    st.write(f"Entradas: R$ {info['entradas']:.2f}")
    st.write(f"Saídas: R$ {info['saidas']:.2f}")

    # ---------- ADICIONAR ----------
    st.subheader("Adicionar")

    nome = st.text_input("Nome")
    valor = st.text_input("Valor")
    categoria = st.text_input("Categoria")

    col1, col2 = st.columns(2)

    if col1.button("Entrada 💰"):
        v = ler_valor(valor)
        texto = f"+ {data_atual()} | {nome} ({categoria}): {v:.2f}"
        info["historico"].append(texto)
        salvar(dados)

    if col2.button("Gasto 💸"):
        v = ler_valor(valor)
        texto = f"- {data_atual()} | {nome} ({categoria}): {v:.2f}"
        info["historico"].append(texto)
        salvar(dados)

    # ---------- HISTÓRICO ----------
    st.subheader("Histórico")
    for i, h in enumerate(info["historico"]):
        st.write(f"{i} - {h}")

    # ---------- EDITAR ----------
    st.subheader("Editar")

    idx = st.number_input("Índice para editar", min_value=0, step=1)
    novo_nome = st.text_input("Novo nome")
    novo_valor = st.text_input("Novo valor")

    if st.button("Editar ✏️"):
        if idx < len(info["historico"]):
            tipo = "+" if info["historico"][idx].startswith("+") else "-"
            v = ler_valor(novo_valor)
            info["historico"][idx] = f"{tipo} {data_atual()} | {novo_nome}: {v:.2f}"
            salvar(dados)

    # ---------- REMOVER ----------
    st.subheader("Remover")

    idx_remove = st.number_input("Índice para remover", min_value=0, step=1, key="remover")

    if st.button("Remover 🗑️"):
        if idx_remove < len(info["historico"]):
            info["historico"].pop(idx_remove)
            salvar(dados)

    # ---------- FILTRO ----------
    st.subheader("Filtro")

    termo = st.text_input("Buscar")

    if termo:
        filtrado = [h for h in info["historico"] if termo.lower() in h.lower()]
        for h in filtrado:
            st.write(h)

    # ---------- COMPARAR ----------
    st.subheader("Comparar Meses")

    entrada = st.text_input("Meses (ex: janeiro, fevereiro)")

    if st.button("Comparar 📊"):
        meses = [m.strip().lower() for m in entrada.split(",")]
        for m in meses:
            if m in dados["usuarios"][user]["meses"]:
                saldo = dados["usuarios"][user]["meses"][m]["saldo"]
                st.write(f"{m}: R$ {saldo:.2f}")
            else:
                st.write(f"{m}: sem dados")

    salvar(dados
