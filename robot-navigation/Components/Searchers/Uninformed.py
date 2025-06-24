from Components.Map.Node import Node
from Components.Map.Grid import Grid
from collections import deque
from Components.Enums.Direction import Direction
from Components.Map.Path import Path
from Components.Interfaces.SearchInterface import IUninformedSearch


class DepthFirstSearch(IUninformedSearch):
    def search(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]):
        stack = [(Node(start[0], start[1]), [])]
        visited = set()
        explored = 0
        visual_changes = []

        while stack:
            current_node, _ = stack.pop()
            explored += 1

            if (current_node.x, current_node.y) == goal:
                return Path.getFullPathFromNode(current_node), explored, visual_changes

            visited.add((current_node.x, current_node.y))
            visual_changes.append(((current_node.x, current_node.y), 'visited'))

            successors = []
            for dx, dy in Direction.getTupleValues():
                nx, ny = current_node.x + dx, current_node.y + dy
                if (nx, ny) not in visited and grid.isMovable(nx, ny):
                    child = Node(nx, ny, current_node, current_node.pathCost + 1)
                    successors.append((child, Path.getFullPathFromNode(current_node)))
                    visual_changes.append(((nx, ny), 'frontier'))

            stack.extend(successors[::-1])

        return None, explored, visual_changes


class BreadthFirstSearch(IUninformedSearch):
    def search(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]):
        queue = deque([[Node(start[0], start[1])]])
        visited = set()
        explored = 0
        visual_changes = []

        while queue:
            path = queue.popleft()
            current = path[-1]
            explored += 1

            if (current.x, current.y) == goal:
                return Path.getFullPathFromNode(current), explored, visual_changes

            visited.add((current.x, current.y))
            visual_changes.append(((current.x, current.y), 'visited'))

            for dx, dy in Direction.getTupleValues():
                nx, ny = current.x + dx, current.y + dy
                if (nx, ny) not in visited and grid.isMovable(nx, ny):
                    child = Node(nx, ny, current, current.pathCost + 1)
                    queue.append(path + [child])
                    visited.add((nx, ny))
                    visual_changes.append(((nx, ny), 'frontier'))

        return None, explored, visual_changes


class CustomSearchOne(IUninformedSearch):
    def dls(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int], depth_limit: int):
        stack = [(Node(start[0], start[1]), [], 0)]
        visited = set()
        explored = 0
        visual_changes = []
        while stack:
            current_node, path, depth = stack.pop()
            explored += 1

            if (current_node.x, current_node.y) == goal:
                return Path.getFullPathFromNode(current_node), explored, visual_changes

            if (current_node.x, current_node.y) not in visited:
                visited.add((current_node.x, current_node.y))
                visual_changes.append(((current_node.x, current_node.y), 'visited'))

                if depth < depth_limit:
                    for dx, dy in Direction.getTupleValues():
                        nx, ny = current_node.x + dx, current_node.y + dy
                        if (nx, ny) not in visited and grid.isMovable(nx, ny):
                            child = Node(nx, ny, current_node, current_node.pathCost + 1)
                            stack.append((child, path + [(current_node.x, current_node.y)], depth + 1))
                            visual_changes.append(((nx, ny), 'frontier'))

        return None, explored, visual_changes
    def iddfs(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]):
        limit = 0
        while True:
            result, explored, visual_changes = self.dls(grid, start, goal, limit)
            if result:
                return result, explored, visual_changes
            limit += 1
    def search(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]):
        return self.iddfs(grid, start, goal)
