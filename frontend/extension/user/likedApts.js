import { getApartments } from '../server/fetchApts.js';
import { deletePrefrence } from '../server/sendDeleteRequest.js'

export async function likedApts() {
    const getApts = {
        user_name: sessionStorage.getItem('user_name'),
        liked: "true"
    };
    
    try {
        const liked_apts = await getApartments(getApts);
        console.log("Liked apts:", liked_apts);

        const drawerBody = document.getElementById('drawerBody');
        if (!drawerBody) return;

        // Initialize content variable
        let content = '';

        // Group apartments by city
        const groupedApts = liked_apts.reduce((acc, apt) => {
            if (!acc[apt.city]) {
                acc[apt.city] = [];
            }
            acc[apt.city].push(apt);
            return acc;
        }, {});

        // Function to handle the deletion of an apartment
        function deleteApt(aptId) {
            const aptElement = document.getElementById(`apt-${aptId}`);
            if (aptElement) {
                aptElement.remove();
                const deletedAptId = aptId;
                console.log(`Apartment with ID ${deletedAptId} was deleted.`);
                //as apartment is currently like a swipe left will remove from liked apartments
                const swipeData = {
                    apt_id: parseInt(aptId),
                    swipe: "left"
                };
            
                deletePrefrence(swipeData)
            }
        }

        // Generate the HTML content for the drawer
        Object.keys(groupedApts).forEach(city => {
            content += `
                <div class="mb-6">
                    <div class="sticky top-0 z-10 bg-white">
                        <p class="text-lg" style="font-weight: bold; border-bottom: 1px solid #000; padding-bottom: 8px; margin-bottom: 8px;">${city}</p>
                    </div>
                    <div class="space-y-2">
            `;
            groupedApts[city].forEach(apt => {
                content += `
                    <div id="apt-${apt.id}" class="flex items-center">
                        <button class="btn btn-circle btn-outline ml-0 mr-2" style="width: 24px; height: 24px; border-radius: 50%; padding: 0; display: flex; align-items: center; justify-content: center;" onclick="deleteApt('${apt.id}')">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" style="width: 14px; height: 14px;">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                            </svg>
                        </button>
                        <p class="text-base"><a class="link link-hover" href="${apt.url}" target="_blank">${apt.address}</a></p>
                    </div>
                `;
            });
            content += `
                    </div>
                </div>
            `;
        });

        // Update the drawer body content
        drawerBody.innerHTML = content;

        // Attach the deleteApt function to the window object so it can be accessed from the onclick attribute
        window.deleteApt = deleteApt;
    } catch (error) {
        console.error("Error fetching liked apts:", error);
    }
}
