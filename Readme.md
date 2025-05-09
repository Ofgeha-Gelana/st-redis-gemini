# AI Chat with Context Memory using Gemini, Redis, and ChromaDB

This project implements two context-aware AI chat applications using **Google's Gemini Pro**, built with **Streamlit**. It demonstrates two approaches for handling conversation memory:

- **Redis-based caching** for session-level chat persistence
- **ChromaDB vector search** for semantic memory retrieval

Both apps use efficient memory strategies to enhance response quality, reduce redundant API calls, and optimize performance.

![Screenshot](https://raw.githubusercontent.com/Ofgeha-Gelana/st-redis-gemini/refs/heads/main/src/Screenshot%20from%202025-02-08%2010-02-11.png)


---

##  Features

- **Streamlit Interface** – Simple and responsive web UI for chatting with AI
- **Memory via Redis** – Stores full chat history in Redis for immediate recall
- **Memory via ChromaDB** – Uses vector embeddings and semantic search for intelligent context
- **Gemini Pro Integration** – Generates responses using Google’s generative AI API
- **Optimized API Usage** – Avoids unnecessary Gemini calls by checking historical context

---

## Technologies

- **[Streamlit](https://streamlit.io/)** – UI framework for rapid prototyping
- **[Google Generative AI SDK](https://ai.google.dev/)** – Access Gemini models
- **[Redis](https://redis.io/)** – High-performance in-memory cache
- **[ChromaDB](https://www.trychroma.com/)** – Local vector database for embeddings
- **[SentenceTransformers](https://www.sbert.net/)** – Text embeddings for semantic search
- **Python** – Core programming language

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Ofgeha-Gelana/st-redis-gemini.git
cd st-redis-gemini

python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

