from typing import Any
import os


class IParse:
    """
    Interface (base class) for any file parser class used to read map input.
    A concrete subclass should implement logic to extract grid dimensions,
    start and goal positions, and wall locations from a file.
    """

    def __init__(self, fileName: str) -> None:
        """
        Opens the file for reading input data.

        Args:
            fileName (str): Name of the file to parse.
        """
        self._openedFile = open(fileName)

    def _parseFileName(self) -> str | Any:
        """
        Returns the name of the opened file.

        Returns:
            str | Any: The name of the file being parsed.
        """
        raise NotImplementedError("This method must be implemented in a subclass")

    def _parseCoordinates(self, text: str) -> tuple:
        """
        Converts a string of coordinates into a tuple of integers.

        Args:
            text (str): A string representing coordinates, e.g., '(2, 3)'.

        Returns:
            tuple: A tuple (x, y) representing grid coordinates.
        """
        raise NotImplementedError("This method must be implemented in a subclass")

    def parse(self) -> list:
        """
        Reads the entire file and extracts structured grid data.

        Returns:
            list: A dictionary or structured list containing grid size,
                  start point, goal points, and wall coordinates.
        """
        raise NotImplementedError("This method must be implemented in a subclass")
