# 🤖 AI-360 Career Mentor Bot

An **AI-powered career mentor** that analyzes resumes and provides **personalized guidance** using Retrieval Augmented Generation (RAG).

Built in **24 hours** during Forge Inspira Hackathon 🚀

## 📌 Problem Statement

Job seekers often struggle with:
- Identifying **skill gaps** in their resumes
- Understanding **career pathways** aligned with their background  
- Receiving **personalized guidance** at scale

**Our solution:** **AI-360 Career Mentor Bot** – a chatbot that parses resumes, compares skills with industry standards, and provides tailored career advice.

## ✨ Key Features

- 📄 **Resume Parsing** → Extracts education, skills, projects, and work experience from PDF resumes
- 🔍 **Skill Gap Analysis** → Matches resume content against role-specific knowledge
- 💡 **Personalized Career Advice** → Provides recommendations on upskilling and career paths
- 🧠 **RAG Chatbot** → Uses vector embeddings + LLMs to answer user's career questions in context
- ⚡ **Streamlit App** → Lightweight, interactive UI for demo

## 📂 Project Structure

```
ai-360-career-mentor-bot/
│
├── src/
│   ├── app.py                  # Streamlit entry point
│   ├── config.py               # API keys / env config
│   ├── utils/                  # Resume + preprocessing utils
│   │   ├── text_preprocessing.py
│   │   ├── pdf_parser.py
│   │   └── resume_parser.py
│   ├── rag/                    # Retrieval Augmented Generation
│   │   ├── retriever.py
│   │   ├── vector_store.py     # FAISS / Pinecone DB
│   │   └── rag_pipeline.py
│   └── chatbot/                # Chatbot logic
│       ├── prompts.py
│       └── career_bot.py
│
├── tests/                      # Unit tests
├── notebooks/                  # Prototyping & experiments
├── data/                       # Sample resumes/JDs
├── .gitignore
├── README.md
└── requirements.txt
```

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** → Frontend UI
- **LangChain** → RAG pipeline
- **FAISS / Pinecone** → Vector database
- **OpenAI / HuggingFace** → Embeddings + LLMs
- **PyPDF2 / pdfplumber** → PDF parsing

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/SOHAM-3T/ai-360-career-mentor-bot.git
cd ai-360-career-mentor-bot
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the root directory and add your API keys:
```env
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
```

### 5. Run the Streamlit app
```bash
streamlit run src/app.py
```

## 🎯 Hackathon MVP Scope

✅ Upload resume PDF → Extract details  
✅ Store + retrieve embeddings using FAISS  
✅ Streamlit chatbot interface  
✅ Answer career questions contextually  

## 📌 Future Scope

- Job recommendation engine
- Interview prep Q&A
- LinkedIn/GitHub integration
- Career progress dashboard
- Multi-language support
- Mobile app version

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Soham**
- GitHub: [@SOHAM-3T](https://github.com/SOHAM-3T)

---

⚡️ *Built in 24 hours during Forge Inspira Hackathon*