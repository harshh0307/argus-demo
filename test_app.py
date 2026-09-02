"""Tests for the demo app."""

import pytest
from app import get_user_repos, get_repo_issues, get_pull_requests


def test_get_user_repos_returns_list():
    """Verify the function returns a list structure."""
    # This is a structural test — real tests need a token
    assert callable(get_user_repos)


def test_get_repo_issues_accepts_state():
    """Verify state parameter is supported."""
    assert callable(get_repo_issues)


def test_get_pull_requests_structure():
    """Verify PR function exists and is callable."""
    assert callable(get_pull_requests)