# Ecos del Ocaso

Un juego de acción y aventura 2D desarrollado en Python con Pygame, que combina combate dinámico, exploración de múltiples niveles y enfrentamientos épicos contra jefes.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Descripción

**Ecos del Ocaso** es un juego de plataformas 2D donde controlas a un valiente guerrero que debe atravesar 8 zonas diferentes, cada una con sus propios enemigos y desafíos. El juego presenta:

- **8 zonas únicas** con mapas continuos creados en Tiled
- **Sistema de combate** con espada y animaciones fluidas
- **Múltiples tipos de enemigos** con IA de patrullaje
- **8 jefes épicos** con diferentes comportamientos y sprites
- **Cinemáticas** entre niveles usando videos
- **Música y efectos de sonido** inmersivos
- **Sistema de muerte y respawn**

## Características Principales

### Sistema de Combate

- Ataques con espada animados
- Detección de colisiones con enemigos
- Sistema de salud para jugador y enemigos
- Efectos de sonido para cada acción

### Enemigos y Jefes

- **Enemigos regulares**: Patrullaje automático con IA básica
- **Jefes de zona**:
  - Gorgona (Zona 1)
  - Boss2 (Zona 2)
  - Kitsune (Zona 3)
  - Minotauro (Zona 4)
  - Ninja (Zona 5)
  - Caballero (Zona 6)
  - Tengu 1 (Zona 7)
  - Tengu 2 (Zona 8)

### Mapas y Niveles

- Mapas creados con Tiled Map Editor
- Sistema de carga dinámica de zonas
- Transiciones suaves entre niveles
- Colisiones con tiles del escenario

## Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**

```bash
git clone https://github.com/VicMeGa/EcosDelOcaso.git
cd EcosDelOcaso
```

2. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

3. **Ejecutar el juego**

```bash
python3 game.py
```

## Dependencias

El proyecto utiliza las siguientes librerías (ver `requirements.txt`):

```
pygame==2.6.1       # Motor del juego
PyTMX==3.32        # Carga de mapas Tiled
ffpyplayer==4.5.3  # Reproducción de videos
Pillow==12.0.0     # Procesamiento de imágenes
```

## Controles

| Tecla               | Acción               |
| ------------------- | -------------------- |
| ⬅️ Flecha Izquierda | Mover a la izquierda |
| ➡️ Flecha Derecha   | Mover a la derecha   |
| Espacio             | Saltar               |
| Z                   | Atacar con espada    |

## Estructura del Proyecto

```
EcosDelOcaso/
├── game.py              # Archivo principal del juego
├── player.py            # Clase del jugador
├── enemy.py             # Clase de enemigos regulares
├── boss.py              # Clase de jefes
├── sword.py             # Clase de la espada
├── menu.py              # Sistema de menús
├── resize.py            # Utilidad de redimensionamiento
├── requirements.txt     # Dependencias del proyecto
├── MANUAL_ENEMY.md      # Documentación de enemigos
│
├── enemies/             # Sprites de enemigos
│   ├── boss2/
│   ├── enemi1/
│   ├── gorgona/
│   ├── kitsune/
│   ├── knight/
│   ├── minotaur/
│   ├── ninja/
│   ├── tengu1/
│   └── tengu2/
│
├── mapa/                # Mapas y tilesets de Tiled
│   ├── nivel1_0.tmx
│   ├── nivel1_1.tmx
│   ├── ...
│   └── [recursos gráficos]
│
├── source/              # Recursos del jugador
│   ├── player/          # Sprites del jugador
│   ├── sfx/             # Efectos de sonido
│   └── videos/          # Cinemáticas
│
└── menu/                # Recursos del menú
```

## Sistema de Sprites

### Jugador

- **Idle**: Animación de reposo
- **Run**: Animación de carrera (7 frames)
- **Jump**: Animación de salto (subida/bajada)
- **Attack**: Animación de ataque (6 frames)
- **Death**: Animación de muerte (8 frames)

### Enemigos

Cada enemigo tiene 4 conjuntos de animaciones:

- **Walk**: Patrullaje
- **Idle**: Reposo
- **Attack**: Ataque
- **Dead**: Muerte

## Desarrollo

### Arquitectura del Código

El juego sigue una arquitectura orientada a objetos:

- **`Player`**: Controla el personaje principal, movimiento y animaciones
- **`Enemy`**: Gestiona enemigos con IA de patrullaje
- **`Boss`**: Extiende Enemy con comportamiento de persecución y mayor complejidad
- **`Sword`**: Maneja el arma del jugador y detección de golpes

### Sistema de Cámara

Implementa una cámara que sigue al jugador:

- Centrada en el jugador
- Limitada a los bordes del mapa
- Soporte para mapas continuos

### Sistema de Colisiones

- Colisiones tile-based con el escenario
- Detección de colisiones jugador-enemigos
- Detección de golpes espada-enemigos
- Manejo de gravedad y física básica

## Cinemáticas

El juego incluye videos cinemáticos para:

- Introducción del juego
- Presentación de cada jefe
- Transiciones entre capítulos

Los videos se reproducen usando **ffpyplayer** con escala automática para ajustarse a la pantalla.

## Solución de Problemas

### El juego no inicia

- Verifica que todas las dependencias estén instaladas: `pip install -r requirements.txt`
- Asegúrate de estar usando Python 3.8 o superior

### Error al cargar recursos

- Verifica que todas las carpetas de recursos (`enemies/`, `source/`, `mapa/`) estén completas
- El juego usa rutas relativas, ejecuta desde la carpeta raíz del proyecto

## Notas de Desarrollo

### Características Implementadas

- ✅ Sistema de combate básico
- ✅ 8 zonas con mapas continuos
- ✅ 8 jefes únicos con comportamiento especial
- ✅ Sistema de muerte y respawn
- ✅ Cinemáticas entre niveles
- ✅ Música de fondo y SFX
- ✅ Animaciones fluidas


## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Créditos

### Recursos

- Sprites de personajes y enemigos: [CraftPix.net](https://craftpix.net/)
- Música: "A Nocturne for All"
- Tilesets y mapas: Varios recursos gratuitos

## Contacto

- **GitHub**: [@VicMeGa](https://github.com/VicMeGa)
- **Repositorio**: [EcosDelOcaso](https://github.com/VicMeGa/EcosDelOcaso)

## ¡Disfruta el juego!

¡Gracias por jugar **Ecos del Ocaso**! Si encuentras algún bug o tienes sugerencias, no dudes en abrir un issue en GitHub.

---

**Desarrollado con ❤️ usando Python y Pygame**
