#!/usr/bin/env python3
"""Find a past commit made on this calendar date."""

import argparse
from datetime import date, datetime
from pathlib import Path
import random
import subprocess
import sys


FIELD_SEPARATOR = "\x1f"
COMMIT_LIMIT = 5000  # ponytail: scans the latest 5,000 commits; make depth configurable if large-history users need it


def terminal_safe(value):
    return "".join(
        char if char.isprintable() else char.encode("unicode_escape").decode("ascii")
        for char in value
    )


def read_commits(repository):
    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(repository),
                "log",
                "--all",
                f"-n{COMMIT_LIMIT}",
                "--format=%H%x1f%aI%x1f%s%x00",
            ],
            check=False,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError as error:
        raise RuntimeError("Git was not found. Install Git and try again.") from error
    except OSError as error:
        raise RuntimeError(f"Could not run Git: {error}") from error

    if result.returncode:
        detail = result.stderr.strip() or "Could not read Git history."
        raise RuntimeError(detail)

    commits = []
    for record in result.stdout.split("\0"):
        fields = record.strip("\r\n").split(FIELD_SEPARATOR, 2)
        if len(fields) != 3:
            continue
        sha, authored_at, subject = fields
        try:
            authored_date = datetime.fromisoformat(authored_at).date()
        except ValueError:
            continue
        commits.append((sha[:7], authored_date, subject))
    return commits


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Revisit a random commit made on this date in a previous year."
    )
    parser.add_argument("repository", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument(
        "--date",
        type=date.fromisoformat,
        default=date.today(),
        metavar="YYYY-MM-DD",
        help="look up a different calendar date",
    )
    args = parser.parse_args(argv)

    try:
        commits = read_commits(args.repository)
    except RuntimeError as error:
        print(f"git-rewind: {terminal_safe(str(error))}", file=sys.stderr)
        return 2

    if not commits:
        print("git-rewind: this repository has no commits yet.", file=sys.stderr)
        return 1

    anniversaries = [
        commit
        for commit in commits
        if commit[1].year < args.date.year
        and (commit[1].month, commit[1].day) == (args.date.month, args.date.day)
    ]
    if anniversaries:
        sha, authored_date, subject = random.choice(anniversaries)
        years = args.date.year - authored_date.year
        print(f"On this day, {years} year{'s' if years != 1 else ''} ago:")
    else:
        earlier_commits = [commit for commit in commits if commit[1] < args.date]
        if not earlier_commits:
            print("git-rewind: no commits before that date were found.", file=sys.stderr)
            return 1
        sha, authored_date, subject = random.choice(earlier_commits)
        print("No anniversary found; here's a random earlier commit:")

    print(
        f"{authored_date.isoformat()}  {sha}  "
        f"{terminal_safe(subject or '(no commit message)')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
