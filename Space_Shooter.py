import pygame
import random
import os
import sys

# Parameters of the window
width = 800
height = 600
fps = 60

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
purple = (255, 0, 255)
cyan = (0, 255, 255)

# The os.path to images (all the images are in the project folder)
# To make the game work on any computer
main_icon_dir = os.path.join(os.path.dirname(__file__), "data", "icon")
sound_dir = os.path.join(os.path.dirname(__file__), "data", "sound")
ships_dir = os.path.join(os.path.dirname(__file__), "data", "ships")
lasers_dir = os.path.join(os.path.dirname(__file__), "data", "lasers")
back_dir = os.path.join(os.path.dirname(__file__), "data", "background.png")
expl_dir = os.path.join(os.path.dirname(__file__), "data", "explosions")
lives_dir = os.path.join(os.path.dirname(__file__), "data", "icon")

# Creating the window and initializing pygame module
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space shooter")
main_icon = pygame.image.load(os.path.join(main_icon_dir, "main_icon.ico"))
pygame.display.set_icon(main_icon)
clock = pygame.time.Clock()

# Loading images
ships_img = ["enemyBlack1.png", "enemyBlack2.png", "enemyBlack3.png", "enemyBlack4.png",
             "enemyBlack5.png", "enemyBlue1.png", "enemyBlue2.png", "enemyBlue3.png",
             "enemyBlue4.png", "enemyBlue5.png", "enemyGreen1.png", "enemyGreen2.png",
             "enemyGreen3.png", "enemyGreen4.png", "enemyGreen5.png", "enemyRed1.png",
             "enemyRed2.png", "enemyRed3.png", "enemyRed4.png", "enemyRed5.png"]
enemies_images = []
for i in ships_img:
    enemies_images.append(pygame.image.load(os.path.join(ships_dir, i)))

expl_anim = []
for i in range(9):
    filename = f"regularExplosion0{i}.png"
    expl_anim.append(pygame.image.load(os.path.join(expl_dir, filename)))

player_img = pygame.image.load(os.path.join(ships_dir, "player.png"))
enemies_laser = pygame.image.load(os.path.join(lasers_dir, "laserRed05.png"))
player_laser = pygame.image.load(os.path.join(lasers_dir, "laserBlue05.png"))
background = pygame.image.load(back_dir)
background = pygame.transform.scale(background, (width, height))
background_rect = background.get_rect()
heart_full_img = pygame.image.load(os.path.join(lives_dir, "heart_full.bmp"))
heart_full_img.set_colorkey(white)  # Ignoring the color in the brackets
heart_empty_img = pygame.image.load(os.path.join(lives_dir, "heart_empty.bmp"))
heart_empty_img.set_colorkey(white)  # Ignoring the color in the brackets

# The sounds
shoot_sound = pygame.mixer.Sound(os.path.join(sound_dir, "laser.wav"))
expl_sound = pygame.mixer.Sound(os.path.join(sound_dir, "explosion.wav"))
death_sound = pygame.mixer.Sound(os.path.join(sound_dir, "player_death.ogg"))
shoot_sound.set_volume(0.4)
expl_sound.set_volume(0.4)
pygame.mixer.music.load(os.path.join(sound_dir, "main_music.ogg"))
pygame.mixer.music.set_volume(0.4)

font_name = pygame.font.match_font("arial")


# Drawing any text
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surf = font.render(text, True, white)
    text_rect = text_surf.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surf, text_rect)


def draw_hp(surf, text, x, y):
    if text < 0:
        text = 0
    bar_length = 100
    bar_height = 10
    fill = (text / 100) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    if fill >= 70:
        pygame.draw.rect(surf, green, fill_rect)
    elif fill >= 35:
        pygame.draw.rect(surf, yellow, fill_rect)
    else:
        pygame.draw.rect(surf, red, fill_rect)
    pygame.draw.rect(surf, white, outline_rect, 2)


def draw_full_lives(surf, lives, x, y, img):
    for j in range(lives):
        img_rect = heart_full_img.get_rect()
        img_rect.x = x + 50 * j
        img_rect.y = y
        surf.blit(img, img_rect)


def draw_empty_lives(surf, lives, x, y, img):
    for k in range(3 - lives):
        img_rect = heart_empty_img.get_rect()
        img_rect.x = x - 50 * k
        img_rect.y = y
        surf.blit(img, img_rect)


# Responsible for creating a new enemy
def new_enemy():
    enemy = Enemies()
    all_sprites.add(enemy)
    enemies.add(enemy)


# Drawing the introduction screen (also after game over)
def intro():
    screen.blit(background, background_rect)
    draw_text(screen, "Space Shooter", 70, width / 2, height / 4 - 20)
    draw_text(screen, str(score), 30, width / 2, 10)
    draw_text(screen, "Счетчик жизней", 25, width - 85, 50)
    draw_text(screen, "Полоска здоровья", 25, 95, 50)
    draw_text(screen, "Счет", 35, width / 2, 50)
    draw_full_lives(screen, 3, width - 150, 10, heart_full_img)
    draw_hp(screen, 100, 15, 20)
    draw_text(screen, "Пробел - стрельба (можно удерживать)", 35, width / 2, height / 2 - 50)
    draw_text(screen, "Стрелки влево и вправо - движение", 35, width / 2, height / 2)
    draw_text(screen, "Игра начинается с одного врага", 25, width / 2, height / 2 + 55)
    draw_text(screen, "После каждых 10 очков будет появляться еще один враг", 25, width / 2, height / 2 + 100)
    draw_text(screen, "Две пули уничтожаются при столкновении", 25, width / 2, height / 2 + 148)
    draw_text(screen, "Враги могут убивать друг друга (очки не начисляются)", 25, width / 2, height / 2 + 195)
    draw_text(screen, "Нажмите ENTER для начала игры ", 35, width / 2, height / 2 + 240)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(fps)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                sys.exit()  # Exiting the window (the program stops)
            if ev.type == pygame.KEYUP:
                if ev.key == pygame.K_RETURN:  # K_RETURN is Enter
                    waiting = False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_img, (50, 50))
        self.rect = self.image.get_rect()  # Getting the size of the image
        self.rect.centerx = width / 2  # Setting up the position
        self.rect.bottom = height - 10
        self.speed_x = 0
        self.hp = 100
        self.shoot_delay = 250  # Time to wait before next shot
        self.last_shot = pygame.time.get_ticks()  # The timer for the last shot
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_timer >= 1000:
            # The spaceship will be hidden within 2 seconds after death
            self.hidden = False
            self.rect.centerx = width / 2
            self.rect.bottom = height - 10
        self.speed_x = 0
        # Check for pressing keys
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.speed_x = -8
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.speed_x = 8
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speed_x
        # The code below doesn't let the spaceship disappear
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width

    def shoot(self):
        now = pygame.time.get_ticks()
        if self.hidden is False and now - self.last_shot >= self.shoot_delay:
            self.last_shot = now
            # Here we call PlayerBullets class to take a shot
            bullet = PlayerBullets(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            player_bullets.add(bullet)
            shoot_sound.play()  # Playing the sound of shooting

    # This function is responsible for hiding the spaceship
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (width / 2, -1000)  # It moves the spaceship off the screen


class Enemies(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(random.choice(enemies_images), (45, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, width - 50)  # Appearing at different places on the screen
        self.rect.y = -20
        self.speed_y = 5

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y == 40:  # Time to take a shot
            bullet = EnemiesBullets(self.rect.centerx, self.rect.bottom)
            all_sprites.add(bullet)
            enemies_bullets.add(bullet)
        if self.rect.y > height + 20:  # Disappearing after leaving the screen
            self.rect.x = random.randrange(0, width - 30)
            self.rect.y = -20
            self.speed_y = 5


class PlayerBullets(pygame.sprite.Sprite):
    def __init__(self, x, y):  # The parameters for the position of the player
        super().__init__()
        self.image = pygame.transform.scale(player_laser, (10, 25))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y < 0:
            self.kill()  # Disappearing after leaving the screen


class EnemiesBullets(pygame.sprite.Sprite):
    def __init__(self, x, y):  # The parameters for the position of the enemies
        super().__init__()
        self.image = pygame.transform.scale(enemies_laser, (10, 25))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed_y = 10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.y > height + 5:
            self.kill()  # Disappearing after leaving the screen


class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = expl_anim[0]  # The initial frame (zero frame)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.frame = 0
        self.last_update = pygame.time.get_ticks()  # The timer
        self.fps = 60

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.fps:  # Time to change the frame
            self.last_update = now
            self.frame += 1  # Changing the frame
        if self.frame < len(expl_anim):
            pos = self.rect.center
            self.image = expl_anim[self.frame]
            self.rect = self.image.get_rect()
            self.rect.center = pos
        else:
            self.kill()  # If all frames have been played


# The sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemies_bullets = pygame.sprite.Group()
player = Player()
death_expl = Explosion(player.rect.midtop)
all_sprites.add(player)

pygame.mixer.music.play(loops=-1)  # Playing music
score = 0
# Game loop
game_over = True
running = True
difficulty = 1
while running:
    if game_over:
        intro()
        game_over = False
        # Resetting all sprites, lives and score
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        player_bullets = pygame.sprite.Group()
        enemies_bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(1):
            new_enemy()
        score = 0
    # Controlling the loop speed
    clock.tick(fps)
    # Process input (response)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()  # Exiting the window (the program stops)
    # Updating the picture
    all_sprites.update()
    # Check for collision
    damage_from_collision = pygame.sprite.spritecollide(player, enemies, True)
    damage_from_bullets = pygame.sprite.spritecollide(player, enemies_bullets, True)
    if damage_from_collision:
        expl_sound.play()  # Playing the sound of explosion
        expl = Explosion(player.rect.midtop)
        all_sprites.add(expl)
        new_enemy()  # A new enemy should appear after the death of another
        if pygame.time.get_ticks() - player.hide_timer >= 4000 or player.lives == 3:
            player.hp -= 50  # Losing HP
        if player.hp <= 0:
            death_sound.play()  # Playing the sound of explosion
            death_expl = Explosion(player.rect.center)
            all_sprites.add(death_expl)
            player.hide()
            player.lives -= 1  # Losing one life
            player.hp = 100

    if damage_from_bullets:
        if pygame.time.get_ticks() - player.hide_timer >= 4000 or player.lives == 3:
            player.hp -= 20  # Losing HP
        if player.hp <= 0:
            death_sound.play()  # Playing the sound of explosion
            death_expl = Explosion(player.rect.center)
            all_sprites.add(death_expl)
            player.hide()
            player.lives -= 1  # Losing one life
            player.hp = 100

    if player.lives == 0 and not death_expl.alive():
        game_over = True  # GAME OVER

    # Check for killing the enemy
    kills = pygame.sprite.groupcollide(enemies, player_bullets, True, True)
    kills_each_other = pygame.sprite.groupcollide(enemies_bullets, enemies, True, True)
    bullets_collision = pygame.sprite.groupcollide(player_bullets, enemies_bullets, True, True)
    for kill in kills:
        expl_sound.play()
        expl = Explosion(kill.rect.center)
        all_sprites.add(expl)
        score += 1
        if score == difficulty * 10:
            difficulty += 1
            new_enemy()
        new_enemy()  # A new enemy should appear after the death of another
    for kill in kills_each_other:
        new_enemy()  # A new enemy should appear after the death of another
    # Rendering
    screen.fill(black)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    # Drawing the interface
    draw_text(screen, str(score), 30, width / 2, 10)
    draw_hp(screen, player.hp, 15, 20)
    draw_full_lives(screen, player.lives, width - 150, 10, heart_full_img)
    draw_empty_lives(screen, player.lives, width - 50, 10, heart_empty_img)
    # Display flip
    pygame.display.flip()
