 🤖 ChatGroq PDF QA Bot

An interactive Streamlit web app that uses **LangChain**, **Groq LLM (Mixtral)**, and **FAISS** to let you ask questions from a directory of PDF documents.

 🚀 Features

- Upload PDFs in `RL/` folder
- Automatically creates embeddings using OpenAI
- Uses Groq's LLM (`mixtral-8x7b-32768`) to answer your questions
- Retrieves relevant chunks using FAISS
- Clean and simple UI with Streamlit

---

📂 Folder Structure

chatgroq-pdf-qa/
├── app.py
├── RL/
│   └── (Your PDF files go here)
├── .env
├── requirements.txt
├── README.md
└── .gitignore
