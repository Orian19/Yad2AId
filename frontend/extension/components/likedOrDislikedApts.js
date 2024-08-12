import { getApartments } from '../server/fetchApts.js';
import { deletePrefrence } from '../server/sendDeleteRequest.js';

export async function getApts(like) {
  const getApts = {
    user_name: sessionStorage.getItem('user_name'),
    liked: like
  };

  try {
    const apts = await getApartments(getApts);
    console.log("apts:", apts);
    const drawerBody = document.getElementById('drawerBody');
    if (!drawerBody) return;

    // Group apartments by city
    const groupedApts = apts.reduce((acc, apt) => {
      if (!acc[apt.city]) {
        acc[apt.city] = [];
      }
      acc[apt.city].push(apt);
      return acc;
    }, {});

    const cities = Object.keys(groupedApts);

    // Create content structure
    let content = `
      <div class="flex flex-col h-full">
        <div class="overflow-x-auto overflow-y-auto flex-grow" style="max-height: 100%;">
    `;

    // Add table only if there are apartments
    if (cities.length === 0) {
      content += `
        <table class="table table-xs table-compact w-full">
        <thead>
            <tr>
              <th>אין דירות שמורות</th>
            </tr>
          </thead>
      `;
    } else {
      content += `
        <table class="table table-xs table-compact w-full">
          <thead>
            <tr>
              <th>עיר</th>
              <th>כתובת</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
      `;

      for (const city in groupedApts) {
        groupedApts[city].forEach((apt) => {
          content += `
            <tr id="apt-${apt.id}" data-city="${apt.city}">
              <td>${apt.city}</td>
              <td><a href="${apt.url}" target="_blank" class="link link-hover">${apt.address}</a></td>
              <td><button class="btn btn-xs btn-error" onclick="deleteApt(${apt.id})">למחוק</button></td>
            </tr>
          `;
        });
      }

      content += `
          </tbody>
        </table>
      `;

      // Add city selection and delete all button
      content += `
        <div class="mt-4 flex justify-between items-center">
          <select id="citySelect" class="select select-bordered mr-2">
            <option value="">בחר עיר</option>
            ${cities.map(city => `<option value="${city}">${city}</option>`).join('')}
          </select>
          <button class="btn btn-error ml-8" onclick="deleteAllInCity()">מחק הכל בעיר הנבחרת</button>
        </div>
      `;
    }

    content += `
        </div>
      </div>
    `;

    // Update the drawer body content
    drawerBody.innerHTML = content;

    // Attach the deleteApt function to the window object
    window.deleteApt = function(aptId) {
      const aptElement = document.getElementById(`apt-${aptId}`);
      if (aptElement) {
        aptElement.remove();
        console.log(`Apartment with ID ${aptId} was deleted.`);
        const swipeData = {
          apt_id: parseInt(aptId),
          swipe: like ? "left" : "right"
        };
        deletePrefrence(swipeData);
      }
    };

    // Attach the deleteAllInCity function to the window object
    window.deleteAllInCity = function() {
      const citySelect = document.getElementById('citySelect');
      const selectedCity = citySelect.value;
      if (!selectedCity) {
        console.log("No city selected.");
        return;
      }
      const rows = document.querySelectorAll(`tr[data-city="${selectedCity}"]`);
      rows.forEach(row => {
        const aptId = row.id.split('-')[1];
        row.remove();
        console.log(`Apartment with ID ${aptId} was deleted from city ${selectedCity}.`);
        const swipeData = {
          apt_id: parseInt(aptId),
          swipe: like ? "left" : "right"
        };
        deletePrefrence(swipeData);
      });
    };
  } catch (error) {
    console.error("Error fetching apts:", error);
  }
}