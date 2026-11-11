# Route for the PM reports (the PM role check is in pm_routes.py)
#   GET /api/pm/reports?period=daily|weekly|monthly

from flask import request
from routes.pm_routes import pm_bp
from boundaries.generate_report_boundary import GenerateReportPg


@pm_bp.route("/reports", methods=["GET"])
def generate_report():
    return GenerateReportPg().generate_report(request.args.get("period"))