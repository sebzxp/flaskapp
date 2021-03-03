import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,800))
    screen.blit(floor_surface,(floor_x_pos + 576,800))

def create_pipe():
    random_pipe_position = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_position))
    top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_position - 300))
    return bottom_pipe,top_pipe 

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 900:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,bird_movement * -3,1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird,new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,50))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,50))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (288,150))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.init()

game_font = pygame.font.Font("04B_19.ttf",40)

screen = pygame.display.set_mode((576,900))

clock = pygame.time.Clock()

#GAME VARIABLES
gravity = 0.10
bird_movement = 0
score = 0
high_score = 0

game_active = True

#the convert isnt nec essary but it can convert the data type to one more familiar in pygame and make it run faster 
bg_surface = pygame.image.load('assets/backgroundsea.png').convert()

#we do this to scale our image
bg_surface = pygame.transform.scale2x(bg_surface)


floor_surface = pygame.image.load('assets/base2.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/fish1.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/fish2.png').convert_alpha())                                         
bird_frames = [bird_downflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)


#bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
#bird_surface = pygame.transform.scale2x(bird_surface)
#bird_rect = bird_surface.get_rect(center = (100,512))

pipe_surface = pygame.image.load('assets/anchor.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [400,600,800]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message2.png'))
game_over_rect = game_over_surface.get_rect(center = (288,512))


death_sound = pygame.mixer.Sound('sound/Nope.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')


#game loop
while True:
    #we're doing this so we can create our game loop and exit it too
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            #need to use sys otherwise we get an error just with the while loop
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 5
            #newgame function
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,512)
                bird_movement = 0
                score = 0
                
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 1:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface,bird_rect = bird_animation()

        
            


    screen.blit(bg_surface,(0,0))

    if game_active == True:
        #bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,(bird_rect))
        game_active = check_collision(pipe_list)

        #pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        #score
        score_display('main_game')
        score += 0.01
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')
        
        
    #floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    #this limits the frame rate, no more than 120 fps
    clock.tick(120)





