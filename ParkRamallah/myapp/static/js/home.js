function search() {
    const location = document.getElementById('location').value;
    const type = document.getElementById('type').value;

    const xhr = new XMLHttpRequest();
    xhr.open('GET', `/search/?location=${location}&type=${type}`, true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            updateParkResults(response.parks);
        } else {
            console.error('Failed to fetch search results');
        }
    };
    xhr.send();
}

function updateParkResults(parks) {
    const parkResultsContainer = document.getElementById('parkResults');
    parkResultsContainer.innerHTML = '';

    parks.forEach(park => {
        const col = document.createElement('div');
        col.className = 'col-md-6';
        col.innerHTML = `
            <div class="card mb-3">
                <div class="card-body">
                    <h5 class="card-title">${park.name}</h5>
                    <p class="card-text">Location: ${park.location}</p>
                    <p class="card-text">Price: ${park.price}</p>
                    <a href="#" class="btn btn-primary">Reserve</a>
                </div>
            </div>
        `;
        parkResultsContainer.appendChild(col);
    });
}

// Function to load user reservations
function loadReservations() {
    // Sample reservations data (replace with actual data from backend)
    const reservations = [
        { id: 1, status: 'Active', parkNumber: 1, arrivalTime: '2024-04-20 09:00', departureTime: '2024-04-20 17:00' },
        { id: 2, status: 'Expired', parkNumber: 2, arrivalTime: '2024-04-22 10:00', departureTime: '2024-04-22 18:00' }
    ];

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

// Call the function to load reservations when the page loads
window.onload = loadReservations;