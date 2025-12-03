from game import iniciarJuego  # función del juego uwu
import pygame
import os
pygame.init()

# Obtener la ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_asset_path(relative_path):
    """Retorna la ruta absoluta del asset"""
    return os.path.join(BASE_DIR, relative_path)


WIDTH, HEIGHT = 800, 580
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def menu_principal():
    menu_running = True
    font = pygame.font.Font(None, 80)

    # Fondo
    fondo = pygame.image.load(get_asset_path("source/5.png")).convert()

    # Botón con imagen
    img_boton_jugar = pygame.image.load(get_asset_path(
        "menu/FreeFairyTaleUIPLAY.png")).convert_alpha()
    img_boton_jugar = pygame.transform.scale(img_boton_jugar, (250, 100))
    boton_jugar_rect = img_boton_jugar.get_rect()
    boton_jugar_rect.topleft = (280, 300)

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar_rect.collidepoint(event.pos):
                    iniciarJuego()          # inicia el juego uwu 🌸
                    menu_running = False    # cierra el menú

        # Dibujar fondo
        screen.blit(fondo, (0, 0))

        # Título
        texto = font.render("Ecos del Ocaso", True, (255, 255, 255))
        screen.blit(texto, (200, 100))

        # Botón
        screen.blit(img_boton_jugar, boton_jugar_rect)

        pygame.display.flip()
        clock.tick(60)


# Llamar al menú
menu_principal()
