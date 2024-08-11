export async function exitExtension () {
    const keysToRemove = [
        'currentApartmentId',
        'showExtensionButtons',
        'user_name',
        'price',
        'city',
        'sqm',
        'rooms',
        'description'
    ];
    
    keysToRemove.forEach(key => {
        sessionStorage.removeItem(key);
    });

    sessionStorage.setItem('showExtensionButtons', 'false'); //remove extension buttons
    sessionStorage.setItem('isLoggedIn', 'false'); //remove user


    window.location.href = "https://www.yad2.co.il/realestate/rent";
}
