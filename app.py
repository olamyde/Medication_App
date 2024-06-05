from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Read the Excel file into a DataFrame
df = pd.read_excel('/mnt/data/Medication_Remedies_and_Generic_Names.xlsx')

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

if __name__ == '__main__':
    app.run(debug=True)
