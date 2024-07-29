export const sendRequest = async (userData, aptFilterData, swipeData) => {
    const response = await fetch('http://127.0.0.1:8000/apartment/', {
        method: 'POST',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user: userData,
            apt_filter: aptFilterData,
            swipe: swipeData
        }),
    });

    if (response.ok) {
        const data = await response.json();
        return data; 
    } else {
        console.error("Failed to fetch data");
        return "";
    }
};
