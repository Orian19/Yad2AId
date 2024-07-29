function createButton(text, style) {
    const button = document.createElement('button');
    button.innerText = text;
    Object.assign(button.style, style);
    return button;
}

export const Yad2Button = createButton('Yad2Aid', {
    position: 'fixed',
    bottom: '10px',
    right: '10px',
    padding: '10px 20px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    zIndex: '1000'
});

export const RightButton = createButton('Right', {
    position: 'fixed',
    top: '50%',
    right: '10px',
    transform: 'translateY(-50%)',
    padding: '10px 20px',
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    zIndex: '1000'
});

export const LeftButton = createButton('Left', {
    position: 'fixed',
    top: '50%',
    left: '10px',
    transform: 'translateY(-50%)',
    padding: '10px 20px',
    backgroundColor: '#17a2b8',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    zIndex: '1000'
});
