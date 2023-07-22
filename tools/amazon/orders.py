import json
from sp_api.api import Orders
from sp_api.base import Marketplaces, ReportType, ProcessingStatus, Granularity
from keys import *
from datetime import datetime, timedelta
from dateutil.tz import tzlocal

from sqlalchemy import (
        create_engine,
        MetaData,
        Table,
        Column,
        Integer,
        String,
        Boolean,
        Float,
        DateTime,
    )
from sqlalchemy.dialects.postgresql import insert

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

def upsert_orders(data):
    print("Attempting to upsert orders")   

    from keys import DB_USER, DB_PASSWORD

    # Define your PostgreSQL connection parameters
    db_user = DB_USER
    db_password = DB_PASSWORD
    db_host = "localhost"
    db_port = "5432"
    db_name = "amazonseller"  # Replace with your database name

    # Create the SQLAlchemy engine
    engine = create_engine(
        f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
    metadata = MetaData()

    # Define the orders_table
    orders_table = Table('orders', metadata, autoload_with=engine)

    for order in data['Orders']:
        # Flatten the order data
        if 'ShippingAddress' in order:
            state_or_region = order['ShippingAddress'].get('StateOrRegion', None)
            shipping_postal_code = order['ShippingAddress'].get('PostalCode', None)
            shipping_city = order['ShippingAddress'].get('City', None)
            shipping_country_code = order['ShippingAddress'].get('CountryCode', None)
        else:
            state_or_region = None
        if 'OrderTotal' in order:
            currency_code = order['OrderTotal'].get('currency_code', None)
            amount = order['OrderTotal'].get('amount', 0)
        else:
            OrderTotal = None
        order_data = {
            'buyer_email': order['BuyerInfo'].get('BuyerEmail', None),
            'amazon_order_id': order['AmazonOrderId'],
            'earliest_ship_date': datetime.fromisoformat(order['EarliestShipDate'].replace("Z", "+00:00")),
            'sales_channel': order['SalesChannel'],
            'order_status': order['OrderStatus'],
            'number_of_items_shipped': order['NumberOfItemsShipped'],
            'order_type': order['OrderType'],
            'is_premium_order': True if order['IsPremiumOrder'] == 'true' else False,
            'is_prime': True if order['IsPrime'] == 'true' else False,
            'has_regulated_items': True if order['HasRegulatedItems'] == 'true' else False,
            'is_replacement_order': True if order['IsReplacementOrder'] == 'true' else False,
            'is_sold_by_ab': True if order['IsSoldByAB'] == 'true' else False,
            'is_ispu': True if order['IsISPU'] == 'true' else False,
            'is_access_point_order': True if order['IsAccessPointOrder'] == 'true' else False,
            'is_business_order': True if order['IsBusinessOrder'] == 'true' else False,
            'is_global_express_enabled': True if order['IsGlobalExpressEnabled'] == 'true' else False,
            'fulfillment_channel': order['FulfillmentChannel'],
            'number_of_items_unshipped': order['NumberOfItemsUnshipped'],
            'latest_ship_date': datetime.fromisoformat(order['LatestShipDate'].replace("Z", "+00:00")),
            'ship_service_level': order['ShipServiceLevel'],
            'marketplace_id': order['MarketplaceId'],
            'purchase_date': datetime.fromisoformat(order['PurchaseDate'].replace("Z", "+00:00")),
            'shipping_state_or_region': state_or_region,
            'shipping_postal_code': shipping_postal_code,
            'shipping_city': shipping_city,
            'shipping_country_code': shipping_country_code,
            'seller_order_id': order['SellerOrderId'],
            'payment_method': amount,
            'currency_code': currency_code,
            'amount': float(amount),
            'payment_method_details': order['PaymentMethodDetails'][0] if order['PaymentMethodDetails'] else None,
            'last_update_date': datetime.fromisoformat(order['LastUpdateDate'].replace("Z", "+00:00")),
            'shipment_service_level_category': order['ShipmentServiceLevelCategory']
        }

        # Create insert statement
        stmt = insert(orders_table).values(**order_data)

        # Specify the action to perform if a conflict occurs
        stmt = stmt.on_conflict_do_update(index_elements=['amazon_order_id'],
                                          set_=order_data
                                          )
        
        # Open a session
        with engine.begin() as connection:
            # Try to insert the data
            try:
                connection.execute(stmt)
            # If a conflict occurs
            except Exception as e:
                print(e)
                # Update the existing row
                connection.execute(
                    orders_table.update()
                    .where(orders_table.c.amazon_order_id == order_data['amazon_order_id'])
                    .values(**order_data)
                )

        # Execute the statement
        with engine.connect() as connection:
            connection.execute(stmt)

    return None

def write_data_to_file(data):
    # Define your file path
    file_path = "/opt/documentation-helper/tools/amazon/responses/orders.json"

    # Open the file in write mode
    with open(file_path, 'w') as json_file:
        # Use the json.dump method to write the data to the file
        json.dump(data, json_file)
    return None

def read_data_from_file():
    # Define your file path
    file_path = "/opt/documentation-helper/tools/amazon/responses/orders.json"

    # Open the file in read mode
    with open(file_path, 'r') as json_file:
        # Use the json.load method to read the data from the file
        data = json.load(json_file)
    return data

if __name__ == "__main__":
    
    dev_mode=True
    if dev_mode:
        print("Running in Dev Mode")
        data = read_data_from_file()
    else:
        print("Running in Live Mode")   
        data = orders_report(365)
        write_data_to_file(data)

    orders = len(data['Orders'])
    canceled_orders = len([order for order in data["Orders"] if order["OrderStatus"] == "Canceled"])
    total_orders = orders - canceled_orders

    print(f"Orders: {orders}")
    print(f"Canceled Orders: {canceled_orders}")
    print(f"Total Orders: {total_orders}")
    upsert_orders(data)