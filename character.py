import pygame
import constants
import os
from constants import *

class Character:
    def __init__(self, x , y):
        self.x = x
        self.y = y

        # Inventario
        self.inventory = {"wood": 0, "stone": 0}

        # Cargar la hoja de sprites
        image_path = os.path.join("assets", "images", "character", "Player.png")
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()

        # Animacion propiedades
        self.frame_size = FRAME_SIZE
        self.size = constants.PLAYER  # Tamaño para colisiones
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_delay = ANIMATION_DELAY
        self.current_state = IDLE_DOWN
        self.moving = False
        self.facing_left = False

        # Cargar animaciones
        self.animations = self.load_animations()

        # Imágenes de los items
        self.item_images = {
            "wood": self.load_item_image("wood.png"),
            "stone": self.load_item_image("smallStone.png")
        }

        # Barras de estado
        self.energy = constants.MAX_ENERGY
        self.food = constants.MAX_FOOD
        self.thirst = constants.MAX_THIRST

    def load_animations(self):
        animations = {}
        for state in range(6):
            frames = []
            for frame in range(CUADROS_BASICOS):  # 6 frames por animacion
                # Extraer el frame del sprite sheet
                x = frame * self.frame_size
                y = state * self.frame_size
                surface = pygame.Surface((self.frame_size, self.frame_size), pygame.SRCALPHA)
                surface.blit(self.sprite_sheet, (0, 0), (x, y, self.frame_size, self.frame_size))
                
                # Escalar si es necesario
                if constants.PLAYER != self.frame_size:
                    surface = pygame.transform.scale(surface, (constants.PLAYER, constants.PLAYER))
                
                frames.append(surface)
            animations[state] = frames
        return animations

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > self.animation_delay:
            self.animation_timer = current_time
            self.animation_frame = (self.animation_frame + 1) % 6


    def load_item_image(self, filename):
        path = os.path.join("assets", "images", "objects", filename)
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (40, 40))


    def draw(self, screen):
        current_frame = self.animations[self.current_state][self.animation_frame]
        if self.facing_left:
            current_frame = pygame.transform.flip(current_frame, True, False)
        screen.blit(current_frame, (self.x, self.y))
        self.draw_status_bars(screen)

    def move(self, dx, dy, world):
        self.moving = dx != 0 or dy != 0

        if self.moving:
            if dy > 0:
                self.current_state = WALK_DOWN
                self.facing_left = False
            elif dy < 0:
                self.current_state = WALK_UP
                self.facing_left = False
            elif dx > 0:
                self.current_state = WALK_RIGHT
                self.facing_left = False
            elif dx < 0:
                self.current_state = WALK_RIGHT
                self.facing_left = True
        else:
            if self.current_state == WALK_DOWN:
                self.current_state = IDLE_DOWN
            elif self.current_state == WALK_UP:
                self.current_state = IDLE_UP
            elif self.current_state == WALK_RIGHT:
                self.current_state = IDLE_RIGHT

        new_x = self.x + dx
        new_y = self.y + dy

        for tree in world.trees:
            if self.check_collision(new_x, new_y, tree):
                self.moving = False
                return

        self.x = new_x
        self.y = new_y

        self.update_animation() 
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