import ollama
import os

# --- CONFIGURACIÓN INPUT---
MODEL = 'llama3.2:1b'
SPEC_FILE_PATH = os.path.join('spec', 'apidocs-aestatistics.yaml')
PROMPT_PATH = os.path.join('prompt', 'javaprompt.txt')
REQUIREMENTS_PATH = 'build.gradle'

# --- CONFIGURACIÓN OUTPUT---
OUTPUT_DIR = 'output'
OUTPUT_FILE = 'java_output.java'
OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

# --- SWITCH PARA CONTROLAR SALIDA ---
OUTPUT_TO_FILE = True


def leer_archivo(path):
    """Lee archivo y devuelve contenido o None si falta."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            contenido = f.read()
            print(f"✔ Archivo leído: {path} ({len(contenido)} chars)")
            return contenido
    except FileNotFoundError:
        print(f"❌ No se encuentra: {path}")
        return None


def leer_y_preguntar():
    """Fusiona prompt + spec + requirements y pregunta a Ollama."""

    contenido_especificacion = leer_archivo(SPEC_FILE_PATH)
    contenido_prompt = leer_archivo(PROMPT_PATH)
    contenido_requirements = leer_archivo(REQUIREMENTS_PATH)

    if not contenido_especificacion or not contenido_prompt:
        print("❌ Proceso detenido: Falta prompt o spec.")
        return

    # Construcción dinámica del prompt reemplazando placeholders
    full_prompt = contenido_prompt.replace("{{ SPEC }}", contenido_especificacion)
    full_prompt = full_prompt.replace("{{ REQS }}", contenido_requirements or "NO DEPENDENCIES FOUND")

    print("\n🚀 Enviando instrucción a Ollama...")

    messages = [{'role': 'user', 'content': full_prompt}]
    respuesta_completa = ""

    try:
        response = ollama.chat(
            model=MODEL,
            messages=messages,
            stream=True,
            options={"temperature": 0.0, "top_p": 0.1}
        )

        for chunk in response:
            respuesta = chunk['message']['content']
            respuesta_completa += respuesta
            print(respuesta, end='', flush=True)

    except Exception as e:
        print(f"\n❌ Error con Ollama: {e}")
        return

    # Guardar output
    if OUTPUT_TO_FILE:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
            f.write(respuesta_completa)
        print(f"\n\n💾 Guardado en: {OUTPUT_PATH}")


if __name__ == "__main__":
    leer_y_preguntar()
