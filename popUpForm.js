import { sendRequest } from './sendRequest.js'

let currentApartmentId = 0;

export function createPopupForm() {
    const popup = document.createElement('div');
    popup.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: white;
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    `;

    popup.innerHTML = `
        <h2>Enter Apartment Details</h2>
        <form id="apartmentForm">
            <label for="user_name">User Name:</label>
            <input type="text" id="user_name" required><br><br>
            
            <label for="price">Price:</label>
            <input type="number" id="price" required><br><br>
            
            <label for="city">City:</label>
            <input type="text" id="city" required><br><br>
            
            <label for="sqm">Square Meters:</label>
            <input type="number" id="sqm" required><br><br>
            
            <label for="rooms">Rooms:</label>
            <input type="number" id="rooms" required><br><br>
            
            <button type="submit">Submit</button>
        </form>
    `;

    document.body.appendChild(popup);

    document.getElementById('apartmentForm').addEventListener('submit', async function(e) {
        e.preventDefault();

        const userData = {
            user_name: document.getElementById('user_name').value
        };

        const aptFilterData = {
            price: parseInt(document.getElementById('price').value),
            city: document.getElementById('city').value,
            sqm: parseInt(document.getElementById('sqm').value),
            rooms: parseInt(document.getElementById('rooms').value)
        };
        
        const swipeData = {
            apt_id: currentApartmentId,
            swipe: "right"
        };
        
        const response = await sendRequest(userData, aptFilterData, swipeData);
        console.log(response)
        if (response && response[0]) {
            currentApartmentId = response[1];
            window.location.href = response[0];
        } else {
            console.error("No redirect URL received");
        }

        // Remove the popup after submission
        popup.remove();
    });
}
export { currentApartmentId };
