from Box import *
from Pinball import *
from Baffle import *


class Game:
    def __init__(self):
        self.baffle = None
        self.pinball_tracker = []
        self.box_tracker = []

        self.gui_init()
        self.load_scene()

    # GUI Init is part of the Game init. Defining new variables in this method should be OK.
    def gui_init(self):
        pygame.init()
        self.WIDTH = 500
        self.HEIGHT = 500
        self.FPS = 60

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pinball")

        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            self.clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
                self.baffle.move_left(0)
            if key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
                self.baffle.move_right(self.WIDTH)

            for pinball in self.pinball_tracker:
                pinball.move(self.baffle, self.box_tracker, self.WIDTH, self.HEIGHT, self.pinball_tracker)

            if not self.pinball_tracker:
                running = False

            self.draw_window()
        pygame.quit()

    def draw_window(self):
        self.window.fill((0, 0, 0))
        self.baffle.draw(self.window)
        for box in self.box_tracker:
            box.draw(self.window)
        for pinball in self.pinball_tracker:
            pinball.draw(self.window)
        pygame.display.update()

    def load_scene(self):
        for i in range(10):
            for j in range(5):
                Box(200 + i * (Box.SIZE + 1), 100 + j * (Box.SIZE + 1), self.box_tracker)
        Pinball(300, 30, 0, 1, self.pinball_tracker)
        self.baffle = Baffle(220, 400, 60, 10)

    def load_cooler_scene(self):
        for i in range(45):
            for j in range(5):
                Box(i * (Box.SIZE + 1), j * (Box.SIZE + 1), self.box_tracker)
        for i in range(8):
            for j in range(20):
                Box(i * (Box.SIZE + 1), 55 + j * (Box.SIZE + 1), self.box_tracker)
                Box(407 + i * (Box.SIZE + 1), 55 + j * (Box.SIZE + 1), self.box_tracker)
        for i in range(20):
            for j in range(12):
                Box(135 + i * (Box.SIZE + 1), 130 + j * (Box.SIZE + 1), self.box_tracker)
        Pinball(100, 100, 0, 1, self.pinball_tracker)
        Pinball(400, 100, 0, 1, self.pinball_tracker)
