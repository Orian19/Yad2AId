import { Yad2Button, LeftButton, RightButton } from './buttons.js'; 
import { createPopupForm ,getSessionData } from './popUpForm.js'
import { swipe } from './swipe.js'

// Add an event listener to the Yad2Button to show the popup form
Yad2Button.addEventListener('click', createPopupForm);
//Add an event listener for the left swipe 
LeftButton.addEventListener('click', () => swipe("left"));
//Add an event listener for the right swipe
RightButton.addEventListener('click', () => swipe("right"));

document.body.appendChild(Yad2Button);

// Function to show the Left and Right buttons
function showSwipeButtons() {
    document.body.appendChild(LeftButton);
    document.body.appendChild(RightButton);
}

// Check if we should show the swipe buttons on page load
//const { showSwipeButtons: shouldShowSwipeButtons } = getSessionData();
//if (shouldShowSwipeButtons) {
showSwipeButtons();
//}