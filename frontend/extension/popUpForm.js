import { sendRequest } from './sendRequest.js';

export function createPopupForm() {
    const popup = document.createElement('div');
    popup.style.cssText = `
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: white;
    padding: 40px;
    border-radius: 5px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    width: 500px;
    direction: ltr;
    text-align: center; /* Center the content */
    `;

    popup.innerHTML = `
     <form id="apartmentForm" style="display: flex; flex-direction: column; align-items: center;">
       <input type="text" id="user_name" placeholder="User Name" class="input input-bordered input-info w-full max-w-xs" required>
       <textarea id="description" placeholder="Describe Your Dream Apartment" class="textarea textarea-bordered textarea-info w-full max-w-xs" required style="margin: 10px 0;"></textarea>
       <input type="number" id="price" placeholder="Price Budget" class="input input-bordered input-info w-full max-w-xs" required>
       <input type="text" id="city" placeholder="Desired City" class="input input-bordered input-info w-full max-w-xs" required style="margin: 10px 0;">
       <input type="number" id="sqm" placeholder="Minimum Square Meter" class="input input-bordered input-info w-full max-w-xs" required>
       <input type="number" id="rooms" placeholder="Number of rooms" class="input input-bordered input-info w-full max-w-xs" required style="margin: 10px 0;">
       <button type="submit" class="btn btn-primary" style="margin-top: 10px;">Submit</button>
     </form>
     `;

    document.body.appendChild(popup);

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
        let currentApartmentId = parseInt(sessionStorage.getItem('currentApartmentId') || '0');

        const swipeData = {
            apt_id: currentApartmentId,
            swipe: "right"
        };

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