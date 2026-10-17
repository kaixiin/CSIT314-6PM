// Connection function for the logout feature
async function triggerLogout() {
    try {
        // Knocks on the door of the backend route you showed me earlier
        const response = await fetch('/api/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include' // Crucial: passes the session cookie down to the backend
        });

        const data = await response.json();

        if (data.success) {
            console.log("Logged out successfully.");
            window.location.href = 'login.html'; // Directs to wherever the login page will live
        } else {
            alert("Logout failed.");
        }
    } catch (error) {
        console.error("Connection error:", error);
        window.location.href = 'login.html'; // Safe fallback
    }
}