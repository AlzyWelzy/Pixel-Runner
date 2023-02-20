import pygame
from sys import exit
from pathlib import Path

# Set the path to the high score file
high_score_path = Path("./high_score.txt")

if high_score_path.exists():
    # Read the high score from the file
    with open(high_score_path, "r") as f:
        high_score = int(f.read().strip())
else:
    # If file doesn't exists, set the high score to 0
    high_score = 0


def display_score():
    global high_score
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    score_surf = test_font.render(f"Score: {current_time}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)

    if current_time > high_score:
        high_score = current_time

        # Write the new high score to the file
        with open(high_score_path, "w") as f:
            f.write(str(high_score))

    high_score_surf = test_font.render(f"High Score: {high_score}", False, (64, 64, 64))
    high_score_rect = high_score_surf.get_rect(topleft=(10, 10))
    screen.blit(high_score_surf, high_score_rect)
    # print(current_time)


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("./font/Pixeltype.ttf", 50)
game_active = True
start_time = 0


sky_surface = pygame.image.load("./graphics/sky.png").convert()
ground_surface = pygame.image.load("./graphics/ground.png").convert()

text_surf = test_font.render("My Game", False, (64, 64, 64))
text_rect = text_surf.get_rect(center=(400, 100))


snail_surf = pygame.image.load("./graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surf.get_rect(bottomright=(600, 300))


# score_surf = test_font.render("Score", False, (64, 64, 64))  """This line of code uses Tuple for RBG color code"""
# score_surf = test_font.render("Score", False, "#404040")
# score_rect = score_surf.get_rect(center=(400, 50))


player_surf = pygame.image.load("./graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0

player_stand = pygame.image.load("./graphics/Player/player_stand.png").convert_alpha()
# player_stand = pygame.transform.scale(player_stand, (200, 400))
# player_stand = pygame.transform.scale2x(player_stand)
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))


while True:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20
                    game_active = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800
                start_time = pygame.time.get_ticks()

        # if event.type == pygame.KEYUP:
        #     print("Key Up")
        # if event.key == pygame.K_SPACE:
        #     print("Jump Down")

        # if event.type == pygame.MOUSEMOTION:
        # if event.type == pygame.MOUSEBUTTONDOWN:
        # if event.type == pygame.MOUSEBUTTONUP:
        #     print(event.pos)

        # if event.type == pygame.MOUSEMOTION:
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if player_rect.collidepoint(event.pos):
        #         # print("collision")
        #         player_gravity = -20

        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         player_gravity = -20
    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        # screen.blit(text_surface, (300, 50))
        # pygame.draw.rect(screen, "#c0e8ec", score_rect)
        # pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
        # screen.blit(score_surf, score_rect)
        display_score()

        # pygame.draw.line(screen, "Red", (0, 0), (800, 400), 1)
        # pygame.draw.line(screen, "Red", (0, 0), pygame.mouse.get_pos(), 1)
        # pygame.draw.ellipse(screen, "Grey", pygame.Rect(50, 200, 100, 100))

        snail_rect.x -= 4
        if snail_rect.right <= 0:
            snail_rect.left = 800
        screen.blit(snail_surf, snail_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity

        if player_rect.bottom >= 300:
            player_rect.bottom = 300

        screen.blit(player_surf, player_rect)
        screen.blit(text_surf, text_rect)

        # if player_rect.colliderect(snail_rect):
        #     print("COLLISION")

        # if player_rect.collidepoint(mouse_pos):
        #     print(pygame.mouse.get_pressed())

        # collision
        if snail_rect.colliderect(player_rect):
            game_active = False
            # pygame.quit()
            # exit()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

    pygame.display.update()
    clock.tick(60)
