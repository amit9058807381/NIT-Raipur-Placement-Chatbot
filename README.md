# NIT Raipur Placement Chatbot

An AI-powered RAG-based chatbot that helps students explore NIT Raipur placement and interview experiences using previously collected placement data.

The system uses semantic search to retrieve relevant placement experiences and Gemini AI to generate answers based only on the retrieved information.

---

## Features

- User Registration and Login
- User-specific Chat History
- Multiple Conversations
- Create New Chat
- Delete Conversations
- Automatic Chat Titles
- AI-powered Placement Q&A
- RAG-based Semantic Search
- Placement and Interview Experience Search
- ChromaDB Vector Database
- MongoDB Atlas for Users, Conversations and Messages
- Gemini Embeddings
- Gemini LLM for Answer Generation
- React-based ChatGPT-style Interface

---

## Tech Stack

### Frontend

- React.js
- Vite
- JavaScript
- CSS

### Backend

- Python
- Flask
- Flask-CORS

### AI / RAG

- Google Gemini
- Gemini Embeddings
- ChromaDB
- Retrieval-Augmented Generation (RAG)

### Database

- MongoDB Atlas

### Data Processing

- Python
- Pandas
- Excel
- CSV

### Authentication

- bcrypt

---

## How It Works

```text
User Question
      |
      v
Gemini Embedding
      |
      v
ChromaDB Semantic Search
      |
      v
Relevant Placement Documents
      |
      v
RAG Context
      |
      v
Gemini LLM
      |
      v
Generated Answer
      |
      v
User

The chatbot retrieves relevant placement experiences from the vector database before generating an answer.

This helps the chatbot answer questions using the available placement data instead of generating unsupported information.

Project Structure
NIT-Raipur-Placement-Chatbot/
|
├── backend/
|   |
|   ├── app.py
|   ├── clean_data.py
|   ├── create_documents.py
|   ├── create_vector_db.py
|   ├── search_documents.py
|   ├── rag_test.py
|   |
|   ├── data/
|   |   ├── Interview Experience (Responses).xlsx
|   |   ├── OA_Interview Experience (Batch 2026).xlsx
|   |   ├── documents/
|   |   |   └── placement_documents.txt
|   |   |
|   |   └── processed/
|   |       └── placement_data.csv
|   |
|   └── ...
|
├── frontend/
|   |
|   ├── src/
|   |   ├── App.jsx
|   |   ├── Login.jsx
|   |   ├── Register.jsx
|   |   ├── App.css
|   |   └── index.css
|   |
|   ├── package.json
|   └── vite.config.js
|
├── .gitignore
└── README.md
Data Pipeline

Placement data can be updated when new placement or interview experiences are collected.

Excel Data
    |
    v
Data Cleaning
    |
    v
placement_data.csv
    |
    v
Document Generation
    |
    v
placement_documents.txt
    |
    v
Gemini Embeddings
    |
    v
ChromaDB

When new placement data is collected, it can be processed through the existing data preparation pipeline and the vector database can be regenerated.

Backend Setup
1. Clone the Repository
git clone https://github.com/amit9058807381/NIT-Raipur-Placement-Chatbot.git
cd NIT-Raipur-Placement-Chatbot
2. Create Python Virtual Environment

Go to the backend folder:

cd backend

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate
3. Install Dependencies

Install the required Python packages:

pip install flask flask-cors python-dotenv google-genai chromadb pymongo bcrypt pandas openpyxl
4. Configure Environment Variables

Create a .env file inside the backend folder:

GEMINI_API_KEY=your_gemini_api_key
MONGODB_URI=your_mongodb_connection_string

Do not upload .env to GitHub.

5. Create Vector Database

From the backend directory:

python create_vector_db.py

This creates the ChromaDB vector collection from the placement documents.

6. Start Backend
python app.py

Backend runs on:

http://127.0.0.1:5000
Frontend Setup

Open another terminal and go to the frontend folder:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

Frontend normally runs on:

http://localhost:5173
Authentication

The application provides:

User Registration
User Login
Password Hashing using bcrypt
User-specific Conversations
User-specific Chat History

Passwords are stored as bcrypt hashes rather than plain text.

Database Structure

MongoDB contains three main collections:

placement_chatbot
|
├── users
├── conversations
└── messages
Users

Stores:

Name
Email
Password Hash
Conversations

Stores:

User Email
Chat Title
Created Time
Updated Time
Messages

Stores:

Conversation ID
User Email
Role
Message Content
Created Time
RAG Architecture

The chatbot follows a Retrieval-Augmented Generation approach.

Retrieval

The user's question is converted into an embedding using Gemini Embeddings.

ChromaDB performs semantic similarity search and retrieves the most relevant placement documents.

Generation

The retrieved documents are provided as context to Gemini.

The model generates the answer using the retrieved placement information.

The prompt instructs the model not to invent information when the answer is unavailable in the placement data.

Example Questions

The chatbot can answer questions such as:

What coding questions were asked in Pine Labs?

What was the test pattern for Deloitte?

What topics were asked in technical interviews?

What companies have interview experiences available?

What kind of coding questions were asked in a particular company?
Future Improvements
Automatic placement data ingestion
Admin dashboard for adding new placement experiences
More placement datasets
Advanced filtering by company, role and batch
Source citations for retrieved experiences
Deployment to cloud platforms
Improved authentication and session management
Analytics dashboard for placement trends
Disclaimer

This project is intended for educational and informational purposes.

The chatbot answers questions based on the placement and interview experience data available in its database. Actual recruitment processes, interview questions and placement outcomes may vary.

Author

Amit Kumar

MCA
NIT Raipur

GitHub: https://github.com/amit9058807381
