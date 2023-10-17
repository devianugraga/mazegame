import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
BACKGROUND_COLOR = (0, 0, 0)
MAZE_COLOR = (255, 255, 255)
PLAYER_COLOR = (0, 0, 255)
EXIT_COLOR = (0, 255, 0)
WALL_COLOR = (255, 0, 0)

# Maze layout
maze = [
    "#########",
    "#S      #",
    "#       #",
    "### # ####",
    "#   #    #",
    "#   #    #",
    "### # ###E",
    "#########",
]

# Maze cell size
CELL_SIZE = WIDTH // len(maze[0])

# Set player's starting position
player_x, player_y = 1, 1

# Set exit position
exit_x, exit_y = 6, 6

# Set the timer (in seconds)
time_limit = 60
start_time = None

# Create the Pygame window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

# Load sound effects
move_sound = pygame.mixer.Sound("C:/Users/HP/Downloads/558117__abdrtar__move.mp3")


font = pygame.font.Font(None, 36)

score = 0
player_step = 1
move_delay = 0.2
last_move_time = 0

def draw_maze():
    for y, row in enumerate(maze):
        for x, char in enumerate(row):
            cell_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if char == '#':
                pygame.draw.rect(screen, WALL_COLOR, cell_rect)
            elif char == 'S':
                pygame.draw.rect(screen, MAZE_COLOR, cell_rect)
            elif char == 'E':
                pygame.draw.rect(screen, EXIT_COLOR, cell_rect)

def move_player(direction):
    global player_x, player_y, last_move_time, player_step

    if time.time() - last_move_time < move_delay:
        return

    last_move_time = time.time()

    if direction == "up" and maze[player_y - 1][player_x] != '#':
        player_y -= 1
    elif direction == "down" and maze[player_y + 1][player_x] != '#':
        player_y += 1
    elif direction == "left" and maze[player_y][player_x - 1] != '#':
        player_x -= 1
    elif direction == "right" and maze[player_y][player_x + 1] != '#':
        player_x += 1

    move_sound.play()

def is_game_over():
    global score
    if player_x == exit_x and player_y == exit_y:
       
        score += 10
        return "win"
    
    if start_time is not None and time.time() - start_time > time_limit:
      
        score -= 5
        return "loss"
    
    if maze[player_y][player_x] == '#':
        score -= 1
        return "loss"

def draw_interface():
    pygame.draw.rect(screen, BACKGROUND_COLOR, (0, HEIGHT - 60, WIDTH, 60))
    
    score_text = font.render("Score: " + str(score), True, MAZE_COLOR)
    game_status = is_game_over()
    if game_status:
        if game_status == "win":
            game_status_text = font.render("You won!", True, (0, 255, 0))
        else:
            game_status_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_status_text, (WIDTH // 2 - game_status_text.get_width() // 2, HEIGHT // 2 - game_status_text.get_height() // 2))
        screen.blit(font.render("Press 'N' for New Game or 'R' to Restart", True, MAZE_COLOR), (WIDTH // 2 - 220, HEIGHT // 2 + 50))
    
    screen.blit(score_text, (WIDTH - score_text.get_width() - 20, HEIGHT - 50))


def start_game():
    global start_time, score, player_x, player_y, player_step, last_move_time
    start_time = time.time()
    player_x, player_y = 1, 1
    score = 0
    player_step = 1
    last_move_time = 0

def restart_game():
    global start_time, player_x, player_y, player_step, last_move_time
    start_time = time.time()
    player_x, player_y = 1, 1
    player_step = 1
    last_move_time = 0

def main():
    start_game()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        key = pygame.key.get_pressed()
        if key[pygame.K_q]:
            pygame.quit()
            sys.exit()

        direction = None
        if key[pygame.K_w]:
            direction = "up"
        elif key[pygame.K_s]:
            direction = "down"
        elif key[pygame.K_a]:
            direction = "left"
        elif key[pygame.K_d]:
            direction = "right"

        if direction:
            move_player(direction)
            result = is_game_over()
            if result:
                if result == "win":
                    game_status_text = font.render("You won!", True, (0, 255, 0))
                else:
                    game_status_text = font.render("Game Over", True, (255, 0, 0))
                screen.blit(game_status_text, (WIDTH // 2 - game_status_text.get_width() // 2, HEIGHT // 2 - game_status_text.get_height() // 2))
                screen.blit(font.render("Press 'N' for New Game or 'R' to Restart", True, MAZE_COLOR), (WIDTH // 2 - 220, HEIGHT // 2 + 50))
                pygame.display.flip()
                time.sleep(2)
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    key = pygame.key.get_pressed()
                    if key[pygame.K_q]:
                        pygame.quit()
                        sys.exit()
                    if key[pygame.K_n]:
                        start_game()
                        break
                    if key[pygame.K_r]:
                        restart_game()
                        break

        screen.fill(BACKGROUND_COLOR)
        draw_maze()
        pygame.draw.rect(screen, PLAYER_COLOR, (player_x * CELL_SIZE, player_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        draw_interface()
        pygame.display.flip()

if __name__ == "__main__":
    main()
