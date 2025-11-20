import os
import subprocess
import requests
import json
from uuid import uuid4

# Importación de la librería de Ollama
try:
    # Intenta importar ollama. Si falla, el script no puede continuar.
    import ollama
except ImportError:
    print("Error: La librería 'ollama' no está instalada. Ejecute 'pip install ollama'.")
    # Es crucial fallar aquí, ya que la lógica central depende de Ollama.
    exit(1)


# --- CONFIGURACIÓN DE REPOSITORIOS (OBTENIDAS DE VARIABLES CI/CD) ---
# ID del Repositorio 1 (Spec) y SHA del commit que disparó el pipeline.
# Estas variables deben ser pasadas por el pipeline trigger del Repo 1.
SPEC_PROJECT_ID = os.environ.get('SPEC_PROJECT_ID')
SPEC_COMMIT_SHA = os.environ.get('SPEC_COMMIT_SHA')
# ID del Repositorio 3 (Target Code) - Debe configurarse como variable CI/CD.
TARGET_PROJECT_ID = os.environ.get('TARGET_PROJECT_ID', 'REEMPLAZAR_ID_TARGET_REPO')
# Token de acceso de GitLab - Debe configurarse como variable secreta CI/CD (CI_GITLAB_TOKEN).
GITLAB_TOKEN = os.environ.get('CI_GITLAB_TOKEN')
# Host de GitLab (ej: gitlab.com)
GITLAB_HOST = os.environ.get('CI_SERVER_HOST', 'gitlab.com')
# Namespace completo del proyecto (ej: 'tu-grupo/tu-subgrupo')
CI_PROJECT_NAMESPACE = os.environ.get('CI_PROJECT_NAMESPACE', 'default_namespace')


# --- CONFIGURACIÓN DE OLLAMA Y ARCHIVOS ---
OLLAMA_MODEL = 'llama3.2:1b'
PROMPT_PATH = 'prompt/prompt_content.txt' # Ruta del prompt en este Repo (Repo 2)
SPEC_FILE = 'openapi.yaml'
GENERATED_FILE = 'src/generated_tests.py' # Ruta de salida del código en el Repo 3
TARGET_BRANCH = 'develop'
SOURCE_BRANCH = f'feature/gen-tests-{uuid4().hex[:8]}'

# --- LÓGICA DE OLLAMA ---
def run_ollama_logic(spec_content: str) -> str:
    """
    Lee el prompt de scaffolding, combina con la especificación y llama a Ollama
    para generar el código.
    """
    print("Iniciando generación de código con Ollama...")

    # 1. Leer el contenido del archivo de PROMPT (Scaffolding)
    try:
        # Abre el prompt de scaffolding que define la estructura de los tests.
        with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
            instruccion = f.read()
            print(f"Archivo de prompt '{PROMPT_PATH}' leído.")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de prompt '{PROMPT_PATH}' en el Repo 2.")
        raise FileNotFoundError(f"Missing prompt file: {PROMPT_PATH}")

    # 2. Construir el prompt completo que incluye las instrucciones y la especificación de la API.
    full_prompt = f"""
    --- INSTRUCCIONES DE SCAFFOLDING Y ESTILO ---
    {instruccion}

    --- ESPECIFICACIÓN DE API PARA ANÁLISIS ---
    {spec_content}
    --- FIN DE ESPECIFICACIÓN ---
    """

    # 3. Llamar a la API de Ollama
    messages = [{'role': 'user', 'content': full_prompt}]
    respuesta_completa = ""

    try:
        # Ollama.chat para obtener la respuesta (no usamos streaming para simplificar el CI)
        response = ollama.chat(model=OLLAMA_MODEL, messages=messages)

        # Capturar la respuesta completa
        respuesta_completa = response['message']['content']
        print(f"✅ Generación de código exitosa con modelo {OLLAMA_MODEL}.")

        # 4. Extracción del bloque de código (CRÍTICO)
        # Asume que el prompt instruye a devolver SOLO el bloque de código Python.
        # Si incluye bloques markdown, necesitamos extraer solo el código.
        if '```python' in respuesta_completa:
            # Encuentra el inicio del bloque de código
            code_start = respuesta_completa.find('```python') + len('```python\n')
            # Busca el fin del bloque (usando '