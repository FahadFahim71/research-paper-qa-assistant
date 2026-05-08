import streamlit as st
import tempfile
import os
from paper_parser import extract_sections_from_document
from rag_chain import build_vector_store_from_sections, get_research_qa_chain

st.set_page_config(page_title="Research Paper Assistant", layout="wide")
st.title("📚 Research Paper Assistant")
st.markdown("Upload a computer science paper (PDF, DOCX, PPTX) – ask questions grounded in the paper.")

uploaded_file = st.file_uploader("Choose a document", type=["pdf", "docx", "pptx"])

if uploaded_file is not None:
    # Save uploaded file to a temporary file
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name
    
    with st.spinner("Parsing paper sections..."):
        sections = extract_sections_from_document(tmp_path)
    
    st.success(f"Loaded {len(sections)} sections: {', '.join([s['heading'] for s in sections])}...")
    
    # Build vector store (cached to avoid recomputing on each question)
    @st.cache_resource
    def get_vector_store(sections):
        return build_vector_store_from_sections(sections)
    
    vector_store = get_vector_store(sections)
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 10, "fetch_k": 50, "lambda_mult": 0.3}
    )
    qa_chain = get_research_qa_chain(retriever)
    
    # Question input
    st.subheader("Ask a question about this paper")
    question = st.text_input("Example: 'What is the main contribution?', 'Which dataset was used?', 'How does this compare to prior work?'")
    
    if question:
        with st.spinner("Searching paper and generating answer..."):
            source_docs = retriever.invoke(question)
            answer = qa_chain.invoke(question)
        
        st.markdown("### Answer")
        st.write(answer)
        
        if source_docs:
            with st.expander("📄 See retrieved excerpts"):
                for i, doc in enumerate(source_docs):
                    heading = doc.metadata.get('heading', 'Unknown section')
                    st.markdown(f"**Excerpt {i+1} – {heading}**")
                    st.text(doc.page_content[:600] + "...")
                    st.divider()
    
    # Clean up temporary file
    os.unlink(tmp_path)
else:
    st.info("👈 Upload a document to begin.")