#VIEW COMPANY PROFILE - #16
# Controller: ViewCompanyProfileC
# Methods:
#   view_company_profile(account_id:int): CompanyProfile

from models.company_profile import CompanyProfile


class ViewCompanyProfileC:
    def view_company_profile(self, account_id):
        return CompanyProfile.view_company_profile(account_id)