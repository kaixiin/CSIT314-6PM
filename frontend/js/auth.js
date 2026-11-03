// auth.js
// Logout. Connected to the real backend per auth_routes.py.

async function triggerLogout() {
    try {
        const response = await fetch(`${API_CONFIG.BASE_URL}/api/logout`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include' // Clears the session cookie server-side
        });

        const data = await response.json();

        if (data.success) {
            me = null;
            show("login");
            console.log("Logged out successfully.");
        } else {
            alert("Logout failed.");
        }

    } catch (error) {
        console.error("Connection error:", error);
        // Even if the server call failed, clear the local session so the
        // person isn't stuck on a screen they can no longer act on.
        me = null;
        show("login");
    }
}

document.getElementById("logout").addEventListener("click", triggerLogout);
