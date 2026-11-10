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
