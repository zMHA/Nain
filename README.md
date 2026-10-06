# Nain — Local AI Desktop Assistant

Nain is a local AI desktop assistant that uses a language model running through LM Studio to understand natural-language commands and interact with Windows applications.

The project started as a simple local AI assistant and is gradually evolving into a more capable Windows automation system.

**Current Version:** v0.1 — Application & System Control
**Current Status:** Active development
**Model Backend:** LM Studio
**Current Model:** Qwen2.5-Coder-7B-Instruct

---

## Features

### 🤖 Local AI

Nain uses a locally running language model through LM Studio.

* Local inference through LM Studio
* OpenAI-compatible API
* Natural-language interaction
* Tool-based action execution
* Configurable model, temperature, and token limits
* No cloud LLM API is required for the core assistant

---

### 🖥️ Windows Application Control

Nain can discover and control Windows applications without requiring every application to be manually added to a configuration file.

The Windows Start Menu is used as the primary source of application discovery, with Windows PATH used as a fallback.

#### Open applications

Examples:

```text
open Chrome
open Word
open Excel
open Task Manager
open VS Code
```

Nain also understands common application aliases:

```text
open vs code
open vscode
open code
```

These are resolved to:

```text
Visual Studio Code
```

#### Close applications

Examples:

```text
close Chrome
close Word
close Excel
close VS Code
close Task Manager
```

---

### 🔀 Multi-Action Commands

Nain can execute multiple independent actions from a single natural-language command.

For example:

```text
open Word and Excel
```

or:

```text
open Chrome and Task Manager
```

It can also process multiple closing actions:

```text
close Word and Excel
```

The model produces multiple tool calls and Nain executes them in the requested order.

---

### 📋 Application Discovery

Nain can discover applications installed through the Windows Start Menu.

Example:

```text
list applications
```

It can return applications such as:

```text
Google Chrome
Microsoft Edge
Visual Studio Code
Microsoft Word
Microsoft Excel
PowerPoint
LM Studio
Notepad
...
```

This means applications do not need to be manually registered one by one.

---

### ⚙️ Windows System Utilities

Nain can also discover Windows system utilities separately.

Example:

```text
list system utilities
```

Examples include:

```text
Task Manager
Command Prompt
PowerShell
Registry Editor
Control Panel
Resource Monitor
Event Viewer
Services
System Information
Task Scheduler
...
```

This separation keeps normal applications and Windows utilities organized.

---

## 🧠 Tool-Based Architecture

Nain does not simply generate text responses.

When an action is required, the language model generates a structured tool request.

### Single action

```json
{
  "tool": "open_application",
  "arguments": {
    "name": "Chrome"
  }
}
```

### Multiple actions

```json
{
  "tools": [
    {
      "tool": "open_application",
      "arguments": {
        "name": "Chrome"
      }
    },
    {
      "tool": "open_application",
      "arguments": {
        "name": "Visual Studio Code"
      }
    }
  ]
}
```

Nain then executes the requested tools locally.

This architecture allows new capabilities to be added as independent tools instead of putting all functionality into a single large program.

---

## 🏗️ Project Structure

```text
Nain/
│
├── main.py
├── config.py
│
├── agent/
│   └── jarvis.py
│
├── tools/
│   ├── system.py
│   ├── files.py
│   └── terminal.py
│
└── venv/
```

### Main components

**`main.py`**

Starts the Nain assistant and provides the interactive command-line interface.

**`config.py`**

Contains LM Studio configuration and the system prompt that defines Nain's behavior and available tools.

**`agent/jarvis.py`**

Handles communication with the language model, tool parsing, and tool execution.

**`tools/system.py`**

Provides Windows application discovery, application launching, application closing, application aliases, and Windows system utility discovery.

**`tools/files.py`**

Provides file-related functionality and is currently part of the project's expanding tool system.

**`tools/terminal.py`**

Provides terminal-related functionality.

---

## 💻 Current Environment

The current development environment uses:

* Windows
* Python
* LM Studio
* Qwen2.5-Coder-7B-Instruct
* PowerShell / Windows Terminal
* Python virtual environment

### LM Studio Endpoint

```text
http://localhost:1234/v1/chat/completions
```

---

## 🚀 Running Nain

Clone the repository:

```bash
git clone https://github.com/zMHA/Nain.git
cd Nain
```

Create a virtual environment:

```bash
python -m venv venv
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Start LM Studio and load the configured model.

Then run:

```powershell
.\venv\Scripts\python.exe main.py
```

You should see:

```text
Model: qwen2.5-coder-7b-instruct
Backend: LM Studio (localhost:1234)
Type 'exit' or 'quit' to close.
```

---

## 🧪 Example Interaction

### Open an application

```text
You: open vs code

[Tool requested: open_application]
[Tool execution completed]

Nain: Visual Studio Code opened successfully.
```

### Multiple applications

```text
You: open notepad and task manager

[Tool requested: open_application]
[Tool execution completed]

[Tool requested: open_application]
[Tool execution completed]

Nain: Notepad opened successfully.
Task Manager opened successfully.
```

### Multiple closing actions

```text
You: close task manager and notepad

[Tool requested: close_application]
[Tool execution completed]

[Tool requested: close_application]
[Tool execution completed]

Nain: Task Manager closed successfully.
Notepad closed successfully.
```

---

## 🛠️ Development Roadmap

Nain is being developed incrementally.

### ✅ Completed

* Local LLM integration through LM Studio
* Natural-language command processing
* Tool-based architecture
* Windows application discovery
* Start Menu application discovery
* Windows PATH fallback
* Application launching
* Application closing
* Application aliases
* Application listing
* Windows system utility discovery
* Multi-action commands
* Sequential multi-tool execution

### 🔨 Next Development Stage

* Window-level application control
* Close a specific application instance/window
* File search and management improvements
* More advanced Windows automation
* Better tool selection and intent handling
* Improved error handling
* More natural conversational interaction

### 🔮 Future

* Graphical user interface
* Voice interaction
* More advanced computer interaction
* Expanded local AI capabilities

---

## 🎯 Long-Term Vision

The goal of Nain is to develop a capable local AI desktop assistant that can understand natural language and interact with the user's computer through reliable, structured tools.

The long-term system is intended to move beyond simple application launching toward:

```text
Natural Language
       ↓
      Nain
       ↓
Intent Understanding
       ↓
Tool Selection
       ↓
Windows / Files / Terminal
       ↓
Action
       ↓
Result
```

The emphasis is on building the system incrementally, testing each capability, and documenting its development publicly.

---

## 📌 Project Status

Nain is an experimental personal AI assistant under active development.

Features and architecture may change as the project evolves.

Major versions and development milestones will be documented as the project progresses.

---

## 👨‍💻 Author

**Muhammad Hasnain**

AI Student & Researcher

* LinkedIn: https://www.linkedin.com/in/zmha1270/
* GitHub: https://github.com/zMHA
* Google Scholar: https://scholar.google.com/citations?user=VE-85okAAAAJ&hl=en
* ORCID: https://orcid.org/0009-0003-8191-5092

---

## 📄 License

License information will be added as the project develops.
