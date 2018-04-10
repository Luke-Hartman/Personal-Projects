PLAYER_RADIUS = 80
PLAYER_MASS = 100
PLAYER_COLORS = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0)] # Blue red green yellow
PLAYER_STARTS = [(200, 200), (200, 1080 - 200), (1920 - 200, 200), (1920 - 200, 1080 - 200)]
PLAYER_COOLDOWN = 0.2

PROJECTILE_RADIUS = 35
PROJECTILE_MASS = 15
PROJECTILE_VELOCITY = 2000

SHAKE_FREQUENCY = 25
SHAKE_OCTAVES = 2
MAX_SHAKE_ANGLE = 5
MAX_SHAKE_DISTANCE = 50
# Trauma from (0-1)^SHAKE_POW determines screen shake
SHAKE_EXPONENT = 2
# Trauma decreases at this rate per second
TRAUMA_DECAY_RATE = 4
# Higher means larger traumas
TRAUMA_MUL = 0.6

KICK_DISTANCE = 100
# Kick decreases exponentially at this rate
KICK_DECAY_RATE = 10

HIT_SOUND = 'sounds/collision.wav'
SHOOT_SOUND = 'sounds/fire.wav'
BACKGROUND_MUSIC = 'sounds/Final_Fantasy_VII_Chocobo_Theme.wav'

FLASH_COLOR = (255,255,148)

''' SURVIVAL MODE CONFIGS '''

DIFFICULTY_RATE = 0.03

DENSITY = 1/100 # Mass is DENSITY*R**2 (Ignoring PI)
MIN_RADIUS = 35
BASE_RADIUS = 70

MIN_MOMENTUM = 50000
BASE_MOMENTUM = 80000

BASE_DELAY = 0.5
