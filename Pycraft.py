import pygame
import sys
import random

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (0, 255, 0)  # Verde
PLAYER_SPEED = 2  # Velocidad del jugador
BLOCK_SIZE = 40
PLAYER_LIFE = 100  # Vida del jugador

# Colores de los bloques
BLOCK_COLORS = {
    "tierra": (139, 69, 19),  # Marrón
    "piedra": (128, 128, 128),  # Gris
    "arena": (194, 178, 128),  # Arena
    "agua": (0, 0, 255),  # Azul
    "pasto": (34, 139, 34)  # Verde pasto
}

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pycraft")

# Clase del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (0, 0, 255), [(10, 0), (0, 20), (20, 20)])
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.change_x = 0
        self.change_y = 0
        self.life = PLAYER_LIFE

    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y

# Generación de bloques
def generate_terrain():
    block_list = pygame.sprite.Group()
    for x in range(0, SCREEN_WIDTH, BLOCK_SIZE):
        for y in range(0, SCREEN_HEIGHT, BLOCK_SIZE):
            rand_value = random.random()
            if rand_value < 0.1:
                block_type = "agua"
            elif rand_value < 0.2:
                block_type = "arena"
            elif rand_value < 0.5:
                block_type = "tierra"
            elif rand_value < 0.8:
                block_type = "pasto"
            else:
                block_type = "piedra"
            
            block = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
            block.fill(BLOCK_COLORS[block_type])
            block_rect = block.get_rect(topleft=(x, y))
            block_list.add(pygame.sprite.Sprite())
            block_list.sprites()[-1].image = block
            block_list.sprites()[-1].rect = block_rect
    
    return block_list

block_list = generate_terrain()

# Creación del jugador
player = Player()
all_sprites = pygame.sprite.Group(player)

# Inventario
inventory = ["tierra", "piedra", "arena", "agua", "pasto"]
selected_block = 0

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_w, pygame.K_UP):
                player.change_y = -PLAYER_SPEED
            elif event.key in (pygame.K_s, pygame.K_DOWN):
                player.change_y = PLAYER_SPEED
            elif event.key in (pygame.K_a, pygame.K_LEFT):
                player.change_x = -PLAYER_SPEED
            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                player.change_x = PLAYER_SPEED
            elif event.key == pygame.K_1:
                selected_block = 0  # Seleccionar el primer bloque del inventario
            elif event.key == pygame.K_2:
                selected_block = 1  # Seleccionar el segundo bloque del inventario
            elif event.key == pygame.K_3:
                selected_block = 2  # Seleccionar el tercer bloque del inventario
            elif event.key == pygame.K_4:
                selected_block = 3  # Seleccionar el cuarto bloque del inventario
            elif event.key == pygame.K_5:
                selected_block = 4  # Seleccionar el quinto bloque del inventario
            elif event.key == pygame.K_SPACE:
                # Colocar un bloque
                block = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                block.fill(BLOCK_COLORS[inventory[selected_block]])
                block_rect = block.get_rect(topleft=(player.rect.x, player.rect.y))
                block_list.add(pygame.sprite.Sprite())
                block_list.sprites()[-1].image = block
                block_list.sprites()[-1].rect = block_rect
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s, pygame.K_UP, pygame.K_DOWN):
                player.change_y = 0
            elif event.key in (pygame.K_a, pygame.K_d, pygame.K_LEFT, pygame.K_RIGHT):
                player.change_x = 0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Minar un bloque
            pos = pygame.mouse.get_pos()
            for block in block_list:
                if block.rect.collidepoint(pos):
                    block.kill()

    # Actualización de sprites
    all_sprites.update()

    # Dibujar todo
    screen.fill(BACKGROUND_COLOR)
    block_list.draw(screen)
    all_sprites.draw(screen)

    # Mostrar inventario y vida
    font = pygame.font.SysFont(None, 24)
    inventory_text = font.render(f"Inventario: {inventory[selected_block]}", True, (0, 0, 0))
    screen.blit(inventory_text, (10, 10))
    life_text = font.render(f"Vida: {player.life}", True, (255, 0, 0))
    screen.blit(life_text, (10, 40))

    # Actualizar pantalla
    pygame.display.flip()

pygame.quit()
sys.exit()

