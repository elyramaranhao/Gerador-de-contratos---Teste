import streamlit as st
from datetime import date
from docx import Document
from io import BytesIO

st.set_page_config(page_title="Gerador de Contrato", layout="centered")
st.title("📄 Gerador de Contrato Automático")

# Formulário
with st.form("formulario"):
    nome = st.text_input("Nome do contratante")
    cpf = st.text_input("CPF")
    endereco = st.text_input("Endereço")
    valor = st.text_input("Valor do contrato (R$)")
    data_inicio = st.date_input("Data de início", date.today())
    data_fim = st.date_input("Data de término", date.today())
    submitted = st.form_submit_button("Gerar contrato")

from io import BytesIO

if submitted:
    doc = Document("modelo_contrato.docx")

    # Substituições seguras
    for p in doc.paragraphs:
        if p.text:
            p.text = p.text.replace("{{NOME}}", nome)
            p.text = p.text.replace("{{CPF}}", cpf)
            p.text = p.text.replace("{{ENDERECO}}", endereco)
            p.text = p.text.replace("{{VALOR}}", valor)
            p.text = p.text.replace("{{DATA_INICIO}}", str(data_inicio))
            p.text = p.text.replace("{{DATA_FIM}}", str(data_fim))

    # CORRETO: buffer em memória com BytesIO
    contrato_em_memoria = BytesIO()
    doc.save(contrato_em_memoria)
    contrato_em_memoria.seek(0)

    st.success("✅ Contrato gerado com sucesso!")

    st.download_button(
        label="📥 Baixar contrato",
        data=contrato_em_memoria.getvalue(),
        file_name=f"Contrato_{nome}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

