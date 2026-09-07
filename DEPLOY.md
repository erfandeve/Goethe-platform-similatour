# استقرار (Deployment)

پروژه دو تکه است و **هر کدام میزبان جدا لازم دارد**:

| بخش | چیست | کجا مستقر می‌شود |
|---|---|---|
| `frontend/` | اپلیکیشن Next.js | **Vercel** |
| `backend/` | Django + DRF | **Railway** (ورسل نمی‌تواند جنگو را اجرا کند) |
| دیتابیس | MongoDB | **Railway** (در همان پروژه) |

> ⚠️ **مکالمه با هوش مصنوعی بدون بک‌اند کار نمی‌کند.** کلید OpenAI فقط روی سرور
> جنگو می‌نشیند؛ مرورگر هیچ‌وقت مستقیم با OpenAI حرف نمی‌زند. اگر فقط فرانت‌اند را
> روی ورسل بالا بیاورید، سایت باز می‌شود ولی ضبط صدا و تحلیل جواب نمی‌دهد.

---

## ۱) بک‌اند + دیتابیس — Railway (یک حساب، هر دو با هم)

Railway هم جنگو را اجرا می‌کند و هم MongoDB می‌دهد، پس فقط **یک** حساب لازم است.

1. [railway.app](https://railway.app) → با گیت‌هاب وارد شوید.
2. **New Project → Deploy from GitHub repo** → `Goethe-platform-similatour`.
3. در تنظیمات سرویس، **Root Directory** را `backend` بگذارید. (`backend/railway.json` و
   `backend/Dockerfile` بقیه‌اش را خودشان می‌گویند.)
4. داخل همان پروژه: **+ New → Database → Add MongoDB**.
5. برو روی سرویس جنگو → تب **Variables** → این‌ها را اضافه کن:

   ```
   SECRET_KEY=<یک رشتهٔ تصادفی بلند>
   DEBUG=False
   MONGO_HOST=${{MongoDB.MONGO_URL}}
   MONGO_DB=goteh
   OPENAI_API_KEY=sk-…            ← فقط اینجا، هیچ‌وقت داخل گیت
   ```

   `${{MongoDB.MONGO_URL}}` را عیناً همین‌طور بنویسید — Railway خودش آدرس
   دیتابیس را جایش می‌گذارد.

6. **Settings → Networking → Generate Domain** تا یک آدرس عمومی بگیرید،
   مثل `goteh-api-production.up.railway.app`.

**نیازی به اجرای دستی seed نیست.** کانتینر موقع بالا آمدن اگر دیتابیس خالی باشد
خودش پُرش می‌کند: دوره‌ها، پادکست‌ها، شبیه‌ساز کامل B2، دورهٔ مکالمه با AI، سه
پلن اشتراک، و این کاربر:

- ایمیل: `student@goteh.de`
- رمز: `goteh1234`
- پنل ادمین: دارد (`/fa/admin`)

سلامت سرویس: `https://<دامنه>/api/health/` باید `{"status":"ok"}` بدهد.

> `ALLOWED_HOSTS` لازم نیست ست شود (پیش‌فرضش `*` است) و `CORS_ORIGINS` هم لازم
> نیست، چون مرورگر هیچ‌وقت مستقیم با جنگو حرف نمی‌زند — همه چیز از مسیر
> `/api/proxy/*` خودِ Next.js رد می‌شود.

### گزینهٔ جایگزین: Render + MongoDB Atlas

اگر Railway را نمی‌خواهید: دیتابیس را روی [Atlas](https://cloud.mongodb.com)
بسازید (کلاستر رایگان M0، در Network Access آی‌پی `0.0.0.0/0` را باز کنید) و
سرویس را روی [Render](https://render.com) با **Root Directory = `api`** بالا
بیاورید؛ `backend/render.yaml` آماده است. همان متغیرهای بالا، فقط `MONGO_HOST` را
دستی با رشتهٔ اتصال Atlas پر کنید.

---

## ۲) فرانت‌اند — Vercel

1. [vercel.com/new](https://vercel.com/new) → همین ریپو.
2. **Root Directory** را روی `frontend` بگذارید. **این تنها تنظیمی است که
   باید دست بزنید** — بدون آن ورسل اپ Next.js را پیدا نمی‌کند.
3. بعد از انتخاب `frontend`، Framework Preset خودش `Next.js` می‌شود و
   `frontend/vercel.json` هم `buildCommand` را صریح `next build` می‌گذارد؛ پس
   هر Override قدیمی روی پروژه (مثلاً `vite build`) بی‌اثر می‌شود.
4. Environment Variables:

   ```
   NEXT_PUBLIC_API_URL=https://<دامنهٔ-railway>/api
   NEXT_PUBLIC_SITE_URL=https://<اسم-پروژه>.vercel.app
   NEXT_PUBLIC_MEDIA_URL=
   NEXT_PUBLIC_MAX_AUDIO_DURATION=60
   ```

   `NEXT_PUBLIC_MEDIA_URL` را **خالی** بگذارید (مقدار تهی، نه حذفش). یعنی
   ویدیوها و صداها از خود ورسل سرو شوند — نسخه‌شان در `public/media/`
   کامیت شده (۷۶ مگابایت) تا نیازی به سرویس فایل نباشد.

5. Deploy.

---

## ۳) بعد از استقرار

- بعد از ست‌کردن متغیرها در ورسل حتماً **Redeploy** بزنید: متغیرهای
  `NEXT_PUBLIC_*` موقع بیلد داخل کد می‌روند، نه موقع اجرا.
- **آپلود از پنل ادمین** ماندگار نیست: فایل جدید روی دیسک سرویس ابری
  می‌نشیند و با هر دیپلوی پاک می‌شود. برای تست کافی است؛ برای پروداکشن باید
  S3 یا Cloudflare R2 وصل شود و `SERVE_MEDIA=false` ست شود.
- مسیر تست مکالمه با AI:
  `/fa` → هدر → «مکالمه با AI» → خرید یا اشتراک → `/fa/learn/einreise-nach-deutschland`

---

## اجرای محلی

```bash
# ویدیوها و صداها یک نسخه دارند و آن نسخه در frontend/public/media است.
# برای اینکه بک‌اند محلی هم بتواند سروشان کند:
cp -R frontend/public/media backend/media

# بک‌اند
cd backend
python -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env      # و OPENAI_API_KEY را داخلش بگذارید
.venv/bin/python manage.py bootstrap
.venv/bin/python manage.py runserver 8010

# فرانت‌اند (در ترمینال دوم)
cd frontend
npm install
cp .env.example .env.local
npm run dev
```
