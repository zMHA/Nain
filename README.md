# Nain — Local AI Desktop Assistant

Nain is a **local AI-powered Windows desktop assistant** designed to understand natural-language commands and interact with the Windows operating system.

The project is evolving from a basic local assistant into a more capable natural-language Windows automation system.

- **Latest completed milestone:** v0.4
- **Current development:** v0.5
- **Status:** Active development

---

## 🚀 Overview

Nain combines a locally running Large Language Model (LLM) with Python-based Windows tools. The agent interprets a request, routes it to an appropriate tool, executes the action, and returns a result.

Example requests:

```text
open calculator
close word
open file config_test.txt
create a file called notes.txt
search for files on Desktop
list open windows
close window titled Untitled - Notepad
```

Nain uses a tool-based architecture that allows new capabilities to be added incrementally.

---

## 🤖 Local AI

Nain currently uses **LM Studio** as its local LLM backend.

| Setting | Configuration |
|---|---|
| Model | Qwen2.5-Coder-7B-Instruct |
| Backend | LM Studio |
| API endpoint | `http://localhost:1234/v1` |
| Interface | OpenAI-compatible local API |

The model runs locally rather than requiring a cloud-based AI API for core inference. Performance depends on the computer's available resources and model configuration.

---

## ✨ Features

### 🖥️ Windows Application Control

Nain supports application discovery and opening and closing applications through its Windows tools.

Examples:

```text
open word
open calculator
open vs code
close word
close calculator
list applications
```

### 🪟 Window-Level Control

Nain can enumerate visible Windows desktop windows and report their:

- Window titles
- Process names
- Process IDs (PIDs)

List open windows:

```text
list open windows
show windows
open windows
```

Request that a specific window close:

```text
close window titled Untitled - Notepad
close window Chrome
```

**Window matching behavior:**

- Prefers an exact, case-insensitive title match.
- Uses partial matching when there is no exact match.
- Reports multiple matching windows rather than arbitrarily selecting one.
- Reports when a matching window cannot be found.

Nain sends the Windows `WM_CLOSE` message to request a normal application close. An application may prompt to save unsaved changes, decline the request, or take time to close. Sending the request does not guarantee that the window has closed.

### 📂 File Management

Nain includes tools for common file-management operations:

- Listing and searching for files
- Reading files
- Creating and editing files
- Copying and moving files
- Renaming files
- Deleting files

Examples:

```text
open file config_test.txt
create a file called notes.txt
edit notes.txt
search for files on Desktop
```

Use file-modification and deletion commands carefully, particularly when working with important data.

### ⚙️ System Utilities

Nain supports interactions with configured Windows system utilities through its tool-based architecture.

Example:

```text
list system utilities
```

### 💻 Command Execution

Nain includes a command-execution tool for supported Windows commands, providing a foundation for more advanced desktop automation.

Commands that modify files, settings, or system state should be tested carefully.

---

## 🧠 Tool-Based Architecture

Nain follows an agent/tool workflow:

```text
User Request
     |
     v
Natural-Language Interpretation
     |
     v
Nain Agent
     |
     v
Local LLM (LM Studio)
     |
     v
Tool Selection and Routing
     |
     +--> Application Control
     |
     +--> Window-Level Control
     |
     +--> File Management
     |
     +--> System Utilities
     |
     +--> Command Execution
     |
     v
Execution Result
     |
     v
User Response
```

This architecture separates natural-language interpretation from operating-system actions, making the project easier to extend and test.

---

## 🏗️ Project Structure

```text
Nain/
├── agent/
│   └── jarvis.py
├── tools/
│   └── system.py
├── tests/
│   └── test_window_control.py
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

The `agent/jarvis.py` and `tools/system.py` filenames are inherited from the project's earlier development.

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| AI model | Qwen2.5-Coder-7B-Instruct |
| LLM backend | LM Studio |
| Operating system | Windows |
| Agent architecture | Local tool-using agent |
| API | OpenAI-compatible local API |
| Automated testing | Python `unittest` |

---

## 💻 Development Environment

The development computer has the following specifications:

- Windows
- Intel Core i5-10310U
- 16 GB RAM
- 512 GB NVMe SSD
- Intel UHD Graphics

Since inference runs locally, performance depends on the available CPU, memory, GPU support, and model settings.

---

## ⚙️ Installation

### 1. Clone the repository

```powershell
git clone https://github.com/zMHA/Nain.git
cd Nain
```

### 2. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script activation, allow it for the current PowerShell process:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure LM Studio

Install LM Studio, download **Qwen2.5-Coder-7B-Instruct**, load the model, and start the local server.

Default endpoint:

```text
http://localhost:1234/v1
```

### 5. Check configuration

Review `config.py` and verify that the model configuration and LM Studio endpoint match your local setup.

### 6. Start Nain

```powershell
python main.py
```

You can then enter natural-language commands through Nain's interface.

---

## 💬 Example Commands

### Application Control

```text
open calculator
open word
open vs code
close word
list applications
```

### Window Control

```text
list open windows
show windows
close window titled Untitled - Notepad
```

### File Management

```text
open file config_test.txt
create a file called notes.txt
edit notes.txt
search for files on Desktop
```

### System Interaction

```text
list system utilities
run command ...
```

The exact behavior depends on the configured tools, command routing, and the response of the target application.

---

## 🧪 Automated Tests

Nain includes regression tests for window-control behavior using Python's built-in `unittest` framework.

The current test suite covers:

- Empty window titles
- Windows that cannot be found
- Multiple matching windows
- Exact title matching
- Preference for exact matches over partial matches
- Successful close-request handling
- Failed close-request handling
- Natural-language command routing for window listing and closing

Run the test suite from the project root:

```powershell
python -m unittest discover -s tests -v
```

**Latest recorded result: 8 tests passed.**

The window-control tests use mocks for the Windows close-request API. They validate the tool logic and routing, but do not guarantee identical behavior across all real applications.

Check Python syntax with:

```powershell
python -m py_compile agent\jarvis.py tools\system.py
```

---

## 🔐 Local-First Design

A central goal of Nain is to maintain a **local-first architecture**.

Design goals include:

- Local model inference through LM Studio
- No mandatory cloud AI API for core inference
- Control over model configuration and execution
- Support for offline-capable assistance when the model and required tools are available locally
- Extensible Python tools under the user's control

Local inference does not automatically make every tool operation risk-free. File operations, command execution, and window control should be tested carefully.

---

## 📈 Development Roadmap

### ✅ v0.1 — Initial Assistant

- Local AI foundation
- Natural-language interaction
- Basic Windows automation

### ✅ v0.2 — Application Control

- Application discovery
- Opening applications
- Application closing
- Improved Windows interaction

### ✅ v0.3 — File Management

- File discovery and search
- File reading and creation
- File editing, copying, moving, renaming, and deletion

### ✅ v0.4 — Improved Command Understanding

- Improved natural-language command handling
- Better tool routing
- Improved application and file-operation distinction
- Expanded tool-based architecture

### 🔨 v0.5 — Active Development

**Implemented:**

- Visible window enumeration
- Window-title, process-name, and PID reporting
- Window-close requests through `WM_CLOSE`
- Exact-match preference and ambiguity handling
- Natural-language routing for window listing and closing
- Automated window-control regression tests

**Planned improvements:**

- More reliable tool selection
- Multi-step task execution
- Better context awareness
- Improved error handling
- Additional Windows automation

### 🎯 Long-Term Vision

The goal is to evolve Nain into a capable **local AI desktop agent** that understands user intent and completes useful computer tasks while keeping its core inference and execution environment under the user's control.

---

## 🏷️ Version History

| Version | Status | Focus |
|---|---|---|
| v0.1 | Complete | Initial local AI assistant |
| v0.2 | Complete | Windows application control |
| v0.3 | Complete | File management |
| v0.4 | Complete | Improved command understanding and tool routing |
| v0.5 | In development | Window-level control and advanced automation |
| v1.0 | Future | Stable public release |

The window-control feature has been pushed to the `master` branch. Version v0.5 remains in development until a formal release is made.

---

## 🔬 Development Philosophy

Nain is developed incrementally:

```text
Build
  |
  v
Test
  |
  v
Improve
  |
  v
Release
  |
  v
Document
  |
  v
Build the Next Capability
```

Each capability should be tested locally before being documented as complete or included in a release.

---

## 📌 Current Status

**Nain v0.4 is the latest completed milestone, and v0.5 is in development.**

The current codebase includes:

- Local LLM inference through LM Studio
- Natural-language interaction
- Windows application control
- File-management tools
- System utilities
- Supported command execution
- Tool-based agent architecture
- Window-level listing and close requests
- Automated window-control regression tests

---

## 👨‍💻 Author

**Muhammad Hasnain**  
AI Researcher & Developer

GitHub: [@zMHA](https://github.com/zMHA)

---

## ⭐ Support the Project

If you find Nain interesting or useful, consider giving the repository a star.

Contributions, ideas, experimentation, and feedback are welcome as the project evolves.

---

## 📄 License

Nain is under active development. Add the appropriate license information before distributing the project as an officially licensed release.
