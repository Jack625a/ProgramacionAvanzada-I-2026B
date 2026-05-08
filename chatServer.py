#Paso 1. Importar las librerias
import socket
import threading

#Paso 2. Definir el host y puerto de conexion en la red 
host="0.0.0.0"
puerto=5000

clientes=[]

#Paso 3. Funcion para enviar el mensaje a Todos
def enviarTodos(mensaje,clienteActual):
    for cliente in clientes:
        if cliente!=clienteActual:
            try:
                cliente.send(mensaje)
            except:
                clientes.remove(cliente)
                
#Paso 4. Crear la funcion que permita manejar las solicitudes
def manejarCliente(cliente):
    while True:
        try:
            mensaje=cliente.recv(1024)
            if mensaje:
                enviarTodos(mensaje,cliente)
        except:
            clientes.remove(cliente)
            cliente.close()
            break

#Paso 5. Crear la funcion para inicar el servidor
def inicarServidor():
    servidor=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    servidor.bind((host,puerto))
    servidor.listen()
    print("Servidor activo escuchando solicitudes")

    #Verificacion de conexiones
    while True:
        cliente,direccion=servidor.accept()
        print(f"Conectado con la ip {direccion}")
        clientes.append(cliente)
        hilo=threading.Thread(target=manejarCliente,args=(cliente,))
        hilo.start()


inicarServidor()