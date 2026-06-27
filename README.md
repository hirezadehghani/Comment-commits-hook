# Comment-commits-hook

Automatically adds an RD-&lt;branch-name> (you can edit RD with any other thing) comment to your source files before each commit.

## Features

* Adds an `RD-<branch-name>` comment before the first modified block in a file.
* Adds the comment to the end of newly created files.
* Supports multiple programming languages.
* Prevents duplicate comments in the same file.
* Supports Laravel Blade comments (`{{-- --}}`).
* Ignores configurable files and directories.
* Works as a Git `pre-commit` hook.

## Supported Comment Styles

| File Type                | Comment Style         |
| ------------------------ | --------------------- |
| PHP                      | `// RD-branch`        |
| Blade                    | `{{-- RD-branch --}}` |
| JavaScript / TypeScript  | `// RD-branch`        |
| Java / C / C++ / C# / Go | `// RD-branch`        |
| Python / Shell / Ruby    | `# RD-branch`         |
| CSS                      | `/* RD-branch */`     |
| HTML                     | `<!-- RD-branch -->`  |

## Installation

Clone the repository:

```bash
git clone https://github.com/<username>/<repository>.git
cd <repository>
```

Configure Git to use the provided hooks:

```bash
git config core.hooksPath githooks
```

Make the hook executable (Linux/macOS):

```bash
chmod +x githooks/pre-commit
```

No additional Python packages are required.

## Project Structure

```text
.
├── githooks/
│   └── pre-commit
├── scripts/
│   └── add_rd_comment.py
└── README.md
```

## How It Works

Before every commit:

1. Detects the current Git branch.
2. Finds all staged files.
3. Ignores configured files and directories.
4. Detects the appropriate comment syntax.
5. Inserts an `RD-<branch-name>` comment:

   * Before the first modified block in an existing file.
   * At the end of a newly created file.
6. Re-stages the modified files automatically.

## Ignored Files

Configure ignored files by editing the `IGNORE_PATTERNS` list inside `scripts/add_rd_comment.py`.

Example:

```python
IGNORE_PATTERNS = [
    "composer.json",
    "composer.lock",
    "package.json",
    "package-lock.json",
]
```

Directories can be ignored using `IGNORE_DIRS`.

## Example

Branch:

```text
feature/payment
```

Generated comment:

```php
// RD-feature/payment
```

Blade:

```blade
{{-- RD-feature/payment --}}
```

Python:

```python
# RD-feature/payment
```
## Change fixed string
For this purpose you can just change the add_rd_comment.py file.

## Requirements

* Git
* Python 3.8+

## Limitations

* Only processes staged files.
* The inserted comment becomes part of the commit.
* Binary files are ignored.
* This tool is intended for source files only.

## License

MIT
