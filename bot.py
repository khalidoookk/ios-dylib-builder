import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# إعدادات التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# الثوابت (يجب استبدالها ببيانات المستخدم)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")  # بصيغة "username/repo"
GITHUB_WORKFLOW = "ios_build_workflow.yml"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎉 مرحبًا بك في بوت DyLib Builder! 🎉\n\n"
        "أنا أقوم بترجمة مشاريع iOS الخاصة بك إلى ملفات .dylib حقيقية\n"
        "باستخدام مشغل macOS على GitHub Actions! 🍎⚙️\n\n"
        "📌 كيفية الاستخدام:\n"
        "• أرسل ملف .zip أو .tar.gz لمشروعك\n"
        "• سأكتشف اللغة وأقوم بترجمتها\n"
        "• ستحصل على ملف .dylib جاهز لـ iOS ARM64!\n\n"
        "🌐 المدعوم:\n"
        "• 🔵 C            — .c .h\n"
        "• 🟣 C++           — .cpp .cxx .cc .hpp .hxx .inl\n"
        "• 🟠 Swift         — .swift\n"
        "• 🔴 Objective-C  — .m .mm .mmh .pch\n"
        "• 🔥 مشروع مختلط — أي مزيج من الأعلى\n\n"
        "لنصنع شيئًا رائعًا! 🚀"
    )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    file_name = document.file_name
    
    if not (file_name.endswith('.zip') or file_name.endswith('.tar.gz')):
        await update.message.reply_text("❌ يرجى إرسال ملف مضغوط بصيغة .zip أو .tar.gz")
        return

    await update.message.reply_text("⏳ جاري استلام الملف وبدء عملية الترجمة على GitHub Actions...")

    # الحصول على رابط الملف من Telegram
    file = await context.bot.get_file(document.file_id)
    file_url = file.file_path

    # تشغيل GitHub Workflow
    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows/{GITHUB_WORKFLOW}/dispatches"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "ref": "main",
        "inputs": {
            "file_url": file_url,
            "chat_id": str(update.effective_chat.id)
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 204:
        await update.message.reply_text("🚀 تم تشغيل عملية البناء بنجاح! سأرسل لك ملف .dylib فور جاهزيته.")
    else:
        await update.message.reply_text(f"❌ فشل تشغيل عملية البناء. خطأ: {response.status_code}\n{response.text}")

if __name__ == '__main__':
    if not all([TELEGRAM_TOKEN, GITHUB_TOKEN, GITHUB_REPO]):
        print("Error: Please set TELEGRAM_TOKEN, GITHUB_TOKEN, and GITHUB_REPO environment variables.")
        exit(1)

    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    document_handler = MessageHandler(filters.Document.ALL, handle_document)
    
    application.add_handler(start_handler)
    application.add_handler(document_handler)
    
    print("Bot is running...")
    application.run_polling()
