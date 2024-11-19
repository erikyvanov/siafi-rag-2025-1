from langchain_community.document_loaders import PyPDFLoader

from langchain_chroma import Chroma # base de datos de vectores
from langchain_ollama import OllamaEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter


from langchain_core.documents import Document

import uuid


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=180,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
    separators=['\n', '.', '\n\n']
)

embeddings_generator = OllamaEmbeddings(
    model='mxbai-embed-large'
)

vector_store = Chroma(
    collection_name='pokemon',
    embedding_function=embeddings_generator,
    persist_directory='./pokemon_emb_db'
)

pdf_loader = PyPDFLoader('./curiosidades.pdf')
pages = pdf_loader.load()


split_documents = text_splitter.split_documents(pages)

for chunk in split_documents:
    chunk.id = str(uuid.uuid4())
    chunk.metadata['source'] = 'https://www.wikidex.net/wiki'
    chunk.metadata['is_curiosity'] = True


vector_store.add_documents(split_documents)
print('Emneddings guardados')
