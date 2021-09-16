import pygame

pygame.init()


# set up display screen
SCREEN_WIDTH = 800
# lock the screen height to 80% of the screen width
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Scrolling Shooter")


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
player2 = Soldier(400, 200, 3)



run = True
while run:
    # display controls
    player.draw()
    player2.draw()




    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False



    # updates screen each frame 
    pygame.display.update()



pygame.quit()