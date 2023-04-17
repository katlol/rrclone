import os
import re
from typing import Union

RRCLONE_CONFIG = os.getenv("RRCLONE_CONFIG", "/rrclone-in/rclone.conf")
RRCLONE_OUT = os.getenv("RRCLONE_OUT", "/rrclone-out/rrclone")
RRCLONE_REGEX = os.getenv("RRCLONE_REGEX", "^\[([^\]]+)\]$")


def get_remotes() -> list:
    remotes = []
    with open(RRCLONE_CONFIG) as f:
        for line in f.read().splitlines():
            if match := re.match(RRCLONE_REGEX, line):
                remotes.append(match.group(1))
    return remotes


def current_remote() -> str:
    if not os.path.exists(RRCLONE_OUT):
        return None

    with open(RRCLONE_OUT) as f:
        return f.read()


def _candidate(remotes: list, current: Union[str, None]) -> str:
    if not current:
        return remotes[0]

    try:
        idx = remotes.index(current)
    except ValueError:
        return remotes[0]

    try:
        return remotes[idx + 1]
    except IndexError:
        return remotes[0]


def commit(candidate: str) -> None:
    with open(RRCLONE_OUT, "w") as f:
        f.write(candidate)


def xprint(sugar: str, variable: any = None):
    print(sugar)
    if variable:
        print(variable)
    print("----")


def run():
    remotes = get_remotes()
    xprint("Found remotes", remotes)

    current = current_remote()
    xprint("Current remote", "None" if not current else current)

    candidate = _candidate(remotes, current)
    xprint("Candidate", candidate)

    commit(candidate)
    xprint("Commit")


if __name__ == "__main__":
    run()
