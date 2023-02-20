import pygame
from sys import exit
from pathlib import Path
from random import randint

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

    return high_score


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False

    return True


def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        # jump
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

        # walk
    # play walking animation if the player is on the floor
    # display the jump surface when player is not on the floor


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Pixel Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("./font/Pixeltype.ttf", 50)
game_active = False
start_time = 0

score = high_score

sky_surface = pygame.image.load("./graphics/sky.png").convert()
ground_surface = pygame.image.load("./graphics/ground.png").convert()

game_name = test_font.render("Pixel Runner", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 90))

# Obstacles
snail_surf = pygame.image.load("./graphics/snail/snail1.png").convert_alpha()
# snail_rect = snail_surf.get_rect(bottomright=(600, 300))

fly_surf = pygame.image.load("./graphics/Fly/Fly1.png").convert_alpha()

obstacle_rect_list = []

# score_surf = test_font.render("Score", False, (64, 64, 64))  """This line of code uses Tuple for RBG color code"""
# score_surf = test_font.render("Score", False, "#404040")
# score_rect = score_surf.get_rect(center=(400, 50))


player_walk_1 = pygame.image.load("./graphics/Player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("./graphics/Player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("./graphics/Player/jump.png").convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0

player_stand = pygame.image.load("./graphics/Player/player_stand.png").convert_alpha()
# player_stand = pygame.transform.scale(player_stand, (200, 400))
# player_stand = pygame.transform.scale2x(player_stand)
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_message = test_font.render(
    "Press space bar to play the game", False, (111, 196, 169)
)
game_message_rect = game_message.get_rect(center=(400, 320))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

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
                # snail_rect.left = 800
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

        if event.type == obstacle_timer and game_active:
            if randint(0, 2):
                obstacle_rect_list.append(
                    snail_surf.get_rect(bottomright=(randint(900, 1100), 300))
                )
            else:
                obstacle_rect_list.append(
                    fly_surf.get_rect(bottomright=(randint(900, 1100), 210))
                )

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        # screen.blit(text_surface, (300, 50))
        # pygame.draw.rect(screen, "#c0e8ec", score_rect)
        # pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
        # screen.blit(score_surf, score_rect)
        score = display_score()

        # pygame.draw.line(screen, "Red", (0, 0), (800, 400), 1)
        # pygame.draw.line(screen, "Red", (0, 0), pygame.mouse.get_pos(), 1)
        # pygame.draw.ellipse(screen, "Grey", pygame.Rect(50, 200, 100, 100))

        # Player
        player_gravity += 1
        player_rect.y += player_gravity

        if player_rect.bottom >= 300:
            player_rect.bottom = 300

        player_animation()
        screen.blit(player_surf, player_rect)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        game_active = collisions(player_rect, obstacle_rect_list)

        # if player_rect.colliderect(snail_rect):
        #     print("COLLISION")

        # if player_rect.collidepoint(mouse_pos):
        #     print(pygame.mouse.get_pressed())

        # collision
        # if snail_rect.colliderect(player_rect):
        #     game_active = False
        # pygame.quit()
        # exit()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0

        screen.blit(game_name, game_name_rect)

        score_message = test_font.render(f"Your Score: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 370))

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
