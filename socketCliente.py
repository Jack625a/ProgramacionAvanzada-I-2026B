#PASO 1. IMPORTAR LIBRERIA
import socket

cliente=socket.socket()
cliente.bind(("0.0.0.0",5000))
#Enviar el mensaje codificado
mensaje=input("Escribe tu mensaje: ")
cliente.send(mensaje.encode())

respuesta=cliente.recv(1024).decode()
print("Servidor: ",respuesta)
