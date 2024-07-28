import { sendRequest } from './sendRequest.js'
import { Yad2Button, LeftButton, RightButton } from './buttons.js'; 

// Global variable for current apartment ID
let currentApartmentId;

// Add an event listener to the button to handle the click event
Yad2Button.addEventListener('click', async function() {
    const userData = {user_name: "Orian"};
    const aptFilterData = {
        price: 10000,
        city: " חיפה",
        sqm: 100,
        rooms: 2
    };
    const swipeData = {
        apt_id: 5, // Use the current apartment ID
        swipe: "right",
    };
    
    const response = await sendRequest(userData, aptFilterData, swipeData);
    if (response && response[0]) {
        // Update the current apartment ID with response[1]
        currentApartmentId = response[1];
        console.log("Updated currentApartmentId:", currentApartmentId);    
        window.location.href = response[0];
    } else {
        console.error("No redirect URL received");
    }
});

document.body.appendChild(Yad2Button);
document.body.appendChild(LeftButton);
document.body.appendChild(RightButton);


