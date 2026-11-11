from models.idp_category import IDPCategory
from models.idp import IDP
from models.idp_view import IDPView
from models.favourite import Favourite

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

    def idps_in_category(self, category_id):
        return IDP.idps_in_category(category_id)

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

# -----------------------------------------
# GENERATE REPORT (daily, weekly, monthly) - #46, #47, #48
# Controller: GenerateReportC
# Methods:
#   generate_report(start_date, end_date, prev_start_date, prev_end_date, limit): dict
#   (returns None if the report could not be built)

class GenerateReportC:
    def generate_report(self, start_date, end_date, prev_start_date, prev_end_date, limit):
        try:
            return {
                "new_idps": {
                    "current": IDP.count_created(start_date, end_date),
                    "previous": IDP.count_created(prev_start_date, prev_end_date),
                },
                "views": {
                    "current": IDPView.count_views_between(start_date, end_date),
                    "previous": IDPView.count_views_between(prev_start_date, prev_end_date),
                },
                "shortlists": {
                    "current": Favourite.count_shortlists_between(start_date, end_date),
                    "previous": Favourite.count_shortlists_between(prev_start_date, prev_end_date),
                },
                "top_projects": IDPView.top_viewed_idp(start_date, end_date, limit),
            }
        except Exception as e:
            print(f"generate_report failed: {e}")
            return None