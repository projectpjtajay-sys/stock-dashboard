import os
from dotenv import load_dotenv
load_dotenv()

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage

def build_or_load_index(persist_dir="storage"):
    if os.path.exists(persist_dir):
        print("Loading existing index...")
        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        return load_index_from_storage(storage_context)
    else:
        print("Building index from documents...")
        documents = SimpleDirectoryReader("documents").load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir)
        return index
    