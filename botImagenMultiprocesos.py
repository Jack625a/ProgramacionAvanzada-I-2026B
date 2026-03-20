#Importar las dependencias
from telegram import Update
from telegram.ext import ApplicationBuilder,MessageHandler,filters,ContextTypes
from multiprocessing import Process, Queue
import cv2

tokenTelegram=""

cola=Queue()
#funcion pesada
def procesar(chat_id,entrada,salida):
    img=cv2.imread(entrada)
    grises=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imwrite(salida,grises)
    cola.put(chat_id,salida)

async def recibir(update:Update,context:ContextTypes.DEFAULT_TYPE):
    chat_id=update.message.chat_id
    foto=update.message.photo[-1]
    archivo=await foto.get_file()
    entrada="entrada.jpg"
    salida="salida.jpg"
    await archivo.download_to_drive(entrada)
    proceso=Process(target=procesar,args=(chat_id,entrada,salida))
    proceso.start()
    await update.message.reply_text("Se esta procesando la imagen...")

async def enviar(context:ContextTypes.DEFAULT_TYPE):
    if not cola.empty():
        chat_id,salida=cola.get()
        await context.bot.send_photo(chat_id=chat_id,photo=open(salida,"rb"))

def main():
    app=ApplicationBuilder().token(tokenTelegram).build()
    app.add_handler(MessageHandler(filters.PHOTO,recibir))
    app.job_queue.run_repeating(enviar,1)
    app.run_polling()

main()