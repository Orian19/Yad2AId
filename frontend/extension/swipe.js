import {sendRequest} from "./sendRequest.js"

function setSessionData(swipe) {
    const sessionData = getSessionData(); 

    const userData = {
        user_name: sessionData.user_name,
    };
    const aptFilterData = {
        price: sessionData.price,
        city:  sessionData.city,
        sqm: sessionData.sqm,
        rooms: sessionData.rooms,
        description: sessionData.description
    };

    const swipeData = {
        apt_id: parseInt(sessionData.currentApartmentId),
        swipe: swipe
    };

    return { userData, aptFilterData, swipeData };
}


export async function swipe (swipe) {
    const { userData, aptFilterData, swipeData } = setSessionData(swipe);

    const response = await sendRequest(userData, aptFilterData, swipeData);

        console.log(response);

        if (response && response[0]) {
            let currentApartmentId = response[1];
            // Store the new currentApartmentId
            sessionStorage.setItem('currentApartmentId', currentApartmentId.toString());
        
            // Set showSwipeButtons to true
            sessionStorage.setItem('showSwipeButtons', 'true');

            window.location.href = response[0];
        } else {
            console.error("No redirect URL received");
        }

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
        description: sessionStorage.getItem('description') || '',
        loggedIn: sessionStorage.getItem('loggedIn') === 'true',
    };
}