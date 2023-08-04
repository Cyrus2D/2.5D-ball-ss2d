from config import Config
from line import Line
from vector import Vector


class Player:
    def __init__(self, pos: Vector = None) -> None:
        self.pos = pos
        self.size = Config.player_size
        self.height = Config.player_height
    
    def get_vertices(self) -> list[Vector]:
        x_offset = Vector(self.size/2, 0)
        z_offset = Vector(0, self.height)
        return [
            self.pos - x_offset,
            self.pos + x_offset,
            self.pos + z_offset + x_offset,
            self.pos + z_offset - x_offset,
        ]
    
    def get_lines(self) -> list[Line]:
        vertices = self.get_vertices()
        vertices.append(vertices[0])

        lines = []
        for i in range(len(vertices) - 1):
            lines.append(Line(vertices[i], vertices[i+1]))
        return lines