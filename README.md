# 🤖 AI-driven API Test Generator

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Ollama-LLM-orange?logo=openai&logoColor=white)](https://ollama.ai/)
[![Java](https://img.shields.io/badge/Java-17+-007396?logo=java&logoColor=white)](https://www.java.com/)
[![Gradle](https://img.shields.io/badge/Gradle-7.6+-02303A?logo=gradle&logoColor=white)](https://gradle.org/)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.0-6BA539?logo=openapis&logoColor=white)](https://www.openapis.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Automatic Java API test generation from OpenAPI specifications, using a local LLM (Ollama).**

---

## 📋 Table of contents

- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project structure](#-project-structure)
- [Configuration](#️-configuration)
- [Output](#-output)
- [CI/CD architecture](#️-cicd-architecture)
- [OpenAPI validation in Pipeline 1](#-openapi-validation-in-pipeline-1)
- [Troubleshooting](#-troubleshooting)

---

## 🔧 Requirements

### System
- Python 3.9+
- Java 17+
- Gradle 7.6+
- Git

### Ollama
- [Ollama](https://ollama.ai/) installed and configured
- A compatible language model (`llama3.2:1b` or larger recommended)
- At least 8 GB of RAM to run the basic model
- Internet access for the first model download

#### Recommended hardware
- CPU: 4+ cores
- RAM: 16 GB or more (depending on model size)
- Storage: 10 GB free (model and dependencies)

#### Supported models
- `llama3.2:1b` (recommended for most use cases)
- `llama3.2:7b` (more accurate, needs more resources)
- `llama3.2:13b` (most accurate, needs significant resources)

## 📥 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/alejandrosierraariasDev/ai-driven-api-qa.git
   cd ai-driven-api-qa
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Ollama server**
   ```bash
   # In one terminal, start the Ollama server
   ollama serve
   ```

4. **Download the language model**
   ```bash
   # In another terminal, download the model (may take a few minutes)
   ollama pull llama3.2:1b
   ```

5. **Check the installation**
   ```bash
   # List the available models
   ollama list
   ```

## 🚀 Usage

1. **Prepare the OpenAPI specification**
   - Put your OpenAPI specification (YAML or JSON) in the `spec/` folder.
   - By default the script looks for a file called `openapi.yaml`.

2. **Configure the prompt**
   - Edit `prompt/java_Prompt.txt` to customize the code-generation instructions.
   - The file can contain placeholders such as `{{ REQS }}` and `{{ SPEC }}`, which are replaced automatically.

3. **Run the generator**
   ```bash
   python java_chat.py
   ```

4. **Results**
   - Generated tests are saved to `output/ai_generated_tests.java`.
   - The script tries to clean up the generated code automatically.

## 📁 Project structure

```
.
├── spec/                 # OpenAPI specifications
│   └── openapi.yaml      # API specification file
├── prompt/
│   └── java_Prompt.txt   # Code-generation instructions
├── output/
│   └── ai_generated_tests.java  # Generated tests
├── build.gradle          # Gradle configuration for the Java project
├── java_chat.py          # Main generation script
└── requirements.txt      # Python dependencies
```

## ⚙️ Configuration

You can change these variables in `java_chat.py`:

- `MODEL`: Ollama model to use (default: `llama3.2:1b`)
- `SPEC_DIRECTORY`: specifications folder
- `SPEC_FILE_NAME`: specification file name
- `OUTPUT_DIR`: output folder
- `OUTPUT_FILE`: output file name
- `PRINT_TO_CONSOLE`: print the output to the console (useful for debugging)

## 📊 Output

The script produces a Java file with tests based on the OpenAPI specification, using:

- JUnit 5
- RestAssured for API testing
- AssertJ assertions

---

## 🏗️ CI/CD architecture

The generator is designed to run as the middle step of a three-repository flow:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Repo #1: api_spec                                                      │
│  └─ spec/openapi.yaml (changed on branch: dev)                          │
└────────────────────────┬────────────────────────────────────────────────┘
                         │ Merge to dev
                         ⬇
┌─────────────────────────────────────────────────────────────────────────┐
│  Pipeline 1 (Repo #1) - THOROUGH VALIDATION                             │
│  ├─ ✅ validate_openapi (swagger-cli + Spectral)                         │
│  │  ├─ Syntax validation                                                │
│  │  └─ Quality validation (custom rules)                                │
│  └─ 🚀 trigger_ai_pipeline (only if validation passes)                  │
└────────────────────────┬────────────────────────────────────────────────┘
                         │ Trigger (only if validation passes)
                         ⬇
┌─────────────────────────────────────────────────────────────────────────┐
│  Repo #2: AI code generation (this repository)                          │
│  ├─ main.py (runs Ollama)                                               │
│  ├─ spec/openapi.yaml (validated input)                                 │
│  ├─ prompt/prompt.txt (AI instructions)                                 │
│  └─ output/chat_output.py (generated artifact)                          │
└────────────────────────┬────────────────────────────────────────────────┘
                         │ Pipeline 2
                         ⬇
┌─────────────────────────────────────────────────────────────────────────┐
│  Repo #3: QA test code                                                  │
│  └─ Receives an automatic merge request with the generated output       │
│     Branch: feature-ai-update-yyyymmddHHMM → dev                        │
└─────────────────────────────────────────────────────────────────────────┘
```

### 🚀 When does it run?

| Event | Result |
|-------|--------|
| `spec/openapi.yaml` is changed and merged in **api_spec** → branch **dev** | **Pipeline 1** starts |
| Pipeline 1: **validation** (swagger-cli + Spectral) | ✅ Passes → continues / ❌ Fails → stops |
| Pipeline 1 notifies the AI repository (only if validation passed) | The **AI** runs and produces the output |
| Pipeline 2 (this repository) finishes | An **automatic merge request** is opened in the QA repository → target: **dev** |

### 🔄 Validation flow

```
Merge openapi.yaml to dev
        ⬇
   Pipeline 1
        ⬇
   validate_openapi
        ⬇
   ┌─────────────────────────────────┐
   │ 1. swagger-cli validate         │
   │    (YAML syntax + structure)    │
   └────────────┬────────────────────┘
                ⬇
            ✅ OK?
           /      \
         ✅        ❌
        /            \
       ⬇              ⬇
   ┌──────────┐   STOP
   │ Spectral │   (blocking)
   │ lint     │
   └────┬─────┘
        ⬇
   Errors?
   /      \
  ❌      ✅
 /         \
⬇           ⬇
STOP      Warnings?
(blocking) /      \
         ❌       ✅
        /           \
       ⬇             ⬇
      STOP        CONTINUE
    (blocking)    (notify)
                   ⬇
            trigger_ai_pipeline
                   ⬇
              Repo #2 (AI)
```

### 🧩 CI/CD files

```
├── main.py                 # Main script
├── .gitlab-ci.yml          # CI/CD pipeline
├── spec/openapi.yaml       # Input: API specification (from Repo #1)
├── prompt/prompt.txt       # AI instructions (template)
├── output/chat_output.py   # Output: AI-generated artifact
└── gitlab/
    ├── 1.gitlab-ci.yaml    # Repo #1 pipeline (validation + trigger)
    └── 2.gitlab-ci.yaml    # Repo #2 pipeline (this repository)
```

| File | Description |
|------|-------------|
| **main.py** | Orchestrates the flow: reads the spec, runs Ollama, saves the output |
| **spec/openapi.yaml** | OpenAPI specification received from Repo #1 |
| **prompt/prompt.txt** | Instruction template for the AI (defines what to generate) |
| **output/chat_output.py** | Automatically generated artifact (sent to Repo #3) |
| **.gitlab-ci.yml** | Pipeline that runs main.py and opens the MR in Repo #3 |

---

## ✅ OpenAPI validation in Pipeline 1

Before the AI runs, Pipeline 1 validates the OpenAPI specification thoroughly, so it meets technical and quality standards.

### 1️⃣ Syntax validation with swagger-cli

**Purpose:** check that the OpenAPI file is well formed and follows the official specification.

**Checks:**
- ✔ The YAML is well formed
- ✔ Required keys (`openapi`, `paths`, `components`, etc.) exist
- ✔ References (`$ref`) are defined correctly
- ✔ There are no orphaned or badly structured elements

**Behavior:** ⛔ if it fails, the pipeline stops immediately (blocking).

### 2️⃣ Quality validation with Spectral

**Purpose:** analyze the semantic content of the OpenAPI file against internal standard rules.

| Case | Action |
|------|--------|
| `.spectral.yaml` exists | The existing file is used |
| It does not exist | One is generated automatically with preconfigured rules |

### 📄 Spectral rules

| Rule | Type | What it checks | Severity |
|-------|------|-----------|----------|
| **operation-description** | Custom | Every endpoint has a clear description | ❌ Error |
| **schema-must-have-type** | Custom | Every schema property declares a `type` | ❌ Error |
| **required-fields** | Custom | If a schema has `properties`, it declares a `required` array | ⚠️ Warning |
| **example-required** | Custom | Every property includes an `example` value | ⚠️ Warning |

### 🚦 Pipeline failure criteria

| Condition | Result |
|-----------|----------|
| Syntax validation fails | ❌ Pipeline stopped (blocking) |
| Spectral finds errors (`severity = error`) | ❌ Pipeline stopped (blocking) |
| Spectral finds only warnings | ⚠️ Pipeline continues, with a notification |

This lets the team improve documentation step by step without blocking development on minor details.

### 🧪 Example output

```
📌 Validating OpenAPI syntax...
✓ No errors found!

🔍 Validating OpenAPI quality with Spectral...
❗ ERROR: paths./users.post description is missing
⚠ WARNING: components.schemas.User.required should be defined

❌ Violations found. Fix before merge.
```

---

## 🛠️ CI/CD requirements

| Dependency | Required | Notes |
|-------------|----------|-------|
| **Python** | 3.9+ | ✔ Required |
| **Ollama** | Installed on the runner | ✔ Required |
| **LLM model** | llama3.2:1b | ✔ Must be downloaded |
| **Git** | Installed on the runner | ✔ Required |
| **Node.js** | 18+ (Pipeline 1 runner) | ✔ For Spectral and swagger-cli |
| **swagger-cli** | NPM package | ✔ Syntax validation |
| **Spectral** | NPM package | ✔ Quality validation |
| **Linux runner** | SSH/Git access | ✔ Required |
| **GITLAB_TOKEN** | CI/CD variable | ✔ Required |

### Environment variables (GitLab CI/CD)

Set them in **Settings → CI/CD → Variables**:

| Variable | Required | Description |
|----------|-------------|-------------|
| **GITLAB_TOKEN** | ✅ | Token with `api`, `write_repository` and `write_merge_requests` scopes |
| **OLLAMA_MODEL** | ❌ | Model to use (default: `llama3.2:1b`) |

To create the token, go to **Settings → Access Tokens**, give it the three scopes above and add it as the `GITLAB_TOKEN` CI/CD variable.

On the Pipeline 1 runner, install the validation tools:

```bash
npm install -g @stoplight/spectral-cli swagger-cli
spectral --version
swagger-cli --version
```

### Automatic merge request

| Parameter | Value |
|-----------|-------|
| **Source branch** | `feature-ai-update-yyyymmddHHMM` |
| **Target branch** | `dev` |
| **Title** | `🤖 AI Generated Update from API Spec` |
| **Description** | Generated by the pipeline |

---

## 🐛 Troubleshooting

**Cannot connect to Ollama.** Make sure the server is running: `ollama serve`.

**Model not found.** Check it is installed with `ollama list`; if not, run `ollama pull <model_name>`.

**`ollama: command not found` in the pipeline.** The runner has no Ollama:
```bash
curl https://ollama.ai/install.sh | sh
ollama pull llama3.2:1b
```

**The MR is not created.** The token lacks scopes: check `api`, `write_repository` and `write_merge_requests`, and regenerate it if needed.

**Empty output.** The OpenAPI file is malformed or the prompt is missing:
```bash
ls -la spec/openapi.yaml prompt/prompt.txt
python3 -c "import yaml; yaml.safe_load(open('spec/openapi.yaml'))"
```

**Git permission errors.** Use HTTPS with the token instead of SSH:
```bash
git config --global url."https://oauth2:${GITLAB_TOKEN}@gitlab.com/".insteadOf "https://gitlab.com/"
```

**`swagger-cli: command not found` in Pipeline 1.** Install Node.js and run `npm install -g @stoplight/spectral-cli swagger-cli` on the runner.

**Spectral reports errors on a valid OpenAPI.** The `.spectral.yaml` rules are too strict: adjust them to the team's standards, or change severities from `error` to `warn`.

**Code generation is poor.** Check the OpenAPI file is valid, the prompt file is well formatted, and try a more specific prompt.

---

## 👥 Roles

| Role | Responsibility |
|------|----------------|
| **Backend team** | Maintains `spec/openapi.yaml` in Repo #1 |
| **QA team** | Maintains the `prompt.txt` logic and generated artifacts, and reviews and approves the generated MR |
| **DevOps** | Maintains CI/CD, tokens, runner and permissions |

## 📌 Roadmap

- [ ] Validate the output automatically before opening the MR
- [ ] Auto-resolve when the generated file does not change
- [ ] Post the result to a team chat channel
- [ ] LLM with incremental memory

## 🧠 Summary

✔ **Automates** the API → AI → code cycle
✔ **Removes** repetitive manual work
✔ **Keeps** consistency and versioning
✔ **Scales** to new languages or rules

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

Built by [Alejandro Sierra](https://alejandrosierra.dev/)
