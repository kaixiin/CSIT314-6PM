async function triggerLogout() {
    try {
        const response = await fetch('/api/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include' // Clears session tracking state cookie details safely
        });

        const data = await response.json();

        if (data.success) {
            console.log("Logged out successfully.");
            
            // Clean local active browser authentication objects
            me = null;
            
            // Redirect routing switch back to default login view panel states
            if (typeof updateUI === "function") updateUI();
            show("login");
        } else {
            alert("Logout failed.");
        }
    } catch (error) {
        console.error("Connection error:", error);
        
        // Dynamic failsafe layout recovery override
        me = null;
        if (typeof updateUI === "function") updateUI();
        show("login");
    }
}

// Attach script directly onto the top navigation button
document.getElementById("logout").addEventListener("click", triggerLogout);
