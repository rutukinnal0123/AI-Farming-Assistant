# AI Farming Assistant

AI Farming Assistant is an AI-powered web application that provides personalized agricultural guidance to farmers. The system combines Google Gemini with Retrieval-Augmented Generation (RAG) to generate context-aware recommendations using farmer information, agricultural documents, farming history, and real-time weather conditions.

The application enables farmers to interact through text or voice, manage multiple farms, track farming activities, and receive personalized recommendations to support better farming decisions.

---

# Problem Statement

Farmers often rely on generic agricultural recommendations that do not consider their individual farming conditions such as crop type, soil type, irrigation method, farm location, previous farming activities, or current weather conditions. This makes decision-making difficult and may reduce productivity.

AI Farming Assistant addresses this problem by providing personalized recommendations using Generative AI and a domain-specific agricultural knowledge base.

---

# Features

### Farmer Management

* Secure farmer registration and login
* User authentication using JWT
* Manage farmer profile information

### Farm Management

* Register and manage multiple farms
* Store crop details
* Store soil type
* Store irrigation method
* Store farm location and land information

### AI Chat Assistant

* Conversational farming assistant powered by Google Gemini 1.5 Flash
* Personalized responses based on farmer profile
* Context-aware recommendations using Retrieval-Augmented Generation (RAG)

### Voice Interaction

* Speech-to-Text for voice input
* Text-to-Speech for AI responses

### Activity Tracking

* Record farming activities
* Maintain activity history
* Generate recommendations using previous farming activities

### Chat History

* Store and retrieve previous conversations

### Weather Integration

* Fetch real-time weather information
* Include weather conditions while generating farming recommendations

### Retrieval-Augmented Generation (RAG)

* Load agricultural reference documents
* Split documents into semantic chunks
* Generate embeddings using Hugging Face Embeddings
* Store embeddings in ChromaDB
* Retrieve relevant document chunks using semantic search
* Generate responses using retrieved knowledge and farmer-specific context

---

# Technology Stack

| Component            | Technology                                       |
| -------------------- | ------------------------------------------------ |
| Frontend             | Streamlit                                        |
| Backend              | FastAPI                                          |
| Programming Language | Python                                           |
| Database             | Supabase                                         |
| Authentication       | JWT                                              |
| AI Framework         | LangChain                                        |
| Large Language Model | Google Gemini 1.5 Flash                          |
| Embedding Model      | Hugging Face Embeddings (BAAI/bge-small-en-v1.5) |
| Vector Database      | ChromaDB                                         |
| AI Technique         | Retrieval-Augmented Generation (RAG)             |
| APIs                 | Gemini API, Weather API                          |
| Voice Processing     | Speech-to-Text, Text-to-Speech                   |

---

# System Architecture

```text
                        Farmer
                           │
                           ▼
                  Streamlit Frontend
                           │
                Text Input / Voice Input
                           │
                           ▼
                    FastAPI Backend
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
    Supabase          Weather API      Speech-to-Text
        │
        ▼
 Farmer Profile
 Farm Details
 Activity History
 Chat History
        │
        ▼
          RAG Pipeline (LangChain)
                  │
      Agricultural PDF Documents
                  │
             Text Chunking
                  │
        Hugging Face Embeddings
                  │
              ChromaDB
                  │
          Semantic Retrieval
                  │
                  ▼
         Google Gemini 1.5 Flash
                  │
                  ▼
      Personalized Recommendation
                  │
                  ▼
            Text-to-Speech
                  │
                  ▼
                Farmer
```

---

# Project Structure

```text
AI-Farming-Assistant/
│
├── backend/
│   ├── services/
│   ├── app.py
│   ├── auth.py
│   ├── chat.py
│   ├── crud.py
│   ├── database.py
│   ├── farmer.db
│   ├── models.py
│   ├── requirements.txt
│   ├── schemas.py
│   ├── security.py
│   └── __init__.py
│
├── frontend/
│   ├── app.py
│   └── ...
│
├── rag/
│   ├── backend/
│   ├── documents/
│   │   ├── 1.pdf
│   │   ├── Beginner vegetable garden.pdf
│   │   ├── Coconut Main Field.pdf
│   │   ├── Coconut Planting Seasons and Climate.pdf
│   │   ├── Coconut Processing.pdf
│   │   ├── Harvest and Post Harvest.pdf
│   │   ├── Irrigation Management.pdf
│   │   ├── Nutrient Management.pdf
│   │   ├── Organic farming.pdf
│   │   ├── Pest and Disease Management.pdf
│   │   ├── Problematic-Soils-and-Their-Management.pdf
│   │   ├── Kerala Agriculture University.pdf
│   │   └── Vegetable Garden.pdf
│   │
│   ├── rag/
│   │   ├── chroma.sqlite3
│   │   ├── embeddings.py
│   │   └── retriever.py
│
├── README.md
└── __notebook_source__.ipynb
```

---

# Working Flow

1. The farmer logs into the application.
2. The farmer registers one or more farms and provides farm details.
3. The farmer interacts with the assistant using text or voice.
4. FastAPI retrieves the farmer profile, farm information, activity history, and weather information.
5. The RAG pipeline retrieves relevant agricultural information from the knowledge base using semantic search.
6. Retrieved document context, farmer information, weather data, and the user's query are combined into a prompt.
7. Google Gemini 1.5 Flash generates a personalized response.
8. The conversation is stored in chat history.
9. The response is displayed in the Streamlit application and can also be converted to speech.

---

Installation
1. Clone the repository
git clone https://github.com/your-username/AI-Farming-Assistant.git

cd AI-Farming-Assistant
2. Install dependencies
pip install -r backend/requirements.txt
3. Configure environment variables

Create a .env file inside the backend directory and add your credentials.

Example:

GEMINI_API_KEY=your_gemini_api_key

SUPABASE_URL=your_supabase_url

SUPABASE_KEY=your_supabase_key

WEATHER_API_KEY=your_weather_api_key
Run the Backend

Navigate to the backend folder and start the FastAPI server.

cd backend

uvicorn app:app --reload

The backend will run at:

http://localhost:8000
Run the Frontend

Open a new terminal and navigate to the frontend folder.

cd frontend

streamlit run app.py

The application will open in your browser at:

http://localhost:8501


# Target Audience

AI Farming Assistant is intended for:

* Farmers seeking personalized agricultural recommendations and farming assistance.
* Agricultural researchers and students exploring AI applications in agriculture.
* Agricultural extension officers supporting farmers with technology-driven advisory services.
* Developers interested in Generative AI, Retrieval-Augmented Generation (RAG), and AI-powered chatbot applications.
* Educational institutions and organizations working on smart farming and precision agriculture solutions.

# Conclusion

AI Farming Assistant demonstrates the practical application of Generative AI in agriculture by integrating Google Gemini with a Retrieval-Augmented Generation pipeline. By combining farmer-specific information, agricultural knowledge, activity history, and weather conditions, the application delivers personalized, context-aware recommendations that help farmers make better-informed decisions.
