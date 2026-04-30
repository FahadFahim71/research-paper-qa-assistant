import os
import shutil

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough, RunnableParallel, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

def build_vector_store_from_sections(sections):
    """
    sections: list of dict [{'heading': str, 'content': str}]
    Returns a Chroma vector store ready for retrieval.
    """
    # Skip noisy sections that are unlikely to help answer questions.
    excluded_headings = {"Front Matter", "References"}

    docs = []
    for sec in sections:
        if sec['heading'] in excluded_headings:
            continue
        enriched_content = f"[SECTION: {sec['heading']}] {sec['content']}"
        doc = Document(
            page_content=enriched_content,
            metadata={'heading': sec['heading']}
        )
        docs.append(doc)
    
    # Split long sections into smaller overlapping chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = splitter.split_documents(docs)
    print(f"Created {len(chunks)} chunks from {len(sections)} sections")
    
    # Create embeddings (local, free)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Remove any stale persisted Chroma DB before rebuilding.
    persist_dir = "./chroma_db"
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)

    vector_store = Chroma.from_documents(chunks, embeddings, persist_directory=persist_dir)
    return vector_store

def get_research_qa_chain(retriever, model_name="llama3.2:3b"):
    llm = Ollama(model=model_name, temperature=0.1)
    
    # Create the prompt template
    system_prompt = (
        "You are a research paper assistant. Use the following pieces of retrieved context "
        "to answer the question. If you don't know the answer, say you don't know.\n\n"
        "RETRIEVED CONTEXT:\n{context}\n\nQUESTION: {question}"
    )
    
    prompt = ChatPromptTemplate.from_template(system_prompt)
    
    # Format retrieved documents into a string
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    # Simple explicit chain: retrieve docs, format them, build prompt, call LLM
    def rag_invoke(question):
        # Step 1: Retrieve
        docs = retriever.invoke(question)
        context = format_docs(docs)
        
        # Step 2: Format prompt with context and question
        formatted_prompt = system_prompt.format(context=context, question=question)
        
        # Step 3: Call LLM
        response = llm.invoke(formatted_prompt)
        return response
    
    return RunnableLambda(rag_invoke)