from telegram import Update
from telegram.ext import ApplicationBuilder,CommandHandler,ContextTypes

#paso 1. configurr el token de telegram
tokenTelegram=""

#paso 2. configurar los comandos
#/start
async def comandostart(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bienvenido al bot..."
    )

#comando /imagen
async def comndoimagen(update:Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo("entrada.jpg")
    

#paso 3. configurar el bot
def main():
    app=ApplicationBuilder().token(tokenTelegram).build()
    #Paso 4. Agregar el comando
    app.add_handler(CommandHandler("start",comandostart))
    app.add_handler(CommandHandler("imagen",comndoimagen))

    app.run_polling()

if __name__=="__main__":
    main()