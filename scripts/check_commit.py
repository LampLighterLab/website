#!/usr/bin/env python3
"""Prepare staged portraits and reject oversized staged files. --check only validates."""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

MAX_FILE_BYTES = 1024 * 1024
PORTRAIT_DIR = "assets/images/people/"
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def git(*args):
    return subprocess.check_output(["git", *args])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate without modifying files")
    parser.add_argument("--all", action="store_true", help="Check every tracked file (for CI)")
    args = parser.parse_args()
    if args.all and not args.check:
        parser.error("--all requires --check")
    root = Path(git("rev-parse", "--show-toplevel").decode().strip())
    os.chdir(root)
    paths = git("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").decode().split("\0")
    entries = {}
    for entry in git("ls-files", "--stage", "-z").decode().split("\0"):
        if entry:
            metadata, name = entry.split("\t", 1)
            mode, oid, stage = metadata.split()
            if stage == "0" and mode in ("100644", "100755"):
                entries[name] = oid
    if args.all:
        paths = list(entries)
    errors, prepared = [], []
    for name in filter(None, paths):
        if name not in entries:
            continue
        oid = entries[name]
        size = int(git("cat-file", "-s", oid))
        path = Path(name)
        is_portrait = name.startswith(PORTRAIT_DIR) and path.suffix.lower() in EXTENSIONS
        if is_portrait:
            if not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*\.(?:jpg|jpeg|png|webp)", path.name):
                errors.append(f"{name}: use lowercase first_last.jpg (or .jpeg/.png/.webp).")
                continue
            try:
                from prepare_portraits import prepare
            except ImportError:
                errors.append("Portrait tooling missing. Run: sh scripts/setup-hooks.sh")
                break
            try:
                original = git("cat-file", "blob", oid)
                result = prepare(original, path.suffix)
                if result != original:
                    if args.check:
                        errors.append(f"{name}: needs preparation; run .venv/bin/python scripts/prepare_portraits.py {name}")
                    elif path.is_symlink() or not path.is_file() or path.read_bytes() != original:
                        errors.append(f"{name}: has unstaged changes; stage the complete photo before committing.")
                    else:
                        prepared.append((path, result))
                size = len(result)
            except (OSError, ValueError) as error:
                errors.append(f"{name}: cannot prepare portrait: {error}")
        if size > MAX_FILE_BYTES:
            errors.append(f"{name}: {size / 1024:.0f} KiB exceeds the 1 MiB limit. Compress it or link to an externally hosted file.")
    if errors:
        print("Commit checks failed:\n" + "\n".join(errors), file=sys.stderr)
        return 1
    for path, result in prepared:
        path.write_bytes(result)
        subprocess.run(["git", "add", "--", str(path)], check=True)
        print(f"Prepared and staged {path} ({len(result) / 1024:.0f} KiB).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
