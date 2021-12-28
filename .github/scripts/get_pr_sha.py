#!/usr/bin/env python3

import argparse
import json
import urllib.request


def main():
    parser = argparse.ArgumentParser(description="Get SHA of PR from GitHub.")
    parser.add_argument("repo", type=str, help="repo name")
    parser.add_argument("num", type=int, help="pr number")
    parser.add_argument("sha_path", type=str, default="/tmp/sha", help="where to write sha")

    args = parser.parse_args()

    print(args)

    url = f"https://api.github.com/repos/{args.repo}/pulls/{args.num}"
    print(url)
    with urllib.request.urlopen(url) as response:
        sha = json.loads(response.read().decode())["head"]["sha"]

    with open(args.sha_path, "w", encoding="UTF-8") as f:
        f.write(sha)


if __name__ == "__main__":
    main()
