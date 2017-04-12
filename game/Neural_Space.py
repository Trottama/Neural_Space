import numpy as np
import sys
import random
import pygame
import Neural_Space_utils
import pygame.surfarray as surfarray
from pygame.locals import *
from itertools import cycle

FPS = 60
SCREENWIDTH  = 400
SCREENHEIGHT = 300


pygame.init()
FPSCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
BACKGROUND = pygame.transform.scale(pygame.image.load('assets/sprites/back.png').convert_alpha(),(SCREENWIDTH,SCREENHEIGHT))
pygame.display.set_caption('Neural Space')

IMAGES, HITMASKS = Neural_Space_utils.load()
PLAYER_WIDTH = IMAGES['player'][0].get_width()
PLAYER_HEIGHT = IMAGES['player'][0].get_height()

class GameState:
    def __init__(self):
        self.score = 0
	self.playerIndex = 0
        self.playerx = 5
        self.playery = int((SCREENHEIGHT - PLAYER_HEIGHT) / 2)
	self.background = [0,SCREENWIDTH]
	Obs1= getRandomObs()
	Obs2= getRandomObs()
 	Obs3= getRandomObs()
	self.Obs = [
		{'x': Obs1[0]['x'], 'y':Obs1[0]['y'],'type':Obs1[0]['type'],'angle':Obs1[0]['angle']},
		{'x': Obs2[0]['x']+(SCREENWIDTH*0.33), 'y':Obs2[0]['y'],'type':Obs2[0]['type'],'angle':Obs2[0]['angle']},
		{'x': Obs3[0]['x']+(SCREENWIDTH*0.66), 'y':Obs3[0]['y'],'type':Obs2[0]['type'],'angle':Obs2[0]['angle']},
	]
	
        # game Speed and Velocities
	self.gameSpeed     = -5
	self.playerUp	   = False
	self.playerDown    =False
	self.playerSpeed   = 8
	self.backSpeed = -np.ceil(self.gameSpeed/10)

    def frame_step(self, input_actions):
        pygame.event.pump()
        FPS=int(self.score/100+60)
        reward = 0.1
        terminal = False

        if sum(input_actions) != 1:
            raise ValueError('Multiple input actions!')

        # input_actions[0] == 1: do nothing
	 #input_actions[1] == 1: Up
        if input_actions[1] == 1:
	    self.playerUp=True
        # input_actions[2] == 1: Down
        if input_actions[2] == 1:
	    self.playerDown=True

	 


        # check for score
	obsPos = self.Obs[0]['x'] + IMAGES['obs'][self.Obs[0]['type']].get_width()/4 
	if obsPos <=self.playerx < obsPos+4:
	    reward = 1

	self.score +=1

        # player's movement

	if self.playerUp and self.playery <= self.playerSpeed :
		self.playery = 0
		self.playerUp=False
	if self.playerUp:
		self.playery -= self.playerSpeed
		self.playerUp=False
	if self.playerDown and self.playery>=SCREENHEIGHT-PLAYER_HEIGHT-self.playerSpeed:
		self.playery=SCREENHEIGHT-PLAYER_HEIGHT
		self.playerDown=False
	if self.playerDown:
		self.playery += self.playerSpeed
		self.playerDown=False

        # move obs to left
 	for obs in self.Obs:
            obs['x'] += self.gameSpeed
	
	self.background[0] -=self.backSpeed
	self.background[1] -=self.backSpeed
	    
	# move background to left for parallax 
	if self.background[0]==-SCREENWIDTH:
		self.background[0]=SCREENWIDTH
	if self.background[1]==-SCREENWIDTH:
		self.background[1]=SCREENWIDTH
	
            
        

        # add new obs when first pipe is about to touch left of screen
	if 0< self.Obs[0]['x'] < 6:
                newObs=getRandomObs()
		self.Obs.append(newObs[0])
	     

       # remove first obs if its out of the screen
        if self.Obs[0]['x'] < -IMAGES['obs'][self.Obs[0]['type']].get_width():
            self.Obs.pop(0)
       
	

        # check if crash here
        isCrash= checkCrash({'x': self.playerx, 'y': self.playery,'index': self.playerIndex},self.Obs)
        if isCrash:
            terminal = True
            self.__init__()
            reward = -1

        # draw sprites
        SCREEN.blit(BACKGROUND, (self.background[0],0))
	SCREEN.blit(BACKGROUND, (self.background[1],0))
	
	for obs in self.Obs:
             SCREEN.blit(pygame.transform.rotate(IMAGES['obs'][obs['type']],obs['angle']), (obs['x'],obs['y']))


        #print score
        #showScore(self.score)
        SCREEN.blit(IMAGES['player'][self.playerIndex],
                    (self.playerx, self.playery))

        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        pygame.display.update()

        FPSCLOCK.tick(FPS)

        return image_data, reward, terminal

def getRandomObs():
	type=random.randint(0,2)
	return[
		{'x':SCREENWIDTH, 'y':random.randint(0,SCREENHEIGHT-IMAGES['obs'][type].get_height()), 'type':type, 'angle':random.randint(0,359)}
        ]


def showScore(score):
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()
    Xoffset = SCREENWIDTH - totalWidth

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, 0))
        Xoffset += IMAGES['numbers'][digit].get_width()


def checkCrash(player, allObs):
	#returns true if collides with rocks
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    playerRect = pygame.Rect(player['x'], player['y'],
                      player['w'], player['h'])

    for obs in allObs:
	    obsRect = pygame.Rect(obs['x'],obs['y'],IMAGES['obs'][obs['type']].get_width(),IMAGES['obs'][obs['type']].get_height())

            # player and obs hitmasks
            pHitMask = HITMASKS['player'][0]
            oHitMask = HITMASKS['obs'][obs['type']]

            # if ship collided with rock
            oCollide = pixelCollision(playerRect, obsRect, pHitMask,oHitMask)
            if oCollide:
                 return True

    return False

def pixelCollision(rect1, rect2, hitmask1,hitmask2):
    #Checks if two objects collide and not just their rects
    rect = rect1.clip(rect2)
    

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
               return True
    return False
