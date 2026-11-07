# CREATE COMPANY PROFILE - #15
# Controller: CreateCompanyProfileC
# Methods:
#   create_company_profile(account_id, company_name, description, address, contact_number, email, logo): bool

from models.company_profile import CompanyProfile


class CreateCompanyProfileC:
    def create_company_profile(self, account_id, company_name, description,
                               address, contact_number, email, logo):
        return CompanyProfile.create_company_profile(
            account_id, company_name, description, address, contact_number, email, logo)