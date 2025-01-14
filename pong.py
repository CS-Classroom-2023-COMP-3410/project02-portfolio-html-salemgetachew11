import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
BALL_SPEED_X, BALL_SPEED_Y = 7, 7
PADDLE_SPEED = 10
OPPONENT_SPEED = 7
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
FPS = 60

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# Ball setup
ball = pygame.Rect(SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT // 2 - 15, 30, 30)

# Paddles setup
paddle_player = pygame.Rect(SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2 - 70, 10, 140)
paddle_opponent = pygame.Rect(10, SCREEN_HEIGHT // 2 - 70, 10, 140)

# Colors
bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)

# Score variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font(None, 36)  # None uses the default font, 36 is the size

def ball_animation():
    global BALL_SPEED_X, BALL_SPEED_Y, player_score, opponent_score

    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    # Ball collision (top or bottom)
    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        BALL_SPEED_Y *= -1

    # Ball collision (left or right)
    if ball.left <= 0:
        BALL_SPEED_X *= -1
        player_score += 1
        respawn_ball()
    if ball.right >= SCREEN_WIDTH:
        BALL_SPEED_X *= -1
        opponent_score += 1
        respawn_ball()

    # Ball collision with paddles
    if ball.colliderect(paddle_player) or ball.colliderect(paddle_opponent):
        BALL_SPEED_X *= -1

def paddle_movement():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and paddle_player.top > 0:
        paddle_player.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and paddle_player.bottom < SCREEN_HEIGHT:
        paddle_player.y += PADDLE_SPEED

def opponent_ai():
    if paddle_opponent.top < ball.y:
        paddle_opponent.y += OPPONENT_SPEED
    if paddle_opponent.bottom > ball.y:
        paddle_opponent.y -= OPPONENT_SPEED

def respawn_ball():
    # Reset ball to the center of the screen
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

def draw_scores():
    player_text = game_font.render(f"{player_score}", False, WHITE)
    opponent_text = game_font.render(f"{opponent_score}", False, WHITE)
    screen.blit(player_text, (SCREEN_WIDTH / 2 + 20, 20))
    screen.blit(opponent_text, (SCREEN_WIDTH / 2 - 40, 20))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ball_animation()
    paddle_movement()
    opponent_ai()

    # Drawing
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, paddle_player)
    pygame.draw.rect(screen, light_grey, paddle_opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))
    draw_scores()  # Display scores

    pygame.display.flip()
    clock.tick(FPS)
