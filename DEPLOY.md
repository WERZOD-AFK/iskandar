# Stars Shop — To'liq deploy qo'llanmasi

Loyiha 4 qismdan iborat, hammasi bir-biriga ulangan:

```
stars-bot/        → Telegram bot (aiogram)
stars-backend/     → API + PostgreSQL (FastAPI)
stars-frontend/     → Mini App (React, foydalanuvchi ko'radigan)
stars-admin/         → Admin panel (bitta HTML fayl)
```

## 0. Oldindan kerak bo'ladigan narsalar

- [@BotFather](https://t.me/BotFather)dan bot yaratib, **BOT_TOKEN** oling
- Railway (yoki boshqa host) hisobingiz
- GitHub repo (har bir loyiha uchun alohida yoki monorepo qilib bitta repo
  ichida 4 ta papka — ikkalasi ham ishlaydi)

## 1. Maxfiy kalitlarni tayyorlab oling

Deploydan oldin quyidagilarni o'zingiz uchun generatsiya qiling (masalan
`openssl rand -hex 24` orqali):

| Kalit | Qayerda ishlatiladi |
|---|---|
| `API_INTERNAL_SECRET` | bot **va** backend — ikkalasida bir xil bo'lishi shart |
| `ADMIN_PANEL_PASSWORD` | backend **va** admin panel — ikkalasida bir xil |
| `BOT_TOKEN` | bot **va** backend — ikkalasida bir xil (backend Mini App initData'sini shu bilan tekshiradi) |

## 2. Backend'ni deploy qilish (birinchi — boshqalar shunga bog'liq)

1. Railway'da PostgreSQL plugin qo'shing.
2. `stars-backend`ni GitHub'ga push qiling, Railway'da yangi service sifatida ulang.
3. Variables:
   ```
   DATABASE_URL=postgresql+asyncpg://...   # Railway PostgreSQL'dan, postgresql+asyncpg:// ga o'zgartiring
   API_INTERNAL_SECRET=<1-qadamdagi kalit>
   ADMIN_PANEL_PASSWORD=<1-qadamdagi kalit>
   BOT_TOKEN=<BotFather'dan>
   REFERRAL_BONUS_STARS=50
   FRONTEND_ORIGIN=*        # frontend deploy qilingach haqiqiy domenga almashtiring
   ADMIN_PANEL_ORIGIN=*     # admin panel deploy qilingach haqiqiy domenga almashtiring
   ```
4. Deploy tugagach, manzilni yozib oling: `https://your-backend.up.railway.app`
5. Tekshirish: `https://your-backend.up.railway.app/health` → `{"status":"ok"}`

## 3. Mini App frontend'ni deploy qilish (Vercel)

1. `stars-frontend`ni GitHub'ga push qiling, Vercel'da import qiling.
2. Environment Variables:
   ```
   VITE_API_BASE_URL=https://your-backend.up.railway.app
   VITE_BOT_USERNAME=your_bot_username
   ```
3. Deploy tugagach manzilni yozib oling: `https://your-app.vercel.app`
4. **Backend'ga qaytib**, `FRONTEND_ORIGIN`ni shu manzilga o'zgartiring va qayta deploy qiling.

## 4. Bot'ni deploy qilish (Railway)

1. `stars-bot`ni GitHub'ga push qiling, Railway'da yangi service sifatida ulang.
2. Variables:
   ```
   BOT_TOKEN=<xuddi backend'dagi bilan bir xil>
   WEBAPP_URL=https://your-app.vercel.app       # 3-qadamdagi Vercel manzili
   API_BASE_URL=https://your-backend.up.railway.app
   API_INTERNAL_SECRET=<1-qadamdagi kalit, backend bilan bir xil>
   USE_WEBHOOK=true
   WEBHOOK_BASE_URL=https://your-bot.up.railway.app   # Railway o'zi beradi
   WEBHOOK_SECRET=<yana bitta tasodifiy kalit>
   ADMIN_IDS=<sizning Telegram ID'ingiz>
   REFERRAL_BONUS_STARS=50
   ```
3. [@BotFather](https://t.me/BotFather)da:
   - `/setmenubutton` → shu bot uchun → Web App URL: `https://your-app.vercel.app`
4. Botni Telegram'da oching, `/start` bosing — menyu tugmasi orqali Mini App ochilishi kerak.

## 5. Admin panelni deploy qilish

1. `stars-admin/index.html`ni istalgan statik hostingga joylang (Vercel/Netlify —
   bitta HTML fayl, build kerak emas) yoki oddiy shunchaki lokal ochib turing.
2. **Backend'ga qaytib**, `ADMIN_PANEL_ORIGIN`ni shu manzilga o'zgartiring.
3. Panelni oching, Backend URL va `ADMIN_PANEL_PASSWORD`ni kiriting.
4. Birinchi ishingiz: **Paketlar** bo'limidan kamida bitta Stars paketini
   qo'shing (masalan 100, 500, 1000) — aks holda Mini App'da katalog bo'sh ko'rinadi.

## 6. To'liq test qilish

1. Admin panelda 3-4 ta paket yarating (birini "Popular" qiling).
2. Botga `/start` yozing → Mini App ochiladi → paketlar ko'rinishi kerak.
3. Bir paket tanlang → "Sotib olish" → Telegram'ning o'z Stars to'lov oynasi ochilishi kerak.
4. To'lovni yakunlang (Telegram test muhitida haqiqiy Stars kerak bo'lishi mumkin —
   [Telegram test bot](https://core.telegram.org/bots/payments#getting-a-token) orqali
   test rejimida sinab ko'ring).
5. To'lovdan keyin: Mini App'dagi "Buyurtmalarim"da status "To'lov qilindi" bo'lishi kerak.
6. Admin panelda "Buyurtmalar"dan shu buyurtmani "Yakunlash" tugmasi bilan yoping —
   agar referal orqali kelgan bo'lsa, referrerga bonus avtomatik yoziladi.

## Muammolarni bartaraf etish

| Muammo | Sabab |
|---|---|
| Mini App'da "401" xatolik | `BOT_TOKEN` bot va backend'da bir xil emas, yoki Mini App Telegram tashqarisida (brauzerda) ochilgan |
| Admin panel kira olmayapti | `ADMIN_PANEL_PASSWORD` noto'g'ri, yoki Backend URL oxirida `/` bor (olib tashlang) |
| CORS xatosi | `FRONTEND_ORIGIN` / `ADMIN_PANEL_ORIGIN` haqiqiy domen bilan mos emas |
| Bot javob bermayapti | Webhook to'g'ri o'rnatilmagan — Railway loglarini tekshiring, yoki `USE_WEBHOOK=false` qilib pollingga o'ting (test uchun) |
| To'lov invoice ochilmayapti | Bot BotFather'da Stars to'lovlari uchun alohida sozlash talab qilmaydi, lekin `createInvoiceLink` xato bersa — `BOT_TOKEN` noto'g'ri bo'lishi mumkin |

## Xavfsizlik bo'yicha yakuniy eslatma

- `API_INTERNAL_SECRET` va `BOT_TOKEN` hech qachon frontend yoki admin panel
  kodiga yozilmaydi — faqat backend va bot muhitida (environment variables).
- Production'ga chiqishdan oldin `FRONTEND_ORIGIN` va `ADMIN_PANEL_ORIGIN`ni
  `*`dan haqiqiy domenlarga almashtiring.
- `ADMIN_PANEL_PASSWORD`ni uzun va murakkab qiling — bu parol admin panelga
  kiruvchi yagona himoya.
