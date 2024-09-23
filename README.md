# PDF Content Analyzer
**Click here for the app:** [Chat With PDF Application](https://chat-with-pdf-abe.streamlit.app/)


This Streamlit application combines two powerful features:
- **PDF Information Extractor and Search**: Upload a PDF, extract its text, and search for specific information using FAISS and Sentence Transformers for efficient similarity search.
- **PDF Flowchart Generator**: Extracts the structure of topics and subtopics from a PDF and visualizes them in a flowchart, offering a clear hierarchical overview of the document's content.

## Features:

### **Home 🏠**
- Users can upload a PDF file and view the extracted text page by page. Both the **Information Extractor and Search** and the **Flowchart Generator** are available.


### **PDF Information Extractor and Search 📄🔍**
- **Text Extraction**: Extracts text from the uploaded PDF, breaking it down into manageable chunks. The app displays the text along with the respective page numbers.
- **Sentence Embeddings**: Converts text chunks into vector embeddings using the pre-trained SentenceTransformer model.
- **FAISS Indexing**: Builds a FAISS index for fast similarity search, enabling efficient retrieval of text related to a query.
- **Search Functionality**: Users can input a search query, and the app will return the most relevant text chunks from the PDF along with their similarity distances to the query. This makes it easy to find specific information.


### **PDF Flowchart Generator 📊**
- **Topic and Subtopic Extraction**: Automatically identifies and organizes the structure of the PDF, extracting the main topics and their subtopics from the document.
- **Flowchart Creation**: Visualizes the topics and subtopics in a network graph, allowing users to see the document's structure at a glance.
- **Graphical Display**: The app displays the flowchart using an interactive network graph, where the main topics are connected to their respective subtopics in a hierarchical structure.
- **Extracted Content Display**: In addition to the flowchart, the extracted topics and subtopics are displayed in a bullet-point list, giving users a clear view of the document’s structure.


## How It Works:
1. **Upload a PDF**: Start by uploading a PDF document into the application.
2. **Extract Text**: The app extracts the text from each page and displays it.
3. **Search for Information**:
   - Input a search query.
   - The app will search the extracted text using FAISS, displaying the relevant text snippets based on similarity to your query.
4. **Visualize the PDF as a Flowchart**:
   - The app identifies topics and subtopics from the PDF text and organizes them into a flowchart.
   - The flowchart provides a clear visual representation of the document’s structure, making it easier to understand the content at a high level.

---

# PDF Information Extractor and Search 📄  


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

---

# Flowchart Generator App Explanation

The Flowchart Generator app enables users to upload a PDF, extract key topics and subtopics, and visualize the extracted content in the form of a hierarchical flowchart. Below is a step-by-step explanation of how the app works:


## 1. PDF Upload
- The app provides a file uploader for users to select and upload a PDF file.
- Once the PDF is uploaded, the app processes the file for further text extraction.

## 2. Text Extraction from PDF
- The app uses a PDF reader to extract text from each page of the PDF.
- It assumes that the first line of every page represents the **main topic**.
- Subsequent lines that begin with characters like "•", "-", or "*" are identified as **subtopics** under the main topic.
- Any paragraphs that follow the subtopics are treated as the main body of text or explanation associated with the topic.

## 3. Topic and Subtopic Mapping
- The app organizes the extracted data into a structure that maps each main topic to its corresponding subtopics and paragraphs.
- This mapping allows for a hierarchical relationship between the topics and subtopics to be visualized later.

## 4. Graph Construction
- The app then builds a directed network graph where the **main topics** act as the **nodes** and the **subtopics** are the **edges** connecting to them.
- This graph visually represents the relationship between topics and subtopics, providing a clear overview of the document’s structure.

## 5. Graph Visualization
- Using a network graph library, the app arranges the main topics at the top of the graph and places the subtopics hierarchically below each topic.
- The graph is displayed in a flowchart format, allowing users to see the structure of the document in a visual and easy-to-understand format.

## 6. Display of Topics and Subtopics
- After generating the flowchart, the app also displays the extracted topics and subtopics in a bullet-point list.
- For each topic, a portion of its associated paragraph is shown to give users additional context about the content.

## 7. User Experience Notes
- The app includes a note that advises users not to upload research papers or handwritten notes, as they may not generate a proper flowchart due to formatting limitations.

---


# Conclusion

Both the **PDF Information Extractor and Search** and **Flowchart Generator** apps offer powerful tools for extracting and interacting with information from PDF documents. The **PDF Information Extractor** uses advanced machine learning techniques to find specific information quickly, while the **Flowchart Generator** visually maps out the structure of the document by identifying topics and subtopics. Together, they provide a comprehensive approach to PDF analysis, combining text search and visualization for an enhanced user experience.


## Requirements:
- **Streamlit**
- **PyPDF2**
- **sentence-transformers**
- **FAISS-cpu**
- **NumPy**
- **Matplotlib**
- **networkx**
- **Pillow**

Make sure to install all required packages before running the app. 📦
