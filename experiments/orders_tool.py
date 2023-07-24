# Import things that are needed generically
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, StructuredTool, Tool, tool
import os
from langchain import SQLDatabase, SQLDatabaseChain
import json

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo")
db = SQLDatabase.from_uri(
    f"postgresql+psycopg2://postgres:{os.environ['POSTGRES_PASSWORD']}@localhost:5432/amazonseller",
)
db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)



tools = [Tool(
        name="InventoryDB",
        func=db_chain.run,
        description="""
        useful for when you need to answer questions about sales, stock and inventory or current products and pricing. 
        There is an inventory table and an orders table.
        The orders table should be used for revenue and sales questions.
        Input should be in the form of a question containing full context"""
    )]

agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)

agent.run(
    "how much in GBP did we sell in july"
)