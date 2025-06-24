from typing import Any
from Components.Map.Grid import Grid


class IHeuristicType:
    """
    Interface (base class) for heuristic functions used in informed search algorithms.
    Each heuristic subclass must implement the `calculate()` method.
    """

    def __init__(self, current: tuple[int, int], goal: tuple[int, int]) -> None:
        """
        Store the current and goal positions.

        Args:
            current (tuple[int, int]): Current node coordinates.
            goal (tuple[int, int]): Goal node coordinates.
        """
        self.current = current
        self.goal = goal

    def calculate(self) -> int | float:
        """
        Computes the heuristic value (h(n)).

        Returns:
            int | float: Heuristic cost estimate from current to goal.
        """
        raise NotImplementedError("This method must be implemented in a subclass")

    def __add__(self, other):
        """
        Overloads + operator to allow combining two heuristics.

        Args:
            other (IHeuristicType): Another heuristic object.

        Returns:
            int | float: Combined heuristic value.
        """
        return self.calculate() + other.calculate()


class ISearch:
    """
    Interface (base class) for all search strategies (both informed and uninformed).
    Provides the common structure for implementing the `search()` method.
    """

    def __init__(self) -> None:
        """Base constructor for ISearch with no initialization needed."""
        pass

    def search(self) -> Any:
        """
        Base method for search logic, to be implemented in child classes.

        Returns:
            Any: The result of the search process.
        """
        raise NotImplementedError("This method must be implemented in a subclass")


class IUninformedSearch(ISearch):
    """
    Interface for uninformed search algorithms (e.g., DFS, BFS, IDDFS).
    Inherits from ISearch.
    """

    def __init__(self) -> None:
        super().__init__()

    def search(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> (tuple[list, int, list] | tuple[None, int, list]):
        """
        Abstract method to be implemented by each uninformed algorithm.

        Args:
            grid (Grid): The environment represented as a grid.
            start (tuple[int, int]): Starting position.
            goal (tuple[int, int]): Target position.

        Returns:
            tuple[list, int, list] | tuple[None, int, list]:
            A tuple of (path to goal, number of visited nodes, list of visual changes), or None if no path is found.
        """
        raise NotImplementedError("This method must be implemented in a subclass")


class IInformedSearch(ISearch):
    """
    Interface for informed search algorithms (e.g., A*, Greedy, Weighted A*).
    Inherits from ISearch.
    """

    def __init__(self) -> None:
        super().__init__()

    def search(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int], heuristicType: IHeuristicType | int) -> (tuple[list, int, list] | tuple[None, int, list]):
        """
        Abstract method to be implemented by each informed algorithm.

        Args:
            grid (Grid): The grid-based environment.
            start (tuple[int, int]): Starting position.
            goal (tuple[int, int]): Goal position.
            heuristicType (IHeuristicType | int): The heuristic strategy to use.

        Returns:
            tuple[list, int, list] | tuple[None, int, list]:
            A tuple of (path to goal, number of visited nodes, list of visual changes), or None if no path is found.
        """
        raise NotImplementedError("This method must be implemented in a subclass")
