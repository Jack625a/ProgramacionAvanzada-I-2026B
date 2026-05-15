from telegram import Bot
import asyncio

chatId=""
tokenTelegram=""

async def enviarMensajePrivado(mensaje):
    async with Bot(token=tokenTelegram) as bot:
        await bot.send_message(
            chat_id=chatId,
            text=mensaje
        )

mensaje=input("Ingrese su mensaje: ")
asyncio.run(enviarMensajePrivado(mensaje))
