WIDTH, HEIGHT = 800, 600
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

# Colores para las barras de etado
ENERGY_COLOR = (255, 255, 0) # Amarillo
FOOD_COLOR = (255, 165, 0) # Naranja
THIRST_COLOR = (0, 191, 255) # Azul
BAR_BACKGROUND = (100, 100, 100) # Gris oscuro

# Intervalo de tiempo
STATUS_UPDATE_INTERVAL = 1000

# Sistema de dia/noche
DAY_LENGTH = 240000 # Duracion del dia
DAWN_TIME = 60000 # Tiempo de amanecer
MORNING_TIME = 80000 # Tiempo de mañana
DUSK_TIME = 180000 # Tiempo de atardecer
MIDNIGHT_TIME = 240000 # Tiempo de medianoche
MAX_DARKNESS = 210 # Nivel de oscuridad maximo

#Para acelerar el dia sacarle un 0 al final de los tiempos

# Colores para iluminacion
NIGHT_COLOR = (20, 20, 50) # Color azul oscuro para la noche
DAY_COLOR = (255, 255, 255) # Color blanco para el dia
DAWN_DUSK_COLOR = (255, 193, 137) # Color anranjado para amanecer y atardecer

