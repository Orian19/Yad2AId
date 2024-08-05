// Create the login dialog element
const login = document.createElement('dialog');
login.setAttribute('id', 'loginModal');
login.className = 'modal';

// Set the inner HTML of the dialog
login.innerHTML = `
    <div class="modal-box rounded-lg"> <!-- Added rounded-lg for rounded corners -->
        <form method="dialog">
            <!-- Close button with rounded edges -->
            <button id="closeLogin" class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2 rounded-full">✕</button>
        </form>
        <h3 class="font-bold text-lg">Login Required</h3>
        <p class="py-4">Please log in to continue using the extension features.</p>
        <div class="modal-action">
            <!-- Username and password input fields -->
            <input type="text" placeholder="Enter username" class="input input-bordered w-full max-w-xs mb-2 text-left placeholder:text-left" />
            <input type="password" placeholder="Enter password" class="input input-bordered w-full max-w-xs mb-2 text-left placeholder:text-left" />
            <!-- Submit button -->
            <button id="submitLogin" class="btn btn-ghost">Submit</button>
        </div>
    </div>
`;

// Export the login dialog
export { login };
