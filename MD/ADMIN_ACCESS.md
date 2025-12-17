# راهنمای دسترسی به پنل مدیریت (Admin Panel)

## ایجاد Superuser

برای دسترسی به پنل مدیریت، ابتدا باید یک superuser ایجاد کنید.

### روش 1: استفاده از دستور مدیریتی سفارشی (پیشنهادی)

```bash
# فعال‌سازی محیط مجازی
source venv/bin/activate

# ایجاد superuser با دستور سفارشی
python manage.py create_admin
```

این دستور به صورت تعاملی از شما اطلاعات زیر را می‌پرسد:
- Username (نام کاربری)
- Email (ایمیل)
- Password (رمز عبور)

### روش 2: استفاده از دستور استاندارد Django

```bash
# فعال‌سازی محیط مجازی
source venv/bin/activate

# ایجاد superuser
python manage.py createsuperuser
```

### روش 3: استفاده از دستور مدیریتی با پارامترها

```bash
# ایجاد superuser بدون تعامل (non-interactive)
python manage.py create_admin --username admin --email admin@example.com --password yourpassword --no-input
```

## دسترسی به پنل مدیریت

پس از ایجاد superuser، می‌توانید از طریق آدرس زیر به پنل مدیریت دسترسی پیدا کنید:

```
http://127.0.0.1:8000/admin/
```

یا اگر آدرس ادمین را تغییر داده‌اید:

```
http://127.0.0.1:8000/{ADMIN_URL}/
```

### تغییر آدرس ادمین

برای امنیت بیشتر، می‌توانید آدرس ادمین را تغییر دهید. برای این کار:

1. فایل `.env` را باز کنید
2. متغیر `ADMIN_URL` را تغییر دهید:

```bash
ADMIN_URL=my-custom-admin-url
```

3. سرور را دوباره راه‌اندازی کنید

## ویژگی‌های امنیتی پنل مدیریت

### 1. محدودیت دسترسی
- فقط کاربرانی با `is_staff=True` می‌توانند وارد پنل شوند
- فقط کاربرانی با `is_superuser=True` دسترسی کامل دارند

### 2. محدودیت IP (اختیاری)
می‌توانید دسترسی را به IP های خاص محدود کنید:

```bash
# در فایل .env
ADMIN_IP_WHITELIST=127.0.0.1,::1,your-ip-address
```

### 3. Rate Limiting
- حداکثر 5 تلاش برای ورود در هر 15 دقیقه
- پس از بیش از حد مجاز، دسترسی موقتاً مسدود می‌شود

### 4. لاگ‌گیری
تمام تلاش‌های ورود و دسترسی به پنل مدیریت در فایل‌های لاگ ثبت می‌شوند:
- `logs/admin.log` - لاگ‌های ادمین
- `logs/django.log` - لاگ‌های کلی

## مدیریت کاربران موجود

اگر کاربری از قبل وجود دارد و می‌خواهید آن را به superuser تبدیل کنید:

### روش 1: از طریق دستور مدیریتی

```bash
python manage.py create_admin --username existing_username
```

اگر کاربر وجود داشته باشد، از شما می‌پرسد که آیا می‌خواهید آن را به superuser تبدیل کنید.

### روش 2: از طریق Django Shell

```bash
python manage.py shell
```

سپس در shell:

```python
from accounts.models import User

# پیدا کردن کاربر
user = User.objects.get(username='your_username')

# تبدیل به superuser
user.is_superuser = True
user.is_staff = True
user.is_active = True
user.save()
```

### روش 3: از طریق پنل مدیریت

اگر به پنل مدیریت دسترسی دارید:
1. وارد پنل مدیریت شوید
2. به بخش Users بروید
3. کاربر مورد نظر را پیدا کنید
4. فیلدهای `is_superuser` و `is_staff` را فعال کنید
5. تغییرات را ذخیره کنید

## عیب‌یابی

### مشکل: نمی‌توانم وارد پنل شوم

1. **بررسی کنید که کاربر superuser است:**
   ```bash
   python manage.py shell
   ```
   ```python
   from accounts.models import User
   user = User.objects.get(username='your_username')
   print(f"is_superuser: {user.is_superuser}")
   print(f"is_staff: {user.is_staff}")
   print(f"is_active: {user.is_active}")
   ```

2. **بررسی لاگ‌ها:**
   ```bash
   tail -f logs/admin.log
   ```

3. **بررسی محدودیت IP:**
   اگر `ADMIN_IP_WHITELIST` تنظیم شده است، مطمئن شوید IP شما در لیست است.

### مشکل: خطای "Too many login attempts"

اگر این خطا را می‌بینید:
1. 15 دقیقه صبر کنید
2. یا کش را پاک کنید:
   ```bash
   python manage.py shell
   ```
   ```python
   from django.core.cache import cache
   # پاک کردن تمام کش (مراقب باشید!)
   cache.clear()
   ```

### مشکل: آدرس ادمین کار نمی‌کند

1. بررسی کنید که `ADMIN_URL` در `.env` صحیح است
2. سرور را دوباره راه‌اندازی کنید
3. بررسی کنید که URL در `config/urls.py` صحیح است

## نکات امنیتی

1. **همیشه از رمز عبور قوی استفاده کنید**
2. **در production، `DEBUG=False` تنظیم کنید**
3. **آدرس ادمین را تغییر دهید** (از `admin` به چیزی دیگر)
4. **محدودیت IP را فعال کنید** در صورت امکان
5. **لاگ‌ها را به طور منظم بررسی کنید**
6. **از HTTPS استفاده کنید** در production

## پشتیبانی

برای مشکلات بیشتر، به فایل‌های زیر مراجعه کنید:
- `MD/ADMIN_SETUP.md` - راهنمای تنظیمات پنل مدیریت
- `MD/SECURITY.md` - راهنمای امنیتی
- `MD/SETUP.md` - راهنمای کلی نصب و راه‌اندازی

