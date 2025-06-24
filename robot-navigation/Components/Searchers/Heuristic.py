from Components.Interfaces.SearchInterface import IHeuristicType

class ManhattanDistance(IHeuristicType):
    def __init__(self, current: tuple[int, int], goal: tuple[int, int]) -> None:
        super().__init__(current, goal)

    def calculate(self) -> int | float:
        return abs(self.current[0] - self.goal[0]) + abs(self.current[1] - self.goal[1])

class EuclideanDistance(IHeuristicType):
    def __init__(self, current: tuple[int, int], goal: tuple[int, int]) -> None:
        super().__init__(current, goal)

    def calculate(self) -> int | float:
        dx = self.current[0] - self.goal[0]
        dy = self.current[1] - self.goal[1]
        return (dx ** 2 + dy ** 2) ** 0.5

class ChebyshevDistance(IHeuristicType):
    def __init__(self, current: tuple[int, int], goal: tuple[int, int]) -> None:
        super().__init__(current, goal)

    def calculate(self) -> int | float:
        dx = abs(self.current[0] - self.goal[0])
        dy = abs(self.current[1] - self.goal[1])
        return max(dx, dy)

class Heuristic:
    def __init__(self, current: tuple[int, int], goal: tuple[int, int]) -> None:
        self.current = current
        self.goal = goal

    def getHeuristicFunction(self, heuristicType: int = 1) -> int | float:
        match heuristicType:
            case 1:
                return ManhattanDistance(self.current, self.goal).calculate()
            case 2:
                return EuclideanDistance(self.current, self.goal).calculate()
            case 3:
                return ChebyshevDistance(self.current, self.goal).calculate()
            case _:
                return float('inf')  # return a large default if undefined
