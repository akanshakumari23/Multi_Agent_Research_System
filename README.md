# 🚀 ResearchMind

### Multi-Agent AI Research Pipeline Powered by LangChain, LangGraph, Tavily & Mistral AI

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge\&logo=python)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge\&logo=streamlit)]()
[![LangChain](https://img.shields.io/badge/LangChain-Agent-green?style=for-the-badge)]()
[![Mistral AI](https://img.shields.io/badge/Mistral-AI-purple?style=for-the-badge)]()

🌐 **Live Demo:** https://researchmind-fjhr.onrender.com

🎥 **Demo Video:** Add Your YouTube Video Link Here

⭐ An intelligent multi-agent research platform that automates web research, information extraction, report generation, and quality review using collaborative AI agents.

---

## 📌 Overview

ResearchMind is a Multi-Agent AI Research System that leverages specialized AI agents to perform end-to-end research workflows autonomously.

Instead of relying on a single LLM response, ResearchMind orchestrates multiple intelligent agents that collaborate to:

* Search the web for relevant information
* Extract and analyze insights
* Generate structured research reports
* Critique and improve outputs
* Deliver publication-ready results

---

## ✨ Key Features

### 🔍 Search Agent

* Real-time web search using Tavily Search API
* Reliable and recent information retrieval
* Intelligent source selection

### 📖 Reader Agent

* Content extraction and summarization
* Key insight identification
* Information filtering

### ✍️ Writer Agent

* Structured report generation
* Professional research formatting
* Clear and coherent content creation

### 🧠 Critique Agent

* Quality assurance
* Research refinement
* Gap detection and improvement

### 🎨 Modern User Interface

* Streamlit-powered UI
* Responsive design
* Interactive workflow visualization

---

## 🏗️ Architecture

User Query
↓
Search Agent
↓
Reader Agent
↓
Writer Agent
↓
Critique Agent
↓
Final Research Report

---

## 🛠️ Tech Stack

* Python
* Streamlit
* LangChain
* LangGraph
* Mistral AI
* Tavily Search API
* BeautifulSoup
* Requests
* Pydantic
* Pandas

---

## 📂 Project Structure

```text
Multi_Agent_Research_System/
│
├── app.py
├── agents.py
├── pipeline.py
├── tools.py
├── requirements.txt
├── runtime.txt
├── .gitignore
│
├── .streamlit/
│   └── config.toml
│
└── README.md
```

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/akanshakumari23/Multi_Agent_Research_System.git

cd Multi_Agent_Research_System
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create `.env`

```env
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### Run Locally

```bash
streamlit run app.py
```

---

## 🌐 Live Demo

https://researchmind-fjhr.onrender.com

---

## 🎥 Demo Video

Upload your demo video to YouTube and place the link here:

```text
https://youtu.be/your-video-id
```

---

## ☁️ Deployment

### Render Deployment

Build Command

```bash
pip install -r requirements.txt
```

Start Command

```bash
streamlit run app.py --server.address=0.0.0.0 --server.port=$PORT
```

Environment Variables

```env
MISTRAL_API_KEY=xxxxxxxx
TAVILY_API_KEY=xxxxxxxx
```

---

## 🎯 Use Cases

* Academic Research
* Literature Reviews
* Technical Research
* Market Analysis
* Industry Reports
* Competitive Intelligence
* AI-Assisted Knowledge Discovery

---

## 🔮 Future Improvements

* PDF Export
* Citation Generation
* Research Memory
* Multi-Language Support
* RAG Integration
* Ollama Support
* Local LLM Support
* Advanced Fact Verification

---

## 👩‍💻 Author

### Akansha Kumari

Electrical Engineering Student | AI Enthusiast | Developer

Built with ❤️ using Streamlit, LangChain, LangGraph, Tavily Search, and Mistral AI.

GitHub:
https://github.com/akanshakumari23

---

## ⭐ Support

If you found this project useful:

⭐ Star the repository

🍴 Fork the project

📢 Share it with fellow developers

Your support helps the project grow and reach more researchers and developers.
