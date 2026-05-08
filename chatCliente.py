#Paso 1. Importacion de las librerias
import socket
import threading

#Paso 2. Definir el host y el puerto
host="192.168.56.1" #ip del servidor
puerto=5000

#Paso 3. Definir la funcion para recibir mensajes
def recibirMensajes(cliente):
    while True:
        try:
            mensaje=cliente.recv(1024).decode("utf-8")
            print(mensaje)
        except:
            print("Error al recibir el mensaje")
            cliente.close()    
            break

#Paso 4. Funcion Enviar Mensaje
def enviarMensaje(cliente):
    while True:
        mensaje=input("Ingrese su mensaje: ")
        cliente.send(mensaje.encode("utf-8"))

#Paso 5. Funcion para configiraConexionServidor
def iniciar():
    cliente=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #IP VERSION 4
    cliente.connect((host,puerto))
    print("Conectado al chat...")
    hiloRecibirMensaje=threading.Thread(target=recibirMensajes,args=(cliente,))
    hiloRecibirMensaje.start()
    enviarMensaje(cliente)

iniciar()