import pygame
import os

# initialize pygame
pygame.init()


# set up display screen
SCREEN_WIDTH = 800
# lock the screen height to 80% of the screen width
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Scrolling Shooter")

# set frame rate
CLOCK = pygame.time.Clock()
FPS = 60

# Define game variables
GRAVITY = 0.75
TILE_SIZE = 40

# Define player action variables
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False

# Load images
# bullet
bullet_img = pygame.image.load("img/icons/bullet.png").convert_alpha()
# grenade
grenade_img = pygame.image.load("img/icons/grenade.png").convert_alpha()
# item boxes
health_box_img = pygame.image.load("img/icons/health_box.png").convert_alpha()
ammo_box_img = pygame.image.load("img/icons/ammo_box.png").convert_alpha()
grenade_box_img = pygame.image.load("img/icons/grenade_box.png").convert_alpha()
item_boxes = {
    'Health' : health_box_img,
    'Ammo' : ammo_box_img,
    'Grenade' : grenade_box_img
}

# Define colors
BG = (144, 201, 120)
# BG = "Black"
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# methods
# define font
font_type = "Futura"
font_size = 30
font = pygame.font.SysFont(font_type, font_size)

def draw_text(text_to_display, font, text_color, x, y):
    img = font.render(text_to_display, True, text_color)
    screen.blit(img, (x, y))

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))



# classes
class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed, ammo, grenades):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        # control if player or enemy is displayed
        self.char_type = char_type
        self.speed = speed
        self.ammo = ammo
        self.start_ammo = ammo
        # limit the frequency that the player can fire
        # every time the player fires the value is increased
        # and then brought back down to zero such that a player 
        # may only fire when the shoot_cooldown is zero 
        self.shoot_cooldown = 0
        self.grenades = grenades
        # set character health
        self.health = 100
        self.max_health = self.health
        # 1 (right) or -1 (left) determine if character is looking left or right
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        # control which frame of animation cycle is displayed
        self.animation_list = []
        self.frame_index = 0
        # character's action: 0 = idle, 1 = run 
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # load all images for the players
        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            # build animation cycle list for idle
            # reset temp list of images
            temp_list = []
            # count number of files in the folder
            num_of_frames = len(os.listdir(f"img/{self.char_type}/{animation}"))
            for i in range(num_of_frames):
                img = pygame.image.load(f"img/{self.char_type}/{animation}/{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            # add the temp_list to the animation list
            self.animation_list.append(temp_list)        
        
        # set the player surface to the correct display
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animation()
        self.check_alive()
        # update shoot cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, moving_left, moving_right):
        # reset movement variables
        # change in x and y 
        dx = 0
        dy = 0

        # assign movement variable if moving left of right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -18
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        # set terminal velocity
        # if player velocity tries to exceed the limit it 
        # is set to its self
        vel_y_limit = 10
        if self.vel_y > vel_y_limit:
            self.vel_y 
        dy += self.vel_y
        # add floor
        # if the bottom of the player is going below the line drawn
        # correct the position to the level of the floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.6 * self.rect.size[0] * self.direction), self.rect.centery, player.direction)
            bullet_group.add(bullet)
            self.ammo -= 1

    def ai(self):
        if self.alive and player.alive:
            if self.direction == 1:
                ai_moving_right = True
            else:
                ai_moving_right = False
            ai_moving_left = not ai_moving_right
            self.move(ai_moving_left, ai_moving_right)



    def update_animation(self):
        # define timer (controls speed of animation)
        ANIMATION_COOLDOWN = 100

        # update image based on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            # reset the timer
            self.update_time = pygame.time.get_ticks()
            # control which frame will be displayed
            self.frame_index += 1
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 3:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different than the previous one
        if new_action != self.action:
            self.action = new_action
            # update aniation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            # set to zero so no negative health
            self.health = 0
            # set to zero so that charater doesn't continue moving
            self.speed = 0
            # set to False so that character is dead
            self.alive = False

            self.update_action(3)

    def draw(self):
        # determine direction to draw character facing and draw
        img_to_flip = self.image
        # when True player faces left
        flip_in_x_axis = self.flip
        flip_in_y_axis = False
        pos_to_draw_at = self.rect
        # draws to screen
        screen.blit(pygame.transform.flip(img_to_flip, flip_in_x_axis, flip_in_y_axis), pos_to_draw_at)
        # # draw border around character rectangles
        # where_to_draw_border = screen
        # color_of_border = RED
        # around_what_to_draw_border = self.rect
        # border_width = 1
        # pygame.draw.rect(where_to_draw_border, color_of_border, around_what_to_draw_border, border_width)


class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        # // takes the floor of a division
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        # collision - player pick up box
        item_box_to_collide = self
        character_to_collide = player
        if pygame.sprite.collide_rect(item_box_to_collide, character_to_collide):
            # check type of item box
            if self.item_type == 'Health':
                player.health += 25
                # limit player health to max_health
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Ammo':
                player.ammo += 50
            elif self.item_type == 'Grenade':
                player.grenades += 10
            # delete item box
            self.kill()


class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health):
        # update with new health
        self.health = health

        # health bar is designed such that there is a constant red
        # health bar always displayed and a green health bar that 
        # increments over top of it to show the player's current health
        where_to_draw = screen
        color_of_rect = RED
        rect_x_pos = self.x
        rect_y_pos = self.y
        rect_width = 150
        rect_height = 20
        # draw a border for the health bar
        pygame.draw.rect(where_to_draw, BLACK, (rect_x_pos - 2, rect_y_pos - 2, rect_width + 4, rect_height + 4))

        # draw the base health bar
        pygame.draw.rect(where_to_draw, color_of_rect, (rect_x_pos, rect_y_pos, rect_width, rect_height))

        # draw the current health bar
        ratio = self.health / self.max_health
        pygame.draw.rect(where_to_draw, GREEN, (rect_x_pos, rect_y_pos, rect_width * ratio, rect_height))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    
    def update(self):
        # move bullet
        self.rect.x += (self.direction * self.speed)
        # check if bullet has left screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        # check collision with characters
        # player
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        # enemies
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    # print(enemy.health)
                    self.kill()


class Grenade(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer = 100
        self.vel_y = -11
        self.speed = 7
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.vel_y += GRAVITY
        # handle the change in x and y to create motion
        dx = self.direction * self.speed
        dy = self.vel_y

        # collision
        # add floor
        # if the bottom of the grenade is going 
        # below the line drawn correct the position 
        # to the level of the floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            # without setting this self.speed to zero the grenade bowls
            self.speed = 0
        # check if grenade collision with screen edge
        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            self.direction *= -1
            dx = self.direction * self.speed

        # update grenade position
        self.rect.x += dx
        self.rect.y += dy

        # countdown timer for explosion
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            x_pos_of_grenade = self.rect.x
            y_pos_of_grenade = self.rect.y
            scale_for_explosion = 0.5
            explosion = Explosion(x_pos_of_grenade, y_pos_of_grenade, scale_for_explosion)
            explosion_group.add(explosion)
            # do damage to anyone that is nearby
            blast_radius = TILE_SIZE * 2
            
            # check for player
            center_of_grenade_x = self.rect.centerx
            center_of_player_x = player.rect.centerx
            center_of_grenade_y = self.rect.centery
            center_of_player_y = player.rect.centery
            # if the absolute value of the difference in distance 
                # between the player and the grenade are within the blast radius
            if (center_of_grenade_x - center_of_player_x ) < blast_radius and\
                    (center_of_grenade_y - center_of_player_y ) < blast_radius:
                # player loses 50 health
                player.health -= 50

            # check for enemy
            for enemy in enemy_group:
                center_of_grenade_x = self.rect.centerx
                center_of_enemy_x = enemy.rect.centerx
                center_of_grenade_y = self.rect.centery
                center_of_enemy_y = enemy.rect.centery               
                # between the enemy and the grenade are within the blast radius
                if (center_of_grenade_x - center_of_enemy_x ) < blast_radius and\
                        (center_of_grenade_y - center_of_enemy_y ) < blast_radius:
                    # enemy loses 50 health
                    enemy.health -= 50


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f'img/explosion/exp{num}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        # define speed at which animation will run
        EXPLOSION_SPEED = 4
        # update explosion animation
        self.counter += 1
        # fuse = if the counter reaches the explosion speed
        if self.counter >= EXPLOSION_SPEED:
            # the counter resets
            self.counter = 0
            # the frame displayed changes
            self.frame_index += 1
            # if animation is complete 
            if self.frame_index >= len(self.images):
                # delete the explosion
                self.kill()
            # if animation is not complete 
            else:
                # the image is updated to the new frame
                self.image = self.images[self.frame_index]







    def draw(self):
        pass



# create sprite groups
# enemies
enemy_group = pygame.sprite.Group()
# bullets
bullet_group = pygame.sprite.Group()
# grenades
grenade_group = pygame.sprite.Group()
# explosions
explosion_group = pygame.sprite.Group()
# item boxes
item_box_group = pygame.sprite.Group()


# temp create item boxes
item_box = ItemBox("Health", 100, 260)
item_box_group.add(item_box)
item_box = ItemBox("Ammo", 400, 260)
item_box_group.add(item_box)
item_box = ItemBox("Grenade", 500, 260)
item_box_group.add(item_box)



# create a player instance
player = Soldier("player", 200, 200, 1.65, 5, 2000, 5)
# create a health bar
health_bar = HealthBar(10, 10, player.health, player.health)
# create an enemy instances and add them to the enemy group
enemy = Soldier("enemy", 400, 200, 1.65, 5, 20, 0)
enemy2 = Soldier("enemy", 300, 200, 1.65, 5, 20, 0)
enemy_group.add(enemy)
enemy_group.add(enemy2)

run = True
while run:
    CLOCK.tick(FPS)

    # display controls
    # draw background color
    draw_bg()

    # show health
    health_bar.draw(player.health)

    # show ammo
    draw_text(f'AMMO: {player.ammo}', font, WHITE, 10, 35)
    # # show ammo as images
    # draw_text('AMMO: ', font, WHITE, 10, 35)
    # for x in range(player.ammo):
    #     screen.blit(bullet_img, (90 + (x * 10), 40))

    # # show grenades
    # draw_text(f'GRENADES: {player.grenades}', font, WHITE, 10, 60)
    # show grenades as images
    draw_text('GRENADES: ', font, WHITE, 10, 60)
    for x in range(player.grenades):
        # fifteen is width of grenade_img
        screen.blit(grenade_img, (135 + (x * 15), 60))

    # update and draw player image
    player.update()
    player.draw()

    # update and draw enemies
    for enemy in enemy_group:
        enemy.ai()
        enemy.update()
        enemy.draw()

    # update and draw groups
    # draw bullets
    bullet_group.update()
    bullet_group.draw(screen)
    # draw item_boxs
    item_box_group.update()
    item_box_group.draw(screen)
    # draw grenades
    grenade_group.update()
    grenade_group.draw(screen)
    # handle explosions
    explosion_group.update()
    explosion_group.draw(screen)
    

    # update player actions if player is alive
    if player.alive:
        # shoot bullets
        if shoot:
            player.shoot()
        # throw grenades
        elif grenade and not grenade_thrown and  player.grenades > 0:
            grenade = Grenade(player.rect.centerx + (player.rect.size[0] * player.direction),\
                            player.rect.top, player.direction)
            grenade_group.add(grenade)
            grenade_thrown = True
            player.grenades -= 1
            # print(player.grenades)
        
        # if player in air cange image to jump
        if player.in_air:
            player.update_action(2)
        # if player is moving change image to run
        elif moving_left or moving_right:
            player.update_action(1)
        # if player is not moving change image to idle
        else:
            player.update_action(0)
        # move player
        player.move(moving_left, moving_right)



    # event handler
    for event in pygame.event.get():
        # close game if exit button is clicked
        if event.type == pygame.QUIT:
            run = False
        # keyboard strikes
        if event.type == pygame.KEYDOWN:
            # close game if escape key is pressed
            if event.key == pygame.K_ESCAPE:
                run = False
            # player actions
            # move left
            if event.key == pygame.K_a:
                moving_left = True
            # move right
            if event.key == pygame.K_d:
                moving_right = True
            # jump
            if event.key == pygame.K_e and player.alive:
                player.jump = True
            # fire weapon 
            if event.key == pygame.K_SPACE:
                shoot = True
            # throw grenade
            if event.key == pygame.K_t:
                grenade = True
            

        # keybord releases
        if event.type == pygame.KEYUP:
            # stop moving left
            if event.key == pygame.K_a:
                moving_left = False
            # stop moving right
            if event.key == pygame.K_d:
                moving_right = False
            # stop firing weapon 
            if event.key == pygame.K_SPACE:
                shoot = False
            # stop throwing grenade
            if event.key == pygame.K_t:
                grenade = False
                grenade_thrown = False


    # updates screen each frame 
    pygame.display.update()


pygame.quit()