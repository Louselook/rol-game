from openai import OpenAI
from decouple import config

def generar_informe_repar(api_key, parametros):
    """
    Genera el esquema narrativo para un juego de rol usando GPT-4.
    """
    client = OpenAI(api_key=api_key)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un escritor experto en crear historias para juegos de rol. Tu tarea es generar un esquema "
                        "narrativo completo y estructurado basado en la temática y características indicadas. "
                        "El esquema debe incluir los siguientes elementos:\n"
                        "1. Introducción narrativa: Contextualiza el mundo, describe el ambiente y establece el estado inicial del conflicto.\n"
                        "2. Objetivo principal: Define la misión o meta central que impulsa la aventura.\n"
                        "3. Localidades y características: Describe lugares clave, sus peligros y oportunidades.\n"
                        "4. Subtramas y giros narrativos: Introduce eventos secundarios que se entrelazan con la trama principal.\n"
                        "5. Personajes Secundarios e interacciones predefinidas: Construye dinámicamente algunos personajes, "
                        "propón desafíos y opciones en los que los jugadores puedan tomar diferentes decisiones.\n\n"
                        "La historia debe ser flexible para permitir que los jugadores influyan en el desarrollo sin perder la estructura base. "
                        "Al final de la respuesta debes posicionar a los personajes en un mismo lugar y darles opciones de que quiere hacer cada uno para iniciar el juego"
                    )
                },
                {
                    "role": "user",
                    "content": (
                        "Inicio de partida:\n"
                        "Temática: {tematica}\n"
                        "Características adicionales: {caracteristicas}\n\n"
                        # "Por favor, genera un esquema narrativo completo y estructurado que cumpla con los elementos indicados."
                    ).format(
                        tematica=parametros.get("tematica", "General"),
                        caracteristicas=parametros.get("caracteristicas", "Sin detalles adicionales")
                    )
                }
            ],
            temperature=0.2,
            max_tokens=3000,
            top_p=0.95
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error en la generación del informe: {str(e)}")
        exit(1)

def guardar_en_archivo(nombre_archivo, contenido):
    """Guarda el contenido en un archivo .txt"""
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)
        print(f"Historia guardada en {nombre_archivo}")
    except Exception as e:
        print(f"Error al guardar el archivo: {str(e)}")

if __name__ == "__main__":
    # Configuración
    API_KEY = config('OPENAI_API_KEY')
    
    # Ejemplo de parámetros para la sesión de juego
    parametros_sala = { 
        "tematica": "Investigacion",
        "caracteristicas": "Hay una serie de asesinatos en la ciudad, no se sabe si es un asesino serial o un culto o fuerzas mas alla de lo humano"
    }

    historia_principal = generar_informe_repar(API_KEY, parametros_sala)
    
    # Guardar la historia en un archivo
    guardar_en_archivo("narrativa/narrativa.txt", historia_principal)
