from models.idp_category import IDPCategory

# IDP CATEGORY
# -----------------------------------------
# CREATE IDP CATEGORY - #41
# Controller: CreateIDPCategoryC
# Methods:
#   create_idp_category(name:str, description:str): bool

class CreateIDPCategoryC:
    def create_idp_category(self, name, description):
        return IDPCategory.create_idp_category(name, description)

# -----------------------------------------
# VIEW IDP CATEGORY - #42
# Controller: ViewIDPCategoryC
# Methods:
#   view_idp_category(category_id:int, include_suspended:bool): IDPCategory
#   (returns None if it does not exist, or is suspended and include_suspended is False)

class ViewIDPCategoryC:
    def view_idp_category(self, category_id):
        return IDPCategory.view_idp_category(category_id)

# -----------------------------------------
# UPDATE IDP CATEGORY - #43
# Controller: UpdateIDPCategoryC
# Methods:
#   update_idp_category(category_id:int, name:str, description:str): bool
#   (returns None if the category does not exist)

class UpdateIDPCategoryC:
    def update_idp_category(self, category_id, name, description):
        if IDPCategory.view_idp_category(category_id) is None:
            return None
        return IDPCategory.update_idp_category(category_id, name, description)

# -----------------------------------------
# SUSPEND IDP CATEGORY - #44
# Controller: SuspendIDPCategoryC
# Methods:
#   suspend_idp_category(category_id:int): bool
#   (returns None if the category does not exist)

class SuspendIDPCategoryC:
    def suspend_idp_category(self, category_id, is_suspended):
        if IDPCategory.view_idp_category(category_id) is None:
            return None
        return IDPCategory.suspend_idp_category(category_id, is_suspended)

# -----------------------------------------
# SEARCH IDP CATEGORY - #45
# Controller: SearchIDPCategoryC
# Methods:
#   search_idp_category(name:str, include_suspended:bool): List[IDPCategory]

class SearchIDPCategoryC:
    def search_idp_category(self, name):
        return IDPCategory.search_idp_category(name)