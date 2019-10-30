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

def cal_trapezoid(glb_rec,rec,trapezoid):
    """
    Calculate polygon from glb_rec rec and trapezoid
    :param glb_rec: global rec [left, top, width, height]
    :param rec: target rec
    :param trapezoid: trapezoid index
    :return: polygon [(points),...]
    """

    gp_lt=(glb_rec[0],glb_rec[1])
    gp_rt=(glb_rec[0]+glb_rec[2],glb_rec[1])
    gp_ld=(glb_rec[0],glb_rec[1]+glb_rec[3])
    gp_rd=(glb_rec[0]+glb_rec[2],glb_rec[1]+glb_rec[3])

    p_lt=(rec[0],rec[1])
    p_rt=(rec[0]+rec[2],rec[1])
    p_ld=(rec[0],rec[1]+rec[3])
    p_rd=(rec[0]+rec[2],rec[1]+rec[3])

    shk_up=(gp_ld[1]-p_lt[1])/glb_rec[3]*(1-trapezoid)+trapezoid
    shk_dw=(gp_ld[1]-p_ld[1])/glb_rec[3]*(1-trapezoid)+trapezoid

    res_lt=((gp_lt[0]+gp_rt[0])/2-((gp_lt[0]+gp_rt[0])/2-p_lt[0])*shk_up,p_lt[1])
    res_rt=((gp_lt[0]+gp_rt[0])/2-((gp_lt[0]+gp_rt[0])/2-p_rt[0])*shk_up,p_rt[1])
    res_ld=((gp_ld[0]+gp_rd[0])/2-((gp_ld[0]+gp_rd[0])/2-p_ld[0])*shk_dw,p_ld[1])
    res_rd=((gp_ld[0]+gp_rd[0])/2-((gp_ld[0]+gp_rd[0])/2-p_rd[0])*shk_dw,p_rd[1])

    return [res_lt,res_rt,res_rd,res_ld]

class VirPiano(object):
    """
    Main class
    """
    def __init__(self):
        self.screen = None
        self.kposidict=dict([])
        self.key_name2id=dict([])
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
        # self.screen = pygame.display.set_mode(display)

    def get_pressed_key(self, timed_note_list, beatc):
        """
        calculate pressed key number from beat counter and timed note list
        """
        if type(timed_note_list[0]) is list:
            assert len(timed_note_list)==2 # Only accepting 2 parts (left hand and right hand)
            active_keyl1=[]
            for item in timed_note_list[0]:
                if item[1]<=beatc and item[2]>beatc:
                    active_keyl1.append(self.key_name2id[item[0]])
            active_keyl2=[]
            for item in timed_note_list[1]:
                if item[1]<=beatc and item[2]>beatc:
                    active_keyl2.append(self.key_name2id[item[0]])
            return [active_keyl1,active_keyl2]
        else:
            active_keyl=[]
            for item in timed_note_list:
                if item[1]<=beatc and item[2]>beatc:
                    active_keyl.append(self.key_name2id[item[0]])
            return active_keyl


    def run(self,timed_note_list,beatpsec=2.0,colorlist=[GREEN,RED]):
        Cont=True
        glb_rec=[0, 600, 1024, 64]
        active_note_id=[None]
        sposi=0
        beatpsec=beatpsec # secpbeat
        beatc=0 # beat counter
        frate=60 # frame per second
        while Cont:
            self.screen.fill((BLACK))
            self.draw_piano(glb_rec=glb_rec,active_note_id=active_note_id,colorlist=colorlist,trapezoid=0.8)
            active_note_id=self.get_pressed_key(timed_note_list,beatc)
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
                        glb_rec[1]=glb_rec[1]-1
                    elif event.key == pygame.K_DOWN:
                        glb_rec[1]=glb_rec[1]+1
                    elif event.key == pygame.K_LEFT:
                        glb_rec[0]=glb_rec[0]-1
                    elif event.key == pygame.K_RIGHT:
                        glb_rec[0]=glb_rec[0]+1
                    elif event.key == pygame.K_a:
                        glb_rec[2]=glb_rec[2]-1
                    elif event.key == pygame.K_d:
                        glb_rec[2]=glb_rec[2]+1
                    elif event.key == pygame.K_s:
                        glb_rec[3]=glb_rec[3]-1
                    elif event.key == pygame.K_w:
                        glb_rec[3]=glb_rec[3]+1
            beatc=beatc+1/frate*beatpsec
            self.fclock.tick(frate)

    def build_piano(self,rec=None):
        xs=rec[0]
        ys=rec[1]
        totL=rec[2]
        keyL=rec[3]
        keyW=totL/52
        # Drawing subkeys
        skeyL=int(2/3*keyL)
        skeyW=int(2/3*keyW)
        # 88 keys in total
        xs=rec[0]
        psubkposi=[-2/3,-1/3,-2/3,-1/2,-1/3]
        psubkpt=-1
        for nn in range(88):
            prdnum=int((nn-3)/12)
            if nn % 12==0:
                keyName="A"+str(prdnum)
                keyrec=[int(xs),ys,int(xs+keyW)-int(xs),keyL]
                xs=xs+keyW
                self.kposidict[keyName]=keyrec
                self.kposidict[nn]=keyrec
                self.key_name2id[keyName]=nn
            elif nn % 12==1:
                psubkpt=-1
                keyName="A#"+str(prdnum)
                keyrec=[int(xs+psubkposi[psubkpt]*skeyW),ys,skeyW,skeyL]
                psubkpt=psubkpt+1
                self.kposidict[keyName]=keyrec
                self.kposidict[nn]=keyrec
                self.key_name2id[keyName]=nn
                keyName="B-"+str(prdnum)
                self.kposidict[keyName]=keyrec
                self.key_name2id[keyName]=nn
            elif nn % 12==2:
                keyName="B"+str(prdnum)
                keyrec=[int(xs),ys,int(xs+keyW)-int(xs),keyL]
                xs=xs+keyW
                self.kposidict[keyName]=keyrec
                self.kposidict[nn]=keyrec
                self.key_name2id[keyName]=nn
            elif nn % 12==3:
                keyName="C"+str(prdnum)
                keyrec=[int(xs),ys,int(xs+keyW)-int(xs),keyL]
                xs=xs+keyW
                self.kposidict[keyName]=keyrec
                self.kposidict[nn]=keyrec
                self.key_name2id[keyName]=nn
            elif nn % 12==4:
                keyName="C#"+str(prdnum)
                keyrec=[int(xs+psubkposi[psubkpt]*skeyW),ys,skeyW,skeyL]
                psubkpt=psubkpt+1
                self.kposidict[keyName]=keyrec
                self.kposidict[nn]=keyrec
                self.key_name2id[keyName]=nn
                keyName="D-"+str(prdnum)
                self.kposidict[keyName]=keyrec
                self.key_name2id[keyName]=nn
            elif nn % 12==5:
                keyName="D"+str(prdnum)
                keyrec=[int(xs),ys,int(xs+keyW)-int(xs),keyL]
                xs=xs+keyW
                self.kposidict[keyName]=keyrec
                self.kposidict[nn]=keyrec
                self.key_name2id[keyName]=nn
            elif nn % 12==6:
                keyName="D#"+str(prdnum)
                keyrec=[int(xs+psubkposi[psubkpt]*skeyW),ys,skeyW,skeyL]
                psubkpt=psubkpt+1
                self.kposidict[keyName]=keyrec
                self.kposidict[nn]=keyrec
                self.key_name2id[keyName]=nn
                keyName="E-"+str(prdnum)
                self.kposidict[keyName]=keyrec
                self.key_name2id[keyName]=nn
            elif nn % 12==7:
                keyName="E"+str(prdnum)
                keyrec=[int(xs),ys,int(xs+keyW)-int(xs),keyL]
                xs=xs+keyW
                self.kposidict[keyName]=keyrec
                self.kposidict[nn]=keyrec
                self.key_name2id[keyName]=nn
            elif nn % 12==8:
                keyName="F"+str(prdnum)
                keyrec=[int(xs),ys,int(xs+keyW)-int(xs),keyL]
                xs=xs+keyW
                self.kposidict[keyName]=keyrec
                self.kposidict[nn]=keyrec
                self.key_name2id[keyName]=nn
                keyName="E#"+str(prdnum)
                self.kposidict[keyName]=keyrec
                self.key_name2id[keyName]=nn
            elif nn % 12==9:
                keyName="F#"+str(prdnum)
                keyrec=[int(xs+psubkposi[psubkpt]*skeyW),ys,skeyW,skeyL]
                psubkpt=psubkpt+1
                self.kposidict[keyName]=keyrec
                self.kposidict[nn]=keyrec
                self.key_name2id[keyName]=nn
                keyName="G-"+str(prdnum)
                self.kposidict[keyName]=keyrec
                self.key_name2id[keyName]=nn
            elif nn % 12==10:
                keyName="G"+str(prdnum)
                keyrec=[int(xs),ys,int(xs+keyW)-int(xs),keyL]
                xs=xs+keyW
                self.kposidict[keyName]=keyrec
                self.kposidict[nn]=keyrec
                self.key_name2id[keyName]=nn
                keyName="F##"+str(prdnum)
                self.kposidict[keyName]=keyrec
                self.key_name2id[keyName]=nn
            elif nn % 12==11:
                keyName="G#"+str(prdnum)
                keyrec=[int(xs+psubkposi[psubkpt]*skeyW),ys,skeyW,skeyL]
                psubkpt=psubkpt+1
                self.kposidict[keyName]=keyrec
                self.kposidict[nn]=keyrec
                self.key_name2id[keyName]=nn
                keyName="A-"+str(prdnum)
                self.kposidict[keyName]=keyrec
                self.key_name2id[keyName]=nn


    def draw_piano(self,glb_rec=[0, 600, 1024, 64],active_note_id=[],colorlist=[],trapezoid=1.0):
        # Drawing main keys
        self.build_piano(rec=glb_rec) ##### Refactor here
        # pygame.draw.rect(self.screen, WHITE, glb_rec)
        polys=cal_trapezoid(glb_rec,glb_rec,trapezoid)
        pygame.draw.polygon(self.screen, WHITE, polys)

        pygame.draw.rect(self.screen, WHITE, [glb_rec[0],glb_rec[1]-10,glb_rec[2],2])
        # polys=cal_trapezoid(glb_rec,[glb_rec[0],glb_rec[1]-10,glb_rec[2],2],trapezoid)
        # pygame.draw.polygon(self.screen, WHITE, polys)

        self.kposidict["ll"]=glb_rec[1]-10
        for nn in range(88):
            rec=self.kposidict[nn]
            if nn%12 in [0,2,3,5,7,8,10]: # Main key
                if type(active_note_id[0]) is list:
                    if nn in active_note_id[0]:
                        # pygame.draw.rect(self.screen, RED, rec)
                        polys=cal_trapezoid(glb_rec,rec,trapezoid)
                        pygame.draw.polygon(self.screen, RED, polys)
                    elif nn in active_note_id[1]:
                        # pygame.draw.rect(self.screen, GREEN, rec)
                        polys=cal_trapezoid(glb_rec,rec,trapezoid)
                        pygame.draw.polygon(self.screen, GREEN, polys)
                else:
                    if nn in active_note_id:
                        # pygame.draw.rect(self.screen, GREEN, rec)
                        polys=cal_trapezoid(glb_rec,rec,trapezoid)
                        pygame.draw.polygon(self.screen, GREEN, polys)
                # pygame.draw.rect(self.screen, GBLACK, rec,1)
                polys=cal_trapezoid(glb_rec,rec,trapezoid)
                pygame.draw.polygon(self.screen, GBLACK, polys,1)

        for nn in range(88):
            rec=self.kposidict[nn]
            if nn%12 not in [0,2,3,5,7,8,10]: # Small key
                # pygame.draw.rect(self.screen, GBLACK, rec)
                polys=cal_trapezoid(glb_rec,rec,trapezoid)
                pygame.draw.polygon(self.screen, GBLACK, polys)
                if type(active_note_id[0]) is list:
                    if nn in active_note_id[0]:
                        # pygame.draw.rect(self.screen, RED, rec)
                        polys=cal_trapezoid(glb_rec,rec,trapezoid)
                        pygame.draw.polygon(self.screen, RED, polys)
                        # pygame.draw.rect(self.screen, GBLACK, rec,1)
                        polys=cal_trapezoid(glb_rec,rec,trapezoid)
                        pygame.draw.polygon(self.screen, GBLACK, polys)
                    elif nn in active_note_id[1]:
                        # pygame.draw.rect(self.screen, GREEN, rec)
                        polys=cal_trapezoid(glb_rec,rec,trapezoid)
                        pygame.draw.polygon(self.screen, GREEN, polys)
                        # pygame.draw.rect(self.screen, GBLACK, rec,1)
                        polys=cal_trapezoid(glb_rec,rec,trapezoid)
                        pygame.draw.polygon(self.screen, GBLACK, polys)

                elif nn in active_note_id:
                    # pygame.draw.rect(self.screen, GREEN, rec)
                    polys=cal_trapezoid(glb_rec,rec,trapezoid)
                    pygame.draw.polygon(self.screen, GREEN, polys)
                    # pygame.draw.rect(self.screen, GBLACK, rec,1)
                    polys=cal_trapezoid(glb_rec,rec,trapezoid)
                    pygame.draw.polygon(self.screen, GBLACK, polys,1)

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

    def get_timed_notes(self,ms, poffset=0):
        """
        Get timed notes list from a measure [note,start_t,end_t]
        """
        notel=[]
        offset=ms.offset
        cpointer=0
        for item in ms:
            if isinstance(item,mu.stream.Voice):
                notesl1=self.get_timed_notes(item,poffset=offset)
                notel=notel+notesl1
            elif isinstance(item,mu.note.Note):
                notel.append((item.nameWithOctave,offset+poffset+cpointer,offset+poffset+cpointer+item.quarterLength))
                cpointer=cpointer+item.quarterLength
            elif isinstance(item,mu.chord.Chord):
                for iitem in item:
                    notel.append((iitem.nameWithOctave,offset+poffset+cpointer,offset+poffset+cpointer+iitem.quarterLength))
                cpointer=cpointer+item.quarterLength
        return notel

if __name__=='__main__':
    mp=MusicParser()
    # mp.play()
    msl=mp.get_measures(part=0)
    tntl=[]
    for ms in msl:
        ntl=mp.get_timed_notes(ms)
        tntl=tntl+ntl

    ms2=mp.get_measures(part=1)
    tnt2=[]
    for ms in ms2:
        ntl=mp.get_timed_notes(ms)
        tnt2=tnt2+ntl
    # mid=1
    # print(msl[mid],len(msl[mid]))
    # for item in msl[mid]:
    #     print(item)
    # mp.show()

    vp=VirPiano()
    vp.run([tntl,tnt2],beatpsec=2.0)


