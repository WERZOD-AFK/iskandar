from aiogram import F, Router
from aiogram.types import Message

from config import settings
from utils.api_client import ApiError, api_client

router = Router(name="orders")

STATUS_LABELS = {
    "pending": "🟡 Kutilmoqda",
    "paid": "🔵 To'lov qilindi",
    "processing": "🟣 Qayta ishlanmoqda",
    "completed": "🟢 Yakunlandi",
    "cancelled": "🔴 Bekor qilindi",
}


@router.message(F.text == "📦 Buyurtmalarim")
async def my_orders(message: Message) -> None:
    user = message.from_user
    assert user is not None
    try:
        orders = await api_client.list_orders(user.id, limit=10)
    except ApiError:
        await message.answer("Buyurtmalarni yuklab bo'lmadi, birozdan so'ng qayta urinib ko'ring.")
        return

    if not orders:
        await message.answer(
            "Sizda hali buyurtmalar yo'q.\n"
            "⭐ Stars sotib olish uchun pastdagi Mini App tugmasidan foydalaning."
        )
        return

    lines = ["<b>📦 So'nggi buyurtmalaringiz</b>\n"]
    for o in orders:
        status = STATUS_LABELS.get(o["status"], o["status"])
        lines.append(
            f"#{o['id']} — ⭐ {o['stars_amount']} — {status}\n"
            f"<i>{o['created_at']}</i>"
        )
    await message.answer("\n\n".join(lines))


@router.message(F.text == "👤 Profil")
async def profile(message: Message) -> None:
    user = message.from_user
    assert user is not None
    try:
        u = await api_client.get_user(user.id)
    except ApiError:
        await message.answer("Profil ma'lumotlarini yuklab bo'lmadi.")
        return

    await message.answer(
        f"👤 <b>{u['full_name']}</b>\n"
        f"Username: @{u.get('username') or '—'}\n\n"
        f"⭐ Jami sotib olingan: {u['total_stars_purchased']}\n"
        f"📦 Buyurtmalar: {u['orders_count']}\n"
        f"🎁 Bonus balans: {u['bonus_balance']}"
    )


@router.message(F.text == "👥 Referal")
async def referral(message: Message) -> None:
    user = message.from_user
    assert user is not None
    bot_username = (await message.bot.get_me()).username
    link = f"https://t.me/{bot_username}?start=ref_{user.id}"
    bonus_note = (
        f"\n\nDo'stingiz Stars sotib olsa, siz {settings.referral_bonus_stars} ⭐ bonus olasiz."
        if settings.referral_bonus_stars > 0
        else ""
    )
    await message.answer(
        f"👥 <b>Sizning referal havolangiz:</b>\n<code>{link}</code>{bonus_note}"
    )
