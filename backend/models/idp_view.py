from extensions import db
from datetime import datetime

class IDPView(db.Model):
    __tablename__ = "idp_view"

    view_id = db.Column(db.Integer, primary_key=True)
    idp_id = db.Column(db.Integer, db.ForeignKey("idp.idp_id"), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("user_account.account_id"), nullable=False)
    viewed_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def to_dict(self):
        return {
            "view_id": self.view_id,
            "idp_id": self.idp_id,
            "account_id": self.account_id,
            "viewed_at": self.viewed_at.isoformat() if self.viewed_at else None
        }

    #RECORD VIEW
    @classmethod
    def record_view(cls, idp_id, account_id):
        try:
            new_view = cls(idp_id=idp_id, account_id=account_id)
            db.session.add(new_view)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error recording view: {e}")
            return False

    #COUNT VIEWS - #37
    @staticmethod
    def count_views(idp_id):
        
        try:
            count = db.session.query(IDPView).filter_by(idp_id=idp_id).count()
            return count
        
        except Exception as e:
            print(f"Error counting views: {e}")
            return 0