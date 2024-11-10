from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import openai
import pdfplumber
from weasyprint import HTML
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

        # Add alt text or other accessibility features
        accessible_html = add_accessibility_features(text_content)

        # Convert HTML back to PDF
        HTML(string=accessible_html).write_pdf("accessible_output.pdf")

        return send_file("accessible_output.pdf", as_attachment=True)

    except Exception as e:
        return jsonify({"error": f"Error processing PDF: {e}"})

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def add_accessibility_features(text):
    # Here, replace with OpenAI's API or other logic to add alt text,
