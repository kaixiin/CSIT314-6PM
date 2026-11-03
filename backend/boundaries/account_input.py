import re

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def read_account_fields(data, need_password):
    """Return (fields, error). error is a message to show, or None if the input is fine."""
    data = data if isinstance(data, dict) else {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    profile_id = data.get("profile_id")

    # the dropdown sends "3" as text, so convert it to an int
    try:
        profile_id = None if isinstance(profile_id, bool) else int(profile_id)
    except (TypeError, ValueError):
        profile_id = None

    if not isinstance(username, str) or not isinstance(email, str) or profile_id is None:
        return None, "Please fill in all fields"
    if need_password and not isinstance(password, str):
        return None, "Please fill in all fields"

    username = username.strip()
    email = email.strip()
    if not username or not email or (need_password and not password):
        return None, "Please fill in all fields"

    if len(username) > 50:
        return None, "Username must be 50 characters or less"
    if len(email) > 255 or not EMAIL_PATTERN.match(email):
        return None, "Please enter a valid email"
    if need_password and len(password) < 8:          # delete these two lines if not needed
        return None, "Password must be at least 8 characters"

    return {"username": username, "email": email,
            "password": password, "profile_id": profile_id}, None