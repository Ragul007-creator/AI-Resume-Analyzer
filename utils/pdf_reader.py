import fitz

def extract_text_from_pdf(uploaded_file):

    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    resume_text = ""

    for page in pdf:
        resume_text += page.get_text()

    pdf.close()

    return resume_text