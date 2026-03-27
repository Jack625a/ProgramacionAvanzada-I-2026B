import cv2
import os
import numpy as np
from multiprocessing import Process,Queue
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

tokenTelegram=""

def procesar(colaEntrada,colaSalida):
    while True:
        rutaImagen=colaEntrada.get()
        if rutaImagen is None:
            break
        img=cv2.imread(rutaImagen)
        conversionGris=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        bordes=cv2.Canny(conversionGris,100,100)
        salida=rutaImagen.replace(".jpg","_procesado.jpg")
        cv2.imwrite(salida,bordes)
        colaSalida.put(salida)

colaEntrante=Queue()
colaSaliente=Queue()

async def recibirImage(update:Update,context:ContextTypes.DEFAULT_TYPE):
    foto=update.message.photo[-1]
    archivo=await foto.get_file()
    ruta=f"image_{foto.file_id}.jpg"
    await archivo.download_to_drive(ruta)
    colaEntrante.put(ruta)
    resultado=colaSaliente.get()
    await update.message.reply_photo(photo=open(resultado,"rb"))
    os.remove(ruta)
    os.remove(resultado)

def main():
    proceso=Process(target=procesar,args=(colaEntrante,colaSaliente))
    proceso.start()

    app=ApplicationBuilder().token(tokenTelegram).build()
    app.add_handler(MessageHandler(filters.PHOTO, recibirImage))
    print("Bot incializado")
    app.run_polling()

if __name__=="__main__":
    main()