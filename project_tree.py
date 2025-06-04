import os
import argparse

# Define ignored files/folders
IGNORED_NAMES = {'.git', 'node_modules','__pycache__', '.DS_Store', '.idea', '.vscode', '.mypy_cache'}

def list_hierarchy(startpath, indent='', level=0, max_level=None):
    if max_level is not None and level > max_level:
        return

    try:
        items = sorted(
            [item for item in os.listdir(startpath) if item not in IGNORED_NAMES and not item.startswith('.')]
        )
    except PermissionError:
        return

    for i, item in enumerate(items):
        path = os.path.join(startpath, item)
        prefix = '└── ' if i == len(items) - 1 else '├── '
        print(indent + prefix + item)
        if os.path.isdir(path):
            extension = '    ' if i == len(items) - 1 else '│   '
            list_hierarchy(path, indent + extension, level + 1, max_level)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List project hierarchy up to a certain depth, ignoring system/hidden files.")
    parser.add_argument("path", nargs="?", default=".", help="Root path of the project (default is current directory).")
    parser.add_argument("--levels", type=int, help="Maximum number of levels to display (default: no limit).")

    args = parser.parse_args()

    project_root = os.path.abspath(args.path)
    print(os.path.basename(project_root))
    list_hierarchy(project_root, level=0, max_level=args.levels)
