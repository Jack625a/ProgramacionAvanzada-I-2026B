#PASO 1. IMPORTAR LA LIBRERIA
import socket

#PASO 2. CREAR EL SERVIDOR
servidor=socket.socket()
servidor.bind(("0.0.0.0",5000)) #Definir host-puerto
servidor.listen(1)

print("Escuchando solicitudes")

#PASO 3. Aceptar las solicitudes de los usuarios
cliente,_=servidor.accept()

#PASO 4. DECODIFICAR EL MENSAJE
mensaje=cliente.recv(1024).decode()
print("El mensaje es ",mensaje)

#PASO 5. ENVIAR LA RESPUESTA CODIFICADA AL CLIENTE
cliente.send("Hola".encode())