import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, patrol_range=(0,0), speed=1):
        super().__init__()
        
        # Cargar animaciones
        self.walk_right = [pygame.image.load(f"enemies/enemi1/walk/walk{i}.png").convert_alpha() for i in range(1,7)]
        self.walk_left = [pygame.transform.flip(img, True, False) for img in self.walk_right]
        self.idle_right = [pygame.image.load(f"enemies/enemi1/idle/idle{i}.png").convert_alpha() for i in range(1,5)]
        self.idle_left = [pygame.transform.flip(img, True, False) for img in self.idle_right]
        self.attack_right = [pygame.image.load(f"enemies/enemi1/atack/atack{i}.png").convert_alpha() for i in range(1,7)]
        self.attack_left = [pygame.transform.flip(img, True, False) for img in self.attack_right]
        self.dead = [pygame.image.load(f"enemies/enemi1/dead/dead{i}.png").convert_alpha() for i in range(1,7)]
        
        self.image = self.idle_right[0]
        self.rect = self.image.get_rect(topleft=pos)
        
        self.speed = speed
        self.direction = 1
        self.start_x, self.end_x = patrol_range
        self.anim_index = 0
        self.state = "idle"  # puede ser: idle, walk, attack, dead

    def update(self, collision_tiles=None):
        self.patrol()
        self.handle_collision(collision_tiles)
        self.animate()

    def patrol(self):
        if self.state != "dead":
            self.rect.x += self.speed * self.direction
            if self.rect.x < self.start_x or self.rect.x > self.end_x:
                self.direction *= -1

    def animate(self, collision_tiles=None):
        # Aquí eliges la animación según el estado
        self.anim_index += 0.2
        if self.state == "walk":
            frames = self.walk_right if self.direction > 0 else self.walk_left
        elif self.state == "idle":
            frames = self.idle_right if self.direction > 0 else self.idle_left
        elif self.state == "attack":
            frames = self.attack_right if self.direction > 0 else self.attack_left
        elif self.state == "dead":
            frames = self.dead
        else:
            frames = [self.image]
        
        if self.anim_index >= len(frames):
            if self.state == "dead":
                self.anim_index = len(frames) - 1  # queda en el último frame
            else:
                self.anim_index = 0
        
        self.image = frames[int(self.anim_index)]
    
    def handle_collision(self, tiles):
        if tiles is None:
            return
        for tile in tiles:
            if self.rect.colliderect(tile):
                # rebota o se detiene
                if self.direction > 0:  # va a la derecha
                    self.rect.right = tile.left
                    self.direction *= -1
                else:  # va a la izquierda
                    self.rect.left = tile.right
                    self.direction *= -1

    def take_hit(self, death_sound=None):
        """Cambia el estado del enemigo a 'dead' si no lo estaba ya."""
        if self.state != "dead":
            self.state = "dead"
            self.anim_index = 0  # Reinicia el índice para empezar la animación de muerte
            self.speed = 0       # Detiene el movimiento
            # Opcional: Deshabilita la colisión con otros objetos si es necesario
            # self.rect.size = (0, 0)
            if death_sound:
                death_sound.play()