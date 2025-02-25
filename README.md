# Instrucciones para Configurar y Ejecutar el Proyecto Python

## Requisitos
- Python 3.8+ instalado
- pip instalado

## Pasos

1. **Crear el entorno virtual**

   - En Windows:
     ```bash
     python -m venv venv
     ```
   - En macOS/Linux:
     ```bash
     python3 -m venv venv
     ```

2. **Activar el entorno virtual**

   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Crear el archivo `requirements.txt` (si no existe)**

   ```bash
   pip freeze > requirements.txt
