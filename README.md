# `clangd-symlink-path-mappings.py`

usage: `clangd-symlink-path-mappings.py [-h] [-p] [-i [PATTERN ...]] [-e [PATTERN ...]] [path]`

Create path-mappings argument for Clangd by resolving symlinks. The provided path is walked recursively and encountered symlinks contribute to the mappings. Where possible, the mappings within a directory are replaced by a single mapping for the directory. This reduces the risk of the argument list for Clangd becoming too long.

positional arguments:

- `path` Defaults to `'.'`.

options:

- `-h`, `--help`
  show this help message and exit

- `-p`, `--pretty`
  Print one mapping per line without comma-separation.

- `-i`, `--include [PATTERN ...]`
  Symlinks to include. Symlink is included if source or target matches PATTERN. If no include pattern is given, all symlinks are included. See https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.full_match

- `-e`, `--exclude [PATTERN ...]`
  Symlinks to exclude. Symlink is excluded if source or target matches PATTERN. A matching exclude pattern overrules a matching include pattern. See https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.full_match
