__author__ = 'harry'

import pygame
from pygame.locals import *

BLACK = (0, 0, 0)
GBLACK = (50, 50, 50)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class VirPiano(object):
    """
    Main class
    """
    def __init__(self):
        self.screen = None
        self.init_window()

    def init_window(self):
        """
        Draw PyGame window
        :return:
        """
        pygame.init()
        display=(1024,768)
        self.screen = pygame.display.set_mode(display, pygame.FULLSCREEN)

    def run(self):
        Cont=True
        while Cont:
            # self.draw_piano()
            self.draw_piano()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    Cont=False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        Cont=False

    def draw_piano(self,rec=[0, 600, 1024, 64]):
        # Drawing main keys
        pygame.draw.rect(self.screen, WHITE, rec)
        xs=rec[0]
        ys=rec[1]
        totL=rec[2]
        keyL=rec[3]
        keyW=totL/52
        # Drawing subkeys
        skeyL=int(2/3*keyL)
        skeyW=int(2/3*keyW)
        psubkind=[0,1,3,4,5]
        psubkposi=[-2/3,-1/3,-2/3,-1/2,-1/3]
        for kn in range(52):
            pygame.draw.rect(self.screen, GBLACK, [int(xs),ys,int(xs+keyW)-int(xs),keyL],1)
            spind=(kn-2)%7
            if spind in psubkind and kn<51:
                skind=psubkind.index(spind)
                pygame.draw.rect(self.screen, GBLACK, [int(xs+keyW+psubkposi[skind]*skeyW),ys,skeyW,skeyL])
            xs=xs+keyW
