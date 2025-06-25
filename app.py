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

# Se clicou no botão
import os
import tempfile

if submitted:
    # Abre o modelo
    doc = Document("modelo_contrato.docx")

    # Substitui os campos
    for p in doc.paragraphs:
        p.text = p.text.replace("{{NOME}}", nome)
        p.text = p.text.replace("{{CPF}}", cpf)
        p.text = p.text.replace("{{ENDERECO}}", endereco)
        p.text = p.text.replace("{{VALOR}}", valor)
        p.text = p.text.replace("{{DATA_INICIO}}", str(data_inicio))
        p.text = p.text.replace("{{DATA_FIM}}", str(data_fim))

    # Cria arquivo temporário no disco
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
        temp_path = tmp_file.name
        doc.save(temp_path)

    # Lê o conteúdo do arquivo salvo
    with open(temp_path, "rb") as f:
        contrato_bytes = f.read()

    # Remove o arquivo temporário do disco
    os.remove(temp_path)

    # Exibe botão de download
    st.success("✅ Contrato gerado com sucesso!")
    st.download_button(
        label="📥 Baixar contrato",
        data=contrato_bytes,
        file_name=f"Contrato_{nome}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
