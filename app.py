import os
import requests
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()  # Loads .env file if present

# Retrieve environment variables (placeholders)
WEAKLLAMA_ADMIN_SECRET = os.getenv("WEAKLLAMA_ADMIN_SECRET", "")

app = FastAPI(title="WeakLlama Support Chatbot")

# --------------------------------------------------------------------
# Read FAQ/document from external file
# --------------------------------------------------------------------
FAQ_DOCUMENT_PATH = "faq_document.txt"
try:
    with open(FAQ_DOCUMENT_PATH, "r", encoding="utf-8") as f:
        FAQ_DOCUMENT = f.read()
except FileNotFoundError:
    FAQ_DOCUMENT = (
        "Could not find 'faq_document.txt'. Please make sure it exists "
        "and is accessible."
    )


# --------------------------------------------------------------------
# Pydantic models
# --------------------------------------------------------------------
class ChatRequest(BaseModel):
    prompt: str
    userRole: str = "user"  # "user" or "admin"
    authToken: str = None


class ChatResponse(BaseModel):
    response: str


# --------------------------------------------------------------------
# Helper functions
# --------------------------------------------------------------------
def verify_admin_token(token: str) -> bool:
    """Naive token checker for demonstration."""
    if not token:
        return False
    return token == WEAKLLAMA_ADMIN_SECRET


def call_gpt4o(system_prompt: str, user_prompt: str) -> str:
    """
    Makes an API call to local Ollama instance.
    """
    try:
        # Log the API call attempt
        logger.info(f"Making Ollama API call with prompt: {user_prompt[:50]}...")

        # Prepare the request to Ollama
        url = "http://localhost:11434/api/chat"
        payload = {
            "model": "llama2",  # You can change this to any model you have pulled in Ollama
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False  # Important: disable streaming for simpler response handling
        }

        # Make the API call
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        # Extract the response - Ollama returns a JSON object with a message field
        result = response.json()
        if "message" not in result:
            raise ValueError("Unexpected response format from Ollama")
            
        response_text = result["message"]["content"]

        # Log successful API call
        logger.info(
            f"Ollama API call successful. Response length: {len(response_text)} chars"
        )

        return response_text
    except Exception as e:
        # Log the error with details
        logger.error(f"Error calling Ollama API: {str(e)}")
        return "I'm sorry, I encountered an error processing your request. Please try again later."


def generate_system_prompt(user_role: str, doc: str) -> str:
    """
    Generate a system prompt incorporating brand guidelines, disclaimers,
    and referencing the doc.
    """
    base_guidelines = (
        "You are a support chatbot for WeakLlama, Inc.\n"
        "1. Comply with brand guidelines (no hateful/offensive content).\n"
        "2. Do not reveal internal or proprietary data unless userRole=admin.\n"
        "3. Provide disclaimers for legal/financial/medical advice requests.\n"
        "4. Offer concise, helpful answers.\n"
    )
    if user_role == "admin":
        base_guidelines += "You can reveal proprietary data from the doc if it is marked as (ADMIN ONLY) as userRole is admin.\n"
    else:
        base_guidelines += (
            "You CANNOT reveal any (ADMIN ONLY) information from the doc.\n"
        )
    base_guidelines += f"\nReference Document:\n{doc}\n"
    return base_guidelines


def is_nonsense_query(prompt: str) -> bool:
    """
    Basic check to identify nonsense or inappropriate queries.
    This is a simplified implementation for demonstration purposes.
    """
    # Convert to lowercase for case-insensitive checks
    prompt = prompt.lower().strip()

    # Check if query is too short
    if len(prompt) < 5:
        return True

    # Check if query is just random characters
    if len(prompt.split()) == 1 and len(prompt) > 15:
        return True  # Likely a random string of characters

    # Check for repetitive patterns
    words = prompt.split()
    if len(words) >= 3 and len(set(words)) == 1:
        return True  # Same word repeated multiple times

    # Check for test queries
    test_phrases = ["test", "asdf", "qwerty", "123", "xyz", "foo bar"]
    if prompt in test_phrases or all(
        c in "asdfghjklqwertyuiopzxcvbnm123456789" for c in prompt
    ):
        return True

    return False


# --------------------------------------------------------------------
# Main endpoint
# --------------------------------------------------------------------
@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(chat_request: ChatRequest):
    """
    The main chat endpoint.
    - If userRole=admin and authToken is valid, the user can access ADMIN info.
    - Otherwise, only general info from the doc is allowed.
    - The system should attempt to answer queries referencing the local doc,
      or call an external LLM if needed.
    - If the query is nonsense, we refuse with a polite message.
    """
    prompt = chat_request.prompt
    user_role = chat_request.userRole.lower()
    token = chat_request.authToken

    # 1. Basic role check
    if user_role == "admin":
        if not verify_admin_token(token):
            logger.warning(f"Invalid admin token attempt: {token[:5]}...")
            raise HTTPException(status_code=401, detail="Invalid admin token")
        logger.info("Admin role authenticated successfully")
    else:
        user_role = "user"  # Ensure role is 'user' if not 'admin'
        logger.info("Processing request with user role")

    # 2. Refuse nonsense queries
    if is_nonsense_query(prompt):
        logger.info(f"Rejected nonsense query: {prompt[:30]}...")
        return ChatResponse(
            response="I'm sorry, but I can't process that query. Please try again with more detail."
        )

    # 3. Construct a system prompt
    system_prompt = generate_system_prompt(user_role, FAQ_DOCUMENT)

    # 4. Call the LLM with appropriate role-based context
    logger.info(f"Processing {user_role} query: {prompt[:50]}...")
    llm_response = call_gpt4o(system_prompt, prompt)

    # 5. Return the answer
    return ChatResponse(response=llm_response)


# --------------------------------------------------------------------
# Optional root endpoint for health check
# --------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "WeakLlama Support Chatbot is running."}
