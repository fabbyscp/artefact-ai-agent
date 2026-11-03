from src.tools import search_products, get_order_status


def test_search_products():
    products = search_products("Yamaha", max_price=1000)

    assert len(products) > 0
    assert all(p["price_brl"] <= 1000 for p in products)
    assert all(p["stock_quantity"] > 0 for p in products)


def test_order_requires_valid_email():
    result = get_order_status(1, "email@errado.com")

    assert "error" in result


def test_order_with_valid_email():
    result = get_order_status(1, "pedro.oliveira@jmail.com")

    assert result["status"] == "delivered"