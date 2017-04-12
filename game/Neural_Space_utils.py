import pygame
import sys
def load():
    PLAYER_PATH = 'assets/sprites/ship.png'
    BACKGROUND_PATH = 'assets/sprites/back.png'
    OBSTACLE_PATH = ('assets/sprites/rock1.png','assets/sprites/rock2.png','assets/sprites/rock3.png')

    IMAGES, HITMASKS = {}, {}

    # numbers sprites for score display
    IMAGES['numbers'] = (
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha()
    )

    # select player sprites
    IMAGES['player'] = (pygame.transform.rotate(pygame.image.load(PLAYER_PATH).convert_alpha(), -90),)

    # select obstacles sprites
    IMAGES['obs'] = (
        pygame.image.load(OBSTACLE_PATH[0]).convert_alpha(),
        pygame.image.load(OBSTACLE_PATH[1]).convert_alpha(),
        pygame.image.load(OBSTACLE_PATH[2]).convert_alpha(),
    )

    # hismask for obstacles
    HITMASKS['obs'] = (
        getHitmask(IMAGES['obs'][0]),
        getHitmask(IMAGES['obs'][1]),
	getHitmask(IMAGES['obs'][2]),
    )

    # hitmask for player
    HITMASKS['player'] = (getHitmask(IMAGES['player'][0]),)

    return IMAGES, HITMASKS

def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask
