import ollama
import os
import re

# --- CONFIGURACIÓN INPUT---
MODEL = 'llama3.2:1b'
SPEC_DIRECTORY = 'spec'
SPEC_FILE_NAME = 'openapi.yaml'
SPEC_PATH = os.path.join(SPEC_DIRECTORY, SPEC_FILE_NAME)

PROMPT_DIRECTORY = 'prompt'
PROMPT_CONTENT = 'java_Prompt.txt'
PROMPT_PATH = os.path.join(PROMPT_DIRECTORY, PROMPT_CONTENT)

# --- ARCHIVOS DE CONTEXTO ---
GRADLE_PATH = 'build.gradle'

# --- CONFIGURACIÓN OUTPUT---
OUTPUT_DIR = 'output'
OUTPUT_FILE = 'ai_generated_tests.java'
OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

# --- SWITCHES PARA CONTROLAR SALIDA ---
OUTPUT_TO_FILE = True
PRINT_TO_CONSOLE = False  # <--- CONTROLADOR PARA EVITAR IMPRIMIR EN CONSOLA


def extract_gradle_dependencies(gradle_path):
    """Extrae las líneas de dependencia relevantes (implementation, compile, testImplementation)."""
    try:
        with open(gradle_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo Gradle '{gradle_path}'.")
        return ""

    # Patrón para capturar líneas de dependencia
    dependency_pattern = re.compile(
        r'^\s*(?:implementation|compile|testImplementation|testRuntimeOnly|annotationProcessor)\s+.*$',
        re.MULTILINE
    )

    dependencies = dependency_pattern.findall(content)

    # Limpiar líneas de comentarios y formato
    cleaned_deps = [dep.strip() for dep in dependencies if
                    not dep.strip().startswith('//') and not 'exclude group:' in dep]

    return "\n".join(cleaned_deps)


def extract_java_code(raw_output):
    """Extrae bloques de código Java de la salida de la IA."""
    # Busca el bloque de código Markdown ```java ... ```
    match = re.search(r'```java\n(.*?)```', raw_output, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Si no hay Markdown, intenta limpiar líneas introductorias/redundantes
    lines = raw_output.split('\n')
    cleaned_lines = []

    # Intenta encontrar el inicio del código por la primera línea de import o class
    in_code_block = False
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith('import') or stripped_line.startswith('package') or stripped_line.startswith(
                'public class'):
            in_code_block = True

        if in_code_block:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()


def leer_y_preguntar(spec_file_path, prompt_file_path, gradle_path, model_name):
    """Lee la especificación, el prompt y las dependencias, pregunta a Ollama y guarda la respuesta."""

    # 1. Leer y preparar el contenido de CONTEXTO
    try:
        with open(spec_file_path, 'r', encoding='utf-8') as f:
            contenido_especificacion = f.read()
            print(f"Archivo de especificación '{spec_file_path}' leído.")

        contenido_dependencias = extract_gradle_dependencies(gradle_path)
        if not contenido_dependencias:
            print("Advertencia: No se pudieron extraer dependencias de Gradle.")

        with open(prompt_file_path, 'r', encoding='utf-8') as f:
            instruccion = f.read()
            print(f"Archivo de prompt '{prompt_file_path}' leído.")

    except FileNotFoundError as e:
        print(f"Error: No se encontró un archivo de contexto: {e}.")
        return

    # 2. Construir el prompt completo que se enviará a Ollama
    full_prompt = instruccion.replace('{{ REQS }}', contenido_dependencias)
    full_prompt = full_prompt.replace('{{ SPEC }}', contenido_especificacion)

    if PRINT_TO_CONSOLE:
        print("\n--- Vista previa del Prompt (Primeras 500 chars) ---")
        print(full_prompt[:500] + "...")
        print("--------------------------------------------------")

    # 3. Llamar a la API de Ollama y capturar la respuesta
    messages = [{'role': 'user', 'content': full_prompt}]
    respuesta_completa = ""

    print(f"\nEnviando solicitud a Ollama con el modelo {model_name}...")

    try:
        response = ollama.chat(model=model_name, messages=messages, stream=True)

        # Configuración para NO imprimir en consola
        if PRINT_TO_CONSOLE:
            print("\n" + "=" * 50)
            print("Respuesta del modelo (Terminal):")

        for chunk in response:
            content = chunk['message']['content']
            respuesta_completa += content

            # Línea crucial: SOLO imprime si PRINT_TO_CONSOLE es True
            if PRINT_TO_CONSOLE:
                print(content, end='', flush=True)

        if PRINT_TO_CONSOLE:
            print("\n" + "=" * 50)
        else:
            print("\n✅ IA finalizada. Generando código...")

    except Exception as e:
        print(f"\nError al interactuar con Ollama. ¿Está 'ollama serve' corriendo? Detalles: {e}")
        return

    # 4. CREAR DIRECTORIO Y GUARDAR RESPUESTA
    if OUTPUT_TO_FILE:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        try:
            cleaned_java_code = extract_java_code(respuesta_completa)

            with open(OUTPUT_PATH, 'w', encoding='utf-8') as outfile:
                outfile.write(cleaned_java_code)

            print(f"\n✅ Respuesta guardada exitosamente en: {OUTPUT_PATH}")

        except Exception as e:
            print(f"\nError al guardar el archivo de salida: {e}")


# Ejecutar la función principal
if __name__ == "__main__":
    leer_y_preguntar(SPEC_PATH, PROMPT_PATH, GRADLE_PATH, MODEL)