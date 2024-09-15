# PDF Information Extractor and Search 📄  
Click here for the app: 

This Streamlit application allows users to upload a PDF, extract its text, and search for specific information within it using FAISS and Sentence Transformers for efficient similarity search.

## Features:
- **Home 🏠**: Users can upload a PDF file and view the extracted text.
- **Text Extraction 📄**: Extracts text from the uploaded PDF and displays it page by page.
- **Search 🔍**: Allows users to enter a query, and the app will return relevant text chunks from the PDF along with their distances from the query, indicating similarity.

## Code Explanation:

### Page Configuration:
- **Title Setting**: Sets the web page title to "PDF Information Extractor and Search."

### Model Initialization:
- **Sentence Transformer Model**: The app uses the `all-MPNet-base-v2` model for generating text embeddings, providing high accuracy in text similarity tasks.

### PDF Text Extraction:
- **Extracting PDF Content**: The `extract_text_from_pdf` function reads and extracts text from the uploaded PDF file using `PyPDF2`. It iterates over each page and captures the content.

### Text Chunking:
- **Create Text Chunks**: The `create_text_chunks` function splits the extracted text into smaller, more manageable chunks (default: 500 characters), helping with the search process.

### FAISS Indexing:
- **Creating a FAISS Index**: The extracted text chunks are converted into embeddings using Sentence Transformers, and a FAISS index is built to allow efficient similarity search using L2 distance.

### Search Function:
- **Search for Information**: Users can input a query, and the FAISS index will return the top 5 most relevant text chunks, ranked by similarity distance. The relevant page number and chunk of text are displayed to the user.

## Streamlit Application:

- **Title and File Upload**: The app displays a title and allows users to upload a PDF file.
- **Text Extraction Display**: After extracting the text from the PDF, it is displayed page by page for easy viewing.
- **Search Functionality**: Users can input a query, and the app returns relevant text chunks, displaying both the page number and a snippet of the text for context.

## Trained Model:
- **Sentence Transformer**: The application uses the `all-MPNet-base-v2` model from the `sentence-transformers` library, which is pre-trained for efficient semantic search tasks.

## Usage:

- **Home 🏠**: Upload a PDF file, and the app will extract and display the text for review.
- **Search 🔍**: Enter a search query, and the app will find and display the most relevant text chunks from the PDF based on semantic similarity.
- **Text Results 📑**: View the extracted text with page numbers and the corresponding similarity score from the search query.

## Requirements:
- **Streamlit**
- **PyPDF2**
- **sentence-transformers**
- **FAISS**
- **NumPy**

Make sure to install all required packages before running the app. 📦
