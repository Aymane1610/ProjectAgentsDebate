<div align="center">

# Project Agents Debate
### High-Fidelity RAG System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" />
  <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" />
  <img src="https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=google%20gemini&logoColor=white" />
</p>

<p align="center">
  <b>A premium Retrieval-Augmented Generation (RAG) system leveraging a Multi-Agent Debate framework to ensure accuracy and depth in AI-generated responses.</b>
</p>

<br />

</div>

## 📖 Overview
This project implements a sophisticated **Multi-Agent System** where specialized AI agents (Pro, Contra, Judge, Synthesizer) debate based on information retrieved from a custom knowledge base. This innovative approach mitigates hallucinations, refines arguments, and improves the reliability of the final output.

---

## 🏗️ Architecture

<div align="center">
  <table>
    <tr>
      <td align="center"><b>Backend</b></td>
      <td align="center"><b>RAG Engine</b></td>
      <td align="center"><b>Debate Logic</b></td>
      <td align="center"><b>Frontend</b></td>
      <td align="center"><b>LLM</b></td>
    </tr>
    <tr>
      <td align="center">FastAPI</td>
      <td align="center">FAISS + SentenceTransformers</td>
      <td align="center">Multi-Agent Orchestration</td>
      <td align="center">Vite + React + Framer Motion</td>
      <td align="center">Gemini / OpenAI</td>
    </tr>
  </table>
</div>

### 🧩 Key Components
- **Backend**: Robust API handling with FastAPI.
- **RAG Engine**: Semantic search using FAISS vector store.
- **Debate Logic**: Agents critique and refine answers in real-time.
- **Frontend**: Modern, minimalist UI with fluid animations.

---

## ✨ Key Features
- **🎯 Accurate RAG**: Grounds all arguments in uploaded documents using vector similarity.
- **🗣️ Multi-Agent Debate**: Orchestrates debates between Pro, Contra, and Judge agents.
- **🖥️ Interactive UI**: Upload PDFs and visualize the thinking process of each agent.
- **🎨 High-Fidelity Design**: Professional "Noir & Blanc" aesthetic with glassmorphism effects.

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.9+**
- **Node.js 18+**

### 1️⃣ Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
# Create a .env file with GOOGLE_API_KEY or OPENAI_API_KEY

# Run server
python app.py
```

### 2️⃣ Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 3️⃣ Usage
1. Open your browser at `http://localhost:5173`.
2. Upload PDF documents to the **Knowledge Base** via the UI.
3. Enter a query and watch the agents debate!

---

## 🎨 Design Aesthetics
- **Style**: Professional Black & White (*Noir & Blanc*).
- **Interface**: Data-centric, minimalist, high-tech (Linear-inspired).
- **Interactions**: Fluid transitions powered by **Framer Motion**.

<br />

<div align="center">
  <hr />
  <p>
    <i>Project Agents Debate — Developed by <b>Safae Elaji</b> & <b>Aymane Assou</b>.</i>
  </p>
  <p>
    Research & Development • Universitat Pompeu Fabra
  </p>
</div>
