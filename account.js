async function triggerCreateAccount(event) {
    event.preventDefault();

    // 1. Target the literal input element IDs inside your HTML layout
    const fullNameInput = document.getElementById('aname').value.trim();
    const emailInput = document.getElementById('aemail').value.trim().toLowerCase();
    const passwordInput = document.getElementById('apw').value;
    const selectedProfile = document.getElementById('aprofile').value;

    // Display a temporary loading state
    msg("accountMsg", "Creating user account...", false);

    try {
        /*
        // --- FUTURE BACKEND CONNECTION CODE (Commented out for local testing) ---
        const response = await fetch('/api/accounts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: fullNameInput,
                email: emailInput,
                password: passwordInput,
                profile: selectedProfile
            }),
            credentials: 'include'
        });

        const data = await response.json();
        */

        // --- LOCAL TESTING LOGIC (Uses the accounts array in your HTML) ---
        // Check if an account with that email already exists in your local mock database array
        const emailExists = accounts.some(acc => acc.email === emailInput);

        const data = {
            success: !emailExists,
            newAccount: {
                name: fullNameInput,
                email: emailInput,
                pw: passwordInput,
                role: "user",
                profile: selectedProfile
            },
            message: `Create failed: an account for "${emailInput}" already exists.`
        };

        if (data.success) {
            console.log("Account created successfully!");
            alert("Account created successfully!");

            // Push the newly created user account into the global accounts database array in your HTML
            if (typeof accounts !== "undefined") {
                accounts.push(data.newAccount);
            }

            // Reset the form layout state safely
            document.getElementById("accountForm").reset();

            // Clear loading display messages gracefully
            msg("accountMsg", "Create a login for a new user and assign a profile.", false);
            
            // Re-render UI table listings contextually if tracking function is active
            if (typeof updateUI === "function") updateUI();
            
            // Switch view panels contextually back to the main user accounts directory layout view
            if (typeof show === "function") {
                show("accounts");
            } else {
                document.querySelectorAll('.view').forEach(v => v.classList.remove('on'));
                document.getElementById("accounts").classList.add('on');
            }

        } else {
            // Render specific mock database conflict errors matching your snapshot layout exactly
            msg("accountMsg", data.message, true);
            document.getElementById('aemail').focus();
        }

    } catch (error) {
        console.error("Connection error during account creation:", error);
        msg("accountMsg", "Cannot connect to account server.", true);
    }
}

// Bind to your form submission lifecycle listener
document.getElementById("accountForm").addEventListener("submit", triggerCreateAccount);