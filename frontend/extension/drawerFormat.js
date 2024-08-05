// Create the drawer
const drawer = document.createElement('div');
drawer.className = 'drawer';
drawer.style.cssText = `
    position: fixed;
    top: 0;
    right: -300px;
    width: 300px;
    height: 100%;
    background-color: #fff;
    box-shadow: -2px 0 5px rgba(0,0,0,0.1);
    transition: right 0.3s ease-in-out;
    z-index: 9999;
`;

// Create the drawer content
drawer.innerHTML = `
    <div class="drawer-content">
        <div class="drawer-nav">
            <button id="apartmentDetailsBtn" class="btn btn-ghost">Apartment Details</button>
            <button id="likedApartmentsBtn" class="btn btn-ghost">Liked Apartments</button>
        </div>
        <div id="drawerBody"></div>
        <div class="drawer-footer">
            <button id="closeDrawer" class="btn btn-ghost">Close</button>
        </div>
    </div>
`;

export { drawer };