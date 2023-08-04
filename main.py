from ball import BallLinearStep
from player import Player
from simulator import SimulateSimpleBallPlayerCollision, SimulateSimpleBallShot
from vector import Vector


course = SimulateSimpleBallPlayerCollision(
        BallLinearStep(Vector(0, 0), Vector(2, 1)),
        Player(Vector(10, 0))
    ).visualize(draw_line=True, show=False, save=True)
