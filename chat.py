import ollama

# Especifica el modelo que has descargado (por ejemplo, 'mistral')
MODEL = 'llama3.2:1b'

# 1. Definir una lista de mensajes para mantener el historial
messages = [
    {'role': 'user', 'content': 'Hola, ¿cuál es la capital de Francia?'},
]

# 2. Llamar a la API de Ollama y obtener la respuesta de forma simple
try:
    print(f"Preguntando a {MODEL}...")
    response = ollama.chat(
        model=MODEL,
        messages=messages
    )

    # El contenido de la respuesta está dentro de la estructura 'message'
    print("\nRespuesta del modelo:")
    print(response['message']['content'])

except Exception as e:
    print(f"Error: No se pudo conectar a Ollama. Asegúrate de que 'ollama serve' esté corriendo. Detalles: {e}")