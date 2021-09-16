import pygame

pygame.init()


# set up display screen
SCREEN_WIDTH = 800
# lock the screen height to 80% of the screen width
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Scrolling Shooter")

# player
player_x, player_y = 200, 200
player_surface = pygame.image.load("img/player/idle/0.png")
player_rect = player_surface.get_rect()
player_rect.center = (player_x, player_y)




run = True
while run:
    # display controls
    screen.blit(player_surface, player_rect)





    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False



    # updates screen each frame 
    pygame.display.update()



pygame.quit()