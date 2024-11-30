import os
from typing import Any

import stripe

from dotenv import load_dotenv

load_dotenv()

STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
stripe.api_key = STRIPE_SECRET_KEY


def stripe_session(amount: int, success_url: str, cancel_url: str) -> tuple[str, str]:
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Товар или услуга',
                },
                'unit_amount': amount,  # Цена в центах (10.00 USD)
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session.id, session.url


def check_stripe_session(session_id):
    session = stripe.checkout.Session.retrieve(session_id)
    print("Status: ", session.payment_status)
    return session.payment_status == 'paid'
