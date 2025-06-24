from io import *
import os
from Components.Interfaces.ParseInterface import IParse

class Parser(IParse):
    def __init__(self, fileName: str) -> None:
        super().__init__(fileName)

    def _parseFileName(self):
        return os.path.basename(self._openedFile.name)

    def _parseCoordinates(self, line: str):
        # Remove brackets, parentheses, and newline characters
        cleaned = line.strip('[]()\n ')
        return tuple(map(int, cleaned.split(',')))

    def parse(self) -> dict:
        lines = self._openedFile.readlines()

        # First line: grid size
        dimensions = self._parseCoordinates(lines[0])
        # Second line: start coordinates
        start = self._parseCoordinates(lines[1])
        # Third line: goal states separated by '|'
        goals = [self._parseCoordinates(part.strip()) for part in lines[2].split('|')]
        # Remaining lines: walls
        walls = [self._parseCoordinates(line) for line in lines[3:]]

        return {
            "fileName": self._parseFileName(),
            "gridSize": dimensions,
            "startLocation": start,
            "goalLocation": goals,
            "walls": walls
        }
