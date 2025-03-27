import pygame
import random

# Initialisation de pygame
pygame.init()

# Définition des couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Paramètres du jeu
WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20
SPEED = 10

# Création de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")


# Fonction principale du jeu
def game():
    clock = pygame.time.Clock()
    running = True
    
    snake = [(100, 100)]
    direction = (CELL_SIZE, 0)
    score = 0
    
    food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
            random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
    
    font = pygame.font.Font(None, 36)
    
    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # Quitte directement la fonction
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)
        
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        
        if new_head in snake or not (0 <= new_head[0] < WIDTH and 0 <= new_head[1] < HEIGHT):
            break  # Fin du jeu
        
        snake.insert(0, new_head)
        
        if new_head == food:
            score += 1
            food = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                    random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)
        else:
            snake.pop()
        
        pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
        
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        pygame.display.flip()
        clock.tick(SPEED)
    
    game_over(score)

# Écran de fin
def game_over(score):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 48)
    text = font.render(f"Game Over! Score: {score}", True, WHITE)
    screen.blit(text, (WIDTH // 6, HEIGHT // 3))
    pygame.display.flip()
    
    pygame.time.delay(2000)
    game()  # Redémarre le jeu après un délai

if __name__ == "__main__":
    game()
    pygame.quit()
