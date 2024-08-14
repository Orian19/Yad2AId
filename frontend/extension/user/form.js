import { sendRequest } from '../server/sendRequest.js';
import { hideDrawer } from './drawer.js'

// Function to create the apartment details form
export function createApartmentDetailsForm() {
    const formHtml = `
    <form id="apartmentForm" style="display: flex; flex-direction: column; gap: 12px;">
      <textarea id="description" placeholder="תיאור" class="textarea textarea-bordered w-full" style="text-align: right;"></textarea>
      
      <label class="input input-bordered flex items-center gap-2">
        <span>מחיר מקסימלי</span>
        <input type="number" id="price" class="grow" required style="text-align: right; border: none; outline: none; background: transparent;">
      </label>
      
      <label class="input input-bordered flex items-center gap-2">
        <span>עיר</span>
        <input type="text" id="city" placeholder="  עברית" class="grow" required style="text-align: right; border: none; outline: none; background: transparent;">
      </label>
      
      <label class="input input-bordered flex items-center gap-2">
        <span>מטר מרובע</span>
        <input type="number" id="sqm" class="grow" required style="text-align: right; border: none; outline: none; background: transparent;">
      </label>
      
      <label class="input input-bordered flex items-center gap-2">
        <span>מספר חדרים</span>
        <input type="number" id="rooms" class="grow" required style="text-align: right; border: none; outline: none; background: transparent;">
      </label>
      
      <button type="submit" class="btn btn-outline btn-success">Submit</button>
    </form>
    `;
    
    
    const drawerBody = document.getElementById('drawerBody');
    drawerBody.innerHTML = formHtml;
    
    // Add event listener for form submission
    document.getElementById('apartmentForm').addEventListener('submit', handleFormSubmit);
    
    // Load form data if available
    loadFormData();
}

// Function to handle form submission
async function handleFormSubmit(e) {
    e.preventDefault();

    const userData = {
        user_name: sessionStorage.getItem('user_name')
    };
    const aptFilterData = {
        price: parseInt(document.getElementById('price').value),
        city: document.getElementById('city').value,
        sqm: parseInt(document.getElementById('sqm').value),
        rooms: parseInt(document.getElementById('rooms').value),
        description: document.getElementById('description').value || ''
    };

    // Store data in sessionStorage
    Object.entries({...aptFilterData}).forEach(([key, value]) => {
        sessionStorage.setItem(key, value);
    });

    let currentApartmentId = parseInt(sessionStorage.getItem('currentApartmentId')) || 0;

    const swipeData = {
        apt_id: currentApartmentId,
        swipe: "right"
    };

    const response = await sendRequest(userData, aptFilterData, swipeData);
    if (response && response[0]) {
        sessionStorage.setItem('currentApartmentId', response[1].toString());
        sessionStorage.setItem('showExtensionButtons', 'true');
        window.location.href = response[0];
    } else {
        console.error("No redirect URL received");
    }

    hideDrawer();
}

// Function to retrieve and populate form data from sessionStorage
function loadFormData() {
    const formFields = ['user_name', 'price', 'city', 'sqm', 'rooms', 'description'];
    formFields.forEach(field => {
        const value = sessionStorage.getItem(field) || '';
        const element = document.getElementById(field);
        if (element) element.value = value;
    });
}