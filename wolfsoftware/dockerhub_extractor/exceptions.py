"""
This module defines custom exceptions for the DockerHubExtractor project.

Classes:
    - DockerhubExtractorError: A custom exception class for errors in the DockerHubExtractor class.
"""


class DockerhubExtractorError(Exception):
    """
    Custom exception class for DockerHubExtractor errors.

    Attributes:
        message (str): The error message to be displayed.
    """

    def __init__(self, message: str) -> None:
        """
        Initialize the DockerhubExtractorError with a given message.

        Parameters:
            message (str): The error message to be displayed.
        """
        super().__init__(message)
        self.message: str = message
