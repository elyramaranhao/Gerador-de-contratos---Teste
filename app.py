import streamlit as st
from datetime import date
from docx import Document
import tempfile

st.set_page_config(page_title="Gerador de Contratos", layout="centered")
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

# Quando o botão for clicado
if submitted:
    doc = Document("modelo_contrato.docx")

    for p in doc.paragraphs:
        p.text = p.text.replace("{{NOME}}", nome)
        p.text = p.text.replace("{{CPF}}", cpf)
        p.text = p.text.replace("{{ENDERECO}}", endereco)
        p.text = p.text.replace("{{VALOR}}", valor)
        p.text = p.text.replace("{{DATA_INICIO}}", str(data_inicio))
        p.text = p.text.replace("{{DATA_FIM}}", str(data_fim))

 with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
    doc.save(tmp.name)
    tmp_path = tmp.name  # salva o caminho do arquivo

st.success("✅ Contrato gerado com sucesso!")

# Lê o arquivo depois de fechar o with
with open(tmp_path, "rb") as file:
    st.download_button(
        label="📥 Baixar contrato",
        data=file.read(),
        file_name=f"Contrato_{nome}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )


