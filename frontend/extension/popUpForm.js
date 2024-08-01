import { sendRequest } from './sendRequest.js';
import {popup} from './popUp.js'

export function createPopupForm() {
    document.body.appendChild(popup);

    const { showExtensionButtons: shouldShowExtensionButtons } = getSessionData();
    if (shouldShowExtensionButtons) {
        loadFormData();
    }
    
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
        };
        const aptFilterData = {
            price: parseInt(document.getElementById('price').value),
            city: document.getElementById('city').value,
            sqm: parseInt(document.getElementById('sqm').value),
            rooms: parseInt(document.getElementById('rooms').value),
            description: document.getElementById('description').value || '' // Use empty string if no description 
        };


        // Store data in sessionStorage
        sessionStorage.setItem('user_name', userData.user_name);
        sessionStorage.setItem('description', aptFilterData.description); 
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
        
            // Set showExtensionButtons to true
            sessionStorage.setItem('showExtensionButtons', 'true');

            window.location.href = response[0];
        } else {
            console.error("No redirect URL received");
        }

        // Remove the popup after submission
        popup.remove();
    });
}

// Function to retrieve and populate form data from sessionStorage
function loadFormData() {
    const user_name = sessionStorage.getItem('user_name') || '';
    const price = sessionStorage.getItem('price') || '';
    const city = sessionStorage.getItem('city') || '';
    const sqm = sessionStorage.getItem('sqm') || '';
    const rooms = sessionStorage.getItem('rooms') || '';
    const description = sessionStorage.getItem('description') || '';


    // Set form fields with the retrieved data
    document.getElementById('user_name').value = user_name;
    document.getElementById('price').value = price;
    document.getElementById('city').value = city;
    document.getElementById('sqm').value = sqm;
    document.getElementById('rooms').value = rooms;
    document.getElementById('description').value = description;

}

// Function to retrieve data from sessionStorage
export function getSessionData() {
    return {
        currentApartmentId: parseInt(sessionStorage.getItem('currentApartmentId') || '0'),
        showExtensionButtons: sessionStorage.getItem('showExtensionButtons') === 'true',
        user_name: sessionStorage.getItem('user_name') || '',
        price: parseInt(sessionStorage.getItem('price') || '0'),
        city: sessionStorage.getItem('city') || '',
        sqm: parseInt(sessionStorage.getItem('sqm') || '0'),
        rooms: parseInt(sessionStorage.getItem('rooms') || '0'),
        description: sessionStorage.getItem('description') || ''
    };
}