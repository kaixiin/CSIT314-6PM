
from extensions import db
from datetime import datetime
import json
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from models.idp_category import IDPCategory

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
        images_list = []

        if self.images:
            if isinstance(self.images, list):
                images_list = [
                    img if img.startswith(("http://", "https://")) else f"/api/idp-images/{img}"
                    for img in self.images
                ]
            elif isinstance(self.images, str):
                try:
                    parsed = json.loads(self.images)
                    images_list = [
                        img if img.startswith(("http://", "https://")) else f"/api/idp-images/{img}"
                        for img in parsed
                    ]
                except Exception:
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

    #CREAT IDP - #20, 25
    @classmethod
    def create_idp(cls, account_id, category_id, title, description,
                   location, budget, status, images=None):
        new_idp = cls(
            account_id=account_id,
            category_id=category_id,
            title=title,
            description=description,
            location=location,
            budget=budget,
            status=status,
            images=images  
        )
        try:
            db.session.add(new_idp)
            db.session.commit()
            return new_idp

        except Exception as e:
            db.session.rollback()
            print(f"Create IDP failed: {e}")
            return False

    # ID VIEW IDP - #21, 26
    @classmethod
    def id_view_idp(cls, idp_id, account_id):
        
        try:
            idp = db.session.get(cls, idp_id)
            
            if idp is None:
                return None
            
            if idp.account_id != account_id:
                return None 
            
            return idp

        except Exception as e:
            print(f"Error fetching IDP: {e}")
            return None

    # UPDATE IDP - #22, 27
    @classmethod
    def update_idp(cls, idp_id, title=None, description=None, location=None, 
                budget=None, category_id=None, status=None, images=None):
        
        try:
            idp = db.session.get(cls, idp_id)

            if idp is None:
                return None

            # Update title if provided
            if title is not None:
                idp.title = title

            # Update description if provided
            if description is not None:
                idp.description = description

            # Update location if provided
            if location is not None:
                idp.location = location

            # Update budget if provided
            if budget is not None:
                idp.budget = budget

            # Update category_id if provided
            if category_id is not None:
                idp.category_id = category_id

            # Update status if provided
            if status is not None:
                idp.status = status

            # Update images if provided
            if images is not None:
                idp.images = images

            db.session.commit()
            return True  
    
        except IntegrityError as e:
            db.session.rollback()
            print(f"Database Integrity Error: {e.orig}")
            return False

        except Exception as e:
            db.session.rollback()
            print(f"An unexpected error occurred: {e}")
            return False

    # DELETE IDP - #22, 27
    @classmethod
    def delete_idp(cls, idp_id, account_id):
        
        try:
            idp = db.session.get(cls, idp_id)
            
            if idp is None:
                return None  

            if idp.account_id != account_id:
                return False 
            
            db.session.delete(idp)
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"delete_idp failed: {e}")
            return False

    # ID SEARCH IDP (+GET ALL IDP) - #24, 29
    @classmethod
    def search_my_idp(cls, account_id, keyword, status=None):

        try:
            query = db.session.query(cls).filter_by(account_id=account_id)
            
            if status and status in ["Current", "Past"]:
                query = query.filter_by(status=status)
            
            if keyword and keyword.strip():
                search_term = f"%{keyword}%"
                query = query.filter(
                    or_(
                        cls.title.ilike(search_term),
                        cls.description.ilike(search_term),
                        cls.location.ilike(search_term)
                    )
                )
            
            idps = query.order_by(cls.created_at.desc()).all()
            return idps
        
        except Exception as e:
            print(f"Error searching IDPs: {e}")
            return None

