---

# Invoice Extractor

This Streamlit web application helps in the extraction process of invoices. It allows users to upload PDF files containing invoices, extracts relevant information, and displays it in a structured format.

## Tools & Technologies

- **Streamlit**: Python library for building interactive web applications.
- **langchain**: Library for natural language processing tasks.
- **Pinecone**: Vector database service for similarity search and recommendation.
- **PyPDF2**: Python library for reading and manipulating PDF files.
- **OpenAI**: API for natural language processing and generation tasks.

## Usage

1. Clone the repository to your local machine.
2. Install the required dependencies listed in `requirements.txt`.
3. Run the `app.py` script using Streamlit.
4. Upload PDF files containing invoices.
5. Click on the "**Extract**" button to initiate the extraction process.

## Features

- Upload one or multiple PDF files containing invoices.
- Extract relevant information from the uploaded PDF files.
- Display extracted information in a structured format.
- Improve efficiency in managing and processing invoices.

## Installation

```bash
git clone https://github.com/Nidhi-Ranawat/Invoice-extractor.git
cd Invoice-extractor
pip install -r requirements.txt
```

## API Keys
Ensure to set up the following API keys before running the application:

Pinecone API Key: Obtained from Pinecone for vector database operations.
OpenAI API Key: Obtained from OpenAI for natural language processing tasks.
Set these API keys as environment variables or directly in the code.
