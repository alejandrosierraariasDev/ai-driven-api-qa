import ollama
import os

# --- CONFIGURACIÓN INPUT---
MODEL = 'llama3.2:1b'
DIRECTORY = 'spec'
FILE_NAME = 'openapi.yaml'
FILE_PATH = os.path.join(DIRECTORY, FILE_NAME)
REQUIREMENTS = 'requirements.txt'
SPEC = 'openapi.yaml'

# --- CONFIGURACIÓN OUTPUT---
OUTPUT_DIR = 'output'
OUTPUT_FILE = 'chat_output.py'
OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

# --- SWITCH PARA CONTROLAR SALIDA ---
OUTPUT_TO_FILE = True  # True = escribe en fichero, False = imprime en consola


def leer_y_preguntar(file_path, model_name):
    """Lee el contenido de un archivo, pregunta a Ollama y guarda la respuesta."""

    # 1. Leer el contenido del archivo
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            contenido_documento = f.read()
            print(f"Archivo '{file_path}' leído correctamente ({len(contenido_documento)} caracteres).")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{file_path}'.")
        return

    # 2. Definir la instrucción y el prompt
    instruccion = (f"Eres un generador de tests automatizados de API en Python usando estas librerias '{REQUIREMENTS}' "
                   f"A partir de esta especificación'{SPEC}': Genera código Python ,  "
                   "Cada endpoint debe tener su test correspondiente (GET, POST, PUT, DELETE) "
                   "Validar campos obligatorios y códigos de respuesta "
                   "Crear fixtures si es necesario con pytest"
                   "Usa clases de PyTest para agrupar tests por endpoint. "
                   "Los comentarios deben ser mínimos, solo indicativos. "
                   "No devuelvas texto adicional fuera del código"
                   "Puedes usar from fastapi import FastAPI, Request from pydantic import BaseModel")

    full_prompt = f"""
{instruccion}

--- DOCUMENTO PARA ANÁLISIS ---
{contenido_documento}
--- FIN DEL DOCUMENTO ---
"""
    messages = [{'role': 'user', 'content': full_prompt}]

    print(f"Enviando solicitud a Ollama con el modelo {model_name}...")

    # 3. Llamar a la API de Ollama y capturar la respuesta
    respuesta_completa = ""

    try:
        response = ollama.chat(model=model_name, messages=messages, stream=True)

        if not OUTPUT_TO_FILE:
            # Mostrar en consola
            print("\n" + "=" * 50)
            print("Respuesta del modelo (Terminal):")

        for chunk in response:
            content = chunk['message']['content']
            respuesta_completa += content
            if not OUTPUT_TO_FILE:
                print(content, end='', flush=True)

        if not OUTPUT_TO_FILE:
            print("\n" + "=" * 50)

    except Exception as e:
        print(f"\nError al interactuar con Ollama. ¿Está 'ollama serve' corriendo? Detalles: {e}")
        return

    # 4. CREAR DIRECTORIO Y GUARDAR RESPUESTA SI OUTPUT_TO_FILE
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
    leer_y_preguntar(FILE_PATH, MODEL)
