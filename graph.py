"""
Grid graph representation for MAPF.
Supports 4-connected grids (up/down/left/right) plus wait action.
"""


class Grid:
    def __init__(self, width, height, obstacles=None):
        self.width = width
        self.height = height
        self.obstacles = set(obstacles) if obstacles else set()

    def in_bounds(self, v):
        x, y = v
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, v):
        return v not in self.obstacles

    def neighbors(self, v):
        """Return all valid adjacent vertices (4-connected) plus the vertex itself (wait)."""
        x, y = v
        candidates = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x, y)]
        return [n for n in candidates if self.in_bounds(n) and self.passable(n)]

    def vertices(self):
        return [
            (x, y)
            for x in range(self.width)
            for y in range(self.height)
            if self.passable((x, y))
        ]

    @classmethod
    def from_map_string(cls, map_str):
        """
        Parse a simple text map where:
          '.' = free cell
          '@' or '#' = obstacle
          'T' = tree/obstacle (Moving AI format)
        Returns a Grid instance.
        """
        lines = [l for l in map_str.strip().splitlines() if l.strip()]
        # Skip Moving AI header lines (type, height, width, map)
        data_lines = []
        width = None
        height = None
        for line in lines:
            if line.startswith("type"):
                continue
            elif line.startswith("height"):
                height = int(line.split()[1])
            elif line.startswith("width"):
                width = int(line.split()[1])
            elif line.startswith("map"):
                continue
            else:
                data_lines.append(line)

        if width is None:
            width = max(len(l) for l in data_lines)
        if height is None:
            height = len(data_lines)

        obstacles = set()
        for y, line in enumerate(data_lines):
            for x, ch in enumerate(line):
                if ch in ('@', '#', 'T', 'S', 'W'):
                    obstacles.add((x, y))
        return cls(width, height, obstacles)

    @classmethod
    def from_file(cls, path):
        with open(path, 'r') as f:
            return cls.from_map_string(f.read())

    def __repr__(self):
        return f"Grid({self.width}x{self.height}, {len(self.obstacles)} obstacles)"
