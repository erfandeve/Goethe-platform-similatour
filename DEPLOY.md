# استقرار لکسورا روی سرور و دامنه واقعی

این راهنما برای یک **سرور مجازی اوبونتو (VPS)** نوشته شده، همان روشی که پروژه‌های دیگرت هم با آن بالا آمده‌اند:
nginx جلوی سایت، دو سرویس systemd (سایت Next.js و API جنگو)، MongoDB روی همان سرور و گواهی SSL رایگان با certbot.

فایل‌های آماده در پوشه `deploy/` هستند:

| فایل | کارش |
|---|---|
| `nginx-lexora.conf` | تنظیم nginx: انتقال www به دامنه اصلی، سرو کردن `/media`، ارسال بقیه درخواست‌ها به سایت |
| `lexora-api.service` / `lexora-web.service` | سرویس‌های systemd |
| `backend.env.example` | متغیرهای سرور (جنگو) |
| `frontend.env.example` | متغیرهای بیلد سایت (روی لپ‌تاپ خودت) |
| `build.sh` | بیلد سایت روی لپ‌تاپ |
| `push.sh` | آپلود روی سرور و ری‌استارت سرویس‌ها |
| `backup.sh` | بکاپ شبانه دیتابیس و فایل‌های آپلودی |

> ⚠️ **بیلد را روی سرور نزن.** بیلد Next.js بیشتر از ۲ گیگ رم لازم دارد. روی لپ‌تاپ بیلد می‌شود و فقط خروجی آپلود می‌شود.

---

## ۱) پیش از شروع

- یک VPS با اوبونتو ۲۲.۰۴ یا ۲۴.۰۴، حداقل ۲ گیگ رم و ۳۰ گیگ دیسک.
- دامنه: در پنل DNS، رکورد `A` برای `@` و `www` را به IP سرور بزن. اگر پنل CDN یا پروکسی دارد، روی «فقط DNS» بگذار تا certbot بتواند گواهی بگیرد.
- یک **کلید OpenAI جدید** بساز. کلید قبلی در چت فرستاده شده و باید باطل شود.

## ۲) آماده‌سازی سرور (فقط یک بار)

```bash
apt update && apt install -y nginx certbot python3-certbot-nginx rsync curl ufw
# Node.js 20 یا جدیدتر (برای اجرای سایت)
curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && apt install -y nodejs
# MongoDB 7 طبق راهنمای رسمی mongodb.com (اگر مخزنش از ایران باز نشد، بسته .deb را جدا دانلود کن)
systemctl enable --now mongod

# پایتون ۳.۱۳ با uv، در مسیری که کاربر www-data هم به آن دسترسی دارد
curl -LsSf https://astral.sh/uv/install.sh | sh
export UV_PYTHON_INSTALL_DIR=/opt/uv-python && ~/.local/bin/uv python install 3.13
chmod -R a+rX /opt/uv-python

mkdir -p /var/www/lexora/{backend,web}
cd /var/www/lexora/backend && ~/.local/bin/uv venv --python 3.13 .venv

ufw allow OpenSSH && ufw allow 'Nginx Full' && ufw enable
```

فایل `/var/www/lexora/backend/.env` را از روی `deploy/backend.env.example` بساز و پر کن:

- **`SECRET_KEY`**: یک رشته تصادفی بلند (دستورش داخل همان فایل هست). اگر خالی یا کوتاه باشد، API عمداً روشن نمی‌شود، چون با کلید معلوم هر کسی می‌تواند توکن ادمین جعل کند.
- **`ADMIN_EMAIL` و `ADMIN_PASSWORD`**: حساب ادمین واقعی تو. رمز حداقل ۱۲ کاراکتر باشد.
- دامنه‌ها در `ALLOWED_HOSTS`، `CSRF_TRUSTED_ORIGINS` و `CORS_ORIGINS`.

## ۳) بیلد و آپلود (هر بار که کد عوض شد)

روی لپ‌تاپ:

```bash
cp deploy/frontend.env.example deploy/frontend.env   # فقط بار اول؛ دامنه را داخلش بنویس
bash deploy/build.sh
SERVER=root@IP-سرور bash deploy/push.sh
```

- `build.sh` اگر `NEXT_PUBLIC_SITE_URL` با `https://` شروع نشود، متوقف می‌شود. این آدرس داخل همه لینک‌های canonical، نقشه سایت و تصاویر اشتراک‌گذاری قرار می‌گیرد، پس باید دامنه واقعی باشد.
- `push.sh` اگر اتصال وسط آپلود قطع شود، خودش دوباره امتحان می‌کند.

## ۴) اولین راه‌اندازی (فقط یک بار، روی سرور)

```bash
cd /var/www/lexora/backend
sudo -u www-data .venv/bin/python manage.py bootstrap --if-empty

cp /var/www/lexora/deploy/lexora-*.service /etc/systemd/system/
systemctl daemon-reload && systemctl enable --now lexora-api lexora-web
```

`bootstrap` روی سرور (با `DEBUG=False`) این کارها را انجام می‌دهد:

- دوره‌ها، آزمون‌ها، مقاله‌ها و پادکست‌ها را می‌سازد.
- **حساب دمو `student@goteh.de` را که رمزش در README نوشته شده پاک می‌کند** و حساب ادمین تو را از `ADMIN_EMAIL` می‌سازد.
- **امتیازها، تعداد نظرها، تعداد دانشجوها و بازدیدهای ساختگی را صفر می‌کند** و نظرهای نمونه را پاک می‌کند. این اعداد در نتایج گوگل هم نمایش داده می‌شوند و عدد ساختگی ممکن است باعث جریمه شود. از این به بعد فقط آمار واقعی نمایش داده می‌شود، و هر عددی که صفر باشد اصلاً نشان داده نمی‌شود.

بعد nginx و SSL:

```bash
sed 's/example.com/دامنه‌ات/g' /var/www/lexora/deploy/nginx-lexora.conf > /etc/nginx/sites-available/lexora
ln -s /etc/nginx/sites-available/lexora /etc/nginx/sites-enabled/ && rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx
certbot --nginx -d دامنه‌ات -d www.دامنه‌ات --redirect
```

و بکاپ شبانه:

```bash
cp /var/www/lexora/deploy/backup.sh /usr/local/bin/lexora-backup && chmod +x /usr/local/bin/lexora-backup
(crontab -l; echo "30 2 * * * /usr/local/bin/lexora-backup") | crontab -
```

## ۵) بعد از بالا آمدن سایت: چک‌لیست سئو

1. **Google Search Console** → Add property → Domain.
   - اگر روش «HTML tag» را انتخاب کردی، مقدار `content` را در `NEXT_PUBLIC_GOOGLE_SITE_VERIFICATION` بگذار، دوباره بیلد و آپلود کن.
   - بعد در بخش Sitemaps آدرس `https://دامنه/sitemap.xml` را ثبت کن.
2. **Bing Webmaster Tools**: همین کار را انجام بده (`NEXT_PUBLIC_BING_SITE_VERIFICATION`). می‌توانی از Search Console هم ایمپورت کنی.
3. لینک صفحه‌های اینستاگرام، تلگرام و یوتیوب را در `NEXT_PUBLIC_SAME_AS` بگذار تا گوگل آن‌ها را به برند لکسورا وصل کند.
4. **آزمون نتایج غنی**: چند صفحه، مثل یک دوره، یک آزمون و یک مقاله، را در https://search.google.com/test/rich-results تست کن.
5. **پیش‌نمایش اشتراک‌گذاری**: لینک سایت را در تلگرام یا واتس‌اپ بفرست. باید تصویر لکسورا به زبان همان صفحه نمایش داده شود.
6. **محتوای نمونه**: پادکست‌ها و بخشی از متن دوره‌ها هنوز محتوای نمونه هستند. قبل از انتشار عمومی از پنل ادمین با محتوای واقعی عوضشان کن. همه ۲۴ اپیزود پادکست توضیح یکسان دارند.

## کارهایی که از قبل در کد انجام شده

- هر صفحه عنوان، توضیح (۱۲۰ تا ۱۶۰ کاراکتر)، canonical و hreflang برای fa، de و en همراه x-default دارد. این‌ها برای ربات‌های جستجو همیشه داخل `<head>` قرار می‌گیرند.
- `sitemap.xml` با hreflang و `robots.txt` آماده‌اند. صفحه‌های خصوصی (پنل، سبد خرید، ورود و آزمون در حال برگزاری) noindex هستند.
- داده ساختاریافته (JSON-LD): سازمان، وب‌سایت، دوره‌ها، سؤالات متداول، breadcrumb، مقاله‌ها و اشتراک‌ها.
- تصویر اشتراک‌گذاری جدا برای هر زبان، آیکون سایت، آیکون اپل و manifest.
- صفحه‌ای که وجود ندارد کد ۴۰۴ واقعی و noindex برمی‌گرداند. ریدایرکت زبان بر اساس ترجیح مرورگر است.
- هدرهای امنیتی، کش طولانی برای فایل‌ها و حذف `X-Powered-By`.

---

### گزینه قدیمی: Vercel و Railway

فایل‌های `frontend/vercel.json`، `backend/railway.json` و `backend/render.yaml` هنوز سر جایشان هستند. ولی برای سایتی که مخاطبش در ایران است، سرور ایرانی مطمئن‌تر است: ممکن است Vercel از ایران در دسترس نباشد و پرداخت این سرویس‌ها هم از ایران ممکن نیست.
