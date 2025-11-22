# 🤖 IA driven API QA

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Ollama-LLM-orange?logo=openai&logoColor=white)](https://ollama.ai/)
[![GitLab CI](https://img.shields.io/badge/GitLab-CI/CD-FC6D26?logo=gitlab&logoColor=white)](https://gitlab.com/)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0-6BA539?logo=openapis&logoColor=white)](https://www.openapis.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Automatiza el análisis de especificaciones API y genera código mediante IA (Ollama)**

Este repositorio forma parte de un flujo automatizado entre tres repositorios que sincroniza cambios en especificaciones de API, ejecuta análisis con IA y genera artefactos automáticamente.

---

## 📋 Tabla de Contenidos

- [Arquitectura](#-arquitectura)
- [¿Cuándo se ejecuta?](#-cuándo-se-ejecuta-este-sistema)
- [Estructura del Repositorio](#-contenido-del-repositorio)
- [Validación de OpenAPI](#-validación-de-openapi-en-pipeline-1)
- [Requisitos](#-requisitos-técnicos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Output](#-output-esperado)
- [Troubleshooting](#-troubleshooting)
- [Roles](#-roles-del-flujo)
- [Roadmap](#-roadmap-futuro)

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  Repo #1: api_spec                                                      │
│  └─ spec/openapi.yaml (modificado en branch: dev)                       │
│                                                                         │
└────────────────────────┬────────────────────────────────────────────────┘
                         │ Merge a dev
                         ⬇
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  Pipeline 1 (Repo #1) - VALIDACIÓN EXHAUSTIVA                           │
│  ├─ ✅ validate_openapi (swagger-cli + Spectral)                        │
│  │  ├─ Validación sintáctica                                            │
│  │  └─ Validación de calidad (reglas custom)                            │
│  │                                                                      │
│  └─ 🚀 trigger_ai_pipeline (si validación OK)                           │
│                                                                         │
└────────────────────────┬────────────────────────────────────────────────┘
                         │ Trigger (solo si pasa validación)
                         ⬇
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  Repo #2: IA_Code (Este repositorio)                                    │
│  ├─ main.py (ejecuta Ollama)                                            │
│  ├─ spec/openapi.yaml (input validado)                                  │
│  ├─ prompt/prompt.txt (instrucciones IA)                                │
│  └─ output/chat_output.py (artefacto generado)                          │
│                                                                         │
└────────────────────────┬────────────────────────────────────────────────┘
                         │ Pipeline 2
                         ⬇
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  Repo #3: QADev_code                                                    │
│  └─ Recibe MR automática con output generado                            │
│     Branch: feature-ai-update-yyyymmddHHMM → dev                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 ¿Cuándo se ejecuta este sistema?

| Evento | Resultado |
|--------|-----------|
| Se modifica y mergea `spec/openapi.yaml` en **api_spec** → branch **dev** | Se lanza **Pipeline 1** |
| Pipeline 1: **Validación** (swagger-cli + Spectral) | ✅ Pasa → Continúa / ❌ Falla → Se detiene |
| Pipeline 1 notifica a **IA_Code** (solo si validación OK) | Se ejecuta **IA** y se genera output |
| Pipeline 2 (en este repo) termina el análisis | Se crea **Merge Request automática** en QADev_code → destino: **dev** |

### 🔄 Flujo Detallado de Validación

```
Merge openapi.yaml a dev
        ⬇
   Pipeline 1
        ⬇
   validate_openapi
        ⬇
   ┌─────────────────────────────────┐
   │ 1. swagger-cli validate         │
   │    (Sintaxis YAML + estructura) │
   └────────────┬────────────────────┘
                ⬇
            ✅ OK?
           /      \
         ✅        ❌
        /            \
       ⬇              ⬇
   ┌──────────┐   STOP
   │ Spectral │   (Blocking)
   │ lint     │
   └────┬─────┘
        ⬇
   ✅ Errores?
   /      \
  ❌      ✅
 /         \
⬇           ⬇
STOP      Warnings?
(Blocking) /      \
         ❌       ✅
        /           \
       ⬇             ⬇
      STOP        CONTINUE
    (Blocking)    (Notify)
                   ⬇
            trigger_ai_pipeline
                   ⬇
              Repo #2 (IA_Code)
```

---

## 🧩 Contenido del Repositorio

```
IA_Code/
├── 📄 README.md                    # Este archivo
├── 📄 requirements.txt             # Dependencias Python
├── 📄 main.py                      # Script principal de ejecución
├── 📄 .gitlab-ci.yml               # Pipeline CI/CD
│
├── 📁 spec/
│   └── openapi.yaml                # Input: Especificación API (desde Repo #1)
│
├── 📁 prompt/
│   └── prompt.txt                  # Instrucciones para la IA (plantilla)
│
├── 📁 output/
│   └── chat_output.py              # Output: Artefacto generado por IA
│
└── 📁 gitlab/
    ├── 1.gitlab-ci.yaml            # Pipeline Repo #1 (validación + trigger)
    └── 2.gitlab-ci.yaml            # Pipeline Repo #2 (este repo)
```

### 📝 Descripción de Archivos Clave

| Archivo | Descripción |
|---------|-------------|
| **main.py** | Script principal que orquesta todo el flujo: lee spec, ejecuta Ollama, guarda output |
| **spec/openapi.yaml** | Especificación OpenAPI que recibe desde Repo #1 |
| **prompt/prompt.txt** | Plantilla de instrucciones para la IA (define qué generar) |
| **output/chat_output.py** | Artefacto generado automáticamente (se envía a Repo #3) |
| **.gitlab-ci.yml** | Pipeline que ejecuta main.py y crea MR en Repo #3 | |

---

## ✅ Validación de OpenAPI en Pipeline 1

Antes de ejecutar la IA, el Pipeline 1 (en Repo #1) realiza validaciones exhaustivas de la especificación OpenAPI para asegurar que cumple con estándares técnicos y de calidad.

### 📌 Etapas de Validación

El job `validate_openapi` ejecuta dos niveles de validación:

#### 1️⃣ Validación Sintáctica con swagger-cli

**Propósito**: Verificar que el archivo OpenAPI está bien formado y cumple con las especificaciones oficiales.

**Qué valida**:
- ✔ Que el YAML está correctamente formado
- ✔ Que claves obligatorias (`openapi`, `paths`, `components`, etc.) existen
- ✔ Que las referencias (`$ref`) están correctamente definidas
- ✔ Que no hay elementos huérfanos o mal estructurados

**Comportamiento**: ⛔ Si falla, la pipeline se detiene inmediatamente (blocking)

#### 2️⃣ Validación de Calidad con Spectral

**Propósito**: Analizar el contenido semántico del archivo OpenAPI según reglas de estándar interno.

**Casos de uso**:

| Caso | Acción |
|------|--------|
| Existe `.spectral.yaml` | Se usa el archivo existente |
| No existe | Se genera automáticamente con reglas preconfiguradas |

### 📄 Reglas Aplicadas por Spectral

Estas reglas definen estándares de escritura y consistencia de la API:

| Regla | Tipo | Qué valida | Severidad |
|-------|------|-----------|----------|
| **operation-description** | Custom | Cada endpoint debe tener una descripción clara | ❌ Error |
| **schema-must-have-type** | Custom | Todas las propiedades en schemas deben declarar un tipo (`type`) | ❌ Error |
| **required-fields** | Custom | Si existe `properties` en un schema, debe declararse un array `required` | ⚠️ Warning |
| **example-required** | Custom | Cada propiedad debe incluir un valor ejemplo (`example`) | ⚠️ Warning |

### 🚦 Criterios de Fallo del Pipeline

| Condición | Resultado |
|-----------|----------|
| Validación sintáctica falla | ❌ Pipeline detenida (blocking) |
| Spectral detecta errores (`severity = error`) | ❌ Pipeline detenida (blocking) |
| Spectral detecta solo warnings | ⚠️ Pipeline continúa, pero se notifica |

Esto permite mejorar progresivamente la documentación sin bloquear el desarrollo por detalles menores.

### 🧪 Ejemplo de Salida Esperada

```
📌 Validando sintaxis OpenAPI...
✓ No errors found!

🔍 Validando calidad OpenAPI con Spectral...
❗ ERROR: paths./users.post description is missing
⚠ WARNING: components.schemas.User.required should be defined

❌ Violations found. Fix before merge.
```

### 🎯 Objetivo de esta Validación

Asegurar que:
- ✔ La API mantiene un estándar uniforme
- ✔ La documentación es clara, robusta y útil para consumidores
- ✔ Se detectan inconsistencias antes de que lleguen al repositorio principal
- ✔ Las reglas pueden evolucionar con el estándar interno del equipo

---

## 🛠️ Requisitos Técnicos

| Dependencia | Requerido | Notas |
|-------------|----------|-------|
| **Python** | 3.9+ | ✔ Obligatorio |
| **Ollama** | Instalado en runner | ✔ Obligatorio |
| **Modelo LLM** | llama3.2:1b | ✔ Debe estar descargado |
| **Git** | Instalado en runner | ✔ Obligatorio |
| **Node.js** | 18+ (en runner Pipeline 1) | ✔ Para Spectral y swagger-cli |
| **swagger-cli** | NPM package | ✔ Validación sintáctica |
| **Spectral** | NPM package | ✔ Validación de calidad |
| **Runner Linux** | SSH/Git accesible | ✔ Obligatorio |
| **GITLAB_TOKEN** | Variable CI/CD | ✔ Obligatorio |

---

## 📥 Instalación

### 1. Clonar el repositorio

```bash
git clone https://gitlab.com/sngular-solutions/qe/IA_Code.git
cd IA_Code
```

### 2. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Verificar Ollama

```bash
# Verificar que Ollama está corriendo
ollama list

# Si no está corriendo, iniciar:
ollama serve

# Descargar modelo (si no está disponible):
ollama pull llama3.2:1b
```

---

## ⚙️ Configuración

### Variables de Entorno (GitLab CI/CD)

Configura estas variables en **Settings → CI/CD → Variables** de tu proyecto GitLab:

| Variable | Obligatoria | Descripción |
|----------|-------------|-------------|
| **GITLAB_TOKEN** | ✅ | Token con permisos: `api`, `write_repository`, `write_merge_requests` |
| **OLLAMA_MODEL** | ❌ | Modelo a usar (default: `llama3.2:1b`) |

### Crear Token en GitLab

1. Ve a **Settings → Access Tokens**
2. Crea un token con permisos:
   - ✅ `api`
   - ✅ `write_repository`
   - ✅ `write_merge_requests`
3. Copia el token y agrégalo como variable `GITLAB_TOKEN` en CI/CD

### Configurar Runner

El runner debe tener:
- Python 3.9+
- Ollama instalado
- Node.js 18+ (para Pipeline 1)
- Acceso a internet para clonar repositorios

### Instalar Herramientas de Validación (Pipeline 1)

En el runner de Pipeline 1, instalar:

```bash
# Instalar swagger-cli y Spectral
npm install -g @stoplight/spectral-cli swagger-cli

# Verificar instalación
spectral --version
swagger-cli --version
```

---

## 🚀 Uso

### Ejecución Manual (Desarrollo)

```bash
# Asegúrate de que Ollama está corriendo
ollama serve &

# Ejecutar el script
python3 main.py
```

### Ejecución Automática (CI/CD)

El pipeline se ejecuta automáticamente cuando:
1. Se modifica `spec/openapi.yaml` en **api_spec** (Repo #1)
2. Se mergea a la rama **dev**
3. Pipeline 1 dispara Pipeline 2 (este repo)
4. Se ejecuta `main.py` automáticamente
5. Se crea MR en **QADev_code** (Repo #3)

---

## 📄 Output Esperado

### Archivo Generado

```
output/chat_output.py
```

Este archivo contiene el código/artefacto generado por la IA basándose en:
- **Input**: `spec/openapi.yaml` (especificación API)
- **Instrucciones**: `prompt/prompt.txt` (qué generar)
- **Modelo**: `llama3.2:1b` (Ollama)

### Ejemplo de Salida en Consola

```
✔ Cargado spec/openapi.yaml
✔ Cargado prompt/prompt.txt
🚀 Ejecutando IA...
[Streaming de respuesta del modelo...]
💾 Guardado en: output/chat_output.py
🏁 Generación completada. Pipeline continuará con push y MR.
```

---

## 🔁 Merge Request Generada Automáticamente

La MR creada en **QADev_code** seguirá este patrón:

| Parámetro | Valor |
|-----------|-------|
| **Branch origen** | `feature-ai-update-yyyymmddHHMM` |
| **Branch destino** | `dev` |
| **Título** | `🤖 AI Generated Update from API Spec` |
| **Descripción** | Automática (generada por pipeline) |

**Ejemplo:**
```
feature-ai-update-202503122048 → dev
```

---

## 🚨 Troubleshooting

### ❌ Pipeline falla con error `ollama: command not found`

**Causa**: Runner no tiene Ollama instalado

**Solución**:
```bash
# En el runner
curl https://ollama.ai/install.sh | sh
ollama pull llama3.2:1b
```

### ❌ MR no se crea

**Causa**: Token sin permisos suficientes

**Solución**:
1. Verifica que `GITLAB_TOKEN` tiene permisos: `api`, `write_repository`, `write_merge_requests`
2. Regenera el token si es necesario

### ❌ Output vacío

**Causa**: OpenAPI mal formado o prompt no encontrado

**Solución**:
```bash
# Validar que los archivos existen
ls -la spec/openapi.yaml
ls -la prompt/prompt.txt

# Validar sintaxis YAML
python3 -c "import yaml; yaml.safe_load(open('spec/openapi.yaml'))"
```

### ❌ Ollama no responde

**Causa**: Servicio Ollama no está corriendo

**Solución**:
```bash
# Iniciar Ollama
ollama serve

# En otra terminal, verificar
ollama list
```

### ❌ Error de permisos en Git

**Causa**: Token de GitLab sin acceso SSH

**Solución**:
```bash
# Usar HTTPS en lugar de SSH
git config --global url."https://oauth2:${GITLAB_TOKEN}@gitlab.com/".insteadOf "https://gitlab.com/"
```

### ❌ Pipeline 1 falla: `swagger-cli: command not found`

**Causa**: Node.js o swagger-cli no instalado en runner

**Solución**:
```bash
# En el runner de Pipeline 1
npm install -g @stoplight/spectral-cli swagger-cli
```

### ❌ Spectral reporta errores en OpenAPI válido

**Causa**: Archivo `.spectral.yaml` con reglas demasiado estrictas

**Solución**:
1. Revisa el archivo `.spectral.yaml` en Repo #1
2. Ajusta las reglas según los estándares del equipo
3. Cambia severidades de `error` a `warn` si es necesario

---

## 👥 Roles del Flujo

| Rol                | Responsabilidad |
|--------------------|-----------------|
| **Equipo Backend** | Mantiene `spec/openapi.yaml` en Repo #1 |
| **Equipo QA**      | Mantiene lógica del `prompt.txt` y artefactos generados |
| **DevOps**         | Mantiene CI/CD, tokens, runner y permisos |
| **Equipo QA**      | Revisa y aprueba la MR generada automáticamente |

---

## 📌 Roadmap Futuro

- [ ] Validación automática del output antes de MR
- [ ] Auto-resolve si el archivo generado no cambia contenido
- [ ] Notificación en canal de google del resultado
- [ ] LLM con memoria incremental
- [ ] Validacion schema de la especificacion en el repositorio 1


---

## 🧠 Resumen

✔ **Automatiza** el ciclo API → IA → Código  
✔ **Elimina** trabajo manual repetitivo  
✔ **Mantiene** consistencia y versionado  
✔ **Escalable** para nuevos lenguajes o reglas  

---

