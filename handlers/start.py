import logging

from aiogram import F, Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message

from keyboards.main import main_menu_kb
from utils.api_client import ApiError, api_client

logger = logging.getLogger(__name__)
router = Router(name="start")


@router.message(CommandStart(deep_link=True))
async def start_with_ref(message: Message, command: CommandObject) -> None:
    """/start ref_12345 — referral orqali kirgan foydalanuvchi."""
    ref_code = None
    payload = command.args or ""
    if payload.startswith("ref_"):
        ref_code = payload.removeprefix("ref_")

    await _register_and_greet(message, ref_code)


@router.message(CommandStart())
async def start_plain(message: Message) -> None:
    await _register_and_greet(message, ref_code=None)


async def _register_and_greet(message: Message, ref_code: str | None) -> None:
    user = message.from_user
    assert user is not None

    try:
        await api_client.upsert_user(
            tg_user_id=user.id,
            username=user.username,
            full_name=user.full_name,
            ref_code=ref_code,
        )
    except ApiError:
        logger.exception("upsert_user muvaffaqiyatsiz, foydalanuvchi baribir kutib olinadi")

    await message.answer(
        f"Assalomu alaykum, {user.first_name}! 👋\n\n"
        "⭐ <b>Stars Shop</b>'ga xush kelibsiz.\n"
        "Pastdagi tugma orqali Stars sotib olishingiz, buyurtmalaringizni "
        "kuzatishingiz va bonuslardan foydalanishingiz mumkin.",
        reply_markup=main_menu_kb(),
    )


@router.message(F.text == "💬 Yordam")
async def help_button(message: Message) -> None:
    from keyboards.main import support_kb
    await message.answer("Qanday yordam bera olamiz?", reply_markup=support_kb())
