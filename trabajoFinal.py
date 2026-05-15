from flask import Flask
from flask_socketio import SocketIO, send
import eventlet

# Conexion con SocketIO
eventlet.monkey_patch()

# Crear app
app = Flask(__name__)

# Configurar SocketIO
socket = SocketIO(
    app,
    cors_allowed_origins="*"
)

# Ruta principal
@app.route("/")
def index():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat UDABOL - Tiempo Real</title>
    <style>
        :root {
            --primary-color: #0B2545; /* Azul Institucional UDABOL */
            --secondary-color: #134074; /* Azul Claro */
            --accent-color: #EEB902; /* Dorado/Amarillo de acento */
            --bg-color: #F4F6F9;
            --text-color: #333333;
            --white: #FFFFFF;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            padding: 20px;
        }

        /* Contenedor Principal del Chat */
        .chat-container {
            width: 100%;
            max-width: 450px;
            height: 85vh;
            background-color: var(--white);
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            border-top: 5px solid var(--accent-color);
        }

        /* Encabezado */
        .chat-header {
            background-color: var(--primary-color);
            color: var(--white);
            padding: 15px 20px;
            text-align: center;
        }

        .chat-header h2 {
            font-size: 1.3rem;
            font-weight: 600;
            letter-spacing: 0.5px;
        }

        .chat-header p {
            font-size: 0.8rem;
            color: rgba(255, 255, 255, 0.7);
            margin-top: 2px;
        }

        /* Sección de Registro de Nombre */
        .login-section {
            display: flex;
            padding: 15px;
            background-color: #EEF2F7;
            border-bottom: 1px solid #E1E6ED;
            gap: 10px;
            transition: all 0.3s ease;
        }

        .login-section.hidden {
            display: none;
        }

        /* Área de Mensajes */
        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            background-color: #FAFBFD;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        /* Estilo de los Mensajes */
        .message {
            background-color: #E9ECEF;
            padding: 10px 14px;
            border-radius: 8px;
            max-width: 85%;
            width: fit-content;
            line-height: 1.4;
            font-size: 0.95rem;
            animation: fadeIn 0.2s ease-in-out;
        }

        /* Resaltado para mis propios mensajes (Simulación visual de flujo) */
        .message.own {
            background-color: #D2E3FC;
            align-self: flex-end;
        }

        .message-user {
            font-weight: bold;
            color: var(--primary-color);
            display: block;
            font-size: 0.8rem;
            margin-bottom: 2px;
        }

        /* Área de Entrada de Mensajes */
        .input-section {
            display: flex;
            padding: 15px;
            background-color: var(--white);
            border-top: 1px solid #E1E6ED;
            gap: 10px;
        }

        /* Componentes de Formulario Comunes */
        input[type="text"] {
            flex: 1;
            padding: 12px 16px;
            border: 1px solid #CCD1D9;
            border-radius: 6px;
            font-size: 0.95rem;
            outline: none;
            transition: border-color 0.2s;
        }

        input[type="text"]:focus {
            border-color: var(--secondary-color);
            box-shadow: 0 0 0 3px rgba(19, 64, 116, 0.1);
        }

        button {
            padding: 12px 20px;
            background-color: var(--primary-color);
            color: var(--white);
            border: none;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.95rem;
            cursor: pointer;
            transition: background-color 0.2s, transform 0.1s;
        }

        button:hover {
            background-color: var(--secondary-color);
        }

        button:active {
            transform: scale(0.98);
        }

        /* Animación suave al recibir mensajes */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(5px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>

<div class="chat-container">
    <!-- Encabezado Institucional -->
    <div class="chat-header">
        <h2>UDABOL</h2>
        <p>Chat en Tiempo Real</p>
    </div>

    <!-- Sección de Acceso -->
    <div class="login-section" id="loginSection">
        <input type="text" id="nombre" placeholder="Ingresa tu nombre completo" autocomplete="off">
        <button onclick="guardarNombre()">Entrar</button>
    </div>

    <!-- Cuerpo del Chat -->
    <div class="chat-messages" id="chat">
        <!-- Los mensajes aparecerán aquí de forma dinámica -->
    </div>

    <!-- Sección de Envío -->
    <div class="input-section">
        <input type="text" id="mensaje" placeholder="Escribe un mensaje aquí..." autocomplete="off">
        <button onclick="enviar()">Enviar</button>
    </div>
</div>

<script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
<script>
    var socket = io();
    var nombre = "";

    // Escuchar el evento 'Enter' en los inputs para mejorar UX
    document.getElementById("nombre").addEventListener("keypress", function(e) {
        if (e.key === "Enter") guardarNombre();
    });

    document.getElementById("mensaje").addEventListener("keypress", function(e) {
        if (e.key === "Enter") enviar();
    });

    function guardarNombre(){
        let input = document.getElementById("nombre");
        if(input.value.trim() === ""){
            alert("Por favor, ingrese su nombre para continuar.");
            input.focus();
            return;
        }
        nombre = input.value.trim();
        
        // Usabilidad: Ocultamos la barra de ingreso de nombre una vez registrado
        document.getElementById("loginSection").classList.add("hidden");
        document.getElementById("mensaje").focus();
    }

    function enviar(){
        let mensajeInput = document.getElementById("mensaje");
        let mensaje = mensajeInput.value;

        if(nombre === ""){
            alert("Debe ingresar su nombre primero.");
            document.getElementById("loginSection").classList.remove("hidden");
            document.getElementById("nombre").focus();
            return;
        }

        if(mensaje.trim() === ""){
            return;
        }

        // Formato estructurado para identificar fácilmente emisor y contenido
        socket.send(JSON.stringify({ user: nombre, text: mensaje }));
        mensajeInput.value = "";
    }

    socket.on("message", function(msg){
        let chat = document.getElementById("chat");
        let p = document.createElement("p");
        p.classList.add("message");

        try {
            // Intentar parsear si viene como JSON structurado
            let data = JSON.parse(msg);
            
            let spanUser = document.createElement("span");
            spanUser.classList.add("message-user");
            spanUser.innerText = data.user;
            
            p.appendChild(spanUser);
            p.append(data.text);
            
            // Si el mensaje es del usuario actual, añadimos una clase visual distintiva
            if(data.user === nombre) {
                p.classList.add("own");
            }
        } catch(e) {
            // Fallback por si el servidor devuelve texto plano plano
            p.innerText = msg;
        }

        chat.appendChild(p);

        // Usabilidad: Scroll automático al fondo al recibir nuevos mensajes
        chat.scrollTop = chat.scrollHeight;
    });
</script>

</body>
</html>
"""

# Evento de mensajes
@socket.on("message")
def recibirMensaje(mensaje):

    print("Mensaje:", mensaje)

    send(mensaje, broadcast=True)

# Ejecutar servidor
if __name__ == "__main__":

    print("Servidor iniciado")

    socket.run(
        app,
        host="0.0.0.0",
        port=5000
    )