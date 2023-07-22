from langchain import SQLDatabase, SQLDatabaseChain
from langchain.chat_models import ChatOpenAI
from datetime import datetime

import os
from backend.speak import say

# Setting up the api key


OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

db = SQLDatabase.from_uri(
    f"postgresql+psycopg2://postgres:{os.environ['POSTGRES_PASSWORD']}@localhost:5432/amazonseller",
)

# setup llm
llm = ChatOpenAI(
    temperature=0, openai_api_key=OPENAI_API_KEY, model_name="gpt-4"
)
# Get the current date and time
now = datetime.now()

# Format the date to a more human-readable form
formatted_now = now.strftime("%Y-%m-%d")

# Create query instruction
QUERY = """
Todays date is the 22nd of july 2023. 
Given an input question, first create a syntactically correct postgresql query to run against the amazonseller table, then look at the results of the query and return the answer.
use the following columns and rules:
for invetory questions use the inventory table.
When dealing with order table always include 'order_status != Canceled' but this column does not eist in the inventory table only the orders table.A
for sales and revenue questions use the orders table. When it makes sense to do so you have join tables.
when using the product name in the final response try to use the shortest name possible, for example "Sotally Tober" instead of "Sotally Tober Drinking Games for Adults"
afn_total_quantity for queries on invetory or stock in amazon warehouse
afn_inbound_shipped_quantity for queries on inbound shipments or products being sent to amazon
if there is a number higher than 0 in afn_inbound_shipped_quantity, then the product is being sent to amazon and you shopuld return data from afn_inbound_receiving_quantity which is how many are being processed by amazon.
Like wise if the question is asking what is in receiving, you should return afn_inbound_receiving_quantity and afn_inbound_shipped_quantity as the user will want to know what is currently in shipment still to arrive and what is being processed.
your_price is the product cost to the end user and is expressed in GBP pence, so 1000 is £10.00
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Provide your final answer based on the data from the sql query, using a short product name like \"Sotally Tober\" or \"Awkward Family Photos\" "

{question}
"""

# Setup the database chain
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)


def get_prompt():
    print("Type 'exit' to quit")

    while True:
        prompt = input("Enter a prompt: ")

        if prompt.lower() == "exit":
            print("Exiting...")
            break
        else:
            try:
                question = QUERY.format(question=prompt)
                answer = db_chain.run(question)
                say(answer)
            except Exception as e:
                print(e)


get_prompt()
