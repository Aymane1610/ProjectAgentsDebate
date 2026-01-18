# Project Agents Debate: High-Fidelity RAG System

A premium High-Fidelity Retrieval-Augmented Generation (RAG) system leveraging a Multi-Agent Debate framework to ensure accuracy and depth in AI-generated responses.

## Overview
This project implements a sophisticated multi-agent system where AI agents (Pro, Contra, Judge, Synthesizer) debate based on retrieved information from a knowledge base. This approach mitigates hallucinations and improves the reliability of the final output.

## Architecture
- **Backend**: FastAPI for robust API handling.
- **RAG Engine**: FAISS vector store + SentenceTransformers for semantic search.
- **Debate Logic**: Multi-agent orchestration (Pro/Contra/Judge/Synthesizer).
- **Frontend**: Modern UI built with Vite, React, Tailwind CSS, and Framer Motion.
- **LLM Integration**: Supports Gemini and OpenAI models.

## Key Features
- **Accurate RAG**: Uses vector similarity search to ground arguments in provided documents.
- **Multi-Agent Debate**: Agents critique and refine answers through structured debate rounds.
- **Interactive UI**: Upload documents and visualize the debate process in real-time.

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+

### 1. Setup Backend
1. Navigate to the `backend/` directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   - Create a `.env` file in `backend/` with your API keys (GOOGLE_API_KEY or OPENAI_API_KEY).
5. Run the server:
   ```bash
   python app.py
   ```

### 2. Setup Frontend
1. Navigate to the `frontend/` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

### 3. Usage
1. Open your browser and navigate to the frontend URL (typically `http://localhost:5173`).
2. Use the UI to upload PDF documents to the Knowledge Base.
3. Enter a query to start the debate between agents.

## Design Aesthetics
- **Style**: Professional Black & White (Noir & Blanc).
- **Interface**: Clean, minimalist, and high-tech.
- **Interactions**: Smooth animations powered by Framer Motion.

---
*Project Agents Debate - Developed by Safae Elaji & Aymane Assou.*
