# 🧩 PDF → Markdown Pipeline

**Conversor avanzado de documentos PDF a Markdown estructurado**, ideal para su uso en asistentes virtuales, sistemas de embeddings, o pipelines de IA (por ejemplo, LibreChat, LangChain, OpenAI File Search, etc).

Este proyecto extrae, limpia y transforma contenido de documentos PDF (papers, informes, manuales técnicos o biomédicos) en texto Markdown semántico, con soporte OCR, detección de tablas y segmentación automática.

---

## 🚀 Características principales

✅ Conversión de PDF a Markdown con estructura semántica (títulos, texto, tablas, listas).  
✅ Limpieza automática de ruido (números de página, saltos de línea, artefactos).  
✅ OCR multilingüe (español e inglés) mediante **Tesseract**.  
✅ Detección y conversión de tablas a formato Markdown.  
✅ División de texto en fragmentos (`chunks`) de tamaño óptimo para embeddings o indexación.  
✅ Compatible con **LibreChat**, **LangChain**, **OpenAI File Search**, y otros frameworks de RAG.  
✅ Integración opcional con **GitHub Actions** para automatizar la conversión al subir nuevos PDFs.

---

## 📂 Estructura del proyecto

```

📁 pdf-to-md-pipeline/
├─ pdf_to_md_advanced.py        # Script principal
├─ requirements.txt             # Dependencias del entorno
├─ .gitignore                   # Archivos a excluir del repo
├─ README.md                    # Este archivo
├─ input_pdfs/                  # Carpeta donde colocar los PDFs de entrada
├─ output_md/                   # Carpeta de salida con los .md generados
└─ .github/
└─ workflows/
└─ convert.yml          # (opcional) Automatización con GitHub Actions

````

---

## 🧠 Requisitos previos

1. **Python 3.10+** instalado  
2. **Tesseract OCR** (para lectura de PDFs escaneados)

### 🔧 Instalación de Tesseract

- **Windows**: [Descarga](https://github.com/UB-Mannheim/tesseract/wiki) e instala Tesseract.  
  Luego agrega su ruta al PATH (ej. `C:\Program Files\Tesseract-OCR`).

- **Ubuntu/Debian**:
  ```bash
  sudo apt install tesseract-ocr
  sudo apt install tesseract-ocr-spa tesseract-ocr-eng


---

## ⚙️ Instalación y uso local

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/<tu-usuario>/pdf-to-md-pipeline.git
cd pdf-to-md-pipeline
```

### 2️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3️⃣ Crear las carpetas de trabajo

```bash
mkdir input_pdfs output_md
```

### 4️⃣ Añadir tus PDFs en `input_pdfs/`

Coloca aquí tus documentos (por ejemplo: `paper1.pdf`, `guia_medica.pdf`).

### 5️⃣ Ejecutar el script

```bash
python pdf_to_md_advanced.py
```

📄 Los archivos convertidos se guardarán en `output_md/`.

---

## 🧩 Ejemplo de uso

Si colocas un archivo `Informe_COVID.pdf` en `input_pdfs/`, el sistema generará:

* `output_md/Informe_COVID.md` → texto completo formateado
* `output_md/Informe_COVID_chunk1.md`, `chunk2.md`, ... → fragmentos listos para embeddings

Cada archivo incluye metadatos YAML como:

```yaml
---
title: "Informe_COVID"
source_file: "input_pdfs/Informe_COVID.pdf"
processed_date: "2025-11-05"
---
```

---

## 🔁 Automatización con GitHub Actions

El flujo opcional `.github/workflows/convert.yml` permite que **cada vez que subas un PDF nuevo**, se genere automáticamente su versión Markdown y se suba al repo.

Ejemplo de ejecución automática:

---

### ⚙️ `.github/workflows/convert.yml`

```yaml
name: Convert PDFs to Markdown

on:
  push:
    paths:
      - 'input_pdfs/*.pdf'

jobs:
  convert:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - name: Run pipeline
        run: python pdf_to_md_advanced.py
      - name: Commit generated files
        run: |
          git config user.name "github-actions"
          git config user.email "actions@github.com"
          git add output_md/*.md
          git commit -m "Auto: PDF converted to Markdown" || echo "No changes"
          git push

```

Esto te permite usar el repositorio como un **repositorio de conocimiento** que se mantiene actualizado sin ejecutar nada localmente.

---

## 🧰 Principales librerías usadas

| Librería                                                            | Función                                        |
| ------------------------------------------------------------------- | ---------------------------------------------- |
| [unstructured](https://github.com/Unstructured-IO/unstructured)     | Análisis estructural y extracción de contenido |
| [markdownify](https://github.com/matthewwithanm/python-markdownify) | Conversión HTML → Markdown                     |
| [langchain](https://github.com/langchain-ai/langchain)              | Segmentación de texto (chunks)                 |
| [pytesseract](https://github.com/madmaze/pytesseract)               | OCR                                            |
| [pdfminer.six](https://github.com/pdfminer/pdfminer.six)            | Soporte de texto en PDFs                       |

---

## 🌐 Uso en GitHub Codespaces (opcional)

Puedes probarlo directamente en la nube, sin instalaciones locales:

1. Abre el repositorio → **Code → Open with Codespaces**
2. Ejecuta:

   ```bash
   pip install -r requirements.txt
   mkdir input_pdfs
   python pdf_to_md_advanced.py
   ```

---

## 🧩 Roadmap (opcional)

* [ ] Añadir extracción de imágenes y gráficos
* [ ] Soporte para conversión directa a JSON estructurado
* [ ] Dashboard Streamlit para cargar y convertir PDFs desde interfaz
* [ ] Integración directa con LangChain VectorStore

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia **MIT**, lo que permite su libre uso, modificación y redistribución con atribución.

---

## ✨ Créditos

Proyecto desarrollado por **Alba Méndez Escribano**
Especialista en Ciencia de Datos e Inteligencia Artificial aplicada al ámbito biomédico.
📧 Contacto profesional: *(puedes añadir si quieres email o perfil LinkedIn)*

---
