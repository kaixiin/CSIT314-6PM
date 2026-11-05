# Entity: CompanyProfile
# Methods:
#   has_company_profile(account_id:int): bool
#   is_name_taken(company_name:str, exclude_company_id:int): bool
#   create_company_profile(account_id, company_name, description, address, contact_number, email, logo): bool
#   view_company_profile(account_id:int): CompanyProfile
#   update_company_profile(company_id, company_name, description, address, contact_number, email, logo): bool
#   delete_company_profile(company_id:int): bool
#   search_company_profile(company_name:str): List[CompanyProfile]

from datetime import datetime
from extensions import db
import models.user_account    # makes sure the user_account table is known for the foreign key


class CompanyProfile(db.Model):
    __tablename__ = "company_profile"

    company_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("user_account.account_id"),
                           unique=True, nullable=False)
    company_name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    logo = db.Column(db.String(255))
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        if not self.logo:
            logo_url = None
        elif self.logo.startswith(("http://", "https://")):
            logo_url = self.logo                      # e.g. a link in the seed data
        else:
            logo_url = f"/api/logos/{self.logo}"
        return {
            "company_id": self.company_id,
            "account_id": self.account_id,
            "company_name": self.company_name,
            "description": self.description,
            "address": self.address,
            "contact_number": self.contact_number,
            "email": self.email,
            "logo_url": logo_url,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def has_company_profile(account_id):
        return db.session.query(
            CompanyProfile.query.filter_by(account_id=account_id).exists()).scalar()

    @staticmethod
    def is_name_taken(company_name, exclude_company_id=None):
        """True if another company already uses this name (ignoring letter case)."""
        query = CompanyProfile.query.filter(
            db.func.lower(CompanyProfile.company_name) == company_name.lower())
        if exclude_company_id is not None:
            query = query.filter(CompanyProfile.company_id != exclude_company_id)
        return db.session.query(query.exists()).scalar()

    @classmethod
    def create_company_profile(cls, account_id, company_name, description,
                               address, contact_number, email, logo=None):
        if cls.has_company_profile(account_id) or cls.is_name_taken(company_name):
            return False
        try:
            db.session.add(cls(account_id=account_id, company_name=company_name,
                               description=description, address=address,
                               contact_number=contact_number, email=email, logo=logo))
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"create_company_profile failed: {e}")
            return False

    @staticmethod
    def view_company_profile(account_id):
        """Return this account's company, or None."""
        return CompanyProfile.query.filter_by(account_id=account_id).first()

    @classmethod
    def update_company_profile(cls, company_id, company_name, description,
                               address, contact_number, email, logo=None):
        """logo=None keeps the current logo."""
        company = db.session.get(cls, company_id)
        if company is None or cls.is_name_taken(company_name, exclude_company_id=company_id):
            return False
        try:
            company.company_name = company_name
            company.description = description
            company.address = address
            company.contact_number = contact_number
            company.email = email
            if logo is not None:
                company.logo = logo
            company.updated_at = datetime.now()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"update_company_profile failed: {e}")
            return False

    @classmethod
    def delete_company_profile(cls, company_id):
        company = db.session.get(cls, company_id)
        if company is None:
            return False
        try:
            db.session.delete(company)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"delete_company_profile failed: {e}")
            return False

    @staticmethod
    def search_company_profile(company_name, exclude_account_id=None):
        """Partial, case-insensitive match on the company name. Empty text lists all.
        exclude_account_id leaves out that account's own company."""
        query = CompanyProfile.query.filter(
            CompanyProfile.company_name.ilike(f"%{company_name}%"))
        if exclude_account_id is not None:
            query = query.filter(CompanyProfile.account_id != exclude_account_id)
        return query.order_by(CompanyProfile.company_name).all()