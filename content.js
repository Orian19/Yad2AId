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
    try {
        console.log("Sending request with data:", { userData, aptFilterData, swipeData });
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
            console.log("Received response:", data);
            return data;
        } else {
            console.error("Failed to fetch data, status:", response.status);
            return null;
        }
    } catch (error) {
        console.error("Error during fetch:", error);
        return null;
    }
};

// Add an event listener to the button to handle the click event
button.addEventListener('click', async function() {
//    const userData = {}; // Replace with actual user data
//    const aptFilterData = {}; // Replace with actual apartment filter data
//    const swipeData = {}; // Replace with actual swipe data
    const userData = {user_name: "Orian"};
    const aptFilterData = {
        price: 10000,
        city:  " חיפה",
        sqm: 100,
        rooms: 2
    };
    const swipeData = {
        apt_id: 5,  // You might want to update this dynamically
        swipe: "right",
    };

    const response = await sendRequest(userData, aptFilterData, swipeData);
    if (response && response[0]) {
        console.log("Redirecting to:", response[0]);
        console.log("ID:", response[1])
        window.location.href = response[0];
    } else {
        console.error("No redirect URL received");
    }
});

// Append the button to the body
document.body.appendChild(button);