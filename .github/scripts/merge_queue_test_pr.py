#!/usr/bin/env python3

# TODO (danielsuo): DELETEME
# NOTE: Assumes you have https://github.com/cli/cli

from pathlib import Path
import subprocess
import time

output = subprocess.run(["git", "pull", "--force"], check=True)
branch = f"branch-{str(int(time.time()))}"
output = subprocess.run(["git", "checkout", "-b", branch], check=True)

workdir = Path.resolve(Path(__file__)).parent.parent / "tmp"
Path.mkdir(workdir, exist_ok=True)

path = workdir / "blah"
with open(path, "w") as f:
    f.write(branch)

output = subprocess.run(["cat", path], check=True)
output = subprocess.run(["git", "add", "."], check=True)
output = subprocess.run(["git", "commit", "-am", f"Add branch {branch}."], check=True)
output = subprocess.run(["git", "push", "-u", "origin", branch], check=True)

output = subprocess.run(["git", "checkout", "main"], check=True)
output = subprocess.run(["gh", "pr", "create", "--base", "main", "--title", branch, "--head", branch, "-f"], check=True)