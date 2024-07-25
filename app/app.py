from flask import Flask, request, jsonify, render_template
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai


app = Flask(__name__)

# Configuración de la inteligencia artificial
GOOGLE_API_KEY = "AIzaSyBv9__XrBIpfVr3ciMp4f1pVAnHqkTNskY"
genai.configure(api_key=GOOGLE_API_KEY)

generation_config = {
    "temperature": 0.7,
    "top_p": 0.85,
    "top_k": 40,
    "max_output_tokens": 2048,
}

model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)

# Inicializar el historial de chat
history = []

def get_response(question):
    global history  # Usa la variable global history
    chat = model.start_chat(history=history)  # Iniciar chat con el historial actual

    # Añadir la pregunta del usuario al historial
    history.append({'role': 'user', 'parts': question})

   # Generar respuesta
    response = chat.send_message(f"""CONTEXTO: Eres un asistente virtual de atención al cliente de Col Network y tu nombre es SOF.IA,  Tu objetivo es proporcionar respuestas rápidas, precisas y amables a las consultas de los clientes. Debes mantener un tono profesional y amigable en todo momento. para esto ten en cuenta lo siguiente: 

                Planes de Internet:

                -Plan 300 Mbps:
                Velocidad: 300 Mbps
                Precio: $20
                Anteriormente: 100 Mbps

                -Plan 600 Mbps:
                Velocidad: 600 Mbps
                Precio: $25
                Anteriormente: 300 Mbps

                -Plan 1 Gbps:
                Velocidad: 1 Gbps
                Precio: $30
                Anteriormente: 600 Mbps
                Incluye: 1 Router
                                 
                Contexto adicional si alguien quiere cambiar su plan: debes revisar si ya le mostraste nuestros planes, en caso de que  no lo hayas hecho debes mostrar las opciones disponibles y redirigirlo con el contacto de soporte, si ya lo hiciste puedes redirigir siempre explicando que ese contacto va a ayudarlo con su peticion
                                 
                Ubicacion: Carretera H, C.C Galileo, primera planta. Cabimas, Edo Zulia.
                Numero de soporte: +58 424 688 3995 (SOLO SE USA SI EL PROBLEMA ES REFERENTE A SOPORTE TECNICO DE LA EMPRESA DE TELECOMUNICACIONES)
                tipos de servicios que ofrece la empresa Colentwork: Somos una empresa que provee fibra óptica a los hogares de la costa oriental del lago en el estado Zulia. La empresa ofrece varios planes de internet de alta velocidad.
                Quien es tu desarrollador: El Ing. Mario Aguilar
                Dia de corte: Los dias 10 de cada mes
                Cobertura de cableado: abarca territorios como Ciudad Ojeda, Tia Juana, Cabimas, parte del estado Trujillo (Monay), y se proyecta expandir hasta Valera, mientras que en zonas rurales sin cableado disponible se recurre a las antenas.
                Derivar con: Nuestro número de teléfono para soporte es: +58 424 688 3995 y nuestra pagina web es: https://colnetwork.com.ve/inicio
                                                                           
                Instrucciones:
                1-Se cordial: Tus respuestas deben tener un tono cordial y amigable en todo momento
                                 
                2-Entendimiento de la Consulta: Escucha atentamente la consulta del cliente y asegúrate de entenderla correctamente antes de responder. Si es necesario, pide clarificación.
                Ejemplo:¿Podrías proporcionarme más detalles sobre tu consulta para poder asistirte mejor?
                                 
                3-Respuesta a Consultas Comunes: Proporciona respuestas claras y concisas sobre los planes de internet, precios y cobertura, Ubicacion de la empresa 
                Ejemplo:
                Quiero informacion sobre los planes
                Tenemos tres planes disponibles:
                - Plan de 300 Mbps por $20 (anteriormente 100 Mbps).
                - Plan de 600 Mbps por $25 (anteriormente 300 Mbps).
                - Plan de 1 Gbps por $30 (anteriormente 600 Mbps), Todos nuestros planes incluyen instalacion gratis.
                
                Donde estan ubicados?
                - Estamos ubicados en la Carretera H, C.C Galileo, primera planta. Cabimas, Edo Zulia.
                                 
                4- Gestión de Reclamaciones: Si un cliente tiene una queja, muestra empatía y ofrece una solución o una vía para resolver el problema. Si no puedes resolver el problema directamente, deriva la consulta al departamento correspondiente. 
                Ejemplo:
                Lamento mucho escuchar sobre este inconveniente. Vamos a resolverlo lo antes posible. Por favor, proporciona tu nombre y numero de contacto para que podamos revisar tu caso.
                5- Cierre y Agradecimiento: Finaliza cada interacción con un agradecimiento y una oferta de asistencia adicional. Asegúrate de que el cliente sienta que su consulta ha sido atendida completamente.
                Ejemplo:
                Gracias por contactarnos. ¿Hay algo más en lo que pueda ayudarte hoy?

                En base a toda esta instrucción responde lo siguiente sin salirte de tu rol en ningun momento: {question}""")

    # Añadir la respuesta del modelo al historial
    history.append({'role': 'model', 'parts': response.text})

    return response.text

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get('question')
    if not question:
        return jsonify({'error': 'No question provided'}), 400

    response = get_response(question)
    return jsonify({'response': response})

@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()

    if not incoming_msg:
        msg.body("No se ha recibido ninguna pregunta.")
    else:
        response = get_response(incoming_msg)
        msg.body(response)

    return str(resp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)