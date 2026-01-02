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
    def __init__(self):
        # aaa inicialización de pygame -bynd
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Plinko - Escape Mode")
        self.clock = pygame.time.Clock()
        
        # vavavava cargamos el nivel usando LevelConfig -bynd
        self.level_config = LevelConfig()
        self.config = self.level_config.get_level()
        
        # ey creamos el espacio de físicas -bynd
        self.space = pymunk.Space()
        self.space.gravity = tuple(self.config['gravity'])
        
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        
        # q chidoteee variables del juego -bynd
        self.rings = []
        self.game_mode = self.config.get('type', 'escape')
        
        # chintrolas variables según el modo -bynd
        if self.game_mode == 'elimination':
            self.balls = []  # lista de todas las bolas (vivas y muertas)
            self.current_ball = None
            self.ball_timer = None
            self.balls_used = 0
            self.max_balls = self.config.get('max_balls', 10)
            self.ball_lifetime = self.config.get('ball_timer', 3)
        else:
            self.ball = None
            self.start_time = None
        
        self.game_over = False
        self.won = False
        self.running = True
        
        # ala creamos el nivel -bynd
        self.setup_level()
        
        # fokeis mostramos info del nivel -bynd
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
        
        # q chidoteee creamos la primera bola -bynd
        if self.game_mode == 'elimination':
            self.spawn_new_ball()
        else:
            self.create_ball()
            self.start_time = time.time()
    
    def create_ball(self):
        # ala creamos una bola para modo escape -bynd
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
    
    def spawn_new_ball(self):
        # aaa spawneamos nueva bola para modo elimination -bynd
        if self.balls_used >= self.max_balls:
            return False
        
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
        
        # vavavava guardamos la bola con su estado -bynd
        ball_data = {
            'shape': shape,
            'body': body,
            'alive': True,
            'spawn_time': time.time()
        }
        
        self.balls.append(ball_data)
        self.current_ball = ball_data
        self.ball_timer = time.time()
        self.balls_used += 1
        
        print(f"⚪ Nueva bola spawneada ({self.balls_used}/{self.max_balls})")
        return True
    
    def kill_current_ball(self):
        # chintrolas matamos la bola actual -bynd
        if not self.current_ball or not self.current_ball['alive']:
            return
        
        # q chidoteee convertimos a estático -bynd
        ball_data = self.current_ball
        old_body = ball_data['body']
        old_shape = ball_data['shape']
        
        # ala removemos el body dinámico -bynd
        self.space.remove(old_body, old_shape)
        
        # fokeis creamos uno estático en la misma posición -bynd
        static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        static_body.position = old_body.position
        
        ball_config = self.config['ball']
        static_shape = pymunk.Circle(static_body, ball_config['radius'])
        static_shape.elasticity = ball_config['elasticity']
        static_shape.friction = ball_config['friction']
        
        self.space.add(static_body, static_shape)
        
        # aaa actualizamos los datos -bynd
        ball_data['alive'] = False
        ball_data['body'] = static_body
        ball_data['shape'] = static_shape
        
        print(f"💀 Bola eliminada en posición ({old_body.position.x:.0f}, {old_body.position.y:.0f})")
        
        # ey spawneamos nueva bola -bynd
        self.spawn_new_ball()
    
    def check_escapes(self):
        # fokeis checamos si la bola escapó de algún anillo -bynd
        if self.game_over:
            return
        
        if self.game_mode == 'elimination':
            if not self.current_ball or not self.current_ball['alive']:
                return
            ball_pos = self.current_ball['body'].position
        else:
            if not self.ball:
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
        # ey checamos el tiempo según el modo -bynd
        if self.game_over:
            return
        
        if self.game_mode == 'elimination':
            # chintrolas timer por bola -bynd
            if self.current_ball and self.current_ball['alive']:
                elapsed = time.time() - self.ball_timer
                if elapsed >= self.ball_lifetime:
                    self.kill_current_ball()
                    
                    # q chidoteee checamos si perdió -bynd
                    if self.balls_used >= self.max_balls:
                        alive_rings = sum(1 for ring in self.rings if not ring.destroyed)
                        if alive_rings > 0:
                            self.game_over = True
                            self.won = False
                            print("💀 SE ACABARON LAS BOLAS")
                            print("=" * 50)
        else:
            # ala timer global para modo escape -bynd
            if not self.start_time:
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
        if self.game_mode == 'elimination':
            if not self.current_ball or not self.current_ball['alive']:
                return 0
            elapsed = time.time() - self.ball_timer
            return max(0, self.ball_lifetime - elapsed)
        else:
            if not self.start_time:
                return self.config.get('timer', 30)
            elapsed = time.time() - self.start_time
            return max(0, self.config.get('timer', 30) - elapsed)
    
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
        # aaa reiniciamos el nivel -bynd
        print("\n🔄 Reiniciando nivel...")
        self.__init__()
    
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
        
        # chintrolas dibujamos las físicas pero con colores custom -bynd
        if self.game_mode == 'elimination':
            # q chidoteee dibujamos bolas muertas y vivas con colores diferentes -bynd
            for ball_data in self.balls:
                shape = ball_data['shape']
                body = ball_data['body']
                
                if ball_data['alive']:
                    color = tuple(self.config['colors']['ball_alive'])
                else:
                    color = tuple(self.config['colors']['ball_dead'])
                
                pos = body.position
                radius = self.config['ball']['radius']
                pygame.draw.circle(self.screen, color, (int(pos.x), int(pos.y)), int(radius))
            
            # ala dibujamos los anillos manualmente -bynd
            for ring in self.rings:
                if not ring.destroyed:
                    ring_color = tuple(self.config['colors']['rings'])
                    for body, shape in ring.segments:
                        a = shape.a
                        b = shape.b
                        pygame.draw.line(self.screen, ring_color, 
                                       (a.x, a.y), (b.x, b.y), 
                                       int(ring.thickness * 2))
        else:
            # fokeis modo escape normal -bynd
            self.space.debug_draw(self.draw_options)
        
        # aaa dibujamos el UI -bynd
        self.draw_ui()
        
        pygame.display.flip()
    
    def draw_ui(self):
        # ala dibujamos el timer y mensajes -bynd
        font_big = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 36)
        font_tiny = pygame.font.Font(None, 24)
        
        # vavavava color del timer según tiempo restante -bynd
        remaining = self.get_remaining_time()
        if self.game_mode == 'elimination':
            if remaining < 1:
                timer_color = tuple(self.config['colors'].get('timer_warning', [255, 100, 100]))
            else:
                timer_color = tuple(self.config['colors']['timer_text'])
        else:
            timer_color = tuple(self.config['colors']['timer_text'])
        
        time_text = font_big.render(f"{remaining:.2f}", True, timer_color)
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
            
            # chintrolas contador según modo -bynd
            if self.game_mode == 'elimination':
                balls_msg = f"Bolas: {self.balls_used}/{self.max_balls}"
                balls_text = font_tiny.render(balls_msg, True, (200, 200, 200))
                self.screen.blit(balls_text, (20, HEIGHT - 70))
                
                dead_balls = sum(1 for b in self.balls if not b['alive'])
                dead_msg = f"Bolas muertas: {dead_balls}"
                dead_text = font_tiny.render(dead_msg, True, (150, 150, 150))
                self.screen.blit(dead_text, (20, HEIGHT - 40))
            
            # q chidoteee anillos restantes -bynd
            remaining_rings = sum(1 for ring in self.rings if not ring.destroyed)
            rings_msg = f"Anillos: {remaining_rings}/{len(self.rings)}"
            rings_text = font_tiny.render(rings_msg, True, (200, 200, 200))
            
            if self.game_mode == 'elimination':
                self.screen.blit(rings_text, (WIDTH - 200, HEIGHT - 40))
            else:
                self.screen.blit(rings_text, (20, HEIGHT - 40))
    
    def print_level_info(self):
        # aaa mostramos info del nivel en consola -bynd
        print("\n" + "=" * 60)
        print("🎮 PLINKO - ESCAPE MODE")
        print("=" * 60)
        print(f"🎯 Modo: {self.game_mode.upper()}")
        print(f"📝 Descripción: {self.config.get('description', 'N/A')}")
        print(f"⭕ Anillos: {len(self.rings)}")
        
        if self.game_mode == 'elimination':
            print(f"⚪ Bolas máximas: {self.max_balls}")
            print(f"⏱️ Timer por bola: {self.ball_lifetime}s")
        else:
            print(f"⏱️ Timer: {self.config.get('timer', 30)}s")
        
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
    # ey ahora solo carga el nivel del JSON -bynd
    game = PlinkoGame()
    game.run()
