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
  display: flex;
  flex-direction: column;
`;

// Create the drawer content
drawer.innerHTML = `
  <div class="drawer-content" style="flex-grow: 1; display: flex; flex-direction: column;">
    <div class="drawer-nav">
      <button id="logInBtn" class="btn btn-ghost">Log In</button>
      <button id="apartmentDetailsBtn" class="btn btn-ghost" style="display: none;">Apartment Details</button>
      <button id="likedApartmentsBtn" class="btn btn-ghost" style="display: none;">My Apartments</button>
      <button id="dislikedApartmentsBtn" class="btn btn-ghost" style="display: none;">Spam Apartments</button>


    </div>
    <div id="drawerBody" style="flex-grow: 1;"></div>
    <div class="drawer-footer" style="display: flex; justify-content: space-between; align-items: flex-end;">
      <button id="closeDrawer" class="btn btn-ghost">Close</button>
      <button id="logOutBtn" class="btn btn-ghost" style="display: none;">Log Out</button>
    </div>
  </div>
`;

export { drawer };