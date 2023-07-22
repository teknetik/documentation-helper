import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from keys import *
from sqlalchemy import create_engine

database_username = DB_USER
database_password = DB_PASSWORD
database_ip       = 'localhost'
database_name     = 'amazonseller'

database_connection = create_engine('postgresql+psycopg2://{0}:{1}@{2}/{3}'.
                                   format(database_username, database_password, 
                                          database_ip, database_name))

query = """
SELECT DATE(purchase_date) as purchase_date, SUM(amount) as daily_sales 
FROM orders 
GROUP BY DATE(purchase_date)
ORDER BY purchase_date;
"""

df = pd.read_sql(query, con=database_connection)

# Ensure purchase_date is in datetime format and set as index
df['purchase_date'] = pd.to_datetime(df['purchase_date'])
df = df.set_index('purchase_date')

# Resample sales_data to monthly frequency
monthly_sales = df['daily_sales'].resample('M').sum()

# Reset index to use seaborn
monthly_sales = monthly_sales.reset_index()

# Plot the sales performance
plt.figure(figsize=(12,8))
sns.barplot(x=monthly_sales['purchase_date'], y=monthly_sales['daily_sales'], color='skyblue')
plt.xticks(rotation=45)
plt.xlabel('Date')
plt.ylabel('Sales Amount')
plt.title('Sales Performance Over Time')
plt.grid(True)
plt.tight_layout()
plt.show()
