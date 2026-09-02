"""Demo app that uses the GitHub API — Argus will detect breaking changes and fix these call sites."""

import requests

GITHUB_API = "https://api.github.com"


def get_user_repos(username: str, token: str) -> list:
    """Fetch all public repos for a user."""
    resp = requests.get(
        f"{GITHUB_API}/users/{username}/repos",
        headers={"Authorization": f"token {token}"},
        params={"per_page": 100, "sort": "updated"},
    )
    resp.raise_for_status()
    return resp.json()


def create_repository(name: str, token: str, private: bool = False) -> dict:
    """Create a new repository."""
    resp = requests.post(
        f"{GITHUB_API}/user/repos",
        headers={"Authorization": f"token {token}"},
        json={"name": name, "private": private, "auto_init": True},
    )
    resp.raise_for_status()
    return resp.json()


def get_repo_issues(owner: str, repo: str, token: str, state: str = "open") -> list:
    """Fetch issues for a repository."""
    resp = requests.get(
        f"{GITHUB_API}/repos/{owner}/{repo}/issues",
        headers={"Authorization": f"token {token}"},
        params={"state": state, "per_page": 50},
    )
    resp.raise_for_status()
    return resp.json()


def create_issue(owner: str, repo: str, title: str, body: str, token: str) -> dict:
    """Create a new issue."""
    resp = requests.post(
        f"{GITHUB_API}/repos/{owner}/{repo}/issues",
        headers={"Authorization": f"token {token}"},
        json={"title": title, "body": body},
    )
    resp.raise_for_status()
    return resp.json()


def get_pull_requests(owner: str, repo: str, token: str) -> list:
    """Fetch pull requests."""
    resp = requests.get(
        f"{GITHUB_API}/repos/{owner}/{repo}/pulls",
        headers={"Authorization": f"token {token}"},
        params={"state": "open", "per_page": 30},
    )
    resp.raise_for_status()
    return resp.json()


def delete_repository(owner: str, repo: str, token: str) -> None:
    """Delete a repository."""
    resp = requests.delete(
        f"{GITHUB_API}/repos/{owner}/{repo}",
        headers={"Authorization": f"token {token}"},
    )
    resp.raise_for_status()


if __name__ == "__main__":
    import os

    token = os.environ.get("GITHUB_TOKEN", "")
    if not token:
        print("Set GITHUB_TOKEN environment variable")
        exit(1)

    repos = get_user_repos("harshh0307", token)
    print(f"Found {len(repos)} repos")

    for repo in repos[:5]:
        issues = get_repo_issues("harshh0307", repo["name"], token)
        prs = get_pull_requests("harshh0307", repo["name"], token)
        print(f"  {repo['name']}: {len(issues)} issues, {len(prs)} PRs")