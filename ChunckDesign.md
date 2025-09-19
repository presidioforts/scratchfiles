from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

# 1. Load textbook (sample file)
loader = TextLoader("grade6_english.txt")
docs = loader.load()

# 2. Chunk into 300-500 tokens
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.split_documents(docs)

# 3. Embedding model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

# 4. Store in ChromaDB
db = Chroma.from_documents(chunks, embedding=embeddings, persist_directory="chroma_db")

# 5. Retriever
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# 6. LLM (teacher brain)
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 7. RetrievalQA chain
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# 8. Ask a sample question
print(qa.run("Explain the story of 'The Friendly Mongoose' for a 6th grader."))
