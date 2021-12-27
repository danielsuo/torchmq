#!/usr/bin/env python3

# TODO (danielsuo): DELETEME

from pathlib import Path
import subprocess
import time

branch = f"{str(int(time.time()))}\n"
output = subprocess.run(["git", "checkout", "-b", branch])

workdir = Path.resolve(Path(__file__)).parent.parent / "tmp"
Path.mkdir(workdir, exist_ok=True)

path = workdir / "blah"
with open(path, "w") as f:
    f.write(branch)

output = subprocess.run(["cat", path])
output = subprocess.run(["git", "add", "."])
output = subprocess.run(["git", "commit", "-am", f"Add branch {branch}."])
output = subprocess.run(["git", "push", "-u", "origin", branch])

output = subprocess.run(["git", "checkout", "main"])