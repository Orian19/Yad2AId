//Azure: https://python-webapp-quickstart-000.azurewebsites.net/deleteApt/

export const deletePrefrence = async (swipeData) => {
    try {
        console.log("Sending login request with data:", { swipeData });
        const response = await fetch('http://127.0.0.1:8000/deleteApt/', {
            method: 'POST',
            mode: 'cors',
            headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(swipeData),
        });
  
        if (response.ok) {
            console.log("Delete Successfull");
            return true;
        } else {
            console.error("Failed to delete, status:", response.status);
            return false;
        }
    } catch (error) {
      console.error("Error during delete:", error);
      return false;
    }
  };