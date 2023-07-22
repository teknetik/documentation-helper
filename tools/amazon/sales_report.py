import json
from sp_api.api import Reports, Sales
from sp_api.base import Marketplaces, ReportType, ProcessingStatus, Granularity
from keys import *
import datetime
from dateutil.tz import tzlocal

CLIENT_CONFIG = {
    "lwa_app_id": LWA_APP_ID,
    "lwa_client_secret": LWA_CLIENT_SECRET,
    "aws_secret_key": AWS_SECRET_KEY,
    "aws_access_key": AWS_ACCESS_KEY,
    "role_arn": ROLE_ARN,
    "refresh_token": REFRESH_TOKEN,
}


def format_date(dt):
    s = dt.strftime("%Y-%m-%dT%H:%M:%S%z")
    return s[:-2] + ":" + s[-2:]


def sales_report(period: int):
    f = open("/opt/documentation-helper/tools/amazon/responses/data.json")
    data = json.load(f)
    asins = [x["asin"] for x in data][:5]

    marketplaces = dict(GB=Marketplaces.GB)
    data = []

    # Get current timezone
    local_tz = tzlocal()

    # Calculate the start and end dates based on the period.
    end_time = datetime.datetime.now(local_tz)
    start_time = end_time - datetime.timedelta(days=period)

    # Format the start and end dates as strings.
    end_time_str = format_date(end_time)
    start_time_str = format_date(start_time)

    for asin in asins:
        for country, marketplace_id in marketplaces.items():
            sales = Sales(credentials=CLIENT_CONFIG, marketplace=marketplace_id)
            res = sales.get_order_metrics(
                interval=(start_time_str, end_time_str),
                # interval=('2023-07-01T00:00:00+01:00', '2023-07-22T00:00:00+01:00'),
                granularity=Granularity.TOTAL,
                asin=asin,
            )
            metrics = res.payload[0]
            print(metrics)
            data.append(
                {
                    "unit_count": metrics["unitCount"],
                    "order_item_count": metrics["orderItemCount"],
                    "order_count": metrics["orderCount"],
                    "country": country,
                    "asin": asin,
                }
            )

    return data


if __name__ == "__main__":
    data = sales_report(7)
    print(data)
