import os
import logging
import requests
import base64
from io import BytesIO
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CLOUDFLARE_API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
CLOUDFLARE_ACCOUNT_ID = os.getenv('CLOUDFLARE_ACCOUNT_ID')

logging.basicConfig(level=logging.INFO)

MODEL = '@cf/black-forest-labs/flux-1-schnell'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text('سلام! متن تصویر را بفرست تا برات تصویر بسازم 🎨')

async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
prompt = update.message.text
await update.message.reply_text('در حال ساخت تصویر... ⏳')

```
try:
    url = f'https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/run/{MODEL}'

    headers = {
        'Authorization': f'Bearer {CLOUDFLARE_API_TOKEN}',
        'Content-Type': 'application/json'
    }

    payload = {
        'prompt': prompt,
        'width': 1024,
        'height': 1024,
        'num_steps': 4
    }

    response = requests.post(url, headers=headers, json=payload, timeout=180)

    if response.status_code != 200:
        await update.message.reply_text(
            f'خطای Cloudflare ({response.status_code}):\\n{response.text}'
        )
        return

    data = response.json()

    if not data.get('success'):
        await update.message.reply_text(f'خطا: {data}')
        return

    result = data.get('result')

    if isinstance(result, dict) and 'image' in result:
        image_bytes = base64.b64decode(result['image'])
    elif isinstance(result, str):
        image_bytes = base64.b64decode(result)
    else:
        await update.message.reply_text(f'فرمت خروجی ناشناخته: {result}')
        return

    image = BytesIO(image_bytes)
    image.name = 'generated.png'
    image.seek(0)

    await update.message.reply_photo(photo=image, caption='تصویر آماده شد ✅')

except Exception as e:
    logging.exception(e)
    await update.message.reply_text(f'خطا: {e}')
```

def main():
app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))
app.run_polling()

if **name** == '**main**':
main()
