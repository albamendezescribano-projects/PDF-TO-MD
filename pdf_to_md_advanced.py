import os
import pytesseract
from unstructured.partition.pdf import partition_pdf
from markdownify import markdownify as md
from langchain.text_splitter import RecursiveCharacterTextSplitter
from datetime import datetime

# 📁 Carpetas
INPUT_DIR = "input_pdfs"
OUTPUT_DIR = "output_md"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ⚙️ Config splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
    separators=["\n\n", "\n", ".", "!", "?"]
)

def clean_text(text):
    """Limpieza básica de ruido de papers."""
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.lower().startswith("page "):
            continue
        if line.isdigit() or line == "-":
            continue
        cleaned.append(line)
    return " ".join(cleaned)

def format_table(el):
    """Convierte tablas detectadas por unstructured a formato Markdown."""
    try:
        rows = [r.strip() for r in el.text.split("\n") if r.strip()]
        formatted = []
        for i, row in enumerate(rows):
            cols = [c.strip() for c in row.split() if c.strip()]
            if not cols:
                continue
            formatted.append("| " + " | ".join(cols) + " |")
            if i == 0:
                formatted.append("|" + " --- |" * len(cols))
        return "\n".join(formatted)
    except Exception:
        return md(el.text)

def process_pdf(pdf_path):
    """Convierte PDF a Markdown estructurado con OCR y tablas."""
    print(f"📄 Procesando: {pdf_path}")
    doc_name = os.path.splitext(os.path.basename(pdf_path))[0]
    md_path = os.path.join(OUTPUT_DIR, f"{doc_name}.md")

    # 🧩 Usa Unstructured con estrategia avanzada
    elements = partition_pdf(
        filename=pdf_path,
        strategy="hi_res",              # Layout-aware parsing (columnas, figuras)
        infer_table_structure=True,
        extract_images=False,
        include_page_breaks=False,
        ocr_languages="spa+eng"         # OCR para español + inglés
    )

    with open(md_path, "w", encoding="utf-8") as f:
        # 🧾 Metadatos YAML
        f.write("---\n")
        f.write(f"title: \"{doc_name}\"\n")
        f.write(f"source_file: \"{pdf_path}\"\n")
        f.write(f"processed_date: \"{datetime.now().strftime('%Y-%m-%d')}\"\n")
        f.write("---\n\n")

        for el in elements:
            category = getattr(el, "category", "Text")
            text = clean_text(el.text)
            if not text:
                continue

            f.write(f"## {category}\n\n")
            if category == "Table":
                f.write(format_table(el))
            else:
                f.write(md(text))
            f.write("\n\n")

    print(f"✅ Guardado: {md_path}")
    return md_path

def split_markdown(md_path):
    """Divide el Markdown en fragmentos listos para embeddings."""
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()
    chunks = splitter.split_text(text)
    base = os.path.splitext(os.path.basename(md_path))[0]
    for i, chunk in enumerate(chunks):
        chunk_path = os.path.join(OUTPUT_DIR, f"{base}_chunk{i+1}.md")
        with open(chunk_path, "w", encoding="utf-8") as f:
            f.write(chunk)

def main():
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print("⚠️ No hay PDFs en input_pdfs/. Coloca aquí tus documentos.")
        return

    for pdf_file in pdf_files:
        path = os.path.join(INPUT_DIR, pdf_file)
        md_file = process_pdf(path)
        split_markdown(md_file)

    print("\n🎯 Conversión completada. Markdown listo en:", OUTPUT_DIR)

if __name__ == "__main__":
    main()
