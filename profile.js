async function triggerCreateProfile(event) {
    event.preventDefault();

    // 1. Target the literal input element IDs inside your HTML layout
    const profileNameInput = document.getElementById('uname').value.trim();
    const descriptionInput = document.getElementById('desc').value.trim();
    
    // Gather all checked permissions from the checkboxes
    const checkedPermissions = [];
    const checkboxes = document.querySelectorAll('#createForm .perms input[type="checkbox"]:checked');
    checkboxes.forEach(cb => {
        checkedPermissions.push(cb.value);
    });

    // Display a temporary loading state
    msg("createMsg", "Creating profile...", false);

    try {
        /*
        // --- FUTURE BACKEND CONNECTION CODE (Commented out for local testing) ---
        const response = await fetch('/api/profiles', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: profileNameInput,
                description: descriptionInput,
                permissions: checkedPermissions
            }),
            credentials: 'include'
        });

        const data = await response.json();
        */

        // --- LOCAL TESTING LOGIC (Uses the profiles array in your HTML) ---
        // Simulating a successful creation object matching your mock structure
        const data = {
            success: profileNameInput.length > 0 ? true : false,
            newProfile: {
                name: profileNameInput,
                desc: descriptionInput,
                perms: checkedPermissions
            },
            message: "Profile name cannot be blank."
        };

        if (data.success) {
            alert("Profile created successfully!");
            console.log("Profile created successfully!");

            // Push the newly created mock profile into the global profiles array in your HTML
            if (typeof profiles !== "undefined") {
                profiles.push(data.newProfile);
            }

            // Reset the form inputs and checkbox states safely
            document.getElementById("createForm").reset();

            // Clear loading display messages gracefully
            msg("createMsg", "Set up a new user group so members can be assigned the right access.", false);
            
            // If you have a function to refresh the list layout view, run it
            if (typeof updateUI === "function") updateUI();
            
            // Switch layout views contextually back to the main profiles dashboard tab
            if (typeof show === "function") {
                show("profiles");
            } else {
                // Fallback manual class manipulation view switcher if show() isn't global
                document.querySelectorAll('.view').forEach(v => v.classList.remove('on'));
                document.getElementById("profiles").classList.add('on');
            }

        } else {
            msg("createMsg", data.message || "Failed to create profile.", true);
            document.getElementById('uname').focus();
        }

    } catch (error) {
        console.error("Connection error during profile creation:", error);
        msg("createMsg", "Cannot connect to profile server.", true);
    }
}

// Bind to your form submission lifecycle listener
document.getElementById("createForm").addEventListener("submit", triggerCreateProfile);