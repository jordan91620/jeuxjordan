import pygame
import random

# Initialisation de pygame
pygame.init()

# Paramètres du jeu
WIDTH = 600
HEIGHT = 800
CAR_WIDTH = 50
CAR_HEIGHT = 100
LANE_COUNT = 5  # Nombre de voies
LANE_WIDTH = WIDTH // LANE_COUNT
SPEED = 5

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de Course")

# Chargement des images
player_car = pygame.image.load("player_car.png")  # Remplace par ton image
player_car = pygame.transform.scale(player_car, (CAR_WIDTH, CAR_HEIGHT))

# Fonction principale du jeu
def game():
    running = True
    clock = pygame.time.Clock()
    
    lane_positions = [(LANE_WIDTH * i + (LANE_WIDTH - CAR_WIDTH) // 2) for i in range(LANE_COUNT)]
    player_lane = LANE_COUNT // 2  # Commence au milieu
    player_x = lane_positions[player_lane]
    player_y = HEIGHT - CAR_HEIGHT - 20
    
    obstacle_x = random.choice(lane_positions)
    obstacle_y = -CAR_HEIGHT
    
    score = 0
    font = pygame.font.Font(None, 36)
    
    while running:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and player_lane > 0:
                    player_lane -= 1
                elif event.key == pygame.K_RIGHT and player_lane < LANE_COUNT - 1:
                    player_lane += 1
                player_x = lane_positions[player_lane]
        
        obstacle_y += SPEED
        
        if obstacle_y > HEIGHT:
            obstacle_y = -CAR_HEIGHT
            obstacle_x = random.choice(lane_positions)
            score += 1
        
        if player_y < obstacle_y + CAR_HEIGHT and player_y + CAR_HEIGHT > obstacle_y and player_x == obstacle_x:
            break  # Collision -> Fin du jeu
        
        pygame.draw.rect(screen, RED, (obstacle_x, obstacle_y, CAR_WIDTH, CAR_HEIGHT))
        screen.blit(player_car, (player_x, player_y))
        
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(30)
    
    game_over(score)

# Écran de fin
def game_over(score):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 48)
    text = font.render(f"Game Over! Score: {score}", True, WHITE)
    screen.blit(text, (WIDTH // 6, HEIGHT // 3))
    pygame.display.flip()
    
    pygame.time.delay(2000)
    game()  # Redémarre le jeu

if __name__ == "__main__":
    game()
    pygame.quit()
