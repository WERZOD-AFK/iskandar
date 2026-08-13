# Stars Shop — Admin Panel

Bitta HTML fayl, build kerak emas. Ochilganda Backend URL va
`ADMIN_PANEL_PASSWORD` (backend `.env`da o'rnatilgan) so'raladi.

## Ishlatish

1. `index.html`ni istalgan statik hostingga joylang (Vercel, Netlify, Railway static,
   yoki hatto shunchaki brauzerda `file://` orqali oching — CORS uchun backend'da
   `ADMIN_PANEL_ORIGIN`ni to'g'ri sozlang, yoki test uchun `*` qoldiring).
2. Ochilganda:
   - **Backend URL** — masalan `https://your-backend.up.railway.app`
   - **Admin parol** — backend `.env`dagi `ADMIN_PANEL_PASSWORD`
3. Kirgach: Dashboard, Buyurtmalar (yakunlash), Paketlar (qo'shish/o'chirish/popular
   qilish), Foydalanuvchilar (qidirish/bloklash), Promo kodlar (yaratish/o'chirish),
   Support (savollarni ko'rish).

## Xavfsizlik

- Parol brauzer `localStorage`da saqlanadi — faqat o'zingiz ishlatadigan qurilmada oching.
- Production'da HTTPS orqali joylashtiring, parolni murakkab va uzun qiling.
- `/broadcast` hozircha faqat bot orqali ishlaydi (`/broadcast` komandasi) — admin
  panelga alohida qo'shilmagan.
