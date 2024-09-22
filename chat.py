import streamlit as st
from streamlit_option_menu import option_menu
import PyPDF2
import networkx as nx
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Initialize SentenceTransformer model
model_name = "all-MiniLM-L12-v2"
model = SentenceTransformer(model_name)

def get_embeddings(texts):
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings

def create_faiss_index(embeddings):
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def search_faiss_index(index, query_embedding, k=5):
    distances, indices = index.search(query_embedding, k)
    return indices, distances

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text_data = []
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text = page.extract_text() or ""
        text_data.append({'page': page_num, 'text': text})
    return text_data

def create_text_chunks(text_data, chunk_size=500):
    chunks = []
    for page in text_data:
        page_text = page['text']
        page_number = page['page']
        for i in range(0, len(page_text), chunk_size):
            chunk = page_text[i:i + chunk_size]
            chunks.append({'page': page_number, 'text': chunk})
    return chunks

def extract_topics_and_subtopics(pdf_reader):
    topic_subtopic_mapping = {}
    
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        lines = page.extract_text().splitlines()

        if not lines:
            continue
        
        current_topic = lines[0].strip()
        topic_subtopic_mapping[current_topic] = {"subtopics": [], "paragraph": ""}
        
        for line in lines[1:]:
            line = line.strip()
            if line and (line.startswith('•') or line.startswith('-') or line.startswith('*')):
                subtopic = line[1:].strip()
                if len(topic_subtopic_mapping[current_topic]["subtopics"]) < len(pdf_reader.pages):
                    topic_subtopic_mapping[current_topic]["subtopics"].append(subtopic)
            elif current_topic and not line.startswith('•') and not line.startswith('-') and not line.startswith('*'):
                topic_subtopic_mapping[current_topic]["paragraph"] += line + " "

    return topic_subtopic_mapping

def create_network_graph(topic_subtopic_mapping):
    G = nx.DiGraph()
    for topic, content in topic_subtopic_mapping.items():
        G.add_node(topic, subset='topic')
        for subtopic in content["subtopics"]:
            G.add_node(subtopic, subset=topic)
            G.add_edge(topic, subtopic)
    return G

# Streamlit app UI
st.set_page_config("PDF Content Analyzer")

# Option menu
with st.sidebar:
    selected = option_menu("Menu", 
                           ["PDF Information Extractor and Search", "PDF to Flowchart Generator"],
                           icons=['file-earmark-text', 'diagram-3'],
                           menu_icon="cast", default_index=0)

if selected == "PDF Information Extractor and Search":
    st.header("PDF Information Extractor and Search")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file:
        with st.spinner("Extracting text from PDF..."):
            text_data = extract_text_from_pdf(uploaded_file)
            text_chunks = create_text_chunks(text_data)

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
                    st.write(f"**Text Chunk:** {chunk['text'][:500]}...")  
                    st.write(f"**Distance:** {dist:.4f}")

        # Display extracted text with page numbers
        st.write("Text extracted from PDF:")
        for page in text_data:
            st.subheader(f"Page {page['page'] + 1}")
            st.text_area("Text", page['text'], height=300)

elif selected == "PDF to Flowchart Generator":
    st.header("PDF to Flowchart Generator")

    st.markdown(
        "<div style='padding: 10px; border-radius: 5px;'>"
        "<strong>Note:</strong> Please do not upload research papers or handwritten notes, as they may not generate a proper graph."
        "</div>", unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file is not None:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        topic_subtopic_mapping = extract_topics_and_subtopics(pdf_reader)
        G = create_network_graph(topic_subtopic_mapping)

        plt.figure(figsize=(10, 6))
        pos = nx.multipartite_layout(G, subset_key='subset')
        nx.draw(G, pos, with_labels=True, arrows=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold')
        plt.title("Topic and Subtopic Network")
        st.pyplot(plt)

        st.subheader("Extracted Topics and Subtopics")
        for topic, content in topic_subtopic_mapping.items():
            st.markdown(f"<div style='color: #007bff; font-weight: bold;'>{topic}</div>", unsafe_allow_html=True)
            for subtopic in content["subtopics"]:
                st.write(f"- {subtopic}")
            st.write(f"**Paragraph:** {content['paragraph'][:200]}...")

