import pygame
import random
import time
import os
import sys
"All names, music, visuals, and assets, including everything in this project, belong to Azerion."
"This is a non-commercial project. If Azerion requests the removal of this project, please contact me, and I will promptly take it down."
def resource_path(relative_path):
    
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


SCREEN_WIDTH = 1092  
SCREEN_HEIGHT = 684

GLOBAL_OFFSET_X = 140
GLOBAL_OFFSET_Y = 50 

OFFSET_X = 120  
OFFSET_Y = 50 

BLOCK_SIZE = 41
BLOCK_COUNT_X = 9 
BLOCK_COUNT_Y = 9

BACKGROUND_X = 0 + OFFSET_X
BACKGROUND_Y = 0 + OFFSET_Y

SCORE_POS_X = 50 + OFFSET_X
SCORE_POS_Y = 50 + OFFSET_Y

GRID_OFFSET_X = 235 + OFFSET_X
GRID_OFFSET_Y = 168 + OFFSET_Y

difficulty = 'NORMAL'

arkaplan_path = resource_path('Harvest/Arkaplan.png')

background = pygame.image.load(arkaplan_path)
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
screen_center_x = (pygame.display.Info().current_w - SCREEN_WIDTH) // 2
screen_center_y = (pygame.display.Info().current_h - SCREEN_HEIGHT) // 2
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{screen_center_x},{screen_center_y}"

BLOCK_IMAGES = {
    "Lahana": pygame.image.load(resource_path('Harvest/Lahana.png')),
    "Kurek": pygame.image.load(resource_path('Harvest/Kurek.png')),
    "Su": pygame.image.load(resource_path('Harvest/Su.png')),
    "Saksi": pygame.image.load(resource_path('Harvest/Saksi.png')),
    "Un": pygame.image.load(resource_path('Harvest/Un.png')),
    "Tas": pygame.image.load(resource_path('Harvest/Tas.png')),
    "Havuc": pygame.image.load(resource_path('Harvest/Havuc.png')),
    None: pygame.Surface((BLOCK_SIZE, BLOCK_SIZE)),
}

empty_block_image = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
empty_block_image.set_colorkey((0, 0, 0))
BLOCK_IMAGES[None] = empty_block_image

def create_grid():
    grid = [[random.choice(list(BLOCK_IMAGES.keys())) for _ in range(BLOCK_COUNT_X)] for _ in range(BLOCK_COUNT_Y)]
    return grid

def load_sounds():
    pygame.mixer.init()
    global music, effect
    music = pygame.mixer.music.load(resource_path('Harvest/Harvest Honors Classic Theme.mp3'))
    effect = pygame.mixer.Sound(resource_path('Harvest/Efekt.mp3'))

def play_music():
    pygame.mixer.music.play(-1)

def play_effect():
    effect.play()

def update_screen(screen, grid, player_score, cpu_score, player_turn):
    screen.blit(background, (0 + GLOBAL_OFFSET_X, 0 + GLOBAL_OFFSET_Y))
    
    for y in range(BLOCK_COUNT_Y):
        for x in range(BLOCK_COUNT_X):
            block_image = BLOCK_IMAGES[grid[y][x]]
            screen.blit(block_image, (GRID_OFFSET_X + x * BLOCK_SIZE, GRID_OFFSET_Y + y * BLOCK_SIZE))
    
    max_score = 100
    bar_width = 200
    bar_height = 48
    
    player_ratio = player_score / max_score
    cpu_ratio = cpu_score / max_score
    
    max_dolum_height = bar_height
    dolum_height = int(min(max(player_score / 20, 0), 1) * max_dolum_height)
    cpu_dolum_height = int(min(max(cpu_score / 20, 0), 1) * max_dolum_height)
    
    player_bar_width = bar_width * player_ratio
    cpu_bar_width = bar_width * cpu_ratio
    
    def draw_rounded_rect(surface, rect, color, border_radius=5):
        pygame.draw.rect(surface, color, rect, border_radius=border_radius)
    
    background_rect_colora = (255, 232, 201)
    background_rect_colorb = (228, 249, 206)
    border_radius = 50
    
    player_bar_bg_rect = pygame.Rect(235, 107, bar_width, bar_height)
    draw_rounded_rect(screen, player_bar_bg_rect, background_rect_colora, border_radius)
    
    cpu_bar_bg_rect = pygame.Rect(635, 107, bar_width, bar_height)
    draw_rounded_rect(screen, cpu_bar_bg_rect, background_rect_colorb, border_radius)
    
    player_bar_rect = pygame.Rect(
        237,
        107 + (bar_height - dolum_height) // 2,
        player_bar_width,
        dolum_height
    )
    draw_rounded_rect(screen, player_bar_rect, (255, 165, 0), border_radius)
    
    cpu_bar_rect = pygame.Rect(
        637,
        107 + (bar_height - cpu_dolum_height) // 2,
        cpu_bar_width,
        cpu_dolum_height
    )
    draw_rounded_rect(screen, cpu_bar_rect, (0, 255, 0), border_radius)
    
    pygame.draw.rect(screen, (255, 255, 255), player_bar_bg_rect, 4, border_radius)
    pygame.draw.rect(screen, (255, 255, 255), cpu_bar_bg_rect, 4, border_radius)
    
    font = pygame.font.Font(None, 40)
    
    def draw_text_with_shadow(surface, text, color, shadow_color, position):
        text_surface = font.render(text, True, color)
        shadow_surface = font.render(text, True, shadow_color)
        shadow_offset = (2, 2)
        
        shadow_rect = shadow_surface.get_rect(topleft=(position[0] + shadow_offset[0], position[1] + shadow_offset[1]))
        text_rect = text_surface.get_rect(topleft=position)
        
        surface.blit(shadow_surface, shadow_rect.topleft)
        surface.blit(text_surface, text_rect.topleft)
    
    draw_text_with_shadow(screen, f"{player_score} / 100", (255, 255, 255), (0, 0, 0), (295, 117))
    
    draw_text_with_shadow(screen, f"{cpu_score} / 100", (255, 255, 255), (0, 0, 0), (695, 117))

    cpu_image = pygame.image.load(resource_path('Harvest/cpu.png'))
    oyuncu_image = pygame.image.load(resource_path('Harvest/oyuncu.png'))
    oyuncu_image = pygame.transform.scale(oyuncu_image, (80, 60))
    cpu_image = pygame.transform.scale(cpu_image, (80, 60))

    if player_turn:
        screen.blit(cpu_image, (495, 100))

    else:
        screen.blit(oyuncu_image, (495, 100))

    pygame.display.flip()

def fill_empty_space(grid, x, y):
    above_y = y - 1
    while above_y >= 0 and grid[above_y][x] is None:
        above_y -= 1
    if above_y >= 0:
        grid[y][x] = grid[above_y][x]
        grid[above_y][x] = None
        check_and_fill_gaps(grid)
    else:
        grid[y][x] = random.choice(list(BLOCK_IMAGES.keys()))
        check_and_fill_gaps(grid)

def check_and_fill_gaps(grid):
    for x in range(BLOCK_COUNT_X):
        for y in range(BLOCK_COUNT_Y):
            if grid[y][x] is None:
                fill_empty_space(grid, x, y)
                

def check_matches(grid):
    matches = False
    score = 0
    for y in range(BLOCK_COUNT_Y):
        for x in range(BLOCK_COUNT_X - 2):
            if grid[y][x] and grid[y][x] == grid[y][x + 1] == grid[y][x + 2]:
                num_matched = 3
                matched_item = grid[y][x]
                while x + num_matched < BLOCK_COUNT_X and grid[y][x + num_matched] == grid[y][x]:
                    num_matched += 1
                for i in range(num_matched):
                    grid[y][x + i] = None
                matches = True
                match_score = num_matched
                if matched_item == 'Havuc':
                    match_score *= 2
                score += match_score
                check_and_fill_gaps(grid)
                check_matches(grid)
    
    for x in range(BLOCK_COUNT_X):
        for y in range(BLOCK_COUNT_Y - 2):
            if grid[y][x] and grid[y][x] == grid[y + 1][x] == grid[y + 2][x]:
                num_matched = 3
                matched_item = grid[y][x]
                while y + num_matched < BLOCK_COUNT_Y and grid[y + num_matched][x] == grid[y][x]:
                    num_matched += 1
                for i in range(num_matched):
                    grid[y + i][x] = None
                matches = True
                match_score = num_matched
                if matched_item == 'Havuc':
                    match_score *= 2
                score += match_score
                check_and_fill_gaps(grid)
                check_matches(grid)

    for x in range(BLOCK_COUNT_X):
        empty_spaces = 0
        for y in range(BLOCK_COUNT_Y - 1, -1, -1):
            if grid[y][x] is None:
                empty_spaces += 1
            elif empty_spaces > 0:
                grid[y + empty_spaces][x] = grid[y][x]
                grid[y][x] = None
                check_and_fill_gaps

    for x in range(BLOCK_COUNT_X):
        for y in range(BLOCK_COUNT_Y):
            if grid[y][x] is None:
                fill_empty_space(grid, x, y)

    return matches, score

def move_animation(screen, grid, selected_block, released_block, player_score, cpu_score, player_turn):
    play_effect()
    start_x, start_y = selected_block
    end_x, end_y = released_block
    dx = (end_x - start_x) * BLOCK_SIZE / 10
    dy = (end_y - start_y) * BLOCK_SIZE / 10
    block_image_selected = BLOCK_IMAGES[grid[end_y][end_x]]
    block_image_released = BLOCK_IMAGES[grid[start_y][start_x]]

    clock = pygame.time.Clock()

    temp_grid = [row[:] for row in grid]

    temp_grid[start_y][start_x] = None
    temp_grid[end_y][end_x] = None

    for i in range(10):
        screen.fill((255, 255, 255), (GRID_OFFSET_X, GRID_OFFSET_Y, BLOCK_COUNT_X * BLOCK_SIZE, BLOCK_COUNT_Y * BLOCK_SIZE))

        update_screen(screen, temp_grid, player_score, cpu_score, player_turn)

        for y in range(BLOCK_COUNT_Y):
            for x in range(BLOCK_COUNT_X):
                if (x, y) == selected_block or (x, y) == released_block:
                    continue
                else:
                    block_image = BLOCK_IMAGES[temp_grid[y][x]] if temp_grid[y][x] is not None else None
                    if block_image:
                        screen.blit(block_image, (GRID_OFFSET_X + x * BLOCK_SIZE, GRID_OFFSET_Y + y * BLOCK_SIZE))

        screen_x_selected = GRID_OFFSET_X + (start_x * BLOCK_SIZE + i * dx)
        screen_y_selected = GRID_OFFSET_Y + (start_y * BLOCK_SIZE + i * dy)
        screen.blit(block_image_selected, (screen_x_selected, screen_y_selected))

        screen_x_released = GRID_OFFSET_X + (end_x * BLOCK_SIZE - i * dx)
        screen_y_released = GRID_OFFSET_Y + (end_y * BLOCK_SIZE - i * dy)
        screen.blit(block_image_released, (screen_x_released, screen_y_released))

        pygame.display.flip()
        clock.tick(60)

    temp_grid[end_y][end_x] = grid[start_y][start_x]
    temp_grid[start_y][start_x] = grid[end_y][end_x]
    return released_block, temp_grid

def player_move(screen, grid, player_score, cpu_score, player_turn):
    selected_block = None
    while selected_block is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                selected_block = ((mouse_x - GRID_OFFSET_X) // BLOCK_SIZE, (mouse_y - GRID_OFFSET_Y) // BLOCK_SIZE)
                if (0 <= selected_block[0] < BLOCK_COUNT_X) and (0 <= selected_block[1] < BLOCK_COUNT_Y):
                    released_block = None
                    while released_block is None:
                        for event in pygame.event.get():
                            if event.type == pygame.MOUSEBUTTONUP:
                                mouse_x, mouse_y = pygame.mouse.get_pos()
                                released_block = ((mouse_x - GRID_OFFSET_X) // BLOCK_SIZE, (mouse_y - GRID_OFFSET_Y) // BLOCK_SIZE)
                                if (0 <= released_block[0] < BLOCK_COUNT_X) and (0 <= released_block[1] < BLOCK_COUNT_Y) and \
                                        (abs(selected_block[0] - released_block[0]) + abs(selected_block[1] - released_block[1]) == 1):
                                    grid[selected_block[1]][selected_block[0]], grid[released_block[1]][released_block[0]] = \
                                        grid[released_block[1]][released_block[0]], grid[selected_block[1]][selected_block[0]]
                                    move_animation(screen, grid, selected_block, released_block, player_score, cpu_score, player_turn)
                                    matches, match_score = check_matches(grid)
                                    if matches:
                                        player_score += match_score
                                    update_screen(screen, grid, player_score, cpu_score, player_turn)  # Skorları güncelle
    return player_score, cpu_score



def find_random_move(grid):
    while True:
        x = random.randint(0, len(grid[0]) - 1)
        y = random.randint(0, len(grid) - 1)

        direction = random.choice(['right', 'down'])
        
        if direction == 'right' and x < len(grid[0]) - 1:
            return (x, y), (x + 1, y)
        elif direction == 'down' and y < len(grid) - 1:
            return (x, y), (x, y + 1)


def cpu_move(screen, grid, player_score, cpu_score, player_turn):
    time.sleep(4)
    check_and_fill_gaps(grid)
    
    if difficulty == 'EASY':
        threshold = 0.40
    elif difficulty == 'HARD':
        threshold = 0.99
    else:
        threshold = 0.65

    if random.random() < threshold:
        best_move = find_best_cpu_move(grid)
    else:
        best_move = find_random_move(grid)
    
    if best_move:
        selected_block, released_block = best_move
        grid[selected_block[1]][selected_block[0]], grid[released_block[1]][released_block[0]] = \
            grid[released_block[1]][released_block[0]], grid[selected_block[1]][selected_block[0]]
        
        play_effect()
        move_animation(screen, grid, selected_block, released_block, player_score, cpu_score, player_turn)
        matches, match_score = check_matches(grid)
        if matches:
            cpu_score += match_score
        
        update_screen(screen, grid, player_score, cpu_score, player_turn)
    
    return player_score, cpu_score

def difficulty_selection(screen):
    global difficulty
    pygame.init()
    
    background_image = pygame.image.load(resource_path('Harvest/Canvas.png'))
    background_image = pygame.transform.scale(background_image, (1366, 768))
    
    font = pygame.font.Font(None, 74)

    easy_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 250, 75)
    normal_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 200, 250, 75)
    hard_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 300, 250, 75)

    easya_button = pygame.Rect(SCREEN_WIDTH // 2 - 102, SCREEN_HEIGHT // 2 + 98, 255, 80)
    normala_button = pygame.Rect(SCREEN_WIDTH // 2 - 102, SCREEN_HEIGHT // 2 + 198, 255, 80)
    harda_button = pygame.Rect(SCREEN_WIDTH // 2 - 102, SCREEN_HEIGHT // 2 + 298, 255, 80)
    
    selecting = True
    while selecting:
        screen.blit(background_image, (0, 0))
        
        pygame.draw.rect(screen, (0, 0, 0), easya_button, border_radius=30)
        pygame.draw.rect(screen, (0, 0, 0), normala_button, border_radius=30)
        pygame.draw.rect(screen, (0, 0, 0), harda_button, border_radius=30)

        pygame.draw.rect(screen, (255, 255, 255), easy_button, border_radius=30)
        pygame.draw.rect(screen, (255, 255, 255), normal_button, border_radius=30)
        pygame.draw.rect(screen, (255, 255, 255), hard_button, border_radius=30)

        easy_text = font.render('EASY', True, (103, 230, 0))
        normal_text = font.render('NORMAL', True, (0, 190, 244))
        hard_text = font.render('HARD', True, (255, 132, 0))
        
        easy_text_rect = easy_text.get_rect(center=easy_button.center)
        normal_text_rect = normal_text.get_rect(center=normal_button.center)
        hard_text_rect = hard_text.get_rect(center=hard_button.center)

        screen.blit(easy_text, easy_text_rect)
        screen.blit(normal_text, normal_text_rect)
        screen.blit(hard_text, hard_text_rect)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if easy_button.collidepoint(mouse_x, mouse_y):
                    difficulty = 'EASY'
                    selecting = False
                elif normal_button.collidepoint(mouse_x, mouse_y):
                    difficulty = 'NORMAL'
                    selecting = False
                elif hard_button.collidepoint(mouse_x, mouse_y):
                    difficulty = 'HARD'
                    selecting = False

def find_best_cpu_move(grid):
    best_move = None
    best_score = 0
    
    for y in range(BLOCK_COUNT_Y):
        for x in range(BLOCK_COUNT_X):
            if x < BLOCK_COUNT_X - 1:
                grid_copy = [row[:] for row in grid]
                grid_copy[y][x], grid_copy[y][x + 1] = grid_copy[y][x + 1], grid_copy[y][x]
                _, score = check_matches(grid_copy)
                if score > best_score:
                    best_score = score
                    best_move = ((x, y), (x + 1, y))
            
            if y < BLOCK_COUNT_Y - 1:
                grid_copy = [row[:] for row in grid]
                grid_copy[y][x], grid_copy[y + 1][x] = grid_copy[y + 1][x], grid_copy[y][x]
                _, score = check_matches(grid_copy)
                if score > best_score:
                    best_score = score
                    best_move = ((x, y), (x, y + 1))
    
    return best_move

def calculate_move_score(grid, move):
    selected_block, released_block = move
    block_value = grid[selected_block[1]][selected_block[0]]

    match_count_horizontal = 1
    for i in range(released_block[0] + 1, BLOCK_COUNT_X):
        if grid[selected_block[1]][i] == block_value:
            match_count_horizontal += 1
        else:
            break

    match_count_vertical = 1
    for i in range(released_block[1] + 1, BLOCK_COUNT_Y):
        if grid[i][selected_block[0]] == block_value:
            match_count_vertical += 1
        else:
            break

    total_match_count = match_count_horizontal + match_count_vertical - 1

    score_multiplier = 1
    if total_match_count >= 4:
        score_multiplier += 2
    elif total_match_count >= 5:
        score_multiplier += 3

    return total_match_count * score_multiplier

def find_matches_recursive(grid, start_pos, current_match_count, best_move, best_match_count):
  x, y = start_pos
  block_value = grid[y][x]

  if block_value == 0:
    return current_match_count

  match_count_horizontal = 1
  for i in range(x + 1, BLOCK_COUNT_X):
    if grid[y][i] == block_value:
      match_count_horizontal += 1
    else:
      break

  match_count_vertical = 1
  for i in range(y + 1, BLOCK_COUNT_Y):
    if grid[i][x] == block_value:
      match_count_vertical += 1
    else:
      break

  total_match_count = current_match_count + max(match_count_horizontal, match_count_vertical) - 1

  if total_match_count > best_match_count:
    best_move = ((x, y), (x + match_count_horizontal - 1, y))
    best_match_count = total_match_count

  if match_count_horizontal > 1:
    find_matches_recursive(grid, (x + match_count_horizontal - 1, y), total_match_count, best_move, best_match_count)

  if match_count_vertical > 1:
    find_matches_recursive(grid, (x, y + match_count_vertical - 1), total_match_count, best_move, best_match_count)

  return total_match_count

def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    pygame.display.set_caption("Harvest Honors Single Player")
    load_sounds()
    grid = create_grid()
    clock = pygame.time.Clock()
    player_score = 0
    cpu_score = 0
    play_music()
    player_turn = True
    running = True
    match_timer = 0
    cpu_wait_time = 2000

    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        match_timer += clock.get_time()
        if match_timer >= 100:
            matches, match_score = check_matches(grid)
            if matches:
                player_score += match_score
                
                match_timer = 0
                cpu_wait_time = 2000

        if player_turn:
            player_score, cpu_score = player_move(screen, grid, player_score, cpu_score)
            player_turn = False
        else:
            if cpu_wait_time > 0:
                cpu_wait_time -= clock.get_time()
            else:
                player_score, cpu_score = cpu_move(screen, grid, player_score, cpu_score)
                player_turn = True

    pygame.quit()

def check_winner(player_score, cpu_score, screen):
    if player_score >= 100:
        display_winner(screen, "Player wins!")
        pygame.time.delay(5000)
        restart_game()
    elif cpu_score >= 100:
        display_winner(screen, "CPU wins!")
        pygame.time.delay(5000)
        restart_game()

def display_winner(screen, message):
    font = pygame.font.Font(None, 75)
    text_surface = font.render(message, True, (255, 255, 255))
    shadow_surface = font.render(message, True, (0, 0, 0))
    shadow_offset = (5, 5)
    
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    shadow_rect = shadow_surface.get_rect(center=(SCREEN_WIDTH // 2 + shadow_offset[0], SCREEN_HEIGHT // 2 + shadow_offset[1]))
    
    screen.blit(shadow_surface, shadow_rect.topleft)
    screen.blit(text_surface, text_rect.topleft)
    pygame.display.flip()

def restart_game():
    main()

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    difficulty_selection(screen)
    pygame.display.set_caption("Match3 Oyunu")
    load_sounds()
    grid = create_grid()
    clock = pygame.time.Clock()
    player_score = 0
    cpu_score = 0
    play_music()
    player_turn = True

    while True:
        if player_turn:
            player_score, cpu_score = player_move(screen, grid, player_score, cpu_score, player_turn)
        else:
            player_score, cpu_score = cpu_move(screen, grid, player_score, cpu_score, player_turn)
        
        update_screen(screen, grid, player_score, cpu_score, player_turn)

        check_winner(player_score, cpu_score, screen)

        player_turn = not player_turn
        clock.tick(30)

if __name__ == "__main__":
    main()