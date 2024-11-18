document.getElementById('fileUploadForm').onsubmit = async function (e) {
    e.preventDefault();
    let formData = new FormData(this);

    // Upload CSV and preview data with available columns
    let response = await fetch('/upload', { method: 'POST', body: formData });
    let data;
    try {
        data = await response.json();
    } catch (error) {
        console.error("Failed to parse JSON:", error);
        alert("An error occurred while processing your request. Please try again.");
        return;
    }

    if (response.ok) {
        // Display preview of the data
        document.getElementById('preview').innerHTML = data.preview;

        // Populate the column selection dropdown
        let columnSelect = document.getElementById('columnSelect');
        columnSelect.innerHTML = "";  // Clear previous options

        data.columns.forEach(colName => {
            let option = document.createElement('option');
            option.value = colName;
            option.textContent = colName;
            columnSelect.appendChild(option);
        });
    } else {
        alert("Failed to upload file: " + data.error);
    }
};

async function submitQuery() {
    let promptInput = document.getElementById('promptInput').value;
    let columnSelect = document.getElementById('columnSelect').value;
    
    if (!promptInput || !columnSelect) {
        alert("Please upload a CSV file, select a column, and enter a query.");
        return;
    }

    let formData = new FormData();
    formData.append('prompt', promptInput);
    formData.append('column', columnSelect);

    let response = await fetch('/process', { method: 'POST', body: formData });
    let data;
    try {
        data = await response.json();
    } catch (error) {
        console.error("Failed to parse JSON:", error);
        alert("An error occurred while processing your request. Please try again.");
        return;
    }

    if (response.ok) {
        // Display results in the result container
        let resultContainer = document.getElementById('resultContainer');
        resultContainer.innerHTML = '';  // Clear previous results

        data.forEach(item => {
            let resultDiv = document.createElement('div');
            resultDiv.innerHTML = `<strong>${item.entity}</strong>: ${item.result}`;

            resultContainer.appendChild(resultDiv);
        });
    } else {
        alert("Error: " + data.error);
    }
}
