from flask import Flask
from flask import request
from flask import render_template, send_from_directory
import base64
import openai
import conexion
app = Flask(__name__)
OPENAI_KEY = "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"
OPENAI_API_URL = "https://api.openai.com/v1"
openai.api_key = OPENAI_KEY
openai.api_base = OPENAI_API_URL

estado_tramite = conexion.estado_tramite("001")
if estado_tramite == "en_demora":
    datos = conexion.en_demora("001")
elif estado_tramite == "listo":
    datos = conexion.listo("001")
else:
    datos = conexion.observado("001") 


system_message = f"""
Eres un asistente virtual de una agencia de tramites. \
se te dio informacion sobre un tramite el cual su estado es {estado_tramite}\
informacion que ahora te proporcionamos \
Si no conoces una respuesta muestra el texto: 'No tengo esta información, le recomendamos contactarse con un asistente.' \

el estado del tramite es en_demora mandale el siguiente mensaje: tu tramite esta en demora, la fecha limite para tenerlo listo es {datos[0]}  \
el estado del tramite es listo mandale el siguiente mensaje: tu tramite esta listo la fecha de aceptacion fue el {datos[0]} y debe recogerlo el {datos[1]}\
el estado del tramite es observado y la descripcion es {datos[0]}, si la descripcion es error fecha dile que tiene un error en la fecha y debe ir a segip a corregir"""

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/resources/<path:path>', methods=['GET'])
def resources(path):
    return send_from_directory('resources', path)

@app.route('/transcribe', methods=['POST'])
def post_audio_file():
    file = request.json['data']

    decoded_bytes = base64.b64decode(file)
    with open('music.webm', 'wb') as wav_file:
        wav_file.write(decoded_bytes)
        
    audio_file = open('music.webm', "rb")

    transcript = openai.Audio.transcribe('whisper-1',audio_file, OPENAI_KEY)
    
    return transcript

@app.route('/chat', methods=['POST'])
def chat():
    prompt = f"el estado de mi tramite es {estado_tramite} que debo hacer?"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']

if __name__ == '__main__':
    app.run('0.0.0.0', 8000)
