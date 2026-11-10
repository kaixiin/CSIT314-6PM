from flask import jsonify
from datetime import datetime, timedelta
from controllers.pm_controller import GenerateReportC

# -----------------------------------------
# GENERATE REPORT (daily, weekly, monthly) - #46, #47, #48
# Boundary: GenerateReportPg
# Methods: generate_report(period), display_report(...), display_fail(message, status)

PERIOD_DAYS = {"daily": 1, "weekly": 7, "monthly": 30}   # the window ends today
TOP_LIMIT = 5


class GenerateReportPg:
    def generate_report(self, period):
        period = (period or "").strip().lower()
        if period not in PERIOD_DAYS:
            return self.display_fail("Period must be daily, weekly or monthly")

        days = PERIOD_DAYS[period]
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start = today - timedelta(days=days - 1)       # first day of the window
        end = today + timedelta(days=1)                # up to, not including, tomorrow
        prev_start = start - timedelta(days=days)      # the same length, just before it

        report = GenerateReportC().generate_report(start, end, prev_start, start, TOP_LIMIT)
        if report is None:
            return self.display_fail("Could not generate the report", 500)
        return self.display_report(period, start, today, report)

    def display_report(self, period, start, today, report):
        report.update({
            "period": period,
            "start_date": start.date().isoformat(),
            "end_date": today.date().isoformat(),
            "generated_at": datetime.now().replace(microsecond=0).isoformat(),
        })
        return jsonify({"success": True, "report": report}), 200

    def display_fail(self, message, status=400):
        return jsonify({"success": False, "message": message}), status