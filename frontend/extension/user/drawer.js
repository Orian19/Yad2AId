import { drawer } from '../components/drawerFormat.js';
import { createApartmentDetailsForm } from './form.js';
import { showLogIn, handleLogout } from './logIn.js';
import { getApts } from './likedOrDislikedApts.js'

// Function to get login status from sessionStorage
export function getLoggedIn() {
  return sessionStorage.getItem('isLoggedIn') === 'true';
}

// Function to set login status in sessionStorage
export function setLoggedIn(status) {
  sessionStorage.setItem('isLoggedIn', status);
  updateButtonVisibility();
}

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
    document.getElementById('logInBtn').addEventListener('click', showLogIn);
    document.getElementById('logOutBtn').addEventListener('click', handleLogout);
    
     // true boolean in getApts retrieves liked apartments
     document.getElementById('likedApartmentsBtn').addEventListener('click', () => getApts(true));
    
     // false boolean in getApts retrieves disliked apartments
     document.getElementById('dislikedApartmentsBtn').addEventListener('click', () => getApts(false));
     
    
    // Update button visibility based on login status
    updateButtonVisibility();
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

// Function to update button visibility based on login status
export function updateButtonVisibility() {
    const logInBtn = document.getElementById('logInBtn');
    const apartmentDetailsBtn = document.getElementById('apartmentDetailsBtn');
    const logOutBtn = document.getElementById('logOutBtn');
    const likedAptBtn = document.getElementById('likedApartmentsBtn')
    const dislikedAptBtn = document.getElementById('dislikedApartmentsBtn')
    const isLoggedIn = sessionStorage.getItem('isLoggedIn') === 'true';
  
    if (isLoggedIn) {
      logInBtn.style.display = 'none';
      apartmentDetailsBtn.style.display = 'block';
      logOutBtn.style.display = 'block';
      likedAptBtn.style.display = 'block';
      dislikedAptBtn.style.display = 'block';
    } else {
      logInBtn.style.display = 'block';
      apartmentDetailsBtn.style.display = 'none';
      logOutBtn.style.display = 'none';
      likedAptBtn.style.display = 'none';
      dislikedAptBtn.style.display = 'none';

    }
  }
