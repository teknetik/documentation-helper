# set the GOOGLE_APPLICATION_CREDENTIALS env var to the path of the json /key.json
import json
from sp_api.base import (
    Client,
    Marketplaces,
    SellingApiException,
    SellingApiForbiddenException,
    Granularity,
)
from sp_api.api import Orders, Catalog, CatalogItems, Sales
from datetime import date
from apscheduler.schedulers.blocking import BlockingScheduler

import datetime
from keys import CLIENT_CONFIG as credentials


current_time = datetime.datetime.utcnow()
formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
print(formatted_time)


def job():
    print(f"Looking for orders")
    CreatedAfterTime = "2020-01-01T00:00:00Z"
    interval = "2023-01-01T00:00:00-07:00–2023-07-031T00:00:00-07:00"
    sales = Sales(credentials=credentials)
    res = sales.get_order_metrics(
        interval,
        Granularity.TOTAL,
        granularityTimeZone="US/Central",
        marketplace=Marketplaces.GB,
    )
    data = res.get_orders(CreatedAfter=CreatedAfterTime)

    # Convert the ApiResponse object to a dictionary
    data_dict = data.payload
    ai_data = {}
    for order in data_dict["Orders"]:
        print(order["AmazonOrderId"])
        print(order["PurchaseDate"])
        print(order["OrderTotal"]["Amount"])


job()
scheduler = BlockingScheduler()
scheduler.add_job(job, "interval", minutes=1)
scheduler.start()

# job()
