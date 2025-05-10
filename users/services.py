import stripe
from config.settings import STRIPE_SECRET_KEY


stripe.api_key = STRIPE_SECRET_KEY


def create_stripe_product(product_name):
    """Создание продукта"""
    product = stripe.Product.create(name=product_name)
    return product.id


def create_stripe_price(product_id, value):
    """Создание цены"""
    return stripe.Price.create(
        currency="usd",
        unit_amount=int(value * 100),
        product=product_id,
    )


def stripe_session_create(price):
    """Создание сессии"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url
