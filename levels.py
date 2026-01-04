import json

class LevelConfig:
    def __init__(self, config_file='level_config.json'):
        # aaa inicializamos con el path del JSON -bynd
        self.config_file = config_file
        self.level_data = None
        self.load_config()
    
    def load_config(self):
        # ey cargamos el archivo JSON directo -bynd
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.level_data = json.load(f)
                print(f"✅ Configuración cargada desde {self.config_file}")
                return True
        except FileNotFoundError:
            print(f"❌ No se encontró {self.config_file}")
            self.level_data = None
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Error al parsear JSON: {e}")
            self.level_data = None
            return False
    
    def get_level(self):
        # vavavava obtenemos la config del nivel sin parámetros -bynd
        if not self.level_data:
            print(f"⚠️ No hay datos cargados, usando config por defecto")
            return self.get_default_level()
        
        # chintrolas validamos q tenga todos los campos necesarios -bynd
        if self.validate_level(self.level_data):
            print(f"✅ Nivel cargado correctamente")
            return self.level_data
        else:
            print(f"⚠️ El nivel tiene campos faltantes")
            return self.get_default_level()
    
    def validate_level(self, level):
        # q chidoteee validamos que el nivel tenga estructura correcta -bynd
        game_type = level.get('type', 'escape')
        
        # ala campos comunes a todos los modos -bynd
        common_fields = ['type', 'rings', 'gravity', 'colors']
        
        for field in common_fields:
            if field not in level:
                print(f"   ❌ Falta campo: {field}")
                return False
        
        # fokeis validamos sub-campos -bynd
        if 'ring_configs' not in level['rings']:
            print(f"   ❌ Falta rings.ring_configs")
            return False
        
        # vavavava validación específica por modo -bynd
        if game_type == '8ball':
            if 'question' not in level:
                print(f"   ⚠️ Falta 'question' para modo 8ball")
            if 'ball_yes' not in level or 'ball_no' not in level:
                print(f"   ❌ Faltan 'ball_yes' o 'ball_no' para modo 8ball")
                return False
        elif game_type == 'elimination':
            if 'ball_timer' not in level or 'max_balls' not in level:
                print(f"   ❌ Faltan 'ball_timer' o 'max_balls' para modo elimination")
                return False
        else:  # escape o cualquier otro
            if 'ball' not in level:
                print(f"   ❌ Falta 'ball' para modo escape")
                return False
        
        return True
    
    def get_default_level(self):
        # fokeis config por defecto si algo falla -bynd
        print("📋 Usando configuración por defecto")
        return {
            "type": "escape",
            "description": "Nivel por defecto",
            "rings_no": 10,
            "timer": 30,
            "ball_start": "center",
            "rings": {
                "thickness": 8,
                "elasticity": 0.9,
                "friction": 0.3,
                "ring_configs": [
                    {"radius": 50, "gap_angle": 0, "gap_size": 45},
                    {"radius": 80, "gap_angle": 90, "gap_size": 45},
                    {"radius": 110, "gap_angle": 180, "gap_size": 45},
                    {"radius": 140, "gap_angle": 270, "gap_size": 45},
                    {"radius": 170, "gap_angle": 45, "gap_size": 45},
                    {"radius": 200, "gap_angle": 135, "gap_size": 45},
                    {"radius": 230, "gap_angle": 225, "gap_size": 45},
                    {"radius": 260, "gap_angle": 315, "gap_size": 45},
                    {"radius": 290, "gap_angle": 60, "gap_size": 45},
                    {"radius": 320, "gap_angle": 150, "gap_size": 45}
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
    
    def get_level_info(self):
        # vavavava info resumida del nivel -bynd
        level = self.get_level()
        
        if not level:
            return None
        
        info = {
            'type': level.get('type', 'unknown'),
            'description': level.get('description', 'Sin descripción'),
            'rings_no': level.get('rings_no', len(level.get('rings', {}).get('ring_configs', []))),
            'timer': level.get('timer', 0)
        }
        
        return info
