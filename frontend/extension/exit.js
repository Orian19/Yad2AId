export async function exitExtension () {
    const keysToRemove = [
        'currentApartmentId',
        'showExtensionButtons',
        'user_name',
        'price',
        'city',
        'sqm',
        'rooms',
        'description',
        'loggedIn'
    ];
    
    keysToRemove.forEach(key => {
        sessionStorage.removeItem(key);
    });

    sessionStorage.setItem('showExtensionButtons', 'false');
    sessionStorage.setItem('loggedIn', 'false');

    window.location.href = "https://www.yad2.co.il/realestate/rent";
}
