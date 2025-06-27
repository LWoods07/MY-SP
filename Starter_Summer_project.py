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
pygame.display.set_caption("Simple Mining Game")
clock = pygame.time.Clock()

# Block types: 0 = sky, 1 = dirt, 2 = stone
BLOCK_COLORS = {
    0: (135, 206, 235),  # Sky
    1: (139, 69, 19),    # Dirt
    2: (105, 105, 105),  # Stone
    3: (255, 215, 0),    # Gold
    4: (192, 192, 192),  # Iron
    5: (0, 128, 0),      # Shop (Green)
    6: (0, 0, 255)       # Reset Station (Blue)
}

# Ore values
ORE_VALUES = {
    3: 50,  # Gold
    4: 20   # Iron
}

# Generate the world
def generate_world():
    new_world = []
    for row in range(GRID_HEIGHT):
        row_data = []
        for col in range(GRID_WIDTH):
            if row < 4:
                row_data.append(0)
            elif row < 9:
                row_data.append(1)
            else:
                if random.random() < 0.15:
                    row_data.append(random.choice([3, 4]))
                else:
                    row_data.append(2)
        new_world.append(row_data)
    return new_world

world = generate_world()

# Place a shop on the surface
shop_x, shop_y = 10, 3
world[shop_y][shop_x] = 5

# Place reset station
reset_x, reset_y = 9, 3
world[reset_y][reset_x] = 6

# Player position
player_x, player_y = 5, 3

# Inventory and money
inventory = {3: 0, 4: 0}
money = 0

# Pickaxe level and upgrades
pickaxe_level = 1
upgrade_costs = {1: 100, 2: 250}
show_upgrade_menu = False

# Font to display UI
font = pygame.font.SysFont("Arial", 20)

def draw_world():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            tile = world[y][x]
            color = BLOCK_COLORS[tile]
            pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, (0, 0, 0), (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

def draw_player():
    pygame.draw.rect(screen, (255, 0, 0), (player_x * TILE_SIZE, player_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def draw_ui():
    money_text = font.render(f" ${money}", True, (255, 255, 255))
    screen.blit(money_text, (SCREEN_WIDTH - 120, 10))

    level_text = font.render(f"Pickaxe: {pickaxe_level}x{pickaxe_level}", True, (255, 255, 255))
    screen.blit(level_text, (10, 10))

def draw_upgrade_menu():
    pygame.draw.rect(screen, (30, 30, 30), (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 75, 300, 150))
    pygame.draw.rect(screen, (255, 255, 255), (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 75, 300, 150), 2)

    title = font.render("Upgrade Pickaxe", True, (255, 255, 255))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 65))

    if pickaxe_level < 3:
        next_level = pickaxe_level + 1
        cost = upgrade_costs[pickaxe_level]
        text = font.render(f"Upgrade to {next_level}x{next_level} for ${cost} [E]", True, (200, 200, 0))
    else:
        text = font.render("Max level reached!", True, (150, 150, 150))

    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))

def is_adjacent(px, py, bx, by):
    return abs(px - bx) <= 1 and abs(py - by) <= 1

def is_walkable(x, y):
    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        return world[y][x] in (0, 5, 6)
    return False

def sell_ores():
    global money
    total = 0
    for ore_type, count in inventory.items():
        total += count * ORE_VALUES[ore_type]
        inventory[ore_type] = 0
    money += total
    if total > 0:
        print(f"Sold ores for ${total}!")

def reset_ground():
    for row in range(4, GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if row < 9:
                world[row][col] = 1  # Dirt layer
            else:
                if random.random() < 0.15:
                    world[row][col] = random.choice([3, 4])  # Gold/Iron
                else:
                    world[row][col] = 2  # Stone
    print("Ground reset! Dirt and ores regenerated.")


def mine_block_area(center_x, center_y):
    for dy in range(-(pickaxe_level // 2), (pickaxe_level // 2) + 1):
        for dx in range(-(pickaxe_level // 2), (pickaxe_level // 2) + 1):
            x = center_x + dx
            y = center_y + dy
            if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                tile = world[y][x]
                if tile in [1, 2, 3, 4]:
                    if tile in inventory:
                        inventory[tile] += 1
                    world[y][x] = 0

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))
    draw_world()
    draw_player()
    draw_ui()

    # Upgrade shop UI
    if world[player_y][player_x] == 5:
        draw_upgrade_menu()

    # Reset ground UI
    if world[player_y][player_x] == 6:
        reset_text = font.render("Press [R] to Reset Ground", True, (255, 255, 255))
        screen.blit(reset_text, (SCREEN_WIDTH // 2 - reset_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

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
                    mine_block_area(block_x, block_y)

        # Key press actions
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and world[player_y][player_x] == 5 and pickaxe_level < 3:
                cost = upgrade_costs[pickaxe_level]
                if money >= cost:
                    money -= cost
                    pickaxe_level += 1
                    print(f"Upgraded to {pickaxe_level}x{pickaxe_level} pickaxe!")

            if event.key == pygame.K_r and world[player_y][player_x] == 6:
                reset_ground()

    # Movement (with collision check)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        new_x = player_x - 1
        if is_walkable(new_x, player_y):
            player_x = new_x
            pygame.time.delay(100)

    if keys[pygame.K_d]:
        new_x = player_x + 1
        if is_walkable(new_x, player_y):
            player_x = new_x
            pygame.time.delay(100)

    if keys[pygame.K_w]:
        new_y = player_y - 1
        if new_y >= 3 and is_walkable(player_x, new_y):
            player_y = new_y
            pygame.time.delay(100)

    if keys[pygame.K_s]:
        new_y = player_y + 1
        if is_walkable(player_x, new_y):
            player_y = new_y
            pygame.time.delay(100)

    # Auto-sell ores if on shop tile
    if world[player_y][player_x] == 5:
        sell_ores()

    clock.tick(60)

pygame.quit()