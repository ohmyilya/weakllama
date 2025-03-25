# WeakLlama

This is a very naive chatbot app that simulates an application that needs to be pen-tested and for which we will create a framework to do automated pen testing.

## High-Level Description
The WeakLlama Support Chatbot is a customer-facing web service that uses an LLM to answer user queries about WeakLlama Inc.’s products and services. The chatbot is intended to:

- Provide support articles, troubleshooting steps, and company policy information for WeakLlama’s offerings.
- Enforce brand guidelines:
    - No hateful/offensive language.
    - No revealing of internal or confidential information unless authorized.
- Follow compliance rules:
    - Refrain from providing direct financial/legal advice.
    - Provide disclaimers when users seek such advice.

## Intended Behavior

### User Queries

Users ask questions like “How do I reset my WeakLlama password?” or “What is WeakLlama’s refund policy?”
The backend calls gpt4o with a system prompt that enforces WeakLlama’s brand and compliance rules.
The user receives a “safe” and brand-compliant response.

### Proactive Disclaimers

If the user requests legal, financial, or medical advice, the system responds with an appropriate disclaimer (e.g., “I am not a licensed [professional]. Please consult a professional.”).
It avoids generating disallowed content (hate speech, violent threats, etc.).

### Partial Auth

There is an “admin” user role that can access proprietary data like product roadmaps, financial details, etc.
This role is protected by a simple token-based authentication (e.g., Authorization: Bearer <token>).
Non-admin users are restricted to general help content only.

## Running the app

To run:

0. Create conda env (optional but recommended, you could use any other env framework)

```
conda env create -f environment.yml
conda activate wllama 
```

1. Install dependencies (if you skipped step 0) :
  
```
pip install -r requirements.txt
```

2. Ensure you have 'faq_document.txt' in the same directory (or adjust the path).
3. Set environment variables:
```
export GPT4O_API_KEY="your-real-key"
export WEAKLLAMA_ADMIN_SECRET="some-admin-token"
```
OR create a ```.env``` file and set them in that file.

If you do not have OPENAI API KEY, feel free to modify code to use a local model instead (some qwen or mistral variant should work)

4. Start server:
```
uvicorn app:app --reload

$ uvicorn app:app --reload
INFO:     Will watch for changes in these directories: ['/home/ydatta/Workspace/WeakLlama']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [191714] using StatReload
INFO:     Started server process [191716]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:39252 - "GET / HTTP/1.1" 200 OK
INFO:     127.0.0.1:39862 - "GET / HTTP/1.1" 200 OK

```

Then from another terminal you can curl to make sure server is up

```
$ curl http://127.0.0.1:8000/
{"message":"WeakLlama Support Chatbot is running."}
```

### Sample request/response

You can ask questions, and you should get some response

```
$ curl -X POST "http://127.0.0.1:8000/api/chat"   -H "Content-Type: application/json"   -d '{
    "prompt": "How do I reset my WeakLlama password?",
    "userRole": "user"
  }'

{"response":"To reset your WeakLlama password, navigate to 'Settings' > 'Account' and click 'Reset Password'. A password reset link will be sent to your registered email."}
```

Some requests will be refused

```
$ curl -X POST "http://127.0.0.1:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "adasfdsfdsfd",
    "userRole": "user"
  }'

{"response":"I'm sorry, but I can't process that query. Please try again with more detail"}
```

There are admin query possible as well, which should work if authToken equals ```WEAKLLAMA_ADMIN_SECRET```

```
$ curl -X POST "http://127.0.0.1:8000/api/chat"   -H "Content-Type: application/json"   -d '{
    "prompt": "What is in the WeakLlama Product Roadmap?",
    "userRole": "admin",
    "authToken": "secret"
  }'

{"response":"The WeakLlama Product Roadmap includes the following:\n\n- Q1: Improve chatbot reliability\n- Q2: Expand to voice-based assistance\n- Q3: Launch new recommendation engine"}
```

If the token does not match, you get 401 UNAUTHORIZED error

```
$ curl -X POST "http://127.0.0.1:8000/api/chat"   -H "Content-Type: application/json"   -d '{
    "prompt": "What is in the WeakLlama Product Roadmap?",
    "userRole": "admin",
    "authToken": "secrset"
  }'

{"detail":"Invalid admin token"}
```
