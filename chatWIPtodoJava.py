import ollama
import os

# --- CONFIGURACIÓN INPUT---
MODEL = 'llama3.2:1b'
DIRECTORY = 'spec'
FILE_NAME = 'openapi.yaml'
FILE_PATH = os.path.join(DIRECTORY, FILE_NAME)

PROMPT_DIRECTORY = 'prompt'
PROMPT_CONTENT = 'prompt.txt'
PROMPT_PATH = os.path.join(PROMPT_DIRECTORY, PROMPT_CONTENT)

# --- CONFIGURACIÓN OUTPUT---
OUTPUT_DIR = 'output'
OUTPUT_FILE = 'chat_output.py'
OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

# --- SWITCH PARA CONTROLAR SALIDA ---
OUTPUT_TO_FILE = True


def leer_y_preguntar(spec_file_path, prompt_file_path, model_name):
    """Lee la especificación y el prompt de scaffolding, pregunta a Ollama y guarda la respuesta."""

    # 1. Leer el contenido del archivo de ESPECIFICACIÓN
    try:
        with open(spec_file_path, 'r', encoding='utf-8') as f:
            contenido_especificacion = f.read()
            print(f"Archivo de especificación '{spec_file_path}' leído ({len(contenido_especificacion)} caracteres).")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de especificación '{spec_file_path}'.")
        return

    # 2. Leer el contenido del archivo de PROMPT
    try:
        with open(prompt_file_path, 'r', encoding='utf-8') as f:
            instruccion = f.read()
            print(f"Archivo de prompt '{prompt_file_path}' leído.")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de prompt '{prompt_file_path}'.")
        return

    # 3. Construir el prompt completo que se enviará a Ollama
    full_prompt = f"""
    --- INSTRUCCIONES DE SCAFFOLDING Y ESTILO ---
    {instruccion}

    --- ESPECIFICACIÓN DE API PARA ANÁLISIS ---
    {contenido_especificacion}
    --- FIN DE ESPECIFICACIÓN ---
    """

    # 4. Llamar a la API de Ollama y capturar la respuesta
    messages = [{'role': 'user', 'content': full_prompt}]
    respuesta_completa = ""

    print(f"\nEnviando solicitud a Ollama con el modelo {model_name}...")

    try:
        response = ollama.chat(model=model_name, messages=messages, stream=True)

        print("\n" + "=" * 50)
        print("Respuesta del modelo (Terminal):")

        for chunk in response:
            content = chunk['message']['content']
            respuesta_completa += content
            print(content, end='', flush=True)

        print("\n" + "=" * 50)

    except Exception as e:
        print(f"\nError al interactuar con Ollama. ¿Está 'ollama serve' corriendo? Detalles: {e}")
        return

    # 5. CREAR DIRECTORIO Y GUARDAR RESPUESTA
    if OUTPUT_TO_FILE:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        try:
            with open(OUTPUT_PATH, 'w', encoding='utf-8') as outfile:
                outfile.write(respuesta_completa)

            print(f"\n✅ Respuesta guardada exitosamente en: {OUTPUT_PATH}")

        except Exception as e:
            print(f"\nError al guardar el archivo de salida: {e}")


# Ejecutar la función principal
if __name__ == "__main__":
    leer_y_preguntar(FILE_PATH, PROMPT_PATH, MODEL)