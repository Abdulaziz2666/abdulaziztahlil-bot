import os
import asyncio
from aiohttp import web

from PIL import Image
import pytesseract

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)


TOKEN = os.getenv("BOT_TOKEN")
def clean_ocr_text(text):

    # Keraksiz reklama va so'zlar
    remove_words = [
        "XUSH KELIBSIZ BONUS",
        "PARIPESA",
        "DEPOZITINGIZ",
        "BONUS",
    ]

    for word in remove_words:
        text = text.replace(word, "")

    # OCR xatolarini tuzatish
    fixes = {
        "Ochilmagan varaga": "Ochilmagan darvoza",
        "BinincHi": "Birinchi",
        "gol o'tkazib yuboruvchi": "Birinchi gol o'tkazib yuboruvchi",
        "tadan ko'prog gol": "tadan ko'p gol",
        "Stastika": "Statistika",
    }

    for old, new in fixes.items():
        text = text.replace(old, new)

    # Ortiqcha bo'sh qatorlarni kamaytirish
    lines = []

    for line in text.splitlines():
        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ABDULAZIZTAHLIL bot ishlayapti ✅\n\n"
        "SofaScore rasmini yuboring 📷\n"
        "Men OCR orqali matnni o'qib beraman 🔍"
    )


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📥 Rasm qabul qilindi...\n"
        "🔍 OCR ishlayapti..."
    )

    file = await update.message.photo[-1].get_file()

    image_path = "sofascore.png"

    await file.download_to_drive(image_path)


    try:
        image = Image.open(image_path)

        # OCR uchun yaxshiroq aniqlik
        image = image.convert("L")

        text = pytesseract.image_to_string(
            image,
            lang="eng"
        )
        text = clean_ocr_text(text)


        if text.strip():

            await update.message.reply_text(
                "📊 OCR NATIJA:\n\n" + text[:4000]
            )

        else:

            await update.message.reply_text(
                "❌ Matn topilmadi.\n"
                "Aniqroq SofaScore screenshot yuboring."
            )


    except Exception as e:

        await update.message.reply_text(
            f"❌ OCR xato:\n{e}"
        )


async def health(request):
    return web.Response(
        text="ABDULAZIZTAHLIL bot ishlayapti ✅"
    )



app = Application.builder().token(TOKEN).build()


app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    MessageHandler(filters.PHOTO, photo)
)



async def main():

    await app.initialize()

    await app.start()

    await app.updater.start_polling()


    print("Bot ishlayapti")


    server = web.Application()

    server.router.add_get(
        "/",
        health
    )


    runner = web.AppRunner(server)

    await runner.setup()


    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )


    site = web.TCPSite(
        runner,
        "0.0.0.0",
        port
    )


    await site.start()


    print(
        f"Web server {port} portda ishlayapti"
    )


    await asyncio.Event().wait()



if __name__ == "__main__":
    asyncio.run(main())
