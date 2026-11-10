from models.idp import IDP

# CUSTOMER ACCESS
# -----------------------------------------
# SEARCH IDP - #32
# Controller: CustSearchIDPC
# Methods:
#   search_idp(self, keyword, category_id)
# Calls: IDP.search_idp() in models/idp.py
class CustSearchIDPC:
    def search_idp(self, keyword, category_id=None):
        return IDP.search_idp(keyword, category_id)
