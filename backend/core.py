import os
from typing import Any, Dict, List

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Chroma
import pinecone


persist_directory='db'

def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    print("Generating response")
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    vectordb = Chroma(persist_directory=persist_directory, 
                  embedding_function=embeddings)
    chat = ChatOpenAI(
        model="gpt-4-0613",
        verbose=True,
        temperature=0,
        max_tokens=4000,
    )

    qa = ConversationalRetrievalChain.from_llm(
        llm=chat, retriever=vectordb.as_retriever(), return_source_documents=True
    )
    return qa({"question": query, "chat_history": chat_history})
