from game import PlinkoGame

def main():
    # aaa mostramos el banner y arrancamos -bynd
    print("🎮 PLINKO - ESCAPE MODE")
    print("=" * 50)
    print("Cargando nivel desde level_config.json...")
    print()
    
    # vavavava creamos y corremos el juego -bynd
    game = PlinkoGame()
    game.run()

if __name__ == "__main__":
    main()
