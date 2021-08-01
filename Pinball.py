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

    def move(self, baffle, box_tracker, width, height, pinball_tracker):
        self.max_t = 1
        self.center_fixed = self.center + self.direction * self.VEL
        self.direction_fixed = self.direction

        for box in box_tracker:
            box.collision(self, box_tracker)

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

    def is_collide(self, p1, p2, q, axis):
        if axis == 0:
            if not self.direction.y or not self.VEL:
                return False
            t = (q - self.center.y - self.RADIUS) / self.direction.y / self.VEL
            if 0 < t <= self.max_t and p1 <= self.center.x + t * self.direction.x * self.VEL <= p2:
                self.max_t = t
                self.direction_fixed = Vector2(self.direction.x, -self.direction.y)
                self.center_fixed = self.center + t * self.direction * self.VEL + (
                        1 - t) * self.direction_fixed * self.VEL
                # TODO: remember to calculate 2 collision in 1 frame
                return True
        if axis == 1:
            if not self.direction.x or not self.VEL:
                return False
            t = (q - self.center.x - self.RADIUS) / self.direction.x / self.VEL
            if 0 < t <= self.max_t and p1 <= self.center.y + t * self.direction.y * self.VEL <= p2:
                self.max_t = t
                self.direction_fixed = Vector2(-self.direction.x, self.direction.y)
                self.center_fixed = self.center + t * self.direction * self.VEL + (
                        1 - t) * self.direction_fixed * self.VEL
                return True
