import json
from Box import *
from Pinball import *
from Baffle import *


class Game:
    def __init__(self):
        self.baffle = None
        self.pinball_tracker = []
        self.box_tracker = []

        self.gui_init()

        self.loaded = False

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
        if not self.loaded:
            print("Please load scene first")
            return
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

    def load_scene(self, file_path):
        with open(file_path) as f:
            data = json.load(f)
            baffle_info = data["baffle"]
            self.baffle = Baffle(baffle_info["left"], baffle_info["top"],
                                 baffle_info["width"], baffle_info["height"])
            for box in data["boxes"]:
                left = box["left"]
                top = box["top"]
                box_lives = box["lives"] if "lives" in box else 1
                for i in range(box["count_along_x"]):
                    for j in range(box["count_along_y"]):
                        Box(left + i * (Box.SIZE + 1), top + j * (Box.SIZE + 1), self.box_tracker, box_lives)
            for wall in data["walls"]:
                left = wall["left"]
                top = wall["top"]
                box_lives = wall["lives"] if "lives" in wall else 1
                for i in range(wall["count_along_x"]):
                    for j in range(wall["count_along_y"]):
                        Wall(left + i * (Wall.SIZE + 1), top + j * (Wall.SIZE + 1), self.box_tracker, box_lives)
            for pinball in data["pinballs"]:
                Pinball(pinball["center_x"], pinball["center_y"], pinball["direction_x"],
                        pinball["direction_y"], self.pinball_tracker)
            self.loaded = True
