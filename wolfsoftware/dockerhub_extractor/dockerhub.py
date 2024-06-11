"""
This module defines a class for interacting with the Docker Hub API.

It provides methods to authenticate with the API, fetch data, fetch paginated data,
and retrieve information about repositories and tags.

Dependencies:
    - requests

Classes:
    - DockerHubExtractor: A class to interact with the Docker Hub API.
"""

from typing import Any, Dict, List, Optional
import requests
from .exceptions import DockerhubExtractorError


class DockerHubExtractor:
    """
    A class to interact with the Docker Hub API.

    Attributes:
        base_url (str): The base URL for the Docker Hub API.
        auth_username (str): The username for authentication.
        auth_password (str): The password for authentication.
        token (str): The authentication token.
    """

    def __init__(self, auth_username: Optional[str] = None, auth_password: Optional[str] = None) -> None:
        """
        Initialize DockerHubExtractor with optional authentication.

        Args:
            auth_username (str, optional): The username for authentication.
            auth_password (str, optional): The password for authentication.
        """
        self.base_url: str = "https://hub.docker.com/v2/"
        self.auth_username: Optional[str] = auth_username
        self.auth_password: Optional[str] = auth_password
        self.token: Optional[str] = None

        if auth_username and auth_password:
            self.token = self.authenticate(auth_username, auth_password)

    def authenticate(self, username: str, password: str) -> str:
        """
        Authenticate with Docker Hub and retrieve a token.

        Args:
            username (str): The username for authentication.
            password (str): The password for authentication.

        Returns:
            str: The authentication token.

        Raises:
            DockerhubExtractorError: If the authentication fails.
        """
        auth_url: str = f"{self.base_url}users/login/"
        response: requests.Response = requests.post(auth_url, json={"username": username, "password": password}, timeout=10)

        if response.status_code != 200:
            raise DockerhubExtractorError("Failed to authenticate with Docker Hub.")

        return response.json()["token"]

    def get_headers(self) -> Dict[str, str]:
        """
        Get the headers for API requests, including the authorization token if available.

        Returns:
            Dict[str, str]: The headers for API requests.
        """
        headers: Dict[str, str] = {}
        if self.token:
            headers["Authorization"] = f"JWT {self.token}"
        return headers

    def fetch_data(self, endpoint: str) -> Dict[str, Any]:
        """
        Fetch data from a specific API endpoint.

        Args:
            endpoint (str): The API endpoint to fetch data from.

        Returns:
            Dict[str, Any]: The JSON response from the API.

        Raises:
            DockerhubExtractorError: If the request fails.
        """
        url: str = f"{self.base_url}{endpoint}"
        headers: Dict[str, str] = self.get_headers()
        response: requests.Response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            raise DockerhubExtractorError(f"Failed to fetch data from {endpoint}")

        return response.json()

    def fetch_paginated_data(self, endpoint: str) -> List[Dict[str, Any]]:
        """
        Fetch paginated data from a specific API endpoint.

        Args:
            endpoint (str): The API endpoint to fetch paginated data from.

        Returns:
            List[Dict[str, Any]]: A list of JSON objects from the paginated response.

        Raises:
            DockerhubExtractorError: If the request fails.
        """
        data: List[Dict[str, Any]] = []
        url: str = f"{self.base_url}{endpoint}"
        headers: Dict[str, str] = self.get_headers()

        while url:
            response: requests.Response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                raise DockerhubExtractorError(f"Failed to fetch paginated data from {endpoint}")

            json_response: Dict[str, Any] = response.json()
            data.extend(json_response['results'])
            url = json_response['next']
        return data

    def get_user_repositories(self, target_username: str) -> List[Dict[str, Any]]:
        """
        Get the list of repositories for a specific user or organization.

        Args:
            target_username (str): The username or organization to fetch repositories for.

        Returns:
            List[Dict[str, Any]]: A list of repositories.

        Raises:
            DockerhubExtractorError: If the request fails.
        """
        return self.fetch_paginated_data(f"repositories/{target_username}/")

    def get_repository_info(self, target_username: str, repository: str) -> Dict[str, Any]:
        """
        Get information about a specific repository.

        Args:
            target_username (str): The username or organization that owns the repository.
            repository (str): The name of the repository.

        Returns:
            Dict[str, Any]: The repository information.

        Raises:
            DockerhubExtractorError: If the request fails.
        """
        return self.fetch_data(f"repositories/{target_username}/{repository}/")

    def get_repository_tags(self, target_username: str, repository: str) -> List[Dict[str, Any]]:
        """
        Get the tags for a specific repository.

        Args:
            target_username (str): The username or organization that owns the repository.
            repository (str): The name of the repository.

        Returns:
            List[Dict[str, Any]]: A list of tags for the repository.

        Raises:
            DockerhubExtractorError: If the request fails.
        """
        return self.fetch_paginated_data(f"repositories/{target_username}/{repository}/tags/")

    def get_repositories_and_versions(self, target_username: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get the list of repositories and their tags for a specific user or organization.

        Args:
            target_username (str): The username or organization to fetch repositories and tags for.

        Returns:
            Dict[str, List[Dict[str, Any]]]: A dictionary with repositories and their tags.

        Raises:
            DockerhubExtractorError: If the request fails.
        """
        try:
            user_repositories: List[Dict[str, Any]] = self.get_user_repositories(target_username)
            repositories: List[Dict[str, Any]] = []

            for repo in user_repositories:
                tags_data: List[Dict[str, Any]] = self.get_repository_tags(target_username, repo['name'])
                tags: Dict[str, Dict[str, Any]] = {tag['name']: tag for tag in tags_data}
                tag_list: List[str] = [tag['name'] for tag in tags_data]
                repo_info: Dict[str, Any] = {
                    'name': repo['name'],
                    'namespace': repo['namespace'],
                    'repository_type': repo['repository_type'],
                    'status': repo['status'],
                    'status_description': 'active' if repo['status'] == 1 else 'inactive',
                    'description': repo['description'],
                    'is_private': repo['is_private'],
                    'star_count': repo['star_count'],
                    'pull_count': repo['pull_count'],
                    'last_updated': repo['last_updated'],
                    'date_registered': repo['date_registered'],
                    'affiliation': repo.get('affiliation', ''),
                    'media_types': repo.get('media_types', []),
                    'content_types': repo.get('content_types', []),
                    'categories': repo.get('categories', []),
                    'tags': tags,
                    'tag_list': tag_list
                }
                repositories.append(repo_info)
            return {'repositories': repositories}
        except requests.RequestException as e:
            raise DockerhubExtractorError(f"An error occurred while fetching repositories and versions: {e}") from e
