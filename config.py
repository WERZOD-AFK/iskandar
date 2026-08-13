"""
Konfiguratsiya — barcha maxfiy va sozlanadigan qiymatlar
faqat environment variables orqali olinadi. Hech qachon
tokenlarni kodga yozib qo'ymang.
"""
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


def _get_env(name: str, required: bool = True, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if required and not value:
        raise RuntimeError(f"Environment variable '{name}' o'rnatilmagan (.env faylini tekshiring)")
    return value


def _get_int_list(name: str) -> list[int]:
    raw = os.getenv(name, "")
    return [int(x.strip()) for x in raw.split(",") if x.strip().isdigit()]


@dataclass(frozen=True)
class Settings:
    # Bot
    bot_token: str = field(default_factory=lambda: _get_env("BOT_TOKEN"))

    # Mini App
    webapp_url: str = field(default_factory=lambda: _get_env("WEBAPP_URL"))

    # Backend API (FastAPI) — bot bu yerga so'rov yuboradi
    api_base_url: str = field(default_factory=lambda: _get_env("API_BASE_URL"))
    api_internal_secret: str = field(default_factory=lambda: _get_env("API_INTERNAL_SECRET"))

    # Webhook (production uchun; local test uchun polling ishlatiladi)
    use_webhook: bool = field(default_factory=lambda: os.getenv("USE_WEBHOOK", "false").lower() == "true")
    webhook_base_url: str = field(default_factory=lambda: _get_env("WEBHOOK_BASE_URL", required=False, default=""))
    webhook_secret: str = field(default_factory=lambda: _get_env("WEBHOOK_SECRET", required=False, default=""))
    webhook_path: str = "/bot/webhook"
    web_server_host: str = "0.0.0.0"
    web_server_port: int = field(default_factory=lambda: int(os.getenv("PORT", "8080")))

    # Admin
    admin_ids: list[int] = field(default_factory=lambda: _get_int_list("ADMIN_IDS"))
    support_username: str = field(default_factory=lambda: os.getenv("SUPPORT_USERNAME", "support"))

    # Referral / bonus
    referral_bonus_stars: int = field(default_factory=lambda: int(os.getenv("REFERRAL_BONUS_STARS", "0")))


settings = Settings()
