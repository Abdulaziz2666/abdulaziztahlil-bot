import os
import asyncio
from aiohttp import web
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ABDULAZIZTAHLIL bot ishlayapti ✅\n"
        "SofaScore rasmini yuboring 📷"
    )


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = await update.message.photo[-1].get_file()
    await photo.download_to_drive("sofascore.png")

    await update.message.reply_text(
        "📊 SofaScore tahlili\n\n"
        "⏳ OCR moduli kutmoqda..."
    )


async def health(request):
    return web.Response(text="ABDULAZIZTAHLIL bot ishlayapti ✅")


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, photo))


async def main():
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    print("Bot ishlayapti")

    server = web.Application()
    server.router.add_get("/", health)

    runner = web.AppRunner(server)
    await runner.setup()

    port = int(os.environ.get("PORT", 10000))

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        port
    )

    await site.start()

    print(f"Web server {port} portda ishlayapti")

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
