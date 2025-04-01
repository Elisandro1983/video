
# Versão final do Res Checker Pro
# Inclui: Validador LED + Calculadora Projeção + Relatório + Assinatura

import streamlit as st

st.set_page_config(page_title="Res Checker Pro", layout="centered")
st.title("📊 Res Checker Pro")

menu = st.radio("Selecione uma ferramenta:", ["📺 Painel de LED (H9)", "🎥 Projeção Blend (Projetores)"])

# =============== PAINEL LED ===============
if menu == "📺 Painel de LED (H9)":
    st.header("📺 Painel de LED - Validador de Resolução")
    modo = st.radio("Modo de cálculo", ["Prático (Windows)", "Técnico (com bits e blanking)"])
    modo_tecnico = modo == "Técnico (com bits e blanking)"
    bits = st.selectbox("Profundidade de cor (bits)", [8, 10, 12]) if modo_tecnico else None
    largura = st.number_input("Largura (px)", min_value=100, value=3840)
    altura = st.number_input("Altura (px)", min_value=100, value=2160)
    framerate = st.selectbox("Frame rate (Hz)", [24, 30, 50, 60, 120], index=3)

    def calcular_largura_banda(largura, altura, framerate, bits, modo_tecnico=False):
        bpp = bits * 3 if bits else 24
        if modo_tecnico:
            largura_total = largura * 1.05
            altura_total = altura * 1.035
            pixels_por_frame = int(largura_total) * int(altura_total)
        else:
            pixels_por_frame = largura * altura
        pixels_por_segundo = pixels_por_frame * framerate
        banda_bps = pixels_por_segundo * bpp
        banda_gbps = banda_bps / 1_000_000_000
        pixel_clock_mhz = pixels_por_segundo / 1_000_000
        return banda_gbps, pixel_clock_mhz

    def calcular_max_resolucao(ratio, altura_max, framerate, bits, limite_banda, limite_pixel_clock, modo_tecnico=False):
        for altura in range(altura_max, 0, -1):
            largura = int(altura * ratio)
            banda, pixel_clock = calcular_largura_banda(largura, altura, framerate, bits, modo_tecnico)
            if banda <= limite_banda and pixel_clock <= limite_pixel_clock:
                return largura, altura
        return None, None

    if st.button("Validar Resolução"):
        banda, pixel_clock = calcular_largura_banda(largura, altura, framerate, bits, modo_tecnico)
        limite_interface = 17.28
        limite_pixel_clock = 600
        st.subheader("📊 Resultado")
        st.markdown(f"**Modo:** {'Técnico' if modo_tecnico else 'Prático'}")
        st.markdown(f"**Resolução:** {largura} x {altura} @ {framerate}Hz")
        st.markdown(f"**Banda estimada:** `{banda:.2f} Gbps`")
        st.markdown(f"**Pixel Clock estimado:** `{pixel_clock:.2f} MHz`")
        if banda <= limite_interface and pixel_clock <= limite_pixel_clock:
            st.success("✅ Compatível com a entrada DP 1.2 da H9")
        else:
            st.error("❌ Não compatível com a entrada da H9")
            if banda > limite_interface:
                st.warning("- A banda excede o limite da interface DP 1.2 (17.28 Gbps)")
            if pixel_clock > limite_pixel_clock:
                st.warning("- O Pixel Clock excede o limite seguro estimado (600 MHz)")
            ratio = largura / altura
            largura_max, altura_max = calcular_max_resolucao(ratio, altura, framerate, bits, limite_interface, limite_pixel_clock, modo_tecnico)
            if largura_max and altura_max:
                st.info(f"📐 Resolução máxima mantendo a proporção {ratio:.3f}: **{largura_max} x {altura_max} @ {framerate}Hz**")

# =============== PROJEÇÃO BLEND ===============
elif menu == "🎥 Projeção Blend (Projetores)":
    st.header("🎥 Calculadora de Projeção - Blend")
    largura_tela = st.number_input("Largura da tela (m)", min_value=1.0, value=10.0)
    altura_tela = st.number_input("Altura da tela (m)", min_value=1.0, value=3.0)
    qtd_proj_horizontal = st.number_input("Quantidade de projetores (horizontal)", min_value=1, value=3)
    margem = st.number_input("Margem de segurança (m)", min_value=0.0, value=0.2)
    blending_percent = st.slider("Blending (%)", 0, 50, 15)
    st.subheader("📄 Informações para Relatório")
    evento = st.text_input("Nome do evento")
    local = st.text_input("Local")
    data = st.date_input("Data")

    if st.button("Gerar Relatório"):
        st.success("📄 Relatório gerado com sucesso!")
        st.markdown(f"**Evento:** {evento}  
**Local:** {local}  
**Data:** {data}")
        st.markdown(f"**Tela:** {largura_tela}m x {altura_tela}m  
**Projetores:** {qtd_proj_horizontal}  
**Blending:** {blending_percent}%  
**Margem:** {margem}m")
        st.info("🖨️ Para imprimir, use `Cmd + P` no navegador ou `Ctrl + P` no Windows.")

# =============== ASSINATURA ===============
st.markdown("""<hr style='margin-top:50px;margin-bottom:10px'>""", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:right; font-size:13px; color:gray;'>"
    "by <a href='https://wa.me/5541999893882' target='_blank' style='text-decoration:none;color:#999;'>"
    "Elisandro Marques</a></div>",
    unsafe_allow_html=True
)
