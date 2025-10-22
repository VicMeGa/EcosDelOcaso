import pygame

class Sword(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        SWORD_WIDTH = 50 
        SWORD_HEIGHT = 40 # Ajusta estos valores a tu gusto
        
        # 1. Cargar la imagen original (mirando a la derecha)
        original_loaded_image = pygame.image.load("source/player/sword/1.png").convert_alpha()
        
        # 2. Escalar la imagen original
        self.original_image = pygame.transform.scale(
            original_loaded_image, 
            (SWORD_WIDTH, SWORD_HEIGHT)
        )
        
        # Guardamos también una versión volteada horizontalmente
        self.flipped_image = pygame.transform.flip(self.original_image, True, False)
        
        # Inicializamos con la imagen original (mirando a la derecha)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        
        self.player = player
        self.offset_x = 26  # distancia horizontal respecto al jugador
        self.offset_y = 5  # distancia vertical
        
        self.visible = False # La espada empieza oculta

    def update(self,tiles):
        # 1. Ajustar la imagen de la espada según la dirección del jugador
        if self.player.direction == "right":
            self.image = self.original_image
            # Ajustar la posición para que esté a la derecha del jugador
            self.rect.topleft = (self.player.rect.x + self.offset_x, self.player.rect.y + self.offset_y)
        else: # self.player.direction == "left"
            self.image = self.flipped_image
            # Ajustar la posición para que esté a la izquierda del jugador.
            # Aquí usamos el 'rect.topright' del jugador y restamos el offset_x,
            # o simplemente ajustamos el 'topright' de la propia espada.
            # La elección de 20px es para que no quede demasiado lejos, puedes ajustarla.
            self.rect.topright = (self.player.rect.x + 12, self.player.rect.y + self.offset_y)
            # Otra opción podría ser:
            # self.rect.topleft = (self.player.rect.x - self.offset_x - self.image.get_width(), self.player.rect.y + self.offset_y)


        # 2. Controlar la visibilidad de la espada
        self.visible = self.player.attacking