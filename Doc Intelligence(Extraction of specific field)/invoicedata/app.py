import os
import json  
import logging
from flask import Flask, request, render_template, jsonify
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.exceptions import HttpResponseError

app = Flask(__name__)

# Form Recognizer credentials and model ID
endpoint = "https://msdocintproject.cognitiveservices.azure.com/"
key = "5bce58fd168e42e2a8f6f425446c0ced"
model_id = "composed_model"  

# Initialize Form Recognizer client
form_recognizer_client = DocumentAnalysisClient(endpoint, AzureKeyCredential(key))

# Configure logging
logging.basicConfig(level=logging.INFO)

# Route to render the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload and document analysis
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Perform document analysis using Azure Form Recognizer
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        with open(file_path, "rb") as f:
            poller = form_recognizer_client.begin_analyze_document(model_id, document=f)
            result = poller.result()

            invoice_results = []
            for document in result.documents:
                invoice_result = extract_invoice_fields(document)
                invoice_results.append(invoice_result)

        # Return formatted JSON response with extracted invoice fields
        return app.response_class(
            response=json.dumps({'invoices': invoice_results}, indent=4, sort_keys=False),
            status=200,
            mimetype='application/json'
        )

    except HttpResponseError as e:
        error_message = f"HTTP Error: {str(e)}"
        logging.error(error_message)
        return jsonify({'error': error_message}), 500

    except Exception as e:
        error_message = f"Error: {str(e)}"
        logging.error(error_message)
        return jsonify({'error': error_message}), 500

# function to extract invoice fields from Form Recognizer result
def extract_invoice_fields(document):
    invoice_result = {}
    invoice_result["Amount Due"] = document.fields.get("Amount Due").value if document.fields.get("Amount Due") else None
    invoice_result["Bill to"] = document.fields.get("Bill to").value if document.fields.get("Bill to") else None
    invoice_result["Date"] = document.fields.get("Date").value if document.fields.get("Date") else None
    invoice_result["Invoice No"] = document.fields.get("Invoice No").value if document.fields.get("Invoice No") else None
    invoice_result["Sales Tax 6.25%"] = document.fields.get("Sales Tax 6.25%").value if document.fields.get("Sales Tax 6.25%") else None
    invoice_result["Sales Tax(USD)"] = document.fields.get("Sales Tax(USD)").value if document.fields.get("Sales Tax(USD)") else None
    invoice_result["Ship to"] = document.fields.get("Ship to").value if document.fields.get("Ship to") else None
    invoice_result["Subtotal"] = document.fields.get("Subtotal").value if document.fields.get("Subtotal") else None
    invoice_result["Tax Rate"] = document.fields.get("Tax Rate").value if document.fields.get("Tax Rate") else None
    invoice_result["Total"] = document.fields.get("Total").value if document.fields.get("Total") else None
    invoice_result["Total(USD)"] = document.fields.get("Total(USD)").value if document.fields.get("Total(USD)") else None

    return invoice_result

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
