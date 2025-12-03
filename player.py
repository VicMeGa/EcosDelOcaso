import pygame
import os

# Obtener la ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_asset_path(relative_path):
    """Retorna la ruta absoluta del asset"""
    return os.path.join(BASE_DIR, relative_path)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.run_right = [pygame.transform.scale(
            pygame.image.load(get_asset_path(
                f'source/player/run/{i}.png')).convert_alpha(),
            (40, 50)) for i in range(7)]
        self.run_left = [pygame.transform.flip(
            img, True, False) for img in self.run_right]
        self.index = 0
        self.image = self.run_right[self.index]
        self.rect = self.image.get_rect(topleft=pos)
        self.dead = [pygame.image.load(get_asset_path(
            f"source/player/death/{i}.png")).convert_alpha() for i in range(8)]
        self.direction = "right"
        self.speed = 3
        self.initial_pos = pos
        self.vel_y = 0
        self.jumping = False
        self.alive = True
        self.health = 5
        self.death_index = 0
        self.death_anim_finished = False

        # Dimensiones del personaje (las mismas que usaste para correr/atacar)
        PLAYER_SIZE = (40, 50)

        # Sprites de Salto (solo una imagen para subir y una para bajar)
        self.jump_up_right = pygame.transform.scale(
            pygame.image.load(get_asset_path(
                'source/player/jump/0.png')).convert_alpha(),
            PLAYER_SIZE)

        self.jump_down_right = pygame.transform.scale(
            pygame.image.load(get_asset_path(
                'source/player/fall/0.png')).convert_alpha(),
            PLAYER_SIZE)

        self.jump_up_left = pygame.transform.flip(
            self.jump_up_right, True, False)
        self.jump_down_left = pygame.transform.flip(
            self.jump_down_right, True, False)

        # Ataque
        self.attack_right = [pygame.transform.scale(
            pygame.image.load(get_asset_path(
                f'source/player/attack/{i}.png')).convert_alpha(),
            (40, 50)) for i in range(6)]

        self.attack_left = [pygame.transform.flip(
            img, True, False) for img in self.attack_right]

        self.attacking = False
        self.attack_index = 0
        # self.visible = False

    def update(self, tiles):
        self.move(tiles)
        self.handle_attack()
        self.animate()

    def move(self, tiles=None):
        keys = pygame.key.get_pressed()
        moving = False
        dx = 0
        dy = 0

        if not self.alive:
            return

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
        # 💀 PRIORIDAD MÁXIMA — Animación de muerte
        if not self.alive:
            if not self.death_anim_finished:
                self.death_index += 0.2

                if self.death_index >= len(self.dead):
                    self.death_index = len(self.dead) - 1
                    self.death_anim_finished = True  # terminó animación

                self.image = pygame.transform.scale(
                    self.dead[int(self.death_index)], (40, 50)
                )
            return  # no dejar que haga otra animación

        # ✨ Animación de ataque
        if self.attacking:
            self.attack_index += 0.3

            if self.attack_index >= len(self.attack_right):
                self.attack_index = 0
                self.attacking = False

            frame = int(self.attack_index)
            self.image = (
                self.attack_right[frame]
                if self.direction == "right"
                else self.attack_left[frame]
            )
            return  # importantísimo: no pase a correr / saltar mientras ataca

        # ✨ Animaciones de salto
        if self.jumping:
            if self.vel_y < 0:  # sube
                self.image = (
                    self.jump_up_right
                    if self.direction == "right"
                    else self.jump_up_left
                )
            else:  # baja
                self.image = (
                    self.jump_down_right
                    if self.direction == "right"
                    else self.jump_down_left
                )
            return

        # ✨ Animación de carrera
        if self.moving:
            self.index += 0.2
            if self.index >= len(self.run_right):
                self.index = 0
            self.image = (
                self.run_right[int(self.index)]
                if self.direction == "right"
                else self.run_left[int(self.index)]
            )
            return

        # ✨ Animación de idle
        self.index = 0
        self.image = (
            self.run_right[0]
            if self.direction == "right"
            else self.run_left[0]
        )

        # **¡Importante!** Se elimina la línea de self.sword.visible,
        # ya que la clase Sword se encarga de eso.

    def handle_attack(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] and not self.attacking:
            self.attacking = True
            self.attack_index = 0  # Reinicia el índice al empezar a atacar

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
        if self.alive:
            self.alive = False              # activa estado de muerte
            self.speed = 0                  # no se puede mover
            self.death_index = 0            # reinicia animación desde el frame 0
            self.death_anim_finished = False

            if player_death_sound:
                player_death_sound.play()

            print("¡El jugador ha muerto uwu!")

    def take_hit(self, damage=1):
        if not self.alive:
            return

        self.health -= damage
        print(f"HP del jugador: {self.health}")

        if self.health <= 0:
            self.die()
