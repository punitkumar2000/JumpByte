"""Lightweight particle bursts for pickups, stomps, and damage feedback."""

import math
import random

import pygame


class Particle:
    def __init__(self, x, y, color, angle, speed, lifetime, radius):
        self.x = float(x)
        self.y = float(y)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color
        self.lifetime = lifetime
        self.age = 0.0
        self.radius = radius

    def update(self, dt):
        self.age += dt
        self.vy += 250 * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, surface):
        fade = max(0.0, 1.0 - self.age / self.lifetime)
        color = tuple(int(channel * fade) for channel in self.color)
        radius = max(1, round(self.radius * fade))
        pygame.draw.circle(surface, color, (round(self.x), round(self.y)), radius)


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def burst(self, x, y, color, count=12, speed=150):
        for _ in range(count):
            angle = random.uniform(0, math.tau)
            particle_speed = random.uniform(speed * 0.35, speed)
            lifetime = random.uniform(0.28, 0.62)
            radius = random.randint(2, 4)
            self.particles.append(
                Particle(x, y, color, angle, particle_speed, lifetime, radius)
            )

    def update(self, dt):
        for particle in self.particles:
            particle.update(dt)
        self.particles = [
            particle for particle in self.particles
            if particle.age < particle.lifetime
        ]

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)
