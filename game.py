import pymunk
import pymunk.pygame_util
import pygame
import sys
import time
from levels import LevelConfig
from ring import Ring

# ey constantes de pantalla en 9:16 para móviles -bynd
WIDTH, HEIGHT = 450, 800
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
        if self.game_mode == '8ball':
            self.ball_yes = None
            self.ball_no = None
            self.yes_score = 0
            self.no_score = 0
            self.start_time = None
            self.last_spawn_time = None
            self.spawn_delay = self.config.get('ball_spawn_delay', 2)
            self.winner = None
        elif self.game_mode == 'elimination':
            self.balls = []
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
        center = (WIDTH // 2, HEIGHT // 2)  # chintrolas centro de la pantalla -bynd
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
                friction=rings_config['friction'],
                rotation_speed=ring_data.get('rotation_speed', 0)
            )
            self.rings.append(ring)
        
        # q chidoteee iniciamos según el modo -bynd
        if self.game_mode == '8ball':
            self.spawn_8ball_pair()
            self.start_time = time.time()
            self.last_spawn_time = time.time()
        elif self.game_mode == 'elimination':
            self.spawn_new_ball()
        else:
            self.create_ball()
            self.start_time = time.time()
    
    def spawn_8ball_pair(self):
        # aaa spawneamos el par de bolas yes/no -bynd
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        
        # vavavava bola YES (cyan) -bynd
        if 'ball_yes' in self.config:
            ball_config = self.config['ball_yes']
            offset_x = ball_config.get('offset_x', -20)
            
            mass = ball_config['mass']
            radius = ball_config['radius']
            
            body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, radius))
            body.position = (center_x + offset_x, center_y)
            
            shape = pymunk.Circle(body, radius)
            shape.elasticity = ball_config['elasticity']
            shape.friction = ball_config['friction']
            shape.collision_type = 1  # ey tipo yes -bynd
            
            self.space.add(body, shape)
            self.ball_yes = shape
        
        # chintrolas bola NO (naranja) -bynd
        if 'ball_no' in self.config:
            ball_config = self.config['ball_no']
            offset_x = ball_config.get('offset_x', 20)
            
            mass = ball_config['mass']
            radius = ball_config['radius']
            
            body = pymunk.Body(mass, pymunk.moment_for_circle(mass, 0, radius))
            body.position = (center_x + offset_x, center_y)
            
            shape = pymunk.Circle(body, radius)
            shape.elasticity = ball_config['elasticity']
            shape.friction = ball_config['friction']
            shape.collision_type = 2  # q chidoteee tipo no -bynd
            
            self.space.add(body, shape)
            self.ball_no = shape
        
        print(f"⚪⚪ Par de bolas spawneado (Yes: cyan, No: naranja)")
    
    def remove_ball(self, ball):
        # ala removemos una bola del espacio -bynd
        if ball and ball.body:
            try:
                self.space.remove(ball.body, ball)
            except:
                pass
    
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
        
        if self.game_mode == '8ball':
            # vavavava checamos ambas bolas -bynd
            if self.ball_yes and self.ball_yes.body:
                yes_pos = self.ball_yes.body.position
                for ring in self.rings:
                    if not ring.destroyed and ring.check_ball_escaped((yes_pos.x, yes_pos.y)):
                        self.yes_score += 1
                        self.remove_ball(self.ball_yes)
                        self.ball_yes = None
                        print(f"💙 YES escapa! Puntos: {self.yes_score}")
                        break
            
            if self.ball_no and self.ball_no.body:
                no_pos = self.ball_no.body.position
                for ring in self.rings:
                    if not ring.destroyed and ring.check_ball_escaped((no_pos.x, no_pos.y)):
                        self.no_score += 1
                        self.remove_ball(self.ball_no)
                        self.ball_no = None
                        print(f"🧡 NO escapa! Puntos: {self.no_score}")
                        break
            
        elif self.game_mode == 'elimination':
            if not self.current_ball or not self.current_ball['alive']:
                return
            ball_pos = self.current_ball['body'].position
            
            for ring in self.rings:
                if ring.check_ball_escaped((ball_pos.x, ball_pos.y)):
                    ring.destroy()
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
        
        if self.game_mode == '8ball':
            # q chidoteee timer global para 8ball -bynd
            elapsed = time.time() - self.start_time
            remaining = self.config.get('timer', 60) - elapsed
            
            if remaining <= 0:
                self.game_over = True
                # chintrolas determinamos ganador -bynd
                if self.yes_score > self.no_score:
                    self.winner = "YES"
                elif self.no_score > self.yes_score:
                    self.winner = "NO"
                else:
                    self.winner = "TIE"
                
                print(f"⏰ TIEMPO TERMINADO")
                print(f"🏆 Ganador: {self.winner}")
                print(f"   YES: {self.yes_score} | NO: {self.no_score}")
                print("=" * 50)
            
            # ala respawnear bolas si no están -bynd
            time_since_spawn = time.time() - self.last_spawn_time
            if time_since_spawn >= self.spawn_delay:
                if not self.ball_yes or not self.ball_no:
                    if not self.ball_yes:
                        self.remove_ball(self.ball_yes)
                    if not self.ball_no:
                        self.remove_ball(self.ball_no)
                    self.spawn_8ball_pair()
                    self.last_spawn_time = time.time()
        
        elif self.game_mode == 'elimination':
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
        if self.game_mode == '8ball':
            if not self.start_time:
                return self.config.get('timer', 60)
            elapsed = time.time() - self.start_time
            return max(0, self.config.get('timer', 60) - elapsed)
        elif self.game_mode == 'elimination':
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
        
        # chintrolas dibujamos los anillos de forma limpia -bynd
        ring_color = tuple(self.config['colors']['rings'])
        for ring in self.rings:
            if not ring.destroyed:
                for body, shape in ring.segments:
                    # q chidoteee obtenemos posiciones en espacio mundial -bynd
                    if ring.body:
                        # ala para anillos que rotan -bynd
                        pv1 = body.local_to_world(shape.a)
                        pv2 = body.local_to_world(shape.b)
                    else:
                        # fokeis para anillos estáticos -bynd
                        pv1 = shape.a + body.position
                        pv2 = shape.b + body.position
                    
                    # vavavava dibujamos línea gruesa -bynd
                    pygame.draw.line(self.screen, ring_color,
                                   (int(pv1.x), int(pv1.y)),
                                   (int(pv2.x), int(pv2.y)),
                                   int(ring.thickness * 2))
        
        # aaa dibujamos las bolas según el modo -bynd
        if self.game_mode == 'elimination':
            # q chidoteee dibujamos bolas muertas y vivas -bynd
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
        
        elif self.game_mode == '8ball':
            # ala dibujamos bola YES -bynd
            if self.ball_yes and self.ball_yes.body:
                yes_color = tuple(self.config['colors']['ball_yes'])
                yes_pos = self.ball_yes.body.position
                yes_radius = self.config['ball_yes']['radius']
                pygame.draw.circle(self.screen, yes_color,
                                 (int(yes_pos.x), int(yes_pos.y)), int(yes_radius))
            
            # fokeis dibujamos bola NO -bynd
            if self.ball_no and self.ball_no.body:
                no_color = tuple(self.config['colors']['ball_no'])
                no_pos = self.ball_no.body.position
                no_radius = self.config['ball_no']['radius']
                pygame.draw.circle(self.screen, no_color,
                                 (int(no_pos.x), int(no_pos.y)), int(no_radius))
        else:
            # vavavava modo escape -bynd
            if self.ball and self.ball.body:
                ball_color = tuple(self.config['colors'].get('ball', [255, 255, 255]))
                ball_pos = self.ball.body.position
                ball_radius = self.config['ball']['radius']
                pygame.draw.circle(self.screen, ball_color,
                                 (int(ball_pos.x), int(ball_pos.y)), int(ball_radius))
        
        # chintrolas dibujamos el UI -bynd
        self.draw_ui()
        
        pygame.display.flip()
    
    def draw_ui(self):
        # ala dibujamos el timer y mensajes -bynd
        font_huge = pygame.font.Font(None, 100)  # chintrolas ajustado para 9:16 -bynd
        font_big = pygame.font.Font(None, 64)
        font_medium = pygame.font.Font(None, 42)
        font_small = pygame.font.Font(None, 32)
        font_tiny = pygame.font.Font(None, 20)
        
        if self.game_mode == '8ball':
            # chintrolas dibujamos pregunta arriba -bynd
            question = self.config.get('question', 'Magic 8 Ball')
            question_color = tuple(self.config['colors']['question_text'])
            
            # q chidoteee dividimos pregunta en dos líneas si es muy larga -bynd
            if len(question) > 30:
                words = question.split()
                mid = len(words) // 2
                line1 = ' '.join(words[:mid])
                line2 = ' '.join(words[mid:])
                
                question_text1 = font_tiny.render(line1, True, question_color)
                question_text2 = font_tiny.render(line2, True, question_color)
                
                q1_width = question_text1.get_width()
                q2_width = question_text2.get_width()
                
                self.screen.blit(question_text1, (WIDTH // 2 - q1_width // 2, 20))
                self.screen.blit(question_text2, (WIDTH // 2 - q2_width // 2, 45))
            else:
                question_text = font_tiny.render(question, True, question_color)
                question_width = question_text.get_width()
                self.screen.blit(question_text, (WIDTH // 2 - question_width // 2, 30))
            
            if not self.game_over:
                # q chidoteee contadores YES y NO -bynd
                yes_color = tuple(self.config['colors']['yes_text'])
                no_color = tuple(self.config['colors']['no_text'])
                
                yes_text = font_medium.render(f"Yes: {self.yes_score}", True, yes_color)
                no_text = font_medium.render(f"No: {self.no_score}", True, no_color)
                
                # ala posiciones ajustadas para 9:16 -bynd
                self.screen.blit(yes_text, (30, HEIGHT - 120))
                self.screen.blit(no_text, (WIDTH - 130, HEIGHT - 120))
                
                # ala timer abajo en el centro -bynd
                timer_color = tuple(self.config['colors']['timer_text'])
                time_text = font_big.render(f"{self.get_remaining_time():.2f}", True, timer_color)
                time_width = time_text.get_width()
                self.screen.blit(time_text, (WIDTH // 2 - time_width // 2, HEIGHT - 70))
            else:
                # fokeis pantalla de ganador -bynd
                winner_color = tuple(self.config['colors']['winner_text'])
                
                if self.winner == "YES":
                    winner_text = font_huge.render("YES", True, tuple(self.config['colors']['yes_text']))
                elif self.winner == "NO":
                    winner_text = font_huge.render("NO", True, tuple(self.config['colors']['no_text']))
                else:
                    winner_text = font_huge.render("TIE", True, (200, 200, 200))
                
                winner_width = winner_text.get_width()
                self.screen.blit(winner_text, (WIDTH // 2 - winner_width // 2, HEIGHT // 2 - 60))
                
                # aaa puntaje final -bynd
                score_text = font_small.render(f"{self.yes_score} - {self.no_score}", True, (200, 200, 200))
                score_width = score_text.get_width()
                self.screen.blit(score_text, (WIDTH // 2 - score_width // 2, HEIGHT // 2 + 40))
                
                # vavavava mensaje de reinicio -bynd
                restart_msg = "Presiona R para reiniciar | ESC para salir"
                restart_text = font_tiny.render(restart_msg, True, (200, 200, 200))
                restart_width = restart_text.get_width()
                self.screen.blit(restart_text, (WIDTH // 2 - restart_width // 2, HEIGHT // 2 + 100))
        
        else:
            # q chidoteee UI para otros modos -bynd
            remaining = self.get_remaining_time()
            if self.game_mode == 'elimination':
                if remaining < 1:
                    timer_color = tuple(self.config['colors'].get('timer_warning', [255, 100, 100]))
                else:
                    timer_color = tuple(self.config['colors']['timer_text'])
            else:
                timer_color = tuple(self.config['colors']['timer_text'])
            
            time_text = font_big.render(f"{remaining:.2f}", True, timer_color)
            time_width = time_text.get_width()
            self.screen.blit(time_text, (WIDTH // 2 - time_width // 2, HEIGHT - 70))
            
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
                if self.game_mode != '8ball':
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
        print("🎮 PLINKO")
        print("=" * 60)
        print(f"🎯 Modo: {self.game_mode.upper()}")
        print(f"📝 Descripción: {self.config.get('description', 'N/A')}")
        
        if self.game_mode == '8ball':
            print(f"❓ Pregunta: {self.config.get('question', 'N/A')}")
            print(f"⏱️ Timer total: {self.config.get('timer', 60)}s")
            print(f"🔄 Spawn delay: {self.spawn_delay}s")
        elif self.game_mode == 'elimination':
            print(f"⚪ Bolas máximas: {self.max_balls}")
            print(f"⏱️ Timer por bola: {self.ball_lifetime}s")
        else:
            print(f"⏱️ Timer: {self.config.get('timer', 30)}s")
        
        print(f"⭕ Anillos: {len(self.rings)}")
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
