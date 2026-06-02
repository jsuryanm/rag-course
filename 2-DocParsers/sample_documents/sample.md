# Document Parsing Best Practices

A comprehensive guide to document parsing for RAG systems.

## Table of Contents

1. [Introduction](#introduction)
2. [Supported Formats](#supported-formats)
3. [Parsing Strategies](#parsing-strategies)
4. [Integration Guide](#integration-guide)

---

## Introduction

Document parsing is a critical component in modern AI applications. It enables the extraction of structured information from unstructured documents, making it possible to:

- Build searchable knowledge bases
- Create training datasets for machine learning
- Enable semantic search and retrieval
- Power question-answering systems

> **Note:** The quality of document parsing directly impacts the performance of downstream AI applications.

## Supported Formats

### Primary Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| PDF | `.pdf` | Portable Document Format |
| Word | `.docx` | Microsoft Word documents |
| Excel | `.xlsx` | Microsoft Excel spreadsheets |
| PowerPoint | `.pptx` | Microsoft PowerPoint presentations |
| HTML | `.html` | Web pages |
| Markdown | `.md` | Plain text formatting |

### Additional Formats

- **Images**: PNG, JPEG, TIFF, BMP
- **Audio**: WAV, MP3 (via ASR)
- **XML**: JATS, USPTO patents

## Parsing Strategies

### 1. Standard Pipeline

The standard pipeline is suitable for most documents:

```python
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("document.pdf")
```

**Features:**
- Layout analysis
- Table structure detection
- OCR for scanned pages
- Reading order determination

### 2. VLM Pipeline

For complex documents, use Vision-Language Models:

```python
from docling.pipeline.vlm_pipeline import VlmPipeline

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_cls=VlmPipeline,
        ),
    }
)
```

**Benefits:**
- Better understanding of visual elements
- Improved accuracy for complex layouts
- End-to-end document understanding

### 3. OCR Configuration

Choose the right OCR engine for your needs:

| Engine | Best For | Platform |
|--------|----------|----------|
| RapidOCR | General use | Cross-platform |
| EasyOCR | Multi-language | Cross-platform |
| Tesseract | Production | Cross-platform |
| OcrMac | macOS native | macOS only |

## Integration Guide

### With LangChain

```python
from langchain_docling import DoclingLoader

loader = DoclingLoader(
    file_path="document.pdf",
    export_type=ExportType.DOC_CHUNKS
)
docs = loader.load()
```

### With Vector Stores

```python
from langchain_community.vectorstores import Chroma

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
```

---

## Summary

- Document parsing is essential for RAG applications
- Multiple formats are supported out of the box
- Choose the right pipeline for your use case
- Integration with popular frameworks is straightforward

---

*This document was created for the Docling tutorial.*
