import io
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import tempfile

#con la libreria SpeechRecognizer creamos una variable que escuche el audio del micro
listener = sr.Recognizer()

class Listener:

    def listen_mic(self):
        try:
            with sr.Microphone() as micro:
                print("Escuchando...")
                listener.adjust_for_ambient_noise(micro)
                audio = listener.listen(micro)
                data = io.BytesIO(audio.get_wav_data())
                audio_clip = AudioSegment.from_file(data)

                #codigo para crear el archivo .wav temporal que usa el Whisper
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                    save = temp_file.name
                    audio_clip.export(save, format="wav")

            return save
        except Exception as error:
            print(error)
            return None  # Manejar el error si la grabación falla

    def __recognize_audio(self, save):
        model_audio = whisper.load_model('base')
        result = model_audio.transcribe(save, language="spanish", fp16= False)  #usando el modelo para transcribir texto
        return result['text']
    
    def listen(self):
        return self.__recognize_audio(self.listen_mic()).lower()