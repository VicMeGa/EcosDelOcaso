# Manual de Clases - enemy.py

## Descripción General
El archivo `enemy.py` contiene la clase `Enemy` que representa a los enemigos en el juego. Esta clase hereda de `pygame.sprite.Sprite` y gestiona el comportamiento, animaciones y estado de los enemigos.

---

## Clase: Enemy

### Herencia
```python
class Enemy(pygame.sprite.Sprite)
```
Hereda de `pygame.sprite.Sprite` para aprovechar el sistema de sprites de Pygame.

---

## Constructor

### `__init__(self, pos, patrol_range=(0,0), speed=1)`

Inicializa una nueva instancia de Enemy.

#### Parámetros:
- **pos** (tuple): Posición inicial del enemigo en formato (x, y)
- **patrol_range** (tuple, opcional): Rango de patrullaje en formato (inicio_x, fin_x). Por defecto: (0, 0)
- **speed** (int, opcional): Velocidad de movimiento del enemigo. Por defecto: 1

#### Atributos inicializados:

##### Animaciones:
- **walk_right**: Lista de 6 imágenes para la animación de caminar hacia la derecha
- **walk_left**: Versión invertida de walk_right
- **idle_right**: Lista de 4 imágenes para la animación de reposo hacia la derecha
- **idle_left**: Versión invertida de idle_right
- **attack_right**: Lista de 6 imágenes para la animación de ataque hacia la derecha
- **attack_left**: Versión invertida de attack_right
- **dead**: Lista de 6 imágenes para la animación de muerte

##### Atributos de control:
- **image**: Imagen actual del sprite
- **rect**: Rectángulo de colisión del sprite
- **speed**: Velocidad de movimiento
- **direction**: Dirección de movimiento (1 = derecha, -1 = izquierda)
- **start_x, end_x**: Límites del rango de patrullaje
- **anim_index**: Índice de la animación actual
- **state**: Estado actual del enemigo ("idle", "walk", "attack", "dead")

#### Ejemplo de uso:
```python
# Crear un enemigo en la posición (100, 400)
# que patrulla entre x=50 y x=300
# con velocidad 2
enemy = Enemy(pos=(100, 400), patrol_range=(50, 300), speed=2)
```

---

## Métodos

### `update(self, collision_tiles=None)`

Método principal que actualiza el estado del enemigo en cada frame.

#### Parámetros:
- **collision_tiles** (list, opcional): Lista de tiles con los que puede colisionar. Por defecto: None

#### Funcionalidad:
1. Ejecuta la lógica de patrullaje
2. Maneja las colisiones
3. Actualiza la animación

#### Ejemplo de uso:
```python
# En el bucle principal del juego
enemy.update(collision_tiles=level_tiles)
```

---

### `patrol(self)`

Controla el movimiento de patrullaje del enemigo.

#### Funcionalidad:
- Mueve al enemigo horizontalmente según su velocidad y dirección
- Invierte la dirección cuando alcanza los límites del rango de patrullaje
- No se ejecuta si el enemigo está muerto (state == "dead")

#### Lógica:
```python
# Movimiento: posición += velocidad * dirección
# Si sale del rango: dirección *= -1 (invierte)
```

---

### `animate(self, collision_tiles=None)`

Gestiona las animaciones del enemigo según su estado actual.

#### Parámetros:
- **collision_tiles**: Parámetro heredado, no utilizado en esta versión

#### Funcionalidad:
- Incrementa el índice de animación en 0.2 por frame
- Selecciona el conjunto de frames según el estado actual
- Considera la dirección para elegir entre animaciones izquierda/derecha
- En estado "dead", mantiene el último frame de la animación

#### Estados y animaciones:
| Estado | Animación derecha | Animación izquierda |
|--------|------------------|---------------------|
| "idle" | idle_right | idle_left |
| "walk" | walk_right | walk_left |
| "attack" | attack_right | attack_left |
| "dead" | dead | dead |

---

### `handle_collision(self, tiles)`

Maneja las colisiones del enemigo con tiles del escenario.

#### Parámetros:
- **tiles** (list): Lista de rectángulos de colisión de tiles

#### Funcionalidad:
- Verifica colisiones con cada tile
- Ajusta la posición del enemigo para evitar superposición
- Invierte la dirección de movimiento al colisionar

#### Lógica de colisión:
```
Si va hacia la derecha → Ajusta a la izquierda del tile
Si va hacia la izquierda → Ajusta a la derecha del tile
Siempre invierte la dirección tras colisionar
```

---

### `take_hit(self, death_sound=None)`

Ejecuta la muerte del enemigo cuando recibe un golpe mortal.

#### Parámetros:
- **death_sound** (pygame.Sound, opcional): Sonido a reproducir al morir. Por defecto: None

#### Funcionalidad:
- Cambia el estado a "dead" si no estaba ya muerto
- Reinicia el índice de animación para reproducir la animación de muerte
- Detiene el movimiento (speed = 0)
- Reproduce el sonido de muerte si se proporciona

#### Ejemplo de uso:
```python
# Cuando el jugador golpea al enemigo
if player.attacking and player.rect.colliderect(enemy.rect):
    enemy.take_hit(death_sound=death_sfx)
```

---

## Diagrama de Estados

```
         ┌─────┐
    ┌───→│IDLE │←───┐
    │    └─────┘    │
    │       │       │
    │       ↓       │
    │    ┌─────┐   │
    └────│WALK │───┘
         └─────┘
            │
            ↓ (al recibir golpe)
         ┌─────┐
         │DEAD │ (estado final)
         └─────┘
```

---

## Flujo de Ejecución

### En cada frame del juego:
1. **update()** se llama desde el bucle principal
2. **patrol()** mueve al enemigo dentro de su rango
3. **handle_collision()** verifica y resuelve colisiones
4. **animate()** actualiza la imagen mostrada
5. Si recibe un golpe → **take_hit()** cambia a estado "dead"

---

## Dependencias

### Librerías requeridas:
- **pygame**: Para manejo de sprites, imágenes y rectángulos

### Archivos necesarios:
```
enemies/enemi1/
├── walk/
│   ├── walk1.png a walk6.png
├── idle/
│   ├── idle1.png a idle4.png
├── atack/
│   ├── atack1.png a atack6.png
└── dead/
    ├── dead1.png a dead6.png
```

---

## Ejemplo de Implementación Completa

```python
import pygame
from enemy import Enemy

# Inicializar pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Cargar sonido de muerte (opcional)
death_sound = pygame.mixer.Sound("source/sfx/enemy_death.wav")

# Crear grupo de enemigos
enemies = pygame.sprite.Group()

# Crear enemigos
enemy1 = Enemy(pos=(200, 400), patrol_range=(100, 400), speed=2)
enemy2 = Enemy(pos=(600, 400), patrol_range=(500, 700), speed=1.5)

enemies.add(enemy1, enemy2)

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Actualizar enemigos
    enemies.update(collision_tiles=None)
    
    # Dibujar
    screen.fill((0, 0, 0))
    enemies.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

---

## Posibles Mejoras

### Sugerencias para extender la funcionalidad:

1. **Sistema de vida**: Agregar atributo `health` para permitir múltiples golpes
2. **Detección de jugador**: Implementar método para detectar y perseguir al jugador
3. **Ataque automático**: Activar estado "attack" cuando el jugador está cerca
4. **IA más compleja**: Estados adicionales como "chase", "flee", "guard"
5. **Diferentes tipos**: Subclases para enemigos con comportamientos distintos
6. **Drops**: Generar items al morir
7. **Sonidos adicionales**: Agregar efectos de sonido para caminar y atacar

---

## Notas Técnicas

### Velocidad de animación:
- El índice se incrementa en **0.2** por frame
- A 60 FPS, esto significa ~12 frames por segundo de animación
- Ajusta este valor para animaciones más rápidas o lentas

### Dirección:
- **direction = 1**: Movimiento hacia la derecha
- **direction = -1**: Movimiento hacia la izquierda

### Optimización:
- Las imágenes se cargan una sola vez en `__init__()`
- Se usan flip de pygame en lugar de cargar imágenes duplicadas

---

## Autor y Versión

- **Archivo**: enemy.py
- **Proyecto**: EcosDelOcaso
- **Fecha de documentación**: 23 de octubre de 2025

---

## Licencia

Este manual de documentación está sujeto a la misma licencia que el proyecto EcosDelOcaso.
