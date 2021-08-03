import pygame

Vector2 = pygame.math.Vector2


class Box:
    SIZE = 10

    def __init__(self, left, top, box_tracker, box_lives=1):
        self.color = (255, 255, 255)
        self.top_left = Vector2(left, top)
        self.box_lives = box_lives
        box_tracker.append(self)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.top_left, Vector2(self.SIZE, self.SIZE)))

    def collision(self, pinball, box_tracker):
        # TODO: RUN ALL TESTS. if only runs the first true statement
        if pinball.is_collide(self.top_left.x, self.top_left.x + self.SIZE, self.top_left.y, 0) or \
                pinball.is_collide(self.top_left.x, self.top_left.x + self.SIZE, self.top_left.y + self.SIZE, 0) or \
                pinball.is_collide(self.top_left.y, self.top_left.y + self.SIZE, self.top_left.x, 1) or \
                pinball.is_collide(self.top_left.y, self.top_left.y + self.SIZE, self.top_left.x + self.SIZE, 1):
            self.reduce_life(box_tracker)

    def reduce_life(self, box_tracker):
        self.box_lives -= 1
        if self.box_lives <= 0:
            box_tracker.remove(self)


class Wall(Box):

    def __init__(self, left, top, box_tracker, box_lives=1):
        super().__init__(left, top, box_tracker, box_lives)
        self.color = (128, 128, 128)

    def reduce_life(self, box_tracker):
        pass
