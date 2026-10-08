import json
import re
import urllib.request
import urllib.error

from config import (
    LM_STUDIO_URL,
    MODEL,
    MAX_TOKENS,
    TEMPERATURE,
    SYSTEM_PROMPT
)

from tools.system import (
    open_application,
    close_application,
    list_applications,
    list_system_utilities
)

from tools.files import (
    list_files,
    read_file,
    create_file,
    edit_file,
    search_files,
    copy_file,
    move_file,
    rename_file,
    delete_file,
)

from tools.terminal import run_command


class Jarvis:

    def __init__(self):

        self.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

    # ==========================================================
    # ASK LM STUDIO
    # ==========================================================

    def ask_model(self):

        payload = {
            "model": MODEL,
            "messages": self.messages,
            "temperature": TEMPERATURE,
            "max_tokens": MAX_TOKENS,
            "stream": False
        }

        data = json.dumps(payload).encode("utf-8")

        request = urllib.request.Request(
            LM_STUDIO_URL,
            data=data,
            headers={
                "Content-Type": "application/json"
            }
        )

        try:

            with urllib.request.urlopen(
                request,
                timeout=180
            ) as response:

                raw_response = (
                    response
                    .read()
                    .decode("utf-8")
                )

            result = json.loads(raw_response)

            message = result["choices"][0]["message"]

            content = message.get(
                "content",
                ""
            )

            if content is None:
                content = ""

            return content.strip()

        except urllib.error.URLError as e:

            return (
                f"LM Studio connection error: {e}"
            )

        except TimeoutError:

            return (
                "Model error: "
                "LM Studio request timed out."
            )

        except Exception as e:

            return f"Model error: {e}"

    # ==========================================================
    # PARSE TOOL JSON
    # ==========================================================

    def parse_tool(self, text):

        if not text:
            return None

        # ------------------------------------------------------
        # Direct JSON
        # ------------------------------------------------------

        try:

            data = json.loads(
                text.strip()
            )

            if isinstance(data, dict):

                if "tool" in data:
                    return data

                if "tools" in data:
                    return data

        except json.JSONDecodeError:
            pass

        # ------------------------------------------------------
        # JSON inside markdown code block
        # ------------------------------------------------------

        match = re.search(
            r"```(?:json)?\s*(\{.*?\})\s*```",
            text,
            re.DOTALL | re.IGNORECASE
        )

        if match:

            try:

                data = json.loads(
                    match.group(1)
                )

                if isinstance(data, dict):

                    if "tool" in data:
                        return data

                    if "tools" in data:
                        return data

            except json.JSONDecodeError:
                pass

        # ------------------------------------------------------
        # Single-tool JSON somewhere in response
        # ------------------------------------------------------

        match = re.search(
            r'\{.*?"tool"\s*:\s*".*?".*?\}',
            text,
            re.DOTALL
        )

        if match:

            try:

                data = json.loads(
                    match.group(0)
                )

                if (
                    isinstance(data, dict)
                    and "tool" in data
                ):
                    return data

            except json.JSONDecodeError:
                pass

        # ------------------------------------------------------
        # Multi-tool JSON somewhere in response
        # ------------------------------------------------------

        match = re.search(
            r'\{.*?"tools"\s*:\s*\[.*?\]\s*\}',
            text,
            re.DOTALL
        )

        if match:

            try:

                data = json.loads(
                    match.group(0)
                )

                if (
                    isinstance(data, dict)
                    and "tools" in data
                ):
                    return data

            except json.JSONDecodeError:
                pass

        return None

    # ==========================================================
    # EXECUTE TOOL
    # ==========================================================

    def execute_tool(self, tool_data):

        tool = tool_data.get(
            "tool"
        )

        arguments = tool_data.get(
            "arguments",
            {}
        )

        try:

            # --------------------------------------------------
            # OPEN APPLICATION
            # --------------------------------------------------

            if tool == "open_application":

                return open_application(
                    arguments.get(
                        "name",
                        ""
                    )
                )

            # --------------------------------------------------
            # CLOSE APPLICATION
            # --------------------------------------------------

            elif tool == "close_application":

                return close_application(
                    arguments.get(
                        "name",
                        ""
                    )
                )

            # --------------------------------------------------
            # LIST APPLICATIONS
            # --------------------------------------------------

            elif tool == "list_applications":

                return list_applications()

            # --------------------------------------------------
            # LIST SYSTEM UTILITIES
            # --------------------------------------------------

            elif tool == "list_system_utilities":

                return list_system_utilities()

            # --------------------------------------------------
            # LIST FILES
            # --------------------------------------------------

            elif tool == "list_files":

                return list_files(
                    arguments.get(
                        "path",
                        ""
                    )
                )

            # --------------------------------------------------
            # READ FILE
            # --------------------------------------------------

            elif tool == "read_file":

                return read_file(
                    arguments.get(
                        "path",
                        ""
                    )
                )

            # --------------------------------------------------
            # CREATE FILE
            # --------------------------------------------------

            elif tool == "create_file":

                return create_file(
                    arguments.get(
                        "path",
                        ""
                    ),
                    arguments.get(
                        "content",
                        ""
                    )
                )

            # --------------------------------------------------
            # EDIT FILE
            # --------------------------------------------------

            elif tool == "edit_file":

                return edit_file(
                    arguments.get(
                        "path",
                        ""
                    ),
                    arguments.get(
                        "content",
                        ""
                    )
                )

            # --------------------------------------------------
            # SEARCH FILES
            # --------------------------------------------------

            elif tool == "search_files":

                return search_files(
                    arguments.get(
                        "path",
                        ""
                    ),
                    arguments.get(
                        "pattern",
                        "*"
                    ),
                    arguments.get(
                        "recursive",
                        False
                    )
                )

            # --------------------------------------------------
            # COPY FILE
            # --------------------------------------------------

            elif tool == "copy_file":

                return copy_file(
                    arguments.get(
                        "source",
                        ""
                    ),
                    arguments.get(
                        "destination",
                        ""
                    )
                )

            # --------------------------------------------------
            # MOVE FILE
            # --------------------------------------------------

            elif tool == "move_file":

                return move_file(
                    arguments.get(
                        "source",
                        ""
                    ),
                    arguments.get(
                        "destination",
                        ""
                    )
                )

            # --------------------------------------------------
            # RENAME FILE
            # --------------------------------------------------

            elif tool == "rename_file":

                return rename_file(
                    arguments.get(
                        "path",
                        ""
                    ),
                    arguments.get(
                        "new_name",
                        ""
                    )
                )

            # --------------------------------------------------
            # DELETE FILE
            # --------------------------------------------------

            elif tool == "delete_file":

                return delete_file(
                    arguments.get(
                        "path",
                        ""
                    )
                )

            # --------------------------------------------------
            # RUN COMMAND
            # --------------------------------------------------

            elif tool == "run_command":

                return run_command(
                    arguments.get(
                        "command",
                        ""
                    )
                )

            # --------------------------------------------------
            # UNKNOWN TOOL
            # --------------------------------------------------

            else:

                return f"Unknown tool: {tool}"

        except Exception as e:

            return (
                f"Tool execution error: {e}"
            )

    # ==========================================================
    # TEXT NORMALIZATION
    # ==========================================================

    def _clean_command_text(self, text):

        return " ".join(
            text.strip()
            .lower()
            .split()
        )

    # ==========================================================
    # APPLICATION NAME EXTRACTION
    # ==========================================================

    def _extract_application_names(self, app_text):

        text = app_text.strip()

        # Normalize comma spacing
        text = re.sub(
            r"\s*,\s*",
            ",",
            text
        )

        # "and" becomes separator
        text = re.sub(
            r"\s+\band\b\s+",
            ",",
            text,
            flags=re.IGNORECASE
        )

        parts = [
            part.strip()
            for part in text.split(",")
            if part.strip()
        ]

        return parts

    # ==========================================================
    # BUILD APPLICATION TOOL REQUESTS
    # ==========================================================

    def _build_tool_requests(
        self,
        tool_name,
        app_names
    ):

        requests = [
            {
                "tool": tool_name,
                "arguments": {
                    "name": name
                }
            }
            for name in app_names
        ]

        if len(requests) == 1:
            return requests[0]

        return {
            "tools": requests
        }

    # ==========================================================
    # PATH HELPERS — v0.4
    # ==========================================================

    def _desktop_path(self):

        return r"C:\Users\zMHA\Desktop"

    def _jarvis_system_path(self):

        return r"C:\Users\zMHA\Desktop\JarvisSystem"

    def _resolve_file_path(self, path):

        """
        Convert simple user paths into Windows paths.

        Examples:

        notes.txt
            -> Desktop\\notes.txt

        Desktop\\notes.txt
            -> Desktop\\notes.txt

        JarvisSystem\\notes.txt
            -> Desktop\\JarvisSystem\\notes.txt
        """

        if not path:
            return ""

        path = path.strip().strip('"').strip("'")

        # Already an absolute Windows path
        if re.match(
            r"^[A-Za-z]:\\",
            path
        ):
            return path

        normalized = path.replace(
            "/",
            "\\"
        )

        lower_path = normalized.lower()

        desktop_prefixes = [
            "desktop\\",
            "desktop/"
        ]

        for prefix in desktop_prefixes:

            if lower_path.startswith(
                prefix
            ):

                remainder = normalized[
                    len(prefix):
                ]

                return (
                    self._desktop_path()
                    + "\\"
                    + remainder
                )

        jarvis_prefixes = [
            "jarvissystem\\",
            "jarvissystem/"
        ]

        for prefix in jarvis_prefixes:

            if lower_path.startswith(
                prefix
            ):

                remainder = normalized[
                    len(prefix):
                ]

                return (
                    self._jarvis_system_path()
                    + "\\"
                    + remainder
                )

        # Bare filename/path -> Desktop
        return (
            self._desktop_path()
            + "\\"
            + normalized
        )

    # ==========================================================
    # SEARCH PATH DETECTION
    # ==========================================================

    def _detect_search_location(self, text):

        """
        Determine search location and recursive behavior.

        Desktop:
            recursive=False

        JarvisSystem:
            recursive=True

        Explicit recursive/subfolder search:
            recursive=True
        """

        clean = self._clean_command_text(
            text
        )

        # ------------------------------------------------------
        # JarvisSystem
        # ------------------------------------------------------

        if (
            "jarvissystem" in clean
            or "inside this folder" in clean
            or "inside this directory" in clean
            or "all subfolders" in clean
            or "recursively" in clean
            or "anywhere inside" in clean
        ):

            return (
                self._jarvis_system_path(),
                True
            )

        # ------------------------------------------------------
        # Desktop
        # ------------------------------------------------------

        if (
            "on desktop" in clean
            or "in desktop" in clean
            or "from desktop" in clean
            or clean.endswith("desktop")
        ):

            return (
                self._desktop_path(),
                False
            )

        # ------------------------------------------------------
        # Default
        # ------------------------------------------------------

        return (
            self._desktop_path(),
            False
        )

    # ==========================================================
    # SEARCH PATTERN DETECTION
    # ==========================================================

    def _extract_search_pattern(self, text):

        clean = self._clean_command_text(
            text
        )

        # ------------------------------------------------------
        # Explicit wildcard
        # ------------------------------------------------------

        wildcard_match = re.search(
            r"([A-Za-z0-9_\-*?.]+\.[A-Za-z0-9_*?]+)",
            clean
        )

        if wildcard_match:

            return wildcard_match.group(1)

        # ------------------------------------------------------
        # "txt files"
        # ------------------------------------------------------

        extension_match = re.search(
            r"\b([a-z0-9]+)\s+files?\b",
            clean
        )

        if extension_match:

            extension = extension_match.group(1)

            # Avoid interpreting generic words as extensions
            ignored = {
                "all",
                "the",
                "my",
                "this",
                "these",
                "folder",
                "folders",
                "files",
                "file"
            }

            if extension not in ignored:

                return (
                    "*."
                    + extension
                )

        # ------------------------------------------------------
        # "python files", "image files", etc.
        # ------------------------------------------------------

        if "python files" in clean:
            return "*.py"

        if "text files" in clean:
            return "*.txt"

        if "word files" in clean:
            return "*.docx"

        if "excel files" in clean:
            return "*.xlsx"

        if "powerpoint files" in clean:
            return "*.pptx"

        # ------------------------------------------------------
        # Search for explicit filename
        # ------------------------------------------------------

        filename_match = re.search(
            r"\b[\w\-.]+\.[a-z0-9]{1,8}\b",
            clean
        )

        if filename_match:

            return filename_match.group(0)

        # ------------------------------------------------------
        # Default
        # ------------------------------------------------------

        return "*"

    # ==========================================================
    # EXTRACT FILENAME
    # ==========================================================

    def _extract_filename_from_command(
        self,
        text
    ):

        clean = text.strip()

        # Quoted filename
        quoted = re.search(
            r'["\']([^"\']+\.[A-Za-z0-9]+)["\']',
            clean
        )

        if quoted:

            return quoted.group(1)

        # Normal filename
        match = re.search(
            r"\b[\w\-.]+\.[A-Za-z0-9]{1,8}\b",
            clean
        )

        if match:

            return match.group(0)

        return None

    # ==========================================================
    # EXTRACT CONTENT
    # ==========================================================

    def _extract_file_content(
        self,
        text
    ):

        patterns = [
            r"\bwith content\s+(.+)$",
            r"\bcontent\s*[:=]\s*(.+)$",
            r"\bcontaining\s+(.+)$"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE
            )

            if match:

                content = match.group(1).strip()

                return content.strip(
                    '"'
                ).strip("'")

        return ""

    # ==========================================================
    # FILE / FOLDER ROUTER — v0.4
    # ==========================================================

    def detect_file_tool(
        self,
        user_input
    ):

        original = user_input.strip()

        text = self._clean_command_text(
            original
        )

        # ======================================================
        # LIST FILES
        # ======================================================

        list_patterns = [
            r"^list files$",
            r"^list files on desktop$",
            r"^list files in desktop$",
            r"^show files$",
            r"^show files on desktop$",
            r"^show files in desktop$",
            r"^show me the files$",
            r"^show me files on desktop$",
            r"^show me files in desktop$",
            r"^list files in jarvissystem$",
            r"^list files inside jarvissystem$",
            r"^show files in jarvissystem$",
            r"^show files inside jarvissystem$"
        ]

        if any(
            re.match(
                pattern,
                text
            )
            for pattern in list_patterns
        ):

            if "jarvissystem" in text:

                path = self._jarvis_system_path()

            else:

                path = self._desktop_path()

            return {
                "tool": "list_files",
                "arguments": {
                    "path": path
                }
            }

        # ======================================================
        # SEARCH / FIND FILES
        # ======================================================

        search_starters = [
            "find ",
            "search ",
            "look for ",
            "find all ",
            "search for "
        ]

        is_search = any(
            text.startswith(prefix)
            for prefix in search_starters
        )

        if is_search:

            path, recursive = (
                self._detect_search_location(
                    text
                )
            )

            pattern = (
                self._extract_search_pattern(
                    text
                )
            )

            return {
                "tool": "search_files",
                "arguments": {
                    "path": path,
                    "pattern": pattern,
                    "recursive": recursive
                }
            }

        # ======================================================
        # READ FILE
        # ======================================================

        read_prefixes = [
            "read ",
            "open file ",
            "show file ",
            "display file ",
            "read file "
        ]

        for prefix in read_prefixes:

            if text.startswith(prefix):

                filename = original[
                    len(prefix):
                ].strip()

                if filename:

                    path = (
                        self._resolve_file_path(
                            filename
                        )
                    )

                    return {
                        "tool": "read_file",
                        "arguments": {
                            "path": path
                        }
                    }

        # ======================================================
        # CREATE FILE
        # ======================================================

        create_match = re.match(
            r"^(?:create|make)\s+(?:a\s+)?file\s+(?:called|named)\s+(.+)$",
            original,
            flags=re.IGNORECASE
        )

        if create_match:

            remainder = (
                create_match
                .group(1)
                .strip()
            )

            content = (
                self._extract_file_content(
                    remainder
                )
            )

            # Remove content part from filename
            filename = re.split(
                r"\bwith content\b|\bcontent\s*[:=]|\bcontaining\b",
                remainder,
                maxsplit=1,
                flags=re.IGNORECASE
            )[0].strip()

            path = (
                self._resolve_file_path(
                    filename
                )
            )

            return {
                "tool": "create_file",
                "arguments": {
                    "path": path,
                    "content": content
                }
            }

        # ======================================================
        # EDIT FILE
        # ======================================================

        edit_match = re.match(
            r"^(?:edit|modify|update)\s+(?:file\s+)?(.+?)\s+(?:with content|content\s*[:=]|containing)\s+(.+)$",
            original,
            flags=re.IGNORECASE
        )

        if edit_match:

            filename = (
                edit_match
                .group(1)
                .strip()
            )

            content = (
                edit_match
                .group(2)
                .strip()
                .strip('"')
                .strip("'")
            )

            path = (
                self._resolve_file_path(
                    filename
                )
            )

            return {
                "tool": "edit_file",
                "arguments": {
                    "path": path,
                    "content": content
                }
            }

        # ======================================================
        # COPY FILE
        # ======================================================

        copy_match = re.match(
            r"^copy\s+(.+?)\s+to\s+(.+)$",
            original,
            flags=re.IGNORECASE
        )

        if copy_match:

            source = (
                copy_match
                .group(1)
                .strip()
            )

            destination = (
                copy_match
                .group(2)
                .strip()
            )

            return {
                "tool": "copy_file",
                "arguments": {
                    "source": self._resolve_file_path(
                        source
                    ),
                    "destination": self._resolve_file_path(
                        destination
                    )
                }
            }

        # ======================================================
        # MOVE FILE
        # ======================================================

        move_match = re.match(
            r"^move\s+(.+?)\s+to\s+(.+)$",
            original,
            flags=re.IGNORECASE
        )

        if move_match:

            source = (
                move_match
                .group(1)
                .strip()
            )

            destination = (
                move_match
                .group(2)
                .strip()
            )

            return {
                "tool": "move_file",
                "arguments": {
                    "source": self._resolve_file_path(
                        source
                    ),
                    "destination": self._resolve_file_path(
                        destination
                    )
                }
            }

        # ======================================================
        # RENAME FILE
        # ======================================================

        rename_match = re.match(
            r"^rename\s+(.+?)\s+to\s+(.+)$",
            original,
            flags=re.IGNORECASE
        )

        if rename_match:

            old_name = (
                rename_match
                .group(1)
                .strip()
            )

            new_name = (
                rename_match
                .group(2)
                .strip()
            )

            # Remove quotes
            old_name = (
                old_name
                .strip('"')
                .strip("'")
            )

            new_name = (
                new_name
                .strip('"')
                .strip("'")
            )

            return {
                "tool": "rename_file",
                "arguments": {
                    "path": self._resolve_file_path(
                        old_name
                    ),
                    "new_name": new_name
                }
            }

        # ======================================================
        # DELETE FILE
        # ======================================================

        delete_match = re.match(
            r"^(?:delete|remove)\s+(?:file\s+)?(.+)$",
            original,
            flags=re.IGNORECASE
        )

        if delete_match:

            filename = (
                delete_match
                .group(1)
                .strip()
            )

            filename = (
                filename
                .strip('"')
                .strip("'")
            )

            return {
                "tool": "delete_file",
                "arguments": {
                    "path": self._resolve_file_path(
                        filename
                    )
                }
            }

        return None

    # ==========================================================
    # DETERMINISTIC SIMPLE TOOL ROUTER
    # ==========================================================

    def detect_simple_tool(
        self,
        user_input
    ):

        text = self._clean_command_text(
            user_input
        )

        # ======================================================
        # RUN COMMAND
        # IMPORTANT:
        # Must be checked before generic "run"
        # application opening.
        # ======================================================

        run_command_prefixes = [
            "run command ",
            "execute command ",
            "execute the command "
        ]

        for prefix in run_command_prefixes:

            if text.startswith(prefix):

                command = (
                    text[len(prefix):]
                    .strip()
                )

                if command:

                    return {
                        "tool": "run_command",
                        "arguments": {
                            "command": command
                        }
                    }

                return None

        # ======================================================
        # SYSTEM UTILITIES
        # ======================================================

        system_utility_phrases = [

            "list system utilities",

            "show system utilities",

            "what system utilities are available",

            "what windows utilities are available",

            "show me windows utilities",

            "list windows utilities",

            "show system tools",

            "what system tools are available",

            "what system tools can you open"
        ]

        if any(
            phrase in text
            for phrase in system_utility_phrases
        ):

            return {
                "tool": "list_system_utilities",
                "arguments": {}
            }

        # ======================================================
        # APPLICATION LISTING
        # ======================================================

        application_list_phrases = [

            "list application",
            "list applications",
            "list app",
            "list apps",

            "list all applications",
            "list all apps",

            "show application",
            "show applications",
            "show app",
            "show apps",

            "show me my applications",
            "show me my apps",

            "what applications are installed",
            "what applications do i have",

            "what apps are installed",

            "what applications can you open",
            "what apps can you open",

            "which applications are available"
        ]

        if any(
            phrase in text
            for phrase in application_list_phrases
        ):

            return {
                "tool": "list_applications",
                "arguments": {}
            }

        # ======================================================
        # OPEN APPLICATION
        # ======================================================

        open_phrases = [
            "open ",
            "launch ",
            "start ",
            "run "
        ]

        for phrase in open_phrases:

            if text.startswith(phrase):

                app_text = (
                    text[len(phrase):]
                    .strip()
                )

                if app_text:

                    app_names = (
                        self._extract_application_names(
                            app_text
                        )
                    )

                    if app_names:

                        return (
                            self._build_tool_requests(
                                "open_application",
                                app_names
                            )
                        )

        # ======================================================
        # CLOSE APPLICATION
        # ======================================================

        close_phrases = [
            "close ",
            "exit ",
            "quit ",
            "terminate "
        ]

        for phrase in close_phrases:

            if text.startswith(phrase):

                app_text = (
                    text[len(phrase):]
                    .strip()
                )

                if app_text:

                    app_names = (
                        self._extract_application_names(
                            app_text
                        )
                    )

                    if app_names:

                        return (
                            self._build_tool_requests(
                                "close_application",
                                app_names
                            )
                        )

        return None

    # ==========================================================
    # PROCESS USER REQUEST
    # ==========================================================

    def process(
        self,
        user_input
    ):
        self.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        # ======================================================
        # v0.4 FILE / FOLDER ROUTER
        #
        # IMPORTANT:
        # File routing is checked BEFORE application routing.
        #
        # This prevents:
        #     open file config_test.txt
        #
        # from being interpreted as:
        #     open_application
        # ======================================================

        file_tool = (
            self.detect_file_tool(
                user_input
            )
        )

        if file_tool:

            # --------------------------------------------------
            # MULTIPLE FILE TOOLS
            # --------------------------------------------------

            if "tools" in file_tool:

                tool_requests = (
                    file_tool.get(
                        "tools",
                        []
                    )
                )

                if not isinstance(
                    tool_requests,
                    list
                ):
                    return (
                        "Invalid multi-tool request."
                    )

                results = []

                for tool_request in tool_requests:

                    if not isinstance(
                        tool_request,
                        dict
                    ):
                        continue

                    tool_name = (
                        tool_request.get(
                            "tool",
                            "unknown"
                        )
                    )

                    print(
                        f"\n[Tool requested: {tool_name}]"
                    )

                    result = (
                        self.execute_tool(
                            tool_request
                        )
                    )

                    print(
                        "[Tool execution completed]"
                    )

                    results.append(
                        str(result)
                    )

                if not results:
                    return (
                        "No valid tools were requested."
                    )

                return "\n".join(
                    results
                )

            # --------------------------------------------------
            # SINGLE FILE TOOL
            # --------------------------------------------------

            tool_name = (
                file_tool.get(
                    "tool",
                    "unknown"
                )
            )

            print(
                f"\n[Tool requested: {tool_name}]"
            )

            result = (
                self.execute_tool(
                    file_tool
                )
            )

            print(
                "[Tool execution completed]"
            )

            return result

        # ======================================================
        # v0.3 DETERMINISTIC APPLICATION / COMMAND ROUTER
        # ======================================================

        simple_tool = (
            self.detect_simple_tool(
                user_input
            )
        )

        if simple_tool:

            # --------------------------------------------------
            # MULTIPLE DETERMINISTIC TOOLS
            # --------------------------------------------------

            if "tools" in simple_tool:

                tool_requests = (
                    simple_tool.get(
                        "tools",
                        []
                    )
                )

                if not isinstance(
                    tool_requests,
                    list
                ):
                    return (
                        "Invalid multi-tool request."
                    )

                results = []

                for tool_request in tool_requests:

                    if not isinstance(
                        tool_request,
                        dict
                    ):
                        continue

                    tool_name = (
                        tool_request.get(
                            "tool",
                            "unknown"
                        )
                    )

                    print(
                        f"\n[Tool requested: {tool_name}]"
                    )

                    result = (
                        self.execute_tool(
                            tool_request
                        )
                    )

                    print(
                        "[Tool execution completed]"
                    )

                    results.append(
                        str(result)
                    )

                if not results:
                    return (
                        "No valid tools were requested."
                    )

                return "\n".join(
                    results
                )

            # --------------------------------------------------
            # SINGLE DETERMINISTIC TOOL
            # --------------------------------------------------

            tool_name = (
                simple_tool.get(
                    "tool",
                    "unknown"
                )
            )

            print(
                f"\n[Tool requested: {tool_name}]"
            )

            result = (
                self.execute_tool(
                    simple_tool
                )
            )

            print(
                "[Tool execution completed]"
            )

            return result

        # ======================================================
        # ASK QWEN
        # ======================================================

        response = self.ask_model()

        # ======================================================
        # CHECK MODEL FAILURE
        # ======================================================

        if response.startswith(
            "LM Studio connection error:"
        ):
            return response

        if response.startswith(
            "Model error:"
        ):
            return response

        # ======================================================
        # PARSE TOOL REQUEST
        # ======================================================

        tool_data = (
            self.parse_tool(
                response
            )
        )

        # ======================================================
        # NORMAL ANSWER
        # ======================================================

        if not tool_data:

            self.messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )

            return response

        # ======================================================
        # STORE ASSISTANT REQUEST
        # ======================================================

        self.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        # ======================================================
        # MULTIPLE TOOLS
        # ======================================================

        if "tools" in tool_data:

            tool_requests = (
                tool_data.get(
                    "tools",
                    []
                )
            )

            if not isinstance(
                tool_requests,
                list
            ):
                return (
                    "Invalid multi-tool request."
                )

            results = []

            for tool_request in tool_requests:

                if not isinstance(
                    tool_request,
                    dict
                ):
                    continue

                tool_name = (
                    tool_request.get(
                        "tool",
                        "unknown"
                    )
                )

                print(
                    f"\n[Tool requested: {tool_name}]"
                )

                result = (
                    self.execute_tool(
                        tool_request
                    )
                )

                print(
                    "[Tool execution completed]"
                )

                results.append(
                    str(result)
                )

            if not results:
                return (
                    "No valid tools were requested."
                )

            return "\n".join(
                results
            )

        # ======================================================
        # SINGLE TOOL
        # ======================================================

        tool_name = (
            tool_data.get(
                "tool",
                "unknown"
            )
        )

        print(
            f"\n[Tool requested: {tool_name}]"
        )

        result = (
            self.execute_tool(
                tool_data
            )
        )

        print(
            "[Tool execution completed]"
        )

        # ======================================================
        # DIRECT RESULT TOOLS
        # ======================================================

        direct_result_tools = [
            "open_application",
            "close_application",
            "list_applications",
            "list_system_utilities",
            "create_file",
            "edit_file",
            "copy_file",
            "move_file",
            "rename_file",
            "delete_file",
            "list_files",
            "search_files",
            "read_file",
            "run_command"
        ]

        if tool_name in direct_result_tools:
            return result

        # ======================================================
        # FALLBACK FOR UNKNOWN / FUTURE TOOLS
        # ======================================================

        self.messages.append(
            {
                "role": "user",
                "content": (
                    "TOOL RESULT:\n"
                    + str(result)
                )
            }
        )

        return result

    # ==========================================================
    # MAIN LOOP
    # ==========================================================

    def run(self):

        print(
            "Model:",
            MODEL
        )

        print(
            "Backend: LM Studio (localhost:1234)"
        )

        print(
            "Type 'exit' or 'quit' to close."
        )

        print()

        while True:

            try:

                user_input = input(
                    "You: "
                ).strip()

            except KeyboardInterrupt:

                print(
                    "\nGoodbye!"
                )

                break

            if not user_input:
                continue

            if user_input.lower() in [
                "exit",
                "quit"
            ]:

                print(
                    "Goodbye!"
                )

                break

            response = (
                self.process(
                    user_input
                )
            )

            print(
                "\nNain:",
                response
            )

            print()