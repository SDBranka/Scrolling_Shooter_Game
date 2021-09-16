import pygame

pygame.init()


# set up display screen
SCREEN_WIDTH = 800
# lock the screen height to 80% of the screen width
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Scrolling Shooter")



# define player action variables
moving_left = False
moving_right = False




class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("img/player/idle/0.png")
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, self.rect)






player = Soldier(200, 200, 3)



run = True
while run:
    # display controls
    player.draw()




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