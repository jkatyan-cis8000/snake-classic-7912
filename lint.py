#!/usr/bin/env python3
"""
Linting tool for the Snake game project.
Enforces layer architecture and file structure rules.
"""

import os
import sys
import ast
from pathlib import Path

# Layer definitions and allowed imports
LAYERS = ['types', 'config', 'repo', 'service', 'runtime', 'ui', 'providers', 'utils']
LAYER_RULES = {
    'types': {'types'},
    'config': {'types', 'config'},
    'repo': {'types', 'config', 'repo'},
    'service': {'types', 'config', 'repo', 'providers', 'service'},
    'runtime': {'types', 'config', 'repo', 'service', 'providers', 'runtime'},
    'ui': {'types', 'config', 'service', 'runtime', 'providers', 'ui'},
    'providers': {'types', 'config', 'utils', 'providers'},
    'utils': {'utils'},
}

MAX_LINES = 300
SRC_DIR = Path('/workspace/snake-classic-7912/src')


def get_layer(filepath: Path) -> str | None:
    """Determine which layer a file belongs to."""
    rel_path = filepath.relative_to(SRC_DIR)
    parts = rel_path.parts
    if parts and parts[0] in LAYERS:
        return parts[0]
    return None


def get_imports(filepath: Path) -> list[str]:
    """Parse imports from a Python file."""
    imports = []
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
    except SyntaxError:
        pass
    return imports


def check_file(filepath: Path) -> list[str]:
    """Check a single file for violations."""
    errors = []
    
    # Rule 1: File must be in a layer directory
    layer = get_layer(filepath)
    if layer is None:
        errors.append(f"{filepath}: File is not in a layer directory")
        return errors
    
    # Check line count
    with open(filepath, 'r') as f:
        lines = f.readlines()
    if len(lines) > MAX_LINES:
        errors.append(f"{filepath}:{len(lines)}: File exceeds {MAX_LINES} lines ({len(lines)} lines)")
    
    # Check imports
    imports = get_imports(filepath)
    allowed = LAYER_RULES[layer]
    for imp in imports:
        # Get the top-level module name
        top_module = imp.split('.')[0]
        # Skip standard library modules
        if top_module not in allowed and top_module not in {'__future__', 'typing', 'enum', 'dataclasses', 'random', 'time', 'curses', 'os'}:
            errors.append(f"{filepath}: Import '{imp}' from disallowed layer '{top_module}'")
    
    return errors


def main():
    """Run lint checks on all Python files in src/."""
    all_errors = []
    
    # Find all Python files in src/
    for root, dirs, files in os.walk(SRC_DIR):
        for filename in files:
            if filename.endswith('.py'):
                filepath = Path(root) / filename
                errors = check_file(filepath)
                all_errors.extend(errors)
    
    # Report results
    if all_errors:
        print("Lint errors found:")
        for error in all_errors:
            print(f"  {error}")
        print(f"\n{len(all_errors)} error(s) found.")
        return 1
    else:
        print("No lint errors found.")
        return 0


if __name__ == '__main__':
    sys.exit(main())
