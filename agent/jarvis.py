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
            re.DOTALL
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
            r'\{.*?"tools"\s*:\s*\[.*?\].*\}',
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
    # DETERMINISTIC SIMPLE TOOL ROUTER
    # ==========================================================
    def detect_simple_tool(self, user_input):
        text = user_input.strip().lower()

        # ============================================================
        # SYSTEM UTILITIES
        # ============================================================

        system_utility_phrases = [
            "list system utilities",
            "show system utilities",
            "what system utilities are available",
            "what windows utilities are available",
            "show me windows utilities",
            "list windows utilities",
            "show system tools",
            "what system tools are available",
            "what system tools can you open",
        ]

        if any(phrase in text for phrase in system_utility_phrases):
            return {
                "tool": "list_system_utilities",
                "arguments": {}
            }

        # ============================================================
        # APPLICATION LISTING
        # ============================================================

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
            "which applications are available",
        ]

        if any(phrase in text for phrase in application_list_phrases):
            return {
                "tool": "list_applications",
                "arguments": {}
            }

        # ============================================================
        # OPEN APPLICATION
        # ============================================================

        open_phrases = [
            "open ",
            "launch ",
            "start ",
            "run "
        ]

        if any(text.startswith(phrase) for phrase in open_phrases):
            for phrase in open_phrases:
                if text.startswith(phrase):
                    app_name = text[len(phrase):].strip()
                    break

            if app_name:
                return {
                    "tool": "open_application",
                    "arguments": {
                        "name": app_name
                    }
                }

        # ============================================================
        # CLOSE APPLICATION
        # ============================================================

        close_phrases = [
            "close ",
            "exit ",
            "quit "
        ]

        if any(text.startswith(phrase) for phrase in close_phrases):
            for phrase in close_phrases:
                if text.startswith(phrase):
                    app_name = text[len(phrase):].strip()
                    break

            if app_name:
                return {
                    "tool": "close_application",
                    "arguments": {
                        "name": app_name
                    }
                }

        return None

    # ==========================================================
    # PROCESS USER REQUEST
    # ==========================================================

    def process(self, user_input):

        self.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        # ------------------------------------------------------
        # DETERMINISTIC SIMPLE TOOL ROUTING
        # ------------------------------------------------------

        simple_tool = self.detect_simple_tool(
            user_input
        )

        if simple_tool:

            tool_name = simple_tool.get(
                "tool",
                "unknown"
            )

            print(
                f"\n[Tool requested: {tool_name}]"
            )

            result = self.execute_tool(
                simple_tool
            )

            print(
                "[Tool execution completed]"
            )

            return result

        # ------------------------------------------------------
        # ASK QWEN
        # ------------------------------------------------------

        response = self.ask_model()

        # ------------------------------------------------------
        # CHECK IF MODEL FAILED
        # ------------------------------------------------------

        if response.startswith(
            "LM Studio connection error:"
        ):

            return response

        if response.startswith(
            "Model error:"
        ):

            return response

        # ------------------------------------------------------
        # PARSE TOOL REQUEST
        # ------------------------------------------------------

        tool_data = self.parse_tool(
            response
        )

        # ------------------------------------------------------
        # NORMAL ANSWER
        # ------------------------------------------------------

        if not tool_data:

            self.messages.append(
                {
                    "role": "assistant",
                    "content": response
                }
            )

            return response

        # ------------------------------------------------------
        # STORE ASSISTANT REQUEST
        # ------------------------------------------------------

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

            tool_requests = tool_data.get(
                "tools",
                []
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

                tool_name = tool_request.get(
                    "tool",
                    "unknown"
                )

                print(
                    f"\n[Tool requested: {tool_name}]"
                )

                result = self.execute_tool(
                    tool_request
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

        tool_name = tool_data.get(
            "tool",
            "unknown"
        )

        print(
            f"\n[Tool requested: {tool_name}]"
        )

        # ------------------------------------------------------
        # Execute tool
        # ------------------------------------------------------

        result = self.execute_tool(
            tool_data
        )

        # ------------------------------------------------------
        # Display tool completion
        # ------------------------------------------------------

        print(
            "[Tool execution completed]"
        )

        # ------------------------------------------------------
        # Direct result tools
        # ------------------------------------------------------

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

        # ------------------------------------------------------
        # Fallback for unknown/future tools
        # ------------------------------------------------------

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

            response = self.process(
                user_input
            )

            print(
                "\nNain:",
                response
            )

            print()