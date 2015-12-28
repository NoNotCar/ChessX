import pygame
pygame.init()
screen=pygame.display.set_mode((576,576))
import Img
import sys, os
from Piece import *
import Board
bw=(198,152,73)
bb=(122,51,0)
clock=pygame.time.Clock()
breaking=False
eRect=pygame.Rect(0,0,0,0)
edit=eRect
play=eRect
check=False
mate=False
while not breaking:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mpos=pygame.mouse.get_pos()
            if edit.collidepoint(*mpos):
                breaking="EDIT"
            elif play.collidepoint(*mpos):
                breaking="PLAY"
    screen.fill((125,125,125))
    Img.bcentre(Img.tfont,"CHESS X",screen)
    play=Img.bcentre(Img.hfont,"PLAY",screen,45)
    edit=Img.bcentre(Img.hfont,"EDIT",screen,75)
    pygame.display.flip()
    clock.tick(30)
if breaking=="PLAY":
    sranks=[]
    ranks=os.listdir("Saves")
    for r in ranks:
        raw=open(os.path.normpath("Saves/"+r))
        rank=[]
        line=raw.readline()
        for symb in line.split():
            for p in pieces:
                if p.symbol==symb:
                    rank.append(p)
                    break
        raw.close()
        sranks.append(rank)
    ranks=[r[:-4] for r in ranks]
    rankselections=[]
    for c in range(2):
        selection=0
        breaking=False
        while not breaking:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    if event.button==4:
                        selection=(selection-1)%len(sranks)
                    elif event.button==5:
                        selection=(selection+1)%len(sranks)
                    elif event.button==1:
                        breaking=True
                        rankselections.append(selection)
            screen.fill((125,125,125))
            Img.bcentrex(Img.tfont,"SELECT ARMY",screen,0)
            for n,pc in enumerate(sranks[selection]):
                screen.blit(pc.imgs[c],(n*64+32,64))
            Img.bcentrex(Img.hfont,ranks[selection],screen,130)
            mpos=pygame.mouse.get_pos()
            if 32<=mpos[0]<544 and 64<=mpos[1]<128:
                pn=(mpos[0]-32)//64
                Img.bcentrex(Img.dfont,sranks[selection][pn].desc,screen,180)
            else:
                Img.bcentrex(Img.dfont,"Scroll through the armies and click to select",screen,180)
            pygame.display.flip()
    board=Board.Board()
    select=Img.img64("Select")
    move=Img.img64("Move")
    capture=Img.img64("Capture")
    hmove=Img.img64("HoverMove")
    hcapt=Img.img64("HoverCapture")
    resign=Img.img("Resign")
    hsel=None
    selected=None
    moves=[]
    for x in range(8):
        board.add_p(Pawn,x,1,1)
        board.add_p(Pawn,x,6,0)
    for c in range(2):
        y=(1-c)*7
        for n,pc in enumerate(sranks[rankselections[c]]):
            board.add_p(pc,n,y,c)
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                mpos=pygame.mouse.get_pos()
                if pygame.Rect(448,544,128,32).collidepoint(*mpos):
                    check=True
                    mate=True
                    board.turn=1-board.turn
                else:
                    mpos=[(m-32)//64 for m in mpos]
                    for mx,my in moves:
                        if mpos==[mx,my]:
                            if board.move_p(selected,mx,my):
                                selected=None
                                board.turn=1-board.turn
                                moves=[]
                                check=board.ischeck(board.turn)
                                mate=board.is_mate(board.turn)
                                if mate:
                                    board.turn=1-board.turn
                            break
                    else:
                        if 0<=mpos[0]<8 and 0<=mpos[1]<8:
                            selp=board.p[mpos[0]][mpos[1]]
                            if selp and selp.c==board.turn:
                                selected=selp
                                moves=[[x,y] for x,y in selected.get_moves(board.p) if 0<=x<8 and 0<=y<8]
                                if selected is hsel:
                                    hsel=None
                            else:
                                selected=None
                                moves=[]
                        else:
                            selected=None
                            moves=[]
        screen.fill((84,33,0))
        for x in range(8):
            for y in range(8):
                pygame.draw.rect(screen,bb if (x+y)%2 else bw, pygame.Rect(x*64+32,y*64+32,64,64))
        if hsel:
            for mx,my in hsel.get_moves(board.p):
                if board.get_p(mx,my):
                    screen.blit(hcapt,(mx*64+32,my*64+32))
                else:
                    screen.blit(hmove,(mx*64+32,my*64+32))
        showpoints=pygame.mouse.get_pressed()[2]
        for row in board.p:
            for p in row:
                if p:
                    screen.blit(p.get_img(),(p.x*64+32,p.y*64+32))
                    if showpoints:
                        Img.brbcorner(Img.dfont,p.value,screen,p.x*64+96,p.y*64+100,(255,255,255) if p.c else (0,0,0))
        if selected:
            screen.blit(select,[s*64+32 for s in [selected.x,selected.y]])
        for mx,my in moves:
            if board.p[mx][my]:
                screen.blit(capture,(mx*64+32,my*64+32))
            else:
                screen.blit(move,(mx*64+32,my*64+32))
        mpos=pygame.mouse.get_pos()
        mpos=[(m-32)//64 for m in mpos]
        if 0<=mpos[0]<8 and 0<=mpos[1]<8:
            p=board.get_p(*mpos)
            if p:
                Img.bcentrex(Img.dfont, p.desc,screen,7,(255,255,255))
                if p is not selected and p is not hsel and list(mpos) not in moves:
                    hsel=p
            else:
                hsel=None
        Img.bcentrex(Img.hfont,"%s TO MOVE" % ("BLACK" if board.turn else "WHITE"),screen,546,(0,0,0) if board.turn else (255,255,255))
        screen.blit(resign,(448,544))
        if check and not mate:
            Img.bcentre(Img.tfont,"CHECK",screen,col=(255,0,0))
        elif check and mate:
            Img.bcentre(Img.tfont,"CHECKMATE",screen,col=(255,0,0))
        elif mate:
            Img.bcentre(Img.tfont,"STALEMATE",screen,col=(255,0,0))
        pygame.display.flip()
        if mate:
            pygame.time.wait(5000)
        else:
            clock.tick(60)
        if check and mate:
            screen.fill((0,0,0) if board.turn else (255,255,255))
            Img.bcentre(Img.tfont,"BLACK WINS" if board.turn else "WHITE WINS",screen,col=(0,0,0) if not board.turn else (255,255,255))
            pygame.display.flip()
            pygame.time.wait(1000)
            sys.exit("CHECKMATE")
        elif not check and mate:
            screen.fill((125,125,125))
            Img.bcentre(Img.tfont,"STALEMATE",screen,col=(0,0,0))
            pygame.display.flip()
            pygame.time.wait(1000)
            sys.exit("STALEMATE")
else:
    screen=pygame.display.set_mode((512,512))
    select=Img.img64("Capture")
    selpiece=None
    array=[None]*8
    array[4]=pieces.index(King)
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mpos=pygame.mouse.get_pos()
                mpos=[m//64 for m in mpos]
                mnum=mpos[0]+mpos[1]*8-8
                if 0<=mnum<len(pieces):
                    selpiece=mnum
                elif mnum<0 and selpiece is not None and mnum!=-4:
                    array[mnum+8]=selpiece
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_s:
                    savef=open("Saves/save.sav","w")
                    savef.write(" ".join([pieces[p].symbol if p is not None else "No" for p in array]))
                    savef.close()
                    sys.exit("SAVED")
        screen.fill((125,125,125))
        for x in range(8):
            pygame.draw.rect(screen,bb if x%2 else bw, pygame.Rect(x*64,0,64,64))
        for n,p in enumerate(array):
            if p is not None:
                screen.blit(pieces[p].imgs[0],(n*64,0))
        for n, p in enumerate(pieces):
            screen.blit(p.imgs[0],(n%8*64,64+n//8*64))
            Img.brbcorner(Img.dfont,p.value,screen,n%8*64+64,64+n//8*64+64,(0,0,0))
            if n is selpiece:
                screen.blit(select,(n%8*64,64+n//8*64))
        arraypoints=sum([pieces[p].value if p is not None else 0 for p in array])
        arraypoints=str(arraypoints)[:-2] if str(arraypoints)[-2:]==".0" else str(arraypoints)
        Img.bcentrex(Img.tfont,"POINTS:%s/31" % arraypoints,screen,448,(125,255,125) if float(arraypoints)<=31 else (255,0,0))
        pygame.display.flip()
        clock.tick(60)