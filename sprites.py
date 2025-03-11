from settings import *
from random import choice, uniform

class Paddle(pygame.sprite.Sprite):

    def __init__(self, groups):
        super().__init__(groups)
        
        # image and rect
        self.image = pygame.Surface(SIZE['paddle'], pygame.SRCALPHA)
        pygame.draw.rect(self.image, COLORS['paddle'], pygame.FRect((0, 0), SIZE['paddle']), 0, 4)
        
        # shadow
        self.shadow_surf = self.image.copy()
        pygame.draw.rect(self.shadow_surf, COLORS['paddle shadow'], pygame.FRect((0, 0), SIZE['paddle']), 0, 4)

        # motion
        self.direction = 0
        

    def move(self, dt):
        # move player in the direction
        self.rect.centery += self.direction * self.speed * dt
        
        # constrain player in screen
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        self.rect.bottom = WINDOW_HEIGHT if self.rect.bottom > WINDOW_HEIGHT else self.rect.bottom


    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.get_direction()
        self.move(dt)


class Player(Paddle):
    def __init__(self, groups):
        super().__init__(groups)
        self.speed = SPEED['player']
        self.rect = self.image.get_frect(center = POS['player'])
        # make copy rect for collision
        self.old_rect = self.rect.copy()


    def get_direction(self):
        # change direction on input
        keys = pygame.key.get_pressed()
        self.direction =  int(keys[pygame.K_DOWN] or keys[pygame.K_s]) - int(keys[pygame.K_UP] or keys[pygame.K_w])


class Opponent(Paddle):
    def __init__(self, groups, ball):
        super().__init__(groups)
        self.speed = SPEED['opponent']
        self.ball = ball
        self.rect = self.image.get_frect(center = POS['opponent'])
        # make copy rect for collision
        self.old_rect = self.rect.copy()

    def get_direction(self):
        self.direction = 1 if self.ball.rect.centery > self.rect.centery else -1


class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, paddle_sprites, update_score):
        super().__init__(groups)
        self.update_score = update_score
        self.paddle_sprites = paddle_sprites

        # circular image
        # srcalpha creates an alpha channel with 0 opacity
        # => ball image is not visible
        self.image = pygame.Surface(SIZE['ball'], pygame.SRCALPHA)
        # draw circle on the invisible surface
        pygame.draw.circle(self.image, COLORS['ball'], (SIZE['ball'][0] / 2, SIZE['ball'][1] / 2), SIZE['ball'][0] / 2)
        
        # shadow
        self.shadow_surf = self.image.copy()
        pygame.draw.circle(self.shadow_surf, COLORS['ball shadow'], (SIZE['ball'][0] / 2, SIZE['ball'][1] / 2), SIZE['ball'][0] / 2)

        # copy rect for collision
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.old_rect = self.rect.copy()
        
        # motion
        # random direction
        self.direction = pygame.Vector2(choice((1, -1)), uniform(0.7, 0.8) * choice((-1, -1)))
        self.speed_modifier = 0
        
        # timer
        self.start_time = pygame.time.get_ticks()
        self.duration = 1200


    def move(self, dt):
        self.rect.centerx += self.direction.x * SPEED['ball'] * dt * self.speed_modifier
        self.collision('horizontal')
        self.rect.centery += self.direction.y * SPEED['ball'] * dt * self.speed_modifier
        self.collision('vertical')


    def collision(self, direction):
        # use old position and new position to detect and handle collisions
        for sprite in self.paddle_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    # current overlap & condition before overlap

                    # if balls right and sprites left have collided
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                        self.direction.x *= -1

                    # ball left and sprite right
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                        self.direction.x *= -1
                    
                else:
                    # vertical collision

                    # ball bottom sprite top
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                        self.direction.y *= -1
                    
                    # ball top and sprite bottom
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                        self.direction.y *= -1


    def wall_collision(self):
        # ball is within display and bounces off edges
        if self.rect.top <= 0:
            self.rect.top = 0
            self.direction.y *= -1

        if self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.direction.y *= -1

        # score updates if ball hits sides
        if self.rect.right >= WINDOW_WIDTH or self.rect.left <= 0:
            self.update_score('player' if self.rect.x < WINDOW_WIDTH / 2 else 'opponent')
            self.reset()


    def reset(self):
        self.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.direction = self.direction = pygame.Vector2(choice((1, -1)), uniform(0.7, 0.8) * choice((-1, -1)))
        self.start_time = pygame.time.get_ticks()

    def timer(self):
        if pygame.time.get_ticks() >= self.start_time + self.duration:
            self.speed_modifier = 1
        else:
            self.speed_modifier = 0


    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.timer()
        self.move(dt)
        self.wall_collision()