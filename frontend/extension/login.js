import { login } from './loginFormat.js'
import { getSessionData } from './swipe.js';

export function showLogin() {
    // Check if the login element is not already in the DOM
    if (!document.body.contains(login)) {
        // Append the login dialog to the body
        document.body.appendChild(login);

        // Add event listeners when the login is added to the DOM
        document.getElementById('submitLogin').addEventListener('click', handleLogin);
        document.getElementById('closeLogin').addEventListener('click', closeLogin);
    }

    // Check if the dialog is already open
    if (!login.open) {
        // Show the modal if it is not already open
        login.showModal();
    }
}

function closeLogin() {
    // Check if the login element is in the DOM
    if (document.body.contains(login)) {
        // Close the dialog if it is open
        if (login.open) {
            login.close();
        }

        document.body.removeChild(login);
    }
}

function handleLogin() {
    // Implement login logic here
    sessionStorage.setItem('loggedIn', 'true');
    const sessionData = getSessionData();

    // Debug: Log the retrieved session data
    console.log("Now session data:", sessionData);
    console.log('Login attempt...');
    // Placeholder for actual login logic

    // Close the modal on successful login
    closeLogin();
}

