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
  <div class="drawer-content" style="flex-grow: 1; display: flex; flex-direction: column; height: 100%;">
    <div class="drawer-nav" style="padding: 10px;">
      <button id="logInBtn" class="btn btn-ghost">כניסה לחשבון</button>
      <button id="apartmentDetailsBtn" class="btn btn-ghost" style="display: none;">פרטי דירה</button>
      <button id="likedApartmentsBtn" class="btn btn-ghost" style="display: none;">דירות שאהבתי</button>
      <button id="dislikedApartmentsBtn" class="btn btn-ghost" style="display: none;">דירות שלא אהבתי</button>
    </div>
    <div id="drawerBody" style="flex-grow: 1; overflow-y: auto; padding: 10px;"></div>
    <div class="drawer-footer" style="display: flex; justify-content: space-between; align-items: center; padding: 10px; border-top: 1px solid #ddd;">
      <button id="closeDrawer" class="btn btn-ghost">לסגור</button>
      <button id="logOutBtn" class="btn btn-ghost" style="display: none;">לצאת מהחשבון</button>
    </div>
  </div>
`;

export { drawer };
