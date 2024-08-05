import { drawer } from './drawerFormat.js';
import { createApartmentDetailsForm } from './form.js';
import { showLikedApartments } from './showLikedApartments.js';

// Function to show the drawer
export function showDrawer() {
    if (!document.body.contains(drawer)) {
        document.body.appendChild(drawer);
        setTimeout(() => {
            drawer.style.right = '0';
        }, 50);

        // Add event listeners when the drawer is added to the DOM
        document.getElementById('closeDrawer').addEventListener('click', hideDrawer);
        document.getElementById('apartmentDetailsBtn').addEventListener('click', createApartmentDetailsForm);
        document.getElementById('likedApartmentsBtn').addEventListener('click', showLikedApartments);
    }
}

// Function to hide the drawer
export function hideDrawer() {
    drawer.style.right = '-300px';
    setTimeout(() => {
        if (document.body.contains(drawer)) {
            document.body.removeChild(drawer);
        }
    }, 300);

    // Reset the drawer body
    resetDrawerBody();
}

// Function to reset the drawer body
function resetDrawerBody() {
    const drawerBody = document.getElementById('drawerBody');
    if (drawerBody) {
        drawerBody.innerHTML = '';
    }
}

