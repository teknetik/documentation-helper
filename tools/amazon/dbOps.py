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

def create_inventory():
    # Define table
    inventory = Table(
        "inventory",
        metadata,
        Column("sku", String),
        Column("fnsku", String),
        Column("asin", String),
        Column("product_name", String),
        Column("condition", String),
        Column("your_price", Integer),
        Column("mfn_listing_exists", Boolean),
        Column("mfn_fulfillable_quantity", Integer),
        Column("afn_listing_exists", Boolean),
        Column("afn_warehouse_quantity", Integer),
        Column("afn_fulfillable_quantity", Integer),
        Column("afn_unsellable_quantity", Integer),
        Column("afn_reserved_quantity", Integer),
        Column("afn_total_quantity", Integer),
        Column("afn_inbound_working_quantity", Integer),
        Column("afn_inbound_shipped_quantity", Integer),
        Column("afn_inbound_receiving_quantity", Integer),
        Column("afn_researching_quantity", Integer),
        Column("afn_reserved_future_supply", Integer),
        Column("afn_future_supply_buyable", Integer),
        Column("per_unit_volume", Float),
        Column("last_updated", DateTime),
    )

    # Create table if not exists
    metadata.create_all(engine, checkfirst=True)

    return None

def create_orders():
    orders_table = Table(
    'orders', metadata,
        Column('buyer_email', String(100)),
        Column('amazon_order_id', String(50), primary_key=True),
        Column('earliest_ship_date', DateTime),
        Column('sales_channel', String(50)),
        Column('order_status', String(20)),
        Column('number_of_items_shipped', Integer),
        Column('order_type', String(20)),
        Column('is_premium_order', Boolean),
        Column('is_prime', Boolean),
        Column('fulfillment_channel', String(20)),
        Column('number_of_items_unshipped', Integer),
        Column('has_regulated_items', Boolean),
        Column('is_replacement_order', Boolean),
        Column('is_sold_by_ab', Boolean),
        Column('latest_ship_date', DateTime),
        Column('ship_service_level', String(20)),
        Column('is_ispu', Boolean),
        Column('marketplace_id', String(20)),
        Column('purchase_date', DateTime),
        Column('shipping_state_or_region', String(50)),
        Column('shipping_postal_code', String(20)),
        Column('shipping_city', String(50)),
        Column('shipping_country_code', String(10)),
        Column('is_access_point_order', Boolean),
        Column('seller_order_id', String(50)),
        Column('payment_method', String(20)),
        Column('is_business_order', Boolean),
        Column('currency_code', String(10)),
        Column('amount', Float),
        Column('payment_method_details', String(20)),
        Column('is_global_express_enabled', Boolean),
        Column('last_update_date', DateTime),
        Column('shipment_service_level_category', String(20)),
    )

    metadata.create_all(engine, checkfirst=True)
    return None


if __name__ == "__main__":
    # create_inventory()
    create_orders()