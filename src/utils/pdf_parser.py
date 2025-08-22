import PyPDF2


def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    try:
        with open(file_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page_num, page in enumerate(reader.pages):
                text += page.extract_text() or ""
                text += "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text.strip()


if __name__ == "__main__":
    pdf_path = "Resume.pdf"
    extracted_text = extract_text_from_pdf(pdf_path)
    print(extracted_text)
