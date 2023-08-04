from config import Config
from vector import Vector

def equation_solver(g, v, h):
    t1 = (-v + (v**2 + 2*g*h)**0.5) / g
    t2 = (-v - (v**2 + 2*g*h)**0.5) / g
    return t1, t2

def move_equation(a, v, delta_t):
    delta_x = 0.5*a*delta_t**2 + v*delta_t
    return delta_x

class Ball:
    def __init__(self, pos: Vector = None, vel: Vector = None) -> None:
        self.pos: Vector = pos
        self.vel: Vector = vel
        self.size = Config.ball_size
    
    def step(self) -> tuple[Vector, Vector]:
        new_pos = self.pos + self.vel
        collision_pos = None
        
        if new_pos.under_ground():
            # 1/2gt2 + vt - h = 0
            g = -Config.gravity.z
            v = -self.vel.z
            h = self.pos.z
            
            t = equation_solver(g, v, h)
            print(t)
            t = max(t)
            
            # Before ground collision
            current_a = self.vel*Config.ball_air_decay - self.vel
            new_pos = self.pos.copy()
            new_pos.x += move_equation(current_a.x, self.vel.x, t)
            new_pos.z = 0.
            
            collision_pos = new_pos.copy()
            
            self.vel.z += Config.gravity.z * t
            self.vel.z *= -1
            self.vel.x += current_a.x*t 
            # self.vel *= Config.ball_energy_loss_ground_collide 
            
            # After ground collision
            t = (1-t)
            new_pos.x += move_equation(current_a.x, self.vel.x, t)
            new_pos.z = move_equation(Config.gravity.z, self.vel.z, t)
        
        self.pos = new_pos
        self.vel += Config.gravity
        self.vel *= Config.ball_air_decay
        
        return self.pos, collision_pos
    
    def ground_collision(self, new_pos: Vector = None):
        if new_pos is not None:
            return new_pos.z - 0 < self.size
        return self.pos.z - 0 < self.size
    
def equation_solver_linear(v, h):
    t = h/v # v = x/t
    return t

def move_equation_linear(v, delta_t):
    delta_x = v*delta_t
    return delta_x

class BallLinearStep(Ball):
    def on_ground(self, new_pos):
        return new_pos.z < 0.1 and abs(self.vel.z) < 0.2
    
    def step(self):
        new_pos = self.pos + self.vel
        collision_pos = None
        
        if self.ground_collision(new_pos) and not self.on_ground(self.pos):
            # 1/2gt2 + vt - h = 0
            g = -Config.gravity.z
            v = -self.vel.z
            h = self.pos.z - Config.ball_size
            
            t = equation_solver_linear(v, h)
            print(t)
            
            # Before ground collision
            new_pos = self.pos.copy()
            new_pos.x += move_equation_linear(self.vel.x, t)
            new_pos.z = self.size
            
            collision_pos = new_pos.copy()
            
            self.vel.z *= -1
            self.vel.z *= Config.ball_energy_loss_ground_collide 
            
            # After ground collision
            t = (1-t)
            new_pos.x += move_equation_linear(self.vel.x, t)
            new_pos.z = move_equation_linear(self.vel.z, t)
            
            print(new_pos, self.vel)
        
        self.pos = new_pos
        if not self.on_ground(new_pos):
            self.vel += Config.gravity
        else:
            self.vel.z = 0
            self.pos.z = self.size
        self.vel *= Config.ball_air_decay
        
        return self.pos, collision_pos
