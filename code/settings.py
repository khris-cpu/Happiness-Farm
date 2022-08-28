from pygame.math import Vector2

## Screen

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64

## Overlay Position

OVERLAY_POSITIONS = {
    'tool' : (40, SCREEN_HEIGHT - 15),
    'seed' : (70, SCREEN_HEIGHT - 5)
}

PLAYER_TOOL_OFFSET = {
    'left' : Vector2(-50,40),
    'right' : Vector2(50,40),
    'up' : Vector2(0,-10),
    'down' : Vector2(0,50)
}

LAYERS = {
    'water' : 0,
    'ground' : 1,
    'soil' : 2,
    'soil water' : 3,
    'rain floor' : 4,
    'house bottom' : 5,
    'ground plant' : 6,
    'main' : 7,
    'house top' : 8,
    'fruit' : 9,
    'rain drops' : 10
}

APPLE_POS = {
    'Small' : [(18,17), (30,37) , (12,50) , (30,45) , (20,30) , (30,10)],
    'Large' : [(30,24), (60,65) , (50,50) , (16,40) , (45,50) , (42,70)]
}

GROW_SPEED = {
    "rice" : 1,
    "tomato" : 0.7,
    "cabbage" : 0.9,
    'beatroot' : 1.7,
    'cauliflower' : 0.5,
    'cucumber' : 0.7,
    'eggplant' : 0.8,
    'flower' : 0.4,
    'radish' : 0.5,
    'carrot' : 0.5,
    'pumkin' : 1.2,
    'purple cauliflower' : 0.9
}

SALE_PRICES = {
    'wood' : 4,
    'apple' : 2,
    'rice' : 10,
    'tomato' : 20,
    'cabbage' : 12,
    'beatroot' : 40,
    'cauliflower' : 8,
    'cucumber' : 10,
    'eggplant' : 12,
    'flower' : 5,
    'radish' : 16,
    'carrot' : 13,
    'pumkin' : 20,
    'purple cauliflower' : 21
}
PURCHASE_PRICES = {
    'rice' : 4,
    'tomato' : 5,
    'cabbage' : 3,
    'beatroot' : 2,
    'cauliflower' : 3,
    'cucumber' : 4,
    'eggplant' : 6,
    'flower' : 1,
    'radish' : 5,
    'carrot' : 5,
    'pumkin' : 10,
    'purple cauliflower' : 11
}
