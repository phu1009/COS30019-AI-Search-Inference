
import tkinter as tk
from tkinter import messagebox, ttk
import random
from Components.Map.Grid import Grid
from Components.Searchers.Searcher import Searcher
from time import *


class UIVisualize(tk.Tk):
    def __init__(self, rows: int, cols: int, search_type: str, cell_size: int = None):
        super().__init__()
        self.title("Tree-based Search Visualizer")
        self.configure(bg='#cedbec')
        self.rows, self.cols = rows, cols

        if cell_size is None:
            self.cell_size = 25 if (self.rows <= 30 or self.cols <= 25) else 22
        else:
            self.cell_size = cell_size

        self.geometry('+600+100')
        self.startColor, self.endColor = (255, 221, 0), (235, 10, 30)
        self.startPoint, self.endPoint = None, None
        self.walls = []
        self.g = Grid(self.cols, self.rows)
        self.buttonFont = ('Arial', 12)
        self.isChoosingStart = self.isChoosingGoal = self.isChoosingWall = False
        self.canvas = tk.Canvas(self, width=self.rows * self.cell_size, height=self.cols * self.cell_size, bg='white')
        self.canvas.pack()
        self.search_type = search_type

    def _drawChanges(self, result=None, changes=None):
        if changes:
            for cell, d_type in changes:
                if cell in (self.startPoint, self.endPoint):
                    continue
                x1, y1 = cell[0] * self.cell_size, cell[1] * self.cell_size
                x2, y2 = (cell[0] + 1) * self.cell_size, (cell[1] + 1) * self.cell_size
                color = '#fbaab1' if d_type == 'frontier' else '#fdd0d4'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                sleep(0.0001)
                self.update()

        for node in result:
            x, y = node.x, node.y
            self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                         (x + 1) * self.cell_size, (y + 1) * self.cell_size, fill='green')
            self.update()

    def _drawGrid(self):
        self.canvas.delete("all")
        for i in range(self.cols):
            for j in range(self.rows):
                x1, y1 = i * self.cell_size, j * self.cell_size
                x2, y2 = (i + 1) * self.cell_size, (j + 1) * self.cell_size

                cell_type = self.grid[i][j]
                color = {'start': '#ff0808', 'end': '#0dff00', 'wall': '#595959'}.get(cell_type, '#cedbec')
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='#0c4da2')

    def _setStart(self, row, col):
        if self.startPoint:
            self.grid[self.startPoint[0]][self.startPoint[1]] = 'e'
        self.startPoint = (row, col)
        self.grid[row][col] = 'start'
        self._drawGrid()

    def _setGoal(self, row, col):
        if self.endPoint and 0 <= self.endPoint[0] <= self.cols and 0 <= self.endPoint[1] <= self.rows:
            self.grid[self.endPoint[0]][self.endPoint[1]] = 'e'
        self.endPoint = (row, col)
        if 0 <= row < self.cols and 0 <= col < self.rows:
            self.grid[row][col] = 'end'
        self._drawGrid()

    def _setWall(self, row, col):
        if self.grid[row][col] in ('start', 'end'):
            return
        self.grid[row][col] = 'wall'
        self.walls.append((row, col, 1, 1))
        self._drawGrid()

    def _randWall(self):
        self._clearMap()
        for i in range(self.cols):
            for j in range(self.rows):
                if random.random() < 0.2:
                    self.grid[i][j] = 'wall'
                    self._setWall(i, j)
                else:
                    self.grid[i][j] = 'e'
        self._drawGrid()

    def _clearMap(self):
        self.startPoint = self.endPoint = None
        self.walls = []
        for i in range(self.cols):
            for j in range(self.rows):
                self.grid[i][j] = 'e'
        self.g.grid = [[0 for _ in range(self.rows)] for _ in range(self.cols)]
        self._drawGrid()

    def _setState(self, state):
        self.isChoosingStart = state == 'start'
        self.isChoosingGoal = state == 'goal'
        self.isChoosingWall = state == 'wall'

    def _handleMouseClick(self, e):
        col = e.y // self.cell_size
        row = e.x // self.cell_size

        if 0 <= row < self.cols and 0 <= col < self.rows:
            if self.isChoosingStart and self.grid[row][col] != 'wall':
                self._setStart(row, col)
            elif self.isChoosingGoal and self.grid[row][col] != 'wall':
                self._setGoal(row, col)
            elif self.isChoosingWall:
                self._setWall(row, col)
            if not self.isChoosingWall:
                self._drawGrid()

    def _visualizePath(self):
        if self.startPoint and self.endPoint:
            searcher = Searcher(self.g, self.startPoint, self.endPoint, self.search_type)
            for wall in self.walls:
                self.g.appendWall(*wall)
            begin = time()
            result, explored, changes = searcher.getResult()
            print(f"{self.search_type} time: {(time() - begin) * 1000.0:.2f} ms")
            print(f"Nodes explored: {explored}")
            if result:
                self._drawChanges(result, changes)
            else:
                messagebox.showinfo("No path found", "No path found in this scenario!")

    def _convertName(self, short_name):
        return {
            'bfs': 'Breadth First Search',
            'dfs': 'Depth First Search',
            'cus1': 'Iterative Deepening DLS',
            'gbfs': 'Greedy Best-First Search',
            'as': 'A*',
            'cus2': 'Weighted A*'
        }.get(short_name, 'Unknown')

    def mainloop(self, n=0):
        self.grid = [['e' for _ in range(self.rows)] for _ in range(self.cols)]
        self._drawGrid()

        self.canvas.bind('<ButtonRelease-1>', self._handleMouseClick)
        self.canvas.bind('<B1-Motion>', self._handleMouseClick)

        btn_config = dict(font=self.buttonFont, bg='#9eb8da', activebackground='#3d71b5', fg='#0c4da2')
        tk.Button(self, text="Start Point", **btn_config, command=lambda: self._setState('start')).pack(side=tk.LEFT, padx=5)
        tk.Button(self, text="Goal Point", **btn_config, command=lambda: self._setState('goal')).pack(side=tk.LEFT, padx=10)
        tk.Button(self, text="Set Walls", **btn_config, command=lambda: self._setState('wall')).pack(side=tk.LEFT, padx=15)
        tk.Button(self, text="Random Walls", **btn_config, command=self._randWall).pack(side=tk.LEFT, padx=15)
        tk.Button(self, text="Clear All", **btn_config, command=self._clearMap).pack(side=tk.LEFT, padx=15)
        tk.Button(self, text="Visualize Path", **btn_config, command=self._visualizePath).pack(side=tk.LEFT, padx=15)

        tk.Label(self, text=self._convertName(self.search_type), font=('Arial', 18), bg='#cedbec', fg='black', height=2).pack(side=tk.LEFT, padx=15)
        return super().mainloop(n)


class MainUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tree-based Search Setup")
        self.geometry("550x500+600+300")
        self.configure(bg='#f0f4f8')

        self.buttonFont = ('Segoe UI', 12)
        self.labelFont = ('Segoe UI Semibold', 13)

        # Title
        tk.Label(self, text="Tree-Based Search Visualizer", font=('Segoe UI Bold', 16),
                 bg='#f0f4f8', fg="#ff0000").pack(pady=15)

        # Frame for input fields
        input_frame = tk.Frame(self, bg='#f0f4f8')
        input_frame.pack(pady=10)

        self._create_field(input_frame, "Rows:", 0)
        self.rows_entry = self._create_entry(input_frame, 0)

        self._create_field(input_frame, "Columns:", 1)
        self.cols_entry = self._create_entry(input_frame, 1)

        self._create_field(input_frame, "Cell Size:", 2)
        self.cell_size_entry = self._create_entry(input_frame, 2)
        self.cell_size_entry.insert(0, '25')

        self._create_field(input_frame, "Search Type:", 3)
        self.searchType = ttk.Combobox(input_frame, values=[
            'BFS', 'DFS', 'Iterative Deepning DLS',
            'Greedy Best-First Search', 'A*', 'Weighted A*'
        ], font=self.buttonFont, state='readonly')
        self.searchType.grid(row=3, column=1, padx=10, pady=10)

        # Start Button
        tk.Button(self, text="Start Visualizer", font=self.buttonFont, width=20,
                  bg='#1f4e79', fg='white', activebackground="#0059ff",
                  command=self._onPress).pack(pady=20)

        # Footer Info
        tk.Label(self, text="Robot Path Navigation", font=self.labelFont,
                 bg='#f0f4f8', fg='#0a2c47').pack()
        tk.Label(self, text="Dinh Phu Nguyen - ID: 105027282", font=('Segoe UI', 11),
                 bg='#f0f4f8', fg='#4a4a4a').pack(pady=(0, 10))

    def _create_field(self, parent, text, row):
        tk.Label(parent, text=text, font=self.labelFont,
                 bg='#f0f4f8', anchor='w').grid(row=row, column=0, padx=10, pady=10, sticky='w')

    def _create_entry(self, parent, row):
        entry = tk.Entry(parent, font=self.buttonFont, width=10)
        entry.grid(row=row, column=1, padx=10, pady=10)
        return entry

    def _convertToInt(self, value):
        try:
            return int(value)
        except ValueError:
            messagebox.showerror("Error", f"Invalid input: {value} must be an integer")
            return 0

    def _onPress(self):
        rows = self._convertToInt(self.rows_entry.get())
        cols = self._convertToInt(self.cols_entry.get())
        cell_size = self._convertToInt(self.cell_size_entry.get())

        search_map = {
            'BFS': 'bfs',
            'DFS': 'dfs',
            'Iterative Deepning DLS': 'cus1',
            'Greedy Best-First Search': 'gbfs',
            'A*': 'as',
            'Weighted A*': 'cus2'
        }

        search_type = search_map.get(self.searchType.get())

        if not search_type:
            messagebox.showerror("Error", "Please select a search type.")
            return

        if rows < 2 or cols < 2 or rows > 30 or cols > 30:
            messagebox.showerror("Error", "Rows and columns must be in range [2, 30].")
        else:
            UIVisualize(rows, cols, search_type, cell_size).mainloop()