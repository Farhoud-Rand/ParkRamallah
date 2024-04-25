document.addEventListener('DOMContentLoaded', function () {
    // Load all parks when the page loads
    loadAllParks();

    // Load user reservations when the page loads
    loadReservations();

    // Add any additional initialization code here
});

// Function to load all parks
function loadAllParks() {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', '/all_parks/', true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            const parks = JSON.parse(xhr.responseText);
            updateParkResults(parks);
        } else {
            console.error('Failed to fetch all parks');
        }
    };
    xhr.send();
}

// Function to load user reservations
function loadReservations() {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', '/user/reservations/', true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            const reservations = JSON.parse(xhr.responseText);
            displayReservations(reservations);
        } else {
            console.error('Failed to fetch user reservations');
        }
    };
    xhr.send();
}

// Function to update park results
function updateParkResults(parks) {
    const parkResultsContainer = document.getElementById('parkResults');
    parkResultsContainer.innerHTML = '';

    parks.forEach(park => {
        const col = document.createElement('div');
        col.className = 'col-md-4';
        col.innerHTML = `
            <div class="card mb-3 text-center">
                <div class="card-body">
                    <h5 class="card-title">${park.name}</h5>
                    <p class="card-text">Location: ${park.location}</p>
                    <p class="card-text">Type: ${park.type}</p>
                    <a href="#" class="btn btn-success">Reserve</a>
                </div>
            </div>
        `;
        parkResultsContainer.appendChild(col);
    });
}

// Function to display user reservations
function displayReservations(reservations) {
    const reservationsAccordion = document.getElementById('reservationsAccordion');
    reservations.forEach(reservation => {
        const accordionItem = document.createElement('div');
        accordionItem.className = 'accordion-item';
        accordionItem.innerHTML = `
            <h2 class="accordion-header">
                <button class="accordion-button collapsed bg-light text-dark fw-bold" type="button" data-bs-toggle="collapse" data-bs-target="#collapse${reservation.id}" aria-expanded="false" aria-controls="collapse${reservation.id}">
                    Reservation ${reservation.id} 
                    <span class="badge bg-${reservation.status.toLowerCase() === 'active' ? 'primary' : 'secondary'} rounded-pill mx-3">${reservation.status}</span>
                </button>
            </h2>
            <div id="collapse${reservation.id}" class="accordion-collapse collapse" aria-labelledby="heading${reservation.id}" data-bs-parent="#reservationsAccordion">
                <div class="accordion-body">
                    <ul class="list-group">
                        <li class="list-group-item">Park Number: ${reservation.parkNumber}</li>
                        <li class="list-group-item">Arrival Time: ${reservation.arrivalTime}</li>
                        <li class="list-group-item">Departure Time: ${reservation.departureTime}</li>
                    </ul>
                    <div class="mt-3">
                        <button type="button" class="btn btn-warning me-2">Edit Reservation</button>
                        <button type="button" class="btn btn-danger">Delete Reservation</button>
                    </div>
                </div>
            </div>
        `;
        reservationsAccordion.appendChild(accordionItem);
    });
}

function search() {
    const location = document.getElementById('location').value;
    const type = document.getElementById('type').value;
    const name = document.getElementById('name').value; 

    const xhr = new XMLHttpRequest();
    xhr.open('GET', `/search/?location=${location}&type=${type}&name=${name}`, true); 

    xhr.onload = function () {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            updateParkResults(response);  // Update park results with the search response
        } else {
            console.error('Failed to fetch search results');
        }
    };
    xhr.send();
}
