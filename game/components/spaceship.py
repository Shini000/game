import pygame
from game.utils.constants import SPACESHIP,SCREEN_WIDTH,BULLET_TYPE,DEFAULT_TYPE

class Spaceship:
    width_spaceship = 40
    height_spaceship = 60
    X_POS = (SCREEN_WIDTH // 2) - 40
    Y_POS = 500
    SHOOTING_TIME = 16
    def __init__(self):
        self.image = SPACESHIP 
        self.image = pygame.transform.scale(self.image,(40,60))
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.is_alive = True
        self.shooting_time = 0
        self.power_type = DEFAULT_TYPE
        self.has_power = False
        self.power_time = 0
        self.live = 2

        
    def update(self,user_input,bullet_handler):
        self.shooting_time += 1
        if user_input[pygame.K_LEFT] or user_input[pygame.K_a]:
            self.move_left()
        if user_input[pygame.K_RIGHT] or user_input[pygame.K_d]:
            self.move_right()
        if user_input[pygame.K_UP] or user_input[pygame.K_w]:
            self.move_up()
        if user_input[pygame.K_DOWN] or user_input[pygame.K_s]:
            self.move_down()
        if user_input[pygame.K_SPACE] :
            self.shoot(bullet_handler)


    def draw(self,screen):
        screen.blit(self.image,self.rect)
        

    def move_left(self):
        if self.rect.left > 0:
            self.rect.x -= 10
        if self.rect.x == 0:
            self.rect.x = SCREEN_WIDTH


    def move_right(self):
        if self.rect.right < SCREEN_WIDTH :
            self.rect.x += 10
        if self.rect.x == (SCREEN_WIDTH - self.width_spaceship):
            self.rect.x = 0


    def move_up(self):
        if self.rect.y > (self.X_POS // 2)  :
            self.rect.y -= 10


    def move_down(self):
        if self.rect.y < self.X_POS :
            self.rect.y += 10
    
    def shoot(self,bullet_handler):
        if self.shooting_time % self.SHOOTING_TIME == 0:
            bullet_handler.add_bullet(BULLET_TYPE, self.rect.center)

    def set_power_image(self,image):
        self.image = image 
        self.image = pygame.transform.scale(self.image,(50,70))

    def set_default_image(self):
        self.image = SPACESHIP 
        self.image = pygame.transform.scale(self.image,(40,60))

    def reset (self):
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.is_alive = True
        self.live = 2