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

# Define player action variables
moving_left = False
moving_right = False
shoot = False

# Load images
bullet_img = pygame.image.load("img/icons/bullet.png").convert_alpha()

# Define colors
BG = (144, 201, 120)
RED = (255, 0, 0)

# methods
def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))



# classes
class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        # control if player or enemy is displayed
        self.char_type = char_type
        self.speed = speed
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
        animation_types = ['Idle', 'Run', 'Jump']
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
                self.frame_index = 0

    def update_action(self, new_action):
        # check if the new action is different than the previous one
        if new_action != self.action:
            self.action = new_action
            # update aniation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        # determine direction to draw character facing and draw
        img_to_flip = self.image
        # when True player faces left
        flip_in_x_axis = self.flip
        flip_in_y_axis = False
        pos_to_draw_at = self.rect
        # draws to screen
        screen.blit(pygame.transform.flip(img_to_flip, flip_in_x_axis, flip_in_y_axis), pos_to_draw_at)


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




# create sprite groups
# bullets
bullet_group = pygame.sprite.Group()





player = Soldier("player", 200, 200, 3, 5)
enemy = Soldier("enemy", 400, 200, 3, 5)



run = True
while run:
    CLOCK.tick(FPS)


    # display controls
    # draw background color
    draw_bg()

    # update and draw player image
    player.update_animation()
    player.draw()

    # draw enemy
    enemy.draw()

    # update and draw groups
    # draw bullets
    bullet_group.update()
    bullet_group.draw(screen)




    # update player actions if player is alive
    if player.alive:
        # shoot bullets
        if shoot:

            bullet = Bullet(player.rect.centerx + (0.6 * player.rect.size[0] * player.direction), player.rect.centery, player.direction)
            bullet_group.add(bullet)
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



    # updates screen each frame 
    pygame.display.update()



pygame.quit()