from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import os

app = Flask(__name__)

# Read the Excel file into a DataFrame
df = pd.read_excel('/app/Medication_Remedies_and_Generic_Names.xlsx')

# Print column names for debugging
print(df.columns)
print(df.head())  # Debug print to show the first few rows

# Search function
def search_medications(query):
    results = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    print(f"Search results: {results}")  # Debug print
    return results.to_dict(orient='records')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    print(f"Query received: {query}")  # Debug print
    if query:
        results = search_medications(query)
        print(f"Results found: {results}")  # Debug print
        return jsonify(results)
    return jsonify([])

@app.route('/', methods=['GET'])
def home():
    return send_from_directory(os.getcwd(), 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
