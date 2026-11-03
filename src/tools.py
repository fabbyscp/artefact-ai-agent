import pandas as pd
from pathlib import Path
from pypdf import PdfReader

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_data(filename):
    return pd.read_csv(DATA_DIR / filename)


def search_products(query="", max_price=None):
    products = load_data("desafio_tecnico_ai_eng - products.csv")

    products = products[
        (products["status"] == "active") &
        (products["stock_quantity"] > 0)
    ]

    if query:
        products = products[
            products["name"].str.contains(query, case=False, na=False) |
            products["description"].str.contains(query, case=False, na=False)
        ]

    if max_price is not None:
        products = products[products["price_brl"] <= max_price]

    return products[
        ["name", "price_brl", "stock_quantity", "description"]
    ].to_dict(orient="records")


def get_order_status(order_id, email):
    orders = load_data("desafio_tecnico_ai_eng - orders.csv")
    customers = load_data("desafio_tecnico_ai_eng - customers.csv")

    order = orders[orders["order_id"] == int(order_id)]

    if order.empty:
        return {"error": "Pedido não encontrado."}

    customer_id = order.iloc[0]["customer_id"]
    customer = customers[
        (customers["customer_id"] == customer_id) &
        (customers["email"].str.lower() == email.lower())
    ]

    if customer.empty:
        return {"error": "Não foi possível validar os dados do pedido."}

    return order.drop(columns=["customer_id"]).to_dict(orient="records")[0]


def get_store_policies(query=""):
    pdf_path = DATA_DIR / "políticas_da_loja.pdf"
    reader = PdfReader(str(pdf_path))

    pages = [
        page.extract_text() or ""
        for page in reader.pages
    ]

    keywords = query.lower().split()

    scored = []
    for page in pages:
        score = sum(page.lower().count(word) for word in keywords)
        if score:
            scored.append((score, page))

    relevant = sorted(scored, reverse=True, key=lambda x: x[0])

    return "\n\n".join(page for _, page in relevant[:2])[:4000]