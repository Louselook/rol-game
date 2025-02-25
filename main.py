from openai import OpenAI
from decouple import config
import os
import json
from datetime import datetime
import pyttsx3
from intro import intro_speak

# Configuración inicial
HISTORY_FILE = "tu_historia.txt"
NARRATIVE_FILE = "narrativa/narrativa.txt"
INITIAL_PROMPT = """
### Instrucciones para el Asistente de Narrativa

1. Mantener coherencia con la historia existente en el archivo de historial
2. Incorporar progresivamente las acciones de los jugadores
3. Respetar las características del universo establecidas
4. Desarrollar personajes de manera orgánica
5. Mantener tensión narrativa y elementos de terror cósmico
6. Incluir consecuencias realistas de las acciones
7. Usar descripciones vívidas y sensoriales
"""

def texto_a_voz(texto):
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

def inicializar_historial():
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            f.write("=== INICIO DEL HISTORIAL ===\n\n")
        print(f"Archivo de historial {HISTORY_FILE} creado.")
        
def cargar_historial():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error cargando historial: {e}")
        return ""

def guardar_historial(contenido):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(HISTORY_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n[ENTRADA - {timestamp}]\n{contenido}\n")
        print(f"Historia actualizada en {HISTORY_FILE}")
    except Exception as e:
        print(f"Error guardando historial: {str(e)}")

def cargar_narrativa():
    try:
        with open(NARRATIVE_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error cargando narrativa: {e}")
        return None

def evaluar_probabilidad(accion_jugador):
    """Evalúa la probabilidad de éxito usando API"""
    client = OpenAI(api_key=config('OPENAI_API_KEY'))
    
    prompt = f"""
    Evalúa la probabilidad de éxito basado en estadísticas:
    Estadísticas: {json.dumps(accion_jugador['estadisticas'], indent=2)}
    Acción intentada: {accion_jugador['accion']}
    
    Considera:
    - Complejidad de la acción
    - Estadísticas relevantes
    - Contexto narrativo
    - Elementos de riesgo
    
    Devuelve SOLO el parámetro en formato:
    Parametro_estadistico: [extramadamente alta|muy alta|alta|media|baja|muy baja|extramadamente baja]
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "Eres un evaluador de probabilidades para acciones en un juego de rol"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=50
        )
        
        respuesta = response.choices[0].message.content.strip()
        parametro = respuesta.split(":")[-1].strip().lower()
        return parametro if parametro in ["extramadamente alta","muy alta", "alta", "media", "baja", "muy baja", "extramadamente baja"] else "media"
        
    except Exception as e:
        print(f"Error evaluando probabilidad: {str(e)}")
        return "media"

def generar_narrativa(accion_jugador, narrativa_base, historial_previo, resultado):
    """Genera la narrativa considerando el resultado"""
    client = OpenAI(api_key=config('OPENAI_API_KEY'))
    
    sistema_prompt = f"""
    {INITIAL_PROMPT}
    
    
    ### Narrativa Base:
    {narrativa_base}
    
    ### Historial Previo:
    {historial_previo[-3000:]}
    
    Instrucciones:
    1. Desarrolla consecuencias acordes al resultado
    2. Integrar la acción del jugador de forma orgánica
    3. Mantén coherencia con el parámetro de probabilidad
    4. Incluye impacto en la trama principal
    5. Limita a 1 párrafos máximo y que sea breve narrando el suceso
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": sistema_prompt},
                {"role": "user", "content": f"Jugador: {json.dumps(accion_jugador['nombre'])}\nAcción: {accion_jugador['accion']}\nResultado: {resultado}"}
            ],
            temperature=0.8,
            max_tokens=1500
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error en generación narrativa: {str(e)}")
        return None

def obtener_accion_jugador():
    """Recolecta acción y estadísticas con validación"""
    print("\n--- Nuevo Turno ---")
    jugador = input("Nombre del jugador: ").strip()
    accion = input("Acción a realizar: ").strip()
    
    return {
        "nombre": jugador,
        "timestamp": datetime.now().isoformat(),
        "accion": accion,
        "estadisticas": {
            "valor": "3",
            "inteligencia": "2",
            "fuerza": "5",
            "velocidad": "3",
            "carisma": "1"
        },
        "metadata": {
            "localizacion_actual": None,
            "objetos": [],
            "estado": "activo"
        }
    }

def main():
    inicializar_historial()
    historial = cargar_historial()
    narrativa = cargar_narrativa()

    # intro_speak(narrativa)
    
    if not narrativa:
        print("Error crítico: No se puede cargar narrativa base")
        return
    
    accion = obtener_accion_jugador()
    
    # Evaluar probabilidad
    parametro = evaluar_probabilidad(accion)
    print(f"\nProbabilidad calculada: {parametro.upper()}")
    
    # Obtener resultado real
    while True:
        resultado = input("¿Resultado final? (success/failure): ").lower().strip()
        if resultado in ["success", "failure"]:
            break
        print("Ingresa solo 'success' o 'failure'")
    
    # Generar narrativa
    nueva_narrativa = generar_narrativa(
        accion_jugador=accion,
        narrativa_base=narrativa,
        historial_previo=historial,
        resultado=resultado
    )
    
    if nueva_narrativa:
        guardar_historial(nueva_narrativa)
        print("\n--- Desarrollo de la Historia ---")
        texto_a_voz(nueva_narrativa)
    else:
        print("Error: No se pudo generar narrativa")

if __name__ == "__main__":
    main()