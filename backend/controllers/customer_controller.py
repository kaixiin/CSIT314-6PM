from models.idp import IDP
from models.idp_view import IDPView
from models.favourite import Favourite
from models.company_profile import CompanyProfile

# CUSTOMER ACCESS
# -----------------------------------------
# CUST SEARCH IDP - #32
# Controller: CustSearchIDPC
# Methods:
#   search_idp(self, keyword, category_id)
# Calls: IDP.search_idp() in models/idp.py
class CustSearchIDPC:
    def search_idp(self, keyword, category_id=None):
        return IDP.search_idp(keyword, category_id)

# -----------------------------------------
# CUST VIEW IDP - #33
# Controller: CustViewIDPC
# Methods:
#   view_idp(self, idp_id, account_id)
# Calls: IDP.view_idp() in models/idp.py 
#        IDPView.record_view in models/idp_view.py
class CustViewIDPC:
    def view_idp(self, idp_id, account_id):
       
        idp = IDP.view_idp(idp_id)
        
        if idp is None:
            return None, False
        
        recorded = IDPView.record_view(idp_id, account_id)
        
        return idp, recorded

    def project_details(self, idp, account_id):
        # The designer's company contact and whether this customer saved the project
        company = CompanyProfile.view_company_profile(idp.account_id)
        return {
            "company_name": company.company_name if company else "",
            "company_email": company.email if company else "",
            "company_phone": company.contact_number if company else "",
            "is_saved": Favourite.is_saved(account_id, idp.idp_id),
        }

# -----------------------------------------
#CUSTOMER SHORTLIST
# -----------------------------------------
# SHORTLIST IDP - #34
# Controller: ShortlistIDPC
# Methods:
#   save_favourite(self, account_id, idp_id)
# Calls: Favourite.save_favourite() in models/favourite.py 
class ShortlistIDPC:
    def save_favourite(self, account_id, idp_id):
        return Favourite.save_favourite(account_id, idp_id)

# -----------------------------------------
# VIEW SHORTLIST IDP - #35
# Controller: ViewShortlistedIDPC
# Methods:
#   view_favourite_list(self, account_id, idp_id)
# Calls: Favourite.view_favourite_list() in models/favourite.py 
class ViewShortlistedIDPC:
    
    def view_favourite_list(self, account_id):
       
        idp_ids = Favourite.view_favourite_list(account_id)
        
        if idp_ids is None:
            return None  
        
        if len(idp_ids) == 0:
            return []  
        
        idps = []
        for idp_id in idp_ids:
            idp = IDP.view_idp(idp_id)

            # only add if IDP still exists
            if idp:  
                idps.append(idp)
        
        return idps

# -----------------------------------------
# SEARCH SHORTLIST IDP - #35
# Controller: SearchShortlistedIDPC
# Methods:
#   search_favourite(self, account_id, keyword)
# Calls: Favourite.search_favourite() in models/favourite.py 
class SearchShortlistedIDPC:
    
    def search_favourite(self, account_id, keyword):
   
        idp_ids = Favourite.search_favourite(account_id, keyword)
        
        if idp_ids is None:
            return None  
        
        if len(idp_ids) == 0:
            return [] 
        
        idps = []
        for idp_id in idp_ids:
            idp = IDP.view_idp(idp_id)
            if idp:
                idps.append(idp)
        
        return idps


