# WeakLlama Security Testing Framework

> **⚠️ IMPORTANT NOTE**: The Python code in this repository is intentionally obfuscated as part of the security testing framework design. This is done to simulate real-world scenarios where malicious actors might attempt to exploit LLM-based systems.

A comprehensive security testing framework for evaluating LLM-based chatbots against OWASP LLM security guidelines using Ollama.

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed locally
- Required Python packages (install via `pip install -r requirements.txt`)

## Setup

1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Start Ollama service locally 
3. Clone this repository:
   ```bash
   git clone https://github.com/ohmyilya/WeakLlama.git
   cd WeakLlama
   pip install -r requirements.txt
   ```

## How It Works

### Test Cases Generator (`test_cases.py`)

The `test_cases.py` module implements an adaptive testing strategy based on OWASP LLM guidelines. It:

- Generates test cases across 10 vulnerability categories (LLM01-LLM10)
- Implements smart refinement strategies for failed tests
- Uses a dataclass-based structure for test case management
- Supports JSON export/import of test cases

Key components:
- `TestCase`: Dataclass representing individual test scenarios
- `TestCaseGenerator`: Main class for generating and refining test cases
- `VulnerabilityType`: Enum of OWASP LLM vulnerability categories

### Test Runner (`run_tests.py`)

The `run_tests.py` module executes the test cases against your Ollama instance. Features:

- Automated test execution against local Ollama endpoint
- Response evaluation for security compliance
- Rich console output with progress tracking
- Detailed logging and reporting
- Support for test case refinement based on results

Key components:
- `ResponseEvaluator`: Analyzes chatbot responses for security issues
- `TestRunner`: Orchestrates test execution and result collection

## Usage

1. Generate test cases:
   ```bash
   python test_cases.py
   ```
   This will create `test_cases.json` with the initial test suite.

2. Run the test suite:
   ```bash
   python run_tests.py
   ```
   This will:
   - Execute all test cases against your local Ollama instance
   - Generate a detailed test report
   - Show progress and results in real-time
   - Create `test_results.json` with detailed findings

## Configuration

The framework uses the local Ollama instance. 
NB. The model is set to **llama2 by default**.

## Logging

- Test generation logs: `test_generation.log`
- Test execution logs: `red_team_test.log`
