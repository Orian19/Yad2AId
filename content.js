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

// Add an event listener to the button to handle the click event
button.addEventListener('click', function() {
    window.location.href = 'http://localhost:3000'; // URL of Next.js app URL
});

// Append the button to the body
document.body.appendChild(button);
