import subprocess
import re
import os
from fnmatch import fnmatch

# -----------------------------
# CONFIG
# -----------------------------
IGNORE_DIRS = [
    "vendor/",
    "node_modules/",
    ".git/",
    "scripts/",
    "githooks/"
    ]

COMMENT_MAP = {
    ".py": "# {}",
    ".php": "// {}",
    ".js": "// {}",
    ".ts": "// {}",
    ".java": "// {}",
    ".c": "// {}",
    ".cpp": "// {}",
    ".cs": "// {}",
    ".go": "// {}",
    ".rb": "# {}",
    ".sh": "# {}",
    ".css": "/* {} */",
    ".html": "<!-- {} -->",
}

IGNORE_PATTERNS = [
    "composer.json",
    "composer.lock",
    "package.json",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "*.min.js",
    "*.min.css",
    "*.svg",
    "*.png",
    "*.jpg",
    "*.jpeg",
    "*.gif",
    "*.pdf",
]

BLADE_COMMENT = "{{-- {} --}}"

# -----------------------------
# HELPERS
# -----------------------------
def run(cmd):
    return subprocess.check_output(cmd, text=True, errors="ignore")


def get_branch():
    return run(["git", "branch", "--show-current"]).strip()


def staged_files():
    return run(["git", "diff", "--cached", "--name-status"]).splitlines()


def is_ignored(file):
    return any(file.startswith(d) for d in IGNORE_DIRS)

def is_ignored_file(file):
    filename = os.path.basename(file)
    for pattern in IGNORE_PATTERNS:
        if fnmatch(filename, pattern):
            return True
    return False

def has_marker(content):
    return bool(re.search(r"RD-[\w/-]+", content))


def get_comment(file, marker):
    if file.endswith(".blade.php"):
        return f"{{-- {marker} --}}"
    
    if file.endswith("composer.json"):
        return;

    for ext, fmt in COMMENT_MAP.items():
        if file.endswith(ext):
            return fmt.format(marker)

    # fallback safe
    return f"// {marker}"


# -----------------------------
# EXTRACT ALL HUNKS START LINES
# -----------------------------
def get_changed_blocks(file):
    diff = run(["git", "diff", "--cached", "--unified=0", file])

    blocks = []
    current_start = None

    for line in diff.splitlines():
        match = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)", line)
        if match:
            current_start = int(match.group(1))
            blocks.append(current_start)

    return blocks


# -----------------------------
# MAIN
# -----------------------------
def main():
    branch = get_branch()
    marker = f"RD-{branch}"

    files = staged_files()

    for entry in files:
        parts = entry.split("\t")
        status = parts[0]
        file = parts[1]

        if is_ignored(file) or not os.path.exists(file) or is_ignored_file(file):
            continue

        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        content = "".join(lines)

        if has_marker(content):
            continue

        comment = get_comment(file, marker)

        # -----------------------------
        # NEW FILE -> append comment to the end of the file
        # -----------------------------
        if status == "A":
        # Ensure the file ends with a newline
            if lines and not lines[-1].endswith("\n"):
                lines[-1] += "\n"

            if lines:
                lines.append("\n")

            lines.append(comment + "\n")

        # -----------------------------
        # MODIFIED FILE
        # -----------------------------
        else:
            blocks = get_changed_blocks(file)

            offset = 0

            for start in blocks:
                idx = max(start - 1 + offset, 0)

                # If the comment would be inserted at the beginning of the file,
                # append it to the end instead.
                if idx == 0:
                    if lines and not lines[-1].endswith("\n"):
                        lines[-1] += "\n"

                    if lines:
                        lines.append("\n")

                    lines.append(comment + "\n")
                else:
                    lines.insert(idx, comment + "\n")
                    offset += 1

        with open(file, "w", encoding="utf-8") as f:
            f.writelines(lines)

        subprocess.run(["git", "add", file])


if __name__ == "__main__":
    main()