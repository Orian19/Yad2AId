function createButton(text, className) {
    const button = document.createElement('button');
    button.innerText = text;
    button.className = className;
    return button;
  }
  
export const Yad2Button = createButton('Yad2Aid', 'btn btn-info btn-lg fixed bottom-3 left-1/2 transform -translate-x-1/2 z-50');
Yad2Button.style.bottom = '20px'; // Increased bottom margin for visibility
Yad2Button.style.transform = 'translateX(-50%)'; // Center horizontally

  
export const RightButton = createButton('Right', 'btn btn-success fixed top-1/2 right-3 transform -translate-y-1/2 z-50');
RightButton.style.top = '50%';
RightButton.style.right = '10px';
RightButton.style.transform = 'translateY(-50%)';
  
export const LeftButton = createButton('Left', 'btn btn-warning fixed top-1/2 left-3 transform -translate-y-1/2 z-50');
LeftButton.style.top = '50%';
LeftButton.style.left = '10px';
LeftButton.style.transform = 'translateY(-50%)';
  