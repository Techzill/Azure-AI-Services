from flask import Flask, request, jsonify, render_template
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

app = Flask(__name__)

# Azure Form Recognizer credentials and endpoint
endpoint = "https://msdocintproject.cognitiveservices.azure.com/"
key = "5bce58fd168e42e2a8f6f425446c0ced"
model_id = "composed_model"  

# Initialize Form Recognizer client
credential = AzureKeyCredential(key)
document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=credential)

# Route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to handle document upload and table extraction
@app.route('/extract_tables', methods=['POST'])
def extract_tables():
    try:
        # Check if file is present in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files['file']

        # Perform table extraction
        poller = document_analysis_client.begin_analyze_document(model_id=model_id, document=file)
        result = poller.result()

        # Prepare the response data
        tables = []
        for table in result.tables:
            table_data = []

            # Collect cell details by rows
            rows = {}
            for cell in table.cells:
                row_index = cell.row_index
                col_index = cell.column_index
                if row_index not in rows:
                    rows[row_index] = {}
                rows[row_index][col_index] = cell.content

            # Convert rows to list of lists
            for row_index, columns in sorted(rows.items()):
                table_data.append([columns.get(i, "") for i in range(len(columns))])

            tables.append({
                "table_number": 1,
                "rows": table_data
            })

        return jsonify({"tables": tables}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
