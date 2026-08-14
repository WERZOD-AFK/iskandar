from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo,
)

from config import settings


def main_menu_kb() -> ReplyKeyboardMarkup:
    """Pastki asosiy menyu — Mini App shu yerdan ochiladi."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⭐ Stars Shop", web_app=WebAppInfo(url=settings.webapp_url))],
            [KeyboardButton(text="📦 Buyurtmalarim"), KeyboardButton(text="👤 Profil")],
            [KeyboardButton(text="👥 Referal"), KeyboardButton(text="💬 Yordam")],
        ],
        resize_keyboard=True,
    )


def open_webapp_inline_kb(text: str = "⭐ Mini App'ni ochish") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, web_app=WebAppInfo(url=settings.webapp_url))]
        ]
    )


def support_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❓ FAQ", callback_data="support:faq")],
            [InlineKeyboardButton(text="✍️ Savol yuborish", callback_data="support:ask")],
            [InlineKeyboardButton(text="👨‍💻 Administrator", url=f"https://t.me/{settings.support_username}")],
        ]
    )


def admin_reply_kb(order_id: int) -> InlineKeyboardMarkup:
    """Admin support ticketga javob berish uchun (admin guruhida ishlatiladi)."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✍️ Javob yozish", callback_data=f"admin:reply:{order_id}")]
        ]
    )
