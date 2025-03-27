import pygame
import random

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de tir - Space Shooter")

# Couleurs
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Charger les images
player_img = pygame.image.load("player.png")  # Mets un fichier 'player.png' dans le dossier
enemy_img = pygame.image.load("enemy.png")  # Mets un fichier 'enemy.png' dans le dossier
bullet_img = pygame.image.load("bullet.png")  # Mets un fichier 'bullet.png' dans le dossier

# Redimensionner les images
player_img = pygame.transform.scale(player_img, (50, 50))
enemy_img = pygame.transform.scale(enemy_img, (40, 40))
bullet_img = pygame.transform.scale(bullet_img, (10, 20))

# Classe du vaisseau joueur
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 60
        self.speed = 5
        self.width = 50
        self.height = 50
        self.lives = 3

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < WIDTH - self.width:
            self.x += self.speed

    def draw(self):
        screen.blit(player_img, (self.x, self.y))

# Classe des ennemis
class Enemy:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 40)
        self.y = random.randint(-100, -40)
        self.speed = random.randint(2, 4)

    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-100, -40)
            self.x = random.randint(0, WIDTH - 40)

    def draw(self):
        screen.blit(enemy_img, (self.x, self.y))

# Classe des balles
class Bullet:
    def __init__(self, x, y):
        self.x = x + 20  # Centrer la balle sur le vaisseau
        self.y = y
        self.speed = 7

    def move(self):
        self.y -= self.speed

    def draw(self):
        screen.blit(bullet_img, (self.x, self.y))

# Fonction principale
def game():
    clock = pygame.time.Clock()
    running = True

    player = Player()
    enemies = [Enemy() for _ in range(5)]
    bullets = []
    score = 0

    font = pygame.font.Font(None, 36)

    while running:
        screen.fill((0, 0, 0))  # Fond noir

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player.x, player.y))

        # Gestion des touches pressées
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move("left")
        if keys[pygame.K_RIGHT]:
            player.move("right")

        # Déplacement des balles
        for bullet in bullets[:]:
            bullet.move()
            if bullet.y < 0:
                bullets.remove(bullet)

        # Déplacement des ennemis
        for enemy in enemies:
            enemy.move()

        # Vérification des collisions balles - ennemis
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if enemy.x < bullet.x < enemy.x + 40 and enemy.y < bullet.y < enemy.y + 40:
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    enemies.append(Enemy())
                    score += 1

        # Vérification des collisions ennemis - joueur
        for enemy in enemies:
            if enemy.x < player.x < enemy.x + 40 and enemy.y + 40 > player.y:
                player.lives -= 1
                enemies.remove(enemy)
                enemies.append(Enemy())
                if player.lives <= 0:
                    game_over(score)
                    return

        # Affichage des éléments
        player.draw()
        for enemy in enemies:
            enemy.draw()
        for bullet in bullets:
            bullet.draw()

        # Affichage du score et des vies
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Vies: {player.lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 100, 10))

        pygame.display.flip()
        clock.tick(60)

# Écran de Game Over
def game_over(score):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 48)
    text = font.render(f"Game Over! Score: {score}", True, RED)
    restart_text = font.render("Appuie sur une touche pour rejouer", True, WHITE)

    screen.blit(text, (WIDTH // 6, HEIGHT // 3))
    screen.blit(restart_text, (WIDTH // 8, HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                waiting = False
                game()

# Lancer le jeu
game()
pygame.quit()
