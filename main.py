import pygame

pygame.init()
Vector2 = pygame.math.Vector2

WIDTH, HEIGHT = 500, 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pinball")

FPS = 60


class Baffle:
    VEL = 5

    def __init__(self):
        self.top_left = Vector2(230, 400)
        self.dim = Vector2(60, 10)
        self.color = WHITE

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.top_left, self.dim))

    def move_left(self):
        if self.top_left.x > 0:
            self.top_left.x -= Baffle.VEL

    def move_right(self):
        if self.top_left.x + self.dim.x < WIDTH:
            self.top_left.x += Baffle.VEL

    def collision(self, pinball):
        if pinball.is_collide(self.top_left.x, self.top_left.x + self.dim.x, self.top_left.y, 0):
            hit_point = pinball.center.x + pinball.max_t * pinball.direction.x * pinball.VEL
            pinball.direction_fixed.x = (hit_point - self.top_left.x) / self.dim.x - 0.5


class Pinball:
    tracker = []
    RADIUS = 5
    VEL = 5

    def __init__(self, x, y, mx, my):
        self.color = WHITE
        self.center = Vector2(x, y)
        self.direction = Vector2(mx, my)

        Pinball.tracker.append(self)

        self.max_t = None
        self.center_fixed = None
        self.direction_fixed = None

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.center, self.RADIUS)

    def move(self, baffle):
        self.max_t = 1
        self.center_fixed = self.center + self.direction * self.VEL
        self.direction_fixed = self.direction

        for box in Box.tracker:
            box.collision(self)

        baffle.collision(self)

        self.center = self.center_fixed
        self.direction = self.direction_fixed

        if self.center.x < self.RADIUS:
            self.center.x, self.direction.x = self.RADIUS, -self.direction.x
        if self.center.x > WIDTH - self.RADIUS:
            self.center.x, self.direction.x = WIDTH - self.RADIUS, -self.direction.x
        if self.center.y < self.RADIUS:
            self.center.y, self.direction.y = self.RADIUS, -self.direction.y
        if self.center.y > HEIGHT:
            Pinball.tracker.remove(self)

    def is_collide(self, p1, p2, q, axis):
        if axis == 0:
            if not self.direction.y or not self.VEL:
                return False
            t = (q - self.center.y - self.RADIUS) / self.direction.y / self.VEL
            if 0 < t <= self.max_t and p1 <= self.center.x + t * self.direction.x * self.VEL <= p2:
                self.max_t = t
                self.direction_fixed = Vector2(self.direction.x, -self.direction.y)
                self.center_fixed = self.center + t * self.direction * self.VEL + (1 - t) * self.direction_fixed * self.VEL
                return True
        if axis == 1:
            if not self.direction.x or not self.VEL:
                return False
            t = (q - self.center.x - self.RADIUS) / self.direction.x / self.VEL
            if 0 < t <= self.max_t and p1 <= self.center.y + t * self.direction.y * self.VEL <= p2:
                self.max_t = t
                self.direction_fixed = Vector2(-self.direction.x, self.direction.y)
                self.center_fixed = self.center + t * self.direction * self.VEL + (1 - t) * self.direction_fixed * self.VEL
                return True


class Box:
    tracker = []
    SIZE = 10

    def __init__(self, left, top, num=1):
        self.color = WHITE
        self.top_left = Vector2(left, top)
        self.num = num
        Box.tracker.append(self)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.top_left, Vector2(self.SIZE, self.SIZE)))

    def collision(self, pinball):
        if pinball.is_collide(self.top_left.x, self.top_left.x + self.SIZE, self.top_left.y, 0) or \
                pinball.is_collide(self.top_left.x, self.top_left.x + self.SIZE, self.top_left.y + self.SIZE, 0) or \
                pinball.is_collide(self.top_left.y, self.top_left.y + self.SIZE, self.top_left.x, 1) or \
                pinball.is_collide(self.top_left.y, self.top_left.y + self.SIZE, self.top_left.x + self.SIZE, 1):
            self.num -= 1
            if self.num <= 0:
                Box.tracker.remove(self)


def get_a_bunch_of_boxes_and_a_pinball():
    for i in range(10):
        for j in range(5):
            Box(200 + i * (Box.SIZE + 1), 100 + j * (Box.SIZE + 1))
    Pinball(300, 30, 0, 0)


def get_a_bunch_of_cooler_boxes_and_pinballs():
    for i in range(45):
        for j in range(5):
            Box(i * (Box.SIZE + 1), j * (Box.SIZE + 1))
    for i in range(8):
        for j in range(20):
            Box(i * (Box.SIZE + 1), 55 + j * (Box.SIZE + 1))
            Box(407 + i * (Box.SIZE + 1), 55 + j * (Box.SIZE + 1))
    for i in range(20):
        for j in range(12):
            Box(135 + i * (Box.SIZE + 1), 130 + j * (Box.SIZE + 1))
    Pinball(100, 100, 0, 1)
    Pinball(400, 100, 0, 1)


def draw_window(baffle):
    WIN.fill(BLACK)
    baffle.draw(WIN)
    for box in Box.tracker:
        box.draw(WIN)
    for pinball in Pinball.tracker:
        pinball.draw(WIN)
    pygame.display.update()


def main():
    clock = pygame.time.Clock()

    baffle = Baffle()
    #get_a_bunch_of_boxes_and_a_pinball()
    get_a_bunch_of_cooler_boxes_and_pinballs()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
            baffle.move_left()
        if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
            baffle.move_right()

        for pinball in Pinball.tracker:
            pinball.move(baffle)

        if not Pinball.tracker:
            run = False

        draw_window(baffle)

    pygame.quit()


if __name__ == "__main__":
    main()
