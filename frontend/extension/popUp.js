const popup = document.createElement('div');
popup.style.cssText = `
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: white;
    padding: 40px;
    border-radius: 5px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    width: 500px;
    direction: ltr;
    text-align: center; /* Center the content */
    `;

popup.innerHTML = `
     <form id="apartmentForm" style="display: flex; flex-direction: column; align-items: center;">
        <input type="text" id="user_name" placeholder="User Name" class="input input-bordered input-info w-full max-w-xs" required>
        <textarea id="description" placeholder="Describe Your Dream Apartment" class="textarea textarea-bordered textarea-info w-full max-w-xs" required style="margin: 10px 0;"></textarea>
        <input type="number" id="price" placeholder="Price Budget" class="input input-bordered input-info w-full max-w-xs" required>
        <input type="text" id="city" placeholder="Desired City" class="input input-bordered input-info w-full max-w-xs" required style="margin: 10px 0;">
        <input type="number" id="sqm" placeholder="Minimum Square Meter" class="input input-bordered input-info w-full max-w-xs" required>
        <input type="number" id="rooms" placeholder="Number of rooms" class="input input-bordered input-info w-full max-w-xs" required style="margin: 10px 0;">
        <button type="submit" class="btn btn-primary" style="margin-top: 10px;">Submit</button>
     </form>
     `;

export {popup}
