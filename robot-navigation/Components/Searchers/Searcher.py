from Components.Map.Grid import Grid
from Components.Searchers.Heuristic import ManhattanDistance
from Components.Searchers.Informed import AStarSearch, CustomSearchTwo, GreedyBestFirstSearch
from Components.Searchers.Uninformed import BreadthFirstSearch, CustomSearchOne, DepthFirstSearch


class Searcher:
    def __init__(self, grid: Grid, start: tuple[int, int], goal: list[tuple[int, int]], typeOfSearch: str) -> None:
        self.grid = grid
        self.start = start
        self.goal = goal
        self.typeOfSearch = typeOfSearch
        self.heuristicFunction = ManhattanDistance
        self.tPath, self.numNodes, self.changes = [], [], []

    def getResult(self):
        if isinstance(self.goal, list):
            for target in self.goal:
                if self.typeOfSearch.lower() == "dfs":
                    path, nodes, visual = DepthFirstSearch().search(self.grid, self.start, target)
                elif self.typeOfSearch.lower() == "bfs":
                    path, nodes, visual = BreadthFirstSearch().search(self.grid, self.start, target)
                elif self.typeOfSearch.lower() == "cus1":
                    path, nodes, visual = CustomSearchOne().search(self.grid, self.start, target)
                elif self.typeOfSearch.lower() == "gbfs":
                    path, nodes, visual = GreedyBestFirstSearch().search(self.grid, self.start, target, self.heuristicFunction)
                elif self.typeOfSearch.lower() == "as":
                    path, nodes, visual = AStarSearch().search(self.grid, self.start, target, self.heuristicFunction)
                elif self.typeOfSearch.lower() == "cus2":
                    path, nodes, visual = CustomSearchTwo().search(self.grid, self.start, target, self.heuristicFunction)
                else:
                    raise ValueError("Please provide a valid search algorithm [bfs, dfs, as, gbfs, cus1, cus2]")

                self.tPath.append(path)
                self.numNodes.append(nodes)
                self.changes.append(visual)

            if self.typeOfSearch.lower() in ["bfs", "dfs", "cus1"]:
                return self.tPath, self.numNodes, self.changes
            else:
                shortest_index = 0
                for i in range(len(self.tPath) - 1):
                    if len(self.tPath[i]) <= len(self.tPath[i + 1]):
                        return [self.tPath[i]], self.numNodes[i], self.changes[i]
                    shortest_index += 1

        if isinstance(self.goal, tuple):
            if self.typeOfSearch.lower() == "dfs":
                path, nodes, visual = DepthFirstSearch().search(self.grid, self.start, self.goal)
            elif self.typeOfSearch.lower() == "bfs":
                path, nodes, visual = BreadthFirstSearch().search(self.grid, self.start, self.goal)
            elif self.typeOfSearch.lower() == "cus1":
                path, nodes, visual = CustomSearchOne().search(self.grid, self.start, self.goal)
            elif self.typeOfSearch.lower() == "gbfs":
                path, nodes, visual = GreedyBestFirstSearch().search(self.grid, self.start, self.goal, self.heuristicFunction)
            elif self.typeOfSearch.lower() == "as":
                path, nodes, visual = AStarSearch().search(self.grid, self.start, self.goal, self.heuristicFunction)
            elif self.typeOfSearch.lower() == "cus2":
                path, nodes, visual = CustomSearchTwo().search(self.grid, self.start, self.goal, self.heuristicFunction)
            else:
                raise ValueError("Please provide a valid search algorithm [bfs, dfs, as, gbfs, cus1, cus2]")

            return path, nodes, visual
