#Paso 1. Importar las depencias
import cv2
import os
from multiprocessing import Process
from telegram import Update
from telegram.ext import ApplicationBuilder,MessageHandler,filters,ContextTypes
import uuid #Generar id aleatorios 

tokenTelegram=""

def procesarImagen(rutaEntrada,rutaSalida):
    try:
        #cargar el modelo de reconocimiento facial
        reconocimiento=cv2.CascadeClassifier(
            cv2.data.haarcascades+'haarcascade_frontalface_default.xml'
        )
            #Leer la imagen
        imagen=cv2.imread(rutaEntrada)
        if imagen is None:
            print("Error al cargar la imagen")
            return False

        grises=cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)
        rostros=reconocimiento.detectMultiScale(grises,1.1,5)
        
        #dibujar las detecciones
        for (x,y,w,h) in rostros:
            cv2.rectangle(imagen,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.imwrite(rutaSalida,imagen)
        print("Procesamiento terminado")
        return True
    except Exception as error:
        print("Error al procesar ",error)
        return False

    #ESCALAS DE DETECCION
    #1.1=> Mas preciso(detecta mas rostros pequeños, pero es mas lento y mas uso de recursos)
    #1.3=>balanceado (detecta rostos pero puede omitir algunos muy pequeños)
    #1.5=> la mas rapida pero menos precios

    #Escala de seguridad (Cuantas veces se va a repetir la deteccion)
    #3=> detecta mas pero brinda falsos positivos 
    #5=> balanceado
    #8=> mas estricto en confirmacion

async def obtenerImagen(update:Update,context:ContextTypes.DEFAULT_TYPE):
    foto=update.message.photo[-1]
    archivo=await foto.get_file()
    nombre=str(uuid.uuid4())

    ruta_Entrada=f"entrada_{nombre}.jpg"
    ruta_Salida=f"salida_{nombre}.jpg"
    await archivo.download_to_drive(ruta_Entrada)
    #Crear el proceso
    proceso=Process(target=procesarImagen,args=(ruta_Entrada,ruta_Salida))
    proceso.start()
    proceso.join()
    await update.message.reply_photo(photo=open(ruta_Salida,"rb"))

def main():
    app=ApplicationBuilder().token(tokenTelegram).build()
    app.add_handler(MessageHandler(filters.PHOTO,obtenerImagen))
    print("Bot iniciado")
    app.run_polling()

if __name__=="__main__":
    main()