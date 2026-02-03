import pygame
import constants
import os

class InventoryItem:
    def __init__(self, name, image_path, quantity=1):
        self.name = name
        self.quantity = quantity
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (constants.SLOT.SIZE - 10, constans.SLOT.SIZE - 10))
        self.dragging = False
        self.drag_offset = (0, 0)

    class Iventory:
        def __init__(self):
            self.hotbar = [None] * constants.HOTBAR_SLOTS
            self.inventory = [[None for _ in range(constants.IVENTORY_COLS)] for _ in range(constants.INVENTORY_ROWS )]
            self.dragged_item = None
            self.font = pygame.font.Font(None, 24)

            # Cargar imagenes de los items
            self.item_images = {
                'wood': os.path.join("assets", "images", "objects", "wood.png"),
                'stone': os.path.join("assets", "images", "objects", "smallStone.png")
            }

        def add_item(self, item_name, quantity=1):
            # Primero intentar apilar en el hotbar
            for i, slot in enumarate(self.hotbar):
                if slot and slot.name == item_name:
                    slot.quantity += quantity
                    return true
