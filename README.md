# Empório da Música — AI Customer Service Agent

A Python-based AI customer service agent developed as a technical challenge for the AI Engineer position at Artefact.

The agent assists customers of Empório da Música, a fictional musical instrument store, by answering questions about products, orders, store information and customer service policies.

## Features

- **Product search:** Search available instruments by name, description and maximum price.
- **Order tracking:** Retrieve order information after validating the customer's registered email.
- **Store policies:** Answer questions using information extracted from the store's official PDF policy manual.
- **Natural conversations:** Maintain conversation context during a CLI session.
- **Out-of-scope handling:** Politely redirect requests unrelated to the store's business.

## Tech Stack

- Python 3.12
- Groq API
- OpenAI GPT-OSS 20B model
- Function Calling
- Pandas
- PyPDF
- python-dotenv
- Pytest

## Project Structure

```text
artefact-ai-agent/
├── data/
│   ├── categories.csv
│   ├── customers.csv
│   ├── order_items.csv
│   ├── orders.csv
│   ├── products.csv
│   ├── promotions.csv
│   └── políticas_da_loja.pdf
├── src/
│   ├── __init__.py
│   ├── agent.py
│   └── tools.py
├── examples/
│   ├── 01_product_search.md
│   ├── 02_store_information.md
│   ├── 03_return_policy.md
│   ├── 04_order_tracking.md
│   └── 05_out_of_scope.md
├── tests/
│   └── test_tools.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd artefact-ai-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Get an API key at https://console.groq.com/keys.

### 5. Run the agent

```bash
python src/agent.py
```

The agent will start an interactive terminal session.

Type `sair` to end the conversation.

## Architecture and Technical Decisions

### Agent Approach

The solution uses an LLM-based agent with Function Calling.

Instead of relying exclusively on the model's internal knowledge, the agent can invoke Python functions to retrieve information from the store's data sources.

Three tools are available:

- `search_products`: searches the product catalog and checks stock availability.
- `get_order_status`: retrieves order information after email validation.
- `get_store_policies`: extracts relevant information from the store's PDF policy manual.

### Model and Provider

The project uses the GPT-OSS 20B model through Groq's API.

This approach provides access to an LLM without requiring a paid model subscription during development, subject to the provider's usage limits and availability.

### Data Processing

Pandas is used to read and filter CSV files.

PyPDF extracts text from the store's policy manual. A simple keyword-based retrieval strategy selects relevant sections before sending them to the model.

### Conversation Context

Conversation history is maintained in memory during the CLI session. No persistent database is required for this prototype.

### Prompt Strategy

The system prompt defines the store assistant's personality, communication style and business rules.

It also instructs the model to consult available tools rather than invent product prices, stock information or order details.

## Running Tests

Execute the automated tests with:

```bash
python -m pytest -v
```

The tests cover product searches, email validation and order retrieval.

## Example Conversations

Five example interactions are available in the `examples/` directory:

1. Product search.
2. Store information.
3. Return policy.
4. Order tracking.
5. Out-of-scope requests.

## Known Limitations

- The prototype uses a command-line interface rather than a web application.
- Conversation history is not persisted between sessions.
- Policy retrieval uses keyword matching rather than a vector database or semantic search.
- Order validation relies on the registered email and does not implement full authentication.
- The solution depends on the external LLM provider and its API availability.
- The automated test suite currently focuses on the core data tools.

### Future Improvements

With more development time, I would consider:

- Adding a FastAPI interface.
- Implementing stronger customer authentication.
- Improving policy retrieval with embeddings and semantic search.
- Expanding automated tests to cover agent behavior and tool calling.
- Adding structured logging and error handling.

## AI-Assisted Development

ChatGPT was used as a development assistant throughout the project, supporting architecture decisions, code implementation, debugging, testing and documentation.

All implementation decisions were reviewed during development, with a focus on understanding the code and keeping the solution simple, maintainable and appropriate for the challenge.

---

Developed as part of the Artefact AI Engineer Technical Challenge.

**Empório da Música — Sua música começa aqui.**