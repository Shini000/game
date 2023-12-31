import pygame
import pygame.mixer

from game.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, WHITE_COLOR, GOLD_COLOR,BUTTON_PLAY,DEFAULT_TYPE,HEART_TYPE,GOLD_LIGHT_COLOR,RED_COLOR,BACKGROUND_1
from game.components.spaceship import Spaceship
from game.components.enemies.enemy_handler import EnemyHandler
from game.components.bullets.bullet_handler import BulletHandler
from game.components.powers.power_handler import PowerHandler
from game.components.enemies.enemy_three import EnemyThree
from game.components import text_utils

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 5
        self.x_pos_bg = 0
        self.y_pos_bg = 0
        self.player = Spaceship()
        self.enemy_handler = EnemyHandler()
        self.bullet_handler = BulletHandler()
        self.boss = EnemyThree()
        self.score = 0
        self.number_death = 0
        self.max_score = 0
        self.power_handler = PowerHandler()
        self.sound = pygame.mixer.Sound("game/assets/music/teme.wav")
        self.sound.play(-1)
        self.sound.set_volume(0.1)
        self.sound_death = None
        self.play_button = None
        self.power_time = None
        self.score_boss = 0
        self.live = 0
        self.live_boss = 0
        self.valid = None

    def run(self):
        # Game loop: events - update - draw
        self.running = True
        while self.running:
            self.events()
            self.update()
            self.draw()
        pygame.display.quit()
        pygame.quit()

    def events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.playing:
                mousepos = pygame.mouse.get_pos()
                self.button_pos(mousepos)
               
    def update(self):
        if self.playing:
            self.valid_boss()
            user_input = pygame.key.get_pressed()
            self.player.update(user_input,self.bullet_handler)
            self.enemy_handler.update(self.bullet_handler)
            self.bullet_handler.update(self.player,self.enemy_handler.enemies)
            self.score = self.enemy_handler.number_enemy_destroyed
            self.score_boss = self.enemy_handler.boss_kill
            self.live_boss = self.boss.live
            self.power_handler.update(self.player)
            self.live = self.player.live
            if not self.player.is_alive:
                self.sound_death = pygame.mixer.Sound("game/assets/music/death.wav")
                self.sound_death.play()
                self.sound.set_volume(0.5)
                pygame.time.delay(1500)
                self.playing = False
                self.number_death += 1
                
    def draw(self):
        self.bg_draw()
        if self.playing:
            self.draw_background()
            self.clock.tick(FPS)
            self.player.draw(self.screen)
            self.enemy_handler.draw(self.screen)
            self.bullet_handler.draw(self.screen)
            self.power_handler.draw(self.screen)
            self.draw_score()
            self.draw_power_time()
        else:
            self.draw_menu()
        pygame.display.update()
        pygame.display.flip()

    def bg_draw(self):
        image = pygame.transform.scale(BACKGROUND_1, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(image, (0, 0))


    def draw_background(self):
        image = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        image_height = image.get_height()
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
        if self.y_pos_bg >= SCREEN_HEIGHT:
            self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
            self.y_pos_bg = 0
        self.y_pos_bg += self.game_speed

    def draw_menu(self):
        if self.number_death == 0:
            play,play_rect = text_utils.get_image(BUTTON_PLAY)
            self.screen.blit(play,play_rect)
            self.play_button = play_rect
        else:

            if self.max_score < self.score:
                self.max_score = self.score
            play,play_rect = text_utils.get_image(BUTTON_PLAY)
            self.screen.blit(play,play_rect)
            score_boss,score_boss_rect = text_utils.get_message(f"dead bosses is: {self.score_boss}",25,WHITE_COLOR,width= 130,height= 110)
            score,score_rect = text_utils.get_message(f"your score is: {self.score}",25,WHITE_COLOR,width= 115,height=20)
            number_death,number_death_rect = text_utils.get_message(f"you have died {self.number_death} times",25,WHITE_COLOR,width=155,height= 80)
            max_score,max_score_rect = text_utils.get_message(f"your score record is : {self.max_score}",25,GOLD_COLOR,width=160,height= 50)
            self.screen.blit(max_score,max_score_rect)
            self.screen.blit(number_death,number_death_rect)
            self.screen.blit(score,score_rect)
            self.screen.blit(score_boss,score_boss_rect)
            


    def button_pos(self,mousepos):
        if self.play_button.collidepoint(mousepos):
            self.playing = True
            self.reset()



    def draw_score(self):
        if self.valid:
            live_boss, live_boss_rect = text_utils.get_message(f"boss life max {self.live_boss}", 20,RED_COLOR, 500, 40)
            self.screen.blit(live_boss, live_boss_rect)

        live, live_rect = text_utils.get_message(f"Your lives {self.live}", 20,GOLD_LIGHT_COLOR, 800, 40)
        self.screen.blit(live, live_rect)
        score, score_rect = text_utils.get_message(f"Your score is {self.score}", 20, WHITE_COLOR, 1000, 40)
        self.screen.blit(score, score_rect)

    def draw_power_time(self):
        if self.player.has_power and not self.player.power_type == HEART_TYPE :
            self.power_time = round((self.player.power_time - pygame.time.get_ticks())/1000,1)
            if self.power_time >= 0:
                text,text_rect = text_utils.get_message(f"{self.player.power_type.capitalize()} is enable for : {self.power_time} ",15,WHITE_COLOR,150,50)
                self.screen.blit(text,text_rect)
            else:
                self.player.has_power = False
                self.player.power_type = DEFAULT_TYPE
                self.player.set_default_image()

    def valid_boss(self):
        lista =self.enemy_handler.enemies
        for enemy in lista :
            if type(enemy) == EnemyThree:
                self.valid = True
            if not type(enemy) == EnemyThree: 
                self.valid = False
    def reset(self):
        self.player.reset()
        self.enemy_handler.reset()
        self.bullet_handler.reset()
        self.power_handler.reset()
        self.power_time = None
        self.boss.retec()
        self.sound.set_volume(0.1)