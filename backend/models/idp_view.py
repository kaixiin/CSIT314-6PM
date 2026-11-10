from models.idp import IDP
from models.idp_category import IDPCategory

# Entity: IDPView
# Methods used by the PM reports:
#   count_views_between(start_date:datetime, end_date:datetime): int
#   top_viewed_idp(start_date:datetime, end_date:datetime, limit:int): List[dict]
# (record_view and count_views belong to the IDP view story, which adds them to this class)

from datetime import datetime
from extensions import db
from models.idp import IDP
from models.idp_category import IDPCategory
import models.user_account    # makes sure the user_account table is known for the foreign key


class IDPView(db.Model):
    __tablename__ = "idp_view"

    view_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("user_account.account_id"), nullable=False)
    idp_id = db.Column(db.Integer, db.ForeignKey("idp.idp_id"), nullable=False)
    viewed_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

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

    @staticmethod
    def count_views_between(start_date, end_date):
        """Views from start_date up to, but not including, end_date."""
        return IDPView.query.filter(IDPView.viewed_at >= start_date,
                                        IDPView.viewed_at < end_date).count()