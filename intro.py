import re
import pyttsx3

def introduccion_narrador(texto):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    spanish_voice = None
    for voice in voices:
        if ("spanish" in voice.name.lower() or "español" in voice.name.lower() or 
            (hasattr(voice, 'languages') and any("es" in lang.decode('utf-8').lower() for lang in voice.languages))):
            spanish_voice = voice.id
            break

    if spanish_voice:
        engine.setProperty('voice', spanish_voice)
    else:
        print("No se encontró una voz en español, usando la voz predeterminada.")

    engine.setProperty('rate', 150)
    engine.say(texto)
    engine.runAndWait()

import re

def extraer_seccion(texto_completo, titulo):
    """
    Extrae el contenido de la sección que comienza con '### {titulo}'
    hasta el siguiente encabezado o hasta el final del texto, eliminando los asteriscos dobles (**).
    """
    # Patrón: encuentra '### Título' y captura todo hasta el siguiente '###' o final
    patron = r"###\s*" + re.escape(titulo) + r"\s*\n(.*?)(?=\n###|\Z)"
    resultado = re.search(patron, texto_completo, re.DOTALL)
    
    if resultado:
        texto_limpio = re.sub(r"\*\*", "", resultado.group(1))  # Eliminar los asteriscos dobles
        return texto_limpio.strip()
    
    return None


def intro_speak(texto_completo):
    # Extraer solo las secciones dinámicas
    seccion_introduccion = extraer_seccion(texto_completo, "Introducción Narrativa")
    seccion_objetivo     = extraer_seccion(texto_completo, "Objetivo Principal")
    seccion_inicio       = extraer_seccion(texto_completo, "Inicio del Juego")

    # Llamar a la función de narración para cada sección extraída
    if seccion_introduccion:
        introduccion_narrador(seccion_introduccion)
    else:
        print("No se encontró la sección 'Introducción Narrativa'.")

    if seccion_objetivo:
        introduccion_narrador(seccion_objetivo)
    else:
        print("No se encontró la sección 'Objetivo Principal'.")

    if seccion_inicio:
        introduccion_narrador(seccion_inicio)
    else:
        print("No se encontró la sección 'Inicio del Juego'.")
