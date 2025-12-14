#!/usr/bin/env python
# SPDX-FileCopyrightText: 2025 Espressif Systems (Shanghai) CO LTD
# SPDX-License-Identifier: Apache-2.0
"""
Script to list all symbolic links in the ESP-IDF repository.

This script searches for all symbolic links in the repository and displays
them along with their targets.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Tuple


def find_symlinks(root_path: Path, exclude_dirs: List[str] = None) -> List[Tuple[Path, Path]]:
    """
    Find all symbolic links in the given directory tree.

    Args:
        root_path: Root directory to search
        exclude_dirs: List of directory names to exclude from search

    Returns:
        List of tuples containing (symlink_path, target_path)
    """
    if exclude_dirs is None:
        exclude_dirs = ['.git', 'build', 'dist', '__pycache__', '.pytest_cache']

    symlinks = []

    for dirpath, dirnames, filenames in os.walk(root_path, followlinks=False):
        # Remove excluded directories from the search
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

        # Check directories for symlinks
        for dirname in dirnames:
            full_path = Path(dirpath) / dirname
            if full_path.is_symlink():
                target = full_path.readlink()
                symlinks.append((full_path, target))

        # Check files for symlinks
        for filename in filenames:
            full_path = Path(dirpath) / filename
            if full_path.is_symlink():
                target = full_path.readlink()
                symlinks.append((full_path, target))

    return symlinks


def print_symlinks(symlinks: List[Tuple[Path, Path]], root_path: Path, show_absolute: bool = False) -> None:
    """
    Print the list of symbolic links.

    Args:
        symlinks: List of (symlink, target) tuples
        root_path: Root path for relative path calculation
        show_absolute: If True, show absolute paths; otherwise show relative paths
    """
    if not symlinks:
        print('No symbolic links found in the repository.')
        return

    print(f'Found {len(symlinks)} symbolic link(s):\n')

    # Sort by path for consistent output
    symlinks.sort(key=lambda x: str(x[0]))

    for link, target in symlinks:
        if show_absolute:
            link_display = str(link)
        else:
            try:
                link_display = str(link.relative_to(root_path))
            except ValueError:
                link_display = str(link)

        print(f'{link_display} -> {target}')


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='List all symbolic links in the ESP-IDF repository'
    )
    parser.add_argument(
        '--root',
        type=str,
        default=None,
        help='Root directory to search (default: ESP-IDF repository root)'
    )
    parser.add_argument(
        '--absolute',
        action='store_true',
        help='Show absolute paths instead of relative paths'
    )
    parser.add_argument(
        '--exclude',
        type=str,
        nargs='+',
        default=None,
        help='Additional directories to exclude from search'
    )

    args = parser.parse_args()

    # Determine root path
    if args.root:
        root_path = Path(args.root).resolve()
    else:
        # Try to find ESP-IDF root by looking for characteristic files
        script_path = Path(__file__).resolve()
        root_path = script_path.parent.parent

    if not root_path.exists():
        print(f'Error: Root path does not exist: {root_path}', file=sys.stderr)
        return 1

    # Set up exclusions
    exclude_dirs = ['.git', 'build', 'dist', '__pycache__', '.pytest_cache']
    if args.exclude:
        exclude_dirs.extend(args.exclude)

    # Find and print symlinks
    symlinks = find_symlinks(root_path, exclude_dirs)
    print_symlinks(symlinks, root_path, args.absolute)

    return 0


if __name__ == '__main__':
    sys.exit(main())
