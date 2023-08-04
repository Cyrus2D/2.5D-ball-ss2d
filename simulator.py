from ball import Ball
from config import Config
from line import Line
from player import Player
from vector import Vector

import matplotlib.pyplot as plt
import numpy as np


class SimulatorBallOnly:
    def __init__(self) -> None:
        self.ball: Ball = None
        self.n_steps = 40
        self.ball_course: list[list[float]] = []
    
    def simulate(self):
        self.ball_course.append(self.ball.pos.to_list() + [+1])
        
        for step in range(self.n_steps):
            new_pos, collision_pos = self.ball.step()
            if collision_pos:
                self.ball_course.append(collision_pos.to_list() + [-1])
            self.ball_course.append(new_pos.to_list() + [+1])
            # print(self.ball.pos, self.ball.vel)
        
        return self.ball_course

    def visualize(self, draw_line=False, show=True, save=False):
        if len(self.ball_course) == 0:
            self.simulate()
            
        data = np.array(self.ball_course)
        data_air = data[data[:, 2] > 0]
        data_collision = data[data[:, 2] < 0]
        
        plt.scatter(data_air[:, 0], data_air[:, 1], c='b')
        plt.scatter(data_collision[:, 0], data_collision[:, 1], c='r')
        if draw_line:
            plt.plot(data_air[:, 0], data_air[:, 1], c='blue')
            plt.plot(data[:, 0], data[:, 1], c='red')
        plt.xlabel('X')
        plt.ylabel('Z')
        if show:
            plt.show()
        if save:
            plt.savefig('simulation', dpi=300)
        
class SimulateSimpleBallShot(SimulatorBallOnly):
    def __init__(self, BALL_OBJ) -> None:
        super().__init__()
        self.ball = BALL_OBJ(Vector(0,1), Vector(2,1))
        # self.n_steps = 10
        
class SimulatorBallAndPlayer(SimulatorBallOnly):
    def __init__(self) -> None:
        super().__init__()
        self.player: Player = None
    
    def simulate(self):
        self.ball_course.append(self.ball.pos.to_list() + [+1])
        
        for step in range(self.n_steps):
            new_pos, collision_pos = self.ball.step()
            if collision_pos is not None:
                self.ball_course.append(collision_pos.to_list() + [-1])
                
            collision_pos = self.check_collision()
            if collision_pos is not None:
                print(f'# COLLISION {self.ball.pos} {collision_pos}')
                self.ball_course.append(collision_pos.to_list() + [-1])
            
            self.ball_course.append(self.ball.pos.to_list() + [+1])
            # print(self.ball.pos, self.ball.vel)
        
        return self.ball_course
    
    def check_collision(self) -> Vector:
        last_ball_pos = Vector(self.ball_course[-1][0], self.ball_course[-1][1])
        ball_path = Line(self.ball.pos, last_ball_pos)
        
        players_body_lines = self.player.get_lines()
        collision_pos = None
        for line in players_body_lines:
            intersection_pos = ball_path.intersection(line)
            if intersection_pos is not None:
                if collision_pos is None:
                    collision_pos = intersection_pos
                elif intersection_pos.dist(last_ball_pos) < collision_pos.dist(last_ball_pos):
                    collision_pos = intersection_pos
        if collision_pos is not None:
            self.ball.vel.x *= -0.1
            self.ball.vel.z *= 0.1
            self.ball.pos = collision_pos.copy()
            self.ball.pos.x -= 0.1
        return collision_pos
        
    def visualize(self, draw_line=False, show=True, save=False):
        super().visualize(draw_line, False)
        player_vertices = self.player.get_vertices()
        player_vertices.append(player_vertices[0])
        data = []
        for pos in player_vertices:
            data.append(pos.to_list())
        data = np.array(data)
        print(data)
        
        plt.scatter(data[:, 0], data[:, 1], c='g')
        plt.plot(data[:, 0], data[:, 1], c='g')
        if show:
            plt.show()
        if save:
            plt.savefig('simulation', dpi=300)
            
class SimulateSimpleBallPlayerCollision(SimulatorBallAndPlayer):
    def __init__(self, ball, player) -> None:
        super().__init__()
        self.ball = ball
        self.player = player
        self.n_steps=20