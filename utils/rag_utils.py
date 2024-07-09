import os
from typing import List, Dict
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from config import Config

class RAGSystem:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
        self.vector_store = None
        self.retriever = None
        self.llm = OpenAI(openai_api_key=Config.OPENAI_API_KEY)
        self.qa_chain = None

    def load_documents(self, documents: List[Dict[str, str]]):
        text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
        texts = []
        for doc in documents:
            split_texts = text_splitter.split_text(doc['content'])
            texts.extend([(text, {"source": doc['filename']}) for text in split_texts])

        self.vector_store = Chroma.from_texts([text for text, metadata in texts], 
                                              self.embeddings, 
                                              metadatas=[metadata for text, metadata in texts],
                                              persist_directory="./chroma_db")
        
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 5})

        template = """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer.

        {context}

        Question: {question}
        Answer:"""
        prompt = PromptTemplate.from_template(template)

        self.qa_chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

    async def query(self, question: str) -> str:
        if not self.qa_chain:
            return "The RAG system hasn't been initialized with documents yet."
        
        try:
            result = self.qa_chain.invoke(question)
            return result
        except Exception as e:
            print(f"Error in RAG query: {e}")
            return "An error occurred while processing your query."

rag_system = RAGSystem()

def initialize_rag(documents: List[Dict[str, str]]):
    rag_system.load_documents(documents)

async def rag_query(question: str) -> str:
    return await rag_system.query(question)