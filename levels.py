import json

class LevelConfig:
    def __init__(self, config_file='level_config.json'):
        # aaa inicializamos con el path del JSON -bynd
        self.config_file = config_file
        self.levels_data = None
        self.load_config()
    
    def load_config(self):
        # ey cargamos el archivo JSON -bynd
        try:
            with open(self.config_file, 'r') as f:
                self.levels_data = json.load(f)
                print(f"✅ Configuración cargada desde {self.config_file}")
                return True
        except FileNotFoundError:
            print(f"❌ No se encontró {self.config_file}")
            self.levels_data = None
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Error al parsear JSON: {e}")
            self.levels_data = None
            return False
    
    def get_level(self, level_name):
        # vavavava obtenemos la config de un nivel específico -bynd
        if not self.levels_data:
            print(f"⚠️  No hay datos cargados, usando config por defecto")
            return self.get_default_level()
        
        if 'levels' not in self.levels_data:
            print(f"⚠️  Formato de JSON incorrecto")
            return self.get_default_level()
        
        level = self.levels_data['levels'].get(level_name)
        
        if not level:
            print(f"⚠️  Nivel '{level_name}' no encontrado")
            available = list(self.levels_data['levels'].keys())
            print(f"   Niveles disponibles: {available}")
            return self.get_default_level()
        
        # chintrolas validamos q tenga todos los campos necesarios -bynd
        if self.validate_level(level):
            print(f"✅ Nivel '{level_name}' cargado correctamente")
            return level
        else:
            print(f"⚠️  Nivel '{level_name}' tiene campos faltantes")
            return self.get_default_level()
    
    def validate_level(self, level):
        # q chidoteee validamos que el nivel tenga estructura correcta -bynd
        required_fields = ['type', 'rings_no', 'timer', 'rings', 'ball', 'gravity', 'colors']
        
        for field in required_fields:
            if field not in level:
                print(f"   ❌ Falta campo: {field}")
                return False
        
        # ala validamos sub-campos -bynd
        if 'ring_configs' not in level['rings']:
            print(f"   ❌ Falta rings.ring_configs")
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
    
    def list_available_levels(self):
        # ey lista todos los niveles disponibles -bynd
        if not self.levels_data or 'levels' not in self.levels_data:
            return []
        
        return list(self.levels_data['levels'].keys())
    
    def get_level_info(self, level_name):
        # vavavava info resumida de un nivel -bynd
        level = self.get_level(level_name)
        
        if not level:
            return None
        
        info = {
            'name': level_name,
            'type': level.get('type', 'unknown'),
            'description': level.get('description', 'Sin descripción'),
            'rings_no': level.get('rings_no', 0),
            'timer': level.get('timer', 0)
        }
        
        return info