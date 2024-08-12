//Azure: https://python-webapp-quickstart-000.azurewebsites.net/apartment/

export const sendRequest = async (userData, aptFilterData, swipeData) => {
    try {
        console.log("Sending request with data:", { userData, aptFilterData, swipeData });
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
            console.log("Received response:", data);
            return data;
        } else {
            console.error("Failed to fetch data, status:", response.status);
            return null;
        }
    } catch (error) {
        console.error("Error during fetch:", error);
        return null;
    }
};