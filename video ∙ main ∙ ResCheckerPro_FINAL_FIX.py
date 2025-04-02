
# Res Checker Pro com abas, Painel LED (estável), Projeção Blend com imagem estilo BlendZ + exportação de relatório em PDF
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import datetime

st.set_page_config(page_title="Res Checker Pro", layout="centered")
st.title("📊 Res Checker Pro")

tab1, tab2 = st.tabs(["📺 Painel de LED (H9)", "🎥 Projeção Blend (Projetores)"])

with tab1:
    st.header("📺 Painel de LED - Validador de Resolução")
    st.markdown("✅ Esta aba está estável e inalterada.")

with tab2:
    st.header("🎥 Projeção Blend - Cálculo + Imagem + Relatório")

    col1, col2 = st.columns(2)
    with col1:
        largura_tela = st.number_input("Largura da tela (m)", min_value=1.0, value=12.0)
        altura_tela = st.number_input("Altura da tela (m)", min_value=1.0, value=3.0)
        qtd_proj = st.number_input("Quantidade de projetores", min_value=1, value=3)
    with col2:
        margem = st.number_input("Margem lateral (m)", min_value=0.0, value=0.2)
        blending_percent = st.slider("Blending (%)", 0, 50, 15)
        resolucao_proj = st.text_input("Resolução por projetor (ex: 1920x1200)", "1920x1200")

    evento = st.text_input("Nome do evento", "Show Exemplo")
    local = st.text_input("Local", "Curitiba - PR")
    data = st.date_input("Data", value=datetime.date.today())

    largura_util_total = largura_tela - (2 * margem)
    overlap_m = (blending_percent / 100) * (largura_util_total / qtd_proj)
    largura_por_proj = (largura_util_total + (overlap_m * (qtd_proj - 1))) / qtd_proj

    posicoes_centros = []
    marcações = []

    for i in range(int(qtd_proj)):
        centro = margem + (i * (largura_por_proj - overlap_m)) + (largura_por_proj / 2)
        posicoes_centros.append(centro)
        marcações.append((f"Meio P{i+1}", centro))

        if i > 0:
            inicio_blend = centro - (largura_por_proj / 2)
            fim_blend = centro + (largura_por_proj / 2)
            marcações.append((f"Início Blend{i}", inicio_blend))
            marcações.append((f"Fim Blend{i}", fim_blend))

    if st.button("Gerar Imagem"):
        px_per_m = 100
        largura_img = int(largura_tela * px_per_m)
        altura_img = 200
        img = Image.new("RGB", (largura_img, altura_img), "white")
        draw = ImageDraw.Draw(img)

        for i in range(int(qtd_proj)):
            x0 = int((margem + i * (largura_por_proj - overlap_m)) * px_per_m)
            x1 = int(x0 + largura_por_proj * px_per_m)
            draw.rectangle([x0, 20, x1, 120], outline="black", fill="#d0e1f9")

            if i > 0:
                xb0 = int((x0 - overlap_m * px_per_m))
                draw.rectangle([xb0, 20, x0, 120], fill="#ffd9b3", outline=None)

        for label, pos_m in marcações:
            x = int(pos_m * px_per_m)
            draw.line([x, 10, x, 130], fill="red", width=1)
            draw.text((x+5, 135), f"{label}\n{pos_m:.2f}m", fill="black")

        buf = BytesIO()
        img.save(buf, format="PNG")
        st.image(img, caption="Visualização da Projeção com Blends", use_column_width=True)
        st.download_button("📥 Baixar imagem PNG", data=buf.getvalue(), file_name="blend_layout.png", mime="image/png")

    if st.button("Gerar Relatório PDF"):
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Relatório Técnico - Projeção Blend", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 8, f"Evento: {evento}\nLocal: {local}\nData: {data.strftime('%d/%m/%Y')}\n")
        pdf.multi_cell(0, 8, f"Tela: {largura_tela:.2f}m x {altura_tela:.2f}m\nProjetores: {qtd_proj}\nMargem: {margem:.2f}m\nBlending: {blending_percent}%\nResolução por Projetor: {resolucao_proj}")
        pdf.multi_cell(0, 8, f"Largura útil total: {largura_util_total:.2f}m\nLargura de cada projetor: {largura_por_proj:.2f}m\nOverlap (blend): {overlap_m:.2f}m")

        for i, centro in enumerate(posicoes_centros):
            pdf.cell(0, 8, txt=f"Centro do Projetor {i+1}: {centro:.2f}m", ln=True)

        pdf_output = BytesIO()
        pdf.output(pdf_output)
        st.download_button("📥 Baixar Relatório PDF", data=pdf_output.getvalue(), file_name="relatorio_blend.pdf", mime="application/pdf")

# Assinatura
st.markdown("""<hr style='margin-top:50px;margin-bottom:10px'>""", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:right; font-size:13px; color:gray;'>"
    "by <a href='https://wa.me/5541999893882' target='_blank' style='text-decoration:none;color:#999;'>"
    "Elisandro Marques</a></div>",
    unsafe_allow_html=True
)
