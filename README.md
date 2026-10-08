# Nain — Local AI Desktop Assistant

Nain is a **local AI-powered Windows desktop assistant** designed to understand natural-language commands and interact with the Windows operating system.

The project started as a simple local AI assistant and is gradually evolving into a more capable **natural-language Windows automation system**.

> **Current Version: v0.4**
> **Status: Active Development**

---

## 🚀 Overview

Nain combines a locally running Large Language Model (LLM) with Python-based Windows tools.

Instead of requiring users to remember specific commands, Nain allows them to interact with their computer using natural language.

For example:

```text
open calculator
```

```text
close word
```

```text
open file config_test.txt
```

```text
create a file called notes.txt
```

```text
search for files on Desktop
```

Nain interprets the request, determines the appropriate action, executes the corresponding tool, and returns the result.

---

## 🤖 Local AI

Nain currently uses **LM Studio** as its local LLM backend.

### Current Model

```text
Qwen2.5-Coder-7B-Instruct
```

### Backend

```text
LM Studio
```

### Local API

```text
http://localhost:1234/v1
```

The model runs locally on the user's computer rather than relying on a cloud-based AI API.

---

## ✨ Features

### 🖥️ Windows Application Control

Nain can interact with installed Windows applications through natural-language instructions.

Current capabilities include:

* Open applications
* Close applications
* Detect running applications
* Discover installed applications
* Work with applications such as:

  * Microsoft Word
  * Microsoft PowerPoint
  * Notepad
  * Calculator
  * Other detected Windows applications

Example:

```text
open word
```

```text
close word
```

---

### 📂 File Management

Nain can perform common file-management operations.

Current tools include:

* List files
* Search files
* Read files
* Create files
* Edit files
* Copy files
* Move files
* Rename files
* Delete files

Example:

```text
open file config_test.txt
```

```text
create a file called notes.txt
```

```text
search for files on Desktop
```

---

### ⚙️ System Utilities

Nain can discover and interact with Windows system utilities through its tool system.

The assistant is designed to distinguish between:

* Applications
* System utilities
* Files
* File operations
* Windows commands

---

### 💻 Command Execution

Nain includes a command-execution tool that allows supported Windows commands to be executed through the assistant.

This provides a foundation for future Windows automation capabilities.

---

## 🧠 Tool-Based Architecture

Nain uses an agent/tool architecture rather than simply generating text responses.

The general workflow is:

```text
User
  │
  ▼
Natural Language Command
  │
  ▼
Nain Agent
  │
  ▼
Local LLM
(LM Studio + Qwen2.5-Coder)
  │
  ▼
Tool Selection
  │
  ├── Application Control
  ├── File Management
  ├── System Utilities
  └── Command Execution
  │
  ▼
Tool Execution
  │
  ▼
Result
  │
  ▼
Nain Response
```

This architecture allows the project to gradually grow by adding new tools without rebuilding the entire assistant.

---

## 🏗️ Project Structure

```text
Nain/
│
├── agent/
│   └── jarvis.py
│
├── tools/
│   └── system.py
│
├── config.py
│
├── main.py
│
├── requirements.txt
│
├── README.md
│
└── venv/
```

> The internal file and module names are currently inherited from the project's early development stage and may be renamed as Nain evolves.

---

## 🛠️ Technology Stack

| Component            | Technology                  |
| -------------------- | --------------------------- |
| Programming Language | Python                      |
| AI Model             | Qwen2.5-Coder-7B-Instruct   |
| LLM Backend          | LM Studio                   |
| Operating System     | Windows                     |
| AI Architecture      | Tool-using local agent      |
| API                  | OpenAI-compatible local API |
| Environment          | Python Virtual Environment  |

---

## 💻 System Requirements

Nain is designed to run locally on a normal Windows computer.

The current development system uses:

* Windows
* Intel Core i5-10310U
* 16 GB RAM
* 512 GB NVMe SSD
* Intel UHD Graphics

Because the LLM runs locally, performance depends on the available system resources and model configuration.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/zMHA/Nain.git
```

Enter the project directory:

```bash
cd Nain
```

---

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Install and configure LM Studio

Install LM Studio and download:

```text
Qwen2.5-Coder-7B-Instruct
```

Load the model in LM Studio and start the local server.

The default API endpoint used by Nain is:

```text
http://localhost:1234/v1
```

---

### 5. Configure Nain

Check:

```text
config.py
```

Make sure the model and LM Studio endpoint match your local configuration.

---

### 6. Start Nain

Run:

```powershell
python main.py
```

You should see something similar to:

```text
Model: qwen2.5-coder-7b-instruct
Backend: LM Studio (localhost:1234)
Type 'exit' or 'quit' to close.
```

You can then interact with Nain using natural language.

---

## 🧪 Example Commands

### Applications

```text
open calculator
```

```text
close calculator
```

```text
open word
```

```text
close word
```

### Files

```text
open file config_test.txt
```

```text
create a file called notes.txt
```

```text
edit notes.txt
```

```text
search for files on Desktop
```

### General System Interaction

```text
list applications
```

```text
list system utilities
```

```text
run command ...
```

Nain determines which tool should handle the request.

---

## 🔐 Local-First Design

One of the main goals of Nain is to maintain a **local-first architecture**.

The current AI inference is performed locally through LM Studio.

This provides several advantages:

* No mandatory cloud AI API
* Local model execution
* Greater control over data
* Offline-capable AI foundation
* Ability to customize the assistant
* Full control over the underlying tools

Nain is being developed with the long-term goal of becoming a more capable local AI environment rather than simply a chatbot.

---

## 📈 Development Roadmap

### ✅ v0.1 — Initial Assistant

* Local AI foundation
* Natural-language interaction
* Basic Windows automation

### ✅ v0.2 — Application Control

* Application discovery
* Open applications
* Close applications
* Improved Windows interaction

### ✅ v0.3 — File Management

* File discovery
* File search
* File reading
* File creation
* File editing
* File copying
* File moving
* File renaming
* File deletion

### ✅ v0.4 — Improved Command Understanding

* Improved natural-language command handling
* Better tool routing
* Improved application/file distinction
* Improved system interaction
* Expanded tool-based architecture

### 🔜 v0.5 — Next Development Phase

Planned development will focus on making Nain more capable, reliable, and intelligent when performing multi-step Windows tasks.

Potential areas include:

* More reliable tool selection
* Multi-step task execution
* Better context awareness
* Improved error handling
* More Windows automation
* Expanded system controls

### 🎯 Long-Term Vision

The long-term goal is to evolve Nain into a powerful **local AI desktop agent** capable of understanding a user's intent and completing useful computer tasks autonomously while keeping the core intelligence and execution environment under the user's control.

---

## 🏷️ Version History

| Version | Status     | Focus                                           |
| ------- | ---------- | ----------------------------------------------- |
| v0.1    | ✅ Complete | Initial local AI assistant                      |
| v0.2    | ✅ Complete | Windows application control                     |
| v0.3    | ✅ Complete | File management                                 |
| v0.4    | ✅ Complete | Improved command understanding and tool routing |
| v0.5    | 🔜 Planned | Advanced automation                             |
| v1.0    | 🎯 Future  | Stable public release                           |

---

## 🔬 Development Philosophy

Nain is being developed incrementally.

Each version introduces a new capability, is tested locally, and is then published as a milestone.

The development philosophy is:

```text
Build
  ↓
Test
  ↓
Improve
  ↓
Release
  ↓
Document
  ↓
Build the next capability
```

The project is intentionally evolving step by step rather than attempting to build a fully autonomous assistant in a single release.

---

## 📌 Current Status

**Nain v0.4 is complete.**

The project currently provides a functional foundation for a local Windows AI assistant with:

* Local LLM inference
* Natural-language interaction
* Application control
* File management
* System utilities
* Command execution
* Tool-based agent architecture

Development is ongoing toward more advanced desktop automation and agent capabilities.

---

## 👨‍💻 Author

**Muhammad Hasnain**

AI Researcher & Developer

GitHub: **[@zMHA](https://github.com/zMHA)**

---

## ⭐ Support the Project

If you find Nain interesting or useful, consider giving the repository a ⭐ on GitHub.

Contributions, ideas, experimentation, and feedback are welcome as the project continues to evolve.

---

## 📄 License

This project is currently under active development.

License information will be added as the project moves toward a stable public release.
