"""Regenerate the open source contributions table in README.md.

Counts pull requests authored by the profile owner across every repository on
GitHub, groups them by repository and rewrites the block between the
OSS:START and OSS:END markers. New projects appear on their own, so the table
keeps up without being edited by hand.

A pull request counts as merged when GitHub says so, and also when its commits
were landed by hand. Some maintainers rebase a contribution onto the default
branch themselves and then close the pull request, which leaves merged_at unset
even though the work shipped; those are recovered by looking for the commit
subjects on the default branch.
"""

import json
import os
import re
import urllib.error
import urllib.request

USER = os.environ.get("OSS_USER", "Pranav-error")
TOKEN = os.environ.get("GITHUB_TOKEN")
README = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")
START, END = "<!-- OSS:START -->", "<!-- OSS:END -->"
MAX_ROWS = 10

# repo -> commit subjects on its default branch, filled in on first use.
_LANDED_CACHE = {}

# What the work in a repository actually was. Repositories without an entry
# fall back to their own GitHub description, so a new project still shows up.
NOTES = {
    "pgmoneta/pgmoneta": "Double frees, use-after-free, unchecked allocations, an off-by-one stack overflow, and a baseline-gated cppcheck CI job",
    "kubernetes/website": "Docs fixes, and a style guide section defining *deprecated* vs *no longer served* vs *removed* for APIs",
    "OSGeo/grass": "Null pointer dereference in the vector library, a null *function pointer* crash in `v.to.rast`, 64-bit cell counters, and unbounded environment growth in the runtime setup",
    "pgagroal/pgagroal": "Memory-safety fixes cross-ported at the lead maintainer's request",
    "pgexporter/pgexporter": "Memory-safety fixes cross-ported at the lead maintainer's request",
    "pgvictoria/pgvictoria": "Memory-safety fixes cross-ported at the lead maintainer's request",
    "fluxcd/source-controller": "Removed unsupported anonymous access for Azure buckets from the docs and code",
    "gnuradio/gnuradio": "QA test covering the real-time scheduling bindings",
    "Sakram-Arch/simulation": "Removed credentials that were committed to the repository, and fixed the migration integration tests",
}


def api(url):
    request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    if TOKEN:
        request.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def landed_subjects(repo):
    """Commit subjects authored by USER on the default branch of a repository."""
    if repo not in _LANDED_CACHE:
        subjects = set()
        try:
            result = api(
                "https://api.github.com/search/commits"
                f"?q=repo%3A{repo}+author%3A{USER}&per_page=100"
            )
            for item in result.get("items", []):
                message = (item.get("commit") or {}).get("message", "")
                subject = message.splitlines()[0].strip() if message else ""
                if subject:
                    subjects.add(subject)
        except (urllib.error.URLError, ValueError):
            # Leave the set empty rather than failing the run: the worst case is
            # the old behaviour, where a hand-landed pull request is not counted.
            pass
        _LANDED_CACHE[repo] = subjects
    return _LANDED_CACHE[repo]


def was_landed_by_hand(repo, number):
    """True when a closed, unmerged pull request's commits are on the default branch."""
    subjects = landed_subjects(repo)
    if not subjects:
        return False
    try:
        commits = api(f"https://api.github.com/repos/{repo}/pulls/{number}/commits?per_page=100")
    except (urllib.error.URLError, ValueError):
        return False
    for commit in commits:
        message = (commit.get("commit") or {}).get("message", "")
        subject = message.splitlines()[0].strip() if message else ""
        if subject and subject in subjects:
            return True
    return False


def collect():
    """Return {repo: {"merged": n, "open": n}} for every repo with a PR."""
    repos = {}
    page = 1
    while True:
        result = api(
            "https://api.github.com/search/issues"
            f"?q=author%3A{USER}+is%3Apr&per_page=100&page={page}"
        )
        items = result.get("items", [])
        for item in items:
            repo = item["repository_url"].split("/repos/", 1)[1]
            counts = repos.setdefault(repo, {"merged": 0, "open": 0})
            if (item.get("pull_request") or {}).get("merged_at"):
                counts["merged"] += 1
            elif item["state"] == "open":
                counts["open"] += 1
            elif was_landed_by_hand(repo, item["number"]):
                counts["merged"] += 1
        if len(items) < 100:
            break
        page += 1
    return repos


def describe(repo):
    if repo in NOTES:
        return NOTES[repo]
    try:
        return api(f"https://api.github.com/repos/{repo}").get("description") or ""
    except urllib.error.URLError:
        return ""


def status(counts):
    parts = []
    if counts["merged"]:
        parts.append(f"**{counts['merged']} merged**")
    if counts["open"]:
        parts.append(f"{counts['open']} open")
    return " · ".join(parts) or "—"


def build(repos):
    # Repositories with no merged and no open PRs are closed-only history.
    active = [(repo, c) for repo, c in repos.items() if c["merged"] or c["open"]]
    rows = [(repo, counts, describe(repo)) for repo, counts in active]
    # Rank by how much work went into a repository rather than merged count
    # alone, so a one-line drive-by does not outrank sustained work in
    # progress, and put repositories we can actually describe first.
    rows.sort(
        key=lambda row: (
            -(row[1]["merged"] + row[1]["open"]),
            0 if row[2] else 1,
            -row[1]["merged"],
            row[0].lower(),
        )
    )
    rows = rows[:MAX_ROWS]

    lines = [
        START,
        "",
        "<div align=\"center\">",
        "",
        "| Project | Contribution | Status |",
        "|:--|:--|:--|",
    ]
    for repo, counts, note in rows:
        lines.append(
            f"| **[{repo.split('/')[-1]}](https://github.com/{repo})** "
            f"| {note} | {status(counts)} |"
        )
    lines += ["", "</div>", "", END]
    return "\n".join(lines)


def main():
    with open(README, encoding="utf-8") as handle:
        readme = handle.read()
    if START not in readme or END not in readme:
        raise SystemExit("markers not found in README.md")
    updated = re.sub(
        re.escape(START) + r".*?" + re.escape(END),
        lambda _: build(collect()),
        readme,
        flags=re.DOTALL,
    )
    if updated != readme:
        with open(README, "w", encoding="utf-8") as handle:
            handle.write(updated)
        print("README.md updated")
    else:
        print("no change")


if __name__ == "__main__":
    main()
