import pygame
import constants
import os

class Character:
    def __init__(self, x , y):
        self.x = x
        self.y = y

        # Inventario
        self.inventory = {"wood": 0, "stone": 0}
        image_path = os.path.join("assets", "images", "character", "character.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.PLAYER, constants.PLAYER))
        self.size = self.image.get_width()

        # Imágenes de los items
        self.item_images = {
            "wood": self.load_item_image("wood.png"),
            "stone": self.load_item_image("smallStone.png")
        }

        # Barras de estado
        self.energy = constants.MAX_ENERGY
        self.food = constants.MAX_FOOD
        self.thirst = constants.MAX_THIRST
    
    def load_item_image(self, filename):
        path = os.path.join("assets", "images", "objects", filename)
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (40, 40))


    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.draw_status_bars(screen)

    def move(self, dx, dy, world):
        new_x = self.x + dx
        new_y = self.y + dy

        for tree in world.trees:
            if self.check_collision(new_x, new_y, tree):
                return

        self.x = new_x
        self.y = new_y
        #Cuando se mueve, pierde energia
        self.update_energy(-0.1)

    def check_collision(self, x, y, obj):
        ratio = 0.6
        cs, os = self.size * ratio, obj.size * ratio
        cx, cy = x + (self.size - cs) / 2, y + (self.size - cs) / 2
        ox, oy = obj.x + (obj.size - os) / 2, obj.y + (obj.size - os) / 2
        return cx < ox + os and cx + cs > ox and cy < oy + os and cy + cs > oy

    def is_near(self, obj, max_distance=10):
        ratio = 0.6
        cs, os = self.size * ratio, obj.size * ratio
        cx = self.x + (self.size - cs) / 2 + cs / 2
        cy = self.y + (self.size - cs) / 2 + cs / 2
        ox = obj.x + (obj.size - os) / 2 + os / 2
        oy = obj.y + (obj.size - os) / 2 + os / 2
        max_allowed = cs / 2 + os / 2 + max_distance
        return abs(cx - ox) <= max_allowed and abs(cy - oy) <= max_allowed

    def interact(self, world):
        for tree in world.trees:
            if self.is_near(tree):
                if tree.chop():
                    self.inventory["wood"] += 1
                    if tree.wood == 0:
                        world.trees.remove(tree)
                return


        for small_stone in world.small_stones:
            if self.is_near(small_stone):
                self.inventory["stone"] += small_stone.stone
                world.small_stones.remove(small_stone)
                return

    def draw_inventory(self, screen):
        background = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)
        background.fill((0, 0, 0, 128))
        screen.blit(background, (0, 0))

        font = pygame.font.Font(None, 36)
        tittle = font.render("Inventory", True, constants.WHITE)
        screen.blit(tittle, (constants.WIDTH // 2 - tittle.get_width() // 2, 20))

        item_font = pygame.font.Font(None, 24)
        y_offset = 80
        for item, quantity in self.inventory.items():
            if quantity > 0:
                screen.blit(self.item_images[item], (constants.WIDTH // 2 - 60, y_offset))
                text = item_font.render(f"{item.capitalize()}: {quantity}", True, constants.WHITE)
                screen.blit(text, (constants.WIDTH // 2 + 10, y_offset + 10))
                y_offset += 60

        close_text = item_font.render("Press 'I' to close", True, constants.WHITE)

        screen.blit(close_text, (constants.WIDTH // 2 - close_text.get_width() // 2, constants.HEIGHT - 40))   

    def update_energy(self, amount):
        self.energy = max(0, min(self.energy + amount, constants.MAX_ENERGY))

    def update_food(self, amount):
        self.food = max(0, min(self.food + amount, constants.MAX_FOOD))

    def update_thirst(self, amount):
        self.thirst = max(0, min(self.thirst + amount, constants.MAX_THIRST))

    def draw_status_bars(self, screen):
        bar_width = 200
        bar_height = 10
        x_offset = 10
        y_offset = 10

        # Energy bar
        pygame.draw.rect(screen, constants.BAR_BACKGROUND, (x_offset, y_offset, bar_width, bar_height))

        pygame.draw.rect(screen, constants.ENERGY_COLOR, (x_offset, y_offset, bar_width * (self.energy / constants.MAX_ENERGY), bar_height))
        
        # Food bar
        y_offset += 15
        pygame.draw.rect(screen, constants.BAR_BACKGROUND, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, constants.FOOD_COLOR, (x_offset, y_offset, bar_width * (self.food / constants.MAX_FOOD), bar_height))

        # Thirst bar
        y_offset += 15
        pygame.draw.rect(screen, constants.BAR_BACKGROUND, (x_offset, y_offset, bar_width, bar_height))
        pygame.draw.rect(screen, constants.THIRST_COLOR, (x_offset, y_offset, bar_width * (self.thirst / constants.MAX_THIRST), bar_height))

    def update_status(self):
        self.update_food(-0.5)
        self.update_thirst(-0.5)

        if self.food < constants.MAX_FOOD * 0.2 or self.thirst < constants.MAX_THIRST * 0.2:
            self.update_energy(-0.1)
        else:
            self.update_energy(0.05)