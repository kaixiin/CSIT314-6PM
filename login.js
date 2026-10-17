// Function that connects the login page text boxes to the backend API
async function triggerLogin(event) {
    // Prevent the web page from automatically reloading when submitting the form
    event.preventDefault();

    // 1. Grab the values written inside the HTML text input boxes
    const usernameInput = document.getElementById('usernameField').value;
    const passwordInput = document.getElementById('passwordField').value;

    try {
        // 2. Send the request to your backend login route
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            // Packages the text up to match data.get("username") in your backend
            body: JSON.stringify({
                username: usernameInput,
                password: passwordInput
            }),
            credentials: 'include' // Saves the Flask session cookie in the browser
        });

        const data = await response.json();

        // 3. Check the backend response keys (Line 27 in your auth_routes.py)
        if (data.success) {
            console.log("Login successful!");
            // Send the user to the application dashboard page
            window.location.href = 'dashboard.html'; 
        } else {
            // Displays "Login failed" from your backend (Line 24)
            alert("Error: " + data.message); 
        }

    } catch (error) {
        console.error("Connection error during login:", error);
        alert("Cannot connect to login server.");
    }
}
// Function that connects the login page text boxes to the backend API
async function triggerLogin(event) {
    // Prevent the web page from automatically reloading when submitting the form
    event.preventDefault();

    // 1. Grab the values written inside the HTML text input boxes
    const usernameInput = document.getElementById('usernameField').value;
    const passwordInput = document.getElementById('passwordField').value;

    try {
        // 2. Send the request to your backend login route
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            // Packages the text up to match data.get("username") in your backend
            body: JSON.stringify({
                username: usernameInput,
                password: passwordInput
            }),
            credentials: 'include' // Saves the Flask session cookie in the browser
        });

        const data = await response.json();

        // 3. Check the backend response keys (Line 27 in your auth_routes.py)
        if (data.success) {
            console.log("Login successful!");
            // Send the user to the application dashboard page
            window.location.href = 'dashboard.html'; 
        } else {
            // Displays "Login failed" from your backend (Line 24)
            alert("Error: " + data.message); 
        }

    } catch (error) {
        console.error("Connection error during login:", error);
        alert("Cannot connect to login server.");
    }
}