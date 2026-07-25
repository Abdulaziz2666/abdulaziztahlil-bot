import os
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


app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, photo))

print("Bot ishga tushdi")
app.run_polling()
