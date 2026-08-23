from PyPDF2 import PdfReader
from docx import Document


def read_pdf(uploaded_file):
    pdf = PdfReader(uploaded_file)
    text = ""

    for page in pdf.pages:
        text += page.extract_text() + "\n"

    return text


def read_docx(uploaded_file):
    doc = Document(uploaded_file)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


def read_txt(uploaded_file):
    return uploaded_file.read().decode("utf-8")


def extract_resume_text(uploaded_file):

    if uploaded_file is None:
        return ""

    file_type = uploaded_file.name.split(".")[-1]

    if file_type == "pdf":
        return read_pdf(uploaded_file)

    elif file_type == "docx":
        return read_docx(uploaded_file)

    elif file_type == "txt":
        return read_txt(uploaded_file)

    return ""