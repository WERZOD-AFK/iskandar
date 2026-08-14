"""
Telegram Stars to'lovlari.

Muhim: Stars uchun currency har doim "XTR" va provider_token bo'sh
string bo'lishi kerak (Telegram Bot API talabi). Bot to'lovni
"muvaffaqiyatli" deb HECH QACHON o'zi hal qilmaydi — faqat
successful_payment eventi kelgandan keyin, backend orqali order
statusini yangilaydi. Backendning o'zi ham Telegram bilan
getStarTransactions orqali tekshirib turishi tavsiya etiladi
(chargeback / firibgarlikning oldini olish uchun).
"""
import logging

from aiogram import F, Router
from aiogram.types import (
    CallbackQuery,
    LabeledPrice,
    Message,
    PreCheckoutQuery,
)

from utils.api_client import ApiError, api_client

logger = logging.getLogger(__name__)
router = Router(name="payments")


async def send_stars_invoice(message_or_query: Message | CallbackQuery, order_id: int, title: str,
                              description: str, stars_amount: int) -> None:
    bot = message_or_query.bot
    chat_id = (
        message_or_query.chat.id
        if isinstance(message_or_query, Message)
        else message_or_query.message.chat.id
    )
    await bot.send_invoice(
        chat_id=chat_id,
        title=title,
        description=description,
        payload=f"order:{order_id}",
        provider_token="",  # Stars uchun har doim bo'sh
        currency="XTR",
        prices=[LabeledPrice(label=title, amount=stars_amount)],
    )


@router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery) -> None:
    """To'lov tasdiqlanishidan oldin oxirgi tekshiruv (10 soniya ichida javob berish shart)."""
    payload = pre_checkout_query.invoice_payload
    if not payload.startswith("order:"):
        await pre_checkout_query.answer(ok=False, error_message="Noto'g'ri buyurtma.")
        return

    order_id = int(payload.removeprefix("order:"))
    try:
        order = await api_client.get_order(order_id)
    except ApiError:
        await pre_checkout_query.answer(ok=False, error_message="Buyurtma topilmadi.")
        return

    if order["status"] != "pending":
        await pre_checkout_query.answer(ok=False, error_message="Bu buyurtma allaqachon qayta ishlangan.")
        return

    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message) -> None:
    payment = message.successful_payment
    assert payment is not None
    order_id = int(payment.invoice_payload.removeprefix("order:"))

    try:
        order = await api_client.mark_order_paid(
            order_id=order_id,
            telegram_payment_charge_id=payment.telegram_payment_charge_id,
        )
    except ApiError:
        logger.exception("Order #%s to'lovini backendda belgilab bo'lmadi", order_id)
        await message.answer(
            "To'lovingiz qabul qilindi, lekin buyurtmani yangilashda muammo yuz berdi. "
            "Iltimos, /support orqali murojaat qiling va buyurtma raqamini (#%s) ko'rsating." % order_id
        )
        return

    await message.answer(
        f"✅ <b>To'lov muvaffaqiyatli!</b>\n\n"
        f"Buyurtma: #{order['id']}\n"
        f"⭐ Miqdor: {order['stars_amount']}\n\n"
        f"Rahmat! Stars hisobingizga tez orada yetkaziladi."
    )
