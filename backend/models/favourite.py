from extensions import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from models.idp import IDP

class Favourite(db.Model):
    __tablename__ = "favourite"

    favourite_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("user_account.account_id"), nullable=False)
    idp_id = db.Column(db.Integer, db.ForeignKey("idp.idp_id"), nullable=False)
    saved_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def to_dict(self):
        return {
            "favourite_id": self.favourite_id,
            "account_id": self.account_id,
            "idp_id": self.idp_id,
            "saved_at": self.saved_at.isoformat() if self.saved_at else None
        }

    @staticmethod
    def is_saved(account_id, idp_id):
        shortlisted = Favourite.query.filter_by(account_id=account_id, idp_id=idp_id).first()
        return shortlisted is not None

    # SHORTLIST IDP - #34
    @classmethod
    def save_favourite(cls, account_id, idp_id):
        try:
        
            if cls.is_saved(account_id, idp_id):
        
                saved = cls.query.filter_by(account_id=account_id, idp_id=idp_id).first()
                db.session.delete(saved)
                db.session.commit()
                return False  
            else:
                new_favourite = cls(account_id=account_id, idp_id=idp_id)
                db.session.add(new_favourite)
                db.session.commit()
                return True  
        
        except IntegrityError as e:
            db.session.rollback()
            print(f"IntegrityError saving favourite: {e.orig}")
            return None  
        
        except Exception as e:
            db.session.rollback()
            print(f"Error saving favourite: {e}")
            return None  

    # VIEW SAVED IDPs - #35
    @classmethod
    def view_favourite_list(cls, account_id):
        try:
        
            favourites = (
                db.session.query(cls).filter_by(account_id=account_id).order_by(cls.saved_at.desc()).all()
            )
            
            return [fav.idp_id for fav in favourites]
            
        except Exception as e:
            print(f"Error getting favourite list: {e}")
            return None

    #SEARCH SHORTLISTED IDP - #36
    @classmethod
    def search_favourite(cls, account_id, keyword):
        
        try:
            search_term = f"%{keyword}%"
            
            results = (
                db.session.query(cls.idp_id)
                .join(IDP, cls.idp_id == IDP.idp_id)
                .filter(cls.account_id == account_id)
                .filter(
                    or_(
                        IDP.title.ilike(search_term),
                        IDP.description.ilike(search_term),
                        IDP.location.ilike(search_term)
                    )
                )
                .order_by(cls.saved_at.desc())
                .all()
            )
            
            return [result[0] for result in results]
            
        except Exception as e:
            print(f"Error searching favourites: {e}")
            return None