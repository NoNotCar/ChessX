__author__ = 'NoNotCar'
import pygame
import os

np = os.path.normpath
loc = os.getcwd() + "/Assets/"
pygame.mixer.init()
pygame.font.init()
pdf = pygame.font.get_default_font()
tfont=pygame.font.Font(pdf,60)
hfont=pygame.font.Font(pdf,30)
dfont=pygame.font.Font(pdf,15)
def pload(fil):
    return imgsz("Pieces/W"+fil,(64,64)),imgsz("Pieces/B"+fil,(64,64))

def imgsz(fil, sz):
    return pygame.transform.scale(pygame.image.load(np(loc + fil + ".png")), sz).convert_alpha()

def img(fil):
    return pygame.image.load(np(loc + fil + ".png")).convert_alpha()
def img64(fil):
    return imgsz(fil,(64,64))

def musplay(fil):
    pygame.mixer.music.load(np(loc + fil))
    pygame.mixer.music.play(-1)


def bcentre(font, text, surface, offset=0, col=(0, 0, 0), xoffset=0):
    render = font.render(str(text), True, col)
    textrect = render.get_rect()
    textrect.centerx = surface.get_rect().centerx + xoffset
    textrect.centery = surface.get_rect().centery + offset
    return surface.blit(render, textrect)

def bcentrex(font, text, surface, y, col=(0, 0, 0)):
    render = font.render(str(text), True, col)
    textrect = render.get_rect()
    textrect.centerx = surface.get_rect().centerx
    textrect.top = y
    return surface.blit(render, textrect)
def brbcorner(font,text,surface,x,y,col=(0,0,0)):
    render = font.render(str(text), True, col)
    textrect = render.get_rect()
    textrect.right = x
    textrect.bottom = y
    return surface.blit(render, textrect)
def sndget(fil):
    return pygame.mixer.Sound(np(loc+fil+".wav"))
