# Stars Shop — Telegram Bot (aiogram 3)

Bu Stars Mini App loyihasining **bot** qismi. Bot foydalanuvchi bilan
birinchi bo'lib gaplashadi: Mini App'ni ochadi, Telegram Stars orqali
to'lovni boshqaradi (invoice yuborish, `pre_checkout_query`,
`successful_payment`), referal va support tizimini ishlatadi.

Bot **hech qanday ma'lumotni o'zida saqlamaydi** — hamma narsa (userlar,
buyurtmalar, mahsulotlar, statistika) backend (FastAPI) orqali
`utils/api_client.py` yordamida olinadi/yoziladi. Shu sabab bu bot ishlashi
uchun backend allaqachon ishlab turgan bo'lishi kerak.

## Loyiha tuzilishi

```
stars-bot/
├── main.py                # Kirish nuqtasi (polling / webhook)
├── config.py               # .env dan o'qiladigan sozlamalar
├── handlers/
│   ├── start.py             # /start, referal, asosiy menyu
│   ├── payments.py          # Telegram Stars invoice va to'lov tasdiqlash
│   ├── orders.py            # Buyurtmalar tarixi, profil, referal havola
│   ├── support.py           # FAQ va savol-javob (FSM)
│   └── admin.py             # /stats, /broadcast, /block
├── keyboards/main.py        # Reply va inline klaviaturalar
├── utils/api_client.py      # Backend bilan HTTP orqali muloqot
├── requirements.txt
├── .env.example
├── Dockerfile
└── README.md
```

## Mahalliy ishga tushirish

1. Python 3.12+ o'rnatilgan bo'lsin.
2. Virtual environment yarating va kutubxonalarni o'rnating:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. `.env.example` faylidan nusxa oling va o'z qiymatlaringizni kiriting:
   ```bash
   cp .env.example .env
   ```
   - `BOT_TOKEN` — [@BotFather](https://t.me/BotFather) dan olinadi.
   - `WEBAPP_URL` — Mini App frontend joylashtirilgan HTTPS manzil
     (mahalliy testda [ngrok](https://ngrok.com/) yoki shunga o'xshash
     tunnel ishlatishingiz mumkin — Telegram WebApp faqat HTTPS'ni qabul qiladi).
   - `API_BASE_URL` — backend manzili.
   - `USE_WEBHOOK=false` qoldiring — mahalliy testda polling qulayroq.
4. Botni ishga tushiring:
   ```bash
   python main.py
   ```

## BotFather sozlamalari

1. `/newbot` — yangi bot yarating, tokenni oling.
2. `/setmenubutton` yoki `/newapp` — Mini App'ni ulang, `WEBAPP_URL` bilan bir xil manzilni bering.
3. Stars orqali to'lov qabul qilish uchun alohida "provider" sozlash **shart emas** —
   Telegram Stars uchun `provider_token` doim bo'sh, `currency="XTR"` ishlatiladi
   (kod ichida `handlers/payments.py`'da allaqachon shunday qilingan).

## Railway'ga deploy qilish (webhook rejimida)

1. Loyihani GitHub'ga push qiling.
2. Railway'da **New Project → Deploy from GitHub repo** tanlang.
3. Railway avtomatik `Dockerfile`ni topib, shu asosda build qiladi.
4. Railway "Variables" bo'limida barcha `.env.example`dagi o'zgaruvchilarni kiriting, qo'shimcha:
   - `USE_WEBHOOK=true`
   - `WEBHOOK_BASE_URL` — Railway sizga bergan public domain
     (masalan `https://your-bot.up.railway.app`)
   - `PORT` — Railway buni o'zi avtomatik beradi, qo'lda kiritish shart emas.
5. Deploy tugagach, bot avtomatik `set_webhook` qiladi (`on_startup` funksiyasida).
6. `/health` endpointi orqali Railway health-check qilib turishi mumkin.

> ⚠️ Railway'ning bepul/trial rejasi vaqt yoki kredit bilan cheklangan bo'lishi
> mumkin — joriy shartlarni deploy qilishdan oldin Railway saytidan tekshirib oling.

## Xavfsizlik bo'yicha eslatmalar

- `BOT_TOKEN` va `API_INTERNAL_SECRET` hech qachon kodga yozilmaydi — faqat `.env` / Railway Variables orqali.
- Bot to'lovni hech qachon o'zi "muvaffaqiyatli" deb belgilamaydi — bu backend ishi (`mark_order_paid`), va u faqat Telegram'dan kelgan haqiqiy `successful_payment` eventidan keyin chaqiriladi.
- Webhook rejimida `WEBHOOK_SECRET` orqali so'rovlar Telegram'dan kelayotganini tasdiqlang (aiogram buni avtomatik tekshiradi).
- Admin komandalar (`/stats`, `/broadcast`, `/block`) faqat `ADMIN_IDS` ro'yxatidagilar uchun ishlaydi.

## Keyingi qadam

Bu bot backend API'ga (`/api/users`, `/api/orders`, `/api/products`, `/api/support`,
`/api/admin/*`) tayanadi. Keyingi bosqichda shu FastAPI backend va PostgreSQL
sxemasini qurish kerak bo'ladi — xohlasangiz shundan davom etamiz.
