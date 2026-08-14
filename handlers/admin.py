"""
Bot ichidagi minimal admin komandalar. To'liq admin panel (statistika
grafiklari, mahsulot boshqaruvi, foydalanuvchi qidiruvi) alohida veb
Admin Panel'da bo'lishi kerak — bu yerda faqat tezkor komandalar bor.
"""
import asyncio

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from config import settings
from utils.api_client import api_client

router = Router(name="admin")


def is_admin(user_id: int) -> bool:
    return user_id in settings.admin_ids


@router.message(Command("stats"))
async def stats(message: Message) -> None:
    if not message.from_user or not is_admin(message.from_user.id):
        return
    data = await api_client._request("GET", "/api/admin/stats")  # noqa: SLF001
    await message.answer(
        "📊 <b>Statistika</b>\n\n"
        f"👥 Foydalanuvchilar: {data['users_count']}\n"
        f"📦 Buyurtmalar: {data['orders_count']}\n"
        f"⭐ Sotilgan Stars: {data['stars_sold']}\n"
        f"💰 Tushum: {data['revenue']}"
    )


class BroadcastForm(StatesGroup):
    waiting_for_text = State()


@router.message(Command("broadcast"))
async def broadcast_start(message: Message, state: FSMContext) -> None:
    if not message.from_user or not is_admin(message.from_user.id):
        return
    await state.set_state(BroadcastForm.waiting_for_text)
    await message.answer("Yubormoqchi bo'lgan xabar matnini yozing:")


@router.message(BroadcastForm.waiting_for_text)
async def broadcast_send(message: Message, state: FSMContext, bot: Bot) -> None:
    await state.clear()
    text = message.text or ""
    user_ids = await api_client._request("GET", "/api/admin/user-ids")  # noqa: SLF001

    sent, failed = 0, 0
    await message.answer(f"Yuborilmoqda: {len(user_ids)} foydalanuvchiga...")
    for uid in user_ids:
        try:
            await bot.send_message(uid, text)
            sent += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.05)  # Telegram rate limitiga tushib qolmaslik uchun

    await message.answer(f"✅ Yuborildi: {sent} | ❌ Xato: {failed}")


@router.message(Command("block"))
async def block_user(message: Message) -> None:
    if not message.from_user or not is_admin(message.from_user.id):
        return
    parts = (message.text or "").split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Foydalanish: /block <telegram_id>")
        return
    target_id = int(parts[1])
    await api_client._request("POST", f"/api/admin/users/{target_id}/block")  # noqa: SLF001
    await message.answer(f"🚫 Foydalanuvchi {target_id} bloklandi.")
