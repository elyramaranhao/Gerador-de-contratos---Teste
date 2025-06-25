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

if submitted:
    # Carrega o modelo
    doc = Document("modelo_contrato.docx")

    # Substitui os placeholders
    for p in doc.paragraphs:
        if "{{NOME}}" in p.text:
            p.text = p.text.replace("{{NOME}}", nome)
        if "{{CPF}}" in p.text:
            p.text = p.text.replace("{{CPF}}", cpf)
        if "{{ENDERECO}}" in p.text:
            p.text = p.text.replace("{{ENDERECO}}", endereco)
        if "{{VALOR}}" in p.text:
            p.text = p.text.replace("{{VALOR}}", valor)
        if "{{DATA_INICIO}}" in p.text:
            p.text = p.text.replace("{{DATA_INICIO}}", str(data_inicio))
        if "{{DATA_FIM}}" in p.text:
            p.text = p.text.replace("{{DATA_FIM}}", str(data_fim))

    # Salva o contrato em memória
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.success("✅ Contrato gerado com sucesso!")
    st.download_button(
        label="📥 Baixar contrato",
        data=buffer.getvalue(),  # lê os bytes diretamente
        file_name=f"Contrato_{nome}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
