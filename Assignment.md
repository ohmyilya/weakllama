# WeakLlama Automated Red-Teaming

Build a **small, automated “red-teaming” tool** for the [**WeakLlama Chatbot App**](./README.md), showcasing a basic **agentic** or iterative strategy. We encourage referencing **OWASP Top 10** (for LLM) or similar security frameworks when designing these **test cases**. The objective is to let your script adapt or refine test cases if initial attempts fail to expose vulnerabilities.

---

## Overview

1. **Generate adversarial test cases** (drawn from the OWASP Top 10 for LLM or other known vulnerabilities) that aim to break or stress-test the chatbot.  
2. **Automate** sending these test cases to the chatbot.  
3. **Refine** test cases (minimally) if the chatbot remains compliant.  
4. **Evaluate** responses with a simple pass/fail “judge.”  
5. **Produce** a short **report** or **log** of test results.

### Why Agentic?

Instead of submitting static test cases, you **slightly refine** them after a “pass” to see if repeated or modified attempts might reveal new vulnerabilities or non-compliant behavior.

Use of some agentic framework is highly encouraged but not mandatory for this task.
You can use:
  - Existing **agentic frameworks** (e.g., [Langgraph](https://github.com/langchain-ai/langgraph), [smolagents](https://github.com/huggingface/smolagents), [crewai](https://github.com/crewAIInc/crewAI) etc), **or**  
  - Your **own custom agent** that orchestrates prompt generation, refinement, and evaluation. 

---

## Requirements

1. **Adversarial Test Cases & Refinement**  
   - Define **3–5 test cases** based on **OWASP Top 10** or similar guidelines for LLM security. Bonus points for automating the generation part as well. 
     - Examples could include prompt injection, data exfiltration (admin-only info), brand/policy violations, etc.  
   - Implement **basic agentic logic**: If the chatbot’s response is “safe,” refine the test case to push boundaries further.

2. **Automation Script or Mini Library**  
   - A Python script (or minimal library) that:
     1. Loads or contains your **base test cases**.  
     2. Iterates over each test case:
        - Sends it to the WeakLlama Chatbot (`POST /api/chat`).  
        - Evaluates the response using a simple “judge” function.  
        - (Optionally) Refines the test case if it didn’t cause a violation.  
     3. **Logs** all requests & responses.

3. **Evaluation (“Judge”)**  
   - Could be:
     - **Rules-based** (search for banned keywords or specific patterns in the response).  
     - **LLM-based** (if you have a local or small model or openai key) classifying the response as safe/unsafe.  
   - Assign a **pass/fail** verdict and a brief reason.

4. **Report / Summary**  
   - Output a **log** (JSON, Markdown, or console output) showing:
     - The **test case** / refined version(s).  
     - The chatbot’s response.  
     - The verdict (pass/fail).  
     - The reason (e.g., “Contains disallowed content” or “Requested admin data without token”).

---

## Deliverables

1. **Code Repository** (or zipped folder)  
   - **`README.md`** with:
     - Setup/run instructions.  
     - A short explanation of your approach of test case generation (using OWASP Top 10 or similar), agentic refinement and report generation.
2. **Log/Report**  
   - **Evidence** of the tests, including final output with test cases, responses, and pass/fail verdicts.

---

## What We’re Looking For

1. Well-structured, maintainable code. Sensible approach to building a modular, extensible test harness.

2. Understanding common LLM weaknesses (prompt injection, policy bypass, data leakage, etc.). Practical test prompts to expose them.

3. Automation of testing cycles, refining prompts, adaptive responses, logging of results, etc.

This is **open-ended**, feel free to add unique scoring methods, custom report formats, or innovative ways to red-team the chatbot. 


---


We look forward to seeing how you approach **automated red teaming** with **agentic systems** in the context of the WeakLlama Chatbot. This challenge should showcase your ability to **think** about LLM security and **engineer** creative solutions.

**Good luck**, and we hope you have fun building this project!
