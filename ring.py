import pymunk
import math

class Ring:
    def __init__(self, space, center, radius, gap_angle, gap_size, thickness, elasticity, friction):
        # aaa inicializamos el anillo con todos sus parámetros -bynd
        self.space = space
        self.center = center
        self.radius = radius
        self.gap_angle = gap_angle
        self.gap_size = gap_size
        self.thickness = thickness
        self.elasticity = elasticity
        self.friction = friction
        
        self.destroyed = False
        self.segments = []
        
        # vavavava creamos los segmentos del anillo -bynd
        self.create_ring_segments()
    
    def create_ring_segments(self):
        # ey dividimos el anillo en segmentos evitando el gap -bynd
        num_segments = 36
        angle_per_segment = 360 / num_segments
        
        gap_start = self.gap_angle - self.gap_size / 2
        gap_end = self.gap_angle + self.gap_size / 2
        
        for i in range(num_segments):
            angle = i * angle_per_segment
            next_angle = (i + 1) * angle_per_segment
            
            # chintrolas checamos si este segmento está en el gap -bynd
            if self.is_in_gap(angle, gap_start, gap_end) and self.is_in_gap(next_angle, gap_start, gap_end):
                continue
            
            # q chidoteee calculamos los puntos del segmento -bynd
            rad1 = math.radians(angle)
            rad2 = math.radians(next_angle)
            
            x1 = self.center[0] + self.radius * math.cos(rad1)
            y1 = self.center[1] + self.radius * math.sin(rad1)
            x2 = self.center[0] + self.radius * math.cos(rad2)
            y2 = self.center[1] + self.radius * math.sin(rad2)
            
            # ala creamos el segmento estático -bynd
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            shape = pymunk.Segment(body, (x1, y1), (x2, y2), self.thickness)
            shape.elasticity = self.elasticity
            shape.friction = self.friction
            
            self.space.add(body, shape)
            self.segments.append((body, shape))
    
    def is_in_gap(self, angle, gap_start, gap_end):
        # vavavava checamos si un ángulo está dentro del gap -bynd
        angle = angle % 360
        gap_start = gap_start % 360
        gap_end = gap_end % 360
        
        if gap_start < gap_end:
            return gap_start <= angle <= gap_end
        else:
            return angle >= gap_start or angle <= gap_end
    
    def check_ball_escaped(self, ball_pos):
        # ey checamos si la bola escapó de este anillo -bynd
        if self.destroyed:
            return False
        
        # chintrolas calculamos distancia del centro -bynd
        dx = ball_pos[0] - self.center[0]
        dy = ball_pos[1] - self.center[1]
        distance = math.sqrt(dx*dx + dy*dy)
        
        # q chidoteee si la bola está fuera del radio del anillo -bynd
        if distance > self.radius + 20:
            # ala calculamos el ángulo donde está la bola -bynd
            angle = math.degrees(math.atan2(dy, dx)) % 360
            
            gap_start = (self.gap_angle - self.gap_size / 2) % 360
            gap_end = (self.gap_angle + self.gap_size / 2) % 360
            
            # fokeis si escapó por el gap -bynd
            if self.is_in_gap(angle, gap_start, gap_end):
                return True
        
        return False
    
    def destroy(self):
        # aaa destruimos el anillo removiendo todos sus segmentos -bynd
        if not self.destroyed:
            for body, shape in self.segments:
                self.space.remove(body, shape)
            self.destroyed = True
            print(f"💥 Anillo destruido! (Radio: {self.radius:.0f}, Gap: {self.gap_angle:.0f}°)")
    
    def get_info(self):
        # ey retornamos info del anillo -bynd
        return {
            'radius': self.radius,
            'gap_angle': self.gap_angle,
            'gap_size': self.gap_size,
            'destroyed': self.destroyed
        }