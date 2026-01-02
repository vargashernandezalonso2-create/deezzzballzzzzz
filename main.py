from game import PlinkoGame
from levels import LevelConfig

def main():
    # aaa mostramos los niveles disponibles -bynd
    level_config = LevelConfig()
    available_levels = level_config.list_available_levels()
    
    print("🎮 PLINKO - ESCAPE MODE")
    print("=" * 50)
    print(f"📋 Niveles disponibles: {', '.join(available_levels)}")
    print()
    
    # ey mostramos info de cada nivel -bynd
    for level_name in available_levels:
        info = level_config.get_level_info(level_name)
        if info:
            print(f"  • {info['name']}")
            print(f"    {info['description']}")
            print(f"    Anillos: {info['rings_no']} | Timer: {info['timer']}s")
            print()
    
    print("=" * 50)
    print()
    
    # vavavava iniciamos con el primer nivel -bynd
    level_to_play = available_levels[0] if available_levels else "escape1"
    
    print(f"🚀 Iniciando nivel: {level_to_play}")
    print()
    
    # q chidoteee creamos y corremos el juego -bynd
    game = PlinkoGame(level_to_play)
    game.run()

if __name__ == "__main__":
    main()