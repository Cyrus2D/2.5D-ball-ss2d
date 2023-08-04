from config import Config
from vector import Vector


class Line:
    def __init__(self, start: Vector, end: Vector) -> None:
        self.start = start
        self.end = end
        
        # ax + by + c = 0
        self.a = start.z - end.z
        self.b = end.x - start.x
        self.c = -self.a*start.x - self.b*start.z
    
    def __repr__(self) -> str:
        return f'{self.start} {self.end} ({self.a}, {self.b}, {self.c})'
    
    def intersection(self, other) -> Vector:
        tmp = self.a * other.b - self.b * other.a
        if abs(tmp) < Config.epsilon:
            return None
        intersection_pos = Vector(
            (self.b * other.c - other.b * self.c) / tmp,
            (other.a * self.c - self.a * other.c) / tmp)
        if self.min_x() - Config.epsilon <= intersection_pos.x <= self.max_x() + Config.epsilon \
            and other.min_x() - Config.epsilon <= intersection_pos.x <= other.max_x() + Config.epsilon \
            and self.min_z() - Config.epsilon <= intersection_pos.z <= self.max_z() + Config.epsilon \
            and other.min_z() - Config.epsilon <= intersection_pos.z <= other.max_z() + Config.epsilon:
            return intersection_pos
        return None
    
    def min_x(self):
        return min(self.start.x, self.end.x)
    
    def max_x(self):
        return max(self.start.x, self.end.x)
    
    def min_z(self):
        return min(self.start.z, self.end.z)
    
    def max_z(self):
        return max(self.start.z, self.end.z)
