import pygame
import sys
import random
import math

# Pygame initialisieren
pygame.init()

# Fenstergröße und andere Konstanten
WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.25
JUMP_STRENGTH = -5
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # Millisekunden zwischen neuen Röhren

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
SKY_BLUE = (135, 206, 235)

# Fenster erstellen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Deluxe")
clock = pygame.time.Clock()

# Schrift für Score und Game Over
font = pygame.font.SysFont("Arial", 30)
large_font = pygame.font.SysFont("Arial", 50)

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.life = 1.0  # Lebensdauer zwischen 0 und 1
        self.decay = random.uniform(0.02, 0.05)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # Schwerkraft für Partikel
        self.life -= self.decay
        return self.life > 0
    
    def draw(self, surface):
        alpha = int(self.life * 255)
        size = int(self.life * 5)
        if alpha > 0 and size > 0:
            particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (*self.color, alpha), (size, size), size)
            surface.blit(particle_surface, (self.x - size, self.y - size))

class PowerUp:
    def __init__(self, x, y, power_type):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.type = power_type  # "shield", "slow", "points"
        self.colors = {
            "shield": BLUE,
            "slow": YELLOW,
            "points": PURPLE
        }
        self.animation_time = 0
    
    def update(self):
        self.x -= PIPE_SPEED
        self.animation_time += 0.1
        return self.x < -self.width
    
    def draw(self):
        # Pulsierende Animation
        size_mod = math.sin(self.animation_time) * 2
        pygame.draw.rect(screen, self.colors[self.type], 
                        (self.x - size_mod, self.y - size_mod, 
                         self.width + size_mod * 2, self.height + size_mod * 2))
        
        # Symbol je nach Typ
        if self.type == "shield":
            pygame.draw.circle(screen, WHITE, (self.x + self.width // 2, self.y + self.height // 2), 6, 2)
        elif self.type == "slow":
            pygame.draw.rect(screen, WHITE, (self.x + 5, self.y + 5, 10, 10), 2)
        elif self.type == "points":
            pygame.draw.polygon(screen, WHITE, [
                (self.x + self.width // 2, self.y + 3),
                (self.x + self.width - 3, self.y + self.height // 2),
                (self.x + self.width // 2, self.y + self.height - 3),
                (self.x + 3, self.y + self.height // 2)
            ])
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Bird:
    def __init__(self):
        self.x = WIDTH // 3
        self.y = HEIGHT // 2
        self.velocity = 0
        self.width = 30
        self.height = 30
        self.angle = 0
        self.shield = False
        self.shield_time = 0
        self.particles = []
        self.flap_animation = 0
    
    def jump(self):
        self.velocity = JUMP_STRENGTH
        # Partikel-Effekt beim Springen
        for _ in range(5):
            self.particles.append(Particle(self.x + self.width, self.y + self.height // 2, YELLOW))
    
    def update(self):
        # Schwerkraft anwenden
        self.velocity += GRAVITY
        self.y += self.velocity
        
        # Vogel-Rotation basierend auf Geschwindigkeit
        self.angle = max(-30, min(30, self.velocity * 3))
        
        # Flügel-Animation
        self.flap_animation += 0.3
        
        # Schild-Timer aktualisieren
        if self.shield:
            self.shield_time -= 1
            if self.shield_time <= 0:
                self.shield = False
        
        # Partikel aktualisieren
        self.particles = [p for p in self.particles if p.update()]
        
        # Flug-Partikel erzeugen
        if random.random() < 0.3:
            self.particles.append(Particle(self.x, self.y + self.height // 2, SKY_BLUE))
        
        # Bodenkollision verhindern
        if self.y >= HEIGHT - self.height:
            self.y = HEIGHT - self.height
            return True  # Game Over
        return False
    
    def draw(self):
        # Partikel zeichnen
        for particle in self.particles:
            particle.draw(screen)
        
        # Schild-Effekt
        if self.shield:
            shield_alpha = 100 + int(math.sin(pygame.time.get_ticks() * 0.01) * 50)
            shield_surface = pygame.Surface((self.width + 10, self.height + 10), pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, (0, 100, 255, shield_alpha), 
                             (self.width // 2 + 5, self.height // 2 + 5), self.width // 2 + 5)
            screen.blit(shield_surface, (self.x - 5, self.y - 5))
        
        # Vogel mit Rotation und Animation
        bird_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Körper
        pygame.draw.ellipse(bird_surface, BLUE, (0, 0, self.width, self.height))
        
        # Flügel (animiert)
        wing_offset = math.sin(self.flap_animation) * 3
        pygame.draw.ellipse(bird_surface, (0, 0, 200), 
                          (5, 5 + wing_offset, self.width - 10, self.height - 15))
        
        # Auge
        pygame.draw.circle(bird_surface, WHITE, (self.width - 8, 10), 5)
        pygame.draw.circle(bird_surface, BLACK, (self.width - 8, 10), 2)
        
        # Schnabel
        pygame.draw.polygon(bird_surface, ORANGE, [
            (self.width - 2, self.height // 2),
            (self.width + 8, self.height // 2 - 3),
            (self.width + 8, self.height // 2 + 3)
        ])
        
        # Rotierte Vogel-Surface
        rotated_bird = pygame.transform.rotate(bird_surface, -self.angle)
        screen.blit(rotated_bird, (self.x, self.y))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def activate_shield(self, duration=300):  # 5 Sekunden bei 60 FPS
        self.shield = True
        self.shield_time = duration

class Pipe:
    def __init__(self, difficulty):
        self.x = WIDTH
        self.width = 50
        self.pipe_gap = PIPE_GAP - difficulty * 5  # Schwierigkeit erhöht sich
        self.top_height = random.randint(50, HEIGHT - self.pipe_gap - 50)
        self.bottom_height = HEIGHT - self.top_height - self.pipe_gap
        self.passed = False
        self.color = (random.randint(0, 100), random.randint(128, 255), random.randint(0, 100))
    
    def update(self):
        self.x -= PIPE_SPEED
        return self.x < -self.width
    
    def draw(self):
        # Obere Röhre mit Verzierung
        pygame.draw.rect(screen, self.color, (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(screen, (0, 100, 0), (self.x - 3, self.top_height - 20, self.width + 6, 20))
        
        # Untere Röhre mit Verzierung
        pygame.draw.rect(screen, self.color, (self.x, HEIGHT - self.bottom_height, self.width, self.bottom_height))
        pygame.draw.rect(screen, (0, 100, 0), (self.x - 3, HEIGHT - self.bottom_height, self.width + 6, 20))
    
    def get_rects(self):
        top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        bottom_rect = pygame.Rect(self.x, HEIGHT - self.bottom_height, self.width, self.bottom_height)
        return top_rect, bottom_rect

class Background:
    def __init__(self):
        self.clouds = []
        self.stars = []
        self.time_of_day = 0  # 0 = Tag, 1 = Nacht
        self.time_speed = 0.0005
        
        # Wolken initialisieren
        for _ in range(5):
            self.add_cloud()
        
        # Sterne initialisieren
        for _ in range(20):
            self.stars.append([random.randint(0, WIDTH), random.randint(0, HEIGHT // 2), 
                             random.uniform(0.5, 1.5)])
    
    def add_cloud(self):
        self.clouds.append([random.randint(0, WIDTH), random.randint(20, HEIGHT // 3), 
                          random.uniform(0.5, 1.0)])
    
    def update(self):
        # Tageszeit ändern
        self.time_of_day = (self.time_of_day + self.time_speed) % 2
        
        # Wolken bewegen
        for cloud in self.clouds:
            cloud[0] -= cloud[2]
            if cloud[0] < -100:
                cloud[0] = WIDTH + 50
                cloud[1] = random.randint(20, HEIGHT // 3)
    
    def draw(self):
        # Himmelsfarbe basierend auf Tageszeit
        if self.time_of_day < 1:  # Tag zu Nacht
            sky_color = (
                int(135 * (1 - self.time_of_day) + 0 * self.time_of_day),
                int(206 * (1 - self.time_of_day) + 0 * self.time_of_day),
                int(235 * (1 - self.time_of_day) + 25 * self.time_of_day)
            )
        else:  # Nacht zu Tag
            t = self.time_of_day - 1
            sky_color = (
                int(0 * (1 - t) + 135 * t),
                int(0 * (1 - t) + 206 * t),
                int(25 * (1 - t) + 235 * t)
            )
        
        screen.fill(sky_color)
        
        # Sterne (nur bei Nacht sichtbar)
        if self.time_of_day > 0.5 and self.time_of_day < 1.5:
            star_alpha = min(1.0, abs(1.0 - self.time_of_day)) * 255
            for x, y, brightness in self.stars:
                twinkle = math.sin(pygame.time.get_ticks() * 0.001 + x) * 0.5 + 0.5
                alpha = int(star_alpha * brightness * twinkle)
                if alpha > 0:
                    star_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
                    pygame.draw.circle(star_surface, (255, 255, 255, alpha), (2, 2), 2)
                    screen.blit(star_surface, (x, y))
        
        # Wolken zeichnen
        for x, y, size in self.clouds:
            cloud_alpha = 200
            cloud_size = int(30 * size)
            for i in range(3):
                offset_x = i * cloud_size // 2
                pygame.draw.circle(screen, (255, 255, 255, cloud_alpha), 
                                 (int(x) + offset_x, int(y)), cloud_size)
                pygame.draw.circle(screen, (255, 255, 255, cloud_alpha), 
                                 (int(x) + offset_x - cloud_size//3, int(y) + cloud_size//3), cloud_size)
        
        # Boden
        pygame.draw.rect(screen, (100, 70, 0), (0, HEIGHT - 20, WIDTH, 20))
        pygame.draw.rect(screen, (120, 90, 0), (0, HEIGHT - 20, WIDTH, 5))

def check_collision(bird, pipes):
    if bird.shield:
        return False
    
    bird_rect = bird.get_rect()
    
    for pipe in pipes:
        top_rect, bottom_rect = pipe.get_rects()
        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            # Explosions-Partikel
            for _ in range(15):
                bird.particles.append(Particle(bird.x + bird.width // 2, bird.y + bird.height // 2, RED))
            return True
    
    return False

def draw_score(score, high_score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"High: {high_score}", True, YELLOW)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 10))

def draw_game_over(score, high_score):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))
    
    game_over_text = large_font.render("Game Over", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, YELLOW)
    restart_text = font.render("Press R to restart", True, WHITE)
    
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 40))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 80))

def draw_power_up_indicator(bird):
    if bird.shield:
        time_left = bird.shield_time / 60  # In Sekunden
        shield_text = font.render(f"Shield: {time_left:.1f}s", True, BLUE)
        screen.blit(shield_text, (WIDTH // 2 - shield_text.get_width() // 2, 50))

def main():
    bird = Bird()
    pipes = []
    power_ups = []
    background = Background()
    score = 0
    high_score = 0
    game_over = False
    difficulty = 0
    
    last_pipe = pygame.time.get_ticks()
    power_up_timer = 0
    
    # Hauptspiel-Schleife
    running = True
    while running:
        # FPS begrenzen
        clock.tick(FPS)
        
        # Events verarbeiten
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.jump()
                if event.key == pygame.K_r and game_over:
                    # Spiel neustarten
                    return main()
        
        if not game_over:
            # Hintergrund aktualisieren
            background.update()
            
            # Vogel aktualisieren
            game_over = bird.update()
            
            # Schwierigkeit basierend auf Score erhöhen
            difficulty = min(10, score // 5)
            
            # Neue Röhren erstellen
            current_time = pygame.time.get_ticks()
            if current_time - last_pipe > PIPE_FREQUENCY - difficulty * 50:
                pipes.append(Pipe(difficulty))
                last_pipe = current_time
            
            # Power-Ups spawnen
            power_up_timer += 1
            if power_up_timer > 300 and random.random() < 0.01:  # Alle ~5 Sekunden Chance
                power_type = random.choice(["shield", "slow", "points"])
                power_ups.append(PowerUp(WIDTH, random.randint(100, HEIGHT - 100), power_type))
                power_up_timer = 0
            
            # Röhren aktualisieren
            for pipe in pipes[:]:
                if pipe.update():
                    pipes.remove(pipe)
                
                # Prüfen, ob Vogel Röhre passiert hat
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    score += 1
                    high_score = max(high_score, score)
            
            # Power-Ups aktualisieren und Kollision prüfen
            for power_up in power_ups[:]:
                if power_up.update():
                    power_ups.remove(power_up)
                elif bird.get_rect().colliderect(power_up.get_rect()):
                    if power_up.type == "shield":
                        bird.activate_shield()
                    elif power_up.type == "points":
                        score += 5
                    # "slow" würde hier die Geschwindigkeit reduzieren
                    power_ups.remove(power_up)
            
            # Kollision prüfen
            if check_collision(bird, pipes):
                game_over = True
        
        # Alles zeichnen
        background.draw()
        
        for pipe in pipes:
            pipe.draw()
        
        for power_up in power_ups:
            power_up.draw()
        
        bird.draw()
        draw_score(score, high_score)
        draw_power_up_indicator(bird)
        
        if game_over:
            draw_game_over(score, high_score)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()