import os
import logging
import replicate
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# استفاده از Environment Variables برای امنیت
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
REPLICATE_API_TOKEN = os.getenv('REPLICATE_API_TOKEN')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! من ربات تصویرساز هستم. متنی که دوست داری رو بفرست تا برات عکس بسازم! 🎨")

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_prompt = update.message.text
    await update.message.reply_text(f"در حال ساخت تصویر برای: '{user_prompt}'... ⏳")

    try:
        # اجرای مدل در Replicate
        output = replicate.run(
            "stability-ai/sdxl:7762fdc0e9063010e1493611723688080f727483293785e918140745a3918363",
            input={"prompt": user_prompt}
        )
        image_url = output[0]
        await update.message.reply_photo(photo=image_url)
    except Exception as e:
        await update.message.reply_text(f"خطایی رخ داد: {e}")

def main():
    if not TELEGRAM_TOKEN or not REPLICATE_API_TOKEN:
        print("خطا: توکن‌ها در محیط تنظیم نشده‌اند!")
        return

    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))

    print("ربات با موفقیت روشن شد...")
    application.run_polling()

if __name__ == '__main__':
    main()
