import ollama
import os

# --- INPUT CONFIG ---
MODEL = 'llama3.2:1b'
SPEC_PATH = 'spec/openapi.yaml'
PROMPT_PATH = 'prompt/prompt.txt'

# --- OUTPUT CONFIG ---
OUTPUT_DIR = 'output'
OUTPUT_FILE = 'chat_output.py'
OUTPUT_PATH = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

# --- ENV FROM PIPELINE ---
BRANCH_NAME = os.getenv('CI_COMMIT_REF_NAME', 'auto-generated')
TOKEN = os.getenv('GITLAB_TOKEN')


def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            print(f"✔ Cargado {path}")
            return f.read()
    except FileNotFoundError:
        print(f"❌ Archivo requerido no existe: {path}")
        return None


def build_prompt(spec, prompt):
    return f"""
### INSTRUCCIONES PARA GENERACIÓN DE CÓDIGO ###
{prompt}

### ESPECIFICACIÓN OPENAPI ###
{spec}
"""


def run_model(full_prompt):
    print("🚀 Ejecutando IA...")
    messages = [{'role': 'user', 'content': full_prompt}]
    result = ""

    response = ollama.chat(model=MODEL, messages=messages, stream=True)
    for chunk in response:
        result += chunk['message']['content']
        print(chunk['message']['content'], end='', flush=True)

    return result


def save_output(text):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"\n💾 Guardado en: {OUTPUT_PATH}")


def main():
    spec = read_file(SPEC_PATH)
    prompt = read_file(PROMPT_PATH)

    if not spec or not prompt:
        print("\n❌ Falta información necesaria. Abortando.")
        return

    full_prompt = build_prompt(spec, prompt)
    generated_code = run_model(full_prompt)

    save_output(generated_code)
    print("\n🏁 Generación completada. Pipeline continuará con push y MR.")


if __name__ == "__main__":
    main()
