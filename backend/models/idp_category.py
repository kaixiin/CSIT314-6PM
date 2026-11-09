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
