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

    // Create table structure with a scrollable container
    let content = `
      <div class="flex flex-col h-full">
        <div class="overflow-x-auto overflow-y-auto flex-grow" style="max-height: 100%;">
          <table class="table table-xs table-compact w-full">
            <thead>
              <tr>
                <th>City</th>
                <th>Address</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
    `;

    // Add rows for each city group
    for (const city in groupedApts) {
      groupedApts[city].forEach((apt) => {
        content += `
          <tr id="apt-${apt.id}">
            <td>${apt.city}</td>
            <td><a href="${apt.url}" target="_blank" class="link link-primary">${apt.address}</a></td>
            <td><button class="btn btn-xs btn-error" onclick="deleteApt(${apt.id})">Delete</button></td>
          </tr>
        `;
      });
    }

    // Close table structure
    content += `
            </tbody>
          </table>
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

  } catch (error) {
    console.error("Error fetching apts:", error);
  }
}
