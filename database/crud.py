from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User, Product, Order, OrderStatus
from datetime import datetime


async def get_or_create_user(session: AsyncSession, telegram_id: int, username: str = None, first_name: str = None) -> User:
    """Получить или создать пользователя"""
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

    return user


async def get_product_by_key(session: AsyncSession, product_key: str) -> Product | None:
    """Получить товар по ключу"""
    result = await session.execute(
        select(Product).where(Product.product_key == product_key, Product.is_active == True)
    )
    return result.scalar_one_or_none()


async def get_all_active_products(session: AsyncSession) -> list[Product]:
    """Получить все активные товары"""
    result = await session.execute(
        select(Product).where(Product.is_active == True)
    )
    return list(result.scalars().all())


async def create_order(session: AsyncSession, user_id: int, product_id: int, amount: int, payment_id: str = None) -> Order:
    """Создать заказ"""
    order = Order(
        user_id=user_id,
        product_id=product_id,
        amount=amount,
        payment_id=payment_id,
        status=OrderStatus.PENDING
    )
    session.add(order)
    await session.commit()
    await session.refresh(order)
    return order


async def update_order_paid(session: AsyncSession, payment_id: str) -> Order | None:
    """Обновить статус заказа на оплачен"""
    result = await session.execute(
        select(Order).where(Order.payment_id == payment_id)
    )
    order = result.scalar_one_or_none()

    if order:
        order.status = OrderStatus.PAID
        order.paid_at = datetime.utcnow()
        await session.commit()
        await session.refresh(order)

    return order


async def get_user_orders(session: AsyncSession, telegram_id: int) -> list[Order]:
    """Получить заказы пользователя"""
    result = await session.execute(
        select(Order).join(User).where(User.telegram_id == telegram_id, Order.status == OrderStatus.PAID)
    )
    return list(result.scalars().all())
