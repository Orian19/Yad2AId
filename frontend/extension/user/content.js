import { Yad2Button, LeftButton, RightButton, ExitButton } from '../components/buttons.js'; 
import { showDrawer } from './drawer.js';
import { exitExtension } from '../components/exit.js';
import { swipe, getSessionData } from '../components/swipe.js';

// Add event listener to the Yad2Button to open the drawer when clicked.
Yad2Button.addEventListener('click', showDrawer);

// Add event listener to the ExitButton to exit extension when clicked.
ExitButton.addEventListener('click', exitExtension);

// Function to send swipe event to Google Analytics
function trackSwipeEvent(direction) {
    if (typeof sendAnalytics === 'function') {
        sendAnalytics('event', {
            'event_category': 'Swipe',
            'event_action': `Swipe ${direction}`,
            'event_label': 'User Interaction'
        });
    }
}

// "Swipe" left when LeftButton is clicked.
LeftButton.addEventListener('click', () => {
    swipe("left");
    trackSwipeEvent('Left');
});

// "Swipe" right when RightButton is clicked.
RightButton.addEventListener('click', () => {
    swipe("right");
    trackSwipeEvent('Right');
});

// Append the Yad2Button to the document's body, making it visible on the page.
document.body.appendChild(Yad2Button);

// Define a function to display navigation buttons on the extension.
function showExtensionButtons() {
    document.body.appendChild(LeftButton);
    document.body.appendChild(RightButton);
    document.body.appendChild(ExitButton);
}
//get button controlling elements from session data 
const { showExtensionButtons: shouldShowExtensionButtons} = getSessionData();

// Conditionally display the navigation buttons based on session data.
if (shouldShowExtensionButtons) {
    showExtensionButtons();
}

