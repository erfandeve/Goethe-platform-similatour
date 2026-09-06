# استقرار (Deployment)

پروژه دو تکه است و **هر کدام میزبان جدا لازم دارد**:

| بخش | چیست | کجا مستقر می‌شود |
|---|---|---|
| ریشهٔ ریپو | اپلیکیشن Next.js | **Vercel** |
| `api/` | Django + DRF | **Render / Railway / Fly.io** (ورسل نمی‌تواند جنگو را اجرا کند) |
| دیتابیس | MongoDB | **MongoDB Atlas** (پلن رایگان کافی است) |

> ⚠️ **مکالمه با هوش مصنوعی بدون بک‌اند کار نمی‌کند.** کلید OpenAI فقط روی سرور
> جنگو می‌نشیند؛ مرورگر هیچ‌وقت مستقیم با OpenAI حرف نمی‌زند. اگر فقط فرانت‌اند را
> روی ورسل بالا بیاورید، سایت باز می‌شود ولی ضبط صدا و تحلیل جواب نمی‌دهد.

---

## ۱) دیتابیس — MongoDB Atlas

1. در [cloud.mongodb.com](https://cloud.mongodb.com) یک کلاستر رایگان (M0) بسازید.
2. **Database Access** → یک کاربر با رمز بسازید.
3. **Network Access** → `0.0.0.0/0` را اضافه کنید (تا سرویس ابری بتواند وصل شود).
4. رشتهٔ اتصال را بردارید:
   `mongodb+srv://USER:PASS@cluster0.xxxxx.mongodb.net/goteh?retryWrites=true&w=majority`

---

## ۲) بک‌اند — Render

`api/render.yaml` و `api/Dockerfile` آماده‌اند.

1. در [render.com](https://render.com) → **New → Web Service** → همین ریپو را وصل کنید.
2. **Root Directory** را `api` بگذارید؛ Render خودش `Dockerfile` را پیدا می‌کند.
3. متغیرهای محیطی را ست کنید:

   ```
   SECRET_KEY=<یک رشتهٔ تصادفی بلند>
   DEBUG=False
   ALLOWED_HOSTS=goteh-api.onrender.com
   CORS_ORIGINS=https://<اسم-پروژه>.vercel.app
   CSRF_TRUSTED_ORIGINS=https://<اسم-پروژه>.vercel.app
   MONGO_HOST=mongodb+srv://…/goteh
   MONGO_DB=goteh
   OPENAI_API_KEY=sk-…            ← فقط اینجا، هیچ‌وقت داخل گیت
   OPENAI_TEXT_MODEL=gpt-5.4-mini
   OPENAI_TRANSCRIPTION_MODEL=gpt-transcribe
   MAX_AUDIO_DURATION=60
   JWT_ACCESS_MINUTES=180
   ```

4. بعد از اولین دیپلوی، در **Shell** سرویس یک بار بزنید:

   ```bash
   python manage.py bootstrap
   ```

   این دستور همهٔ دیتای نمونه را می‌سازد: دوره‌ها، پادکست‌ها، شبیه‌ساز B2 کامل،
   دورهٔ مکالمه با AI، سه پلن اشتراک، و کاربر نمونه:

   - ایمیل: `student@goteh.de`
   - رمز: `goteh1234`
   - دسترسی پنل ادمین: دارد (`/fa/admin`)

5. سلامت سرویس: `https://goteh-api.onrender.com/api/health/` باید `{"status":"ok"}` بدهد.

> پلن رایگان Render بعد از ۱۵ دقیقه بی‌کاری می‌خوابد؛ اولین درخواست بعدی
> ~۳۰ ثانیه طول می‌کشد. برای تست مشکلی نیست.

---

## ۳) فرانت‌اند — Vercel

1. [vercel.com/new](https://vercel.com/new) → همین ریپو.
2. **Root Directory** را دست نزنید — اپ Next.js در ریشهٔ ریپو است، پس مقدار
   پیش‌فرض (`./`) درست است. اگر از قبل روی `web` تنظیم شده، خالی‌اش کنید.
3. Framework Preset خودش `Next.js` تشخیص داده می‌شود، و `vercel.json` ریشه هم
   `buildCommand` را صریح `next build` می‌گذارد؛ پس هر Override قدیمی روی
   پروژه (مثلاً `vite build`) بی‌اثر می‌شود.
4. Environment Variables:

   ```
   NEXT_PUBLIC_API_URL=https://goteh-api.onrender.com/api
   NEXT_PUBLIC_SITE_URL=https://<اسم-پروژه>.vercel.app
   NEXT_PUBLIC_MEDIA_URL=
   NEXT_PUBLIC_MAX_AUDIO_DURATION=60
   ```

   `NEXT_PUBLIC_MEDIA_URL` را **خالی** بگذارید (مقدار تهی، نه حذفش). یعنی
   ویدیوها و صداها از خود ورسل سرو شوند — نسخه‌شان در `public/media/`
   کامیت شده (۷۶ مگابایت) تا نیازی به سرویس فایل نباشد.

5. Deploy.

---

## ۴) بعد از استقرار

- `CORS_ORIGINS` و `CSRF_TRUSTED_ORIGINS` روی Render باید دقیقاً برابر دامنهٔ
  ورسل باشند، وگرنه ورود کار نمی‌کند.
- **آپلود از پنل ادمین** روی ورسل ماندگار نیست: فایل جدید روی دیسک Render
  می‌نشیند و با هر دیپلوی پاک می‌شود. برای تست کافی است؛ برای پروداکشن باید
  S3 یا Cloudflare R2 وصل شود و `SERVE_MEDIA=false` ست شود.
- مسیر تست مکالمه با AI:
  `/fa` → هدر → «مکالمه با AI» → خرید یا اشتراک → `/fa/learn/einreise-nach-deutschland`

---

## اجرای محلی

```bash
# ویدیوها و صداها یک نسخه دارند و آن نسخه در public/media است.
# برای اینکه بک‌اند محلی هم بتواند سروشان کند:
cp -R public/media api/media

# بک‌اند
cd api
python -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env      # و OPENAI_API_KEY را داخلش بگذارید
.venv/bin/python manage.py bootstrap
.venv/bin/python manage.py runserver 8010

# فرانت‌اند (ریشهٔ ریپو)
cd ..
npm install
cp .env.example .env.local
npm run dev
```
