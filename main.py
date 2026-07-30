import os
import logging
import requests
from io import BytesIO
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# تنظیم لاگ
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# متغیرهای محیطی
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")

MODEL = "@cf/black-forest-labs/flux-1-schnell"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! 👋\n\nمتن تصویر را بفرست تا برات تصویر بسازم 🎨"
    )


async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text

    await update.message.reply_text("در حال ساخت تصویر... ⏳")

    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{CLOUDFLARE_ACCOUNT_ID}/ai/run/{MODEL}"
    )

    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "image/png",
    }

    payload = {
        "prompt": prompt
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=180,
        )

        print("STATUS:", response.status_code)
        print("CONTENT-TYPE:", response.headers.get("content-type"))

        if response.status_code != 200:
            await update.message.reply_text(
                f"خطای Cloudflare ({response.status_code}):\n{response.text}"
            )
            return

        image = BytesIO(response.content)
        image.name = "generated.png"
        image.seek(0)

        await update.message.reply_photo(photo=image)

    except Exception as e:
        logging.exception(e)
        await update.message.reply_text(f"خطا: {e}")


def main():
    if not TELEGRAM_TOKEN:
        print("خطا: TELEGRAM_TOKEN تنظیم نشده است")
        return

    if not CLOUDFLARE_API_TOKEN:
        print("خطا: CLOUDFLARE_API_TOKEN تنظیم نشده است")
        return

    if not CLOUDFLARE_ACCOUNT_ID:
        print("خطا: CLOUDFLARE_ACCOUNT_ID تنظیم نشده است")
        return

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image)
    )

    print("ربات روشن شد.")
    app.run_polling()


if __name__ == "__main__":
    main()
