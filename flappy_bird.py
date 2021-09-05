import pygame, sys, random

#                                                   ---------FUNCTIONS------------

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 500))
    screen.blit(floor_surface, (floor_x_pos + 576, 500))

def create_pipe():
    random_pipe_height = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_height))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_height-150))
    return top_pipe, bottom_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            inverted_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(inverted_pipe, pipe)

def check_collison(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):

            return False
        if bird_rect.top <= -100 or bird_rect.bottom >= 490:

            return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, bird_movement*3 , 1)
    return new_bird

def score_check(pipes):
    score = 0
    for pipe in pipes:
        if bird_rect.centerx > pipe.right:
            score += 0.5
    return int(score)
def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center= (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_status):
    if game_status == "main_game":
        score_surface = game_font.render(f'Score: {int(score)}', True, (255,255, 255))
        score_rect = score_surface.get_rect(center= (288, 100) )
        screen.blit(score_surface, score_rect)
    if game_status == 'game_over':
        high_score_surface = game_font.render(f'High Score: {int(high_score) }', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 250))
        screen.blit(high_score_surface, high_score_rect)

def update_high_score(score, high_score):
    if score >= high_score:
        high_score = score
    return high_score

#                                               --------FUNCTIONS END------------
pygame.init()
screen = pygame.display.set_mode((576, 600))
clock = pygame.time.Clock()
game_font = pygame.font.SysFont("arial.ttf", 40)

common_path = "C:/Users/Veenal/Desktop/Mobile - Flappy Bird - Everything/Everything"
# Game Variables
gravity = 0.25
bird_movement = 0
score = 0
high_score = 0

bg_surface = pygame.image.load("C:/Users/Veenal/Desktop/Mobile - Flappy Bird - Everything/Everything/images/background-day.png").convert()
bg_surface = pygame.transform.scale(bg_surface, (576, 600))

end_game = pygame.image.load("C:/Users/Veenal/Desktop/Mobile - Flappy Bird - Everything/Everything/images/gameover.png")

game_active = True

floor_surface = pygame.image.load(
    "C:/Users/Veenal/Desktop/Mobile - Flappy Bird - Everything/Everything/images/base.png").convert()
floor_surface = pygame.transform.scale(floor_surface, (576, 100))
floor_x_pos = 0

bird_downflap = pygame.image.load("C:/Users/Veenal/Desktop/Mobile - Flappy Bird - Everything/Everything/images/bluebird-downflap.png").convert_alpha()
bird_midflap = pygame.image.load("C:/Users/Veenal/Desktop/Mobile - Flappy Bird - Everything/Everything/images/bluebird-midflap.png").convert_alpha()
bird_upflap = pygame.image.load("C:/Users/Veenal/Desktop/Mobile - Flappy Bird - Everything/Everything/images/bluebird-upflap.png").convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]

bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center= (100, 300))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)
#bird_surface = pygame.image.load("C:/Users/Veenal/Desktop/Mobile - Flappy Bird - Everything/Everything/images/bluebird-midflap.png").convert_alpha()
#bird_rect = bird_surface.get_rect(center=(100, 300))

pipe_surface = pygame.image.load("C:/Users/Veenal/Desktop/Mobile - Flappy Bird - Everything/Everything/images/pipe-green.png")
pipe_height = [400, 500, 300]
pipe_surface = pygame.transform.scale(pipe_surface, (50, 800))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 5
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 300)
                bird_movement = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))
    if game_active:
        # Bird_movement
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement

        score += 0.01
        score_display('main_game')

        screen.blit(rotated_bird, bird_rect)
        game_active = check_collison(pipe_list)



        # Pipes_Spawn
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
    else:
        high_score = update_high_score(score, high_score)
        score_display('game_over')
        game_over = pygame.image.load("C:/Users/Veenal/Desktop/Mobile - Flappy Bird - Everything/Everything/images/gameover.png").convert_alpha()

        screen.blit(game_over, (208, 300))
        score = 0

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
