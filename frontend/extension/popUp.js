const popup = document.createElement('div');

// Applying the card styling from the template
popup.className = 'card bg-base-100 w-96 shadow-xl';
popup.style.cssText = `
    position: fixed;
    top: 55%; 
    left: 50%;
    transform: translate(-50%, -50%);
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    border-radius: 8px;
    overflow: hidden; /* Ensure no overflow issues */
    padding: 16px;
    z-index: 9999; /* Ensure the popup is in front of other content */
`;

// Adding the content of the popup
popup.innerHTML = `
    <div class="card-body items-center text-center">
        <form id="apartmentForm" style="display: flex; flex-direction: column; gap: 12px;">
            <input type="text" id="user_name" placeholder="User Name" class="input input-bordered w-full" required style="text-align: left;">
            <textarea id="description" placeholder="Description" class="textarea textarea-bordered w-full" required style="text-align: left;"></textarea>
            <input type="number" id="price" placeholder="Price Budget" class="input input-bordered w-full" required style="text-align: left;">
            <input type="text" id="city" placeholder="City - Hebrew" class="input input-bordered w-full" required style="text-align: left;">
            <input type="number" id="sqm" placeholder="Minimum Square Meter" class="input input-bordered w-full" required style="text-align: left;">
            <input type="number" id="rooms" placeholder="Number of rooms" class="input input-bordered w-full" required style="text-align: left;">
        </form>
        <div class="card-actions justify-end mt-4">
            <button type="submit" form="apartmentForm" class="btn btn-ghost">Submit</button>
            <button type="button" id="cancelButton" class="btn btn-ghost">Cancel</button>
        </div>
    </div>
`;

export { popup }
