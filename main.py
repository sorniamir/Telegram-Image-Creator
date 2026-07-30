import os
import logging
import requests
from io import BytesIO
from urllib.parse import quote

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text(
"سلام! 👋\n\nمتن تصویر را بفرست تا برات تصویر بسازم 🎨"
)

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
prompt = update.message.text

```
await update.message.reply_text("در حال ساخت تصویر... ⏳")

try:
    encoded_prompt = quote(prompt)
    url = (
        f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        f"?width=1024&height=1024&model=flux"
    )

    response = requests.get(url, timeout=180)

    if response.status_code != 200:
        await update.message.reply_text(
            f"خطا در ساخت تصویر: {response.status_code}"
        )
        return

    image = BytesIO(response.content)
    image.name = "image.png"
    image.seek(0)

    await update.message.reply_photo(photo=image)

except Exception as e:
    logging.exception(e)
    await update.message.reply_text(f"خطا: {e}")
```

def main():
if not TELEGRAM_TOKEN:
raise RuntimeError("TELEGRAM_TOKEN تنظیم نشده است")

```
app = Application.builder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image)
)

print("ربات روشن شد...")
app.run_polling()
```

if **name** == "**main**":
main()
