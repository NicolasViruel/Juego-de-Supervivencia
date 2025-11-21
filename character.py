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

        self.item_images = {
            "wood": self.load_item_image("wood.png"),
            "stone": self.load_item_image("smallStone.png")
        }
    
    def load_item_image(self, filename):
        path = os.path.join("assets", "images", "objects", filename)
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (40, 40))


    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, dx, dy, world):
        new_x = self.x + dx
        new_y = self.y + dy

        for tree in world.trees:
            if self.check_collision(new_x, new_y, tree):
                return

        self.x = new_x
        self.y = new_y

    def check_collision(self, x, y, obj):
        return x < obj.x + obj.size*.75 and x + self.size*.75 > obj.x and y < obj.y + obj.size*.75 and y + self.size*.75 > obj.y

    def is_near(self, obj):
        return (abs(self.x - obj.x) <= self.size + obj.size and
                abs(self.y - obj.y) <= self.size + obj.size)

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