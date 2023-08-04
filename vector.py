

class Vector:
    def __init__(self, x=0, z=0) -> None:
        self.x = x
        self.z = z
    
    def to_list(self):
        return [self.x, self.z]
    
    def __iadd__(self, other):
        self.x += other.x
        self.z += other.z
        return self
    
    def __imul__(self, other):
        self.x *= other
        self.z *= other
        return self
    
    def __mul__(self, other):
        return Vector(self.x*other, self.z*other)
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.z + other.z)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.z - other.z)
    
    def __repr__(self) -> str:
        return f'({self.x :.2f}, {self.z :.2f})'
    
    def under_ground(self):
        return self.z <= 0.
    
    def copy(self):
        return Vector(self.x, self.z)
    
    def dist(self, other):
        return ((self.x - other.x)**2 + (self.z - other.z)**2)**0.5