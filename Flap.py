import pygame,sys,random

#Floor run
def draw_floor():
	screen.blit(floor,(floor_x_pos,650))
	screen.blit(floor,(floor_x_pos+432,650))
#Create pipe
def create_pipe():
	random_pipes_pos = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop = (500,random_pipes_pos))
	top_pipe = pipe_surface.get_rect(midtop = (500,random_pipes_pos-650))
	return bottom_pipe,top_pipe
#Pipe movement
def move_pipe(pipes):
	for pipe in pipes:
		pipe.centerx -=3
	return pipes
#Draw pipe
def draw_pipe(pipes):
	for pipe in pipes:
		if pipe.bottom >= 600 :
			screen.blit(pipe_surface,pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface,False,True)
			screen.blit(flip_pipe,pipe)
#Collision
def check_collision(pipes):
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			hit_sound.play()
			return False
	if bird_rect.bottom >=650:
		die_sound.play()
		return False
	return True
def rotate_bird(bird1):
	new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1)
	return new_bird
def bird_animation():
	new_bird = bird_list[bird_index]
	new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery)) 
	return new_bird,new_bird_rect
def score_display(game_state):
	if game_state == 'main_game':
		score_surface = game_font.render(str(int(score)),True,(255,255,255))
		score_rect = score_surface.get_rect(center = (216,100))
		screen.blit(score_surface,score_rect)
	if game_state == 'game_over':
		score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
		score_rect = score_surface.get_rect(center = (216,100))
		screen.blit(score_surface,score_rect)

		high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
		high_score_rect = score_surface.get_rect(center = (165

			,610))
		screen.blit(high_score_surface,high_score_rect)
def update_score(score,high_score):
	if score > high_score:
		high_score = score
	return high_score
pygame.mixer.pre_init(frequency = 44100,size = -16,channels = 2,buffer = 512)
	
pygame.init()

#Screen/run
run = True
screen = pygame.display.set_mode((432,768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('Font/04B_19.TTF',40)

#Gravity 
gravity = 0.15
bird_movement = 0
game_active = True
score = 0
high_score = 0

#Background
bgsc = pygame.image.load('Assests/background-night.png').convert()
bg = pygame.transform.scale(bgsc, (int(bgsc.get_width() * 1.5), int(bgsc.get_height() * 1.5)))
#Floor
floorsc = pygame.image.load('Assests/floor.png').convert()
floor = pygame.transform.scale2x(floorsc)
floor_x_pos = 0
#Bird
bird_down = pygame.transform.scale2x(pygame.image.load('Assests/yellowbird-downflap.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('Assests/yellowbird-midflap.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('Assests/yellowbird-upflap.png').convert_alpha())
bird_list = [bird_down,bird_mid,bird_up]
bird_index = 0
bird = bird_list[bird_index]
# birdsc = pygame.image.load('Assests/yellowbird-midflap.png').convert()
# bird = pygame.transform.scale2x(birdsc)
bird_rect = bird.get_rect(center = (100,384))
#Bird timer
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap,200)
#Pipe
pipe_surface = pygame.image.load('Assests/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
#Timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe,1200)
pipe_height = [200,300,400]
#End Surface
game_over_surface = pygame.transform.scale2x(pygame.image.load('Assests/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (216,350))
#Sound
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
point_sound = pygame.mixer.Sound('sound/sfx_point.wav')
swooshing_sound = pygame.mixer.Sound('sound/sfx_swooshing.wav')
die_sound = pygame.mixer.Sound('sound/sfx_die.wav')
score_sound_coutdown = 100

while run:
	screen.blit(bg,(0,0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		#Bird move
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active:
				flap_sound.play()
				bird_movement = 0
				bird_movement -=5
			if event.key == pygame.K_SPACE and game_active == False:
				swooshing_sound.play()
				game_active = True
				pipe_list.clear()
				bird_rect.center = (100,384)
				bird_movement = 0
				score = 0
		#Pipe create
		if event.type == spawnpipe:
			pipe_list.extend(create_pipe())
		if event.type == birdflap:
			if bird_index < 2:
				bird_index +=1
			else:
				bird_index = 0
			bird, bird_rect = bird_animation()
	#Game True
	if game_active:
		#Draw
		rotated_bird = rotate_bird(bird)
		screen.blit(rotated_bird,bird_rect)
		#Gravit bird
		bird_movement +=gravity
		bird_rect.centery += bird_movement
		game_active = check_collision(pipe_list)
		#Pipe
		pipe_list = move_pipe(pipe_list)	
		draw_pipe(pipe_list)
		score += 0.01
		score_display('main_game')
		score_sound_coutdown -=1
		if score_sound_coutdown <=0:
			point_sound.play()
			score_sound_coutdown = 100
		#NO COPYRIGHT
		made_font = pygame.font.Font('Font/Minecraft.ttf',20)
		made = made_font.render("Made by stephen",False,(255,255,255))
		screen.blit(made,(250,630))
	else:
		screen.blit(game_over_surface,game_over_rect)
		high_score = update_score(score,high_score)
		score_display('game_over')

	floor_x_pos -=1
	draw_floor()
	if floor_x_pos <= -432:
		floor_x_pos = 0

	pygame.display.update()
	clock.tick(120)