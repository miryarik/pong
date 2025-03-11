from settings import * 
from sprites import *
import json
from groups import AllSprites

class Game():
    def __init__(self):
        pygame.init()
        self.display_surf = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")
        # game loop and clock
        self.running = True
        self.clock = pygame.time.Clock()

        # groups and sprites
        self.all_sprites = AllSprites()
        self.paddle_sprites = pygame.sprite.Group()
        self.player = Player((self.all_sprites, self.paddle_sprites))
        self.ball = Ball(self.all_sprites, self.paddle_sprites, self.update_score)
        self.opponent = Opponent((self.all_sprites, self.paddle_sprites), self.ball)

        # score load
        try:
            with open(join('data', 'score.txt')) as score_file:
                self.score = json.load(score_file)
        except:
            self.score = {'player': 0, 'opponent': 0}

        # font
        self.font = pygame.font.Font(None, 160)


    def display_score(self):
        # player
        player_surf = self.font.render(str(self.score['player']), True, COLORS['bg detail'])
        player_rect = player_surf.get_frect(center = (WINDOW_WIDTH / 2 + 100, WINDOW_HEIGHT / 2))
        self.display_surf.blit(player_surf, player_rect)

        # opponent
        opponent_surf = self.font.render(str(self.score['opponent']), True, COLORS['bg detail'])
        opponent_rect = opponent_surf.get_frect(center = (WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2))
        self.display_surf.blit(opponent_surf, opponent_rect)

        # mid line
        pygame.draw.line(self.display_surf, COLORS['bg detail'], (WINDOW_WIDTH / 2, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT), 5)


    def update_score(self, side):
        self.score['player' if side == 'player' else 'opponent'] += 1



    def run(self):
        while self.running:
            # delta time in ms
            dt = self.clock.tick() / 1000

            # check if game was quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    # score save
                    with open(join('data', 'score.txt'), 'w') as score_file:
                        json.dump(self.score, score_file)

            # update all sprites with dt
            self.all_sprites.update(dt)            

            
            # draw 
            self.display_surf.fill(COLORS['bg'])
            self.display_score()
            self.all_sprites.draw()
       

            pygame.display.update()

        # recommended quit
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()



