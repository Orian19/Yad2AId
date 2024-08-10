import { setLoggedIn, updateButtonVisibility } from './drawer.js';
import { loginUser } from './sendLogIn.js';

// Function to show login form
export function showLogIn() {
  const drawerBody = document.getElementById('drawerBody');
  
  // Create login form HTML
  const loginForm = `
    <form id="loginForm">
      <div style="margin-bottom: 15px;">
        <label for="email" style="display: block; margin-bottom: 5px;">Email:</label>
        <input type="email" id="email" required style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px;">
      </div>
      <button type="submit" style="background-color: #4CAF50; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer;">Log In</button>
    </form>
  `;

  // Set the drawer body content
  drawerBody.innerHTML = loginForm;

  // Add event listener to the form
  const form = document.getElementById('loginForm');
  form.addEventListener('submit', handleSubmit);
}

// Function to handle form submission
async function handleSubmit(event) {
  event.preventDefault();
  const email = document.getElementById('email').value.trim();

  //set user name of session
  sessionStorage.setItem('user_name', email)
  
  const userData = {
    user_name: email,
  };

  //Login the user 
  const loginSuccessful = await loginUser(userData);

  //TEST checks for success of login
  if (loginSuccessful) {
    setTimeout(() => {
      setLoggedIn(true);
      //Delete email input box & submit button
      const drawerBody = document.getElementById('drawerBody');
      drawerBody.innerHTML = ``;
      updateButtonVisibility();
    }, 200); // Simulating server delay
  } else {
    console.log("Login failed");
    // Handle login failure
  }

}

// Function to handle logout
export function handleLogout() {
  sessionStorage.setItem('isLoggedIn', 'false'); //set loggedIn indicator to false 

  sessionStorage.removeItem('user_name'); // Remove user_name from session storage
  console.log("post log out", sessionStorage.getItem('user_name'))
  updateButtonVisibility();
  // Clear any user-specific data or reset the drawer state as needed
  const drawerBody = document.getElementById('drawerBody');
  drawerBody.innerHTML = '';
}
