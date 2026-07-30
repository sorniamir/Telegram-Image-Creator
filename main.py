import os
import logging
import replicate
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# خواندن توکن‌ها از Railway Variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# تنظیم توکن Replicate
if REPLICATE_API_TOKEN:
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# تنظیم لاگ
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! من ربات تصویرساز هستم. 🎨\n\n"
        "هر متنی که دوست داری بفرست تا برات تصویر بسازم."
    )


async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_prompt = update.message.text

    await update.message.reply_text(
        f"در حال ساخت تصویر برای:\n\n{user_prompt}\n\nلطفاً چند ثانیه صبر کن... ⏳"
    )

    try:
        # اجرای مدل FLUX Schnell
        output = replicate.run(
            "black-forest-labs/flux-schnell",
            input={
                "prompt": user_prompt
            },
        )

        # خروجی ممکن است لیست یا رشته باشد
        if isinstance(output, list):
            image_url = output[0]
        else:
            image_url = str(output)

        await update.message.reply_photo(photo=image_url)

    except Exception as e:
        logger.exception("Replicate error")
        await update.message.reply_text(f"خطای Replicate:\\n{e}")


def main():
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN تنظیم نشده است.")
        return

    if not REPLICATE_API_TOKEN:
        logger.error("REPLICATE_API_TOKEN تنظیم نشده است.")
        return

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image)
    )

    logger.info("ربات با موفقیت روشن شد.")
    application.run_polling()


if __name__ == "__main__":
    main()
