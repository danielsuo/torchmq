#!/usr/bin/env python3

# TODO (danielsuo): DELETEME
# NOTE: Assumes you have https://github.com/cli/cli

from pathlib import Path
import subprocess
import time

output = subprocess.run(["git", "pull", "--hard"])
branch = f"branch-{str(int(time.time()))}"
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
output = subprocess.run(["gh", "pr", "create", "--base", "main", "--title", branch, "--head", branch, "-f"])