"""Regenerate the open source contributions table in README.md.

Counts pull requests authored by the profile owner across every repository on
GitHub, groups them by repository and rewrites the block between the
OSS:START and OSS:END markers. New projects appear on their own, so the table
keeps up without being edited by hand.

"Merged" is counted as commits GitHub attributes to this account on a repo's
default branch (GET /repos/{repo}/commits?author=USER) — not PR merge status.
Several maintainers (pgmoneta, pgagroal, ...) apply patches by hand (rebase,
cherry-pick, git am) and close the PR without using the merge button, so a PR
search undercounts real landed work; the commit itself is the ground truth
regardless of how it got there. This matches what GitHub's own contribution
graph shows for that repo.

Verified 2026-10-08: the previous approach here (matching a PR's own commits
against a `search/commits?q=repo:X+author:Y` listing) silently missed 26 of
pgmoneta's merged patches after a maintainer merge wave — that search
endpoint doesn't reliably resolve hand-landed/rebased commits back to the
author, while the direct `?author=` commits endpoint does. Don't revert to
PR-search-based "merged" counting without re-verifying against this endpoint.

Run this from the workflow, not by hand. The search API returns whatever the
token can see, so a personal token pulls in private repositories and writes
their names into a public README. The workflow token only sees public ones.
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request

USER = os.environ.get("OSS_USER", "Pranav-error")
TOKEN = os.environ.get("GITHUB_TOKEN")
README = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")
START, END = "<!-- OSS:START -->", "<!-- OSS:END -->"
MAX_ROWS = 10

# Own repos and friends'/internship repos aren't "contributions to open source" even
# when they have real merged commits counted the same reliable way.
EXCLUDE = {
    "Sakram-Arch/simulation",
    "Patel-Muhammad/name-pr",
    "PritamP20/HackSprint",
    "DotDev-Club/DotDev",
    "chiraghontec/qnit-customer-discovery",
}
EXCLUDE_OWNERS = {USER, "Site-Analysis"}

# What the work in a repository actually was. Repositories without an entry
# fall back to their own GitHub description, so a new project still shows up.
NOTES = {
    "pgmoneta/pgmoneta": "Double frees, use-after-free, unchecked allocations, an off-by-one stack overflow, error-path null dereferences, and corner-case tests for the core string helpers",
    "kubernetes/website": "Docs fixes, and a style guide section defining *deprecated* vs *no longer served* vs *removed* for APIs",
    "OSGeo/grass": "Null pointer dereference in the vector library, a null *function pointer* crash in `v.to.rast`, 64-bit cell counters, and unbounded environment growth in the runtime setup",
    "pgagroal/pgagroal": "An unbounded `strcat` stack overflow in the CLI, unchecked reallocs, and silent truncation in the numeric append helpers — found by writing the corner-case tests",
    "pgexporter/pgexporter": "Unchecked allocations in the YAML and network paths, plus a kqueue accept-drain fix ported from pgagroal",
    "pgvictoria/pgvictoria": "Cross-ported allocation checks and string-helper fixes, with corner-case tests for the append family",
    "fluxcd/source-controller": "Removed unsupported anonymous access for Azure buckets from the docs and code",
    "fluxcd/flux2": "Removed dead fields from the install flags",
    "gnuradio/gnuradio": "QA test for the real-time scheduling bindings, and float-tolerance fixes for two numeric tests that compared approximations for bit equality",
    "JabRef/jabref": "Repaired fetcher tests that broke when upstream metadata services changed their responses",
    "Sakram-Arch/simulation": "Removed credentials that were committed to the repository, and fixed the migration integration tests",
}


def api(url):
    request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    if TOKEN:
        request.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def landed_commit_count(repo):
    """Commits GitHub attributes to USER on repo's default branch — the real
    "merged" count, however the commit actually got there."""
    n, page = 0, 1
    while True:
        items = api(f"https://api.github.com/repos/{repo}/commits?author={USER}&per_page=100&page={page}")
        n += len(items)
        if len(items) < 100 or page >= 10:
            return n
        page += 1


def open_pr_count(repo):
    res = api("https://api.github.com/search/issues?q="
              + urllib.parse.quote(f"repo:{repo} author:{USER} is:pr is:open"))
    return res.get("total_count", 0)


def discover_repos():
    """Every repo with at least one PR by USER — just used to find candidates;
    merged counts come from landed_commit_count, not PR state."""
    repos, page = set(), 1
    while True:
        result = api(
            "https://api.github.com/search/issues"
            f"?q=author%3A{USER}+is%3Apr&per_page=100&page={page}"
        )
        items = result.get("items", [])
        for item in items:
            repo = item["repository_url"].split("/repos/", 1)[1]
            if repo not in EXCLUDE and repo.split("/")[0] not in EXCLUDE_OWNERS:
                repos.add(repo)
        if len(items) < 100:
            break
        page += 1
    return repos


def collect():
    """Return {repo: {"merged": n, "open": n}} for every repo with a PR."""
    repos = {}
    for repo in discover_repos():
        try:
            merged = landed_commit_count(repo)
        except (urllib.error.URLError, ValueError):
            continue  # unreachable or rate-limited this run; try again next run rather than report 0
        try:
            open_n = open_pr_count(repo)
        except (urllib.error.URLError, ValueError):
            open_n = 0
        if merged or open_n:
            repos[repo] = {"merged": merged, "open": open_n}
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
    import re
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
