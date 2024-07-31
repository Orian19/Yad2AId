import { sendRequest } from './sendRequest.js';
import {popup} from './popUp.js'

export function createPopupForm() {
    document.body.appendChild(popup);

    const cancelButton = document.getElementById('cancelButton');
    if (cancelButton) {
        cancelButton.addEventListener('click', function() {
            document.body.removeChild(popup); // Remove the popup from the DOM
        });
    } else {
    console.error('Cancel button not found');
    }

    document.getElementById('apartmentForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const userData = {
            user_name: document.getElementById('user_name').value,
            description: document.getElementById('description').value  // Add the description field here
        };
        const aptFilterData = {
            price: parseInt(document.getElementById('price').value),
            city: document.getElementById('city').value,
            sqm: parseInt(document.getElementById('sqm').value),
            rooms: parseInt(document.getElementById('rooms').value)
        };


        // Store data in sessionStorage
        sessionStorage.setItem('user_name', userData.user_name);
        sessionStorage.setItem('description', userData.description); // Store the description in sessionStorage
        sessionStorage.setItem('price', aptFilterData.price);
        sessionStorage.setItem('city', aptFilterData.city);
        sessionStorage.setItem('sqm', aptFilterData.sqm);
        sessionStorage.setItem('rooms', aptFilterData.rooms);

        // Retrieve currentApartmentId from sessionStorage or default to 0
        let currentApartmentId = parseInt(sessionStorage.getItem('currentApartmentId'));

        //if currentApartmentId does not exist set to 0
        if (isNaN(currentApartmentId)) {
            currentApartmentId = 0;
        }

        const swipeData = {
            apt_id: currentApartmentId,
            swipe: "right"
        };
        console.log("Swipe Data:", swipeData);
        console.log("User Data:", userData);
        console.log("Apartment Filter Data:", aptFilterData);

        const response = await sendRequest(userData, aptFilterData, swipeData);
        console.log(response);
        if (response && response[0]) {
            currentApartmentId = response[1];
            // Store the new currentApartmentId
            sessionStorage.setItem('currentApartmentId', currentApartmentId.toString());
        
            // Set showSwipeButtons to true
            sessionStorage.setItem('showSwipeButtons', 'true');

            window.location.href = response[0];
        } else {
            console.error("No redirect URL received");
        }

        // Remove the popup after submission
        popup.remove();
    });
}

// Function to retrieve data from sessionStorage
export function getSessionData() {
    return {
        currentApartmentId: parseInt(sessionStorage.getItem('currentApartmentId') || '0'),
        showSwipeButtons: sessionStorage.getItem('showSwipeButtons') === 'true',
        user_name: sessionStorage.getItem('user_name') || '',
        price: parseInt(sessionStorage.getItem('price') || '0'),
        city: sessionStorage.getItem('city') || '',
        sqm: parseInt(sessionStorage.getItem('sqm') || '0'),
        rooms: parseInt(sessionStorage.getItem('rooms') || '0'),
        description: sessionStorage.getItem('description') || ''
    };
}