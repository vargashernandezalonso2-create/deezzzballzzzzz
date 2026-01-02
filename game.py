import pymunk
import pymunk.pygame_util
import pygame
import sys
import time
from levels import LevelConfig
from ring import Ring

# ey constantes de pantalla -bynd
WIDTH, HEIGHT = 800, 600
FPS = 60

class PlinkoGame:
    def __init__(self, level_name="escape1"):
        # aaa inicialización de pygame -bynd
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Plinko - Escape Mode")
        self.clock = pygame.time.Clock()
        
        # vavavava cargamos el nivel usando LevelConfig -bynd
        self.level_config = LevelConfig()
        self.config = self.level_config.get_level(level_name)
        self.current_level_name = level_name
        
        # ey creamos el espacio de físicas -bynd
        self.space = pymunk.Space()
        self.space.gravity = tuple(self.config['gravity'])
        
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        
        # q chidoteee variables del juego -bynd
        self.rings = []
        self.ball = None
        self.start_time = None
        self.game_over = False
        self.won = False
        
        self.running = True
        
        # chintrolas creamos el nivel -bynd
        self.setup_level()
        
        # ala mostramos info del nivel -bynd
        self.print_level_info()
    
    def setup_level(self):
        # vavavava configuramos todos los elementos del nivel -bynd
        center = (WIDTH // 2, HEIGHT // 2)
        rings_config = self.config['rings']
        
        # ey iteramos sobre cada config de anillo -bynd
        for ring_data in rings_config['ring_configs']:
            ring = Ring(
                space=self.space,
                center=center,
                radius=ring_data['radius'],
                gap_angle=ring_data['gap_angle'],
                gap_size=ring_data['gap_size'],
                thickness=rings_config['thickness'],
                elasticity=rings_config['elasticity'],
                friction=rings_config['friction']
            )
            self.rings.append(ring)
        
        # q chidoteee creamos la bola -bynd
        self.create_ball()
        
        # chintrolas iniciamos el timer -bynd
        self.start_time = time.time()
    
    def create_ball(self):
        # ala creamos la bola según la config -bynd
        ball_config = self.config['ball']
        center = (WIDTH // 2, HEIGHT // 2)
        
        mass = ball_config['mass']
        radius = ball_config['radius']
        
        body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, radius))
        body.position = center
        
        shape = pymunk.Circle(body, radius)
        shape.elasticity = ball_config['elasticity']
        shape.friction = ball_config['friction']
        
        self.space.add(body, shape)
        self.ball = shape
    
    def check_escapes(self):
        # fokeis checamos si la bola escapó de algún anillo -bynd
        if not self.ball or self.game_over:
            return
        
        ball_pos = self.ball.body.position
        
        for ring in self.rings:
            if ring.check_ball_escaped((ball_pos.x, ball_pos.y)):
                ring.destroy()
        
        # vavavava checamos si ganó -bynd
        all_destroyed = all(ring.destroyed for ring in self.rings)
        if all_destroyed and not self.game_over:
            self.won = True
            self.game_over = True
            print("🎉 ¡GANASTE! Escapaste de todos los anillos")
            print("=" * 50)
    
    def check_timer(self):
        # ey checamos el tiempo restante -bynd
        if self.game_over or not self.start_time:
            return
        
        elapsed = time.time() - self.start_time
        remaining = self.config['timer'] - elapsed
        
        if remaining <= 0:
            self.game_over = True
            self.won = False
            print("⏰ SE ACABÓ EL TIEMPO")
            print("=" * 50)
    
    def get_remaining_time(self):
        # chintrolas calculamos tiempo restante -bynd
        if not self.start_time:
            return self.config['timer']
        
        elapsed = time.time() - self.start_time
        remaining = max(0, self.config['timer'] - elapsed)
        return remaining
    
    def handle_events(self):
        # q chidoteee manejo de eventos -bynd
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # ala reiniciar nivel -bynd
                    self.restart_level()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def restart_level(self):
        # aaa reiniciamos el nivel actual -bynd
        print("\n🔄 Reiniciando nivel...")
        self.__init__(self.current_level_name)
    
    def update(self):
        # vavavava actualizamos el juego -bynd
        if not self.game_over:
            dt = 1.0 / FPS
            self.space.step(dt)
            self.check_escapes()
            self.check_timer()
    
    def draw(self):
        # ey dibujamos todo en pantalla -bynd
        bg_color = tuple(self.config['colors']['background'])
        self.screen.fill(bg_color)
        
        # chintrolas dibujamos las físicas -bynd
        self.space.debug_draw(self.draw_options)
        
        # q chidoteee dibujamos el UI -bynd
        self.draw_ui()
        
        pygame.display.flip()
    
    def draw_ui(self):
        # ala dibujamos el timer y mensajes -bynd
        font_big = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 36)
        font_tiny = pygame.font.Font(None, 24)
        
        timer_color = tuple(self.config['colors']['timer_text'])
        time_text = font_big.render(f"{self.get_remaining_time():.2f}", True, timer_color)
        self.screen.blit(time_text, (WIDTH // 2 - 80, HEIGHT - 100))
        
        # fokeis mensajes de estado -bynd
        if self.game_over:
            if self.won:
                msg = "¡GANASTE!"
                color = (100, 255, 100)
            else:
                msg = "GAME OVER"
                color = (255, 100, 100)
            
            text = font_small.render(msg, True, color)
            self.screen.blit(text, (WIDTH // 2 - 100, 50))
            
            restart_msg = "Presiona R para reiniciar | ESC para salir"
            restart_text = font_tiny.render(restart_msg, True, (200, 200, 200))
            self.screen.blit(restart_text, (WIDTH // 2 - 180, 90))
        else:
            msg = self.config.get('description', 'Escapa de todos los anillos!')
            text = font_tiny.render(msg, True, (255, 255, 255))
            text_width = text.get_width()
            self.screen.blit(text, (WIDTH // 2 - text_width // 2, 20))
            
            # vavavava contador de anillos restantes -bynd
            remaining_rings = sum(1 for ring in self.rings if not ring.destroyed)
            rings_msg = f"Anillos restantes: {remaining_rings}/{len(self.rings)}"
            rings_text = font_tiny.render(rings_msg, True, (200, 200, 200))
            self.screen.blit(rings_text, (20, HEIGHT - 40))
    
    def print_level_info(self):
        # aaa mostramos info del nivel en consola -bynd
        print("\n" + "=" * 60)
        print("🎮 PLINKO - ESCAPE MODE")
        print("=" * 60)
        print(f"📋 Nivel: {self.current_level_name}")
        print(f"📝 Descripción: {self.config.get('description', 'N/A')}")
        print(f"⭕ Anillos: {len(self.rings)}")
        print(f"⏱️  Timer: {self.config['timer']}s")
        print(f"🎱 Bola: Radio {self.config['ball']['radius']}, Masa {self.config['ball']['mass']}")
        print(f"🌍 Gravedad: {self.config['gravity']}")
        print("-" * 60)
        print("💡 Controles:")
        print("   R - Reiniciar nivel")
        print("   ESC - Salir")
        print("=" * 60 + "\n")
    
    def run(self):
        # q chidoteee el loop principal -bynd
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

# chintrolas punto de entrada del programa -bynd
if __name__ == "__main__":
    # ey puedes cambiar el nivel aquí -bynd
    game = PlinkoGame("escape1")  # o "escape2", "test_simple"
    game.run()