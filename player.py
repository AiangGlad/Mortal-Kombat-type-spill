import pygame

class Player():
    def __init__(self, x, y, frames, controls, surface):
        self.surface = surface
        self.rect = pygame.Rect((x, y, 80, 288))
        self.controls = controls
        self.vel_y = 0
        self.vel_y_thowable = 0
        self.throw_cooldown = 0
        self.jump = False
        self.punch = False
        self.punch_cooldown = 0
        self.defense = False
        self.defense_cooldown = 0
        self.defense_time = 0
        self.throw = False
        self.direction = 80
        self.frames = frames
        self.frame_nr = 0
        self.active_frames = 0
        self.motion = "idle"
        self.health = 100

    def actions(self, WIDTH, HEIGHT, enemy):
        SPEED = 14
        GRAVITY = 4
        dx = 0 
        dy = 0
        dy_T = 0

        self.punch_cooldown -= 1
        self.defense_cooldown -= 1
        self.throw_cooldown -= 1

        key = pygame.key.get_pressed()
        if self.punch == False and self.health > 0:
            if self.controls == "WASD":
                if key[pygame.K_a] and self.throw == False and self.punch_cooldown <= 10:
                    dx = -SPEED
                    self.direction = -80
                    self.motion = "walk"
                if key[pygame.K_d] and self.throw == False and self.punch_cooldown <= 10:
                    dx = SPEED
                    self.direction = 80
                    self.motion = "walk"
                if key[pygame.K_w]  and self.jump == False:
                    self.vel_y = -40
                    self.jump = True
                if key[pygame.K_r]  and self.jump == False:
                    self.melee(enemy)
                if key[pygame.K_1] and self.throw_cooldown <= 0:
                    self.range()
                if key[pygame.K_q]:
                    self.block()

            if self.controls == "Arrows":
                if key[pygame.K_LEFT] and self.throw == False and self.punch_cooldown <= 10:
                    dx = -SPEED
                    self.direction = -80
                    self.motion = "walk"
                if key[pygame.K_RIGHT] and self.throw == False and self.punch_cooldown <= 10:
                    dx = SPEED
                    self.direction = 80
                    self.motion = "walk"
                if key[pygame.K_DOWN]  and self.jump == False:
                    self.vel_y = -40
                    self.jump = True
                if key[pygame.K_PAGEUP]  and self.jump == False:
                    self.melee(enemy)
                if key[pygame.K_KP0] and  self.throw_cooldown <= 0:
                    self.range()
                if key[pygame.K_PAGEDOWN]:
                    self.block()

        self.vel_y += GRAVITY
        dy += self.vel_y

        if self.rect.bottom + dy >= HEIGHT-100:
            self.vel_y = 0
            dy = 0
            self.jump = False
        if self.rect.left + dx < 0 or self.rect.right + dx > WIDTH:
            dx = 0
        if self.rect.bottom <= 500:
            self.motion = "jump"

        if self.punch_cooldown >= 10:
            self.motion = "punch"
            
        if self.punch_cooldown <= 0:
            self.rect.x += dx
            self.rect.y += dy 
        
        if self.defense_cooldown <= 500:
           self.defense = False

        if self.throw == True:
            self.vel_y_thowable += GRAVITY 
            dy_T += self.vel_y_thowable - 10
            self.throwable.y += dy_T

            if self.direction == -80:
                self.throwable.x -= 30
            else:
                self.throwable.x += 30

            throwable_pic = pygame.transform.scale(pygame.image.load(self.frames[7]), (250, 250))
            self.surface.blit(throwable_pic, (self.throwable.x - 100, self.throwable.y - 100))

            if self.throwable.y >= 700:
                self.throw = False
                self.vel_y_thowable = 0
            if self.throwable.colliderect(enemy.rect):
                enemy.health -= 9
                self.throw = False
                self.vel_y_thowable = 0

            self.throw_cooldown = 120

    def draw(self):
        self.frame_nr += 1

        if self.motion == "idle":
            if self.frame_nr < 30:
                self.active_frames = 0
            if self.frame_nr > 30:
                self.active_frames = 1
        if self.motion == "walk":
            if self.frame_nr < 30:
                self.active_frames = 2
            if self.frame_nr > 30:
                self.active_frames = 3
        if self.motion == "jump":
            self.active_frames = 4
        if self.motion == "punch":
            self.active_frames = 5
        if self.frame_nr >= 60:
            self.frame_nr = 0
        self.motion = "idle"
        
        if self.health <= 0:
            self.active_frames = 9

        #pygame.draw.rect(surface, (255, 0, 0), self.rect)
        player = pygame.transform.scale(pygame.image.load(self.frames[self.active_frames]), (300, 300))
        playerFlip = pygame.transform.flip(player, True, False)
        if self.direction == -80:
            self.surface.blit(playerFlip, (self.rect.x-120, self.rect.y-17))
        else:
            self.surface.blit(player, (self.rect.x-100, self.rect.y-17))

    def healthbar(self, x, y, B_pic, bonus_pixels_p, bonus_pixels_b, bonus_pixels_t):
        self.health_rect = pygame.Rect((x, y, self.health * 4, 30))
        self.red_health = pygame.Rect((x, y, 400, 30))
        self.defense_bar = pygame.Rect((x, y, self.defense_time, 30))

        player_pic = pygame.transform.scale(pygame.image.load(self.frames[6]), (150, 150))
        self.surface.blit(player_pic, (5 + bonus_pixels_p, 42))
        pygame.draw.rect(self.surface, (255, 0, 0), self.red_health)
        pygame.draw.rect(self.surface, (0,255,0), self.health_rect)

        block_pic = pygame.transform.scale(pygame.image.load(B_pic), (150, 150))
        if self.defense == True:
            self.defense_time -= 4
            pygame.draw.rect(self.surface, (0,0,255), self.defense_bar)
        if self.defense_cooldown <= 0:
            self.surface.blit(block_pic, (5 + bonus_pixels_b, 42))

        throwable_pic = pygame.transform.scale(pygame.image.load(self.frames[8]), (150, 150))
        if self.throw_cooldown <= 0:
            self.surface.blit(throwable_pic, (5 + bonus_pixels_t, 42))
            
    def melee(self, enemy):
        if self.punch_cooldown <= 0:
            self.punch = True
            hitbox = pygame.Rect(self.rect.x + self.direction, self.rect.y+120,100,180)
            if hitbox.colliderect(enemy.rect) and enemy.defense == False:
                enemy.health -= 7
                self.knockback(enemy)
            self.punch_cooldown = 23
            self.punch = False
    
    def range(self):
        self.throw = True
        self.throwable = pygame.Rect((self.rect.x, self.rect.y, 40, 40))

    def block(self):
        if self.defense_cooldown <= 0:
            self.defense = True
            self.defense_cooldown = 600
            self.defense_time = 400

    def knockback(self, enemy):
            if self.direction == 80 and self.rect.x + 70 < 1000:
                enemy.rect.x += 70
            if self.direction == -80 and self.rect.x - 70 > 100:
                enemy.rect.x -= 70