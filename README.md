# Admission Document Upload and Confirmation System

This is a Django-based system that allows users to upload admission documents, extract data using OCR, and confirm the extracted information before saving it.

## Prerequisites

- Python (version 3.7+)
- Django (version 3.2+)
- Tesseract-OCR (for OCR processing)

## Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/Denisganga/chatbot.git
cd chatbot
```

### 2. Setup Virual Environment

```sh
source source venv/bin/activate
pip install -r requirements.txt
```

### 3. Create Superuser

```sh
python manage.py createsuperuser 
```

### 4. Fireup Server

```sh
python manager.py runserver
```

> [!NOTE]
> You can then access the server from http://localhost:8000