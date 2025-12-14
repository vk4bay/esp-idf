# Symbolic Links in ESP-IDF Repository

## Current Status

As of the latest check, **there are no symbolic links** in the ESP-IDF repository.

## How to List Symlinks

A utility script has been created to list all symbolic links in the repository:

```bash
python tools/list_symlinks.py
```

### Script Usage

The `list_symlinks.py` script provides several options:

```bash
# List all symlinks in the repository (relative paths)
python tools/list_symlinks.py

# List symlinks with absolute paths
python tools/list_symlinks.py --absolute

# Search a specific directory
python tools/list_symlinks.py --root /path/to/directory

# Exclude additional directories from search
python tools/list_symlinks.py --exclude build dist

# Show help
python tools/list_symlinks.py --help
```

### Default Exclusions

By default, the script excludes the following directories from the search:
- `.git` - Git repository metadata
- `build` - Build artifacts
- `dist` - Distribution files
- `__pycache__` - Python cache files
- `.pytest_cache` - Pytest cache files

### Output Format

When symlinks are found, the script outputs them in the format:

```
Found N symbolic link(s):

path/to/symlink -> target/path
```

## Manual Verification

You can also manually search for symlinks using command-line tools:

### Using find command:
```bash
find . -type l
```

### Using git:
```bash
# Git stores symlinks with mode 120000
git ls-files -s | grep '^120000'
```

### Using ls:
```bash
# In a specific directory, symlinks are shown with 'l' type
ls -la | grep '^l'
```

## Notes

- The ESP-IDF project currently does not use symbolic links in its source tree
- This may change in future versions of the repository
- If symlinks are added in the future, they can be detected using the provided script
