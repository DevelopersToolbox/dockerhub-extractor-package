<!-- markdownlint-disable -->
<p align="center">
    <a href="https://github.com/DevelopersToolbox/">
        <img src="https://cdn.wolfsoftware.com/assets/images/github/organisations/developerstoolbox/black-and-white-circle-256.png" alt="DevelopersToolbox logo" />
    </a>
    <br />
    <a href="https://github.com/DevelopersToolbox/dockerhub-extractor-package/actions/workflows/cicd.yml">
        <img src="https://img.shields.io/github/actions/workflow/status/DevelopersToolbox/dockerhub-extractor-package/cicd.yml?branch=master&label=build%20status&style=for-the-badge" alt="Github Build Status" />
    </a>
    <a href="https://github.com/DevelopersToolbox/dockerhub-extractor-package/blob/master/LICENSE.md">
        <img src="https://img.shields.io/github/license/DevelopersToolbox/dockerhub-extractor-package?color=blue&label=License&style=for-the-badge" alt="License">
    </a>
    <a href="https://github.com/DevelopersToolbox/dockerhub-extractor-package">
        <img src="https://img.shields.io/github/created-at/DevelopersToolbox/dockerhub-extractor-package?color=blue&label=Created&style=for-the-badge" alt="Created">
    </a>
    <br />
    <a href="https://github.com/DevelopersToolbox/dockerhub-extractor-package/releases/latest">
        <img src="https://img.shields.io/github/v/release/DevelopersToolbox/dockerhub-extractor-package?color=blue&label=Latest%20Release&style=for-the-badge" alt="Release">
    </a>
    <a href="https://github.com/DevelopersToolbox/dockerhub-extractor-package/releases/latest">
        <img src="https://img.shields.io/github/release-date/DevelopersToolbox/dockerhub-extractor-package?color=blue&label=Released&style=for-the-badge" alt="Released">
    </a>
    <a href="https://github.com/DevelopersToolbox/dockerhub-extractor-package/releases/latest">
        <img src="https://img.shields.io/github/commits-since/DevelopersToolbox/dockerhub-extractor-package/latest.svg?color=blue&style=for-the-badge" alt="Commits since release">
    </a>
    <br />
    <a href="https://github.com/DevelopersToolbox/dockerhub-extractor-package/blob/master/.github/CODE_OF_CONDUCT.md">
        <img src="https://img.shields.io/badge/Code%20of%20Conduct-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/DevelopersToolbox/dockerhub-extractor-package/blob/master/.github/CONTRIBUTING.md">
        <img src="https://img.shields.io/badge/Contributing-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/DevelopersToolbox/dockerhub-extractor-package/blob/master/.github/SECURITY.md">
        <img src="https://img.shields.io/badge/Report%20Security%20Concern-blue?style=for-the-badge" />
    </a>
    <a href="https://github.com/DevelopersToolbox/dockerhub-extractor-package/issues">
        <img src="https://img.shields.io/badge/Get%20Support-blue?style=for-the-badge" />
    </a>
</p>

## Overview

DockerHub Extractor is a Python package designed to fetch and process detailed information about repositories hosted on Docker Hub.
This package is particularly useful for users who want to retrieve and analyze metadata for repositories maintained by a specific Docker Hub user.

## Features

- Retrieve a list of repositories maintained by a specific Docker Hub user.
- Fetch detailed metadata for each repository, including information such as tags, stars, pulls, and more.
- Custom exceptions for handling errors gracefully.
- Option to set the Docker Hub username after initializing the class.

## Installation

You can install the package using pip:

```sh
pip install wolfsoftware.dockerhub-extractor
```

## Usage

### Basic Usage

Here's a basic example of how to use the DockerHub Extractor:

```python
from wolfsoftware.dockerhub_extractor import DockerHubExtractor

# Initialize without username
dockerhub_extractor = DockerHubExtractor()

# Set username later
dockerhub_extractor.set_username("your_dockerhub_username")

# Get detailed information for all repositories
try:
    repositories_details = dockerhub_extractor.get_all_repositories_details()
    print(repositories_details)
except DockerHubExtractorError as e:
    print(f"An error occurred: {e.message}")
```

### Setting Username During Initialization

You can also set the username during initialization:

```python
dockerhub_extractor = DockerHubExtractor("your_dockerhub_username")
```

### Retrieving User Repositories

You can retrieve a list of repositories maintained by a specific user:

```python
repositories = dockerhub_extractor.get_user_repositories()
print(repositories)
```

### Retrieving Repository Details

To get detailed information about a specific repository:

```python
repository_details = dockerhub_extractor.get_repository_details("repository_name")
print(repository_details)
```

## API Reference

### Classes

#### `DockerHubExtractor`

A class to fetch and process repository details for a given Docker Hub user.

##### `__init__(self, username: str)`

- Initializes the `DockerHubExtractor` with a username.
- Parameters:
  - `username` (str): The Docker Hub username.
- Raises:
  - `DockerHubExtractorError`: If the username is not provided.

##### `set_username(self, username: str)`

- Sets the Docker Hub username.
- Parameters:
  - `username` (str): The Docker Hub username.
- Raises:
  - `DockerHubExtractorError`: If the username is not provided.

##### `get_user_repositories(self) -> list`

- Fetches the list of repositories for the given Docker Hub user.
- Returns:
  - `list`: A list of dictionaries containing repository names and summaries.
- Raises:
  - `DockerHubExtractorError`: If there is an error fetching or parsing the user profile.

##### `get_repository_details(self, repository_name: str) -> dict`

- Fetches detailed information for a specific repository.
- Parameters:
  - `repository_name` (str): The name of the repository.
- Returns:
  - `dict`: A dictionary containing detailed information about the repository.
- Raises:
  - `DockerHubExtractorError`: If there is an error fetching or parsing the repository details.

##### `get_all_repositories_details(self) -> list`

- Fetches detailed information for all repositories of the given Docker Hub user.
- Returns:
  - `list`: A list of dictionaries containing detailed information about each repository.
- Raises:
  - `DockerHubExtractorError`: If there is an error fetching or processing the repository details.

#### `DockerHubExtractorError`

Custom exception class for `DockerHubExtractor` errors.

<br />
<p align="right"><a href="https://wolfsoftware.com/"><img src="https://img.shields.io/badge/Created%20by%20Wolf%20on%20behalf%20of%20Wolf%20Software-blue?style=for-the-badge" /></a></p>
