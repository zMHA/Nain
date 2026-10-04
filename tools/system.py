# ============================================================
# SECTION 1 — IMPORTS
# ============================================================

import subprocess


# ============================================================
# SECTION 2 — APPLICATION DATABASE
# ============================================================

APPLICATIONS = {
    # Browsers
    "chrome": "chrome",
    "google chrome": "chrome",
    "chrome browser": "chrome",

    "edge": "msedge",
    "microsoft edge": "msedge",

    # Windows applications
    "calculator": "calc",
    "calc": "calc",
    "windows calculator": "calc",

    "notepad": "notepad",
    "windows notepad": "notepad",

    "explorer": "explorer",
    "file explorer": "explorer",
    "windows explorer": "explorer",

    # VS Code
    "vscode": "code",
    "vs code": "code",
    "visual studio code": "code",
}


# ============================================================
# SECTION 3 — OPEN APPLICATION
# ============================================================

def open_application(name):

    name = name.strip().lower()

    if name not in APPLICATIONS:
        return (
            f"I don't have a configured launcher for '{name}'. "
            f"Available applications: "
            f"{', '.join(sorted(APPLICATIONS.keys()))}"
        )

    application = APPLICATIONS[name]

    try:
        subprocess.Popen(
            ["cmd", "/c", "start", "", application],
            shell=False
        )

        return f"{name.title()} opened successfully."

    except Exception as e:
        return f"Could not open {name}: {e}"


# ============================================================
# SECTION 4 — CLOSE APPLICATION
# ============================================================

def close_application(name):
    name = name.strip().lower()

    if name not in APPLICATIONS:
        return (
            f"I don't have a configured application for '{name}'. "
            f"Available applications: "
            f"{', '.join(sorted(APPLICATIONS.keys()))}"
        )

    application = APPLICATIONS[name]

    try:
        # Windows Calculator is a packaged app.
        # Close it through its process name.
        if application == "calc":
            result = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    "Get-Process CalculatorApp -ErrorAction SilentlyContinue | Stop-Process -Force"
                ],
                capture_output=True,
                text=True
            )

            # Check whether Calculator is still running
            check = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    "Get-Process CalculatorApp -ErrorAction SilentlyContinue"
                ],
                capture_output=True,
                text=True
            )

            if not check.stdout.strip():
                return "Calculator closed successfully."

            return "Calculator could not be closed."

        # Normal Win32 applications
        result = subprocess.run(
            ["taskkill", "/IM", f"{application}.exe", "/F"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return f"{name.title()} closed successfully."

        return f"{name.title()} is not currently running."

    except Exception as e:
        return f"Could not close {name}: {e}"