from models.company_profile import CompanyProfile
from models.idp import IDP

# COMPANY PROFILE
# -----------------------------------------
# CREATE COMPANY PROFILE - #15
# Controller: CreateCompanyProfileC
# Methods:
#   create_company_profile(account_id, company_name, description, address, contact_number, email, logo): bool

class CreateCompanyProfileC:
    def create_company_profile(self, account_id, company_name, description,
                               address, contact_number, email, logo):
        return CompanyProfile.create_company_profile(
            account_id, company_name, description, address, contact_number, email, logo)

# -----------------------------------------
#VIEW COMPANY PROFILE - #16
# Controller: ViewCompanyProfileC
# Methods:
#   view_company_profile(account_id:int): CompanyProfile

class ViewCompanyProfileC:
    def view_company_profile(self, account_id):
        return CompanyProfile.view_company_profile(account_id)

# -----------------------------------------
# UPDATE COMPANY PROFILE - #17
# Controller: UpdateCompanyProfileC
# Methods:
#   update_company_profile(account_id, company_name, description, address, contact_number, email, logo): bool
#   (returns None if this account has no company profile)

class UpdateCompanyProfileC:
    def update_company_profile(self, account_id, company_name, description,
                               address, contact_number, email, logo):
        company = CompanyProfile.view_company_profile(account_id)
        if company is None:
            return None
        return CompanyProfile.update_company_profile(
            company.company_id, company_name, description,
            address, contact_number, email, logo)
# -----------------------------------------
# DELETE COMPANY PROFILE - #18
# Controller: DeleteCompanyProfileC
# Methods:
#   delete_company_profile(account_id:int): bool
#   (returns None if this account has no company profile)

class DeleteCompanyProfileC:
    def delete_company_profile(self, account_id):
        company = CompanyProfile.view_company_profile(account_id)
        if company is None:
            return None
        return CompanyProfile.delete_company_profile(company.company_id)
# -----------------------------------------
# SEARCH COMPANY PROFILE - #19
# Controller: SearchCompanyProfileC
# Methods:
#   search_company_profile(company_name:str): List[CompanyProfile]

class SearchCompanyProfileC:
    def search_company_profile(self, company_name, exclude_account_id=None):
        return CompanyProfile.search_company_profile(company_name, exclude_account_id)

# IDP
# -----------------------------------------
# CREATE IDP (PAST + PRESENT) - #20, 25
# Controller: CreateIDPC
# Methods:
#   create_idp(account_id, category_id, title, description, location, budget, status, images) : IDP

class CreateIDPC:
    def create_idp(self, account_id, category_id, title, description, location, budget, status, images=None):
        return IDP.create_idp(account_id, category_id, title, description, location, budget, status, images)

# -----------------------------------------
# ID VIEW IDP - #21, 26
# Controller: IDViewIDPC
# Methods:
#   id_view_idp()
# Calls: IDP.id_view_idp() in models/idp.py
 
class IDViewIDPC:
    def id_view_idp(self, idp_id, account_id):
        idp = IDP.id_view_idp(idp_id, account_id)

        return idp

# -----------------------------------------
# UPDATE IDP - #22, 27
# Controller:UpdateIDPC
# Methods:
#   update_idp()
# Calls: IDP.update_idp() in models/idp.py
 
class UpdateIDPC:
    def update_idp(self, idp_id, title=None, description=None, location=None,
                   budget=None, category_id=None, status=None, images=None):
        
        is_updated = IDP.update_idp(idp_id, title=title, description=description, location=location, 
                budget=budget, category_id=category_id, status=status, images=images)

        return is_updated

# -----------------------------------------
# DELETE IDP - #23, 28
# Controller:DeleteIDPC
# Methods:
#   delete_idp()
# Calls: IDP.delete_idp() in models/idp.py
 
class DeleteIDPC:
    def delete_idp(self, account_id, idp_id):
        
        is_deleted = IDP.delete_idp(account_id, idp_id)

        return is_deleted

# -----------------------------------------
# ID SEARCH IDP - #24, 29
# Controller: IDSearchIDPC
# Methods:
#   search_my_idp()
# Calls: IDP.search_my_idp() in models/idp.py
 
class IDSearchIDPC:
    def search_my_idp(self, account_id, keyword, status=None):
        return IDP.search_my_idp(account_id, keyword, status)