import pyttsx3 as voz
import subprocess as sub
import speech_recognition as sr
from datetime import datetime
import pyjokes
import requests

voice = voz.init()

def talk(text):
    voice.say(text)
    voice.runAndWait()

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Escuchando...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio, language="es-ES")
        print("Has dicho:", command)
        return command.lower()

    except sr.UnknownValueError:
        print("No se pudo entender el comando.")
        return None

    except sr.RequestError:
        talk("Lo siento, no puedo acceder al servicio de reconocimiento de voz en este momento.")
        return None


def obtener_tiempo(ciudad, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric"
    respuesta = requests.get(url)
    datos = respuesta.json()

    if datos["cod"] == 200:
        clima = datos["weather"][0]["description"]
        temperatura = datos["main"]["temp"]
        humedad = datos["main"]["humidity"]
        viento = datos["wind"]["speed"]

        print(f"El tiempo en {ciudad} es {clima}.")
        print(f"Temperatura: {temperatura}°C")
        print(f"Humedad: {humedad}%")
        print(f"Velocidad del viento: {viento} m/s")
    else:
        print("¡No se pudo obtener la información del tiempo!")

if __name__ == "__main__":
    ciudad = input("Ingrese el nombre de la ciudad: ")
    api_key = "tu_api_key_aqui"  # Reemplaza "tu_api_key_aqui" con tu propia API key de OpenWeatherMap
    obtener_tiempo(ciudad, api_key)

def runJarvis():
    command = listen()

    if command is not None:
        if 'hola' in command:
            talk("Hola, ¿cómo estás?")

        elif 'qué hora es' in command:
            hora = datetime.now().strftime("%H:%M:%S")
            talk(hora)

        elif 'fecha' in command:
            fecha = datetime.now().date()
            talk(fecha)

        elif 'gracias' in command:
            talk("De nada surmano")

        elif 'cuenta un chiste' in command:
            broma = pyjokes.get_joke(language="es", category="all")
            talk(broma)

        elif 'el tiempo' in command:
            talk(None)

        elif 'muestra el tiempo' in command:
            string = "Este es el pronóstico actual"
            talk(string)

        elif 'adiós' in command:
            talk("Nos vemos neno")
            quit()



talk("Que hay de nuevo viejo, soy Jarvis")

while True:
    runJarvis()
