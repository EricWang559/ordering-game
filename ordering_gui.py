import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ordering Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [RED, GREEN, BLUE, (255, 255, 0), (255, 0, 255)]

# Game variables
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)
items = list(range(5))
shuffled_items = random.sample(items, 5)

# Rectangles for items and drop zones
item_rects = []
drop_zones = []
for i in range(5):
    # Initial positions of draggable items
    item_rects.append(pygame.Rect(150 * i + 50, 400, 100, 100))
    # Drop zones at the top
    drop_zones.append(pygame.Rect(150 * i + 50, 100, 100, 100))

# Game state
selected_item = None
selected_rect = None
original_pos = None
offset_x, offset_y = 0, 0
game_over = False
score = 0

# Button
check_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 75, 500, 150, 50)
BUTTON_COLOR = (100, 200, 100)
BUTTON_DISABLED_COLOR = (200, 200, 200)

def calculate_score():
    current_score = 0
    for i, rect in enumerate(item_rects):
        # Check if the item is in the correct drop zone
        # The item 'j' should be in drop_zones[shuffled_items.index(j)]
        item_value = items[i]
        correct_zone_index = shuffled_items.index(item_value)
        if drop_zones[correct_zone_index].colliderect(rect):
            current_score += 1
    return current_score

def draw_elements():
    screen.fill(WHITE)

    # Draw drop zones
    for i, zone in enumerate(drop_zones):
        pygame.draw.rect(screen, (200, 200, 200), zone, 2) # Gray border
        unknown = font.render("?", True, (200, 200, 200))
        screen.blit(unknown, (zone.centerx - unknown.get_width() // 2, zone.centery - unknown.get_height() // 2))


    # Draw items
    for i, rect in enumerate(item_rects):
        pygame.draw.rect(screen, COLORS[items[i]], rect)
        text = font.render(str(items[i] + 1), True, BLACK)
        screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

    # Display score
    score_text = small_font.render(f"Correct: {score}/5", True, BLACK)
    screen.blit(score_text, (50, 50))

    # Draw check button
    all_placed = all(any(rect.colliderect(zone) for zone in drop_zones) for rect in item_rects)
    button_color = BUTTON_COLOR if all_placed else BUTTON_DISABLED_COLOR
    pygame.draw.rect(screen, button_color, check_button_rect)
    button_text = small_font.render("Check", True, BLACK)
    screen.blit(button_text, (check_button_rect.centerx - button_text.get_width() // 2, check_button_rect.centery - button_text.get_height() // 2))


    if game_over:
        win_text = font.render("You Won!", True, GREEN)
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - win_text.get_height() // 2))
        restart_text = small_font.render("Press R to Restart", True, BLACK)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

    pygame.display.flip()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Check button click
                    all_placed = all(any(rect.colliderect(zone) for zone in drop_zones) for rect in item_rects)
                    if check_button_rect.collidepoint(event.pos) and all_placed:
                        score = calculate_score()
                        if score == 5:
                            game_over = True
                    else: # Check for item click
                        for i, rect in enumerate(item_rects):
                            if rect.collidepoint(event.pos):
                                selected_item = i
                                selected_rect = rect
                                original_pos = rect.topleft
                                offset_x = event.pos[0] - rect.x
                                offset_y = event.pos[1] - rect.y
                                break

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and selected_item is not None:
                    # Check for snapping
                    snapped = False
                    for i, zone in enumerate(drop_zones):
                        if selected_rect.colliderect(zone):
                            # Find if another item is in the zone
                            other_item_index = -1
                            for j, other_rect in enumerate(item_rects):
                                if j != selected_item and other_rect.center == zone.center:
                                    other_item_index = j
                                    break
                            
                            if other_item_index != -1:
                                # Swap positions
                                item_rects[other_item_index].topleft = original_pos
                            
                            selected_rect.center = zone.center
                            snapped = True
                            break
                    
                    if not snapped:
                        # Return to original position
                        selected_rect.topleft = original_pos

                    selected_item = None
                    selected_rect = None
                    original_pos = None

            if event.type == pygame.MOUSEMOTION:
                if selected_item is not None:
                    selected_rect.x = event.pos[0] - offset_x
                    selected_rect.y = event.pos[1] - offset_y

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                # Reset game
                shuffled_items = random.sample(items, 5)
                item_rects = []
                for i in range(5):
                    item_rects.append(pygame.Rect(150 * i + 50, 400, 100, 100))
                game_over = False
                score = 0

    draw_elements()
