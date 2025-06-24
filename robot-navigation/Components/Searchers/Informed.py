from Components.Map.Node import Node
from Components.Map.Grid import Grid
from Components.Enums.Direction import Direction
from Components.Searchers.Heuristic import Heuristic
import heapq
from Components.Map.Path import Path
from Components.Interfaces.SearchInterface import IHeuristicType, IInformedSearch


class GreedyBestFirstSearch(IInformedSearch):
    def search(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int], heuristicType: IHeuristicType | int):
        heuristic_cost = heuristicType(start, goal).calculate() if issubclass(heuristicType, IHeuristicType) else Heuristic(start, goal).getHeuristicFunction(heuristicType)
        frontier = [(heuristic_cost, Node(start[0], start[1]))]
        heapq.heapify(frontier)

        visited = set()
        changes = []
        explored = 0

        while frontier:
            cost, current = heapq.heappop(frontier)
            explored += 1

            if (current.x, current.y) == goal:
                return Path.getFullPathFromNode(current), explored, changes

            visited.add((current.x, current.y))
            changes.append(((current.x, current.y), 'visited'))

            for dx, dy in Direction.getTupleValues():
                nx, ny = current.x + dx, current.y + dy
                if (nx, ny) not in visited and grid.isMovable(nx, ny):
                    child = Node(nx, ny, current, current.pathCost + 1)
                    cost = heuristicType((nx, ny), goal).calculate() if issubclass(heuristicType, IHeuristicType) else Heuristic((nx, ny), goal).getHeuristicFunction(heuristicType)
                    heapq.heappush(frontier, (cost, child))
                    visited.add((nx, ny))
                    changes.append(((nx, ny), 'frontier'))

        return None, explored, changes


class AStarSearch(IInformedSearch):
    def search(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int], heuristicType: IHeuristicType | int):
        initial_heuristic = heuristicType(start, goal).calculate() if issubclass(heuristicType, IHeuristicType) else Heuristic(start, goal).getHeuristicFunction(heuristicType)
        frontier = [(initial_heuristic, Node(start[0], start[1]))]
        heapq.heapify(frontier)

        visited = set()
        explored = 0
        changes = []

        while frontier:
            cost, current = heapq.heappop(frontier)
            explored += 1

            if (current.x, current.y) == goal:
                return Path.getFullPathFromNode(current), explored, changes

            visited.add((current.x, current.y))
            changes.append(((current.x, current.y), 'visited'))

            for dx, dy in Direction.getTupleValues():
                nx, ny = current.x + dx, current.y + dy
                if (nx, ny) not in visited and grid.isMovable(nx, ny):
                    child = Node(nx, ny, current, current.pathCost + 1)
                    heuristic = heuristicType((nx, ny), goal).calculate() if issubclass(heuristicType, IHeuristicType) else Heuristic((nx, ny), goal).getHeuristicFunction(heuristicType)
                    total_cost = child.pathCost + heuristic
                    heapq.heappush(frontier, (total_cost, child))
                    visited.add((nx, ny))
                    changes.append(((nx, ny), 'frontier'))

        return None, explored, changes


class CustomSearchTwo(IInformedSearch):
    def search(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int], heuristicType: IHeuristicType | int, weight: int = 0):
        w = 1.25 if weight == 0 else weight
        return self._weightedAStar(grid, start, goal, heuristicType, w)

    def _weightedAStar(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int], heuristicType: IHeuristicType | int, weight: float):
        start_node = Node(start[0], start[1], None, 0)

        h = heuristicType(start, goal).calculate() if issubclass(heuristicType, IHeuristicType) else Heuristic(start, goal).getHeuristicFunction(heuristicType)
        start_cost = start_node.pathCost + weight * h
        frontier = [(start_cost, start_node)]
        heapq.heapify(frontier)

        visited = set()
        explored = 0
        changes = []

        while frontier:
            current_cost, current = heapq.heappop(frontier)
            explored += 1

            if (current.x, current.y) == goal:
                return Path.getFullPathFromNode(current), explored, changes

            visited.add((current.x, current.y))
            changes.append(((current.x, current.y), 'visited'))

            for dx, dy in Direction.getTupleValues():
                nx, ny = current.x + dx, current.y + dy
                if (nx, ny) not in visited and grid.isMovable(nx, ny):
                    child = Node(nx, ny, current, current.pathCost + 1)
                    h = heuristicType((nx, ny), goal).calculate() if issubclass(heuristicType, IHeuristicType) else Heuristic((nx, ny), goal).getHeuristicFunction(heuristicType)
                    f = child.pathCost + weight * h
                    heapq.heappush(frontier, (f, child))
                    visited.add((nx, ny))
                    changes.append(((nx, ny), 'frontier'))

        return None, explored, changes
