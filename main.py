import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import settings
from handlers import admin, orders, payments, start, support
from utils.api_client import api_client

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)


def build_dispatcher() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start.router)
    dp.include_router(payments.router)
    dp.include_router(orders.router)
    dp.include_router(support.router)
    dp.include_router(admin.router)
    return dp


async def on_startup(bot: Bot) -> None:
    await api_client.start()
    if settings.use_webhook:
        webhook_url = f"{settings.webhook_base_url.rstrip('/')}{settings.webhook_path}"
        await bot.set_webhook(
            webhook_url,
            secret_token=settings.webhook_secret,
            drop_pending_updates=True,
        )
        logger.info("Webhook o'rnatildi: %s", webhook_url)
    else:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Polling rejimida ishga tushmoqda")


async def on_shutdown(bot: Bot) -> None:
    await api_client.close()
    if settings.use_webhook:
        await bot.delete_webhook()


async def run_polling() -> None:
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = build_dispatcher()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


def run_webhook() -> None:
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = build_dispatcher()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot, secret_token=settings.webhook_secret).register(
        app, path=settings.webhook_path
    )
    setup_application(app, dp, bot=bot)

    # Railway/health-check uchun oddiy endpoint
    async def health(_request: web.Request) -> web.Response:
        return web.Response(text="ok")

    app.router.add_get("/health", health)

    web.run_app(app, host=settings.web_server_host, port=settings.web_server_port)


if __name__ == "__main__":
    if settings.use_webhook:
        run_webhook()
    else:
        asyncio.run(run_polling())
