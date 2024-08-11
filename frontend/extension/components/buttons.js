//SVG to create heart on swipeRight button
const heartIconSVG = `
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    fill="none"
    viewBox="0 0 24 24"
    stroke="currentColor">
    <path
      stroke-linecap="round"
      stroke-linejoin="round"
      stroke-width="2"
      d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
  </svg>
`;

//SVG to create "X" on swipeLeft button
const xIconSVG = `
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width="24"
    height="24"
    fill="none"
    viewBox="0 0 24 24"
    stroke="currentColor">
    <path
      stroke-linecap="round"
      stroke-linejoin="round"
      stroke-width="2"
      d="M6 18L18 6M6 6l12 12" />
  </svg>
`;

// Function to create a button with an SVG icon and class names
function createButton(iconSVG, className) {
  const button = document.createElement('button');
  button.innerHTML = iconSVG; // Insert the SVG icon
  button.className = className;
  button.style.display = 'flex'; // Ensure the SVG is visible
  button.style.alignItems = 'center'; // Center content
  button.style.justifyContent = 'center'; // Center content
  return button;
}

// Create the RightButton with the heart icon
export const RightButton = createButton(heartIconSVG, 'btn btn-success fixed top-1/2 right-3 transform -translate-y-1/2 z-50');
RightButton.style.top = '50%';
RightButton.style.right = '10px';
RightButton.style.transform = 'translateY(-50%)';

// Create the LeftButton with the "X" icon
export const LeftButton = createButton(xIconSVG, 'btn btn-warning fixed top-1/2 left-3 transform -translate-y-1/2 z-50');
LeftButton.style.top = '50%';
LeftButton.style.left = '10px';
LeftButton.style.transform = 'translateY(-50%)';

// Create the Yad2Button with text 
export const Yad2Button = createButton('<span>Yad2Aid</span>', 'btn btn-outline btn-success fixed bottom-3 right-3 transform -translate-x-1/2 z-50');
Yad2Button.style.width = '100px'; // Match the width of Yad2Button
Yad2Button.style.bottom = '20px'; 
Yad2Button.style.right = '20px'; 
Yad2Button.style.transform = 'none';

// Create the ExitButton with text
export const ExitButton = createButton('<span>Exit</span>','btn btn-outline btn-warning fixed bottom-3 left-3 transform -translate-x-1/2 z-50');
ExitButton.style.width = '100px'; // Match the width of Yad2Button
ExitButton.style.bottom = '20px'; 
ExitButton.style.left = '20px'; 
ExitButton.style.transform = 'none';