export async function exitExtension () {
    sessionStorage.setItem('showExtensionButtons', 'false');
    window.location.href = "https://www.yad2.co.il/realestate/rent";
}
