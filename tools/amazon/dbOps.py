from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, Float, DateTime
from datetime import datetime
import pandas as pd
from keys import DB_USER, DB_PASSWORD
# Define your PostgreSQL connection parameters
db_user = DB_USER
db_password = DB_PASSWORD
db_host = 'localhost'
db_port = '5432'
db_name = 'amazonseller'  # Replace with your database name

# Create the SQLAlchemy engine
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
metadata = MetaData()

# Define table
inventory = Table('inventory', metadata,
                  Column('sku', String),
                  Column('fnsku', String),
                  Column('asin', String),
                  Column('product_name', String),
                  Column('condition', String),
                  Column('your_price', Integer),
                  Column('mfn_listing_exists', Boolean),
                  Column('mfn_fulfillable_quantity', Integer),
                  Column('afn_listing_exists', Boolean),
                  Column('afn_warehouse_quantity', Integer),
                  Column('afn_fulfillable_quantity', Integer),
                  Column('afn_unsellable_quantity', Integer),
                  Column('afn_reserved_quantity', Integer),
                  Column('afn_total_quantity', Integer),
                  Column('afn_inbound_working_quantity', Integer),
                  Column('afn_inbound_shipped_quantity', Integer),
                  Column('afn_inbound_receiving_quantity', Integer),
                  Column('afn_researching_quantity', Integer),
                  Column('afn_reserved_future_supply', Integer),
                  Column('afn_future_supply_buyable', Integer),
                  Column('per_unit_volume', Float),
                  Column('last_updated', DateTime)
                  )

# Create table if not exists
metadata.create_all(engine, checkfirst=True)

# The data
data = [{'sku': 'HO-NTMR-XI7C', 'fnsku': 'X001Q5REZZ', 'asin': 'B07M5YWVVB', 
         'product_name': 'Sotally Tober Drinking Games for Adults - Outrageously Fun Adult Party Card Game', 
         'condition': 'New', 'your_price': 1499, 'mfn_listing_exists': False, 'mfn_fulfillable_quantity': None, 
         'afn_listing_exists': True, 'afn_warehouse_quantity': 112, 'afn_fulfillable_quantity': 112, 
         'afn_unsellable_quantity': 0, 'afn_reserved_quantity': 0, 'afn_total_quantity': 112, 
         'afn_inbound_working_quantity': 0, 'afn_inbound_shipped_quantity': 0, 'afn_inbound_receiving_quantity': 0, 
         'afn_researching_quantity': 0, 'afn_reserved_future_supply': 0, 'afn_future_supply_buyable': 0, 
         'per_unit_volume': 371.17, 'last_updated': datetime.now()}]

# Convert list of dict to dataframe
df = pd.DataFrame(data)

# Write data to PostgreSQL using DataFrame's to_sql() method
df.to_sql('inventory', engine, if_exists='append', index=False)
