# Entity: Favourite
# Methods used by the PM reports:
#   count_shortlists_between(start_date:datetime, end_date:datetime): int
# (save_favourite, view_favourite_list and the rest belong to the favourite stories, which add them to this class)

from datetime import datetime
from extensions import db
import models.idp             # make sure the idp and user_account tables are known for the foreign keys
import models.user_account


class Favourite(db.Model):
    __tablename__ = "favourite"

    favourite_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey("user_account.account_id"), nullable=False)
    idp_id = db.Column(db.Integer, db.ForeignKey("idp.idp_id"), nullable=False)
    saved_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    @staticmethod
    def count_shortlists_between(start_date, end_date):
        """Times an IDP was shortlisted from start_date up to, but not including, end_date."""
        return Favourite.query.filter(Favourite.saved_at >= start_date,
                                      Favourite.saved_at < end_date).count()