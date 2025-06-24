import pygame
import random

# Initialize pygame
pygame.init()

# Settings
TILE_SIZE = 32
GRID_WIDTH = 20
GRID_HEIGHT = 15
SCREEN_WIDTH = TILE_SIZE * GRID_WIDTH
SCREEN_HEIGHT = TILE_SIZE * GRID_HEIGHT

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("🪓 Simple Mining Game")
clock = pygame.time.Clock()

# Block types: 0 = sky, 1 = dirt, 2 = stone
BLOCK_COLORS = {
    0: (135, 206, 235),  # Sky
    1: (139, 69, 19),    # Dirt
    2: (105, 105, 105),  # Stone
}

# Generate the world
world = []
for row in range(GRID_HEIGHT):
    row_data = []
    for col in range(GRID_WIDTH):
        if row < 7:
            row_data.append(0)
        elif row < 11:
            row_data.append(1)
        else:
            row_data.append(2)
    world.append(row_data)

# Player position
player_x = 5
player_y = 5

def draw_world():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            tile = world[y][x]
            color = BLOCK_COLORS[tile]
            pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, (0, 0, 0), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

def draw_player():
    pygame.draw.rect(screen, (255, 0, 0), (player_x * TILE_SIZE, player_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def is_adjacent(px, py, bx, by):
    return abs(px - bx) <= 1 and abs(py - by) <= 1

def is_walkable(x, y):
    """Returns True if block is sky (air) and inside bounds"""
    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        return world[y][x] == 0
    return False

# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    draw_world()
    draw_player()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mining with mouse click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            block_x = mouse_x // TILE_SIZE
            block_y = mouse_y // TILE_SIZE

            if 0 <= block_x < GRID_WIDTH and 0 <= block_y < GRID_HEIGHT:
                if is_adjacent(player_x, player_y, block_x, block_y):
                    world[block_y][block_x] = 0  # Mine the block

    # Movement (with collision check)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        new_x = player_x - 1
        if is_walkable(new_x, player_y):
            player_x = new_x
            pygame.time.delay(100)
    if keys[pygame.K_RIGHT]:
        new_x = player_x + 1
        if is_walkable(new_x, player_y):
            player_x = new_x
            pygame.time.delay(100)
    if keys[pygame.K_UP]:
        new_y = player_y - 1
        if is_walkable(player_x, new_y):
            player_y = new_y
            pygame.time.delay(100)
    if keys[pygame.K_DOWN]:
        new_y = player_y + 1
        if is_walkable(player_x, new_y):
            player_y = new_y
            pygame.time.delay(100)

    clock.tick(60)

pygame.quit()
