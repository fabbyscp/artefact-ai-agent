import os
import json
from dotenv import load_dotenv
from groq import Groq

from tools import search_products, get_order_status, get_store_policies

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "openai/gpt-oss-20b"

SYSTEM_PROMPT = """
You are the virtual assistant of Empório da Música,
a musical instrument store in Campo Grande, Brazil.

Your personality:
- Friendly, welcoming and professional.
- Speak naturally in Brazilian Portuguese.
- Be concise and helpful.

Rules:
- Only provide product prices and availability after searching the catalog.
- Always check order information using the order tool.
- Consult store policies before answering policy questions.
- Never invent information.
- The store sells musical instruments only, not accessories.
- For unrelated questions, politely redirect the customer.
- Protect customer information. Never reveal order details
  without validating the customer's email.
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search available musical instruments by name or description and optional maximum price.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "max_price": {"type": "number"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Check an order using its ID and customer email.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "integer"},
                    "email": {"type": "string"}
                },
                "required": ["order_id", "email"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_store_policies",
            "description": "Retrieve the store policies from the official PDF.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The specific policy topic to search for."
                    }
                },
                "required": ["query"]
            }
        }
    }
]

FUNCTIONS = {
    "search_products": search_products,
    "get_order_status": get_order_status,
    "get_store_policies": get_store_policies
}


def chat(message, history=None):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    messages.extend(history or [])
    messages.append({"role": "user", "content": message})

    for _ in range(5):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.2
        )

        assistant_message = response.choices[0].message
        messages.append(assistant_message)

        if not assistant_message.tool_calls:
            return assistant_message.content

        for tool_call in assistant_message.tool_calls:
            name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            result = FUNCTIONS[name](**arguments)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, ensure_ascii=False, default=str)
            })

    return "Não consegui concluir sua solicitação. Pode tentar novamente?"


if __name__ == "__main__":
    print("\n🎸 EMPÓRIO DA MÚSICA")
    print("Digite 'sair' para encerrar.\n")

    history = []

    while True:
        message = input("Você: ")

        if message.lower() == "sair":
            break

        try:
            answer = chat(message, history)
            print(f"\nAtendente: {answer}\n")

            history.extend([
                {"role": "user", "content": message},
                {"role": "assistant", "content": answer}
            ])

        except Exception as error:
            print(f"Erro: {error}")