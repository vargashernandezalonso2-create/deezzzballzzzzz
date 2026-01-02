# Plinko - Escape Mode

Sistema modular de juego tipo Plinko con motor de físicas Pymunk.

## 📁 Estructura del Proyecto

```
plinko/
├── main.py              # Punto de entrada del programa
├── game.py              # Clase principal del juego
├── levels.py            # Lector e intérprete de configuraciones JSON
├── ring.py              # Clase Ring (anillo con apertura)
└── level_config.json    # Configuraciones de todos los niveles
```

## 🎯 Arquitectura Modular

### `levels.py`
- Clase `LevelConfig` que lee y valida el JSON
- Métodos:
  - `get_level(level_name)` - Obtiene config de un nivel
  - `validate_level(level)` - Valida estructura del nivel
  - `list_available_levels()` - Lista todos los niveles
  - `get_level_info(level_name)` - Info resumida de un nivel

### `ring.py`
- Clase `Ring` que representa un anillo con apertura
- Todo es paramétrico (radio, ángulo del gap, tamaño del gap)
- Detecta cuando la bola escapa por su apertura
- Se puede destruir cuando la bola escapa

### `game.py`
- Clase `PlinkoGame` que maneja toda la lógica del juego
- Usa `LevelConfig` para cargar niveles
- Crea instancias de `Ring` según la configuración
- Maneja físicas, timer, detección de victoria/derrota

## 📋 Formato del JSON

Cada nivel en `level_config.json` tiene esta estructura:

```json
{
  "type": "escape",
  "description": "Descripción del nivel",
  "rings_no": 20,
  "timer": 30,
  "ball_start": "center",
  "rings": {
    "thickness": 8,
    "elasticity": 0.9,
    "friction": 0.3,
    "ring_configs": [
      {"radius": 30, "gap_angle": 0, "gap_size": 45},
      {"radius": 47, "gap_angle": 85, "gap_size": 45}
    ]
  },
  "ball": {
    "radius": 12,
    "mass": 1,
    "elasticity": 0.7,
    "friction": 0.5
  },
  "gravity": [0, 400],
  "colors": {
    "background": [20, 20, 30],
    "rings": [255, 180, 100],
    "ball": [255, 255, 255],
    "timer_text": [255, 220, 100]
  }
}
```

### Parámetros Clave

- `ring_configs`: Array donde **cada anillo tiene su configuración específica**
  - `radius`: Radio del anillo (en píxeles)
  - `gap_angle`: Ángulo donde está el gap (0-360 grados)
  - `gap_size`: Tamaño del gap en grados
- **Nada es aleatorio** - Todo es paramétrico y definido en el JSON

## 🎮 Controles

- **R** - Reiniciar nivel
- **ESC** - Salir del juego

## 🚀 Cómo Usar

### Instalación
```bash
pip install pymunk pygame
```

### Ejecutar
```bash
python main.py
```

O directamente con un nivel específico:
```bash
python game.py  # Usa "escape1" por defecto
```

### Crear Nuevos Niveles

1. Abre `level_config.json`
2. Agrega un nuevo nivel en el objeto `levels`
3. Define todos los parámetros (ver formato arriba)
4. Guarda el archivo
5. Ejecuta el juego

Ejemplo rápido:
```json
"mi_nivel": {
  "type": "escape",
  "description": "Mi nivel custom",
  "rings_no": 10,
  "timer": 40,
  "rings": {
    "thickness": 8,
    "elasticity": 0.9,
    "friction": 0.3,
    "ring_configs": [
      {"radius": 50, "gap_angle": 0, "gap_size": 50},
      {"radius": 100, "gap_angle": 90, "gap_size": 50}
    ]
  }
}
```

## 🔧 Ventajas del Sistema Modular

1. **Separación de responsabilidades**
   - `levels.py` solo lee y valida JSON
   - `ring.py` solo maneja lógica de anillos
   - `game.py` solo coordina el juego

2. **Fácil de extender**
   - Agregar nuevos tipos de obstáculos → crear nueva clase
   - Agregar nuevos modos de juego → modificar solo `game.py`
   - Nuevos niveles → solo editar JSON

3. **Todo paramétrico**
   - Cero valores hardcodeados
   - Cero aleatoriedad (a menos que lo agregues en el JSON)
   - Todo configurable desde JSON

4. **Fácil de testear**
   - Cada clase se puede probar independientemente
   - Crear niveles de prueba es trivial

## 📝 Próximas Funcionalidades

- [ ] Más tipos de obstáculos
- [ ] Sistema de audio
- [ ] Pantalla de selección de niveles
- [ ] Sistema de puntajes
- [ ] Efectos visuales al destruir anillos