import pygame
import constants
from elements import Tree, SmallStone
import random
import os
from pygame import Surface

class WorldChunk: 
    # Representa un segmento del mundo con sus elementos
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        #Creamos una semilla basada en las coordenadas del chunk
        chunk_seed = hash(f"{x}_{y}")
        old_state = random.getstate()
        random.seed(chunk_seed)

        # Generamos elementos dle chunk (arboles)
        self.trees = [
            Tree(
                self.x + random.randint(0, width-constants.TREE),
                self.y + random.randint(0, height-constants.TREE)
            ) for _ in range(5)
        ]

        # Generamos elementos del chunk (piedras pequeñas)
        self.small_stones = [
            SmallStone(
                self.x + random.randint(0, width-constants.SMALL_STONE),
                self.y + random.randint(0, height-constants.SMALL_STONE)
            ) for _ in range(10)
        ]

        # Restauramos el estado anterior del generador de numeros aleatorios
        random.setstate(old_state)

    def draw(self, screen, grass_image, camera_x, camera_y):
        # Dibujar el pasto en este chunk con offset de camara
        # Calcular el rango de tiles de pasto visibles con un tile extra para evitar lineas
        start_x = max(0, (camera_x - self.x) // constants.GRASS - 1)
        end_x = min(self.width // constants.GRASS + 1,
                    (camera_x + constants.WIDTH - self.x) // constants.GRASS + 2)
        start_y = max(0, (camera_y - self.y) // constants.GRASS - 1)
        end_y = min(self.height // constants.GRASS + 1,
                    (camera_y + constants.HEIGHT - self.y) // constants.GRASS + 2)

        for y in range(int(start_y), int(end_y)):
            for x in range(int(start_x), int(end_x)):
                screen_x = self.x + x * constants.GRASS - camera_x
                screen_y = self.y + y * constants.GRASS - camera_y
                screen.blit(grass_image, (screen_x, screen_y))

        # Remover elementos agotados
        self.trees = [tree for tree in self.trees if not tree.is_depleted()]
        self.small_stones = [stone for stone in self.small_stones if not stone.is_depleted()]
        
        # Dibujar elementos solo si estan en pantalla
        for stone in self.small_stones:
            stone_screen_x = stone.x - camera_x
            stone_screen_y = stone.y - camera_y
            if (stone_screen_x + stone.size >= 0 and stone_screen_x <= constants.WIDTH and
                stone_screen_y + stone.size >= 0 and stone_screen_y <= constants.HEIGHT):
                stone.draw(screen, camera_x, camera_y)

        # Dibujar arboles solo si estan en pantalla
        for tree in self.trees:
            tree_screen_x = tree.x - camera_x
            tree_screen_y = tree.y - camera_y
            if (tree_screen_x + tree.size >= 0 and tree_screen_x <= constants.WIDTH and
                tree_screen_y + tree.size >= 0 and tree_screen_y <= constants.HEIGHT):
                tree.draw(screen, camera_x, camera_y)

class World: 
    def __init__(self, width, height):

        self.chunk_size = constants.WIDTH
        self.active_chunks = {}


        self.view_width = width
        self.view_height = height
        

        grass_path = os.path.join("assets", "images", "objects", "grass.png")
        self.grass = pygame.image.load(grass_path).convert()
        self.grass = pygame.transform.scale(self.grass, (constants.GRASS, constants.GRASS))

        # Sistema dia/noche
        self.current_time = constants.MORNING_TIME
        self.day_overlay = Surface((width, height))
        self.day_overlay.fill(constants.DAY_COLOR)
        self.day_overlay.set_alpha(0)

        # Generar el chunk inicial y adyacentes
        self.generate_chunk(0, 0)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                    self.generate_chunk(dx, dy)

    def get_chunk_key(self, x, y):
        # Obtiene la llave del chunk basada en las coordenadas globales
        chunk_x = x // self.chunk_size
        chunk_y = y // self.chunk_size
        return (chunk_x, chunk_y)

    def generate_chunk(self, chunk_x, chunk_y):
        # Generamos un nuevo chunk en las coordenadas especificas
        key = (chunk_x, chunk_y)
        if key not in self.active_chunks:
            x = chunk_x * self.chunk_size
            y = chunk_y * self.chunk_size
            self.active_chunks[key] = WorldChunk(x, y, self.chunk_size, self.chunk_size)

    def update_chunks(self, player_x, player_y):
        # Actualiza los chunks basado en la posicion del jugador
        current_chunk = self.get_chunk_key(player_x, player_y)

        # Generar chunks adyacentes (para no ver las lineas negras)
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                chunk_x = current_chunk[0] + dx
                chunk_y = current_chunk[1] + dy
                self.generate_chunk(chunk_x, chunk_y)

        # Eliminar chunks lejanos
        chunks_to_remove = []
        for chunk_key in self.active_chunks:
            distance_x = abs(chunk_key[0] - current_chunk[0])
            distance_y = abs(chunk_key[1] - current_chunk[1])
            if distance_x > 2 or distance_y > 2:
                chunks_to_remove.append(chunk_key)

        for chunk_key in chunks_to_remove:
            del self.active_chunks[chunk_key]


    def update_time(self, dt):
        self.current_time = (self.current_time + dt) % constants.DAY_LENGTH
        alpha = 0
        # Calcular el color y la intensidad basado en la hora del dia
        if constants.MORNING_TIME <= self.current_time < constants.DUSK_TIME:
            # Durante el dia (8:00 - 18:00)
            self.day_overlay.fill(constants.DAY_COLOR)
            alpha = 0
        elif constants.DAWN_TIME <= self.current_time < constants.MORNING_TIME:
            # Entre 6:00 y 8:00 - Amanecer
            self.day_overlay.fill(constants.NIGHT_COLOR)
            morning_progress = (self.current_time - constants.DAWN_TIME) / (constants.MORNING_TIME - constants.DAWN_TIME)
            alpha = int(constants.MAX_DARKNESS * (1 - morning_progress))
        elif constants.DUSK_TIME <= self.current_time < constants.MIDNIGHT_TIME:
            # Entre 18:00 y 00:00 - Atardecer
            self.day_overlay.fill(constants.NIGHT_COLOR)
            night_progress = (self.current_time - constants.DUSK_TIME) / (constants.MIDNIGHT_TIME - constants.DUSK_TIME)
            alpha = int(constants.MAX_DARKNESS * night_progress)
        else: 
            # Entre 00:00 y 6:00 - Medianoche
            self.day_overlay.fill(constants.NIGHT_COLOR)
            alpha = constants.MAX_DARKNESS

        self.day_overlay.set_alpha(alpha)


    def draw(self, screen, camera_x, camera_y):
        # Dibujar todos los chunks activos con offset de camara
        for chunk in self.active_chunks.values():
            chunk.draw(screen, self.grass, camera_x, camera_y)

        # Aplicar el overlay dia/noche
        screen.blit(self.day_overlay, (0, 0))

    def draw_inventory(self, screen, character):
        font = pygame.font.Font(None, 36)
        instruction_text = font.render("Press 'I' to open inventory", True, constants.WHITE)
        screen.blit(instruction_text, (10, 10))


    @property
    def trees(self):
        # Retorna todos los arboles de todos los chunks activos
        all_trees = []
        for chunk in self.active_chunks.values():
            all_trees.extend(chunk.trees)
        return all_trees

    @property
    def small_stones(self):
        # Retorna todas las piedras pequeñas de todos los chunks activos
        all_stones = []
        for chunk in self.active_chunks.values():
            all_stones.extend(chunk.small_stones)
        return all_stones
        