function fetchData(metric) {
    fetch(`/systeminfo?metric=${metric}`)
        .then(response => response.text())
        .then(data => {
            // Clear previous table content
            document.getElementById("table-header").innerHTML = "";
            document.getElementById("table-body").innerHTML = "";

            // Parse the response and update the table
            parseAndDisplayTable(data);
        })
        .catch(error => {
            console.error("Error fetching data:", error);
            alert("Failed to retrieve data.");
        });
}

function fetchJsonData() {
    fetch(`/systeminfo/json`)
        .then(response => response.json())
        .then(data => {
            // Clear previous table content
            document.getElementById("table-header").innerHTML = "";
            document.getElementById("table-body").innerHTML = "";

            // Display JSON data in the table
            displayJsonTable(data);
        })
        .catch(error => {
            console.error("Error fetching JSON data:", error);
            alert("Failed to retrieve JSON data.");
        });
}

function parseAndDisplayTable(data) {
    const rows = data.split("\n");
    let headersSet = false;

    rows.forEach(row => {
        const [key, value] = row.split(": ");

        if (!headersSet) {
            const headerRow = document.getElementById("table-header");
            headerRow.innerHTML = `<th>Key</th><th>Value</th>`;
            headersSet = true;
        }

        const bodyRow = document.createElement("tr");
        bodyRow.innerHTML = `<td>${key}</td><td>${value}</td>`;
        document.getElementById("table-body").appendChild(bodyRow);
    });
}

function displayJsonTable(data) {
    const keys = Object.keys(data);

    // Set table headers if not already set
    const headerRow = document.getElementById("table-header");
    headerRow.innerHTML = `<th>Metric</th><th>Data</th>`;

    // Loop through data to create rows
    keys.forEach(key => {
        const row = document.createElement("tr");
        row.innerHTML = `<td>${key}</td><td>${JSON.stringify(data[key], null, 2)}</td>`;
        document.getElementById("table-body").appendChild(row);
    });
}
