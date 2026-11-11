from flask import jsonify, session
from controllers.pm_controller import (
    CreateIDPCategoryC, ViewIDPCategoryC, UpdateIDPCategoryC,
    SuspendIDPCategoryC, SearchIDPCategoryC)

MAX_NAME = 100            
MAX_DESCRIPTION = 500

def read_category_fields(data):
    """Return (fields, error). error is a message to show, or None if the input is fine."""
    data = data if isinstance(data, dict) else {}
    name = data.get("name")
    description = data.get("description")
    
    if not isinstance(name, str) or not isinstance(description, str):
        return None, "Please fill in all fields"
        
    name = name.strip()
    description = description.strip()
    
    if not name or not description:
        return None, "Please fill in all fields"
        
    if len(name) > MAX_NAME:
        return None, f"Name must be {MAX_NAME} characters or less"
        
    if len(description) > MAX_DESCRIPTION:
        return None, f"Description must be {MAX_DESCRIPTION} characters or less"
        
    return {"name": name, "description": description}, None