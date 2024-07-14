import os
import logging
from typing import List, Dict
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RAGSystem:
    def __init__(self):
        logger.info("Initializing RAG System")
        self.embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
        self.vector_store = None
        self.retriever = None
        self.llm = OpenAI(openai_api_key=Config.OPENAI_API_KEY)
        self.qa_chain = None

    def load_documents(self, documents: List[Dict[str, str]]):
        logger.info(f"Loading {len(documents)} documents into RAG system")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=150,
            length_function=len,
            add_start_index=True,
        )
        texts = []
        for doc in documents:
            split_texts = text_splitter.split_text(doc['content'])
            texts.extend([(text, {"source": doc['filename'], "start_index": i * 300}) for i, text in enumerate(split_texts)])
        
        logger.info(f"Split documents into {len(texts)} text chunks")

        self.vector_store = Chroma.from_texts([text for text, metadata in texts], 
                                              self.embeddings, 
                                              metadatas=[metadata for text, metadata in texts],
                                              persist_directory="./chroma_db")
        
        logger.info(f"Created vector store with {self.vector_store._collection.count()} elements")
        
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 5})

        template = """Use the following pieces of context to answer the question at the end. 
        If you don't know the answer, just say that you don't know, don't try to make up an answer.
        Always mention the source of the information you're using to answer the question.

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
        logger.info("RAG system fully initialized and ready for queries")

    async def query(self, question: str) -> str:
        if not self.qa_chain:
            logger.warning("Attempted to query RAG system before initialization")
            return "The RAG system hasn't been initialized with documents yet."
        
        try:
            logger.info(f"Processing RAG query: {question}")
            result = self.qa_chain.invoke(question)
            logger.info("RAG query processed successfully")
            return result
        except Exception as e:
            logger.error(f"Error in RAG query: {e}", exc_info=True)
            return "An error occurred while processing your query."

rag_system = RAGSystem()

def initialize_rag(documents: List[Dict[str, str]]):
    logger.info("Starting RAG system initialization")
    rag_system.load_documents(documents)
    logger.info("RAG system initialization completed")

async def rag_query(question: str) -> str:
    logger.info(f"Received RAG query: {question}")
    response = await rag_system.query(question)
    logger.info("RAG query response generated")
    return response