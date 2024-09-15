import streamlit as st
import PyPDF2
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Initialize SentenceTransformer model
model_name = "all-MPNet-base-v2"  # Updated model for better accuracy
model = SentenceTransformer(model_name)

def get_embeddings(texts):
    # Get embeddings from SentenceTransformer
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings

# Initialize FAISS index
def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]  # Embedding dimension
    index = faiss.IndexFlatL2(dimension)  # L2 distance metric
    index.add(embeddings)  # Add embeddings to index
    return index

def search_faiss_index(index, query_embedding, k=5):
    distances, indices = index.search(query_embedding, k)
    return indices, distances

# Function to extract text from PDF using PdfReader
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text_data = []
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text() or ""
        text_data.append({
            'page': page_num,
            'text': text
        })
    return text_data

# Function to create text chunks with metadata
def create_text_chunks(text_data, chunk_size=500):
    chunks = []
    for page in text_data:
        page_text = page['text']
        page_number = page['page']
        # Split text into chunks of chunk_size characters
        for i in range(0, len(page_text), chunk_size):
            chunk = page_text[i:i+chunk_size]
            chunks.append({
                'page': page_number,
                'text': chunk
            })
    return chunks

# Streamlit app
st.set_page_config(page_title="Chat with PDF")
st.title("PDF Information Extractor and Search")

# Upload PDF
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    # Extract text from PDF
    with st.spinner("Extracting text from PDF..."):
        text_data = extract_text_from_pdf(uploaded_file)
        text_chunks = create_text_chunks(text_data)
        
        # Display extracted text with page numbers
        st.write("Text extracted from PDF:")
        for page in text_data:
            st.subheader(f"Page {page['page'] + 1}")
            st.text_area("Text", page['text'], height=300)

    # Initialize embeddings and FAISS index
    chunk_texts = [chunk['text'] for chunk in text_chunks]
    embeddings = get_embeddings(chunk_texts)
    index = create_faiss_index(embeddings)

    # Search for information
    query = st.text_input("Search for information")

    if query:
        with st.spinner("Searching for information..."):
            query_embedding = get_embeddings([query])
            indices, distances = search_faiss_index(index, query_embedding)

            st.write("Search Results:")
            for idx, dist in zip(indices[0], distances[0]):
                chunk = text_chunks[idx]
                page_num = chunk['page']
                st.write(f"**Page {page_num + 1}**")
                st.write(f"**Text Chunk:** {chunk['text'][:500]}...")  # Displaying a snippet
                st.write(f"**Distance:** {dist:.4f}")

