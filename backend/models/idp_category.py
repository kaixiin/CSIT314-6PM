# Entity: IDPCategory - #41, #42, #43, #44, #45
# Methods:
#   check_existing(name:str, category_id:int): bool
#   create_idp_category(name:str, description:str): bool
#   view_idp_category(category_id:int): IDPCategory
#   update_idp_category(category_id:int, name:str, description:str): bool
#   suspend_idp_category(category_id:int): bool
#   search_idp_category(name:str, include_suspended:bool): List[IDPCategory]

from extensions import db

class IDPCategory(db.Model):
    __tablename__ = "idp_category"

    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    is_suspended = db.Column(db.Boolean, default = False)

    def to_dict(self):
        return {
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description,
            "isSuspended":self.is_suspended
        }
    @staticmethod
    def check_existing(name, category_id=None):
        """True if another category already uses this name (ignoring letter case)."""
        query = IDPCategory.query.filter(db.func.lower(IDPCategory.name) == name.lower())
        if category_id is not None:
            query = query.filter(IDPCategory.category_id != category_id)
        return db.session.query(query.exists()).scalar()

    @classmethod
    def create_idp_category(cls, name, description):
        if cls.check_existing(name):
            return False
        try:
            db.session.add(cls(name=name, description=description))
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"create_idp_category failed: {e}")
            return False

    @staticmethod
    def view_idp_category(category_id):
        """Return the category, or None."""
        return db.session.get(IDPCategory, category_id)

    @classmethod
    def update_idp_category(cls, category_id, name, description):
        category = db.session.get(cls, category_id)
        if category is None or cls.check_existing(name, category_id):
            return False
        try:
            category.name = name
            category.description = description
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"update_idp_category failed: {e}")
            return False

    @classmethod
    def suspend_idp_category(cls, category_id, is_suspended=True):
        """Set is_suspended (True suspends, False reactivates). False if the account is missing or saving fails."""
        category = db.session.get(cls, category_id)
        if category is None:
            return False
        try:
            category.is_suspended = is_suspended
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"suspend_idp_category failed: {e}")
            return False

    @staticmethod
    def search_idp_category(name, include_suspended=True):
        """Partial, case-insensitive match on the name. Empty text lists all."""
        query = IDPCategory.query.filter(IDPCategory.name.ilike(f"%{name}%"))
        if not include_suspended:
            query = query.filter(IDPCategory.is_suspended.is_not(True))
        return query.order_by(IDPCategory.name).all()

    @classmethod
    def get_all_categories(cls):
    
        try:
            categories = db.session.query(cls).order_by(cls.name).all()
            return categories
        except Exception as e:
            print(f"Error fetching categories: {e}")
            return None