document.addEventListener('DOMContentLoaded', function () {
    // Load all parks when the page loads
    loadAllParks();

    // Load user reservations when the page loads
    loadReservations();
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
                    <a href="/reserve/${park.id}" class="btn btn-success">Reserve</a>
                </div>
            </div>
        `;
        parkResultsContainer.appendChild(col);
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
// Function to display user reservations
function displayReservations(reservations) {
    const reservationsAccordion = document.getElementById('reservationsAccordion');
    let reservationCounter = 1; // Initialize counter
    reservations.forEach(reservation => {
        const accordionItem = document.createElement('div');
        accordionItem.className = 'accordion-item';
        accordionItem.innerHTML = `
            <h2 class="accordion-header">
                <button class="accordion-button collapsed bg-light text-dark fw-bold" type="button" data-bs-toggle="collapse" data-bs-target="#collapse${reservationCounter}" aria-expanded="false" aria-controls="collapse${reservationCounter}">
                    Reservation ${reservationCounter} 
                    <span class="badge bg-${getBadgeColor(reservation.status)} rounded-pill mx-3">${reservation.status}</span>
                </button>
            </h2>
            <div id="collapse${reservationCounter}" class="accordion-collapse collapse" aria-labelledby="heading${reservationCounter}" data-bs-parent="#reservationsAccordion">
                <div class="accordion-body">
                    <ul class="list-group">
                        <li class="list-group-item">Park Number: ${reservation.park}</li>
                        <li class="list-group-item">Arrival Time: ${reservation.start_time}</li>
                        <li class="list-group-item">Duration Time: ${reservation.duration}</li>
                    </ul>
                    <div class="mt-3">
                        ${reservation.status === 'active' ? `<button type="button" class="btn btn-warning me-2" onclick="editReservation(${reservation.id})">Edit Reservation</button>` : ''}
                        ${reservation.status === 'active' ? `<button type="button" class="btn btn-danger" onclick="cancelReservation(${reservation.id})">Cancel Reservation</button>` : ''}
                        ${(reservation.status === 'cancelled' || reservation.status === 'expired') ? `<button type="button" class="btn btn-danger" onclick="removeReservation(${reservation.id})">Remove Reservation</button>` : ''}

                    </div>
                </div>
            </div>
        `;
        reservationsAccordion.appendChild(accordionItem);
        reservationCounter++; // Increment counter
    });
}


// Function to determine badge color based on reservation status
function getBadgeColor(status) {
    switch (status.toLowerCase()) {
        case 'active':
            return 'primary';
        case 'cancelled':
            return 'danger';
        case 'expired':
            return 'secondary';
        default:
            return 'secondary';
    }
}
// Function to edit a reservation
function editReservation(reservationId) {
    // Send a request to the server to update the reservation status to "cancelled"
    fetch(`/edit_reservation/${reservationId}/`, {  // Note the trailing slash
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Include CSRF token
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({}) // Empty body since we're just updating the status
    })
    .then(response => {
        if (response.ok) {
            // Reservation successfully cancelled
            console.log(`Reservation with ID ${reservationId} edited successfully.`);        
        } else {
            // Error occurred while cancelling reservation
            console.error(`Error cancelling reservation with ID ${reservationId}: ${response.statusText}`);
        }
    })
    .catch(error => {
        console.error(`Error editting reservation with ID ${reservationId}: ${error}`);
    });
}

// Function to cancel a reservation
function cancelReservation(reservationId) {
    // Display a sweet alert to confirm cancellation
    Swal.fire({
        title: 'Are you sure?',
        text: 'You are about to cancel this reservation!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, cancel it!',
        cancelButtonText: 'No, keep it'
    }).then((result) => {
        if (result.isConfirmed) {
            // User confirmed the cancellation
            const csrfToken = document.getElementById('csrf_token').value;
            // Send a request to the server to update the reservation status to "cancelled"
            fetch(`/cancel_reservation/${reservationId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken, // Include CSRF token
                },
            })
            .then(response => {
                if (response.ok) {
                    window.location.href = '/home';    
                }
            })
            .catch(error => {
                console.error(`Error cancelling reservation with ID ${reservationId}: ${error}`);
            });
        }
    });
}

// Function to remove a reservation
function removeReservation(reservationId) {
    // Display a sweet alert to confirm cancellation
    Swal.fire({
        title: 'Are you sure?',
        text: 'This reservation will be no longer in you Reservations!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, remove it!',
        cancelButtonText: 'No, keep it'
    }).then((result) => {
        if (result.isConfirmed) {
            // User confirmed the cancellation
            const csrfToken = document.getElementById('csrf_token').value;

            // Send a request to the server to remove the reservation
            fetch(`/remove_reservation/${reservationId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken, // Include CSRF token
                },
            })
            .then(response => {
                if (response.ok) {
                    window.location.href = '/home';    
                }
            })
            .catch(error => {
                console.error(`Error removing reservation with ID ${reservationId}: ${error}`);
            });
        }
    });
}
