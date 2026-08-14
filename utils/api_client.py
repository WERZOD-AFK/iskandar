"""
Backend (FastAPI) bilan gaplashuvchi yagona nuqta.
Bot HECH QACHON to'lovni o'zi "muvaffaqiyatli" deb belgilamaydi —
buni faqat backend, Telegram'dan kelgan successful_payment eventi
asosida qiladi.
"""
import logging
from typing import Any

import aiohttp

from config import settings

logger = logging.getLogger(__name__)


class ApiError(Exception):
    def __init__(self, status: int, detail: str):
        self.status = status
        self.detail = detail
        super().__init__(f"API error {status}: {detail}")


class ApiClient:
    def __init__(self) -> None:
        self._base_url = settings.api_base_url.rstrip("/")
        self._session: aiohttp.ClientSession | None = None

    async def start(self) -> None:
        self._session = aiohttp.ClientSession(
            headers={
                # Bot -> backend so'rovlarini tashqi so'rovlardan ajratish uchun.
                # Backend bu headerni tekshirmasa, hech kim uni taqlid qila olmasligi kerak.
                "X-Internal-Secret": settings.api_internal_secret,
                "Content-Type": "application/json",
            },
            timeout=aiohttp.ClientTimeout(total=10),
        )

    async def close(self) -> None:
        if self._session:
            await self._session.close()

    async def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        assert self._session is not None, "ApiClient.start() chaqirilmagan"
        url = f"{self._base_url}{path}"
        try:
            async with self._session.request(method, url, **kwargs) as resp:
                data = await resp.json(content_type=None)
                if resp.status >= 400:
                    detail = data.get("detail", "unknown error") if isinstance(data, dict) else str(data)
                    raise ApiError(resp.status, detail)
                return data
        except aiohttp.ClientError as exc:
            logger.exception("API so'rovida tarmoq xatosi: %s %s", method, url)
            raise ApiError(0, str(exc)) from exc

    # ---- Users -------------------------------------------------------

    async def upsert_user(self, tg_user_id: int, username: str | None, full_name: str,
                           ref_code: str | None = None) -> dict:
        return await self._request(
            "POST", "/api/users/upsert",
            json={
                "tg_user_id": tg_user_id,
                "username": username,
                "full_name": full_name,
                "ref_code": ref_code,
            },
        )

    async def get_user(self, tg_user_id: int) -> dict:
        return await self._request("GET", f"/api/users/{tg_user_id}")

    # ---- Products ------------------------------------------------------

    async def list_active_products(self) -> list[dict]:
        return await self._request("GET", "/api/products", params={"active": "true"})

    # ---- Orders --------------------------------------------------------

    async def create_order(self, tg_user_id: int, product_id: int, promo_code: str | None = None) -> dict:
        return await self._request(
            "POST", "/api/orders",
            json={"tg_user_id": tg_user_id, "product_id": product_id, "promo_code": promo_code},
        )

    async def list_orders(self, tg_user_id: int, limit: int = 20) -> list[dict]:
        return await self._request("GET", f"/api/orders", params={"tg_user_id": tg_user_id, "limit": limit})

    async def get_order(self, order_id: int) -> dict:
        return await self._request("GET", f"/api/orders/{order_id}")

    async def mark_order_paid(self, order_id: int, telegram_payment_charge_id: str) -> dict:
        """Faqat successful_payment eventidan keyin chaqiriladi."""
        return await self._request(
            "POST", f"/api/orders/{order_id}/mark-paid",
            json={"telegram_payment_charge_id": telegram_payment_charge_id},
        )

    # ---- Support ---------------------------------------------------------

    async def create_support_ticket(self, tg_user_id: int, message: str) -> dict:
        return await self._request(
            "POST", "/api/support/tickets",
            json={"tg_user_id": tg_user_id, "message": message},
        )


api_client = ApiClient()
