export const getApartments = async (getApts) => {
    try {
        console.log("Sending login request with data:", { getApts });
        const response = await fetch('http://127.0.0.1:8000/getApts/', {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(getApts),
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
        console.error("Error during login:", error);
        return null;
    }
};