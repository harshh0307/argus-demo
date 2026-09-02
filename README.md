# Argus Demo

This is a demo repository for testing **Argus** — an automated API breaking-change detection and self-healing PR platform.

## What's Inside

- `app.py` — Main application using GitHub REST API (users, repos, issues, PRs)
- `webhook_handler.py` — GitHub webhook processor with API calls
- `github_client.py` — Reusable GitHub API client class
- `test_app.py` — Basic test suite

## How Argus Works With This Repo

1. Argus monitors OpenAPI specs (e.g., GitHub API spec)
2. When a breaking change is detected (e.g., endpoint removed, parameter renamed)
3. Argus scans this codebase and finds all affected call sites
4. Argus generates patches and opens a PR with fixes
5. All automatic — no human intervention needed

## Setup

```bash
pip install -r requirements.txt
export GITHUB_TOKEN=your_token_here
python app.py
```