# Import things that are needed generically
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool, StructuredTool, Tool, tool
import os
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
        text
    )


OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

def execSQL(sql):
        engine = create_engine(
            f"postgresql+psycopg2://postgres:{os.environ['POSTGRES_PASSWORD']}@localhost:5432/amazonseller",
        )
        with engine.connect() as connection:
            result = connection.execute(text(sql))
            data = result.fetchall()
        return data


@tool
def inventory_fetch(query: str):
    """Fetches inventory data from the database"""
    sql = f"""
    SELECT * FROM inventory
    """
    data = execSQL(sql)
    return data

tools = [inventory_fetch]
llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo")
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

agent.run(
    "What is our current inventory?"
)