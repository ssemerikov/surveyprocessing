#!/usr/bin/env python3
"""
Code structure verification without requiring dependencies.
Verifies Python syntax and code organization.
"""

import ast
import os
from pathlib import Path


def verify_python_file(file_path):
    """Verify Python file syntax and structure."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()

        # Parse AST
        tree = ast.parse(code, filename=file_path)

        # Count elements
        classes = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
        functions = sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
        imports = sum(1 for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom)))

        return {
            'valid': True,
            'classes': classes,
            'functions': functions,
            'imports': imports,
            'lines': len(code.splitlines())
        }
    except SyntaxError as e:
        return {
            'valid': False,
            'error': f"Syntax error at line {e.lineno}: {e.msg}"
        }
    except Exception as e:
        return {
            'valid': False,
            'error': str(e)
        }


def main():
    """Verify all Python files."""
    print("=" * 80)
    print("CODE STRUCTURE VERIFICATION")
    print("=" * 80)

    src_dir = Path("src")
    test_dir = Path("tests")

    total_files = 0
    valid_files = 0
    total_classes = 0
    total_functions = 0
    total_lines = 0

    print("\nVerifying Source Code...")
    print("-" * 80)

    for py_file in sorted(src_dir.rglob("*.py")):
        result = verify_python_file(py_file)
        total_files += 1

        status = "✓" if result['valid'] else "✗"
        rel_path = str(py_file.relative_to(src_dir))

        if result['valid']:
            valid_files += 1
            total_classes += result['classes']
            total_functions += result['functions']
            total_lines += result['lines']
            print(f"  {status} {rel_path:<40} "
                  f"{result['classes']:>2} classes, "
                  f"{result['functions']:>3} functions, "
                  f"{result['lines']:>4} lines")
        else:
            print(f"  {status} {rel_path:<40} ERROR: {result['error']}")

    print("\nVerifying Tests...")
    print("-" * 80)

    test_files = 0
    valid_tests = 0

    for py_file in sorted(test_dir.rglob("*.py")):
        if py_file.name == "__pycache__":
            continue

        result = verify_python_file(py_file)
        test_files += 1

        status = "✓" if result['valid'] else "✗"
        rel_path = str(py_file.relative_to(test_dir))

        if result['valid']:
            valid_tests += 1
            # Count test functions
            with open(py_file, 'r') as f:
                code = f.read()
            test_count = code.count("def test_")
            print(f"  {status} {rel_path:<40} {test_count:>2} tests, {result['lines']:>4} lines")
        else:
            print(f"  {status} {rel_path:<40} ERROR: {result['error']}")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"\nSource Code:")
    print(f"  Total files:      {total_files}")
    print(f"  Valid files:      {valid_files}")
    print(f"  Total classes:    {total_classes}")
    print(f"  Total functions:  {total_functions}")
    print(f"  Total lines:      {total_lines:,}")

    print(f"\nTest Code:")
    print(f"  Test files:       {test_files}")
    print(f"  Valid files:      {valid_tests}")

    if valid_files == total_files and valid_tests == test_files:
        print("\n✓ ALL FILES HAVE VALID PYTHON SYNTAX!")
        return 0
    else:
        print(f"\n✗ {total_files + test_files - valid_files - valid_tests} FILES HAVE ERRORS")
        return 1


if __name__ == '__main__':
    exit(main())
