"""
This module contains fixtures and tests for the DockerHubExtractor class.

It provides fixtures to create instances of DockerHubExtractor for testing purposes,
along with mocks for external dependencies such as requests.post.
"""
from typing import Generator, Union, Any

from unittest.mock import patch, MagicMock, AsyncMock

import pytest

from wolfsoftware.dockerhub_extractor import DockerHubExtractor


@pytest.fixture
def dockerhub_instance() -> DockerHubExtractor:
    """
    Fixture to provide an instance of DockerHubExtractor for testing.

    This fixture initializes a DockerHubExtractor object with default configuration
    for use in unit tests.

    Returns:
        DockerHubExtractor: An instance of the DockerHubExtractor class.
    """
    return DockerHubExtractor()


@pytest.fixture
def mock_requests_post() -> Generator[Union[MagicMock, AsyncMock], Any, None]:
    """
    Fixture to provide a mocked version of requests.post for testing.

    This fixture patches the requests.post function with a MagicMock object
    to simulate HTTP POST requests in unit tests.

    Yields:
        Generator[Union[MagicMock, AsyncMock], Any, None]: A generator yielding a MagicMock object.
    """
    with patch('requests.post') as mock_post:
        yield mock_post
