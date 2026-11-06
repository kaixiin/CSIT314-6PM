def validate_user_profile_fields(data, require_all=True):
    
    data = data if isinstance(data, dict) else {}
    validated = {}
    
    # --- NAME ---
    if "name" in data:
        name = data.get("name")
        
        if not isinstance(name, str):
            return None, "Name must be text"
        
        name = name.strip()
        
        if not name:
            return None, "Profile name cannot be empty"
        
        if len(name) > 50:
            return None, "Profile name must be 50 characters or less"
        
    # --- ACCOUNT_TYPE ---
        account_type = name.replace(" ", "")
        
        if len(account_type) > 50:
            return None, "Profile name is too long (account type exceeds 50 characters)"
        
        validated["name"] = name
        validated["account_type"] = account_type
        
    elif require_all:
        return None, "Profile name is required"
    
    # --- DESCRIPTION ---
    if "description" in data:
        description = data.get("description")
        
        if not isinstance(description, str):
            return None, "Description must be text"
        
        description = description.strip()
        
        if not description:
            return None, "Description cannot be empty"
        
        if len(description) > 255:
            return None, "Description must be 255 characters or less"
        
        validated["description"] = description
        
    elif require_all:
        return None, "Description is required"
    
    if not require_all and not validated:
        return None, "No fields provided for update"
    
    return validated, None

# Convenience functions for clarity
def validate_create(data):
    return validate_user_profile_fields(data, require_all=True)

def validate_update(data):
    return validate_user_profile_fields(data, require_all=False)