import json
from sp_api.api import Orders
from sp_api.base import Marketplaces, ReportType, ProcessingStatus, Granularity
from keys import *
from datetime import datetime, timedelta
from dateutil.tz import tzlocal

CLIENT_CONFIG = {
    "lwa_app_id": LWA_APP_ID,
    "lwa_client_secret": LWA_CLIENT_SECRET,
    "aws_secret_key": AWS_SECRET_KEY,
    "aws_access_key": AWS_ACCESS_KEY,
    "role_arn": ROLE_ARN,
    "refresh_token": REFRESH_TOKEN,
}


def orders_report(period: int):
    period = period - 1
    marketplace_id = Marketplaces.GB

    # Get current timezone
    local_tz = tzlocal()
    current_time = datetime.now(local_tz) - timedelta(minutes=62)
    CreatedBefore = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time_str = datetime.now(local_tz) - timedelta(days=period)
    CreatedAfter = end_time_str.strftime("%Y-%m-%dT00:00:00Z")
    # print(CreatedAfter)
    # print(CreatedBefore)

    orders = Orders(credentials=CLIENT_CONFIG, marketplace=marketplace_id)
    res = orders.get_orders(
        CreatedAfter=CreatedAfter,
        CreatedBefore=CreatedBefore,
    )
    metrics = res.payload

    filtered_orders = [
        order for order in metrics["Orders"] if order["OrderStatus"] != "Canceled"
    ]
    metrics[
        "Orders"
    ] = filtered_orders  # replacing the original list with the filtered list

    next_token = metrics.get("NextToken")
    if next_token is not None:
        metrics.pop("NextToken")
        while True:
            # print(f"NextToken found: {next_token}")
            res = orders.get_orders(NextToken=next_token)
            for i in res.payload["Orders"]:
                metrics["Orders"].append(i)
            next_token = res.payload.get("NextToken")
            if next_token is None:
                # print("NextToken not found in this dictionary.")
                break

    else:
        print("NextToken not found in this dictionary.")
    return metrics


if __name__ == "__main__":
    data = orders_report(365)

    print(len(data["Orders"]))

    canceled = [order for order in data["Orders"] if order["OrderStatus"] == "Canceled"]
    print(len(canceled))
