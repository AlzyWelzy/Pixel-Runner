import pygame
from pathlib import Path
from random import choice
from player import Player
from obstacle import Obstacle


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


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Pixel Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("./font/Pixeltype.ttf", 50)
game_active = False
start_time = 0

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

score = high_score

bg_music = pygame.mixer.Sound("./audio/music.wav")
bg_music.play(loops=1)

sky_surface = pygame.image.load("./graphics/sky.png").convert()
ground_surface = pygame.image.load("./graphics/ground.png").convert()

game_name = test_font.render("Pixel Runner", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 90))


player_stand = pygame.image.load("./graphics/Player/player_stand.png").convert_alpha()

player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_message = test_font.render(
    "Press space bar to play the game", False, (111, 196, 169)
)
game_message_rect = game_message.get_rect(center=(400, 320))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)


while True:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["fly", "snail", "snail", "snail"])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                # snail_rect.left = 800
                start_time = pygame.time.get_ticks()

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        # player_rect.midbottom = (80, 300)
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
