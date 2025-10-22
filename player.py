import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.run_right = [pygame.transform.scale(
                      pygame.image.load(f'source/player/run/{i}.png').convert_alpha(),
                      (40, 50)) for i in range(7)]
        self.run_left = [pygame.transform.flip(img, True, False) for img in self.run_right]
        self.index = 0
        self.image = self.run_right[self.index] 
        self.rect = self.image.get_rect(topleft=pos)
        self.dead = [pygame.image.load(f"source/player/death/{i}.png").convert_alpha() for i in range(8)]
        self.direction = "right"
        self.speed = 3
        self.initial_pos = pos
        self.vel_y = 0
        self.jumping = False
        self.alive = True
        self.health = 5 
        # Dimensiones del personaje (las mismas que usaste para correr/atacar)
        PLAYER_SIZE = (40, 50) 

        # Sprites de Salto (solo una imagen para subir y una para bajar)
        self.jump_up_right = pygame.transform.scale(
            pygame.image.load('source/player/jump/0.png').convert_alpha(),
            PLAYER_SIZE)
            
        self.jump_down_right = pygame.transform.scale(
            pygame.image.load('source/player/fall/0.png').convert_alpha(),
            PLAYER_SIZE)

        self.jump_up_left = pygame.transform.flip(self.jump_up_right, True, False)
        self.jump_down_left = pygame.transform.flip(self.jump_down_right, True, False)

        #Ataque
        self.attack_right = [pygame.transform.scale(
                        pygame.image.load(f'source/player/attack/{i}.png').convert_alpha(),
                        (40, 50)) for i in range(6)]

        self.attack_left = [pygame.transform.flip(img, True, False) for img in self.attack_right]

        self.attacking = False
        self.attack_index = 0
        #self.visible = False 

    def update(self,tiles):
        self.move(tiles)
        self.handle_attack()
        self.animate()

    def move(self, tiles=None):
        keys = pygame.key.get_pressed()
        moving = False
        dx = 0
        dy = 0

        # Movimiento horizontal
        if keys[pygame.K_LEFT]:
            dx = -self.speed
            self.direction = "left"
            moving = True
        if keys[pygame.K_RIGHT]:
            dx = self.speed
            self.direction = "right"
            moving = True

        # Gravedad
        self.vel_y += 1
        if self.vel_y > 15:  # velocidad terminal
            self.vel_y = 15
        dy = self.vel_y

        # Salto
        if keys[pygame.K_SPACE] and not self.jumping:
            self.vel_y = -15
            dy = self.vel_y
            self.jumping = True

        # Aplicar movimiento + colisiones
        self.rect.x += dx
        if tiles:
            self.check_collision(dx, 0, tiles)

        self.rect.y += dy
        if tiles:
            self.check_collision(0, dy, tiles)

        self.moving = moving

    def animate(self):
        # La lógica de animación debe priorizar el ataque
        if self.alive:
            if self.attacking:
                # Animación de ataque
                self.attack_index += 0.3 # Ajusta la velocidad de animación a tu gusto
                
                if self.attack_index >= len(self.attack_right):
                    self.attack_index = 0
                    self.attacking = False # EL ATAQUE TERMINA SOLO AQUÍ, una vez finalizada la animación.
                
                # Dibujar el frame de ataque
                current_frame = int(self.attack_index)
                if self.direction == "right":
                    self.image = self.attack_right[current_frame]
                else:
                    self.image = self.attack_left[current_frame]
            elif self.jumping:
                # Está subiendo
                if self.vel_y < 0:
                    if self.direction == "right":
                        self.image = self.jump_up_right
                    else:
                        self.image = self.jump_up_left
                # Está bajando
                elif self.vel_y > 0:
                    if self.direction == "right":
                        self.image = self.jump_down_right
                    else:
                        self.image = self.jump_down_left
                        
            # Animación de correr/reposo (solo si no estamos atacando)
            elif self.moving:
                self.index += 0.2
                if self.index >= len(self.run_right):
                    self.index = 0
                self.image = self.run_right[int(self.index)] if self.direction == "right" else self.run_left[int(self.index)]
            else:
                self.index = 0
                self.image = self.run_right[0] if self.direction == "right" else self.run_left[0]
        
        # **¡Importante!** Se elimina la línea de self.sword.visible,
        # ya que la clase Sword se encarga de eso.
    
    def handle_attack(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] and not self.attacking:
            self.attacking = True
            self.attack_index = 0 # Reinicia el índice al empezar a atacar
    
    def check_collision(self, dx, dy, tiles):
        for tile in tiles:
            if self.rect.colliderect(tile):
                if dx > 0:  # choca a la derecha
                    self.rect.right = tile.left
                if dx < 0:  # choca a la izquierda
                    self.rect.left = tile.right
                if dy > 0:  # cae sobre el piso
                    self.rect.bottom = tile.top
                    self.vel_y = 0
                    self.jumping = False
                if dy < 0:  # golpea el techo
                    self.rect.top = tile.bottom
                    self.vel_y = 0
    
    def die(self, player_death_sound=None):
        """Maneja el estado de muerte del jugador."""
        if self.alive:
            self.alive = False
            self.speed = 0 # Detiene el movimiento
            # TODO: Aquí podrías iniciar una animación de 'game over' o
            # simplemente detener el juego y reiniciar el nivel/mostrar un menú.
            if player_death_sound:
                player_death_sound.play()
            print("¡El jugador ha muerto!")
            self.health= 5
    
    def take_hit(self, damage=1):
        if not self.alive:
            return

        self.health -= damage
        print(f"HP del jugador: {self.health}")

        if self.health <= 0:
            self.die()
