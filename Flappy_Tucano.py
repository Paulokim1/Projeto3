#Blibioteca do pygame importada
import pygame
import random

#Iniciação do código
pygame.init()
GAME = True
#Especificações sobre a janela e o seu Título
WIDTH = 800
HEIGHT = 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Tucano')

#Inicia assets
TUCANO_WIDTH = 100
TUCANO_HEIGHT = 100


TUCANO = pygame.image.load('tucano2.png').convert_alpha()
TUCANO = pygame.transform.scale(TUCANO, (TUCANO_WIDTH, TUCANO_HEIGHT))

FUNDO = pygame.image.load('wallpaper.jpg').convert()
FUNDO = pygame.transform.scale(FUNDO,(WIDTH,HEIGHT))

TRONCO = pygame.image.load('tronco.jpg').convert_alpha()

BRANCO = (255,255,255)
TRONCO.set_colorkey(BRANCO)
TRONCO_GAP = 300

SPEED = 10

GRAVITY = 1 
#inicia sprites
class Tucano(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.image = TUCANO
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH/2
		self.rect.bottom = HEIGHT/2
		self.speed = SPEED*2

	def update(self):
		self.speed += GRAVITY
		self.rect.y += self.speed

	def pulo(self):
		self.speed = -SPEED*1.5

class Tronco(pygame.sprite.Sprite):
	def __init__(self,inverted,xpos,ysize):
		pygame.sprite.Sprite.__init__(self)
		
		self.image = TRONCO 
		self.rect = self.image.get_rect()
		self.rect[0] = xpos

		if inverted:
			self.image = pygame.transform.flip(self.image,False,True)
			self.rect[1] = - (self.rect[3] - ysize)
		else:
			self.rect[1] = HEIGHT - ysize

	def update(self):
		self.rect[0] -= SPEED

def random_size(xpos):
	size = random.randint(100,300)
	tronco = Tronco(False,xpos,size)
	tronco_invertido = Tronco(True,xpos,HEIGHT - size - TRONCO_GAP)
	return (tronco,tronco_invertido)

def is_off_screen(sprite):
	return sprite.rect[0] < -(sprite.rect[2])


tucano_group = pygame.sprite.Group()
tronco_group = pygame.sprite.Group()
player_tucano = Tucano()
tucano_group.add(player_tucano)


for i in range(2):
	troncos = random_size(WIDTH*i)
	tronco_group.add(troncos[0])
	tronco_group.add(troncos[1])


clock = pygame.time.Clock()
FPS = 30

#Tela inicial
PRETO = (0,0,0)
TELA_INICIAL = True
while TELA_INICIAL:
	FONTE_TITULO = pygame.font.SysFont(None, 48)
	FONTE_INSTRUCOES = pygame.font.SysFont(None, 24)
	TITULO = FONTE_TITULO.render("FLAPPY TUCANO", True, (255,255,255))
	INSTRUCOES = FONTE_INSTRUCOES.render("Aperte espaço para controlar a altura do tucano", True,(255,255,255))
	START = FONTE_INSTRUCOES.render("Aperte enter para começar o jogo", True, (255,255,255))
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				TELA_INICIAL = False
		if event.type == pygame.QUIT:
			TELA_INICIAL = False
			GAME = False


	WINDOW.blit(FUNDO,(0,0))
	WINDOW.blit(TITULO, (250, 100))
	WINDOW.blit(INSTRUCOES, (200, 220))
	WINDOW.blit(START, (250, 450))
	pygame.display.update()

#Loop principal
while GAME:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			GAME = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player_tucano.pulo()


	WINDOW.blit(FUNDO, (0,0))

	if is_off_screen(tronco_group.sprites()[0]):
		tronco_group.remove(tronco_group.sprites()[0])
		tronco_group.remove(tronco_group.sprites()[0])

		troncos = random_size(WIDTH*2)

		tronco_group.add(troncos[0])
		tronco_group.add(troncos[1])



	
	tucano_group.draw(WINDOW)
	tronco_group.draw(WINDOW)
	tucano_group.update()
	tronco_group.update()

	if pygame.sprite.groupcollide(tronco_group,tucano_group,False,False):
		break

	pygame.display.update()

#Finalização do código
pygame.quit()

