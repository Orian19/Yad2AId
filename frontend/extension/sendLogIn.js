export const loginUser = async (userData) => {
    try {
        console.log("Sending login request with data:", { userData });
        const response = await fetch('http://127.0.0.1:8000/login/', {
            method: 'POST',
            mode: 'cors',
            headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
        });
  
        if (response.ok) {
            console.log("Login successful");
            return true;
        } else {
            console.error("Failed to login, status:", response.status);
            return false;
        }
    } catch (error) {
      console.error("Error during login:", error);
      return false;
    }
  };