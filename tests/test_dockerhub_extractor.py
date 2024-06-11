"""
This module contains unit tests for the DockerHubExtractor class.

It includes tests for versioning and various functionality tests for methods
such as authenticate, get_headers, fetch_data, fetch_paginated_data,
get_user_repositories, get_repository_info, get_repository_tags,
and get_repositories_and_versions.
"""

from typing import Any, Dict, List, Optional

import importlib.metadata
from unittest.mock import MagicMock

from wolfsoftware.dockerhub_extractor import DockerHubExtractor


def test_version() -> None:
    """
    Test to ensure the version of the package is correctly retrieved.

    This test retrieves the version of the package using importlib.metadata and asserts that the version
    is not None and not 'unknown'.
    """
    version: Optional[str] = None

    try:
        version = importlib.metadata.version('wolfsoftware.dockerhub_extractor')
    except importlib.metadata.PackageNotFoundError:
        version = None

    assert version is not None, "Version should be set"  # nosec: B101
    assert version != 'unknown', f"Expected version, but got {version}"  # nosec: B101


def test_authenticate(dockerhub_instance: DockerHubExtractor, mock_requests_post: MagicMock) -> None:
    """
    Test the authenticate method of DockerHubExtractor.

    This test verifies that the authenticate method of DockerHubExtractor
    successfully authenticates with Docker Hub and retrieves a token.
    """
    # Mocking the response
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.json.return_value = {"token": "dummy_token"}

    # Call the authenticate method
    token: str = dockerhub_instance.authenticate("dummy_username", "dummy_password")

    # Assertions
    assert token == "dummy_token", "Token should be retrieved after successful authentication"  # nosec: B101, B105
    mock_requests_post.assert_called_once_with(
        "https://hub.docker.com/v2/users/login/",
        json={"username": "dummy_username", "password": "dummy_password"},
        timeout=10
    )


def test_get_headers(dockerhub_instance: DockerHubExtractor) -> None:
    """
    Test the get_headers method of DockerHubExtractor.

    This test verifies that the get_headers method of DockerHubExtractor
    returns a dictionary of HTTP headers.
    """
    headers: Dict[str, str] = dockerhub_instance.get_headers()

    assert isinstance(headers, dict), "Headers should be a dictionary"  # nosec: B101


def test_fetch_data(dockerhub_instance: DockerHubExtractor) -> None:
    """
    Test the fetch_data method of DockerHubExtractor.

    This test verifies that the fetch_data method of DockerHubExtractor
    successfully fetches data from a specified endpoint.
    """
    # Example endpoint for testing
    endpoint = "repositories/wolfsoftwareltd/alpine-bash/"
    data: Dict[str, Any] = dockerhub_instance.fetch_data(endpoint)

    assert isinstance(data, dict), "Fetched data should be a dictionary"  # nosec: B101


def test_fetch_paginated_data(dockerhub_instance: DockerHubExtractor) -> None:
    """
    Test the fetch_paginated_data method of DockerHubExtractor.

    This test verifies that the fetch_paginated_data method of DockerHubExtractor
    successfully fetches paginated data from a specified endpoint.
    """
    # Example endpoint for testing
    endpoint = "repositories/wolfsoftwareltd/alpine-bash/tags/"
    data: List[Dict[str, Any]] = dockerhub_instance.fetch_paginated_data(endpoint)

    assert isinstance(data, list), "Fetched paginated data should be a list"  # nosec: B101


def test_get_user_repositories(dockerhub_instance: DockerHubExtractor) -> None:
    """
    Test the get_user_repositories method of DockerHubExtractor.

    This test verifies that the get_user_repositories method of DockerHubExtractor
    successfully retrieves repositories for a specified username.
    """
    # Example username for testing
    username = "wolfsoftwareltd"
    repositories: List[Dict[str, Any]] = dockerhub_instance.get_user_repositories(username)

    assert isinstance(repositories, list), "User repositories should be a list"  # nosec: B101


def test_get_repository_info(dockerhub_instance: DockerHubExtractor) -> None:
    """
    Test the get_repository_info method of DockerHubExtractor.

    This test verifies that the get_repository_info method of DockerHubExtractor
    successfully retrieves information about a specified repository.
    """
    # Example username and repository for testing
    username = "wolfsoftwareltd"
    repository = "alpine-bash"
    repo_info: Dict[str, Any] = dockerhub_instance.get_repository_info(username, repository)

    assert isinstance(repo_info, dict), "Repository info should be a dictionary"  # nosec: B101


def test_get_repository_tags(dockerhub_instance: DockerHubExtractor) -> None:
    """
    Test the get_repository_tags method of DockerHubExtractor.

    This test verifies that the get_repository_tags method of DockerHubExtractor
    successfully retrieves tags for a specified repository.
    """
    # Example username and repository for testing
    username = "wolfsoftwareltd"
    repository = "alpine-bash"
    tags: List[Dict[str, Any]] = dockerhub_instance.get_repository_tags(username, repository)

    assert isinstance(tags, list), "Repository tags should be a list"  # nosec: B101


def test_get_repositories_and_versions(dockerhub_instance: DockerHubExtractor) -> None:
    """
    Test the get_repositories_and_versions method of DockerHubExtractor.

    This test verifies that the get_repositories_and_versions method of DockerHubExtractor
    successfully retrieves information about repositories and their versions for a specified username.
    """
    # Example username for testing
    username = "wolfsoftwareltd"
    repositories_info: Dict[str, List[Dict[str, Any]]] = dockerhub_instance.get_repositories_and_versions(username)

    assert isinstance(repositories_info, dict), "Repositories and versions info should be a dictionary"  # nosec: B101
