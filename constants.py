# WIDTH, HEIGHT = 800, 600
WIDTH, HEIGHT = 1280, 720
PLAYER = 60
GRASS = 64
TREE = 64
SMALL_STONE = 22

#ANIMACIONES
CUADROS_BASICOS = 6
IDLE_DOWN = 0
IDLE_RIGHT = 1
IDLE_UP = 2
WALK_DOWN = 3
WALK_RIGHT = 4
WALK_UP = 5
FRAME_SIZE = 32
ANIMATION_DELAY = 100
RUNNING_ANIMATION_DELAY = 50

# Velocidad del personaje
PLAYER_SPEED = 3  # Píxeles por frame (reducido de 5)

# Colores

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
GRAY = (128, 128, 128)
BROWN = (165, 42, 42)
CYAN = (0, 255, 255)

# Barras de estado
MAX_ENERGY = 100
MAX_FOOD = 100
MAX_THIRST = 100
MAX_STAMINA = 100

# Colores para las barras de etado
ENERGY_COLOR = (255, 255, 0) # Amarillo
FOOD_COLOR = (255, 165, 0) # Naranja
THIRST_COLOR = (0, 191, 255) # Azul
STAMINA_COLOR = (124,252,98) # Verde
BAR_BACKGROUND = (100, 100, 100) # Gris oscuro

# Intervalo de tiempo
STATUS_UPDATE_INTERVAL = 1000

# Sistema de dia/noche
DAY_LENGTH = 2400000 # Duracion del dia
DAWN_TIME = 600000 # Tiempo de amanecer
MORNING_TIME = 800000 # Tiempo de mañana
DUSK_TIME = 180000 # Tiempo de atardecer
MIDNIGHT_TIME = 2400000 # Tiempo de medianoche
MAX_DARKNESS = 210 # Nivel de oscuridad maximo

#Para acelerar el dia sacarle un 0 al final de los tiempos

# Colores para iluminacion
NIGHT_COLOR = (20, 20, 50) # Color azul oscuro para la noche
DAY_COLOR = (255, 255, 255) # Color blanco para el dia
DAWN_DUSK_COLOR = (255, 193, 137) # Color anranjado para amanecer y atardecer

# Velocidades de disminuacion de estados
FOOD_DECREASE_RATE = 0.01 # Velocidad de disminucion de la comida
THIRST_DECREASE_RATE = 0.02 # Velocidad de disminucion del sed
ENERGY_DECREASE_RATE = 0.005 # Velocidad de disminucion de la energia en estado critico
ENERGY_INCREASE_RATE = 0.001 # Velocidad de aumento de la energia en estado normal
MOVEMENT_ENERGY_COST = 0.001 # Costo de energia por movimiento

# Nuevas constantes para correr
WALK_SPEED = 5
RUN_SPEED = 8
STAMINA_DECREASE_RATE = 0.05
STAMINA_INCREASE_RATE = 0.02
RUN_FOOD_DECREASE_MULTIPLIER = 2.0
RUN_THIRST_DECREASE_MULTIPLIER = 2.0

# Iventory constants
SLOT_SIZE = 64
HOTBAR_SLOTS = 8
IVENTORY_ROWS = 4
IVENTORY_COLS = 5
MARGIN = 10

# Hotbar position (siempre visible abajo)
HOTBAR_Y = HEIGHT - SLOT_SIZE - MARGIN
HOTBAR_X = (WIDTH - (SLOT_SIZE * HOTBAR_SLOTS)) // 2

# Main inventory position (en el centro cuando esta abierto)
INVENTORY_X = (WIDTH - (SLOT_SIZE * IVENTORY_COLS)) // 2
INVENTORY_Y = (HEIGHT - (SLOT_SIZE * IVENTORY_ROWS)) // 2

# Color for inventory
SLOT_COLOR = (139, 139, 139)
SLOT_BORDER = (100, 100, 100)
SLOT_HOVER = (160, 160, 160)