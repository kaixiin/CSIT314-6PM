from extensions import db
from datetime import datetime

class IDP(db.Model):
    __tablename__ = "idp"

    idp_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("user_account.account_id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("idp_category.category_id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(255), nullable=False)
    budget = db.Column(db.Numeric(12, 2), nullable=False)
    status = db.Column(db.Enum('Current', 'Past'), nullable=False, default='Current')
    images = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def to_dict(self):
        # Parse images JSON if it exists
        images_list = []
        if self.images:
            # If images is already a list (from JSON column)
            if isinstance(self.images, list):
                images_list = [
                    img if img.startswith(("http://", "https://")) else f"/api/idp-images/{img}"
                    for img in self.images
                ]
            # If images is stored as JSON string, parse it
            elif isinstance(self.images, str):
                import json
                try:
                    parsed = json.loads(self.images)
                    images_list = [
                        img if img.startswith(("http://", "https://")) else f"/api/idp-images/{img}"
                        for img in parsed
                    ]
                except:
                    images_list = []
        
        return {
            "idp_id": self.idp_id,
            "account_id": self.account_id,
            "category_id": self.category_id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "budget": float(self.budget) if self.budget else 0.0,
            "status": self.status,
            "images": images_list,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
