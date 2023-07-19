# set the GOOGLE_APPLICATION_CREDENTIALS env var to the path of the json /key.json
import json
from sp_api.base import Client, Marketplaces, SellingApiException, SellingApiForbiddenException, Granularity
from sp_api.api import Orders, Catalog, CatalogItems, Sales
from datetime import date
from apscheduler.schedulers.blocking import BlockingScheduler

import datetime

credentials=dict(
        refresh_token='Atzr|IwEBIL6ZEO0q-2PF40e0ElealFUUy27nDBZPqGWZayozUylTzT1WNI1swVEYTIPj-YN8gFDnoNn666YtXYKK7QDIanttgCDCrrxiSZGtR0DLMcuis741-VfbrzZm4mRqfcLv58Sn4VkKRnPBrT8y_SJ1x75LDlBRbeF9DpnsaqUJy53WcjLEdZ2074Ps1-6GNz2j2A0VNG5zsjSU5eGyBExWI8sZQdtyVkuxBpf1AFBQ9nJ3-8KIAkD5fzZfM2EbOsokhHPhqFZanonXOtB87rpacy7I63rYvEx9izMXpF0dSvX35KadQDb4o94wnat_DsidPEE',
        lwa_app_id='amzn1.application-oa2-client.9ef5bbf03f0f49e9a46960e593fa8168',
        lwa_client_secret='75acfac47c715a4ae70a325c2366bbdb41718dc7c63eb3b772a6802c03cea3dd',
        aws_secret_key='2pfivOSK+9fMR7eK0MJw6bduydXQk7ZqErANgBr6',
        aws_access_key='AKIAT2Z73IF6JZPNVDU3',
        role_arn='arn:aws:iam::263737524604:role/Python-SP-API-Access',
    )


current_time = datetime.datetime.utcnow()
formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
print(formatted_time)

def job():
    print(f"Looking for orders")
    CreatedAfterTime = '2020-01-01T00:00:00Z'
    interval=('2023-01-01T00:00:00-07:00–2023-07-031T00:00:00-07:00')
    sales = Sales(credentials=credentials)
    res = sales.get_order_metrics(interval, Granularity.TOTAL, granularityTimeZone='US/Central', marketplace=Marketplaces.GB)
    data = res.get_orders(CreatedAfter=CreatedAfterTime)

    
    # Convert the ApiResponse object to a dictionary
    data_dict = data.payload
    ai_data = {}
    for order in data_dict['Orders']:
        print(order['AmazonOrderId'])
        print(order['PurchaseDate'])
        print(order['OrderTotal']['Amount'])
    
   
job()
scheduler = BlockingScheduler()
scheduler.add_job(job, 'interval', minutes=1)
scheduler.start()

#job()




