// Function that connects the profile creation form to the backend API
async function triggerCreateProfile(event) {
    event.preventDefault(); // Prevents the webpage from automatically reloading

    // 1. Grab values from the HTML input fields your team builds later
    const usernameInput = document.getElementById('profileUsername').value;
    const groupInput = document.getElementById('profileGroup').value;

    try {
        // 2. Reach out to the backend profile creation route
        const response = await fetch('/api/profiles', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: usernameInput,
                group: groupInput
            }),
            credentials: 'include' // Passes the active admin session cookie
        });

        const data = await response.json();

        // 3. Process backend response
        if (data.success) {
            alert("User profile created successfully!");
            // Refresh list or redirect back to admin dashboard panel
            window.location.reload(); 
        } else {
            alert("Failed to create profile: " + data.message);
        }

    } catch (error) {
        console.error("Connection error during profile creation:", error);
        alert("Cannot connect to server.");
    }
}
