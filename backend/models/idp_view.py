from extensions import db
from datetime import datetime
from models.idp import IDP
from models.idp_category import IDPCategory

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

    @staticmethod
    def count_views_between(start_date, end_date):
        """Views from start_date up to, but not including, end_date."""
        return IDPView.query.filter(IDPView.viewed_at >= start_date,
                                    IDPView.viewed_at < end_date).count()

    @staticmethod
    def top_viewed_idp(start_date, end_date, limit):
        """The most viewed IDPs in the period, with their category."""
        views = db.func.count().label("views")
        rows = (db.session.query(IDP.idp_id, IDP.title, IDPCategory.name, views)
                .select_from(IDPView)
                .join(IDP, IDPView.idp_id == IDP.idp_id)
                .join(IDPCategory, IDP.category_id == IDPCategory.category_id)
                .filter(IDPView.viewed_at >= start_date, IDPView.viewed_at < end_date)
                .group_by(IDP.idp_id, IDP.title, IDPCategory.name)
                .order_by(views.desc(), IDP.title)
                .limit(limit)
                .all())
        return [{"idp_id": i, "title": t, "category": c, "views": int(v)}
                for i, t, c, v in rows]
