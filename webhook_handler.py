"""Webhook handler — processes GitHub events and calls the API."""

import hashlib
import hmac
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

import requests

GITHUB_API = "https://api.github.com"


class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        payload = json.loads(body)

        event = self.headers.get("X-GitHub-Event", "")

        if event == "push":
            self._handle_push(payload)
        elif event == "pull_request":
            self._handle_pr(payload)
        elif event == "issues":
            self._handle_issue(payload)
        else:
            print(f"Ignoring event: {event}")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"ok": true}')

    def _handle_push(self, payload):
        repo = payload["repository"]["full_name"]
        branch = payload["ref"].split("/")[-1]
        commits = len(payload.get("commits", []))
        print(f"Push to {repo}/{branch}: {commits} commits")

        # Fetch updated repo info
        resp = requests.get(
            f"{GITHUB_API}/repos/{repo}",
            headers={"Accept": "application/vnd.github+json"},
        )
        if resp.ok:
            data = resp.json()
            print(f"  Default branch: {data.get('default_branch')}")

    def _handle_pr(self, payload):
        action = payload["action"]
        pr = payload["pull_request"]
        print(f"PR {action}: #{pr['number']} in {pr['base']['repo']['full_name']}")

        if action == "opened":
            # Fetch PR details
            resp = requests.get(
                pr["url"],
                headers={"Accept": "application/vnd.github+json"},
            )
            if resp.ok:
                print(f"  Title: {resp.json().get('title')}")

    def _handle_issue(self, payload):
        action = payload["action"]
        issue = payload["issue"]
        print(f"Issue {action}: #{issue['number']} - {issue['title']}")


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), WebhookHandler)
    print("Webhook server running on port 8080")
    server.serve_forever()