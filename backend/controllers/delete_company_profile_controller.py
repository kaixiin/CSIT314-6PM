# DELETE COMPANY PROFILE - #17
# Controller: DeleteCompanyProfileC
# Methods:
#   delete_company_profile(account_id:int): bool
#   (returns None if this account has no company profile)

from models.company_profile import CompanyProfile


class DeleteCompanyProfileC:
    def delete_company_profile(self, account_id):
        company = CompanyProfile.view_company_profile(account_id)
        if company is None:
            return None
        return CompanyProfile.delete_company_profile(company.company_id)