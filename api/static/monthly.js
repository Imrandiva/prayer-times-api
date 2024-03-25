document.addEventListener("DOMContentLoaded", () => {
    // const url = "https://prayer-times-api-gamma.vercel.app/api/stockholm";
    const loadingSpinner = document.getElementById("loadingSpinner");

    // // const cachedData = localStorage.getItem("cachedData");


    // // Get todays month
    // let today = new Date();
    // let day = today.getDate();
    // let month = today.toLocaleString('default', { month: 'short' });
    // month = month.charAt(0).toUpperCase() + month.slice(1);
    // let weekday = today.toLocaleDateString('en-US', { weekday: 'short' });

    // // Format the date as "Weekday Day Month"
    // let todayFormatted = `${weekday} ${day} ${month}`.replace('.', '');
    // //&& cachedData. month === month

    // // Fixa så vi updaterar cahce varje månad
    // if (cachedData ) {
    //     const jsonData = JSON.parse(cachedData);

    //     if (jsonData[todayFormatted] === undefined) {
    //         fetchPrayerData(url, loadingSpinner);
    //         return
    //     }

    //     loadingSpinner.style.display = "none";
    //     displayPrayerTimes(jsonData);
    // } else {
        fetchAPI(loadingSpinner);
    // }
});



function fetchAPI(loadingSpinner) {
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
            loadingSpinner.style.display = "none";
            getMonthlyPrayerTimes(data);
        })
        .catch(error => {
            console.error('Error fetching API data:', error);
        });
}

// Get the data from the cache
function checkCache(url) {
    return caches.open('api-cache')
        .then(cache => cache.match(url))
        .then(response => (response ? response.json() : null));
}


// Update the cache with new data
function updateCache(url, data) {
    caches.open('api-cache').then(cache => {
        const response = new Response(JSON.stringify(data));
        cache.put(url, response);
    });
}


function getMonthlyPrayerTimes(json) {
    const tbody = document.querySelector('tbody');

    let today = getTodaysDate();

    for (const [date, times] of Object.entries(json)) {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${date}</td><td>${times.Fajr}</td><td>${times.Sunrise}</td><td>${times.Dhuhr}</td><td>${times.Asr}</td><td>${times.Maghrib}</td><td>${times["Isha'a"]}</td>`;
        console.log(date, today)
        if (date == today) {
            row.style.backgroundColor = 'lightblue';
            tbody.appendChild(row);

            row.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            tbody.appendChild(row);
        }
    }
}

function getTodaysDate() {
    let today = new Date();
    let day = today.getDate();
    let month = today.toLocaleString('en-US', { month: 'short' });
    month = month.substring(0, 3); 
    month = month.charAt(0).toUpperCase() + month.slice(1); // Capitalize the first letter
    let weekday = today.toLocaleDateString('en-US', { weekday: 'short' });
    let todayFormatted = `${weekday} ${day} ${month}`;

    return todayFormatted;
}



