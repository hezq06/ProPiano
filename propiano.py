__author__ = 'harry'

import pygame
from pygame.locals import *

import music21 as mu
mu.environment.set("musicxmlPath", "C:\\Program Files (x86)\\MuseScore 2\\bin\\MuseScore.exe")
mu.environment.set('musescoreDirectPNGPath', "C:\\Program Files (x86)\\MuseScore 2\\bin\\MuseScore.exe")

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
        self.kposidict=dict([])
        self.fclock=pygame.time.Clock()
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
        rec=[0, 600, 1024, 64]
        sposi=0
        while Cont:
            self.screen.fill((BLACK))
            self.draw_piano(rec=rec)
            if sposi-100<self.kposidict["ll"]:
                self.draw_note(20,sposi,100)
            sposi=sposi+1
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    Cont=False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        Cont=False
                    elif event.key == pygame.K_UP:
                        rec[1]=rec[1]-1
                    elif event.key == pygame.K_DOWN:
                        rec[1]=rec[1]+1
                    elif event.key == pygame.K_LEFT:
                        rec[0]=rec[0]-1
                    elif event.key == pygame.K_RIGHT:
                        rec[0]=rec[0]+1
                    elif event.key == pygame.K_a:
                        rec[2]=rec[2]-1
                    elif event.key == pygame.K_d:
                        rec[2]=rec[2]+1
                    elif event.key == pygame.K_s:
                        rec[3]=rec[3]-1
                    elif event.key == pygame.K_w:
                        rec[3]=rec[3]+1
            self.fclock.tick(120)


    def draw_piano(self,rec=[0, 600, 1024, 64],gkey=[20]):
        # Drawing main keys
        pygame.draw.rect(self.screen, WHITE, rec)
        pygame.draw.rect(self.screen, WHITE, [rec[0],rec[1]-10,rec[2],2])
        self.kposidict["ll"]=rec[1]-10
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
            if kn in gkey:
                pygame.draw.rect(self.screen, GREEN, [int(xs),ys,int(xs+keyW)-int(xs),keyL])
            else:
                pygame.draw.rect(self.screen, GBLACK, [int(xs),ys,int(xs+keyW)-int(xs),keyL],1)
            self.kposidict[kn]=[int(xs),ys,int(xs+keyW)-int(xs),keyL]
            xs=xs+keyW
        xs=rec[0]
        for kn in range(52):
            spind=(kn-2)%7
            if spind in psubkind and kn<51:
                skind=psubkind.index(spind)
                pygame.draw.rect(self.screen, GBLACK, [int(xs+keyW+psubkposi[skind]*skeyW),ys,skeyW,skeyL])
            xs=xs+keyW

    def draw_note(self,note,start,length):
        # Draw a bar of note
        kposi=self.kposidict[note]
        ll=self.kposidict["ll"]
        if start<ll:
            pygame.draw.rect(self.screen, GREEN, [kposi[0],start-length,kposi[2],length])
        else:
            pygame.draw.rect(self.screen, GREEN, [kposi[0],start-length,kposi[2],ll-(start-length)])

class MusicParser(object):
    """
    Main class for music parsing
    """
    def __init__(self,file="music\\Final_Fantasy_Main_Theme.musicxml",format='musicxml'):
        """
        Initiation
        """
        # file="music\\Wings_of_Piano.mxl"
        file="music\\Deemo_Anima-Xi.mxl"
        # file="music\\Necrofantasia_Yukaris_Theme_Touhou.mxl"
        self.muf=mu.converter.parse(file,format=format)
        self.mups=None

    def show(self):
        self.muf.show()

    def play(self):
        # ff=mu.converter.parse("music\\Final_Fantasy_Main_Theme.musicxml",format='musicxml')
        self.muf.show("midi")

    def get_parts(self):
        mups = self.muf.parts.stream()
        print("Number of parts: ",len(mups))
        self.mups=mups

    def get_instruments(self):
        if self.mups is None:
            self.get_parts()
        for pt in self.mups:
            if isinstance(pt[0],mu.instrument.Instrument):
                print(pt[0])
                # print(pt[0].instrumentName)

    def get_measures(self,part=0):
        if self.mups is None:
            self.get_parts()
        msl=[]
        for ms in self.mups[part]:
            if isinstance(ms,mu.stream.Measure):
                # print(ms,ms.barDuration)
                msl.append(ms)
        return msl

    def get_timed_nots(self,ms):
        """
        Get timed notes list from a measure [note,start_t,end_t]
        """

if __name__=='__main__':
    mp=MusicParser()
    # mp.play()
    msl=mp.get_measures(part=0)
    mid=0
    print(msl[mid],len(msl[mid]))
    for item in msl[mid]:
        print(item)
    mp.show()

