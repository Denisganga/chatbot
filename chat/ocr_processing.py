# ocr_processing.py
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from io import BytesIO
import tempfile
import os
def ocr_function(pdf_document):
    # Ensure we get a proper file object from FieldFile
    with pdf_document.open('rb') as file:
        # Create a temporary file and save the content of the uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            temp_pdf.write(file.read())  # Write the content to a temporary PDF
            temp_pdf.close()  # Close the temporary file

            # Now use the temporary file path to process with pdf2image
            pages = convert_from_path(temp_pdf.name, 300)  # Use temp file path for pdf2image

            extracted_text = ''
            for page in pages:
                text = pytesseract.image_to_string(page)
                extracted_text += text + '\n'

            # Clean up the temporary file after processing
            os.remove(temp_pdf.name)

    return extracted_text
def extract_preferred_path(text):
    # Check if the text contains any of the preferred paths
    if 'STEM' in text:
        return 'STEM'
    elif 'Arts and Sports Science' in text:
        return 'Arts and Sports Science'
    elif 'Social Sciences' in text:
        return 'Social Sciences'
    return None

def process_documents(admission_document):
    # Process each document type (result slip, birth certificate, admission letter)
    extracted_data = {}

    # Process result slip if uploaded
    if admission_document.result_slip:
        with admission_document.result_slip.open('rb') as pdf_file:
            result_text = ocr_function(pdf_file)
            extracted_data['result_slip'] = result_text

    # Process birth certificate if uploaded
    if admission_document.birth_certificate:
        with admission_document.birth_certificate.open('rb') as pdf_file:
            birth_text = ocr_function(pdf_file)
            extracted_data['birth_certificate'] = birth_text

    # Process admission letter if uploaded
    if admission_document.admission_letter:
        with admission_document.admission_letter.open('rb') as pdf_file:
            admission_text = ocr_function(pdf_file)
            extracted_data['admission_letter'] = admission_text

            # Extract preferred path from admission letter
            preferred_path = extract_preferred_path(admission_text)
            if preferred_path:
                extracted_data['preferred_path'] = preferred_path

    return extracted_data
