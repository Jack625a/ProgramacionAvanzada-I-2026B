#Importacion de las librerias
from telegram import Update
from telegram.ext import ApplicationBuilder,MessageHandler,filters,ContextTypes
from multiprocessing import Process, Queue
import time

#Creacion de la funcion pesado
def tareaN(texto,cola):
    print("Procesando tarea")
    time.sleep(7)
    resultado=f"Procesando {texto}"
    cola.put(resultado)

async def responder(update:Update,context:ContextTypes.DEFAULT_TYPE):
    mensaje=update.message.text
    cola=Queue()
    #Creacion de los procesos
    proceso=Process(target=tareaN,args=(mensaje,cola))
    proceso.start()
    proceso.join()
    resultado=cola.get()
    await update.message.reply_text(resultado)

#funcion principal
def main():
    apiTelegram=""
    app=ApplicationBuilder().token(apiTelegram).build()
    app.add_handler(MessageHandler(filters.TEXT,responder))
    print("Bot esta funcionando...")
    app.run_polling()


if __name__=="__main__":
    main()