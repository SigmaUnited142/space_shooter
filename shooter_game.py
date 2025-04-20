import pygame
from pygame import *
import random

pygame.init()

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')

background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)

shoot_sound = mixer.Sound('fire.ogg')  

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (100, 100))

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - self.rect.width:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -10)  
        bullets.add(bullet)
        shoot_sound.play()  

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.image = transform.scale(image.load(player_image), (80, 80))

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            global score_missed 
            score_missed += 1   
            self.rect.y = random.randint(-100, -40)  
            self.rect.x = random.randint(0, win_width - self.rect.width)

class Bullet(GameSprite):
    def __init__(self, bullet_image, bullet_x, bullet_y, bullet_speed):
        super().__init__(bullet_image, bullet_x, bullet_y, bullet_speed)
        self.image = transform.scale(image.load(bullet_image), (10, 20))

    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:  
            self.kill() 

player = Player('rocket.png', 300, 400, 5)

enemies = sprite.Group()
bullets = sprite.Group()

for _ in range(5):
    enemy = Enemy('ufo.png', random.randint(0, win_width - 80), random.randint(-100, -40), random.randint(1, 3))
    enemies.add(enemy)

score_hit = 0
score_missed = 0
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 70)

game = True
game_running = True 
clock = pygame.time.Clock()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE and game_running:  
                player.fire()
            if e.key == K_r: 
                score_hit = 0
                score_missed = 0
                bullets.empty()
                enemies.empty()
                for _ in range(5):
                    enemy = Enemy('ufo.png', random.randint(0, win_width - 80), random.randint(-100, -40), random.randint(1, 3))
                    enemies.add(enemy)
                game_running = True

    if game_running:
        window.blit(background, (0, 0))
        player.update()
        player.reset()
        
        enemies.update()
        enemies.draw(window)

        bullets.update()
        bullets.draw(window)

        for bullet in bullets:
            hit_enemies = sprite.spritecollide(bullet, enemies, False)  
            if hit_enemies:
                score_hit += len(hit_enemies) 
                bullet.kill()  
                for enemy in hit_enemies:
                    enemy.rect.y = random.randint(-100, -40)

        for enemy in enemies:
            if enemy.rect.y > win_height:
                score_missed += 1
                enemy.rect.y = random.randint(-100, -40) 
            
            if player.rect.colliderect(enemy.rect):
                score_missed += 1
                enemy.rect.y = random.randint(-100, -40)
                enemy.rect.x = random.randint(0, win_width - enemy.rect.width)
                game_running = False 
                lose_text = font2.render('Ты проиграл!', True, (255, 0, 0))
                window.blit(lose_text, (200, 200))
                
        missed_text = font1.render(f'Пропущено: {score_missed}', True, (255, 255, 255))
        hit_text = font1.render(f'Счёт: {score_hit}', True, (255, 255, 255))
        window.blit(missed_text, (10, 10))
        window.blit(hit_text, (10, 40)) 

        if score_hit >= 10:
            win_text = font2.render('Ты выиграл!', True, (0, 128, 0))
            window.blit(win_text, (200, 200))
            game_running = False  
        elif score_missed >= 3:
            lose_text = font2.render('Ты проиграл!', True, (255, 0, 0))
            window.blit(lose_text, (200, 200))
            game_running = False 
    else:
        restart_text = font1.render('Нажмите R для перезапуска', True, (255, 255, 255))
        window.blit(restart_text, (190, 250))

    display.update()
    clock.tick(60)

pygame.quit()