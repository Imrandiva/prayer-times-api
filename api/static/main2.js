function fetchAPI() {
    fetch('/api')
        .then(response => {
            console.log('API response:', response)
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Display the API data
            displayData(data);
        })
        .catch(error => {
            console.error('Error fetching API data:', error);
        });
}

function displayData(data) {
    // Clear previous data
    const apiDataElement = document.getElementById('apiData');
    apiDataElement.innerHTML = '';

    // Iterate over the data and append to the display section
    for (const [key, value] of Object.entries(data)) {
        const paragraph = document.createElement('p');
        paragraph.textContent = `${key}: ${value}`;
        apiDataElement.appendChild(paragraph);
    }
}

fetchAPI();
