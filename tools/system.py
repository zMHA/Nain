# ============================================================
# NAIN — SYSTEM APPLICATION TOOLS
# ============================================================

# Purpose:
#   Windows application discovery, opening, closing, and
#   system utility discovery for the Nain AI assistant.
#
# Design:
#   1. Windows system-app aliases are checked first.
#   2. Windows Start Menu is the primary source of truth.
#   3. Windows PATH is used as a fallback.
#   4. Common human-friendly application aliases are supported.
#   5. No large hardcoded application database is required.

# ============================================================


import os
import re
import subprocess


# ============================================================
# SECTION 1 — WINDOWS START MENU LOCATIONS
# ============================================================

START_MENU_PATHS = [

    # --------------------------------------------------------
    # All users
    # --------------------------------------------------------

    os.path.join(
        os.environ.get("PROGRAMDATA", ""),
        "Microsoft",
        "Windows",
        "Start Menu",
        "Programs"
    ),

    # --------------------------------------------------------
    # Current user
    # --------------------------------------------------------

    os.path.join(
        os.environ.get("APPDATA", ""),
        "Microsoft",
        "Windows",
        "Start Menu",
        "Programs"
    ),
]


# ============================================================
# SECTION 2 — COMMON APPLICATION ALIASES
# ============================================================

APPLICATION_ALIASES = {

    "vs code": "visual studio code",
    "vscode": "visual studio code",
    "code": "visual studio code",

}


# ============================================================
# SECTION 3 — WINDOWS SYSTEM APPLICATIONS
# ============================================================

# These are Windows applications/utilities that may not appear
# as normal .lnk applications in the Start Menu scan.
#
# The values are commands understood by Windows.
#
# This is intentionally kept small and focused on common
# human-friendly Windows applications.

WINDOWS_SYSTEM_APPS = {

    # Calculator
    "calculator": "calc.exe",
    "calc": "calc.exe",

    # Settings
    "settings": "ms-settings:",

    # File Explorer
    "file explorer": "explorer.exe",
    "explorer": "explorer.exe",

    # Command Prompt
    "command prompt": "cmd.exe",
    "cmd": "cmd.exe",

    # PowerShell
    "powershell": "powershell.exe",
    "windows powershell": "powershell.exe",

    # Registry Editor
    "registry editor": "regedit.exe",
    "regedit": "regedit.exe",

    # Control Panel
    "control panel": "control.exe",

    # Task Manager
    "task manager": "taskmgr.exe",
    "taskmgr": "taskmgr.exe",

    # Resource Monitor
    "resource monitor": "resmon.exe",

    # Character Map
    "character map": "charmap.exe",

    # Magnifier
    "magnifier": "magnify.exe",
    "magnify": "magnify.exe",

    # On-Screen Keyboard
    "on screen keyboard": "osk.exe",
    "on-screen keyboard": "osk.exe",

    # Narrator
    "narrator": "narrator.exe",

    # Snipping Tool
    "snipping tool": "snippingtool.exe",

}


# ============================================================
# SECTION 4 — NORMALIZE APPLICATION NAME
# ============================================================

def normalize_application_name(name):
    """
    Normalize a user-provided application name.

    Examples:

        "Open Chrome"
            -> "chrome"

        "close Excel"
            -> "excel"

        "VS Code"
            -> "visual studio code"
    """

    if not name:
        return ""

    # --------------------------------------------------------
    # Convert to lowercase and remove surrounding spaces
    # --------------------------------------------------------

    name = name.strip().lower()

    # --------------------------------------------------------
    # Remove common command prefixes
    # --------------------------------------------------------

    prefixes = [
        "open ",
        "launch ",
        "start ",
        "run ",
        "close ",
        "exit ",
        "quit ",
        "terminate "
    ]

    for prefix in prefixes:

        if name.startswith(prefix):

            name = name[len(prefix):].strip()

            break

    # --------------------------------------------------------
    # Normalize multiple spaces
    # --------------------------------------------------------

    name = " ".join(name.split())

    # --------------------------------------------------------
    # Apply application aliases
    # --------------------------------------------------------

    name = APPLICATION_ALIASES.get(
        name,
        name
    )

    return name


# ============================================================
# SECTION 5 — SEARCH WINDOWS SYSTEM APPLICATIONS
# ============================================================

def search_windows_system_app(name):
    """
    Search the internal Windows system application resolver.

    Returns:
        Windows command/path
        or None
    """

    name = normalize_application_name(name)

    if not name:
        return None

    return WINDOWS_SYSTEM_APPS.get(name)


# ============================================================
# SECTION 6 — SEARCH WINDOWS START MENU
# ============================================================

def search_start_menu(name):
    """
    Search Windows Start Menu for an application shortcut.

    Search order:

        1. Exact match
        2. Partial match
    """

    name = normalize_application_name(name)

    if not name:
        return None

    # --------------------------------------------------------
    # PASS 1 — EXACT MATCH
    # --------------------------------------------------------

    for start_menu in START_MENU_PATHS:

        if not start_menu:
            continue

        if not os.path.exists(start_menu):
            continue

        for root, dirs, files in os.walk(start_menu):

            for file in files:

                if not file.lower().endswith(".lnk"):
                    continue

                shortcut_name = (
                    os.path.splitext(file)[0]
                    .lower()
                    .strip()
                )

                if shortcut_name == name:

                    return os.path.join(
                        root,
                        file
                    )

    # --------------------------------------------------------
    # PASS 2 — PARTIAL MATCH
    # --------------------------------------------------------

    for start_menu in START_MENU_PATHS:

        if not start_menu:
            continue

        if not os.path.exists(start_menu):
            continue

        for root, dirs, files in os.walk(start_menu):

            for file in files:

                if not file.lower().endswith(".lnk"):
                    continue

                shortcut_name = (
                    os.path.splitext(file)[0]
                    .lower()
                    .strip()
                )

                # User input exists inside shortcut name
                if name in shortcut_name:

                    return os.path.join(
                        root,
                        file
                    )

                # Shortcut name exists inside user input
                if shortcut_name in name:

                    return os.path.join(
                        root,
                        file
                    )

    return None


# ============================================================
# SECTION 7 — RESOLVE WINDOWS SHORTCUT
# ============================================================

def resolve_shortcut(shortcut_path):
    """
    Resolve a Windows .lnk shortcut to its actual target.
    """

    if not shortcut_path:
        return None

    # --------------------------------------------------------
    # Already an executable/path
    # --------------------------------------------------------

    if not shortcut_path.lower().endswith(".lnk"):

        return shortcut_path

    try:

        # ----------------------------------------------------
        # Use Windows PowerShell + WScript.Shell
        # to resolve the shortcut target.
        # ----------------------------------------------------

        powershell_command = (
            "$shell = New-Object -ComObject WScript.Shell; "
            f"$shortcut = $shell.CreateShortcut('{shortcut_path}'); "
            "Write-Output $shortcut.TargetPath"
        )

        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                powershell_command
            ],
            capture_output=True,
            text=True
        )

        target = result.stdout.strip()

        if target:

            return target

    except Exception:

        pass

    return None


# ============================================================
# SECTION 8 — SEARCH WINDOWS PATH
# ============================================================

def search_windows_path(name):
    """
    Search Windows PATH for an executable.
    """

    name = normalize_application_name(name)

    if not name:
        return None

    try:

        result = subprocess.run(
            [
                "where",
                name
            ],
            capture_output=True,
            text=True,
            shell=False
        )

        if result.returncode == 0:

            paths = result.stdout.strip().splitlines()

            if paths:

                return paths[0]

    except Exception:

        pass

    return None


# ============================================================
# SECTION 9 — FIND APPLICATION
# ============================================================

def find_application(name):
    """
    Find an application using Windows discovery.

    Search order:

        1. Windows system application resolver
        2. Start Menu
        3. Windows PATH
    """

    name = normalize_application_name(name)

    if not name:
        return None

    # --------------------------------------------------------
    # METHOD 1 — WINDOWS SYSTEM APPLICATIONS
    # --------------------------------------------------------

    system_application = search_windows_system_app(name)

    if system_application:

        return system_application

    # --------------------------------------------------------
    # METHOD 2 — WINDOWS START MENU
    # --------------------------------------------------------

    shortcut = search_start_menu(name)

    if shortcut:

        return shortcut

    # --------------------------------------------------------
    # METHOD 3 — WINDOWS PATH
    # --------------------------------------------------------

    application = search_windows_path(name)

    if application:

        return application

    return None


# ============================================================
# SECTION 10 — OPEN APPLICATION
# ============================================================

def open_application(name):
    """
    Open a Windows application.
    """

    original_name = name

    name = normalize_application_name(name)

    if not name:

        return "No application name was provided."

    application = find_application(name)

    if not application:

        return (
            f"I could not find an application named "
            f"'{original_name}'."
        )

    try:

        # ----------------------------------------------------
        # WINDOWS URI / PROTOCOL
        # ----------------------------------------------------

        if (
            isinstance(application, str)
            and application.endswith(":")
        ):

            os.startfile(application)

        # ----------------------------------------------------
        # START MENU SHORTCUT
        # ----------------------------------------------------

        elif application.lower().endswith(".lnk"):

            os.startfile(application)

        # ----------------------------------------------------
        # EXECUTABLE / PATH APPLICATION
        # ----------------------------------------------------

        else:

            subprocess.Popen(
                [
                    "cmd",
                    "/c",
                    "start",
                    "",
                    application
                ],
                shell=False
            )

        return (
            f"{name.title()} opened successfully."
        )

    except Exception as e:

        return (
            f"Could not open {name}: {e}"
        )


# ============================================================
# SECTION 11 — GET ACTUAL PROCESS NAME
# ============================================================

def get_process_name(application):
    """
    Determine the actual Windows process name.
    """

    if not application:

        return None

    # --------------------------------------------------------
    # Windows system application process mappings
    # --------------------------------------------------------

    system_processes = {

        "calculator": "CalculatorApp.exe",
        "calc": "CalculatorApp.exe",

        "settings": "SystemSettings.exe",

        "file explorer": "explorer.exe",
        "explorer": "explorer.exe",

        "task manager": "Taskmgr.exe",
        "taskmgr": "Taskmgr.exe",

        "command prompt": "cmd.exe",
        "cmd": "cmd.exe",

        "powershell": "powershell.exe",
        "windows powershell": "powershell.exe",

        "registry editor": "regedit.exe",
        "regedit": "regedit.exe",

        "resource monitor": "resmon.exe",

        "control panel": "control.exe",

        "character map": "charmap.exe",

        "magnifier": "Magnify.exe",
        "magnify": "Magnify.exe",

        "on screen keyboard": "osk.exe",
        "on-screen keyboard": "osk.exe",

        "narrator": "Narrator.exe",

        "snipping tool": "SnippingTool.exe",

    }

    normalized = normalize_application_name(
        application
    )

    if normalized in system_processes:

        return system_processes[normalized]

    # --------------------------------------------------------
    # Resolve Windows shortcut
    # --------------------------------------------------------

    if application.lower().endswith(".lnk"):

        target = resolve_shortcut(application)

        if not target:

            return None

        application = target

    # --------------------------------------------------------
    # Extract executable filename
    # --------------------------------------------------------

    filename = os.path.basename(application)

    if not filename:

        return None

    if filename.lower().endswith(".exe"):

        return filename

    return filename + ".exe"


# ============================================================
# SECTION 12 — CHECK IF PROCESS IS RUNNING
# ============================================================

def is_process_running(process_name):
    """
    Check whether a Windows process is currently running.
    """

    if not process_name:

        return False

    try:

        result = subprocess.run(
            [
                "tasklist",
                "/FI",
                f"IMAGENAME eq {process_name}"
            ],
            capture_output=True,
            text=True
        )

        return (
            process_name.lower()
            in result.stdout.lower()
        )

    except Exception:

        return False


# ============================================================
# SECTION 13 — CLOSE APPLICATION
# ============================================================

def close_application(name):
    """
    Close a Windows application.

    The application is first discovered through Windows,
    then its actual executable process is determined.
    """

    original_name = name

    name = normalize_application_name(name)

    if not name:
        return "No application name was provided."

    application = find_application(name)

    # --------------------------------------------------------
    # If application is not found, check known Windows
    # system applications.
    # --------------------------------------------------------

    if not application:

        if name in WINDOWS_SYSTEM_APPS:
            application = WINDOWS_SYSTEM_APPS[name]

        else:
            return (
                f"I could not find an application named "
                f"'{original_name}'."
            )

    try:

        # ----------------------------------------------------
        # FIRST:
        # Try to determine process from the actual
        # application/shortcut that was discovered.
        # ----------------------------------------------------

        process_name = get_process_name(application)

        # ----------------------------------------------------
        # SECOND:
        # Known Windows system-app process fallbacks.
        # ----------------------------------------------------

        if not process_name:

            process_fallbacks = {

                "task manager":
                    "Taskmgr.exe",

                "command prompt":
                    "cmd.exe",

                "windows powershell":
                    "powershell.exe",

                "powershell":
                    "powershell.exe",

                "windows powershell ise":
                    "powershell_ise.exe",

                "registry editor":
                    "regedit.exe",

                "resource monitor":
                    "resmon.exe",

                "control panel":
                    "control.exe",

                "calculator":
                    "CalculatorApp.exe",

                "calc":
                    "CalculatorApp.exe",

                "settings":
                    "SystemSettings.exe",

                "character map":
                    "charmap.exe",

                "magnifier":
                    "Magnify.exe",

                "magnify":
                    "Magnify.exe",

                "on screen keyboard":
                    "osk.exe",

                "on-screen keyboard":
                    "osk.exe",

                "narrator":
                    "Narrator.exe",

                "snipping tool":
                    "SnippingTool.exe",

            }

            process_name = process_fallbacks.get(
                name.lower()
            )

        # ----------------------------------------------------
        # PROCESS COULD NOT BE DETERMINED
        # ----------------------------------------------------

        if not process_name:

            return (
                f"Could not determine the process for "
                f"{name.title()}."
            )

        # ----------------------------------------------------
        # CHECK WHETHER PROCESS IS RUNNING
        # ----------------------------------------------------

        if not is_process_running(process_name):

            return (
                f"{name.title()} is not currently running."
            )

        # ----------------------------------------------------
        # TERMINATE PROCESS
        # ----------------------------------------------------

        result = subprocess.run(
            [
                "taskkill",
                "/IM",
                process_name,
                "/F"
            ],
            capture_output=True,
            text=True
        )

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        if result.returncode == 0:

            return (
                f"{name.title()} "
                f"closed successfully."
            )

        # ----------------------------------------------------
        # PERMISSION ERROR
        # ----------------------------------------------------

        error_output = (
            result.stderr.strip()
            + " "
            + result.stdout.strip()
        )

        if (
            "Access is denied"
            in error_output
            or
            "access is denied"
            in error_output
        ):

            return (
                f"Could not close {name.title()}: "
                "Windows requires administrator privileges "
                "to terminate this application."
            )

        # ----------------------------------------------------
        # GENERAL FAILURE
        # ----------------------------------------------------

        return (
            f"{name.title()} could not be closed."
        )

    except Exception as e:

        return (
            f"Could not close {name}: {e}"
        )

# ============================================================
# SECTION 14 — LIST DISCOVERED APPLICATIONS
# ============================================================

def list_applications():
    """
    Discover normal applications from the Windows Start Menu.

    Windows remains the source of truth instead of maintaining
    a manual list of installed applications.
    """

    applications = set()

    # --------------------------------------------------------
    # ITEMS TO EXCLUDE FROM NORMAL APPLICATION LIST
    # --------------------------------------------------------

    ignored_keywords = [

        # Documentation / help
        "help",
        "manual",
        "manuals",
        "release notes",
        "module docs",

        # Uninstallers
        "uninstall",

        # Windows system utilities
        "administrative tools",
        "character map",
        "command prompt",
        "component services",
        "computer management",
        "control panel",
        "disk cleanup",
        "event viewer",
        "iscsi initiator",
        "livecaptions",
        "magnify",
        "memory diagnostics tool",
        "narrator",
        "odbc data sources",
        "on-screen keyboard",
        "performance monitor",
        "print management",
        "recoverydrive",
        "registry editor",
        "remote desktop connection",
        "resource monitor",
        "security configuration management",
        "spreadsheet compare",
        "office language preferences",
        "dfrgui",
        "run",
        "services",
        "windows defender firewall with advanced security",
        "steps recorder",
        "system configuration",
        "system information",
        "task manager",
        "task scheduler",
        "voiceaccess",
        "windows fax and scan",
        "windows media player legacy",
        "windows powershell",
        "windows powershell ise",

    ]

    # --------------------------------------------------------
    # SCAN START MENU
    # --------------------------------------------------------

    for start_menu in START_MENU_PATHS:

        if not start_menu:

            continue

        if not os.path.exists(start_menu):

            continue

        for root, dirs, files in os.walk(
            start_menu
        ):

            for file in files:

                if not file.lower().endswith(".lnk"):

                    continue

                application_name = (
                    os.path.splitext(file)[0].strip()
                )

                if not application_name:

                    continue

                name_lower = (
                    application_name.lower()
                )

                # ------------------------------------------------
                # Ignore utilities, documentation, and uninstallers
                # ------------------------------------------------

                if any(
                    keyword in name_lower
                    for keyword in ignored_keywords
                ):

                    continue

                applications.add(
                    application_name
                )

    # --------------------------------------------------------
    # SORT APPLICATIONS
    # --------------------------------------------------------

    applications = sorted(
        applications,
        key=str.lower
    )

    if not applications:

        return (
            "I could not find any usable applications "
            "in the Windows Start Menu."
        )

    # --------------------------------------------------------
    # BUILD RESPONSE
    # --------------------------------------------------------

    response = (
        "Applications available to Nain:\n\n"
    )

    for number, application in enumerate(
        applications,
        start=1
    ):

        response += (
            f"{number}. {application}\n"
        )

    return response


# ============================================================
# SECTION 15 — LIST WINDOWS SYSTEM UTILITIES
# ============================================================

def list_system_utilities():
    """
    Discover Windows system utilities from the Start Menu.
    """

    utilities = set()

    # --------------------------------------------------------
    # WINDOWS UTILITY KEYWORDS
    # --------------------------------------------------------

    utility_keywords = [

        "administrative tools",
        "character map",
        "command prompt",
        "component services",
        "computer management",
        "control panel",
        "disk cleanup",
        "dfrgui",
        "event viewer",
        "iscsi initiator",
        "livecaptions",
        "magnify",
        "memory diagnostics tool",
        "narrator",
        "office language preferences",
        "odbc data sources",
        "on-screen keyboard",
        "performance monitor",
        "print management",
        "recoverydrive",
        "registry editor",
        "remote desktop connection",
        "resource monitor",
        "run",
        "services",
        "security configuration management",
        "spreadsheet compare",
        "steps recorder",
        "system configuration",
        "system information",
        "task manager",
        "task scheduler",
        "voiceaccess",
        "windows fax and scan",
        "windows powershell",
        "windows powershell ise",
        "windows defender firewall with advanced security",
        "windows media player legacy",

    ]

    # --------------------------------------------------------
    # SCAN START MENU
    # --------------------------------------------------------

    for start_menu in START_MENU_PATHS:

        if not start_menu:

            continue

        if not os.path.exists(start_menu):

            continue

        for root, dirs, files in os.walk(
            start_menu
        ):

            for file in files:

                if not file.lower().endswith(".lnk"):

                    continue

                application_name = (
                    os.path.splitext(file)[0].strip()
                )

                if not application_name:

                    continue

                name_lower = (
                    application_name.lower()
                )

                # ------------------------------------------------
                # Check whether this is a Windows utility
                # ------------------------------------------------

                for keyword in utility_keywords:

                    if (
                        keyword.lower()
                        in name_lower
                    ):

                        utilities.add(
                            application_name
                        )

                        break

    # --------------------------------------------------------
    # ADD RESOLVABLE SYSTEM APPS
    # --------------------------------------------------------

    utilities.add("Calculator")
    utilities.add("Settings")

    # --------------------------------------------------------
    # SORT UTILITIES
    # --------------------------------------------------------

    utilities = sorted(
        utilities,
        key=str.lower
    )

    if not utilities:

        return (
            "I could not find any Windows system utilities."
        )

    # --------------------------------------------------------
    # BUILD RESPONSE
    # --------------------------------------------------------

    response = (
        "Windows system utilities available to Nain:\n\n"
    )

    for number, utility in enumerate(
        utilities,
        start=1
    ):

        response += (
            f"{number}. {utility}\n"
        )

    return response