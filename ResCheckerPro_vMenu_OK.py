
# Res Checker Pro - Versão Web
# Tela inicial com menu, validador de LED, projeção blend, relatório e assinatura

import streamlit as st

st.set_page_config(page_title="Res Checker Pro", layout="centered")
st.title("📊 Res Checker Pro")

menu = st.radio("Selecione uma ferramenta:", ["📺 Painel de LED (H9)", "🎥 Projeção Blend (Projetores)"])

if menu == "📺 Painel de LED (H9)":
    st.write("Painel de LED - módulo de validação de resolução.")
    # Conteúdo do validador seria aqui

elif menu == "🎥 Projeção Blend (Projetores)":
    st.write("Calculadora de projeção - entrada de dados e relatório.")
    # Conteúdo da calculadora de projeção

st.markdown("""<hr style='margin-top:50px;margin-bottom:10px'>""", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:right; font-size:13px; color:gray;'>"
    "by <a href='https://wa.me/5541999893882' target='_blank' style='text-decoration:none;color:#999;'>"
    "Elisandro Marques</a></div>",
    unsafe_allow_html=True
)
