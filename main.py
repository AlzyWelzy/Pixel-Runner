import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("./font/Pixeltype.ttf", 50)

sky_surface = pygame.image.load("./graphics/sky.png").convert()
ground_surface = pygame.image.load("./graphics/ground.png").convert()
# text_surface = test_font.render("My Game", False, "Black")

snail_surf = pygame.image.load("./graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surf.get_rect(bottomright=(600, 300))

# score_surf = test_font.render("Score", False, (64, 64, 64))
score_surf = test_font.render("Score", False, "#404040")
score_rect = score_surf.get_rect(center=(400, 50))


player_surf = pygame.image.load("./graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, 300))

player_gravity = 0

while True:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            # print("Key Down")
            if event.key == pygame.K_SPACE:
                print("Jump Down")

        if event.type == pygame.KEYUP:
            print("Key Up")
            # if event.key == pygame.K_SPACE:
            #     print("Jump Down")

        # if event.type == pygame.MOUSEMOTION:
        # if event.type == pygame.MOUSEBUTTONDOWN:
        # if event.type == pygame.MOUSEBUTTONUP:
        #     print(event.pos)

        # if event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(event.pos):
        #         print("collision")

    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    # screen.blit(text_surface, (300, 50))
    pygame.draw.rect(screen, "#c0e8ec", score_rect)
    pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
    screen.blit(score_surf, score_rect)

    # pygame.draw.line(screen, "Red", (0, 0), (800, 400), 1)
    # pygame.draw.line(screen, "Red", (0, 0), pygame.mouse.get_pos(), 1)
    # pygame.draw.ellipse(screen, "Grey", pygame.Rect(50, 200, 100, 100))

    snail_rect.x -= 4
    if snail_rect.right <= 0:
        snail_rect.left = 800
    screen.blit(snail_surf, snail_rect)

    screen.blit(player_surf, player_rect)

    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]:
    #     print("Jump")

    # if player_rect.colliderect(snail_rect):
    #     print("COLLISION")

    # if player_rect.collidepoint(mouse_pos):
    #     print(pygame.mouse.get_pressed())

    pygame.display.update()
    clock.tick(60)
