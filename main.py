import os
import logging
import requests
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
url = f'https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/run/{MODEL}'

headers = {
    'Authorization': f'Bearer {CLOUDFLARE_API_TOKEN}',
    'Content-Type': 'application/json',
    'Accept': 'image/png'
}

payload = {
    'prompt': prompt
}

response = requests.post(url, headers=headers, json=payload, timeout=180)

print('STATUS:', response.status_code)
print('CONTENT-TYPE:', response.headers.get('content-type'))

if response.status_code != 200:
    await update.message.reply_text(response.text[:500])
    return

image = BytesIO(response.content)
image.name = 'image.png'
image.seek(0)

await update.message.reply_photo(photo=image)
```

def main():
app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_image))
app.run_polling()

if **name** == '**main**':
main()
