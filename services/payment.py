import uuid
from config import settings

# Конфигурация ЮKassa (только если не мок-режим)
if not settings.MOCK_PAYMENTS:
    from yookassa import Configuration, Payment
    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


def create_payment(amount: int, description: str, return_url: str = None) -> dict:
    """
    Создать платёж в ЮKassa (или мок-платёж)

    Args:
        amount: Сумма в рублях
        description: Описание платежа
        return_url: URL возврата после оплаты (опционально)

    Returns:
        dict с данными платежа (id, confirmation_url)
    """
    # МОК-РЕЖИМ: все платежи проходят автоматически
    if settings.MOCK_PAYMENTS:
        mock_payment_id = f"mock_{uuid.uuid4()}"
        return {
            "payment_id": mock_payment_id,
            "confirmation_url": None,  # В моке не нужен URL
            "status": "succeeded"
        }

    # Реальный платёж через ЮKassa
    idempotence_key = str(uuid.uuid4())

    payment_data = {
        "amount": {
            "value": f"{amount}.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": return_url or "https://t.me/your_bot"
        },
        "capture": True,
        "description": description
    }

    payment = Payment.create(payment_data, idempotence_key)

    return {
        "payment_id": payment.id,
        "confirmation_url": payment.confirmation.confirmation_url,
        "status": payment.status
    }


def check_payment(payment_id: str) -> dict:
    """
    Проверить статус платежа

    Args:
        payment_id: ID платежа в ЮKassa

    Returns:
        dict с данными платежа (status, paid)
    """
    # МОК-РЕЖИМ: все платежи всегда успешны
    if settings.MOCK_PAYMENTS or payment_id.startswith("mock_"):
        return {
            "status": "succeeded",
            "paid": True,
            "amount": 0  # В моке сумма не важна
        }

    # Реальная проверка через ЮKassa
    payment = Payment.find_one(payment_id)

    return {
        "status": payment.status,
        "paid": payment.paid,
        "amount": float(payment.amount.value) if payment.amount else 0
    }
