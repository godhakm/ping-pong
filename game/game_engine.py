import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        self.winning_score = 5
        self.game_over = False
        self.winner_text = ""
        self.winner_font = pygame.font.SysFont("Arial", 50)
        self.instruction_font = pygame.font.SysFont("Arial", 20)

        # NEW: Load sound effects
        self.paddle_hit_sound = pygame.mixer.Sound("assets/paddle_hit.wav")
        self.wall_bounce_sound = pygame.mixer.Sound("assets/wall_bounce.wav")
        self.score_sound = pygame.mixer.Sound("assets/score.wav")

    def reset_game(self):
        # ... (this method is unchanged)
        self.player_score = 0
        self.ai_score = 0
        self.game_over = False
        self.winner_text = ""
        self.ball.reset()

    def handle_input(self):
        # ... (this method is unchanged)
        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                self.player.move(10, self.height)

    def update(self):
        if not self.game_over:
            self.ball.x += self.ball.velocity_x

            if self.ball.rect().colliderect(self.player.rect()):
                if self.ball.velocity_x < 0:
                    self.ball.velocity_x *= -1
                    self.ball.x = self.player.x + self.player.width
                    self.paddle_hit_sound.play() # NEW: Play paddle hit sound

            if self.ball.rect().colliderect(self.ai.rect()):
                if self.ball.velocity_x > 0:
                    self.ball.velocity_x *= -1
                    self.ball.x = self.ai.x - self.ball.width
                    self.paddle_hit_sound.play() # NEW: Play paddle hit sound
            
            self.ball.move() # This now only moves the ball on the Y-axis

            # NEW: Wall bounce logic moved from ball.py
            if self.ball.y <= 0 or self.ball.y + self.ball.height >= self.height:
                self.ball.velocity_y *= -1
                self.wall_bounce_sound.play() # NEW: Play wall bounce sound
            
            if self.ball.x <= 0:
                self.ai_score += 1
                self.ball.reset()
                self.score_sound.play() # NEW: Play score sound
                if self.ai_score >= self.winning_score:
                    self.winner_text = "AI Wins!"
                    self.game_over = True

            elif self.ball.x >= self.width:
                self.player_score += 1
                self.ball.reset()
                self.score_sound.play() # NEW: Play score sound
                if self.player_score >= self.winning_score:
                    self.winner_text = "Player Wins!"
                    self.game_over = True
            
            self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # ... (this method is unchanged)
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        if self.game_over:
            text_surface = self.winner_font.render(self.winner_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width/2, self.height/2 - 30))
            screen.blit(text_surface, text_rect)
            
            instruction_text = "Press SPACE to Play Again or ESC to Exit"
            inst_surface = self.instruction_font.render(instruction_text, True, WHITE)
            inst_rect = inst_surface.get_rect(center=(self.width/2, self.height/2 + 30))
            screen.blit(inst_surface, inst_rect)
        else:
            pygame.draw.rect(screen, WHITE, self.player.rect())
            pygame.draw.rect(screen, WHITE, self.ai.rect())
            pygame.draw.ellipse(screen, WHITE, self.ball.rect())
            
            player_text = self.font.render(str(self.player_score), True, WHITE)
            ai_text = self.font.render(str(self.ai_score), True, WHITE)
            screen.blit(player_text, (self.width//4 - player_text.get_width()//2, 20))
            screen.blit(ai_text, (self.width * 3//4 - ai_text.get_width()//2, 20))