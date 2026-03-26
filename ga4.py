#!/usr/bin/env python3
"""
GA4 Analytics query runner for CIM (cim.io).

Standalone script — no MCP dependency. Talks directly to the
Google Analytics Data API v1beta and Admin API v1beta.

Requirements (install once):
    pip install google-analytics-data google-analytics-admin

Auth: uses Application Default Credentials.
    gcloud auth application-default login
    gcloud auth application-default set-quota-project cim-analytics-mcp
"""

import argparse
import json
import os
import sys

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    RunRealtimeReportRequest,
)
from google.analytics.admin_v1beta import AnalyticsAdminServiceClient

PROPERTY_ID = os.environ.get("GA4_PROPERTY_ID", "274384629")


def _rows_to_dicts(response) -> list[dict]:
    dim_headers = [h.name for h in response.dimension_headers]
    met_headers = [h.name for h in response.metric_headers]
    rows = []
    for row in response.rows:
        d = {}
        for i, dv in enumerate(row.dimension_values):
            d[dim_headers[i]] = dv.value
        for i, mv in enumerate(row.metric_values):
            d[met_headers[i]] = mv.value
        rows.append(d)
    return rows


def run_report(metrics, dimensions=None, start_date="28daysAgo",
               end_date="yesterday", limit=100, property_id=None):
    pid = property_id or PROPERTY_ID
    client = BetaAnalyticsDataClient()
    request = RunReportRequest(
        property=f"properties/{pid}",
        metrics=[Metric(name=m) for m in metrics],
        dimensions=[Dimension(name=d) for d in (dimensions or [])],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        limit=limit,
    )
    response = client.run_report(request)
    return {"row_count": response.row_count, "rows": _rows_to_dicts(response)}


def run_realtime(metrics=None, dimensions=None, limit=50, property_id=None):
    pid = property_id or PROPERTY_ID
    client = BetaAnalyticsDataClient()
    request = RunRealtimeReportRequest(
        property=f"properties/{pid}",
        metrics=[Metric(name=m) for m in (metrics or ["activeUsers"])],
        dimensions=[Dimension(name=d) for d in (dimensions or [])],
        limit=limit,
    )
    response = client.run_realtime_report(request)
    return {"row_count": response.row_count, "rows": _rows_to_dicts(response)}


def get_property_details(property_id=None):
    pid = property_id or PROPERTY_ID
    client = AnalyticsAdminServiceClient()
    prop = client.get_property(name=f"properties/{pid}")
    return {
        "property_id": pid,
        "display_name": prop.display_name,
        "time_zone": prop.time_zone,
        "currency_code": prop.currency_code,
        "industry_category": str(prop.industry_category),
        "create_time": prop.create_time.isoformat() if prop.create_time else None,
    }


PRESETS = {
    "realtime": lambda args: run_realtime(
        dimensions=args.dimensions, limit=args.limit),
    "top-pages": lambda args: run_report(
        metrics=["screenPageViews", "activeUsers", "averageSessionDuration"],
        dimensions=["pagePath", "pageTitle"],
        start_date=args.start, end_date=args.end, limit=args.limit),
    "traffic-sources": lambda args: run_report(
        metrics=["sessions", "activeUsers", "bounceRate"],
        dimensions=["sessionSource", "sessionMedium"],
        start_date=args.start, end_date=args.end, limit=args.limit),
    "demographics": lambda args: run_report(
        metrics=["activeUsers", "sessions"],
        dimensions=["country", "deviceCategory"],
        start_date=args.start, end_date=args.end, limit=args.limit),
    "property": lambda args: get_property_details(),
    "custom": lambda args: run_report(
        metrics=args.metrics, dimensions=args.dimensions,
        start_date=args.start, end_date=args.end, limit=args.limit),
}


def main():
    parser = argparse.ArgumentParser(description="GA4 Analytics for CIM")
    parser.add_argument("preset", choices=PRESETS.keys(),
                        help="Report preset to run")
    parser.add_argument("--metrics", nargs="+", default=["activeUsers"])
    parser.add_argument("--dimensions", nargs="+", default=None)
    parser.add_argument("--start", default="7daysAgo")
    parser.add_argument("--end", default="yesterday")
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    result = PRESETS[args.preset](args)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
