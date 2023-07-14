import os

from langchain.document_loaders import ReadTheDocsLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders import UnstructuredHTMLLoader
import pinecone

pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENVIRONMENT_REGION"],
)
INDEX_NAME = "langchain-doc"

import os

def get_files_in_dir(directory):
    file_list = []

    # Walk through directory
    for dirpath, dirnames, filenames in os.walk(directory):
        for file in filenames:
            # Check if the file is .html
            if file.endswith('.html'):
                file_list.append(os.path.join(dirpath, file))
            #file_list.append(os.path.join(dirpath, file))
    return file_list


def ingest_docs(file):
    #loader = ReadTheDocsLoader(path="/home/teknetik/websites/docs.kong/docs.konghq.com/index.html")
    loader =  UnstructuredHTMLLoader(file)
    raw_documents = loader.load()
    print(f"loaded {len(raw_documents)} documents")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", " ", ""]
    )
    documents = text_splitter.split_documents(raw_documents)
    for doc in documents:
        new_url = doc.metadata["source"]
        new_url = new_url.replace("/home/teknetik/websites/docs.kong/", "https:/")
        doc.metadata.update({"source": new_url})

    embeddings = OpenAIEmbeddings()
    print(f"Going to add {len(documents)} to Pinecone")
    Pinecone.from_documents(documents, embeddings, index_name=INDEX_NAME)
    print("****Loading to vectorestore done ***")


if __name__ == "__main__":
    ###
    # Change the directory, only uploading one version at a time
    #
    # Ensure to update the meta data with the product and version or other applicable metadata
    #
    ###
    directory_to_scan = "/home/teknetik/websites/docs.kong/docs.konghq.com/mesh/latest/"  # Change this to your target directory
    file_list = get_files_in_dir(directory_to_scan)
    file_num = len(file_list)
    i =1
    for file in file_list:
        print(file + " " + str(i) + " of " + str(file_num))
        ingest_docs(file)
        i += 1
