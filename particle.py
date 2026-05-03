import random

from raylib import *
from pyray import *
from settings import *

class Particle:
    def __init__(self, position):
        self.position = position
        self.acceleration = Vector2(0, -0.2)
        self.velocity = Vector2(random.uniform(-30, 30), random.uniform(-30, -10))
        self.color = Color(random.randint(200, 255), random.randint(100, 150), random.randint(50, 100), 255, 255)
        self.radius =  PARTICLE_SIZE 
    def update(self, delta_time):
        self.velocity = Vector2Add(self.velocity, self.acceleration)
        self.position = Vector2Add(self.position, Vector2(self.velocity.x * delta_time, self.velocity.y * delta_time))
        self.color.a = max(0, self.color.a - 5)
        if GetRandomValue(0, 100) < 10:
            self.radius -= 1
        
    def draw(self):
        DrawCircle(int(self.position.x), int(self.position.y), self.radius, self.color)
        
class System:
        def __init__(self, position):
            self.particles = []
            for i in range(MAX_PARTICLES):
                new_position = Vector2(position.x + random.uniform(-5, 5), position.y + random.uniform(-20, -10))
                self.particles.append(Particle(new_position))
        def update(self, position, delta_time):
            for i in range(len(self.particles)-1, -1, -1):
                particle = self.particles[i]
                particle.update(delta_time)
                if particle.color.a <= 0 or particle.radius <= 0:
                    self.particles.pop(i)
                if len(self.particles) < MAX_PARTICLES:
                    new_position = Vector2(position.x + random.uniform(-5, 5), position.y + random.uniform(-4, 2))
                    self.particles.append(Particle(new_position))
        def draw(self):
            for particle in self.particles:
                particle.draw()
            