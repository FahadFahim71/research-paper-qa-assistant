# Research Paper Assistant

An interactive Streamlit application that allows users to upload computer science research papers (PDF) and ask questions grounded in the paper's content using Retrieval-Augmented Generation (RAG).

## Features

- 📄 **PDF Upload**: Upload any computer science research paper in PDF format
- 🔍 **Section Parsing**: Automatically extracts and identifies paper sections (Abstract, Introduction, Methodology, etc.)
- 💬 **Question Answering**: Ask natural language questions about the paper and get accurate, sourced answers
- 📚 **Contextual Answers**: Answers are grounded in the paper's content with citations to relevant sections
- 🎯 **Smart Retrieval**: Uses MMR (Maximal Marginal Relevance) for diverse and relevant passage retrieval
- 📊 **Source Excerpts**: View the exact text excerpts used to generate each answer

## How It Works

1. **Upload Paper**: Users upload a PDF research paper
2. **Section Extraction**: The application parses the PDF to identify logical sections using heading patterns
3. **Vector Store**: Paper sections are embedded and stored in a ChromaDB vector store
4. **Question Processing**: When a question is asked:
   - Relevant sections are retrieved using semantic search
   - A language model generates an answer based solely on the retrieved context
   - Source excerpts are displayed for verification

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/research-paper-assistant.git
   cd research-paper-assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Dependencies

- `streamlit` - Web application framework
- `langchain` - LLM orchestration framework
- `langchain-community` - Community integrations for LangChain
- `langchain-text-splitters` - Text splitting utilities
- `chromadb` - Vector database for embeddings
- `sentence-transformers` - Text embedding models
- `pypdf` - PDF parsing library
- `python-docx` - DOCX handling (for potential future extensions)
- `beautifulsoup4` - HTML/XML parsing
- `requests` - HTTP library

## Usage

1. Launch the application: `streamlit run app.py`
2. Upload a PDF research paper using the file uploader
3. Wait for the paper to be processed (sections will be displayed)
4. Ask questions in the text input box (e.g., "What is the main contribution?", "Which dataset was used?")
5. View the answer and click on "See retrieved excerpts" to verify the sources

## Example Questions

- What is the main contribution of this paper?
- Which dataset was used in the experiments?
- How does this approach compare to prior work?
- What are the limitations mentioned by the authors?
- What future work is suggested?

## How Section Parsing Works

The application uses pattern matching to identify section headings in PDFs:
- Matches common section names (Abstract, Introduction, Methodology, etc.)
- Handles numbered headings (e.g., "1. Introduction", "2.1 Related Work")
- Combines section numbers with titles when split across lines
- Falls back to "Front Matter" for content before the first recognized section

## Limitations

- Works best with structured PDFs containing clear section headings
- May struggle with multi-column layouts or unconventional formatting
- Answer quality depends on the underlying language model's capabilities
- Currently optimized for computer science papers (section keywords reflect CS conventions)

## Future Improvements

- Support for additional document formats (DOCX, PPTX)
- Improved section detection using ML models
- Multi-paper comparison capabilities
- Export functionality for Q&A sessions
- User authentication and session persistence

## Contributing

Feel free to submit issues and pull requests to improve the application!

---
*Built with Streamlit and LangChain*