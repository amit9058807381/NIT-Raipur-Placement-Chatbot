import os
import re

from flask import Flask, request, jsonify
from flask_cors import CORS

from dotenv import load_dotenv
from google import genai
import chromadb
from pymongo import MongoClient
import bcrypt
from datetime import datetime
from bson import ObjectId


# 1. Load environment variables


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
mongodb_uri = os.getenv("MONGODB_URI")


if not api_key:
    print("ERROR: GEMINI_API_KEY not found!")
    exit()


if not mongodb_uri:
    print("ERROR: MONGODB_URI not found!")
    exit()



# 2. Create Flask app


app = Flask(__name__)

CORS(app)



# 3. Create Gemini client


client = genai.Client(
    api_key=api_key
)



# 4. Connect to ChromaDB

chroma_client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = chroma_client.get_collection(
    name="placement_documents"
)



# 5. Connect to MongoDB Atlas


mongo_client = MongoClient(
    mongodb_uri
)

db = mongo_client["placement_chatbot"]

users_collection = db["users"]

conversations_collection = db["conversations"]

messages_collection = db["messages"]



# 6. Home / Health Check


@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "NIT Raipur Placement Chatbot API is running!"
    })



# 7. USER REGISTRATION

@app.route("/api/auth/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")


    
    # Validate fields
    

    if not name or not email or not password:

        return jsonify({
            "error": "Name, email and password are required"
        }), 400


    
    # Check existing user
    

    existing_user = users_collection.find_one({
        "email": email
    })

    if existing_user:

        return jsonify({
            "error": "User already exists"
        }), 409


    
    # Hash password
    

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )


    
    # Save user in MongoDB
    

    users_collection.insert_one({

        "name": name,

        "email": email,

        "password": password_hash.decode("utf-8")

    })


    
    # Response
    

    return jsonify({

        "message": "User registered successfully"

    }), 201



# 8. USER LOGIN


@app.route("/api/auth/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    

    # Validate field
    
    if not email or not password:

        return jsonify({
            "error": "Email and password are required"
        }), 400


    
    # Find user
    

    user = users_collection.find_one({
        "email": email
    })

    if not user:

        return jsonify({
            "error": "Invalid email or password"
        }), 401



    # Check password

    password_match = bcrypt.checkpw(

        password.encode("utf-8"),

        user["password"].encode("utf-8")

    )


    if not password_match:

        return jsonify({
            "error": "Invalid email or password"
        }), 401


    
    # Login successful

    return jsonify({

        "message": "Login successful",

        "name": user["name"],

        "email": user["email"]

    }), 200



# 9. CREATE NEW CONVERSATION

@app.route("/api/conversations", methods=["POST"])
def create_conversation():

    data = request.get_json()

    email = data.get("email")


    if not email:

        return jsonify({
            "error": "Email is required"
        }), 400


    current_time = datetime.utcnow()


    conversation = {

        "user_email": email,

        "title": "New Chat",

        "created_at": current_time,

        "updated_at": current_time

    }


    result = conversations_collection.insert_one(
        conversation
    )


    return jsonify({

        "message": "Conversation created",

        "conversation_id": str(
            result.inserted_id
        ),

        "title": conversation["title"]

    }), 201



# 10. GET CHAT HISTORY

@app.route("/api/conversations", methods=["GET"])
def get_conversations():

    email = request.args.get("email")


    if not email:

        return jsonify({
            "error": "Email is required"
        }), 400


    conversations = conversations_collection.find(

        {
            "user_email": email
        }

    ).sort(

        "updated_at",
        -1
    )


    result = []


    for conversation in conversations:

        result.append({

            "_id": str(
                conversation["_id"]
            ),

            "title": conversation.get(
                "title",
                "New Chat"
            ),

            "user_email": conversation.get(
                "user_email"
            ),

            "created_at":
                conversation.get(
                    "created_at"
                ).isoformat()
                if conversation.get("created_at")
                else None,

            "updated_at":
                conversation.get(
                    "updated_at"
                ).isoformat()
                if conversation.get("updated_at")
                else None

        })


    return jsonify(result), 200



# 11. GET MESSAGES OF A CONVERSATION

@app.route(
    "/api/conversations/<conversation_id>",
    methods=["GET"]
)
def get_messages(conversation_id):

    email = request.args.get("email")


    if not email:

        return jsonify({
            "error": "Email is required"
        }), 400


    
    # Check conversation belongs to this user

    try:

        conversation = conversations_collection.find_one({

            "_id": ObjectId(conversation_id),

            "user_email": email

        })

    except Exception:

        return jsonify({
            "error": "Invalid conversation ID"
        }), 400


    if not conversation:

        return jsonify({
            "error": "Conversation not found"
        }), 404


    
    # Get messages of this user's conversation

    messages = messages_collection.find({

        "conversation_id": conversation_id,

        "user_email": email

    }).sort(

        "created_at",
        1
    )


    chat_messages = []


    for message in messages:

        chat_messages.append({

            "role": message["role"],

            "content": message["content"],

            "created_at": message["created_at"]

        })


    return jsonify(chat_messages), 200



# 12. DELETE CONVERSATION

@app.route(
    "/api/conversations/<conversation_id>",
    methods=["DELETE"]
)
def delete_conversation(conversation_id):

    try:

        conversation = conversations_collection.find_one({

            "_id": ObjectId(conversation_id)

        })

    except Exception:

        return jsonify({

            "error": "Invalid conversation ID"

        }), 400


    if not conversation:

        return jsonify({

            "error": "Conversation not found"

        }), 404


    # Delete all messages of this conversation

    messages_collection.delete_many({

        "conversation_id": conversation_id

    })


    # Delete conversation

    conversations_collection.delete_one({

        "_id": ObjectId(conversation_id)

    })


    return jsonify({

        "message": "Conversation deleted successfully"

    }), 200



# 13. CHAT / RAG API

@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.get_json()

    query = data.get("query")

    email = data.get("email")

    conversation_id = data.get(
        "conversation_id"
    )


    
    # Validate query

    if not query:

        return jsonify({

            "error": "Query is required"

        }), 400


    
    # Validate email

    if not email:

        return jsonify({

            "error": "Email is required"

        }), 400


    
    # Validate conversation

    if not conversation_id:

        return jsonify({

            "error": "Conversation ID is required"

        }), 400


    
    # STUDY PLAN REQUEST DETECTION

    study_plan_keywords = [

        "study plan",

        "preparation plan",

        "prepare",

        "preparation",

        "interview plan",

        "days left",

        "day plan",

        "din ka plan",

        "din baad interview",

        "interview ke liye",

        "preparation karni hai"

    ]


    is_study_plan_request = any(

        keyword in query.lower()

        for keyword in study_plan_keywords

    )


    
    # DETECT NUMBER OF DAYS

    requested_days = None

    day_patterns = [
        r"(\d+)\s*days?",
        r"(\d+)\s*day",
        r"(\d+)\s*din",
        r"(\d+)\s*days?\s*(?:left|baad)",
        r"(\d+)\s*din\s*(?:baad|bache)"
    ]

    for pattern in day_patterns:

        match = re.search(
            pattern,
            query.lower()
        )

        if match:
            requested_days = int(match.group(1))
            break


    
    # HANDLE TOMORROW / KAL

    if requested_days is None:

        if (
            "tomorrow" in query.lower()
            or "kal" in query.lower()
        ):
            requested_days = 1


    
    # Check conversation belongs to user

    try:

        conversation = conversations_collection.find_one({

            "_id": ObjectId(conversation_id),

            "user_email": email

        })

    except Exception:

        return jsonify({

            "error": "Invalid conversation ID"

        }), 400


    if not conversation:

        return jsonify({

            "error": "Conversation not found"

        }), 404


    
    # Create query embedding

    try:

        response = client.models.embed_content(

            model="gemini-embedding-001",

            contents=query

        )

        query_embedding = response.embeddings[0].values

    except Exception as e:

        print("Embedding Error:", e)

        return jsonify({

            "error": "Unable to process the query embedding"

        }), 500


    
    # Search ChromaDB
    

    try:

        results = collection.query(

            query_embeddings=[query_embedding],

            n_results=3

        )

    except Exception as e:

        print("ChromaDB Error:", e)

        return jsonify({

            "error": "Unable to search placement data"

        }), 500


    
    # Get documents

    documents = results["documents"][0]


    
    # Create context

    context = "\n\n".join(documents)


    
    # RAG PROMPT

    if is_study_plan_request:

        prompt = f"""
You are an NIT Raipur placement and interview preparation assistant.

The user is asking for a study/preparation plan.

IMPORTANT RULES:

1. Use ONLY the placement information provided in the Context.

2. Do NOT use outside knowledge.

3. Do NOT invent interview topics, coding questions,
   subjects, HR questions or company information.

4. Identify the company relevant to the user's current
   conversation/question from the Context.

5. Create the study plan ONLY from topics/questions
   actually present in the retrieved placement records.

6. The number of days in the plan MUST match the number
   of days requested by the user.

7. If the user says:
   "2 days"
   create exactly 2 days.

8. If the user says:
   "5 days"
   create exactly 5 days.

9. Do not create extra days.

10. Distribute the available reported topics across
    the requested number of days.

11. Prioritize topics that were actually asked in the
    company's reported interview experience.

12. If coding questions are available, include them
    in the preparation plan.

13. If core subject questions are available, include them.

14. If project discussion is available, include project
    preparation.

15. If HR or miscellaneous questions are available,
    include them.

16. Do not claim that a topic was asked if it is not
    present in the Context.

17. If the requested number of days is larger than the
    available information, distribute the available
    topics across the requested days without inventing
    new topics.

18. Use Markdown formatting.

19. Keep the plan practical and easy to follow.

20. Mention the actual company name when it is available.

--------------------------------------------------
STUDY PLAN FORMAT
--------------------------------------------------

Use this structure:

## <Number>-Day <Company> Interview Preparation Plan

### Day 1

**Topics to Study:**
- Topic from reported experience
- Topic from reported experience

**Practice:**
- Actual reported coding/interview question

### Day 2

**Topics to Study:**
- Topic from reported experience

**Practice:**
- Actual reported question

Continue until EXACTLY the requested number of days
has been completed.

--------------------------------------------------
CONTEXT
--------------------------------------------------

{context}

--------------------------------------------------
USER QUESTION
--------------------------------------------------

{query}

--------------------------------------------------
FINAL ANSWER
--------------------------------------------------
"""

    else:

        prompt = f"""
You are an NIT Raipur placement and interview assistant.

Your job is to answer the user's question using ONLY
the placement information provided in the Context.

The user has exactly {requested_days} day(s) available for preparation.

IMPORTANT RULES:

1. Do NOT make up any information.

2. Do NOT use outside knowledge.

3. If the requested information is not available in
   the Context, clearly say:

   "This information is not available in the placement data."

4. Use Markdown formatting.

5. Make the answer clean, structured and easy to read.

6. Whenever a placement experience is being described,
   use the original placement column names as headings.

7. Do NOT combine different placement experiences.

8. If multiple companies or multiple records are
   relevant, show them separately.

9. If the user asks about one specific field, such as
   coding questions, show only the relevant field.

10. If the user asks for complete company information,
    show all available relevant fields.

11. Do not create values for fields that are missing.

12. Keep the answer concise but informative.

13. The study plan MUST contain exactly {requested_days} days.

14. Do NOT create fewer or more than {requested_days} days.

15. Distribute the available reported topics across
   exactly {requested_days} days.

16. Create the study plan ONLY from topics and questions
    actually present in the retrieved placement records.

17. If coding questions are available, include them.

18. If project discussion is available, include it.

19. If core subject questions are available, include them.

20. Do NOT invent topics just to fill the requested days.
--------------------------------------------------
STRUCTURED FORMAT
--------------------------------------------------

When complete placement information is available,
follow this format:

### Company Name: <company>

**Source:** <source>

**CTC:** <ctc>

**Test Pattern:** <test pattern>

**Test Duration:** <test duration>

**Question Topics:** <question topics>

**Interview Duration:** <interview duration>

**Topics Asked:** <topics asked>

**Coding Questions Asked:** <coding questions>

**Core Subject Questions:** <core subject questions>

**Project Discussion:** <project discussion>

**Miscellaneous:** <miscellaneous>

Only display fields that actually exist in the
retrieved context.

--------------------------------------------------
MULTIPLE EXPERIENCES
--------------------------------------------------

If more than one placement experience is relevant,
separate them clearly:

### Company Name: Optum

**Source:** ...

**CTC:** ...

**Test Pattern:** ...

...

---

### Company Name: Deloitte

**Source:** ...

**CTC:** ...

**Test Pattern:** ...

...

--------------------------------------------------
FIELD-SPECIFIC QUESTIONS
--------------------------------------------------

If the user asks:

"What coding questions were asked in Optum?"

Answer like:

### Optum

**Coding Questions Asked:**

- Question 1
- Question 2
- Question 3

Do NOT show unrelated fields.

If the user asks:

"What was the test pattern of Optum?"

Answer like:

### Optum

**Test Pattern:** ...

--------------------------------------------------
IMPORTANT
--------------------------------------------------

Preserve the actual information from the retrieved
placement records.

Do not change company names.

Do not change CTC values.

Do not invent missing values.

Do not merge two different records just because
the company name is the same.

--------------------------------------------------
CONTEXT
--------------------------------------------------

{context}

--------------------------------------------------
USER QUESTION
--------------------------------------------------

{query}

--------------------------------------------------
FINAL ANSWER
--------------------------------------------------
"""


    # Generate answer

    try:

        answer_response = client.models.generate_content(

            model="gemini-3.1-flash-lite",

            contents=prompt

        )

        answer = answer_response.text

    except Exception as e:

        print("Gemini Generation Error:", e)

        return jsonify({

            "error": "Unable to generate answer"

        }), 500


    
    # Save user message

    current_time = datetime.utcnow()


    messages_collection.insert_one({

        "conversation_id": conversation_id,

        "user_email": email,

        "role": "user",

        "content": query,

        "created_at": current_time

    })


    
    # Update chat title using first question

    message_count = messages_collection.count_documents({

        "conversation_id": conversation_id,

        "role": "user"

    })


    if message_count == 1:

        chat_title = query.strip()


        # Keep title short

        if len(chat_title) > 40:

            chat_title = (
                chat_title[:40] + "..."
            )


        conversations_collection.update_one(

            {
                "_id": ObjectId(conversation_id)
            },

            {
                "$set": {

                    "title": chat_title,

                    "updated_at": datetime.utcnow()

                }
            }

        )

    else:

        conversations_collection.update_one(

            {
                "_id": ObjectId(conversation_id)
            },

            {
                "$set": {

                    "updated_at": datetime.utcnow()

                }
            }

        )


    
    # Save AI message

    messages_collection.insert_one({

        "conversation_id": conversation_id,

        "user_email": email,

        "role": "assistant",

        "content": answer,

        "created_at": datetime.utcnow()

    })


    
    # Update conversation

    conversations_collection.update_one(

        {
            "_id": ObjectId(conversation_id)
        },

        {
            "$set": {

                "updated_at": datetime.utcnow()

            }
        }

    )


    
    # Return answer

    return jsonify({

        "query": query,

        "answer": answer,

        "conversation_id": conversation_id

    }), 200



# 14. Run Flask server

if __name__ == "__main__":

    app.run(

        debug=True,

        port=5000

    )
