#!/usr/bin/env python3
"""
Script to format Python files in cookiecutter template directory using ruff.

The script temporarily replaces cookiecutter variables with valid Python identifiers,
runs ruff format, then restores the original variables.
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def find_python_files(template_dir: str) -> List[Path]:
    """Find all Python files in the template directory."""
    template_path = Path(template_dir)
    if not template_path.exists():
        raise FileNotFoundError(f"Template directory not found: {template_dir}")

    python_files = []
    for py_file in template_path.rglob("*.py"):
        python_files.append(py_file)

    return python_files


def create_replacement_map() -> Dict[str, str]:
    """Create mapping of cookiecutter variables to valid Python identifiers."""
    return {
        "{{ cookiecutter.package_name }}": "placeholder_package",
        "{{cookiecutter.package_name}}": "placeholder_package",  # Handle no spaces
    }


def backup_and_replace_variables(files: List[Path], replacement_map: Dict[str, str]) -> Dict[Path, str]:
    """
    Replace cookiecutter variables in files and return original content for restoration.

    Returns:
        Dictionary mapping file paths to their original content
    """
    original_content = {}

    for file_path in files:
        # Read original content
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Store original content
        original_content[file_path] = content

        # Replace variables
        modified_content = content
        for cookiecutter_var, replacement in replacement_map.items():
            modified_content = modified_content.replace(cookiecutter_var, replacement)

        # Write modified content if it changed
        if modified_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(modified_content)
            print(f"Temporarily replaced variables in: {file_path}")

    return original_content


def run_ruff_commands(python_files: List[Path]) -> bool:
    """Run ruff check and format on individual Python files to avoid parsing non-Python config files."""
    success = True

    try:
        # Test if ruff is available
        subprocess.run(["ruff", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ Ruff not found. Please install ruff: pip install ruff")
        return False

    # Define ruff rules to check
    ruff_rules = ["E", "W", "F", "I", "B", "UP"]
    rules_arg = ",".join(ruff_rules)

    # Step 1: Run ruff check --fix --unsafe-fixes
    print("Running ruff check --fix --unsafe-fixes...")
    check_success = True
    fixed_count = 0

    for file_path in python_files:
        try:
            result = subprocess.run(
                ["ruff", "check", "--fix", "--unsafe-fixes", "--select", rules_arg, "--isolated", str(file_path)],
                capture_output=True,
                text=True,
                check=False,  # Don't raise exception on non-zero exit (ruff check returns 1 if issues found)
            )

            if result.returncode == 0:
                print(f"✓ No issues found: {file_path}")
            elif result.returncode == 1:
                # Issues found and potentially fixed
                fixed_count += 1
                print(f"✓ Fixed issues: {file_path}")
                if result.stdout.strip():
                    print(f"  Details: {result.stdout.strip()}")
            else:
                # Actual error
                check_success = False
                print(f"✗ Failed to check {file_path}: {result.stderr.strip()}")

        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to check {file_path}: {e}")
            if e.stderr:
                print(f"  Error: {e.stderr.strip()}")
            check_success = False

    if check_success:
        print(f"✓ Ruff check completed ({fixed_count} files had fixes applied)")
    else:
        print("✗ Some files failed ruff check")
        success = False

    # Step 2: Run ruff format
    print("\nRunning ruff format...")
    format_success = True
    formatted_count = 0

    for file_path in python_files:
        try:
            result = subprocess.run(
                ["ruff", "format", "--isolated", str(file_path)], capture_output=True, text=True, check=True
            )
            formatted_count += 1
            print(f"✓ Formatted: {file_path}")

        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to format {file_path}: {e}")
            if e.stderr:
                print(f"  Error: {e.stderr.strip()}")
            format_success = False

    if format_success:
        print(f"✓ Successfully formatted {formatted_count} Python files")
    else:
        print(f"✗ Some files failed to format ({formatted_count} successful)")
        success = False

    return success


def restore_original_content(original_content: Dict[Path, str]) -> None:
    """Restore original content to all files."""
    for file_path, content in original_content.items():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Restored original content: {file_path}")


def apply_formatted_changes_with_cookiecutter_vars(
    python_files: List[Path],
    replacement_map: Dict[str, str],
    original_content: Dict[Path, str]
) -> None:
    """Apply the formatted changes but restore cookiecutter variables."""
    reverse_replacement_map = {v: k for k, v in replacement_map.items()}

    for file_path in python_files:
        # Read the currently formatted content (with placeholder variables)
        with open(file_path, "r", encoding="utf-8") as f:
            formatted_content = f.read()

        # Restore cookiecutter variables in the formatted content
        final_content = formatted_content
        for placeholder, cookiecutter_var in reverse_replacement_map.items():
            final_content = final_content.replace(placeholder, cookiecutter_var)

        # Only write if the content actually changed from original
        if final_content != original_content[file_path]:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(final_content)
            print(f"Applied formatting changes: {file_path}")
        else:
            # Still need to restore cookiecutter variables even if no other changes
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(final_content)
            print(f"Restored cookiecutter variables: {file_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Format cookiecutter template Python files")
    parser.add_argument(
        "--apply-changes",
        action="store_true",
        help="Apply formatting changes permanently (default: temporary)"
    )
    args = parser.parse_args()

    template_dir = "{{cookiecutter.project_slug}}"

    print(f"Formatting Python files in cookiecutter template: {template_dir}")
    if args.apply_changes:
        print("⚠️  Changes will be applied permanently!")
    else:
        print("ℹ️  Changes will be temporary (use --apply-changes to make permanent)")

    try:
        # Step 1: Find all Python files
        python_files = find_python_files(template_dir)
        print(f"Found {len(python_files)} Python files")

        if not python_files:
            print("No Python files found in template directory")
            return

        # Step 2: Create replacement mapping
        replacement_map = create_replacement_map()

        # Step 3: Backup and replace variables
        print("\nStep 1: Replacing cookiecutter variables with valid Python identifiers...")
        original_content = backup_and_replace_variables(python_files, replacement_map)

        try:
            # Step 4: Run ruff check and format
            print("\nStep 2: Running ruff check and format...")
            format_success = run_ruff_commands(python_files)

            if format_success:
                print("✓ All files checked and formatted successfully!")
            else:
                print("✗ Some operations failed")

        finally:
            if args.apply_changes:
                # Step 5a: Apply formatting changes permanently
                print("\nStep 3: Applying formatting changes with cookiecutter variables...")
                apply_formatted_changes_with_cookiecutter_vars(python_files, replacement_map, original_content)
                print("✓ Formatting changes applied permanently with cookiecutter variables!")
            else:
                # Step 5b: Restore original content (temporary mode)
                print("\nStep 3: Restoring original cookiecutter variables...")
                restore_original_content(original_content)
                print("✓ Original cookiecutter variables restored")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

