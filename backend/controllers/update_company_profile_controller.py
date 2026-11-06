# UPDATE COMPANY PROFILE - #17
# Controller: UpdateCompanyProfileC
# Methods:
#   update_company_profile(account_id, company_name, description, address, contact_number, email, logo): bool
#   (returns None if this account has no company profile)

from models.company_profile import CompanyProfile


class UpdateCompanyProfileC:
    def update_company_profile(self, account_id, company_name, description,
                               address, contact_number, email, logo):
        company = CompanyProfile.view_company_profile(account_id)
        if company is None:
            return None
        return CompanyProfile.update_company_profile(
            company.company_id, company_name, description,
            address, contact_number, email, logo)