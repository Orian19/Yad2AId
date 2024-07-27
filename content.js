// Create a new button element
const button = document.createElement('button');
button.innerText = 'Yad2Aid';
button.style.position = 'fixed';
button.style.bottom = '10px';
button.style.right = '10px';
button.style.padding = '10px 20px';
button.style.backgroundColor = '#007bff';
button.style.color = 'white';
button.style.border = 'none';
button.style.borderRadius = '5px';
button.style.cursor = 'pointer';
button.style.zIndex = '1000';

// Define the sendRequest function
const sendRequest = async (userData, aptFilterData, swipeData) => {
    const response = await fetch('http://127.0.0.1:8000/apartment/', {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user: userData,
            apt_filter: aptFilterData,
            swipe: swipeData
        }),
    });

    if (response.ok) {
        const data = await response.json();
        return data.url; // Assuming the backend returns the URL in a field named 'url'
    } else {
        console.error("Failed to fetch data");
        return "";
    }
};

// Add an event listener to the button to handle the click event
button.addEventListener('click', async function() {
//    const userData = {}; // Replace with actual user data
//    const aptFilterData = {}; // Replace with actual apartment filter data
//    const swipeData = {}; // Replace with actual swipe data

    const userData = {user_name: "Orian"};//testing
    const aptFilterData = { 
        price: parseInt(10000), 
        city: " חיפה", 
        sqm: parseInt(50), 
        rooms: parseInt(2)
    }; // testing
    const swipeData = {
        apt_id: 1,
        swipe: "right",    
        }; 

    const redirectUrl = await sendRequest(userData, aptFilterData, swipeData);
    if (redirectUrl[0]) {
        console.log(redirectUrl)
        window.location.href = redirectUrl;
    }
});

// Append the button to the body
document.body.appendChild(button);
