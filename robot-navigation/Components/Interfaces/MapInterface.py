class IGrid:
    """
    Abstract base class representing a 2D grid structure used in pathfinding algorithms.
    Defines core methods for wall handling and movement validation.
    """

    def __init__(self, rows: int, cols: int) -> None:
        """
        Initialize a grid with a given number of rows and columns.

        Args:
            rows (int): Number of rows in the grid.
            cols (int): Number of columns in the grid.
        """
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def appendWall(self, x: int, y: int, w: int, h: int) -> None:
        """
        Add a wall to the grid by marking a rectangular area.

        Args:
            x (int): Top-left x-coordinate of the wall.
            y (int): Top-left y-coordinate of the wall.
            w (int): Width of the wall.
            h (int): Height of the wall.
        """
        raise NotImplementedError("appendWall must be implemented in a subclass.")

    def isMovable(self, x: int, y: int) -> bool:
        """
        Determine whether the given grid cell is traversable.

        Args:
            x (int): Row index.
            y (int): Column index.

        Returns:
            bool: True if the cell is not a wall and within bounds, False otherwise.
        """
        raise NotImplementedError("isMovable must be implemented in a subclass.")

    def toArray(self):
        """
        Convert the grid to a standard array format for processing or export.

        Returns:
            Any: Representation of the grid structure.
        """
        raise NotImplementedError("toArray must be implemented in a subclass.")


class INode:
    """
    Abstract base class for a node used in search algorithms.
    Encapsulates coordinates, cost, parent reference, and depth tracking.
    """

    def __init__(self, sX: int, sY: int, parent=None, pathCost: int = 0) -> None:
        """
        Initialize a node with its position, optional parent, and path cost.

        Args:
            sX (int): X-coordinate of the node.
            sY (int): Y-coordinate of the node.
            parent (INode, optional): Parent node used for backtracking.
            pathCost (int, optional): Accumulated cost from start to this node.
        """
        self.x = sX
        self.y = sY
        self.parent = parent
        self.pathCost = pathCost
        self.depth = 0  # May be used in depth-based algorithms like IDDFS

    def __repr__(self) -> str:
        """Provide a debug-friendly string representation of the node."""
        return f"<Node ({self.x}, {self.y})>"

    def __lt__(self, node: object) -> bool:
        """
        Support comparison for use in priority queues.

        Args:
            node (object): Another node to compare with.

        Returns:
            bool: True if this node is considered less than the other.
        """
        return (self.x + self.y) < (node.x + node.y) if isinstance(node, INode) else False

    def __eq__(self, node: object) -> bool:
        """
        Check equality between two nodes based on position.

        Args:
            node (object): Node to compare against.

        Returns:
            bool: True if both nodes share the same position.
        """
        return (self.x + self.y) == (node.x + node.y) if isinstance(node, INode) else False


class IPath:
    """
    Abstract base class for path utilities.
    Responsible for reconstructing and interpreting paths.
    """

    def __init__(self) -> None:
        pass

    def getFullPathFromNode(self, node: INode) -> list:
        """
        Trace the path from the given node back to the start.

        Args:
            node (INode): End node of the path.

        Returns:
            list: Full reconstructed path as a list of nodes.
        """
        raise NotImplementedError("getFullPathFromNode must be implemented in a subclass.")

    def reinterpretPath(self, path: INode, next: INode) -> str:
        """
        Translate the movement between two nodes into a meaningful action or direction.

        Args:
            path (INode): Current node in the path.
            next (INode): Next node in the path.

        Returns:
            str: Direction or label representing the transition.
        """
        raise NotImplementedError("reinterpretPath must be implemented in a subclass.")
