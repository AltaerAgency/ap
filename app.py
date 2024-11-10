from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import openai
import pdfplumber
import fitz  # PyMuPDF
import os

app = Flask(__name__)
CORS(app)

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/upload", methods=["POST"])
def upload_pdf():
    try:
        # Save the uploaded PDF
        file = request.files["file"]
        file.save("uploaded.pdf")

        # Extract text from the PDF
        text_content = extract_text_from_pdf("uploaded.pdf")

        # Generate an accessible PDF with the extracted text
        generate_accessible_pdf(text_content, "accessible_output.pdf")

        return send_file("accessible_output.pdf", as_attachment=True)

    except Exception as e:
        return jsonify({"error": f"Error processing PDF: {e}"})

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def generate_accessible_pdf(text, output_path):
    # Create a new PDF with the extracted text
    pdf_document = fitz.open()  # Create a new PDF
    page = pdf_document.new_page()  # Add a new page
    page.insert_text((72, 72), text)  # Insert the text at position (72, 72)
    pdf_document.save(output_path)
    pdf_document.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
