from flask import Flask, request, jsonify, render_template
import pandas as pd
import os

app = Flask(__name__)
uploaded_data = None  # Global variable to store the DataFrame in memory

# Endpoint to render the HTML template
@app.route('/')
def index():
    return render_template('dashboard.html')

# Endpoint to handle CSV upload and send column names for preview
@app.route('/upload', methods=['POST'])
def upload_csv():
    global uploaded_data  # Access the global variable
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file provided"}), 400

    try:
        uploaded_data = pd.read_csv(file)  # Store DataFrame in memory
    except Exception as e:
        return jsonify({"error": "Invalid CSV file format"}), 400

    # Generate HTML preview of the data and column names
    preview_html = uploaded_data.head().to_html(classes="table table-striped")
    columns = uploaded_data.columns.tolist()
    
    return jsonify({"preview": preview_html, "columns": columns})

# Endpoint to process the query based on user input and selected column
@app.route('/process', methods=['POST'])
def process_query():
    global uploaded_data  # Access the DataFrame stored in memory

    if uploaded_data is None:
        return jsonify({"error": "No data available. Please upload a CSV file first."}), 400

    prompt = request.form.get('prompt')
    column = request.form.get('column')
    
    # Check if the selected column exists in the DataFrame
    if column not in uploaded_data.columns:
        return jsonify({"error": f"Column '{column}' not found in the uploaded data."}), 400

    # Filter the dataframe based on the prompt
    result = []
    if prompt.lower() == "average":
        avg = uploaded_data[column].mean()
        result.append({"entity": column, "result": f"Average: {avg:.2f}"})
    elif prompt.lower() == "max":
        max_value = uploaded_data[column].max()
        result.append({"entity": column, "result": f"Max: {max_value}"})
    elif prompt.lower() == "min":
        min_value = uploaded_data[column].min()
        result.append({"entity": column, "result": f"Min: {min_value}"})
    elif prompt.lower() == "mode":
        mode_value = uploaded_data[column].mode().iloc[0]
        result.append({"entity": column, "result": f"Mode: {mode_value}"})
    elif prompt.lower() == "median":
        median_value = uploaded_data[column].median()
        result.append({"entity": column, "result": f"Median: {median_value}"})
    elif prompt.lower() == "variance":
        variance_value = uploaded_data[column].var()
        result.append({"entity": column, "result": f"Variance: {variance_value:.2f}"})
    elif prompt.lower() == "standard deviation":
        std_dev = uploaded_data[column].std()
        result.append({"entity": column, "result": f"Standard Deviation: {std_dev:.2f}"})
    else:
        result.append({"entity": "Error", "result": "Unsupported query. Try 'average', 'max', 'min', 'mode', 'median', 'variance', or 'standard deviation'."})

    return jsonify(result)

if __name__ == '__main__':
    # Ensure the uploads directory exists
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
