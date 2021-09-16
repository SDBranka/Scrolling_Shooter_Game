import pygame

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


# define player action variables
moving_left = False
moving_right = False

# define colors
BG = (144, 201, 120)

def draw_bg():
    screen.fill(BG)



class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        # 1 (right) or -1 (left) determine if character is looking left or right
        self.direction = 1
        self.flip = False
        img = pygame.image.load("img/player/idle/0.png")
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
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



        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy



    def draw(self):

        # determine direction to draw character facing and draw
        img_to_flip = self.image
        # when True player faces left
        flip_in_x_axis = self.flip
        flip_in_y_axis = False
        pos_to_draw_at = self.rect
        screen.blit(pygame.transform.flip(img_to_flip, flip_in_x_axis, flip_in_y_axis), pos_to_draw_at)






player = Soldier(200, 200, 3, 5)



run = True
while run:
    CLOCK.tick(FPS)


    # display controls
    # draw background color
    draw_bg()

    # draw player
    player.draw()
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
            # player movement
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
        # keybord releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False



    # updates screen each frame 
    pygame.display.update()



pygame.quit()