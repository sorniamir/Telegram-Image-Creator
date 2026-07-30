import os
import logging
from io import BytesIO

from openai import OpenAI
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! 👋\n\nمتن تصویر را بفرست تا برات تصویر بسازم 🎨"
    )


async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text

    await update.message.reply_text("در حال ساخت تصویر... ⏳")

    try:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024",
        )

        image_base64 = result.data[0].b64_json

        import base64

        image_bytes = base64.b64decode(image_base64)
        image_file = BytesIO(image_bytes)
        image_file.name = "image.png"
        image_file.seek(0)

        await update.message.reply_photo(
            photo=image_file,
            caption="تصویر آماده شد ✅"
        )

    except Exception as e:
        logging.exception(e)
        await update.message.reply_text(f"خطا: {e}")


def main():
    if not TELEGRAM_TOKEN:
        raise RuntimeError("TELEGRAM_TOKEN تنظیم نشده است")

    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY تنظیم نشده است")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image)
    )

    print("ربات روشن شد.")
    app.run_polling()


if __name__ == "__main__":
    main()
