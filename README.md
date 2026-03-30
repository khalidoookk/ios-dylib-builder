# دليل إعداد بوت DyLib Builder 🚀

هذا الدليل سيساعدك في تشغيل البوت الخاص بك وربطه بـ GitHub Actions لترجمة ملفات iOS dylib.

## المتطلبات الأساسية 📋
1. **حساب GitHub**: ستحتاج إلى مستودع (Repository) خاص بالبوت.
2. **Telegram Bot Token**: احصل عليه من [@BotFather](https://t.me/BotFather).
3. **GitHub Personal Access Token (PAT)**: ستحتاج إلى توكن بصلاحيات `workflow` و `repo`.
4. **خادم لتشغيل البوت**: يمكنك تشغيله على أي خادم يدعم Python.

---

## الخطوة 1: إعداد مستودع GitHub ⚙️
1. قم بإنشاء مستودع جديد على GitHub (مثلاً باسم `ios-dylib-builder`).
2. أنشئ مجلداً باسم `.github/workflows` داخل المستودع.
3. ارفع ملف `ios_build_workflow.yml` المرفق إلى هذا المجلد.
4. اذهب إلى إعدادات المستودع (Settings) -> Secrets and variables -> Actions.
5. أضف سرًا جديدًا (New repository secret) باسم `TELEGRAM_TOKEN` وضع فيه توكن البوت الخاص بك.

---

## الخطوة 2: إعداد كود البوت 🐍
1. تأكد من تثبيت مكتبة `python-telegram-bot` و `requests`:
   ```bash
   pip install python-telegram-bot requests
   ```
2. قم بتعيين المتغيرات البيئية التالية قبل تشغيل `bot.py`:
   - `TELEGRAM_TOKEN`: توكن البوت من BotFather.
   - `GITHUB_TOKEN`: التوكن الخاص بك من GitHub (PAT).
   - `GITHUB_REPO`: اسم المستودع بصيغة `username/repo_name`.

---

## الخطوة 3: تشغيل البوت 🚀
قم بتشغيل البوت باستخدام الأمر:
```bash
python bot.py
```

---

## كيف يعمل البوت؟ 🤔
1. يرسل المستخدم ملف `.zip` يحتوي على ملفات المصدر (`.swift`, `.m`, `.cpp`, إلخ).
2. يقوم البوت بإرسال رابط الملف إلى GitHub Actions عبر API.
3. يقوم GitHub Actions بتشغيل macOS runner، وتحميل الملف، وترجمته باستخدام `clang` أو `swiftc`.
4. بعد انتهاء الترجمة، يقوم GitHub Actions بإرسال ملف الـ `.dylib` الناتج مباشرة إلى المستخدم عبر Telegram.

---

**ملاحظة**: تأكد من أن المستودع يحتوي على فرع (branch) باسم `main` أو قم بتغيير القيمة في `bot.py` لتناسب اسم الفرع لديك.
