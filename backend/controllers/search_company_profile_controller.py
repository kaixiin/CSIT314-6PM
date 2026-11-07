# SEARCH COMPANY PROFILE - #19
# Controller: SearchCompanyProfileC
# Methods:
#   search_company_profile(company_name:str): List[CompanyProfile]

from models.company_profile import CompanyProfile


class SearchCompanyProfileC:
    def search_company_profile(self, company_name, exclude_account_id=None):
        return CompanyProfile.search_company_profile(company_name, exclude_account_id)