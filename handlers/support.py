from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from config import settings
from utils.api_client import ApiError, api_client

router = Router(name="support")

FAQ_TEXT = (
    "❓ <b>Tez-tez so'raladigan savollar</b>\n\n"
    "1. <b>Stars qachon yetkaziladi?</b>\nTo'lov tasdiqlangach, odatda bir necha daqiqada.\n\n"
    "2. <b>To'lov qaytarilishi mumkinmi?</b>\nMuammo bo'lsa, administratorga murojaat qiling.\n\n"
    "3. <b>Referal bonusi qanday ishlaydi?</b>\n👥 Referal bo'limidan havolangizni oling va do'stlaringizga ulashing."
)


class SupportForm(StatesGroup):
    waiting_for_question = State()


@router.callback_query(F.data == "support:faq")
async def show_faq(callback: CallbackQuery) -> None:
    await callback.message.answer(FAQ_TEXT)
    await callback.answer()


@router.callback_query(F.data == "support:ask")
async def ask_question_start(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(SupportForm.waiting_for_question)
    await callback.message.answer("Savolingizni yozib yuboring, admin tez orada javob beradi 👇")
    await callback.answer()


@router.message(StateFilter(SupportForm.waiting_for_question))
async def ask_question_receive(message: Message, state: FSMContext) -> None:
    user = message.from_user
    assert user is not None
    await state.clear()

    try:
        await api_client.create_support_ticket(tg_user_id=user.id, message=message.text or "")
    except ApiError:
        await message.answer("Xabaringizni yuborishda xatolik yuz berdi, birozdan so'ng qayta urinib ko'ring.")
        return

    await message.answer("✅ Xabaringiz qabul qilindi. Admin tez orada javob beradi.")

    for admin_id in settings.admin_ids:
        try:
            await message.bot.send_message(
                admin_id,
                f"💬 <b>Yangi savol</b>\n"
                f"Foydalanuvchi: {user.full_name} (@{user.username or '—'}, id: {user.id})\n\n"
                f"{message.text}",
            )
        except Exception:
            continue
