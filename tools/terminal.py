import subprocess


def run_command(command: str) -> str:
    print(f"\n[APPROVAL REQUIRED]")
    print(f"Jarvis wants to run:\n{command}")

    answer = input("Allow this command? [y/N]: ").strip().lower()
    if answer not in {"y", "yes"}:
        return "User denied execution of the command."

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,
        )

        output = result.stdout
        if result.stderr:
            output += "\nSTDERR:\n" + result.stderr

        if not output.strip():
            output = f"Command finished with exit code {result.returncode}."

        return output[:12000]
    except subprocess.TimeoutExpired:
        return "Command timed out after 60 seconds."
    except Exception as e:
        return f"Command failed: {e}"
