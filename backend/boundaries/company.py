import base64
import binascii
import os
import re
import uuid

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_PATTERN = re.compile(r"^[0-9 +()\-]{6,20}$")
LOGO_PATTERN = re.compile(r"^data:image/(png|jpeg);base64,(.+)$", re.DOTALL)
MAX_LOGO_BYTES = 5 * 1024 * 1024
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads", "logos")


def read_company_fields(data):
    """Return (fields, error). error is a message to show, or None if the input is fine."""
    data = data if isinstance(data, dict) else {}
    names = ("company_name", "description", "address", "contact_number", "email")
    values = {name: data.get(name) for name in names}
    if not all(isinstance(v, str) for v in values.values()):
        return None, "Please fill in all fields"
    values = {name: v.strip() for name, v in values.items()}
    if not all(values.values()):
        return None, "Please fill in all fields"

    if len(values["company_name"]) > 100:
        return None, "Company name must be 100 characters or less"
    if len(values["description"]) > 1000:
        return None, "Description must be 1000 characters or less"
    if len(values["address"]) > 255:
        return None, "Address must be 255 characters or less"
    if not PHONE_PATTERN.match(values["contact_number"]):
        return None, "Please enter a valid contact number"
    if len(values["email"]) > 255 or not EMAIL_PATTERN.match(values["email"]):
        return None, "Please enter a valid email"
    return values, None


def save_logo(logo):
    """logo is a data URL such as "data:image/png;base64,...".
    Return (filename, error). filename is None when no logo was sent."""
    if logo is None or logo == "":
        return None, None
    match = LOGO_PATTERN.match(logo) if isinstance(logo, str) else None
    if not match:
        return None, "Logo must be a JPG or PNG image"
    try:
        raw = base64.b64decode(match.group(2), validate=True)
    except (binascii.Error, ValueError):
        return None, "Logo must be a JPG or PNG image"
    if len(raw) > MAX_LOGO_BYTES:
        return None, "Logo must be 5MB or smaller"

    is_png = match.group(1) == "png" and raw.startswith(b"\x89PNG\r\n\x1a\n")
    is_jpg = match.group(1) == "jpeg" and raw.startswith(b"\xff\xd8\xff")
    if not (is_png or is_jpg):
        return None, "Logo must be a JPG or PNG image"

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.{'png' if is_png else 'jpg'}"
    with open(os.path.join(UPLOAD_FOLDER, filename), "wb") as f:
        f.write(raw)
    return filename, None


def remove_logo(filename):
    """Delete a saved logo file (used when saving the profile failed)."""
    if filename:
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, filename))
        except OSError:
            pass


def read_company_form(data):
    """Check the text fields, then save the logo. Return (fields, error)."""
    fields, error = read_company_fields(data)
    if error:
        return None, error
    logo, error = save_logo(data.get("logo"))
    if error:
        return None, error
    fields["logo"] = logo          # None means no new logo
    return fields, None