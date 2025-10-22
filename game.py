import pygame
from player import Player
from sword import Sword
from enemy import Enemy
from pytmx.util_pygame import load_pygame
from pytmx import TiledTileLayer, TiledImageLayer, TiledObjectGroup
import pytmx
from boss import Boss
from ffpyplayer.player import MediaPlayer

pygame.init()
WIDTH, HEIGHT = 800, 580
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

MUSIC_FILE = 'source/sfx/A Nocturne for All.mp3'

try:
    pygame.mixer.music.load(MUSIC_FILE)
    print(f"Música de fondo cargada: {MUSIC_FILE}")
except pygame.error as e:
    print(f"Error al cargar la música: {e}")

try:
    # 🌟 Carga ÚNICA del sonido en una variable global o una constante 🌟
    ENEMY_DEATH_SOUND = pygame.mixer.Sound('source/sfx/punch.mp3')
    PLAYER_DEATH_SOUND = pygame.mixer.Sound('source/sfx/diePlayer.wav')
except pygame.error as e:
    print(f"Error al cargar el sonido: {e}")
    ENEMY_DEATH_SOUND = PLAYER_DEATH_SOUND = None

# Colores
WHITE = (255,255,255)
GRAY = (100,100,100)
collision_tiles = []
# --- CARGAR VARIOS MAPAS ---
#map_files = ['mapa/nivel2_0.tmx', 'mapa/nivel2_1.tmx']
#mapas = [load_pygame(f) for f in map_files]
#
zonas = [
    ['mapa/nivel1_0.tmx', 'mapa/nivel1_1.tmx'],
    ['mapa/nivel2_0.tmx', 'mapa/nivel2_1.tmx']
]

zona_actual = 0
def cargar_zona(zona_idx):
    global mapas, map_offsets, mapas_y_offsets, tmx_data, collision_tiles, MAP_WIDTH, MAP_HEIGHT
    mapas = [load_pygame(f) for f in zonas[zona_idx]]

    # Calcular offsets de cada mapa para render y colisiones
    map_offsets = [0]
    for i in range(1, len(mapas)):
        prev = mapas[i-1]
        map_offsets.append(map_offsets[-1] + prev.width * prev.tilewidth)
    
    mapas_y_offsets = list(zip(mapas, map_offsets))

    # MAP_WIDTH de toda la zona
    MAP_WIDTH = sum(m.width * m.tilewidth for m in mapas)
    MAP_HEIGHT = mapas[0].height * mapas[0].tileheight  # asumimos misma altura

    # Cargar todas las colisiones de todos los mapas
    collision_tiles.clear()
    for mapa, offset_x in mapas_y_offsets:
        for layer in mapa.layers:
            if layer.name == 'piso' and isinstance(layer, TiledTileLayer):
                for x, y, gid in layer:
                    if gid != 0:
                        rect = pygame.Rect(x * mapa.tilewidth + offset_x,
                                           y * mapa.tileheight,
                                           mapa.tilewidth,
                                           mapa.tileheight)
                        collision_tiles.append(rect)

    # Usamos el primer mapa para tmx_data, solo para render_map inicial
    tmx_data = mapas[0]

cargar_zona(zona_actual)

def cargar_enemigos_zona(mapas_y_offsets, enemigos_sprites):
    enemigos_sprites.empty()
    for tmx_data, offset_x in mapas_y_offsets:
        print(f"🗺️ Procesando mapa con offset {offset_x}")
        for layer in tmx_data.layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                if layer.name == "Enemy":
                    print(f"📦 Capa Enemy encontrada con {len(layer)} objetos")
                    for obj in layer:
                        x = obj.x + offset_x
                        y = obj.y - 100
                        # Si hay patrol_end en propiedades, úsalo; si no, patrulla 200px a la derecha
                        patrol_end = obj.properties.get("patrol_end", None)
                        if patrol_end is None:
                            patrol_end = x + 200  # Patrulla hacia la DERECHA
                        else:
                            patrol_end += offset_x  # También sumar offset si viene de Tiled
                        
                        enemigo = Enemy((x, y), (x, patrol_end))
                        enemigos_sprites.add(enemigo)
                        print(f"✅ Enemigo: inicio={x}, fin={patrol_end}")


def cargar_boss_zona(mapas_y_offsets, bosses_sprites):
    """
    Carga bosses desde la capa 'boss' de cada mapa uwu.
    Usa los offsets que ya están precomputados por cargar_zona().
    """
    bosses_sprites.empty()

    for mapa, offset_x in mapas_y_offsets:
        for layer in mapa.layers:
            if layer.name.lower() == "boss":
                print(f"🐍 Capa 'boss' detectada en mapa con offset {offset_x}")
                for obj in layer:
                    if zona_actual == 0:
                        sprite_set = "gorgona"
                        video_path = "source/videos/finalNivel1.mp4"
                        minuz = 100
                    elif zona_actual == 1:
                        sprite_set = "boss2"
                        video_path = "source/videos/fianlNivel2.mp4"
                        minuz = 55
                    else:
                        sprite_set = "gorgona" 
                    # posición global del boss sumando offset
                    pos = (obj.x + offset_x, obj.y - minuz)
                    print(f"🧿 Boss colocado en {pos}")
                    
                    # rango de patrulla del boss
                    patrol_range = (pos[0] - 150, pos[0] + 150)


                    boss = Boss(pos, patrol_range=patrol_range, sprite_set=sprite_set, health=20, video_path=video_path)
                    bosses_sprites.add(boss)


def reproducir_video(video_path):
    video = MediaPlayer(video_path)
    playing = True

    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        frame, val = video.get_frame()
        if val == 'eof':
            playing = False
            break
        if frame is not None:
            img, t = frame
            video_width, video_height = img.get_size()
            screen_width, screen_height = 800, 600

            # Calcular escala manteniendo aspect ratio
            scale_w = screen_width / video_width
            scale_h = screen_height / video_height
            scale = min(scale_w, scale_h)  # escala para que quepa sin recortar

            new_w = int(video_width * scale)
            new_h = int(video_height * scale)

            # Convertir frame a superficie de pygame
            frame_surf = pygame.image.frombuffer(img.to_bytearray()[0], img.get_size(), 'RGB')
            frame_surf = pygame.transform.scale(frame_surf, (new_w, new_h))

            # Calcular offset para centrar
            offset_x = (screen_width - new_w) // 2
            offset_y = (screen_height - new_h) // 2

            # Pintar en pantalla centrado
            screen.fill((0,0,0))  # fondo negro
            screen.blit(frame_surf, (offset_x, offset_y))
            pygame.display.flip()
            clock.tick(30)

# Calcular offsets acumulativos para que se dibujen seguidos
map_offsets = [0]
for i in range(1, len(mapas)):
    prev = mapas[i-1]
    map_offsets.append(map_offsets[-1] + prev.width * prev.tilewidth)

mapas_y_offsets = list(zip(mapas, map_offsets))

# --- USAR EL PRIMER MAPA PARA DATOS BASE ---
tmx_data = mapas[0]
TILESIZE = tmx_data.tilewidth
MAP_WIDTH = sum(m.width * m.tilewidth for m in mapas)
MAP_HEIGHT = tmx_data.height * TILESIZE



# --- EXTRAER TILES DE COLISIÓN ---
collision_layer = None
for layer in tmx_data.layers:
    if layer.name == 'piso':
        if isinstance(layer, TiledTileLayer):
            print(f"Usando capa '{layer.name}' como colisiones 💫")
            collision_layer = layer
            break

if not collision_layer:
    print("😿 No se encontró ninguna capa de teselas.")
else:
    for x, y, gid in collision_layer:
        if gid != 0:
            rect = pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
            collision_tiles.append(rect)

# --- JUGADOR Y ESPADA ---
player = Player((50, 50))
player.update(collision_tiles)
sword = Sword(player)
player.sword = sword

enemigos_sprites = pygame.sprite.Group()
cargar_enemigos_zona(mapas_y_offsets, enemigos_sprites)



all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(sword)

def fade_out():
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill((0, 0, 0))
    for alpha in range(0, 255, 10):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)

def fade_in():
    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.fill((0, 0, 0))
    for alpha in range(255, 0, -10):
        fade.set_alpha(alpha)
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)

def reproducir_video_intro(video_path):
    player = MediaPlayer(video_path)
    playing = True

    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        frame, val = player.get_frame()
        if val == 'eof':
            playing = False
            break

        if frame is not None:
            img, t = frame
            video_width, video_height = img.get_size()
            
            # Escala para que quepa en la pantalla sin deformar
            scale_w = WIDTH / video_width
            scale_h = HEIGHT / video_height
            scale = min(scale_w, scale_h)
            new_w = int(video_width * scale)
            new_h = int(video_height * scale)

            # Convertir frame a superficie pygame
            frame_surf = pygame.image.frombuffer(img.to_bytearray()[0], img.get_size(), 'RGB')
            frame_surf = pygame.transform.scale(frame_surf, (new_w, new_h))

            # Calcular offsets para centrar
            offset_x = (WIDTH - new_w) // 2
            offset_y = (HEIGHT - new_h) // 2

            # Dibujar video
            screen.fill((0,0,0))
            screen.blit(frame_surf, (offset_x, offset_y))
            pygame.display.flip()
            clock.tick(30)

# --- FUNCIÓN DE RENDERIZADO MULTIMAPA ---
def render_map(offset_x, offset_y, mapas_y_offsets=None):
    PARALLAX_FACTOR = 0.5

    if mapas_y_offsets:
        for tmx_data, base_x in mapas_y_offsets:
            for layer in tmx_data.visible_layers:
                if isinstance(layer, pytmx.TiledImageLayer):
                    if layer.image:
                        screen.blit(layer.image, ((offset_x + base_x) * PARALLAX_FACTOR,
                                                  offset_y * PARALLAX_FACTOR))

                elif isinstance(layer, pytmx.TiledTileLayer) and layer.name != 'Colisiones':
                    for x, y, gid in layer:
                        tile = tmx_data.get_tile_image_by_gid(gid)
                        if tile:
                            pos_x = base_x + x * tmx_data.tilewidth + offset_x
                            pos_y = y * tmx_data.tileheight + offset_y
                            tile_height = tile.get_height()
                            pos_y += tmx_data.tileheight - tile_height
                            screen.blit(tile, (pos_x, pos_y))
    else:
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledImageLayer):
                if layer.image:
                    screen.blit(layer.image, (offset_x * PARALLAX_FACTOR,
                                              offset_y * PARALLAX_FACTOR))

            elif isinstance(layer, pytmx.TiledTileLayer) and layer.name != 'Colisiones':
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        pos_x = x * TILESIZE + offset_x
                        pos_y = y * TILESIZE + offset_y
                        tile_height = tile.get_height()
                        pos_y += TILESIZE - tile_height
                        screen.blit(tile, (pos_x, pos_y))

if 'MUSIC_FILE' in locals() and not pygame.mixer.music.get_busy():
    # El valor -1 indica bucle infinito. El 0.0 indica iniciar desde el principio.
    pygame.mixer.music.play(-1, 0.0) 
    pygame.mixer.music.set_volume(0.3)  # 30% de volumen, bajito uwu
    print("Reproduciendo música de fondo...")

# 👹 Grupo de bosses
bosses_sprites = pygame.sprite.Group()

# Cargar bosses de la zona actual
cargar_boss_zona(mapas_y_offsets, bosses_sprites)
# --- BUCLE PRINCIPAL ---

reproducir_video_intro("source/videos/inicio.mp4")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update(collision_tiles)
    enemigos_sprites.update(collision_tiles)
    bosses_sprites.update(collision_tiles, player)

    screen.fill((0, 0, 0))

    # 1. Ejecutar updates solo si el jugador está vivo
    # 1. Ejecutar updates solo si el jugador está vivo
    if player.alive:
        all_sprites.update(collision_tiles)
        enemigos_sprites.update(collision_tiles)
    
        # --- LÓGICA DE DETECCIÓN DE DAÑO AL JUGADOR (Corregida) ---
        
        # Obtener la lista de todos los enemigos que colisionan con el jugador
        # El último False indica que no queremos eliminar los enemigos del grupo automáticamente
        colliding_enemies = pygame.sprite.spritecollide(player, enemigos_sprites, False) 
        
        for enemy in colliding_enemies:
            # ¡IMPORTANTE! Solo si el enemigo NO está en estado "dead" puede causar daño.
            if enemy.state != "dead": 
                player.die(PLAYER_DEATH_SOUND)
                break # El jugador ha muerto, no necesitamos revisar más enemigos
        colliding_bosses = pygame.sprite.spritecollide(player, bosses_sprites, False)
        for boss in colliding_bosses:
            if boss.state != "dead" and boss.state == "attack":
                player.take_hit()
                break  # Detiene más daños en el mismo frame uwu
            if boss.health <= 0 and not boss.video_played:
                boss.video_played = True
                if boss.video_path:
                    reproducir_video(boss.video_path)
    if not player.alive:
        fade_out() # Oscurece la pantalla

        # Pausa temporal para el efecto de muerte
        pygame.time.wait(300) 
        
        # --- REINICIO DE POSICIÓN Y ESTADO ---
        # 1. Reiniciar posición del jugador
        player.rect.topleft = player.initial_pos
        player.vel_y = 0 # Reinicia gravedad
        player.direction = "right"
        
        # 2. Restablecer el estado de vida del jugador
        player.alive = True
        player.speed = 3 # Restaura la velocidad original
        
        # 3. Recargar enemigos (si no quieres que los enemigos muertos revivan, omite esto)
        #    Si los enemigos deben revivir al morir el jugador:
        #    cargar_enemigos_zona(mapas_y_offsets, enemigos_sprites)

        fade_in() # Aclara la pantalla

    if sword.visible:
        # 2. Usamos spritecollide para ver qué enemigos chocan con la espada.
        #    False/False indica que no borramos la espada ni los enemigos automáticamente.
        hit_enemies = pygame.sprite.spritecollide(sword, enemigos_sprites, False)

        for enemy in hit_enemies:
            # 3. Llamamos al método que implementamos en el enemigo
            enemy.take_hit(ENEMY_DEATH_SOUND)

    # --- CÁMARA ---
    camera_x_offset = WIDTH // 2 - player.rect.centerx
    if camera_x_offset > 0:
        camera_x_offset = 0
    elif camera_x_offset < WIDTH - MAP_WIDTH:
        camera_x_offset = WIDTH - MAP_WIDTH

    camera_y_offset = HEIGHT // 2 - player.rect.centery
    if camera_y_offset > 0:
        camera_y_offset = 0
    elif camera_y_offset < HEIGHT - MAP_HEIGHT:
        camera_y_offset = HEIGHT - MAP_HEIGHT

    # --- DIBUJAR MAPAS CONTINUOS ---
    render_map(camera_x_offset, camera_y_offset, mapas_y_offsets)
    if player.rect.x > MAP_WIDTH - 50:  # Ajusta margen si quieres
        fade_out()
        zona_actual += 1
        if zona_actual < len(zonas):
            cargar_zona(zona_actual)
            cargar_enemigos_zona(mapas_y_offsets, enemigos_sprites)
            cargar_boss_zona(mapas_y_offsets, bosses_sprites)
            player.rect.x = 50  # Posición inicial del nuevo mapa
            fade_in()
        else:
            print("¡Fin del juego uwu!")
            running = False
    bosses_sprites.update(collision_tiles, player)
    for boss in bosses_sprites:
        draw_x = boss.rect.x + camera_x_offset
        draw_y = boss.rect.y + camera_y_offset
        screen.blit(boss.image, (draw_x, draw_y))

    for enemigo in enemigos_sprites:
        draw_position_x = enemigo.rect.x + camera_x_offset
        draw_position_y = enemigo.rect.y + camera_y_offset
        screen.blit(enemigo.image, (draw_position_x, draw_position_y))
        #print(f"🎨 Dibujando enemigo en pantalla: ({draw_position_x}, {draw_position_y})")  # Debug


    # --- DIBUJAR SPRITES ---
    for sprite in all_sprites:
        if sprite is sword and not sprite.visible:
            continue
        draw_position_x = sprite.rect.x + camera_x_offset
        draw_position_y = sprite.rect.y + camera_y_offset
        screen.blit(sprite.image, (draw_position_x, draw_position_y))

    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
