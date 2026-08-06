# AI Farming Assistant

An AI-powered farming assistant that provides personalized agricultural guidance based on farmer profiles, farming activities, and agricultural knowledge. The system combines Generative AI with Retrieval-Augmented Generation (RAG) to deliver context-aware recommendations instead of generic responses.

---

## Overview

AI Farming Assistant is designed to support smallholder farmers by providing personalized farming recommendations. Traditional advisory systems often provide the same recommendations to every farmer without considering factors such as crop type, soil conditions, irrigation methods, or farming history.

This project addresses that challenge by combining farmer-specific information with agricultural knowledge stored in a vector database. Before generating a response, the system retrieves relevant information from agricultural documents and combines it with the farmer's profile, allowing the AI to generate more accurate and context-aware recommendations.

---

## Problem Statement

Smallholder farmers face several challenges while making day-to-day farming decisions:

* Generic farming recommendations that do not consider local conditions
* Lack of personalized agricultural support
* Difficulty maintaining farming activity records
* Limited access to organized agricultural knowledge

The goal of this project is to provide farmers with a digital assistant capable of understanding their farming context and providing personalized guidance.

---

## Features

### Farmer Management

* Farmer registration and login
* Secure authentication using JWT
* Manage farmer profile information

### Farm Management

* Create and manage farm details
* Store crop information
* Store soil type
* Store irrigation method
* Store farm location and land details

### AI Chat Assistant

* Ask farming-related questions in natural language
* Personalized responses based on farmer profile
* Context-aware recommendations using RAG
* Conversational interaction with Gemini

### Activity Tracking

* Record farming activities
* Maintain farming history
* Use previous activities as additional context for recommendations

### Retrieval-Augmented Generation (RAG)

* Agricultural documents are converted into embeddings
* Documents are stored in a FAISS vector database
* Relevant information is retrieved before sending the prompt to Gemini
* Responses are generated using both retrieved knowledge and farmer context

---

## System Architecture

```text
                Farmer
                   │
                   ▼
            React Frontend
                   │
                   ▼
            FastAPI Backend
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
 PostgreSQL Database      RAG Pipeline
        │                     │
        │              Agricultural PDFs
        │                     │
 Farmer Profile         Document Chunking
 Farm Details                 │
 Activities              Embeddings
                              │
                           FAISS
                              │
                     Relevant Context
                              │
                              ▼
                        Gemini API
                              │
                              ▼
                  Personalized Response
```

---

## Technology Stack

| Component       | Technology                     |
| --------------- | ------------------------------ |
| Frontend        | React                          |
| Backend         | FastAPI                        |
| Language        | Python                         |
| Database        | PostgreSQL                     |
| ORM             | SQLAlchemy                     |
| Authentication  | JWT                            |
| LLM             | Google Gemini                  |
| AI Framework    | LangChain                      |
| Embedding Model | Hugging Face Embeddings        |
| Vector Database | FAISS                          |
| RAG             | Retrieval-Augmented Generation |

---

## Project Structure

```text
AI-Farming-Assistant/

├── frontend/
│
├── backend/
│   ├── app.py
│   ├── auth.py
│   ├── chat.py
│   ├── crud.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│
├── rag/
│   ├── documents/
│   ├── chroma_db/
│   ├── retriever.py
│   └── prompt.py
│
├── requirements.txt
└── README.md
```

---

## How It Works

1. Farmer logs into the application.
2. Farmer creates or updates their farm profile.
3. Farmer asks a farming-related question.
4. The backend retrieves the farmer's profile and previous farming activities.
5. The RAG pipeline searches the agricultural knowledge base for relevant information.
6. The retrieved context and farmer information are combined into a prompt.
7. Gemini generates a personalized recommendation.
8. The response is returned to the farmer through the application.

---

## Example Workflow

**Farmer Profile**

* Crop: Coconut
* Soil Type: Laterite
* Irrigation: Drip Irrigation

**Farmer Question**

> When should I irrigate my crop?

**System Process**

* Retrieves farmer profile
* Searches agricultural documents using RAG
* Combines retrieved context with the farmer's question
* Generates a personalized recommendation using Gemini

---

## Future Improvements

Potential enhancements for future versions include:

* Voice-based interaction
* Weather-based recommendations
* Government scheme notifications
* Crop price information
* Plant disease detection using computer vision

---

## Learning Outcomes

This project provided practical experience in:

* Full Stack Web Development
* FastAPI
* React
* PostgreSQL
* JWT Authentication
* LangChain
* Retrieval-Augmented Generation (RAG)
* Vector Databases
* Hugging Face Embeddings
* Google Gemini API Integration
* Prompt Engineering

---

## Conclusion

AI Farming Assistant demonstrates how Generative AI and Retrieval-Augmented Generation can be used to build a personalized agricultural advisory system. By combining farmer-specific information with agricultural knowledge, the application provides recommendations that are tailored to individual farming conditions rather than generic responses.
