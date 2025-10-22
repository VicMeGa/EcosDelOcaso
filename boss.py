import pygame

class Boss(pygame.sprite.Sprite):
    def __init__(self, pos, patrol_range=(0,0), speed=2, detection_range=300, health=20, sprite_set="gorgona", video_path=None):  # 🔧 Cambio: detection_range=300
        super().__init__()
        if sprite_set== "gorgona":
            lanw=14
            lanid=8
            lande=4
            lanat=8
        else:
            lanw=7
            lanid=5
            lande=5
            lanat=7
        self.video_played = False  # evita reproducir varias veces
        self.video_path = video_path
        # 🐾 Animaciones propias del boss
        self.walk_right = [pygame.image.load(f"enemies/{sprite_set}/walk/walk{i}.png").convert_alpha() for i in range(1,lanw)]
        self.walk_left = [pygame.transform.flip(img, True, False) for img in self.walk_right]

        self.idle_right = [pygame.image.load(f"enemies/{sprite_set}/idle/idle{i}.png").convert_alpha() for i in range(1,lanid)]
        self.idle_left = [pygame.transform.flip(img, True, False) for img in self.idle_right]

        self.attack_right = [pygame.image.load(f"enemies/{sprite_set}/atack/atack{i}.png").convert_alpha() for i in range(1,lanat)]
        self.attack_left = [pygame.transform.flip(img, True, False) for img in self.attack_right]

        self.dead = [pygame.image.load(f"enemies/{sprite_set}/dead/dead{i}.png").convert_alpha() for i in range(1,lande)]

        # Estado inicial
        self.image = self.idle_right[0]
        self.rect = self.image.get_rect(topleft=pos)

        # 🔧 Arreglo del patrol_range
        if patrol_range[0] == patrol_range[1]:
            # Si no hay rango, crear uno de 200px
            self.start_x = pos[0] - 100
            self.end_x = pos[0] + 100
        else:
            self.start_x, self.end_x = patrol_range
        
        print(f"🎯 Boss creado en {pos} | Patrol: {self.start_x} -> {self.end_x}")
        
        self.speed = speed
        self.direction = 1  # 1 = derecha, -1 = izquierda
        self.anim_index = 0
        self.state = "walk"
        self.health = health
        self.detection_range = detection_range  # 300px en vez de 150
        self.hit_cooldown = 0
        self.is_chasing = False
        self.attack_range = 100  # 🔧 Aumentado a 100px

    def update(self, tiles=None, player=None):
        # reducir cooldown
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

        self.check_player(player)
        self.move(tiles)
        self.check_player_hit(player)
        self.animate()

    def check_player(self, player):
        if not player or self.state == "dead":
            return
        
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = (dx**2 + dy**2)**0.5

        if distance < self.attack_range:
            # 🗡️ Muy cerca → atacar y detenerse
            self.state = "attack"
            self.is_chasing = False
            self.direction = 1 if dx > 0 else -1
            print(f"⚔️ ATACANDO - Distancia: {distance:.1f}")
        elif distance < self.detection_range:
            # 👁️ En rango de detección → perseguir
            self.state = "walk"
            self.is_chasing = True
            self.direction = 1 if dx > 0 else -1
            print(f"🏃 PERSIGUIENDO - Distancia: {distance:.1f}")
        else:
            # 🚶 Fuera de rango → patrullar normalmente
            self.is_chasing = False
            if self.state != "dead":
                self.state = "walk"

    def move(self, tiles=None):
        old_x = self.rect.x
        
        if self.state == "walk":
            if self.is_chasing:
                # 🏃 Perseguir al jugador
                self.rect.x += self.speed * self.direction
                print(f"🏃 Moviéndose hacia jugador: {old_x} -> {self.rect.x}")
            else:
                # 🚶 Patrullar normalmente
                self.rect.x += self.speed * self.direction
                if self.rect.x <= self.start_x:
                    self.rect.x = self.start_x
                    self.direction = 1
                elif self.rect.x >= self.end_x:
                    self.rect.x = self.end_x
                    self.direction = -1
        elif self.state == "attack":
            # 🛑 Detenerse completamente durante ataque
            pass

        # Colisiones con el suelo - 🔧 Comentado temporalmente para debug
        # if tiles:
        #     for tile in tiles:
        #         if self.rect.colliderect(tile):
        #             if self.direction > 0:
        #                 self.rect.right = tile.left
        #             else:
        #                 self.rect.left = tile.right

    def check_player_hit(self, player):
        if not player or self.state == "dead":
            return

        # 🗡️ Daño del player (espada)
        if hasattr(player, 'sword') and player.sword.visible and self.hit_cooldown == 0:
            if self.rect.colliderect(player.sword.rect):
                self.take_hit()
                self.hit_cooldown = 10

        # 💀 Daño al player si el boss ataca
        if self.state == "attack":
            if self.rect.colliderect(player.rect):
                if hasattr(player, 'take_damage') and self.hit_cooldown == 0:
                    player.take_damage(1)
                    self.hit_cooldown = 30

    def take_hit(self, damage=1, death_sound=None):
        self.health -= damage
        print(f"💥 Boss HP: {self.health}")
        if self.health <= 0 and self.state != "dead":
            self.state = "dead"
            self.anim_index = 0
            self.speed = 0
            print("💀 Boss derrotado!")
            if death_sound:
                death_sound.play()

    def animate(self):
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
                self.anim_index = len(frames) - 1
            else:
                self.anim_index = 0

        # 🔧 Mantener la posición del rect cuando cambia el sprite
        old_center = self.rect.center
        self.image = frames[int(self.anim_index)]
        self.rect = self.image.get_rect(center=old_center)