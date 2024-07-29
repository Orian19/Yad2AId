import { Yad2Button, LeftButton, RightButton } from './buttons.js'; 
import { createPopupForm } from './popUpForm.js'
import { currentApartmentId } from './popUpForm.js';

// Add an event listener to the Yad2Button to show the popup form
Yad2Button.addEventListener('click', createPopupForm);

document.body.appendChild(Yad2Button);
//document.body.appendChild(LeftButton);
//document.body.appendChild(RightButton);