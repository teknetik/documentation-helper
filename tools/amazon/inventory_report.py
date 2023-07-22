import csv
import json
import time
import pandas as pd
import requests
from sp_api.api import Reports, Sales
from sp_api.base import Marketplaces, ReportType, ProcessingStatus, Granularity
from cross_platform.os_detect import base_path
from keys import *
from sqlalchemy import create_engine
import os 
base_path = base_path()

engine = create_engine(f"postgresql+psycopg2://postgres:{os.environ['POSTGRES_PASSWORD']}@localhost:5432/amazonseller")


CLIENT_CONFIG = {
    "lwa_app_id": LWA_APP_ID,
    "lwa_client_secret": LWA_CLIENT_SECRET,
    "aws_secret_key": AWS_SECRET_KEY,
    "aws_access_key": AWS_ACCESS_KEY,
    "role_arn": ROLE_ARN,
    "refresh_token": REFRESH_TOKEN,
}


def inventory_report():
    report_type = ReportType.GET_FBA_MYI_ALL_INVENTORY_DATA
    res = Reports(credentials=CLIENT_CONFIG, marketplace=Marketplaces.GB)
    data = res.create_report(reportType=report_type)
    report = data.payload
    print(report)
    report_id = report["reportId"]
    report_id = "66494019560"
    res = Reports(credentials=CLIENT_CONFIG, marketplace=Marketplaces.GB)
    data = res.get_report(report_id)

    report_data = ""

    while data.payload.get("processingStatus") not in [
        ProcessingStatus.DONE,
        ProcessingStatus.FATAL,
        ProcessingStatus.CANCELLED,
    ]:
        print(data.payload)
        print("Sleeping...")
        time.sleep(2)
        data = res.get_report(report_id)

    if data.payload.get("processingStatus") in [
        ProcessingStatus.FATAL,
        ProcessingStatus.CANCELLED,
    ]:
        print("Report failed!")
        report_data = data.payload
    else:
        print("Success:")
        print(data.payload)
        report_data = res.get_report_document(data.payload["reportDocumentId"])
        print("Document:")
        print(report_data.payload)

    report_url = report_data.payload.get("url")
    print(report_url)

    res = requests.get(report_url)
    decoded_content = res.content.decode("cp1252")
    reader = csv.DictReader(decoded_content.splitlines(), delimiter="\t")

    data_list = []
    for row in reader:
        data = {
            "sku": row["sku"],
            "fnsku": row["fnsku"],
            "asin": row["asin"],
            "product_name": row["product-name"],
            "condition": row["condition"],
            "your_price": int(float(row["your-price"] or "0") * 100),
            "mfn_listing_exists": row["mfn-listing-exists"] == "Yes",
            "mfn_fulfillable_quantity": row["mfn-fulfillable-quantity"] or None,
            "afn_listing_exists": row["afn-listing-exists"] == "Yes",
            "afn_warehouse_quantity": row["afn-warehouse-quantity"],
            "afn_fulfillable_quantity": row["afn-fulfillable-quantity"],
            "afn_unsellable_quantity": row["afn-unsellable-quantity"],
            "afn_reserved_quantity": row["afn-reserved-quantity"],
            "afn_total_quantity": row["afn-total-quantity"],
            "afn_inbound_working_quantity": row["afn-inbound-working-quantity"],
            "afn_inbound_shipped_quantity": row["afn-inbound-shipped-quantity"],
            "afn_inbound_receiving_quantity": row["afn-inbound-receiving-quantity"],
            "afn_researching_quantity": row["afn-researching-quantity"],
            "afn_reserved_future_supply": row["afn-reserved-future-supply"],
            "afn_future_supply_buyable": row["afn-future-supply-buyable"],
            "per_unit_volume": float(row["per-unit-volume"])
            if row["per-unit-volume"]
            else None,
        }
        data_list.append(data)
    print(data_list)
    with open(f"{base_path}/documentation-helper/tools/amazon/responses/data.json", "w") as out:
        json.dump(data_list, out)

    df = pd.DataFrame([data], index=[0])
    df.to_sql('inventory', engine, if_exists='append', index=False)
    print(df)
    return df


if __name__ == "__main__":
    inventory_report()
