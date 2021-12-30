#!/usr/bin/env python3

import argparse
import json
import os
import requests
import subprocess


GH_GQL_API = "https://api.github.com/graphql"


# TODO: would be great to just get commit conclusion from hash.
# Current mechanism for doing this is bad because we take the entire
# commit history of mq. The consequence is that we have to filter
# and do a bunch of checks. No bueno.
def query_gh_gql(path, token, owner, name):
    # NOTE: building the query can be done in much better ways
    with open(path, "r", encoding="UTF-8") as f:
        gql = f.read()
        gql = gql.replace("{owner}", f'"{owner}"')
        gql = gql.replace("{name}", f'"{name}"')

    response = requests.post(
        GH_GQL_API, json={"query": gql}, headers={"Authorization": f"Bearer {token}"}
    )

    # TODO: check r.status_code is 200
    data = json.loads(response.text)
    history = data["data"]["repository"]["ref"]["target"]["history"]["nodes"]

    result = {}
    # Error checking/filtering
    for commit in history:
        oid = commit["oid"]
        checkSuites = commit["checkSuites"]["nodes"]
        if len(checkSuites) == 0:
            continue
        checkRuns = checkSuites[0]["checkRuns"]["nodes"]
        if len(checkRuns) == 0:
            continue
        conclusion = checkRuns[0]["conclusion"]
        result[oid] = conclusion
    return result


def main():
    parser = argparse.ArgumentParser(description="Collect runs")
    parser.add_argument("token", type=str)
    parser.add_argument("--repo", type=str, default="danielsuo/torchmq", help="repo name")

    args = parser.parse_args()

    owner, name = args.repo.split("/")
    conclusions = query_gh_gql(
        os.path.join(os.path.dirname(__file__), "get_mq_status.gql"),
        args.token,
        owner,
        name,
    )

    output = subprocess.run(["git", "rev-list", "main..mq"], capture_output=True)
    revs = output.stdout.decode("ascii").split()
    revs.reverse()

    for rev in revs:
        print(rev)

if __name__ == "__main__":
    main()
