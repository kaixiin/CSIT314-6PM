import base64
import binascii
import json
import os
import uuid
import re
from decimal import Decimal, InvalidOperation
from config import Config

IMAGE_PATTERN = re.compile(r"^data:image/(png|jpeg);base64,(.+)\$", re.DOTALL)
MAX_IMAGE_BYTES = 5 * 1024 * 1024
UPLOAD_FOLDER = Config.UPLOAD_FOLDER  # or os.path.join("uploads", "idp-images")

def read_idp_fields(data):
    """
    Validate IDP text fields.
    Return (fields, error). error is a message to show, or None if the input is fine.
    """
    data = data if isinstance(data, dict) else {}
    
    # Required field names
    names = ("title", "description", "location", "budget", "category_id")
    values = {name: data.get(name) for name in names}
    
    # Check all required fields are provided
    if not all(v is not None for v in values.values()):
        return None, "Please fill in all required fields"
    
    # Validate title
    if not isinstance(values["title"], str):
        return None, "Title must be text"
    values["title"] = values["title"].strip()
    if not values["title"]:
        return None, "Title cannot be empty"
    if len(values["title"]) > 100:
        return None, "Title must be 100 characters or less"
    
    # Validate description
    if not isinstance(values["description"], str):
        return None, "Description must be text"
    values["description"] = values["description"].strip()
    if not values["description"]:
        return None, "Description cannot be empty"
    
    # Validate location
    if not isinstance(values["location"], str):
        return None, "Location must be text"
    values["location"] = values["location"].strip()
    if not values["location"]:
        return None, "Location cannot be empty"
    if len(values["location"]) > 255:
        return None, "Location must be 255 characters or less"
    
    # Validate budget (DECIMAL(12,2))
    try:
        if isinstance(values["budget"], str):
            budget = Decimal(values["budget"])
        elif isinstance(values["budget"], (int, float)):
            budget = Decimal(str(values["budget"]))
        else:
            budget = Decimal(values["budget"])
        
        if budget < 0:
            return None, "Budget must be a positive number"
        if budget > Decimal("9999999999.99"):
            return None, "Budget exceeds maximum allowed value"
        
        values["budget"] = float(budget)
        
    except (InvalidOperation, ValueError, TypeError):
        return None, "Please enter a valid budget amount"
    
    # Validate category_id
    try:
        category_id = int(values["category_id"])
        if category_id < 1:
            return None, "Invalid category"
        values["category_id"] = category_id
    except (ValueError, TypeError):
        return None, "Invalid category"
    
    # Status is optional, defaults to 'Current'
    status = data.get("status", "Current")
    if status not in ["Current", "Past"]:
        return None, "Status must be 'Current' or 'Past'"
    values["status"] = status
    
    return values, None

def save_idp_image(image_data):
    """
    Save a single IDP image (base64 data URL).
    Return (filename, error). filename is None when no image was sent.
    """
    if image_data is None or image_data == "":
        return None, None
    
    match = IMAGE_PATTERN.match(image_data) if isinstance(image_data, str) else None
    if not match:
        return None, "Image must be a JPG or PNG"
    
    try:
        raw = base64.b64decode(match.group(2), validate=True)
    except (binascii.Error, ValueError):
        return None, "Invalid image data"
    
    if len(raw) > MAX_IMAGE_BYTES:
        return None, "Image must be 5MB or smaller"
    
    is_png = match.group(1) == "png" and raw.startswith(b"\x89PNG\r\n\x1a\n")
    is_jpg = match.group(1) == "jpeg" and raw.startswith(b"\xff\xd8\xff")
    if not (is_png or is_jpg):
        return None, "Image must be a JPG or PNG"
    
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filename = f"{uuid.uuid4().hex}.{'png' if is_png else 'jpg'}"
    with open(os.path.join(UPLOAD_FOLDER, filename), "wb") as f:
        f.write(raw)
    
    return filename, None

def save_idp_images(images):
    """
    Save multiple IDP images.
    images can be:
      - None/empty: no images
      - List of base64 data URLs
      - Single base64 data URL
    Return (filenames_list, error).
    """
    if images is None or images == "":
        return [], None
    
    # Convert single image to list
    if isinstance(images, str):
        images = [images]
    
    if not isinstance(images, list):
        return None, "Images must be a list"
    
    if len(images) > 10:
        return None, "Maximum 10 images allowed"
    
    saved_filenames = []
    
    for idx, img in enumerate(images):
        filename, error = save_idp_image(img)
        if error:
            # Cleanup already saved images
            for saved in saved_filenames:
                remove_idp_image(saved)
            return None, f"Image {idx + 1}: {error}"
        if filename:
            saved_filenames.append(filename)
    
    return saved_filenames, None

def remove_idp_image(filename):
    """Delete a saved IDP image file."""
    if filename:
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, filename))
        except OSError:
            pass

def remove_idp_images(filenames):
    """Delete multiple saved IDP image files."""
    if filenames and isinstance(filenames, list):
        for filename in filenames:
            remove_idp_image(filename)

def read_idp_form(data):
    """
    Validate IDP form: check text fields, then save images.
    Return (fields, error).
    """
    # Validate text fields
    fields, error = read_idp_fields(data)
    if error:
        return None, error
    
    # Save images (optional)
    images, error = save_idp_images(data.get("images"))
    if error:
        return None, error
    
    # Add images to fields (empty list if no images)
    fields["images"] = json.dumps(images) if images else None
    
    return fields, None

def validate_update_idp_fields(data):
    """
    Validate IDP update fields (partial updates allowed).
    Return (validated_fields, error).
    """
    data = data if isinstance(data, dict) else {}
    validated = {}
    
    # Title (optional for update)
    if "title" in data:
        title = data.get("title")
        if not isinstance(title, str):
            return None, "Title must be text"
        title = title.strip()
        if not title:
            return None, "Title cannot be empty"
        if len(title) > 100:
            return None, "Title must be 100 characters or less"
        validated["title"] = title
    
    # Description (optional for update)
    if "description" in data:
        description = data.get("description")
        if not isinstance(description, str):
            return None, "Description must be text"
        description = description.strip()
        if not description:
            return None, "Description cannot be empty"
        validated["description"] = description
    
    # Location (optional for update)
    if "location" in data:
        location = data.get("location")
        if not isinstance(location, str):
            return None, "Location must be text"
        location = location.strip()
        if not location:
            return None, "Location cannot be empty"
        if len(location) > 255:
            return None, "Location must be 255 characters or less"
        validated["location"] = location
    
    # Budget (optional for update)
    if "budget" in data:
        try:
            budget = Decimal(str(data["budget"]))
            if budget < 0:
                return None, "Budget must be a positive number"
            if budget > Decimal("9999999999.99"):
                return None, "Budget exceeds maximum allowed value"
            validated["budget"] = float(budget)
        except (InvalidOperation, ValueError, TypeError):
            return None, "Please enter a valid budget amount"
    
    # Category ID (optional for update)
    if "category_id" in data:
        try:
            category_id = int(data["category_id"])
            if category_id < 1:
                return None, "Invalid category"
            validated["category_id"] = category_id
        except (ValueError, TypeError):
            return None, "Invalid category"
    
    # Status (optional for update)
    if "status" in data:
        status = data.get("status")
        if status not in ["Current", "Past"]:
            return None, "Status must be 'Current' or 'Past'"
        validated["status"] = status
    
    # Images (optional for update)
    if "images" in data:
        images, error = save_idp_images(data.get("images"))
        if error:
            return None, error
        validated["images"] = json.dumps(images) if images else None
    
    # Check at least one field is being updated
    if not validated:
        return None, "No fields provided for update"
    
    return validated, None

