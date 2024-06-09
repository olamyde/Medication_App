from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import os

app = Flask(__name__)

# Read the Excel file into a DataFrame
df = pd.read_excel('/app/Medication_Remedies_and_Generic_Names.xlsx')

# Search function
def search_medications(query):
    results = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    return results.to_dict(orient='records')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if query:
        results = search_medications(query)
        return jsonify(results)
    return jsonify([])

@app.route('/', methods=['GET'])
def home():
    return send_from_directory(os.getcwd(), 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
