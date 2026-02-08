#!/usr/bin/env python3

# SPDX-License-Identifier: MIT

import argparse
from   pathlib import Path
import sys
from   typing import List, Tuple


def walk(path : Path, include, exclude) -> Tuple[bool, List[Tuple[Path, Path]]]:
    if path.is_symlink():
        try:
            target = path.resolve(True)
        except OSError as e:
            print(f"ignoring broken symlink: {path} -> {path.readlink()} -- {e}", file=sys.stderr)
            return True, []

        m = (path, target)
        keep = True

        if include:
            keep &= any((x.full_match(pat) for x in m for pat in include))
        if exclude:
            keep &= not any((x.full_match(pat) for x in m for pat in exclude))

        if keep:
            return True, [(path, target)]
        else:
            return False, []

    elif path.is_dir():
        mappings = []
        all_same_target_parent = True
        target_parent = None
        for child in path.iterdir():
            match walk(child, include, exclude):
                case True, [(_, target)] as sub:
                    mappings += sub
                    if all_same_target_parent:
                        if target_parent:
                            all_same_target_parent &= target_parent == target.parent
                        else:
                            target_parent = target.parent
                case all_same, sub:
                    mappings += sub
                    all_same_target_parent &= all_same
                case x, y:
                    assert(False)
        if all_same_target_parent and target_parent:
            return True, [(path, target_parent)]
        else:
            # When target_parent is unset, mappings is implicitly empty.
            return all_same_target_parent, mappings

    else:
        return False, []


def getMappings(path: Path, include, exclude) -> List[Tuple[Path, Path]]:
    _, ret = walk(path, include, exclude)
    return ret


def output_pretty(mappings: List[Tuple[Path, Path]]) -> None:
    for (k, v) in mappings:
        print(f"{v}={k}")


def output(mappings: List[Tuple[Path, Path]]) -> None:
    comma = ""
    for k, v in mappings:
        print(f"{comma}{v}={k}", end="")
        comma = ","


def main() -> None:
    parser = argparse.ArgumentParser(
        description=
            "Create path-mappings argument for Clangd by resolving symlinks. "
            "The provided path is walked recursively and encountered symlinks "
            "contribute to the mappings. Where possible, the mappings within "
            "a directory are replaced by a single mapping for the directory. "
            "This reduces the risk of the argument list for Clangd becoming "
            "too long.")
    parser.add_argument('path', nargs='?', default=Path("."), type=Path, help=
        "Defaults to '.'.")
    parser.add_argument('-p', '--pretty', action='store_true', help=
        "Print one mapping per line without comma-separation.")
    parser.add_argument('-i', '--include', metavar="PATTERN", nargs='*', help=
        "Symlinks to include. "
        "Symlink is included if source or target matches PATTERN. "
        "If no include pattern is given, all symlinks are included. "
        "See https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.full_match")
    parser.add_argument('-e', '--exclude', metavar="PATTERN", nargs='*', help=
        "Symlinks to exclude. "
        "Symlink is excluded if source or target matches PATTERN. "
        "A matching exclude pattern overrules a matching include pattern. "
        "See https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.full_match")
    args = parser.parse_args()

    mappings = getMappings(args.path, args.include, args.exclude)

    if args.pretty:
        output_pretty(mappings)
    else:
        output(mappings)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        sys.exit(130)







