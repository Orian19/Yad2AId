import { getLikedApts } from './fetchLikedApts.js'

export async function likedApts() {
    const userData = {
        user_name: sessionStorage.getItem('user_name')
    };
    
    try {
        const liked_apts = await getLikedApts(userData);
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
                    <p class="text-base"><a class="link link-success" href="${apt.url}" target="_blank">${apt.address}</a></p>
                `;
            });
            content += `
                    </div>
                </div>
            `;
        });

        // Update the drawer body content
        drawerBody.innerHTML = content;
    } catch (error) {
        console.error("Error fetching liked apts:", error);
    }
}
