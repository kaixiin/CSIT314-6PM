async function triggerLogin(event) {
    event.preventDefault();

    // 1. Target the literal input element IDs inside your HTML layout
    const emailInput = document.getElementById('email').value.trim().toLowerCase();
    const passwordInput = document.getElementById('pw').value;

    msg("loginMsg", "Signing in...", false);

    try {
        /*
        // 2. Fetch connection pointing directly to your backend Blueprint routing prefix
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: emailInput, // Matches data.get("username") in Flask
                password: passwordInput // Matches data.get("password") in Flask
            }),
            credentials: 'include' // Transmits and handles Flask session cookies automatically
        });

        const data = await response.json();
*/

        // This looks up the user inside the accounts array in your HTML file
        const foundUser = accounts.find(acc => acc.email === emailInput && acc.pw === passwordInput);
        
        // This creates a fake "data" object that mimics a successful server response
        const data = {
            success: foundUser ? true : false,
            account: foundUser ? {
                username: foundUser.email,
                account_type: foundUser.role,
                permissions: ["View"]
            } : null,
            message: "Invalid email or password."
        };
        // ---------------------------------------------------------
        
        // 3. Process return payload using keys matching your auth_routes.py exactly
        if (true) {
            alert("Login successful!");
            console.log("Login successful!");

            // Reconstruct your internal session context tracking mapping
            me = {
                name: data.account.username,
                email: data.account.username,
                role: data.account.account_type === "admin" ? "admin" : "user",
                permissions: data.account.permissions
            };

            // Reset form layout state safely
            document.getElementById("loginForm").reset();

            // Clear loading display and flip active application layout view panels contextually
            msg("loginMsg", "Choose your role, then enter your email and password.", false);
            
// Switch views natively based on the user's role assignment
            document.querySelectorAll('.view').forEach(v => v.classList.remove('on'));
            if (me.role === "admin") {
                document.getElementById("dash").classList.add('on');
            } else {
                document.getElementById("home").classList.add('on');
                if (document.getElementById("welcome")) {
                    document.getElementById("welcome").innerText = `Welcome, ${me.name}!`;
                }
            }

        } else {
            // Render specific backend-driven error text message strings cleanly
            msg("loginMsg", data.message || "Login failed", true);
            document.getElementById('email').focus();
        }

    } catch (error) {
        console.error("Connection error during login:", error);
        msg("loginMsg", "Cannot connect to login server.", true);
    }
}

// Bind to your form submission lifecycle listener
document.getElementById("loginForm").addEventListener("submit", triggerLogin);
