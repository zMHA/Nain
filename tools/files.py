# ============================================================
# SECTION 1 — IMPORTS
# ============================================================

from pathlib import Path
import shutil


# ============================================================
# SECTION 2 — LIST FILES
# ============================================================

def list_files(path):
    p = Path(path).expanduser()

    if not p.exists():
        return f"Path does not exist: {p}"

    if not p.is_dir():
        return f"Not a directory: {p}"

    items = []

    for item in sorted(p.iterdir()):
        item_type = "[DIR]" if item.is_dir() else "[FILE]"
        items.append(f"{item_type} {item.name}")

    return "\n".join(items) if items else "Directory is empty."


# ============================================================
# SECTION 3 — READ FILE
# ============================================================

def read_file(path):
    p = Path(path).expanduser()

    if not p.exists():
        return f"File does not exist: {p}"

    if not p.is_file():
        return f"Not a file: {p}"

    try:
        return p.read_text(encoding="utf-8")[:12000]
    except Exception as e:
        return f"Could not read file: {e}"


# ============================================================
# SECTION 4 — CREATE FILE
# ============================================================

def create_file(path, content):
    p = Path(path).expanduser()

    if p.exists():
        return f"File already exists: {p}"

    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"File created successfully: {p}"
    except Exception as e:
        return f"Could not create file: {e}"


# ============================================================
# SECTION 5 — EDIT FILE
# ============================================================

def edit_file(path, content):
    p = Path(path).expanduser()

    if not p.exists():
        return f"File does not exist: {p}"

    if not p.is_file():
        return f"Not a file: {p}"

    try:
        p.write_text(content, encoding="utf-8")
        return f"File updated successfully: {p}"
    except Exception as e:
        return f"Could not edit file: {e}"


# ============================================================
# SECTION 6 — SEARCH FILES
# ============================================================

def search_files(path, pattern, recursive=True):
    root = Path(path).expanduser()

    if not root.exists():
        return f"Path does not exist: {root}"

    if not root.is_dir():
        return f"Not a directory: {root}"

    try:
        if recursive:
            results = list(root.rglob(pattern))
        else:
            results = list(root.glob(pattern))

        # Only files, not directories
        results = [
            item for item in results
            if item.is_file()
        ]

        if not results:
            return f"No files found matching: {pattern}"

        output = []

        for item in results[:200]:
            output.append(f"[FILE] {item}")

        if len(results) > 200:
            output.append("\n...showing first 200 results.")

        return "\n".join(output)

    except Exception as e:
        return f"Search failed: {e}"


# ============================================================
# SECTION 7 — COPY FILE
# ============================================================

def copy_file(source, destination):
    src = Path(source).expanduser()
    dst = Path(destination).expanduser()

    if not src.exists():
        return f"Source does not exist: {src}"

    try:
        dst.parent.mkdir(parents=True, exist_ok=True)

        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)

        return f"Copied successfully:\n{src}\n→ {dst}"

    except Exception as e:
        return f"Copy failed: {e}"


# ============================================================
# SECTION 8 — MOVE FILE
# ============================================================

def move_file(source, destination):
    src = Path(source).expanduser()
    dst = Path(destination).expanduser()

    if not src.exists():
        return f"Source does not exist: {src}"

    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))

        return f"Moved successfully:\n{src}\n→ {dst}"

    except Exception as e:
        return f"Move failed: {e}"


# ============================================================
# SECTION 9 — RENAME FILE
# ============================================================

def rename_file(path, new_name):
    src = Path(path).expanduser()

    if not src.exists():
        return f"File or folder does not exist: {src}"

    try:
        destination = src.parent / new_name
        src.rename(destination)

        return f"Renamed successfully:\n{src.name} → {destination.name}"

    except Exception as e:
        return f"Rename failed: {e}"


# ============================================================
# SECTION 10 — DELETE FILE
# ============================================================

def delete_file(path):
    target = Path(path).expanduser()

    if not target.exists():
        return f"File or folder does not exist: {target}"

    print("\n[DELETE CONFIRMATION]")
    print("Jarvis wants to delete:")
    print(target)

    answer = input("Are you sure? [y/N]: ").strip().lower()

    if answer != "y":
        return "Delete cancelled by user."

    try:
        if target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()

        return f"Deleted successfully: {target}"

    except Exception as e:
        return f"Delete failed: {e}"