"""GitHub API client — wraps all API interactions."""

import requests

GITHUB_API = "https://api.github.com"


class GitHubClient:
    def __init__(self, token: str):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json",
        })

    def get_repo(self, owner: str, repo: str) -> dict:
        resp = self.session.get(f"{GITHUB_API}/repos/{owner}/{repo}")
        resp.raise_for_status()
        return resp.json()

    def list_branches(self, owner: str, repo: str) -> list:
        resp = self.session.get(f"{GITHUB_API}/repos/{owner}/{repo}/branches")
        resp.raise_for_status()
        return resp.json()

    def get_file(self, owner: str, repo: str, path: str, ref: str = "main") -> str:
        resp = self.session.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}",
            params={"ref": ref},
        )
        resp.raise_for_status()
        import base64
        return base64.b64decode(resp.json()["content"]).decode("utf-8")

    def create_pull(self, owner: str, repo: str, title: str, head: str, base: str, body: str) -> dict:
        resp = self.session.post(
            f"{GITHUB_API}/repos/{owner}/{repo}/pulls",
            json={"title": title, "head": head, "base": base, "body": body},
        )
        resp.raise_for_status()
        return resp.json()

    def merge_pull(self, owner: str, repo: str, pull_number: int) -> dict:
        resp = self.session.put(
            f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{pull_number}/merge",
        )
        resp.raise_for_status()
        return resp.json()