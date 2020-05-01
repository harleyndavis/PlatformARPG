import pygame
import math

pygame.init()


DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 480
FPS = 27
GRAVITY = .1

// image loading / animation list
walkRight = [pygame.image.load("img/R1.png"), pygame.image.load("img/R2.png"), pygame.image.load("img/R3.png"), pygame.image.load("img/R4.png"), pygame.image.load("img/R5.png"), pygame.image.load("img/R6.png"), pygame.image.load("img/R7.png"), pygame.image.load("img/R8.png"), pygame.image.load("img/R9.png")]
walkLeft = [pygame.image.load("img/L1.png"), pygame.image.load("img/L2.png"), pygame.image.load("img/L3.png"), pygame.image.load("img/L4.png"), pygame.image.load("img/L5.png"), pygame.image.load("img/L6.png"), pygame.image.load("img/L7.png"), pygame.image.load("img/L8.png"), pygame.image.load("img/L9.png")]
bg = pygame.image.load("img/bg.jpg")
char = pygame.image.load("img/standing.png")

clock = pygame.time.Clock()

class Block(object):
	def __init__(self, x, y, ):
		self.x = x
		self.y = y
		self.width = 32
		self.height = 32
		self.hitbox  = (self.x, self.y, 32, 32)
		self.img = pygame.image.load("img/ground.png")
		
	def draw(self, gameDisplay):
		gameDisplay.blit(self.img, (self.x, self.y))
		pygame.draw.rect(gameDisplay, RED, self.hitbox, 2)

class player(object):
	def __init__(self, X, Y, width, height):
		self.x = X
		self.y = Y
		self.width = width
		self.height = height
		self.vel = 7
		self.velx = 0
		self.vely = 0
		self.left = False
		self.right = False
		self.walkCount = 0
		self.jumpCount = 10
		self.onGround = True
		self.airTime = 0
		self.isAlive = True
		self.jumpvel = 20
		self.hitbox = (self.x + 18, self.y + 15, 28, 49)
		
	def draw(self, win, blocks):
		if not self.onGround:
			self.airTime += 1
			self.vely += self.airTime * self.airTime * GRAVITY
		
		if self.left: 
			self.velx -= self.vel
		elif self.right:
			self.velx += self.vel
		
		sety = False
		setX = False
		nexty = DISPLAY_HEIGHT + 1
		for block in blocks:		
			if  ( self.isAlive and (self.hitbox[0] > block.x or self.hitbox[0] + self.hitbox[2] > block.x ) and ( self.hitbox[0] < block.x + block.width or self.hitbox[0] + self.hitbox[2] < block.x + block.width)):
				if ( self.hitbox[1] + self.hitbox[3] + self.vely) >= block.y and (self.hitbox[1] + self.hitbox[3]) <= block.y:
					tempy = block.y - self.height
					if tempy < nexty:
						nexty = tempy
					self.onGround = True
					sety = True
		
		if not setX:
			self.x += self.velx
		
		
		if sety:
			self.y = nexty
			self.hitbox = (self.x + 18, self.y + 15, 28, 49)
			self.airTime = 0
			self.vely = 0
		else:
			self.onGround = False
			self.y += self.vely
			self.hitbox = (self.x + 18, self.y + 15, 28, 49)
		
		if (self.y + self.hitbox[3] >= DISPLAY_HEIGHT and self.isAlive):
			self.y = DISPLAY_HEIGHT - self.height
			self.isAlive = False
		
		if self.walkCount + 1 >= 27:
			self.walkCount = 0
		
		if self.left:
			gameDisplay.blit(walkLeft[self.walkCount//3], (self.x, self.y))
			if self.onGround:
				self.walkCount += 1
		elif self.right:
			gameDisplay.blit(walkRight[self.walkCount//3], (self.x, self.y))
			if self.onGround:
				self.walkCount += 1
		elif not self.right and not self.left or not self.isAlive:
			self.walkCount = 0
			gameDisplay.blit(char, (self.x, self.y))
		
		self.velx = 0
			
		pygame.draw.rect(gameDisplay, RED, self.hitbox, 2)
			
class Projectile(object):
	def __init__(self, x, y, radius, color, mousex, mousey):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		difx = mousex - x
		dify = mousey - y
		vectormagnitude = round(math.sqrt((mousex-x)**2+(mousey-y)**2))
		self.velx = round(( mousex - x ) / vectormagnitude * 10)
		self.vely = round(( mousey - y ) / vectormagnitude * 10)
		print(str(self.velx) + " " + str(self.vely))
	
	def draw(self, gameDisplay):
		pygame.draw.circle(gameDisplay, self.color, (self.x, self.y), self.radius)

		


BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))

pygame.display.set_caption('Platform of Exile')

def redrawGameWindow(projectiles, blocks, man):

	gameDisplay.blit(bg, (0,0))
	
	for block in blocks:
		block.draw(gameDisplay)
	
	for projectile in projectiles:
		if projectile.x <  DISPLAY_WIDTH and projectile.x > 0 and projectile.y < DISPLAY_HEIGHT and projectile.y > 0:
			projectile.x += projectile.velx
			projectile.y += projectile.vely
		else:
			projectiles.pop(projectiles.index(projectile))
		projectile.draw(gameDisplay)
	
	man.draw(gameDisplay, blocks)
	pygame.display.update()

	
def main():
	#main loop
	run = True
	while run:
		man = player(300,384, 64, 64)
		projectiles = []
		blocks = []

		for i in range(10, 15):
			y = 448
			blocks.append(Block(i*32+1, y))
		
		for i in range(10, 11):
			y = 416
			blocks.append(Block(i*32+1, y))
		for i in range(14, 15):
			y = 416
			blocks.append(Block(i*32+1, y))
			
		for i in range(17, 20):
			y = 448
			blocks.append(Block(i*32+1, y))
			
		for i in range(2, 8):
			y = 352
			blocks.append(Block(i*32+1, y))
			
		for i in range(11, 12):
			y = 352
			blocks.append(Block(i*32+1, y))	

		while man.isAlive:
			clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
					man.isAlive = False
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					projectiles.append(Projectile( round(man.x + man.width // 2), round(man.y + man.width//2), 6, WHITE, *event.pos) )
								
			keys = pygame.key.get_pressed()
			
			if keys[pygame.K_a] and man.x >= man.velx:
				man.left = True
				man.right = False
			elif keys[pygame.K_d] and man.x < DISPLAY_WIDTH - man.width:
				man.left = False
				man.right = True
			else:
				man.right = False
				man.left = False
			if keys[pygame.K_SPACE] and man.onGround:
				man.onGround = False
				man.walkCount = 0
				man.vely -= man.jumpvel
			
			redrawGameWindow(projectiles, blocks, man)
			
			if not man.isAlive and run:
				man.vely = 0 - man.jumpvel
				man.airTime = 0
								
				for i in range(27):
					redrawGameWindow(projectiles, blocks, man)
					pygame.time.wait( round( 1000 / FPS) )
					

	pygame.quit()
	quit()
	
if __name__== "__main__":	
		main()
	
pygame.quit()
quit()	

