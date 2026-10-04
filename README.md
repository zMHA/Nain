# Jarvis v0.1

Local, text-based Windows AI assistant.

## Requirements

- Windows
- Python 3.10+
- LM Studio
- Qwen2.5-Coder-7B-Instruct Q4_K_M loaded in LM Studio
- LM Studio local server on port 1234

## Start

Open CMD:

    cd /d C:\Users\zMHA\Desktop\JarvisSystem
    venv\Scripts\activate

Make sure LM Studio's local server is running, then:

    python main.py

## Test

    hello Jarvis
    what is 25 * 4?
    list the files in C:\Users\zMHA\Desktop
    open Chrome

Terminal commands always require confirmation.

## Architecture

Python owns the tool execution loop. The local Qwen model decides whether a tool is needed, and Python performs the actual action.

This intentionally does NOT depend on Open Interpreter.
