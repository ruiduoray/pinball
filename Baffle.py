import pygame
Vector2 = pygame.math.Vector2


class Baffle:
    VEL = 5

    def __init__(self, left, top, dim_x, dim_y):
        self.top_left = Vector2(left, top)
        self.dim = Vector2(dim_x, dim_y)
        self.color = (255, 255, 255)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.top_left, self.dim))

    def move_left(self, left_boundary=0):
        if self.top_left.x > Baffle.VEL + left_boundary:
            self.top_left.x -= Baffle.VEL
        else:
            self.top_left.x = left_boundary

    def move_right(self, right_boundary):
        if self.top_left.x + self.dim.x < right_boundary - Baffle.VEL:
            self.top_left.x += Baffle.VEL
        else:
            self.top_left.x = right_boundary - self.dim.x

    def collision(self, pinball):
        # TODO: Add check for side segments
        if pinball.is_collide(self.top_left.x, self.top_left.x + self.dim.x, self.top_left.y, 0):
            hit_point = pinball.center.x + pinball.max_t * pinball.direction.x * pinball.VEL
            pinball.direction_fixed.x = (hit_point - self.top_left.x) / self.dim.x - 0.5
