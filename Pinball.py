import math

import pygame

Vector2 = pygame.math.Vector2


class Pinball:
    RADIUS = 5
    VEL = 5

    def __init__(self, x, y, direction_x, direction_y, pinball_tracker):
        self.color = (255, 255, 255)
        self.center = Vector2(x, y)
        self.direction = Vector2(direction_x, direction_y)

        pinball_tracker.append(self)

        self.max_t = None
        self.center_fixed = None
        self.direction_fixed = None

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.center, self.RADIUS)

    def move(self, baffle, box_tracker, width, height, pinball_tracker, remaining_time=1):
        self.max_t = remaining_time
        self.center_fixed = self.center + self.direction * self.VEL
        self.direction_fixed = self.direction

        hit_box = None
        for box in box_tracker:
            if box.is_collide(self):
                hit_box = box
        if hit_box:
            hit_box.reduce_life(box_tracker)

        baffle.collision(self)

        self.center = self.center_fixed
        self.direction = self.direction_fixed

        if self.center.x < self.RADIUS:
            self.center.x, self.direction.x = self.RADIUS, -self.direction.x
        if self.center.x > width - self.RADIUS:
            self.center.x, self.direction.x = width - self.RADIUS, -self.direction.x
        if self.center.y < self.RADIUS:
            self.center.y, self.direction.y = self.RADIUS, -self.direction.y
        if self.center.y > height:
            pinball_tracker.remove(self)

        if self.max_t < remaining_time:
            self.move(baffle, box_tracker, width, height, pinball_tracker, remaining_time - self.max_t)

    def is_collide(self, p1, p2, q, axis):
        if axis == 0:
            if not self.direction.y or not self.VEL:
                return False
            radius_offset = self.RADIUS if self.direction.y > 0 else -self.RADIUS
            t = (q - self.center.y - radius_offset) / self.direction.y / self.VEL
            if 0 < t <= self.max_t and p1 <= self.center.x + t * self.direction.x * self.VEL <= p2:
                self.max_t = t
                self.direction_fixed = Vector2(self.direction.x, -self.direction.y)
                self.center_fixed = self.center + t * self.direction * self.VEL + (
                        1 - t) * self.direction_fixed * self.VEL
                return True
        if axis == 1:
            if not self.direction.x or not self.VEL:
                return False
            radius_offset = self.RADIUS if self.direction.x > 0 else -self.RADIUS
            t = (q - self.center.x - radius_offset) / self.direction.x / self.VEL
            if 0 < t <= self.max_t and p1 <= self.center.y + t * self.direction.y * self.VEL <= p2:
                self.max_t = t
                self.direction_fixed = Vector2(-self.direction.x, self.direction.y)
                self.center_fixed = self.center + t * self.direction * self.VEL + (
                        1 - t) * self.direction_fixed * self.VEL
                return True
        return False
