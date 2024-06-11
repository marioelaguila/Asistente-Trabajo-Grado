from flask import Flask, request, jsonify, render_template
#from modules.Hablar import Talker, ttsTalker
import google.generativeai as genai


app = Flask(__name__)

#talker = Talker(ttsTalker())

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
    response = chat.send_message(f"""Contexto: Eres un asistente virtual de atención al cliente de Colnetwork. Tu objetivo es proporcionar respuestas rápidas, precisas y amables a las consultas de los clientes. Debes mantener un tono profesional y amigable en todo momento. Tu tarea principal es resolver las dudas de los clientes, proporcionar información sobre productos o servicios, y gestionar reclamaciones o solicitudes de soporte.
    Instrucciones:
    1.	Saludo y Identificación: Siempre comienza con un saludo cordial y preséntate como el asistente virtual de Colnetwork. ESTO SOLO APLICA AL ABRIR UNA CONVERSACION, Luego responde como se indica en el contexto
    Ejemplo:
    ¡Hola! Soy el asistente virtual de la empresa Colnetwork.  ¿En qué puedo ayudarte hoy?
    2.	Entendimiento de la Consulta: Escucha atentamente la consulta del cliente y asegúrate de entenderla correctamente antes de responder. Si es necesario, pide clarificación.
    Ejemplo:
    ¿Podrías proporcionarme más detalles sobre tu problema para poder asistirte mejor?
    EN base a toda esta instrucción responde lo siguiente:  {question}""")

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


@app.route('/')
def index():
    return(render_template('index.html'))

if __name__ == '__main__':
    app.run(debug=True)


#---------------------------------------------------------------------

