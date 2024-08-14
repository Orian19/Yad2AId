import { setLoggedIn, updateButtonVisibility } from './drawer.js';
import { loginUser } from '../server/sendLogIn.js';

// Function to show login form
export function showLogIn() {
  const drawerBody = document.getElementById('drawerBody');
  
  // Create login form HTML
  const loginForm = `
    <form id="loginForm">
      <div style="margin-bottom: 15px;">
        <label class="input input-bordered flex items-center gap-2">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 16 16"
            fill="currentColor"
            style="width: 14px; height: 14px; opacity: 0.7;">
            <path
              d="M2.5 3A1.5 1.5 0 0 0 1 4.5v.793c.026.009.051.02.076.032L7.674 8.51c.206.1.446.1.652 0l6.598-3.185A.755.755 0 0 1 15 5.293V4.5A1.5 1.5 0 0 0 13.5 3h-11Z" />
            <path
              d="M15 6.954 8.978 9.86a2.25 2.25 0 0 1-1.956 0L1 6.954V11.5A1.5 1.5 0 0 0 2.5 13h11a1.5 1.5 0 0 0 1.5-1.5V6.954Z" />
          </svg>
          <input type="email" id="email" class="grow" placeholder=" אימייל" required>
        </label>
      </div>
      <button type="submit" class="btn btn-outline btn-success">הרשמה</button>
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
