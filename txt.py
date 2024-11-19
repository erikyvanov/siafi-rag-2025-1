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

txt_document_path = './mega.txt'
txt_text = ''

with open(txt_document_path, 'r') as file:
    txt_text = file.read()

result = text_splitter.split_text(txt_text)
print(len(result))

for chunk in result:
    document = Document(
        page_content=chunk,
        id=str(uuid.uuid4()),
        metadata={
            'source': 'https://www.wikidex.net/wiki/Megaevoluci%C3%B3n',
            'is_info': True,
        }
    )

    vector_store.add_documents([document])