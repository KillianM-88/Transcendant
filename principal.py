#import des modules pygame permettant l'interface graphique
import pygame
import time
import random
import math

from pygame.locals import *


#initialisation de pygame
pygame.init()
pygame.mixer.init() #et du module musical

#demarrage
"""
faut trouver une musique de demarrage et un lancement mais cette fonction initialisera le jeu en gros
ca serait bien de la mettre juset apres la creation de la fenetre, comme ca python charge les images pendant
que l'animation se lance
"""
#################################################################################################################



def animation(ani):
    global crash_sound
    debut=time.time()
    if ani=="demarrage":
        while time.time()-debut<1:
            fenetre.blit(launch,(0,0))
            pygame.display.update()
    elif ani=="ecran_noir":
        while time.time()-debut<1.5:
            fenetre.fill((0,0,0))
            pygame.display.update()
    elif ani=="decollage":
        for img in anim_deco:
            fenetre.blit(img,(0,0))
            pygame.display.update()
            pygame.time.wait(180)
    elif ani=="vol":
        for img in anim_vol :
            fenetre.blit(img, (0,0))
            pygame.display.update()
            pygame.time.wait(140)
        crash_sound.play()
    elif ani=="possess":
        if sexe=="femme":
            p=anim_possess[0]
        elif sexe=="homme":
            p=anim_possess[1]
        else:
            p=anim_possess[2]
        for img in p:
            fenetre.blit(img, (0,0))
            pygame.display.update()
            pygame.time.wait(140)
        fenetre.fill((0,0,0))
        pygame.display.update()
        pygame.time.wait(800)
    elif ani=="vs_s1":
        fenetre.fill((0,0,0))
        pygame.display.update()
        pygame.time.wait(700)
        if sexe=="femme":
            p=anim_vs_s1[0]
        else:
            p=anim_vs_s1[1]
        for img in p:
            fenetre.blit(img, (0,0))
            pygame.display.update()
            pygame.time.wait(320)
        pygame.time.wait(1500)
        fenetre.fill((0,0,0))
        pygame.display.update()
        pygame.time.wait(2500)
    elif ani=="win_vs_s1":
        fenetre.fill((0,0,0))
        pygame.display.update()
        pygame.time.wait(700)
        if sexe=="femme":
            p=anim_win_s1[0]
        else:
            p=anim_win_s1[1]
        for img in p:
            fenetre.blit(img, (0,0))
            pygame.display.update()
            pygame.time.wait(2500)
        fenetre.fill((0,0,0))
        pygame.display.update()
        pygame.time.wait(1500)
    elif ani=="fin":
        for img in fin :
            fenetre.blit(img, (0,0))
            pygame.display.update()
            pygame.time.wait(10000)
    elif ani=="perdu":
        fenetre.blit(perdu, (0,0))
        pygame.display.update()
        pygame.time.wait(6000)


#################################################################################################################



class Menu :
    def __init__ (self,fond,boutons,icones):
        """
         fond c'est l'image de fond du menu
         boutons ca sera une liste avec l'image du boutons, les coordonnees ou il sera et les coordonnees de
        l'appui
         icones sera aussi  une liste mais c'est genre des logos etc qu'on appuie pas
        """
        self.fond = None #image
        self.boutons = []
        self.icone = []
        self.indice_animation = 0



#################################################################################################################

pv={"femme":1000,"homme":1000,"soldat":950,"parrain":1200}

degats={"up":      {"femme":40,"homme":40,"soldat":35,"parrain":45},
        "straight":{"femme":30,"homme":35,"soldat":35,"parrain":45},
        "down":    {"femme":40,"homme":35,"soldat":35,"parrain":45},
        "air":     {"femme":30,"homme":20,"soldat":40,"parrain":50}}

mult={"up":      {"femme":(0.9,1.6),"homme":(1.4,1.4),"soldat":(1.1,1.3),"parrain":(1,1)},
      "straight":{"femme":(1.6,0.7),"homme":(1.8,0.3),"soldat":(1.7,0.1),"parrain":(1,1)},
      "down":    {"femme":(1,1.5),"homme":(0.3,0.3),"soldat":(1.2,0.6),"parrain":(1,1)},
      "air":     {"femme":(1.5,0.3),"homme":(0.4,1.5),"soldat":(1,1),"parrain":(1,1)}}

cost={"up":      {"femme":3.2,"homme":3.3,"soldat":3,"parrain":3.1},
      "straight":{"femme":2.4,"homme":2.4,"soldat":2.9,"parrain":3.1},
      "down":    {"femme":3.6,"homme":2.8,"soldat":3.1,"parrain":3.1},
      "air":     {"femme":2.8,"homme":4,"soldat":3,"parrain":3.1}}

vitesses={"depl":    {"femme":1.1,"homme":1.1,"soldat":0.97,"parrain":0.99},
          "stand":   {"femme":0.1,"homme":0.12,"soldat":0.12,"parrain":0.11},
          "i_depl":  {"femme":0.09,"homme":0.085,"soldat":0.1,"parrain":0.1},
          "jump":    {"femme":0.08,"homme":0.09,"soldat":0.07,"parrain":0.08},
          "straight":{"femme":0.1,"homme":0.13,"soldat":0.13,"parrain":0.12},
          "up":      {"femme":0.11,"homme":0.15,"soldat":0.14,"parrain":0.12},
          "down":    {"femme":0.12,"homme":0.1,"soldat":0.12,"parrain":0.12},
          "air":     {"femme":0.08,"homme":0.12,"soldat":0.07,"parrain":0.08},
          "touched": {"femme":0.07,"homme":0.07,"soldat":0.07,"parrain":0.07}}

rectangles={"hitbox":{"femme":((180,160),180,95,400),"homme":((180,160),180,95,400),"soldat":((160,160),190,110,400),"parrain":((180,160),180,95,400)},

           "straight":{"femme":((210,0),550,250,60),"homme":((210,20),550,250,60),"soldat":((210,20),550,250,60),"parrain":((210,20),550,250,60)},

           "air":{"femme":((210,10),600,200,120),"homme":((100,0),150,300,700),"soldat":((210,10),700,200,120),"parrain":((100,0),150,300,700)},

           "up":{"femme":((300,10),400,140,600),"homme":((280,30),400,140,100),"soldat":((280,30),400,140,100),"parrain":((280,30),400,140,100)},

           "down":{"femme":((210,10),600,200,120),"homme":((210,30),600,200,120),"soldat":((210,30),500,220,90),"parrain":((210,30),500,200,120)},

           "sneak":{"femme":((180,160),400,95,200),"homme":((180,160),400,95,200),"soldat":((160,160),400,110,200),"parrain":((180,160),400,95,200)},

           "jump":{"femme":((180,160),180,95,150),"homme":((180,160),180,95,150),"soldat":((160,160),190,110,150),"parrain":((180,160),180,95,150)}}

class Personnage_vs :
    """classe qui determine le personnage choisi par le joueur, la fait se deplacer, attaquer, gere les collision et autres actions du personnage"""

    def __init__(self, nom, pv, degats, vitesses, mult, cost, x,y, rect):
        """fonction d'initialisation de la classe qui defini pv, degats, hitbox etc... et qui charge les images correspondant au personage choisi
        en fonction du nom"""

        self.x=x
        self.y=500
        self.ground=y
        self.sens=None

        self.d=False
        self.g=False
        self.sneak=False

        self.sprite=None
        self.indice=0

        self.v_saut = 0
        self.is_blocking=False

        self.coup=None
        self.rect_coup = None
        self.rect=pygame.Rect(self.x+35,self.y+55,60,108)

        self.energy=20
        self.cost={"straight":cost["straight"][nom],"down":cost["down"][nom],"up":cost["up"][nom],"air":cost["air"][nom]}

        self.jump_able=True
        self.hit_able=True
        self.air_hit_able=False
        self.move_able=True
        self.ult_able=False
        self.hit=True
        self.blocking=False
        self.maj=False

        self.touched=False
        self.v_touched_x=0
        self.mutipl_dist={"straight":mult["straight"][nom],"down":mult["down"][nom],"up":mult["up"][nom],"air":mult["air"][nom]}

        self.hp=pv[nom]
        self.pv_totaux=pv[nom]

        self.degats={"straight":degats["straight"][nom],"down":degats["down"][nom],"up":degats["up"][nom],"air":degats["air"][nom]}

        self.indices={"depl":vitesses["depl"][nom],"stand":vitesses["stand"][nom],"i_depl":vitesses["i_depl"][nom],"down":vitesses["down"][nom],"straight":vitesses["straight"][nom],"up":vitesses["up"][nom],"air":vitesses["air"][nom],"jump":vitesses["jump"][nom],"touched":vitesses["touched"][nom]}


        #images du personnage
        self.rectangle={"hitbox":rect["hitbox"][nom],
                       "down":rect["down"][nom],
                       "air":rect["air"][nom],
                       "straight":rect["straight"][nom],
                       "up":rect["up"][nom],
                       "sneak":rect["sneak"][nom],
                       "jump":rect["jump"][nom]}

        nom=nom+"_kombat"
        self.standing_n=[]
        i=1
        while i!=0:
            try:
                img=pygame.image.load("packs/personnages/"+nom+"/standing_"+str(i)+".png").convert_alpha()
                img=pygame.transform.scale(img,(164*2,304*2))
                self.standing_n.append(img)
                i+=1
            except:
                i=0

        self.standing_i =[pygame.transform.flip(image,True,False) for image in self.standing_n]
        self.standing=[self.standing_n,self.standing_i]

        self.walk_n=[]
        i=1
        while i!=0:
            try:
                img=pygame.image.load("packs/personnages/"+nom+"/walk_"+str(i)+".png").convert_alpha()
                img=pygame.transform.scale(img,(164*2,304*2))
                self.walk_n.append(img)
                i+=1
            except:
                i=0

        self.walk_i =[pygame.transform.flip(image,True,False) for image in self.walk_n]
        self.walk=[self.walk_n,self.walk_i]
        

        self.block_n=[]
        i=1
        while i!=0:
            try:
                img=pygame.image.load("packs/personnages/"+nom+"/block_"+str(i)+".png").convert_alpha()
                img=pygame.transform.scale(img,(164*2,304*2))
                self.block_n.append(img)
                i+=1
            except:
                i=0

        self.block_i =[pygame.transform.flip(image,True,False) for image in self.block_n]
        self.block=[self.block_n,self.block_i]

        self.jump_n=[]
        i=1
        while i!=0:
            try:
                img=pygame.image.load("packs/personnages/"+nom+"/jump_"+str(i)+".png").convert_alpha()
                img=pygame.transform.scale(img,(164*2,304*2))
                self.jump_n.append(img)
                i+=1
            except:
                i=0

        self.jump_i =[pygame.transform.flip(image,True,False) for image in self.jump_n]
        self.jump=[self.jump_n,self.jump_i]

        self.straight_n=[]
        i=1
        while i!=0:
            try:
                img=pygame.image.load("packs/personnages/"+nom+"/straight_"+str(i)+".png").convert_alpha()
                img=pygame.transform.scale(img,(164*2,304*2))
                self.straight_n.append(img)
                i+=1
            except:
                i=0

        self.straight_i =[pygame.transform.flip(image,True,False) for image in self.straight_n]
        self.straight=[self.straight_n,self.straight_i]

        self.down_n=[]
        i=1
        while i!=0:
            try:
                img=pygame.image.load("packs/personnages/"+nom+"/down_"+str(i)+".png").convert_alpha()
                img=pygame.transform.scale(img,(164*2,304*2))
                self.down_n.append(img)
                i+=1
            except:
                i=0

        self.down_i =[pygame.transform.flip(image,True,False) for image in self.down_n]
        self.down=[self.down_n,self.down_i]

        self.up_n=[]
        i=1
        while i!=0:
            try:
                img=pygame.image.load("packs/personnages/"+nom+"/up_"+str(i)+".png").convert_alpha()
                img=pygame.transform.scale(img,(164*2,304*2))
                self.up_n.append(img)
                i+=1
            except:
                i=0

        self.up_i =[pygame.transform.flip(image,True,False) for image in self.up_n]
        self.up=[self.up_n,self.up_i]

        self.spc1_n=[]
        i=1
        while i!=0:
            try:
                img=pygame.image.load("packs/personnages/"+nom+"/spc1_"+str(i)+".png").convert_alpha()
                img=pygame.transform.scale(img,(164*2,304*2))
                self.spc1_n.append(img)
                i+=1
            except:
                i=0

        self.spc1_i =[pygame.transform.flip(image,True,False) for image in self.spc1_n]
        self.spc1=[self.spc1_n,self.spc1_i]

        self.touch_n=[]
        i=1
        while i!=0:
            try:
                img=pygame.image.load("packs/personnages/"+nom+"/touch_"+str(i)+".png").convert_alpha()
                img=pygame.transform.scale(img,(164*2,304*2))
                self.touch_n.append(img)
                i+=1
            except:
                i=0

        self.touch_i =[pygame.transform.flip(image,True,False) for image in self.touch_n]
        self.touch=[self.touch_n,self.touch_i]

        self.ko_n=[]
        i=1
        while i!=0:
            try:
                img=pygame.image.load("packs/personnages/"+nom+"/ko_"+str(i)+".png").convert_alpha()
                img=pygame.transform.scale(img,(164*2,304*2))
                self.ko_n.append(img)
                i+=1
            except:
                i=0

        self.ko_i =[pygame.transform.flip(image,True,False) for image in self.ko_n]
        self.ko=[self.ko_n,self.ko_i]

        self.crouch_n=[]
        i=1
        while i!=0:
            try:
                img=pygame.image.load("packs/personnages/"+nom+"/crouch_"+str(i)+".png").convert_alpha()
                img=pygame.transform.scale(img,(164*2,304*2))
                self.crouch_n.append(img)
                i+=1
            except:
                i=0

        self.crouch_i =[pygame.transform.flip(image,True,False) for image in self.crouch_n]
        self.crouch=[self.crouch_n,self.crouch_i]

        self.jump_hit_n=[]
        i=1
        while i!=0:
            try:
                img=pygame.image.load("packs/personnages/"+nom+"/jump_hit_"+str(i)+".png").convert_alpha()
                img=pygame.transform.scale(img,(164*2,304*2))
                self.jump_hit_n.append(img)
                i+=1
            except:
                i=0

        self.jump_hit_i =[pygame.transform.flip(image,True,False) for image in self.jump_hit_n]
        self.jump_hit=[self.jump_hit_n,self.jump_hit_i]        
        self.back_n=[]
        i=1
        while i!=0:
            try:
                img=pygame.image.load("packs/personnages/"+nom+"/back_"+str(i)+".png").convert_alpha()
                img=pygame.transform.scale(img,(164*2,304*2))
                self.back_n.append(img)
                i+=1
            except:
                i=0
                
        if self.back_n==[]:
            for i in range (len(self.walk_n)):
                self.back_n.append(self.walk_n[-(i+1)])
            

        self.back_i =[pygame.transform.flip(image,True,False) for image in self.back_n]
        self.back=[self.back_n,self.back_i]



    def touches_J1(self,type,key):
        """fonction prenant en parametre l'action realise, la touche pressée et l'id du personnage pour en ressortir l'action du joueur
        comme des attaques, saut, deplacements etc...
        POUR LE JOUEUR 1"""

        if type==KEYDOWN:

            if key==K_d:
                self.d=True
                self.g=False
            if key==K_q:
                self.g=True
                self.d=False
            if key==K_s:
                self.sneak=True
            if key==K_z and self.jump_able==True:
                self.v_saut=15
                self.indice=0
            if key==K_v and self.hit_able==True and self.energy>=self.cost["down"]:
                self.coup="down"
                self.rect_coup=pygame.Rect(self.x+self.rectangle["down"][0][self.sens],
                                               self.y+self.rectangle["down"][1]+self.ground-350,
                                               self.rectangle["down"][2],
                                               self.rectangle["down"][3])
                self.maj=True
            if key==K_v and self.air_hit_able==True and self.energy>=self.cost["air"]:
                self.coup="air"
                self.rect_coup=pygame.Rect(self.x+self.rectangle["air"][0][self.sens],
                                               self.y+self.rectangle["air"][1]+self.ground-350,
                                               self.rectangle["air"][2],
                                               self.rectangle["air"][3])
                self.maj=True
            if key==K_c and self.hit_able==True and self.energy>=self.cost["straight"]:
                self.coup="straight"
                self.rect_coup=pygame.Rect(self.x+self.rectangle["straight"][0][self.sens],
                                               self.y+self.rectangle["straight"][1]+self.ground-350,
                                               self.rectangle["straight"][2],
                                               self.rectangle["straight"][3])
                self.maj=True
            if key==K_b and self.hit_able==True and self.energy>=self.cost["up"]:
                self.coup="up"
                self.rect_coup=pygame.Rect(self.x+self.rectangle["up"][0][self.sens],
                                               self.y+self.rectangle["up"][1]+self.ground-350,
                                               self.rectangle["up"][2],
                                               self.rectangle["up"][3])
                self.maj=True

            if self.maj==True:
                self.indice=0
                self.hit=False
                self.energy-=self.cost[self.coup]
                if self.sneak==True:
                    self.sneak="wait"
                self.maj=False

        if type==KEYUP:

            if key==K_d:
                self.d=False
            if key==K_q:
                self.g=False
            if key==K_s:
                self.sneak=False

    def touches_J2(self,type,key):
        """fonction prenant en parametre l'action realise, la touche pressée et l'id du personnage pour en ressortir l'action du joueur
        comme des attaques, saut, deplacements etc...
        POUR LE JOUEUR 2"""

        if type==KEYDOWN:

            if key==K_RIGHT:
                self.d=True
                self.g=False
            if key==K_LEFT:
                self.g=True
                self.d=False
            if key==K_DOWN:
                self.sneak=True
            if key==K_UP and self.jump_able==True:
                self.v_saut=15
                self.indice=0
            if key==K_l and self.hit_able==True and self.energy>=self.cost["down"]:
                self.coup="down"
                self.rect_coup=pygame.Rect(self.x+self.rectangle["down"][0][self.sens],
                                               self.y+self.rectangle["down"][1]+self.ground-350,
                                               self.rectangle["down"][2],
                                               self.rectangle["down"][3])

                self.maj=True
            if key==K_l and self.air_hit_able==True and self.energy>=self.cost["air"]:
                self.coup="air"
                self.rect_coup=pygame.Rect(self.x+self.rectangle["air"][0][self.sens],
                                               self.y+self.rectangle["air"][1]+self.ground-350,
                                               self.rectangle["air"][2],
                                               self.rectangle["air"][3])
                self.maj=True
            if key==K_k and self.hit_able==True and self.energy>=self.cost["straight"]:
                self.coup="straight"
                self.rect_coup=pygame.Rect(self.x+self.rectangle["straight"][0][self.sens],
                                               self.y+self.rectangle["straight"][1]+self.ground-350,
                                               self.rectangle["straight"][2],
                                               self.rectangle["straight"][3])
                self.maj=True
            if key==K_m and self.hit_able==True and self.energy>=self.cost["up"]:
                self.coup="up"
                self.rect_coup=pygame.Rect(self.x+self.rectangle["up"][0][self.sens],
                                               self.y+self.rectangle["up"][1]+self.ground-350,
                                               self.rectangle["up"][2],
                                               self.rectangle["up"][3])
                self.maj=True

            if self.maj==True:
                self.indice=0
                self.hit=False
                self.energy-=self.cost[self.coup]
                if self.sneak==True:
                    self.sneak="wait"
                self.maj=False

        if type==KEYUP:

            if key==K_RIGHT:
                self.d=False
            if key==K_LEFT:
                self.g=False
            if key==K_up:
                self.sneak=False


    def deplacement(self,opp):
        """fonction prenant en parametre le joueur et son adversaire
        gere la gravite
        gere un deplacement renvoye par les fonctions de touche
        gere la garde
        gere le changement d'hitbox en fonction de l'action et de l'emplacement"""

        self.y = int(self.y-self.v_saut)   #saut
        self.v_saut-=0.5
        if self.y >= self.ground :        #gravite
            self.y = self.ground

        cote=0
        if opp.x-self.x==0:
            cote=1                          #choix d'un cote pour eviter les bugs quand les joueurs sont tous deux en x=0 (plusieurs fois dans le code)
            if max(self.x,opp.x)>600:
                cote=-1
        self.x = int(self.x-self.v_touched_x*1.2*((opp.x-self.x+cote)/abs(opp.x-self.x+cote))) #recul si attaqué
        if self.collision(opp)==False:
            self.x = int(self.x+self.v_touched_x*1.2*((opp.x-self.x+cote)/abs(opp.x-self.x+cote))) #sauf si collision
        self.v_touched_x-=0.725
        if self.v_touched_x<0:
            self.v_touched_x=0

        if self.touched==True and self.y==self.ground: #pu de recul quand on atterri
            self.touched=False

        if self.move_able==True:

            if self.d==True :
                self.x+=(4-self.sens*1.5)*self.indices["depl"] #deplacement en fonction de si on recul ou avance, et de la vitesse du perso
                if self.y <self.ground:
                    self.x+=2                                  #plus rapide en sautant
                if self.collision(opp)==False:
                    self.x-=(4-self.sens*1.5)*self.indices["depl"]
                    if self.y <self.ground:
                        self.x-=2

            if self.g==True:
                self.x-=(2+self.sens*1.5)*self.indices["depl"]
                if self.y <self.ground:                                 #pareil que le deplacement a droite
                    self.x-=2
                if self.collision(opp)==False:
                    self.x+=(2+self.sens*1.5)*self.indices["depl"]
                    if self.y <self.ground:
                        self.x+=2

        if self.collision(opp)=="push":            #effet de poussee si contact avec l'adevrsaire
            cote=0
            if opp.x-self.x==0:
                cote=1
                if max(self.x,opp.x)>600:
                    cote=-1
            opp.x+=(opp.x-self.x+cote)/abs(opp.x-self.x+cote)*5
            if opp.collision(self)==False:
                opp.x-=(opp.x-self.x+cote)/abs(opp.x-self.x+cote)*5
            self.x+=(self.x-opp.x+cote)/abs(self.x-opp.x+cote)*5            #recul du joueur et de l'adversaire en fonction du sens et des collisions
            if self.collision(opp)==False:
                self.x-=(self.x-opp.x+cote)/abs(self.x-opp.x+cote)*5

        if self.coup in ["down","straight","up"]:
            self.y = self.ground
            if self.indice>=len(self.sprite[0]):  #coup qui utilise tous les sprites
                self.coup=None
                if self.sneak=="wait":            #si le joueur etait accrostraighti, il le redevient apres son coup
                    self.sneak=True

        if self.coup=="air":
            if self.indice>=len(self.sprite[0]):
                self.coup=None
            self.rect_coup=pygame.Rect(self.x+self.rectangle["air"][0][self.sens],
                                               self.y+self.rectangle["air"][1]+self.ground-350,    #mise a jour du coup aerien
                                               self.rectangle["air"][2],
                                               self.rectangle["air"][3])


        #si le joueur recule, il bloque les attaques
        if self.d==True and self.sens==1:
            self.blocking=True

        elif self.g==True and self.sens==0:
            self.blocking=True

        else:
            self.blocking=False

        if self.collision(opp)==False and self.x<600:
            self.x+=1

        if self.collision(opp)==False and self.x>600:
            self.x-=1

        #hitbox en fonction de l'action
        if self.sneak==True:
            self.rect=pygame.Rect(self.x+self.rectangle["sneak"][0][self.sens],
                                               self.y+self.rectangle["sneak"][1],
                                               self.rectangle["sneak"][2],
                                               self.rectangle["sneak"][3])

        elif self.y<self.ground:
            self.rect=pygame.Rect(self.x+self.rectangle["jump"][0][self.sens],
                                               self.y+self.rectangle["jump"][1],
                                               self.rectangle["jump"][2],
                                               self.rectangle["jump"][3])

        else:
            self.rect=pygame.Rect(self.x+self.rectangle["hitbox"][0][self.sens],
                                               self.y+self.rectangle["hitbox"][1],
                                               self.rectangle["hitbox"][2],
                                               self.rectangle["hitbox"][3])

    def images(self):
        """fonction qui determine la liste d'images utilisee en fonction de l'action du joueur
        change aussi les indices de changements d'images"""

        if self.sprite is None:
            self.sprite=self.standing
            self.plus_i=self.indices["stand"]

        if self.d==True:
            self.sprite=(self.walk,self.back)[self.sens]
            self.plus_i=self.indices["i_depl"]

        if self.g==True:
            self.sprite=(self.back,self.walk)[self.sens]
            self.plus_i=self.indices["i_depl"]

        if self.d==False and self.g==False:
            self.sprite=self.standing
            self.plus_i=self.indices["stand"]

        if self.sneak==True:
            self.sprite=self.crouch

        if self.y<self.ground:
            self.sprite=self.jump
            self.plus_i=self.indices["jump"]

        if self.coup=="down":
            self.sprite=self.down
            self.plus_i=self.indices["down"]

        if self.coup=="straight":
            self.sprite=self.straight
            self.plus_i=self.indices["straight"]

        if self.coup=="up":
            self.sprite=self.up
            self.plus_i=self.indices["up"]

        if self.coup=="air":
            self.sprite=self.jump_hit
            self.plus_i=self.indices["air"]

        if self.touched==True:
            self.sprite=self.touch
            self.plus_i=self.indices["touched"]
            
        if self.is_blocking==True:
            self.sprite=self.block

        if self.hp<=0:
            self.sprite=self.ko



    def able(self):
        """determine si le joueur est autorise ou non a realiser differentes action suivant l'action qu'il realise actuellement"""

        if self.y<self.ground:
            self.jump_able=False
            self.hit_able=False
            self.air_hit_able=True
            self.move_able=True

        if self.y>=self.ground:
            self.jump_able=True
            self.hit_able=True
            self.air_hit_able=False
            self.move_able=True
            self.is_blocking=False

        if self.coup in ["down","straight","up"]:
            self.jump_able=False
            self.hit_able=False
            self.move_able=False

        if self.coup=="air":
            self.air_hit_able=False

        if self.touched==True:
            self.jump_able=False
            self.hit_able=False
            self.air_hit_able=False
            self.move_able=False

        if self.sneak==True:
            self.jump_able=False
            self.hit_able=True
            self.move_able=False

        if self.hp<=0:
            self.jump_able=False
            self.hit_able=False
            self.air_hit_able=False
            self.move_able=False

    def collision(self,opp):
        """gere les collisions avec les murs, l'ennemi et les teleportation de la map portail"""

        if carte=="maps2":                       #pour la map portail
            if self.rect.colliderect((63,450,1,150)) :
                self.x=850
            if self.rect.colliderect((1118,450,1,150)) :
                self.x=0

        if self.rect.colliderect(0,0,1,600) or self.rect.colliderect(1199,0,1,600):
            return False

        if self.rect.colliderect(opp.rect):
                return "push"

        return True

    def bobo(self,opp):
        """determine si le joueur est touche oar le coup adverse, et si il le bloque ou non"""

        if self.coup is not None:
            if self.rect_coup.colliderect(opp.rect) and self.hit==False and self.coup in ["up","down"] and opp.blocking==True and opp.energy>=4:
                opp.energy-=1.5
                opp.v_saut=int(7)
                opp.v_touched_x=int(5)
                opp.is_blocking=True
                self.hit=True                        #le joueur bloque mais perd de l'energie
            elif self.rect_coup.colliderect(opp.rect) and self.hit==False:
                opp.hp-=self.degats[self.coup]
                opp.touched=True                                        #le joueur est touche, perd des pv et recul en fonction du coup
                opp.v_saut=int(7*self.mutipl_dist[self.coup][0])
                opp.v_touched_x=int(5*self.mutipl_dist[self.coup][1])
                self.hit=True

    def update(self,opp):
        """lance toutes les fonction de la classe personnage et mets a jour l'energie"""

        self.deplacement(opp)
        self.images()
        self.able()
        self.bobo(opp)
        self.indice+=self.plus_i
        #l'energie depend de ce qu'on a deja, pour "punir" les "spammeurs"
        if self.energy<3:
            self.energy+=0.022
        elif self.energy<6:
            self.energy+=0.028
        elif self.energy<10:
            self.energy+=0.033
        elif self.energy<20:
            self.energy+=0.044
        else:
            self.energy=20




class IA:

    def __init__(self,nom,pv, degats, vitesses, x,y, id_force=None): #def des attaques etc (reprenant les éléments de la classe personnage)
        self.perso = Personnage_vs(nom, pv, degats, vitesses, mult, cost, x,y, rectangles)
        self.cooldown = 0
        self.action = "standing"
        self.action_timer = 0  #duree de l'action en cours


    def update(self, joueur):
        self.perso.update(joueur)
        distance = abs(self.perso.x - joueur.x)

        #cooldown attaque
        if self.cooldown > 0:
            self.cooldown -= 1
            if self.action_timer > 0:
                self.action_timer -= 1
                self.executer_action(joueur)
            return

        #timer d'action
        if self.action_timer > 0:
            self.action_timer -= 1
            self.executer_action(joueur)
            return

        #decision seulement si aucune action en cours
        if distance > 300:
            self.action = "avancer"
            self.action_timer = 40

        elif distance > 200:
            choices = ["avancer", "avancer", "avancer", "idle"]
            #probabilité de saut
            if self.perso.jump_able and random.random() < 0.15:
                choices.append("sauter")
            self.action = random.choice(choices)
            self.action_timer = 30

        elif distance > 120:
            #chances d'attaquer
            choices = ["avancer", "attaquer", "attaquer"]
            if self.perso.jump_able and random.random() < 0.2:
                choices.append("sauter")
            self.action = random.choice(choices)
            self.action_timer = 25

        else:
            #plus agressif à courte distance
            choices = ["attaquer", "attaquer", "attaquer", "reculer"]
            if self.perso.jump_able and random.random() < 0.12:
                choices.append("sauter")
            self.action = random.choice(choices)
            self.action_timer = 20

        #action
        self.executer_action(joueur)

    def executer_action(self, joueur):
        distance = abs(self.perso.x - joueur.x)

        # reset déplacements
        self.perso.d = False
        self.perso.g = False

        # avancer vers le joueur
        if self.action == "avancer":
            if self.perso.x < joueur.x:
                self.perso.d = True
            else:
                self.perso.g = True

        # sauter
        elif self.action == "sauter":
            if self.perso.jump_able:
                self.perso.v_saut = 15
                self.perso.indice = 0
                #avancer en sautant
                if self.perso.x < joueur.x:
                    self.perso.d = True
                else:
                    self.perso.g = True
                #possibilité d'attaque aérienne
                if distance < 180 and random.random() < 0.6:
                    self.action = "attaque_air"
            self.cooldown = 20

        #attaque au sol choisit aléatoirement entre straight, up et down
        elif self.action == "attaquer":
            if distance < 150 and self.perso.hit_able:
                #choisir le type d'attaque en fonction de l'énergie disponible
                attaques_possibles = []

                if self.perso.energy >= self.perso.cost["straight"]:
                    attaques_possibles.append("straight")
                if self.perso.energy >= self.perso.cost["up"]:
                    attaques_possibles.append("up")
                if self.perso.energy >= self.perso.cost["down"]:
                    attaques_possibles.append("down")

                if attaques_possibles:
                    type_attaque = random.choice(attaques_possibles)

                    self.perso.coup = type_attaque
                    self.perso.rect_coup = pygame.Rect(
                        self.perso.x + self.perso.rectangle[type_attaque][0][self.perso.sens],
                        self.perso.y + self.perso.rectangle[type_attaque][1],
                        self.perso.rectangle[type_attaque][2],
                        self.perso.rectangle[type_attaque][3]
                    )

                    if type_attaque == "straight":
                        self.perso.sprite = self.perso.straight
                    elif type_attaque == "up":
                        self.perso.sprite = self.perso.up
                    elif type_attaque == "down":
                        self.perso.sprite = self.perso.down

                    self.perso.indice = 0
                    self.perso.hit = False
                    self.perso.energy -= self.perso.cost[type_attaque]
                    self.cooldown = 50

                #reculer par rapport au joueur
        elif self.action == "reculer":
            if self.perso.x < joueur.x:
                self.perso.g = True  #recule vers la gauche
            else:
                self.perso.d = True #ou vers la droite


            self.cooldown = 15

            self.cooldown = 30  #petit cooldown pour éviter qu'elle recule trop

        #attaque en l'air
        elif self.action == "attaque_air":
            if distance < 180 and self.perso.air_hit_able and self.perso.energy >= self.perso.cost["air"]:
                self.perso.coup = "air"
                self.perso.rect_coup = pygame.Rect(
                    self.perso.x + self.perso.rectangle["air"][0][self.perso.sens],
                    self.perso.y + self.perso.rectangle["air"][1],
                    self.perso.rectangle["air"][2],
                    self.perso.rectangle["air"][3]
                )
                self.perso.sprite = self.perso.jump_hit
                self.perso.indice = 0
                self.perso.hit = False
                self.perso.energy -= self.perso.cost["air"]
                self.cooldown = 40

        #standing
        else:
            pass

    def attaque(self, opp, type_attaque="straight"): #gère les attaques et inflige des dégâts à l'opposnt

        distance = abs(self.x - opp.x)#dist pour frapper

        if distance < 150:  #dist de l'attaque
            if type_attaque =="straight":
                opp.hp -= self.dgt_straight
                opp.sprite = opp.touch
                opp.indice = 0
            elif type_attaque == "up":
                opp.hp -= self.dgt_up
                opp.sprite = opp.touch
                opp.indice = 0
            elif type_attaque == "down":
                opp.hp -= self.dgt_down
                opp.sprite = opp.touch
                opp.indice = 0



#femme = Personnages_vs(id, noms, pv, degats, vitesses, mult, cost, x,y, rect)   #################################################################################################################"
#garde = Personnages_vs(id, noms, pv, degats, vitesses, mult, cost, x,y, rect)
#################################################################################################################





#################################################################################################################



#################################################################################################################





def sens(J1,J2):
    """fonction prenant en parametres J1 et J2 de la classe personnage afin de determiner le sens de chacun
    0 = a gauche de l'autre joueur ; 1 = a droite de l'autre joueur"""
    if J1.sens is None:
        J1.sens=0
        J2.sens=1

    if J1.x>J2.x:
        J1.sens=1
        J2.sens=0

    else:
        J1.sens=0
        J2.sens=1




#################################################################################################################

#creation de la fenetre (taille, et autres paramètres optionnels)

#fenetre = pygame.display.set_mode((0,0),FULLSCREEN)
fenetre = pygame.display.set_mode((1280,720))
"""alternez entre les deux fenetres pour quand on code"""

clock=pygame.time.Clock() #initialistaion de l'horloge


taille=pygame.display.get_surface().get_size() #recupere taille de l'ecran
mult_x=taille[0]/1280
mult_y=taille[1]/720
pygame.mouse.set_visible(False)


def t(nom,xplus=None,yplus=None):
    global mult_x, mult_y
    img=pygame.image.load("packs/"+nom).convert_alpha()
    if xplus is None and yplus is None:
        dimensions=img.get_rect().size
    else :
        dimensions=(xplus,yplus)
    return(pygame.transform.scale(img,(int(dimensions[0]*mult_x),int(dimensions[1]*mult_y))))

def b(img,x,y):
    fenetre.blit(img,(x*mult_x,y*mult_y))



def map_actuelle():
    global lieu, sexe, carte, indice_base,lumiere
    if lieu=="MOON":
        carte=map_moon
    if lieu=="BASE":
        if indice_base>1:
            indice_base=0
            carte=map_bases[random.choice([0]*67+[1]*6)]
    if lieu=="LABO":
        carte=map_labo
        lumiere=(False,True)[random.choice([0]*67+[1]*6)]
    if lieu == "FIRST":
        carte = map_first_step
    if lieu == "POSTE_PILOTE":
        carte = interieur_vaisseau
    if lieu == "CRASH" :
        carte = map_crash
    if lieu == "MANOIR":
        carte = map_manoir
    if lieu == "BUREAU":
        carte = map_bureau


launch=t("menus/menu_0.png",1280,720)
animation("demarrage")
#################################
"""TESTEZ LES CURSEURS ET ON SE METTRA D'ACCORD"""
curseur_p=t("icons/curseur.png",50,50) #curseur 1
curseur=t("icons/curseur_2.png",85,85) #curseur 2
#curseur=t("icons/curseur_3.png",40,40) #curseur 3
#curseur=t("icons/curseur_4.png",40,40) #curseur 4



class garde :
    """classe qui dicte le comportement des pnj rpg"""
    def __init__(self, direction):
        self.x = 380
        self.y = 79
        self.indice = 0
        self.anim_indice=1
        self.vivant=True
        self.rect_garde = pygame.Rect(self.x, self.y, self.x-494, self.y-144)
        self.rect_regarde = pygame.Rect(200,200,200,200)
        self.haut=self.bas=False
        self.direction = direction
        self.h=[]
        i=1
        while i!=0:
            try:
                img=t("personnages/soldat/h"+str(i)+".png",38*2.3,33*2.3)
                self.h.append(img)
                i+=1
            except:
                i=0

        self.b=[]
        i=1
        while i!=0:
            try:
                img=t("personnages/soldat/b"+str(i)+".png",38*2.3,33*2.3)
                self.b.append(img)
                i+=1
            except:
                i=0


        self.g=[]
        i=1
        while i!=0:
            try:
                img=t("personnages/soldat/g"+str(i)+".png",38*2.3,33*2.3)
                self.g.append(img)
                i+=1
            except:
                i=0

        self.d=[]
        i=1
        while i!=0:
            try:
                img=t("personnages/soldat/d"+str(i)+".png",38*2.3,33*2.3)
                self.d.append(img)
                i+=1
            except:
                i=0
        self.sprite=self.b
    def deplacement_lineaire(self):

        if self.direction == 'bas' :
            self.y += 2
            self.rect_garde = pygame.Rect(self.x+15, self.y, 60, 83)
            self.rect_regarde = pygame.Rect(self.x+15,self.y+48,65,200)
            if self.rect_garde.collidelist(liste_collision_base) !=-1 :
                self.y -= 2
                self.direction = 'haut'
                self.rect_garde = pygame.Rect(self.x, self.y, 20, 20)
                self.rect_regarde = pygame.Rect(self.x,self.y-200,35,200)
        elif self.direction =='haut' :
            self.y -= 2
            self.rect_garde = pygame.Rect(self.x+15, self.y, 60, 83)
            self.rect_regarde = pygame.Rect(self.x+15,self.y-200,65,200)
            if self.rect_garde.collidelist(liste_collision_base) !=-1 :
                self.y += 2
                self.direction = 'bas'
                self.rect_garde = pygame.Rect(self.x, self.y, 20, 20)
                self.rect_regarde = pygame.Rect(self.x,self.y+48,35,200)

    def mort(self):
        self.rect_garde = pygame.Rect(self.x, self.y, 20, 20)
        self.rect_regarde = pygame.Rect(self.x,self.y+48,0,0)
        b(soldat_mort,self.x+35,self.y+180)

    def affichage(self) :
        self.anim_indice += 0.08
        if self.direction == 'haut' :
            b(self.h[int(self.anim_indice)%3],self.x,self.y)
        elif self.direction == 'bas' :
            b(self.b[int(self.anim_indice)%3],self.x,self.y)
soldat_combat = garde("bas")

class perso_rpg:
    """classe qui fait le perso du rpg quoi"""
    def __init__(self):
        self.sexe=None
        self.soldat=None
        self.x,self.y=550*mult_x, 350*mult_y
        self.acceleration=0
        self.indice=1
        #self.inventaire=Inventaire()
        self.capacites=[]
        self.etat = "ombre"
        self.vitesse = 0
        self.droite=self.gauche=self.haut=self.bas=self.run=self.dash=False
        self.rect = pygame.Rect(self.x,self.y,71,62)

        self.d=[]
        i=1
        while i!=0:
            try:
                img=t("personnages/ombre/d"+str(i)+".png",38*2,33*2)
                self.d.append(img)
                i+=1
            except:
                i=0

        self.h=[]
        i=1
        while i!=0:
            try:
                img=t("personnages/ombre/h"+str(i)+".png",38*2,33*2)
                self.h.append(img)
                i+=1
            except:
                i=0

        self.g=[]
        i=1
        while i!=0:
            try:
                img=t("personnages/ombre/g"+str(i)+".png",38*2,33*2)
                self.g.append(img)
                i+=1
            except:
                i=0

        self.b=[]
        i=1
        while i!=0:
            try:
                img=t("personnages/ombre/b"+str(i)+".png",38*2,33*2)
                self.b.append(img)
                i+=1
            except:
                i=0

        self.db=[]
        i=1
        while i!=0:
            try:
                img=t("personnages/ombre/db"+str(i)+".png",38*2,33*2)
                self.db.append(img)
                i+=1
            except:
                i=0

        self.dh=[]
        i=1
        while i!=0:
            try:
                img=t("personnages/ombre/dh"+str(i)+".png",38*2,33*2)
                self.dh.append(img)
                i+=1
            except:
                i=0

        self.gb=[]
        i=1
        while i!=0:
            try:
                img=t("personnages/ombre/gb"+str(i)+".png",38*2,33*2)
                self.gb.append(img)
                i+=1
            except:
                i=0

        self.gh=[]
        i=1
        while i!=0:
            try:
                img=t("personnages/ombre/gh"+str(i)+".png",38*2,33*2)
                self.gh.append(img)
                i+=1
            except:
                i=0

        self.sprite=self.b

    def chg_etat(self,sexe):

        if self.etat=="ombre":
            self.sexe=sexe
            self.d=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/"+self.sexe+"/d"+str(i)+".png",38*2,33*2)
                    self.d.append(img)
                    i+=1
                except:
                    i=0

            self.h=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/"+self.sexe+"/h"+str(i)+".png",38*2,33*2)
                    self.h.append(img)
                    i+=1
                except:
                    i=0

            self.g=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/"+self.sexe+"/g"+str(i)+".png",38*2,33*2)
                    self.g.append(img)
                    i+=1
                except:
                    i=0

            self.b=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/"+self.sexe+"/b"+str(i)+".png",38*2,33*2)
                    self.b.append(img)
                    i+=1
                except:
                    i=0

            self.rd=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/"+self.sexe+"/rd"+str(i)+".png",38*2,33*2)
                    self.rd.append(img)
                    i+=1
                except:
                    i=0

            self.rh=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/"+self.sexe+"/rh"+str(i)+".png",38*2,33*2)
                    self.rh.append(img)
                    i+=1
                except:
                    i=0

            self.rg=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/"+self.sexe+"/rg"+str(i)+".png",38*2,33*2)
                    self.rg.append(img)
                    i+=1
                except:
                    i=0

            self.rb=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/"+self.sexe+"/rb"+str(i)+".png",38*2,33*2)
                    self.rb.append(img)
                    i+=1
                except:
                    i=0

            self.dd=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/"+self.sexe+"/dd"+str(i)+".png",38*2,33*2)
                    self.dd.append(img)
                    i+=1
                except:
                    i=0

            self.dh=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/"+self.sexe+"/dh"+str(i)+".png",38*2,33*2)
                    self.dh.append(img)
                    i+=1
                except:
                    i=0

            self.dg=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/"+self.sexe+"/dg"+str(i)+".png",38*2,33*2)
                    self.dg.append(img)
                    i+=1
                except:
                    i=0

            self.db=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/"+self.sexe+"/db"+str(i)+".png",38*2,33*2)
                    self.db.append(img)
                    i+=1
                except:
                    i=0

            self.sprite_direction=(self.b,self.rb,self.db)

        else:
            self.d=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/ombre/d"+str(i)+".png",38*2,33*2)
                    self.d.append(img)
                    i+=1
                except:
                    i=0

            self.h=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/ombre/h"+str(i)+".png",38*2,33*2)
                    self.h.append(img)
                    i+=1
                except:
                    i=0

            self.g=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/ombre/g"+str(i)+".png",38*2,33*2)
                    self.g.append(img)
                    i+=1
                except:
                    i=0

            self.b=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/ombre/b"+str(i)+".png",38*2,33*2)
                    self.b.append(img)
                    i+=1
                except:
                    i=0

            self.db=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/ombre/db"+str(i)+".png",38*2,33*2)
                    self.db.append(img)
                    i+=1
                except:
                    i=0

            self.dh=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/ombre/dh"+str(i)+".png",38*2,33*2)
                    self.dh.append(img)
                    i+=1
                except:
                    i=0

            self.gb=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/ombre/gb"+str(i)+".png",38*2,33*2)
                    self.gb.append(img)
                    i+=1
                except:
                    i=0

            self.gh=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/ombre/gh"+str(i)+".png",38*2,33*2)
                    self.gh.append(img)
                    i+=1
                except:
                    i=0


    def dpl_corps(self,touche,action):

        """touche c'est la touche engagee et action c'est appui ou relache genre"""
        if self.dash==False:
            if action==KEYDOWN:

                if touche==K_d:
                    self.droite=True
                    self.gauche=False
                if touche==K_q:
                    self.droite=False
                    self.gauche=True
                if touche==K_z:
                    self.haut=True
                    self.bas=False
                if touche==K_s:
                    self.haut=False
                    self.bas=True
                if touche==K_SPACE:
                    self.run=True
                if touche==K_LSHIFT and True in (self.haut,self.bas,self.droite,self.gauche) and self.indice>10:
                    self.dash=True
                    self.indice=0


            elif action==KEYUP:

                if touche==K_d:
                    self.droite=False
                if touche==K_q:
                    self.gauche=False
                if touche==K_z:
                    self.haut=False
                if touche==K_s:
                    self.bas=False
                if touche==K_SPACE:
                    self.run=False

    def bouge_corps(self):
        if self.dash==False:
            self.vitesse=3
            if self.run==True:
                self.vitesse+=1
            if self.droite==True:
                self.x+=self.vitesse
            if self.gauche==True:
                self.x-=self.vitesse
            if self.bas==True:
                self.y+=self.vitesse
            if self.haut==True:
                self.y-=self.vitesse

        if self.dash==True:
            self.vitesse=8
            if self.indice>=3:
                self.dash=False
            else:
                if self.droite==True:
                    self.x+=self.vitesse
                if self.gauche==True:
                    self.x-=self.vitesse
                if self.bas==True:
                    self.y+=self.vitesse
                if self.haut==True:
                    self.y-=self.vitesse

        self.rect = pygame.Rect(joueur.x+26,joueur.y+45,28,15)

        if self.collide() in (True,"trans"):  ######################## A continuer pour controler si on peut traverser les murs ou pas
                if self.droite==True:
                    self.x-=self.vitesse
                if self.gauche==True:
                    self.x+=self.vitesse
                if self.bas==True:
                    self.y-=self.vitesse
                if self.haut==True:
                    self.y+=self.vitesse


    def collide(self):
        for col in choix_collision():
            if self.rect.colliderect(col):
                return True
        if self.dash==False:
            for col in choix_collision("trans"):
                if self.rect.colliderect(col):
                    return True

    def interaction(self,touche,action):
        global lieu,event,collision_xoford, xoford_text, dash_text, map_first_step,start_k,droit_pass, scenario_1, scenario_2, dialogue_leparrain, collision_leparrain,pensee_0, pensee_1, pensee_2, objectif_0, parole_0, parole_1, KOMBAT_PARRAIN

        if lieu == "MOON":
            if self.etat == "ombre " and self.rect.colliderect(collision_objectif) :
                if event.type==KEYUP and event.key == K_SPACE:
                    objectif_0 = not objectif_0
            if self.etat == "ombre" and self.rect.colliderect(collision_xoford):
                if action == KEYUP and touche == K_e:
                    xoford_text = not xoford_text
                if event.type==KEYUP and event.key == K_SPACE:
                    pensee_0 = not pensee_0

        if lieu == "POSTE_PILOTE":
            if self.rect.colliderect(collision_decollage):
                if action==KEYUP and touche==K_e:
                    pygame.mixer.music.stop()
                    decollage_sound.play()
                    animation("decollage")
                    animation("vol")
                    lieu = "CRASH"
                    joueur.x, joueur.y = 80,276
                    joueur.chg_etat(ombre)
                    joueur.etat = "ombre"


        if lieu=="FIRST":

            if self.etat == "ombre " and self.rect.colliderect(collision_objectif) :
                if event.type==KEYUP and event.key == K_SPACE:
                    objectif_0 = not objectif_0

            if self.rect.colliderect(liste_collision_scenario[0]):
                if event.type==KEYUP and event.key == K_e:
                    scenario_1 = not scenario_1
                if event.type==KEYUP and event.key == K_SPACE:
                    pensee_1 = not pensee_1

            if self.rect.colliderect(liste_collision_scenario[1]):
                if action == KEYUP and touche == K_e :
                    scenario_2 = not scenario_2
                if event.type==KEYUP and event.key == K_SPACE:
                    pensee_2 = not pensee_2

            if self.rect.colliderect(collision_casse_vitre):
                if action==KEYUP and touche==K_e:
                    breakglass_sound.play()
                    animation("ecran_noir")
                    droit_pass = True
                    map_first_step = t("maps/firststep2.png", 1280, 720)

        if lieu == "BUREAU" :
            if self.rect.colliderect(collision_leparrain):
                if event.type==KEYUP and event.key == K_e:
                    dialogue_leparrain = not dialogue_leparrain
                if event.type==KEYUP and event.key == K_a:
                    parole_1 = not parole_1
                if event.type==KEYUP and event.key == K_p:
                    start_k = True

        if lieu=="BASE":
            if self.etat == "corps" and self.rect.colliderect(collision_pan_dash):
                if event.type==KEYUP and event.key == K_e:
                    dash_text = not dash_text
                if event.type==KEYUP and event.key == K_a:
                    parole_0 = not parole_0





    def collide_chg(self):
        global lieu, sexe, map_bases, start_k, collision_champ_magnetique, collision_incarnation_soldat
        if lieu=="MOON":
            if droit_pass == False :
                if self.rect.colliderect(collision_champ_magnetique):
                    if joueur.x < 213 :
                        joueur.x, joueur.y = joueur.x-15, joueur.y-15
                    elif joueur.x< 359 and joueur.y >449:
                        joueur.y-= 15
                    else :
                        joueur.x = joueur.x+15
            else:
                collision_champ_magnetique = (0,0,0,0)
            if self.rect.colliderect(collision_femme):
                lieu="BASE"
                joueur.x,joueur.y = 1159, 408


            if self.rect.colliderect(collision_firststep):
                lieu="FIRST"
                joueur.x,joueur.y = 82,390

        elif lieu == "FIRST":
            if self.rect.colliderect(collision_retour_firststep):
                lieu = "MOON"
                joueur.x,joueur.y = 873, 473


        elif lieu == "BASE" :
            if self.rect.colliderect(collision_retour_moon):
                lieu = "MOON"
                joueur.x,joueur.y = 411, 511
            if joueur.rect.colliderect(collision_labo):
                lieu="LABO"
                joueur.x,joueur.y = 295, 63
            if joueur.etat == "corps" and joueur.rect.colliderect(collision_acces_vaisseau):
                lieu="POSTE_PILOTE"
                joueur.x,joueur.y = 534,537
            if joueur.etat == "corps" and self.rect.colliderect(soldat_combat.rect_regarde) :
                start_k = True
                pygame.mixer.music.pause()
                scream_sound.play()

        elif lieu == "POSTE_PILOTE":
             if joueur.etat == "corps" and joueur.rect.colliderect(collision_retour_acces_vaisseau):
                lieu = "BASE"
                joueur.x,joueur.y = 95, 510

        elif lieu=="LABO":
            if self.rect.colliderect(collision_incarnation_f) and joueur.etat=="ombre":
                            sexe="femme"
                            joueur.chg_etat(sexe)
                            joueur.etat="corps"
                            map_base_1 = []
                            for i in range (2):
                                img=t("maps/ABaseF"+str(i+1)+"_open.png")
                                map_base_1.append(img)
                            map_bases=map_base_1
                            possess_sound.play()
                            animation("possess")
                            self.x,self.y=1180,297

            elif self.rect.colliderect(collision_incarnation_h) and joueur.etat=="ombre":
                            sexe="homme"
                            joueur.chg_etat(sexe)
                            joueur.etat="corps"
                            map_base_1 = []
                            for i in range (2):
                                img=t("maps/ABaseF"+str(i+1)+"_open.png")
                                map_base_1.append(img)
                            map_bases=map_base_1
                            possess_sound.play()
                            animation("possess")
                            self.x,self.y=1180,174

            if self.rect.colliderect(collision_retour_base):
                lieu="BASE"
                joueur.x,joueur.y = 1032,249

        elif lieu == "CRASH":
            if joueur.etat =="ombre" and self.rect.colliderect(collision_incarnation_soldat):
                possess_sound.play()
                sexe ="soldat"
                joueur.chg_etat(sexe)
                joueur.etat="corps"
                possess_sound.play()
                animation("possess")
            if joueur.etat =="corps":
                if self.rect.colliderect(collision_manoir):
                    lieu = "MANOIR"
                    joueur.x, joueur.y = 578, 620


        elif lieu == "MANOIR":
            if self.rect.colliderect(collision_entree_manoir):
                pygame.mixer.music.load("sounds/parrain_ost.mp3")
                pygame.mixer.music.play()
                lieu = "BUREAU"
                joueur.x, joueur.y = 594,632
            if self.rect.colliderect(collision_retour_manoir):
                lieu = "CRASH"
                joueur.x, joueur.y = 620, 65


        elif lieu == "BUREAU":
            if self.rect.colliderect(collision_sortie_manoir):
                lieu = "MANOIR"
                joueur.x, joueur.y = 590,325





    def sprt_corps(self):

        if self.bas==True:
            self.sprite_direction=(self.b,self.rb,self.db)
        if self.haut==True:
            self.sprite_direction=(self.h,self.rh,self.dh)
        if self.droite==True:
            self.sprite_direction=(self.d,self.rd,self.dd)
        if self.gauche==True:
            self.sprite_direction=(self.g,self.rg,self.dg)
        if self.run==True:
            self.sprite=self.sprite_direction[1]
        if self.dash==True:
            self.sprite=self.sprite_direction[2]
        if self.dash==False and self.run==False:
            self.sprite=self.sprite_direction[0]


    def dpl_ombre(self, x,y ):
        # x et y du clic ainsi que de l'objet ombre
        v_x = x -  self.x-40
        v_y = y -  self.y-40
        norme = math.sqrt(v_x**2 + v_y**2)
        if norme > 1.5 :
             self.x +=v_x *(3+self.acceleration)*mult_x // norme
             self.y+=v_y *(3+self.acceleration)*mult_y // norme

    def sprt_ombre(self,x,y):
        v_x = x -  self.x-40
        v_y = y -  self.y-40
        if v_x!=0:
            coeff=v_y/v_x
        if v_x>0:
            if -0.5<coeff<0.5:
                self.sprite=self.d
            elif 0.5<coeff<1.5:
                self.sprite=self.db
            elif 1.5<coeff<2:
                self.sprite=self.b
            elif -1.5<coeff<-0.5:
                self.sprite=self.dh
            elif -2<coeff<-1.5:
                self.sprite=self.h
        elif v_x<0:
            if -0.5<coeff<0.5:
                self.sprite=self.g
            elif 0.5<coeff<1.5:
                self.sprite=self.gh
            elif 1.5<coeff<2:
                self.sprite=self.h
            elif -1.5<coeff<-0.5:
                self.sprite=self.gb
            elif -2<coeff<-1.5:
                self.sprite=self.b
        if math.sqrt(v_x**2 + v_y**2)<1.5:
            self.sprite=self.b

    def update(self,x,y):
        if self.etat=="ombre":
            if resume==False:
                self.dpl_ombre(x,y)
            self.rect = pygame.Rect(joueur.x+24,joueur.y+24,34,36)
            self.sprt_ombre(x,y)
            self.acceleration-=0.1
            if self.acceleration<0:
                self.acceleration=0
            self.indice+=0.13
        else:
            if resume==False:
                self.sprt_corps()
                self.bouge_corps()
                if True in (self.droite, self.gauche, self.haut, self.bas) and self.dash==False:
                    self.indice+=0.09
                elif self.dash==True:
                    self.indice+=0.12
        self.collide_chg()





#modif Eden 10 mars
liste_comet_anim =[]
for i in range (1,6):
    image = t("icons/comet_"+str(i)+".png")
    liste_comet_anim.append(image)

liste_diagomet_anim =[]
for i in range (1,6):
    image = t("icons/diagomet_"+str(i)+".png")
    liste_diagomet_anim.append(image)
#################################################################################################################
 ### modif
x, y =0,0
lieu = "MOON"
acceleration=0
joueur=perso_rpg()
sexe=None
ombre=True
KOMBAT = False
lumiere=False
start_k=False
#images map
pause=t("menus/pause.png")
resume=False
guidage = t("icons/indications_touches.png", 344,316)
guidage_ombre = t("icons/indications_touches_ombre.png", 200,150)
touches_kombat = t("icons/touches_kombat.png", 266,589)
lit = t("icons/lit_cadavre.png")
map_moon= t("maps/Amoon.png", 1280, 720)
map_first_step = t("maps/firststep.png", 1280, 720)
map_base_1 = []
map_crash = t("maps/map_crash.png")
map_manoir = t("maps/mansion_godfather_2.png", 1280, 720)
map_bureau = t("maps/bureau_parrain.png", 1280, 720)
for i in range (2):
    img=t("maps/ABaseF"+str(i+1)+".png")
    map_base_1.append(img)
dessus_base=t("maps/base_up.png")
indice_x=0

map_bases=map_base_1
indice_base=1.1
indice_comete=1

map_labo=t("maps/LABO.png")
filtre=t("maps/voit_r.png")
filtre_o=t("maps/voit_r_o.png")
dessus_labo=t("maps/labo_up.png")

KO=pygame.image.load("packs/icons/KO.png").convert_alpha()
KO=pygame.transform.scale(KO,(230,107))
energy_icon=pygame.image.load("packs/icons/energy.png").convert_alpha()
energy_icon=pygame.transform.scale(energy_icon,(40,40))

# images elements in game
xoford = []
for i in range(1,5):
    img=t("personnages/cadavre"+str(i)+".png", 2.5*37,2.5*19)
    xoford.append(img)
femme_morte =t("personnages/cadavre_f.png", 1.4*45, 1.4*26)
homme_mort = t("personnages/cadavre_h.png", 1.35*45, 1.35*26)
soldat_mort = t("personnages/cadavre_soldat.png", 1.35*45, 1.35*26)
kombat_labo = t("maps/kombat_labo.png", 1280, 720)
kombat_parrain = t("maps/kombat_bureau.png", 1280, 720)
open_gate = t("icons/open_gate.png")
interieur_vaisseau = t("maps/interieur_vaisseau.png", 1280, 720)
carte=map_moon
liste_rects_lits = []
possess_sound = pygame.mixer.Sound('sounds/possess.mp3')
possess_sound.set_volume(0.80)
scream_sound = pygame.mixer.Sound('sounds/scream_bring.mp3')
scream_sound.set_volume(0.50)
breakglass_sound =pygame.mixer.Sound('sounds/verrebrisé_sound.wav')
decollage_sound =pygame.mixer.Sound('sounds/decollage_sound.mp3')
crash_sound =pygame.mixer.Sound('sounds/crash_sound.mp3')
pygame.mixer.music.load("sounds/bring_me.mp3")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.5)


xoford_text = False
droit_pass = False
scenario_1 = False
scenario_2 = False
dash_text = False
pensee_0 = False
pensee_1 = False
pensee_2 = False
objectif_0 = False
tps=None
dialogue_leparrain = False
parole_0 = False
parole_1 = False
ordrec = 0



sprite_feu = pygame.image.load("packs/icons/feu.png").convert_alpha()
images_feu= [sprite_feu.subsurface(16*i,0,16,16) for i in range(5)]
for i in range(len(images_feu)):
    images_feu[i]= pygame.transform.scale(images_feu[i],(38,50))

liste_image_fog =[]
for i in range (1,4):
    image=pygame.image.load("packs/icons/fog_"+str(i)+".png")
    image = pygame.transform.scale(image, (115*4,115*4))
    liste_image_fog.append(image)

indice_guidage = 1
liste_pan = []
for i in range(1,4):
    image = pygame.image.load("packs/icons/pan_"+str(i)+".png")
    #image = pygame.transform.scale(image, (115*4,115*4))
    liste_pan.append(image)

panneau = pygame.image.load("packs/icons/pan_0.png").convert_alpha()
anim_deco=[]
for i in range(21):
    img=t("animation/animation_decollage_"+str(i+1)+".png")
    anim_deco.append(img)

anim_vol=[]
for i in range(1, 49):
    img=t("animation/animation_vol_"+str(i)+".png")
    anim_vol.append(img)
    
fin=[]
for i in range(1, 3):
    img=t("animation/end_"+str(i)+".png")
    fin.append(img)
    
perdu=t("animation/game_over.png")

different=["f","h","s"]
anim_possess=[]
for s in different:
    anim_=[]
    for i in range (1,7):
        img=t("animation/possess_"+s+"_"+str(i)+".png",1280,720)
        anim_.append(img)
    anim_possess.append(anim_)

different=["f","h"]
anim_vs_s1=[]
for s in different:
    anim_=[]
    for i in range (1,9):
        img=t("animation/vs_s1_"+s+"_"+str(i)+".png",1280,720)
        anim_.append(img)
    anim_vs_s1.append(anim_)

ws1f=t("animation/win_s1_f.png",1280,720)
ws1h=t("animation/win_s1_h.png",1280,720)
obt_badge=t("animation/obt_badge.png",1280,720)
anim_win_s1=[(ws1f,obt_badge),(ws1h,obt_badge)]

################################################################################################################
collision_acces_vaisseau = (95, 510, 125 - 95, 520-510)
collision_retour_acces_vaisseau = (495, 614, 580-532, 695-622)
collision_decollage =  (563, 371, 699-563, 442-340)
collision_labo = (930, 260, 945-930, 274-260)
collision_retour_moon = (1263,401,1272-1263,431-401)
collision_retour_base = (297,22,353-297,46-22)
collision_incarnation_f = (1189, 373, 50, 25)
collision_incarnation_h = (1189,173,50,25)
collision_incarnation_soldat = (295, 178, 297 - 263, 154-134)
collision_firststep = (974,513,1101-974,631-513)
collision_retour_firststep = (0,342, 24-0, 435-342)
collision_casse_vitre=(533,202,736-533,251-202)
collision_manoir = (562, 8, 686 - 562, 32-8)
collision_retour_manoir = (564,699,645-564,719-699)
collision_entree_manoir = (589,279,624-589,310-279)
collision_sortie_manoir =(555,689,693-555, 718-689)
collision_leparrain=(533,145,709-533, 236-145)
liste_collision_scenario = [(211, 303, 332-211,386-286),
                            (939,315,1088-939,391-315)]
collision_pan_dash = (707,239,772-707,300-239)

liste_collision_moon=[]
trans_moon=[]

liste_collision_first = [(0,488,165-0,712-488),
                                      (425,491,837-425,713-491),
                                      (1109,492,1273-1109,712-492),
                                      (1242,5,1280-1242,476-5),
                                      (0,0,200-0,336-0),
                                      (194,0,492-194,294-0),
                                      (492,0,849-492,205-0),
                                      (849,0,1229-849,288-0),
                                      (172,539,426-172,569-539),#########################" A METTRE EN TRANS
                                      (841,539,426-172,569-539),#######################" PAREIL QUE UNE LIGNE AVANT
                                      (419,200,480-419,315-200),
                                      (0,448,91-0,477-448),
                                      (1184,452,91-0,477-448),
                                      (494,205,527-485,292-199),
                                      (742,205,527-485,292-199),
                                      (790,199,842-790,313-199),
                                      (1162,284,1228-1162,342-284),
                                      (476,439,788-476,487-439)]
trans_first=[]

liste_collision_base = [( 685, 335, 723-685, 693-335),
                                      (811, 55, 865 - 811, 368-55),
                                      (1087,480,1179-1087,559-480),
                                      (19, 306, 200-19, 512- 306),
                                      (817,337,1131-817,411-337),
                                      (1096,608,1167-1096,682-608),
                                      (968,608,1033-968,682-608),
                                      (958,475,1038-958,547-475),
                                      (819,603,897-819,680-603),
                                      (817,481,897-817,552-481),
                                      (677,41,718-677,247-41),
                                      (1096,298,1123-1096,403-298),
                                      (2,701,1270-2,709-701),
                                      (719,99,814-719,124-99),########################",
                                      (1135,109,1225-1135,123-109),
                                      (1230,119,1264-1230,373-119),
                                      (1226,473,1269-1226,689-473),
                                      (856,91,1129-856,159-91),
                                      (870,292,1029-864,313-292),
                                      (1089,136,1133-1089,197-136),
                                      (272,5,712-272,65-5),
                                      (268,6,307-268,244-6),
                                      (589,351,691-581,414-351),
                                      (806,551,856-806,594-551),
                                      (314,333,334-314,570-333),
                                      (318,335,494-318,344-335),
                                      (480,339,492-480,571-339),
                                      (331,547,386-331,558-547),
                                      (316,575,396-309,598-557),
                                      (455,560,495-455,603-560),
                                      (0,0,5-0,695-5)]

trans_base=[(704,274,9,60)]

liste_collision_labo = [(0,2,53,707-2),
                                      (648,413,1273-648,709-413),
                                      (48,4,280-48,117-4),
                                      (356,12,1260-356,125-12),
                                      (52,337,144-52,456-337),
                                      (490,340,642-490,559-340),
                                      (51,689,643-51,707-689),
                                      (197,215,301-197,327-215),
                                      (363,208,457-363,326-208),
                                      (673,165,737-673,196-165),
                                      (875,165,939-875,190-155),
                                      (975,167,1044-975,199-167),
                                      (1075,165,1134-1074,197-165),
                                      (1175,165,742-675,303-269),
                                      (675,266,742-675,303-269),
                                      (773,165,835-773,198-165),
                                      (772,266,845-772,303-269),
                                      (873,266,936-873,303-269),
                                      (973,266,1041-973,303-269),
                                      (1075,266,742-675,303-269),
                                      (1173,266,742-675,303-269),
                                      (1074,368,742-675,303-269),
                                      (1171,368,742-675,303-269),
                                      (674,368,742-675,303-269),
                                      (774,368,742-675,303-269),
                                      (874,368,742-675,303-269),
                                      (974,368,742-675,303-269),
                                      (212,337,483-212,377-337),
                                      (300,381,491-300,561-381),
                                      (212,569,639-212,626-569),
                                      (49,571,162-46,624-571),]


trans_labo=[]

liste_collision_vaisseau = [(0,371,1270-0,419-371),
                                      (363,375,492-363,636-375),
                                      (695,475,858-690,654-419),
                                      (852,375,1263-852,687-375),
                                      (560,615,858-690,654-419),
                                      (495,483,625-495,512-483),
                                      (626,555, 610-532, 695-622),
                                      (497,500, 596-532, 715-622)]
trans_vaisseau=[]

liste_collision_crash = [(0,0,21-0,707-0), ##KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK
                                      (2,707,1268-2,711-699),
                                      (0,0,540-0,22-0),
                                      (691,2,540-0,22-0),
                                      (1254,0,1278-1244,736-28),
                                      (71,110,237-51,216-94),
                                      (983,271,1077-983,287-271),
                                      (1122,275,1220-1122,293-275),
                                      (984,3,987-978,290-3),
                                      (1208,3,1217-1208,283-3)]
trans_crash=[]

liste_collision_manoir = []
trans_manoir = []

liste_collision_intmanoir= []
trans_intmanoir = []
collision_femme = (185, 501, 343-185, 665-501)
collision_champ_magnetique = (128, 451, 400-128, 689-451)
collision_xoford = (642, 321, 744-642,391-321)


liste_scenario = [("La race Transcendant résulte d'experiences scientifiques ","humaines. Ce projet experimental a permis aux spécimens ","concluants d'obtenir des capacités surnaturelles."),
                    ("Par exemple, certains individus peuvent quitter leur corps", "d'origine pour incarner des corps inanimés par un simple contact.","Nous prennons Femmes, Hommes et même enfants pour", "nos experiences.")]

liste_scenario_parrain = [("Que faites vous ici ? Je ne vous ai pas affilié à ce site !","Je vais vous faire payer votre insubordination !","Garde incompétent ! Il parait même que des transcendant "),("s'echappent !")]

liste_nos_pensees = [("Mais... C'est MON CORPS ?!","Que m'arrive-t-il ...?"), ("Mais alors... Je suis une experience ?","Un... Transcendant...?"),("Prendre possesions de corps inanimés ? Je serai capable de ça ?", " Moi ?Alors autant me servir de cette faculté pour m'echapper","d'ici, et trouver qui m'a fait ça !!")]

liste_parole = [("Je devrais pouvoir passer cette porte avec le dash !","(Maj.)"),("Je ne suis pas un garde ! Et je suis un des Transcendant","qui s'est échappé, c'est moi qui vais te faire payer ce que tu m'as fait !","--APPUYEZ P POUR LANCER LE COMBAT FINAL--")]

liste_objectif = [("Explorez la base en interagissant avec les panneaux "), ("Ce Transcendant c'est échappé, trouvez un corps et faites de même !")]
scenario_dash = [('"Porte verrouillée."',"")]
#def collision() :

            #if joueur.rect.colliderect(collision_vaisseau):
                #if joueur.etat =="ombre":
                  #  pygame.draw.rect(fenetre,(47, 6, 70),(40,400,460,280))
                  #  pygame.draw.rect(fenetre,(0,0,0),(40,400,460,280),3)
                  #  pygame.draw.rect(fenetre,(0,0,0),(45,405,450,270),3)
                 #   b(panneau1, 57, 360)
               # else :

                 #   pygame.draw.rect(fenetre,(205,185,116),(20,300,460,180))
                 #   pygame.draw.rect(fenetre,(0,0,0),(20,300,460,180),3)
                 #   pygame.draw.rect(fenetre,(0,0,0),(25,305,450,170),3)
                 #pygame.draw.rect(fenetre, (255,0,0),(collision_vaisseau),3)
                    #blit garde ou animation de garde qui bouge grace a un futur booléen



def choix_collision(col=None):
    global lieu
    if col is None :
        if lieu=="MOON":
            return liste_collision_moon
        if lieu=="FIRST":
            return liste_collision_first
        if lieu == "BASE":
            return liste_collision_base
        if lieu=="LABO":
            return liste_collision_labo
        if lieu == "POSTE_PILOTE":
            return liste_collision_vaisseau
        if lieu == "CRASH":
            return liste_collision_crash
        if lieu == "MANOIR":
            return liste_collision_manoir
        if lieu == "BUREAU":
            return liste_collision_intmanoir

    else :
        if lieu=="MOON":
            return trans_moon
        if lieu=="FIRST":
            return trans_first
        if lieu == "BASE":
            return trans_base
        if lieu=="LABO":
            return trans_labo
        if lieu == "POSTE_PILOTE":
            return trans_vaisseau
        if lieu == "CRASH":
            return trans_crash
        if lieu == "MANOIR":
            return trans_manoir
        if lieu == "BUREAU":
            return trans_intmanoir


# if lieu == "FARM":
        #pygame.draw.rect[.......]


######################################

#################################################################################################################
def rafraichissement():
    """fonction servant a rafraichir la page suivant les actions du jeu"""
    global x,y , indice, lieu, joueur, ordrea, joueur, pensee_0, pensee_1, pensee_2, KOMBAT, KOMBAT_PARRAIN
    fenetre.fill((0,0,0))
    if KOMBAT==False:
        pygame.mixer.music.unpause()
        b(carte, 0,0)
        if lieu == "MOON" :
            if droit_pass == False :
                fenetre.blit(liste_image_fog[int(indice_guidage)%3],(38,403))
            b(xoford[int(indice_x)%4], 662,339)
            b(liste_comet_anim[int(indice_comete)%5],2500-(24*mult_x*indice_comete)%3600,20)
            b(liste_comet_anim[int(indice_comete)%5],1800-(29*mult_x*indice_comete)%2700,100)
            b(liste_diagomet_anim[int(indice_comete)%5],1200-(30*mult_x*indice_comete)%4200,0+(7*mult_y*indice_comete)%977)
            if xoford_text == True:
                if joueur.etat == "ombre":
                    pygame.draw.rect(fenetre,(205,185,116),(20,300,460,180))
                    pygame.draw.rect(fenetre,(0,0,0),(20,300,460,180),3)
                    pygame.draw.rect(fenetre,(0,0,0),(25,305,450,170),3)
                    police= pygame.font.Font(None,45)
                    texte= police.render("Appuyez sur espace pour", True, (0,0,0))
                    fenetre.blit(texte, (40,320))
                    texte= police.render("ecouter vos pensées.", True, (0,0,0))
                    fenetre.blit(texte, (40,360))
                    if pensee_0 == True:
                        pygame.draw.rect(fenetre,(255,255,255),(20,300,460,180))
                        pygame.draw.rect(fenetre,(0,0,0),(20,300,460,180),3)
                        pygame.draw.rect(fenetre,(0,0,0),(25,305,450,170),3)
                        police= pygame.font.Font(None,45)
                        for i in range (len(liste_nos_pensees[0])):
                            texte = police.render(liste_nos_pensees[0][i], True, (0,0,0))
                            fenetre.blit(texte, (34, 320+i*50))

        #b(liste_soldat[int(indice)%5])

        if lieu == "LABO":
            for x_lit in range(660,1256,100) :
                for y_lit in range(150,417,100) :
                    b(lit ,x_lit,y_lit)
            if joueur.etat=="ombre":
                b(filtre_o,joueur.x-1240,joueur.y-680)
            if joueur.etat=="corps":
                b(filtre,joueur.x-1240,joueur.y-680)
            if joueur.etat=="ombre" or sexe=="homme":
                b(femme_morte, 1180, 363)
            if joueur.etat=="ombre" or sexe=="femme":
                b(homme_mort, 1180, 166)
            if lumiere==True:
                b(dessus_labo,0,0)

        if lieu == "BASE":
            if soldat_combat.vivant==True:
                soldat_combat.deplacement_lineaire()
                soldat_combat.affichage()
            else:
                soldat_combat.mort()
            if joueur.etat=="corps":
                b(panneau,708,230)
            if dash_text == True :
                pygame.draw.rect(fenetre,(205,185,116),(171,549,1097-171,700-180))
                pygame.draw.rect(fenetre,(0,0,0),(170,550,930,280),3)
                pygame.draw.rect(fenetre,(0,0,0),(175,555,920,270),3)
                police= pygame.font.Font(None,45)
                for i in range (len(scenario_dash[0])):
                    texte = police.render(scenario_dash[0][i], True, (0,0,0))
                    fenetre.blit(texte, (186, 565+i*45))
                if parole_0 == True :
                    pygame.draw.rect(fenetre,(255,0,0),(171,549,1097-171,700-180))
                    pygame.draw.rect(fenetre,(0,0,0),(170,550,930,280),3)
                    pygame.draw.rect(fenetre,(0,0,0),(175,555,920,270),3)
                    police= pygame.font.Font(None,45)
                    for i in range (len(liste_parole[0])):
                        texte = police.render(liste_parole[0][i], True, (0,0,0))
                        fenetre.blit(texte, (186, 565+i*50))
        if lieu == "FIRST":
            fenetre.blit(liste_pan[int(indice_guidage)%3],(236,323))
            fenetre.blit(liste_pan[int(indice_guidage)%3],(613,207))
            fenetre.blit(liste_pan[int(indice_guidage)%3],(987,319))


            if scenario_1 == True :
                pygame.draw.rect(fenetre,(205,185,116),(171,549,1097-171,700-180))
                pygame.draw.rect(fenetre,(0,0,0),(170,550,930,280),3)
                pygame.draw.rect(fenetre,(0,0,0),(175,555,920,270),3)
                police= pygame.font.Font(None,45)
                for i in range (len(liste_scenario[0])):
                    texte = police.render(liste_scenario[0][i], True, (0,0,0))
                    fenetre.blit(texte, (186, 565+i*50))
                if pensee_1 == True :
                    pygame.draw.rect(fenetre,(255,255,255),(171,549,1097-171,700-180))
                    pygame.draw.rect(fenetre,(0,0,0),(170,550,930,280),3)
                    pygame.draw.rect(fenetre,(0,0,0),(175,555,920,270),3)
                    police= pygame.font.Font(None,45)
                    for i in range (len(liste_nos_pensees[1])):
                        texte = police.render(liste_nos_pensees[1][i], True, (0,0,0))
                        fenetre.blit(texte, (186, 565+i*50))
            if scenario_2 == True :
                pygame.draw.rect(fenetre,(205,185,116),(171,549,1097-171,700-180))
                pygame.draw.rect(fenetre,(0,0,0),(170,550,930,280),3)
                pygame.draw.rect(fenetre,(0,0,0),(175,555,920,270),3)
                police= pygame.font.Font(None,35)
                for i in range (len(liste_scenario[1])):
                    texte = police.render(liste_scenario[1][i], True, (0,0,0))
                    fenetre.blit(texte, (186, 565+i*45))
                if pensee_2 == True :
                    pygame.draw.rect(fenetre,(255,255,255),(171,549,1097-171,700-180))
                    pygame.draw.rect(fenetre,(0,0,0),(170,550,930,280),3)
                    pygame.draw.rect(fenetre,(0,0,0),(175,555,920,270),3)
                    police= pygame.font.Font(None,35)
                    for i in range (len(liste_nos_pensees[2])):
                        texte = police.render(liste_nos_pensees[2][i], True, (0,0,0))
                        fenetre.blit(texte, (186, 565+i*50))

        if lieu == "POSTE_PILOTE":
            b(soldat_mort,753,420 )

        if joueur.etat=="ombre": ##KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK
            fenetre.blit(curseur,(x,y))
        if joueur.etat=="corps":
            b(joueur.sprite[int(joueur.indice)%len(joueur.sprite)],joueur.x,joueur.y)
        #elif joueur.etat=="corps" and joueur.soldat == "soldat":
            #b(joueur.sprite[int(joueur.indice)%4],joueur.x,joueur.y)

        if lieu=="BASE":
            b(dessus_base,0,0)
        if lieu == "CRASH":

            fenetre.blit(images_feu[int(indice_guidage)%5],(24, 222))##KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK COPIE COLLE TT LES FLAMMES STP
            fenetre.blit(images_feu[int(indice_guidage)%5],(58.0, 238.0))
            fenetre.blit(images_feu[int(indice_guidage)%5],(301.0, 134.0))
            fenetre.blit(images_feu[int(indice_guidage)%5],(282.0, 111.0))
            fenetre.blit(images_feu[int(indice_guidage)%5],(270.0, 185.0))
            fenetre.blit(images_feu[int(indice_guidage)%5],(244.0, 127.0))
            fenetre.blit(images_feu[int(indice_guidage)%5],(150.0, 208.0))
            fenetre.blit(images_feu[int(indice_guidage)%5],(208.0, 114.0))
            fenetre.blit(images_feu[int(indice_guidage)%5],(251.0, 252.0))
            fenetre.blit(images_feu[int(indice_guidage)%5],(61.0, 175.0))
            fenetre.blit(images_feu[int(indice_guidage)%5],(64.0, 220.0))
            fenetre.blit(images_feu[int(indice_guidage)%5],(158.0, 270.0))
            fenetre.blit(images_feu[int(indice_guidage)%5],(209.0, 227.0))
            fenetre.blit(images_feu[int(indice_guidage)%5],(104.0, 256.0))
            fenetre.blit(images_feu[int(indice_guidage)%5],(56.0, 267.0))
            fenetre.blit(images_feu[int(indice_guidage)%5],(247.0, 137.0))
            b(open_gate, 510,9)
            #KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK
        if lieu == "BUREAU":
            if dialogue_leparrain == True :
                pygame.draw.rect(fenetre,(205,185,116),(171,549,1097-171,700-180))
                pygame.draw.rect(fenetre,(0,0,0),(170,550,930,280),3)
                pygame.draw.rect(fenetre,(0,0,0),(175,555,920,270),3)
                police= pygame.font.Font(None,45)
                for i in range (len(liste_scenario_parrain[0])):
                        texte = police.render(liste_scenario_parrain[0][i], True, (0,0,0))
                        fenetre.blit(texte, (186, 565+i*45))
                if parole_1 == True :
                    pygame.draw.rect(fenetre,(255,0,0),(171,549,1097-171,700-180))
                    pygame.draw.rect(fenetre,(0,0,0),(170,550,930,280),3)
                    pygame.draw.rect(fenetre,(0,0,0),(175,555,920,270),3)
                    police= pygame.font.Font(None,45)
                    for i in range (len(liste_parole[1])):
                        texte = police.render(liste_parole[1][i], True, (0,0,0))
                        fenetre.blit(texte, (186, 565+i*50))

    else:
        if lieu=="BASE":
            b(kombat_labo, 0,0)
        else:
            b(kombat_parrain, 0,0)
        fenetre.blit(combattant.sprite[combattant.sens][int(combattant.indice%len(combattant.sprite[combattant.sens]))],(combattant.x+105-105*combattant.sens,combattant.y))
        fenetre.blit(adversaire.perso.sprite[adversaire.perso.sens][int(adversaire.perso.indice%len(adversaire.perso.sprite[adversaire.perso.sens]))],(adversaire.perso.x+105-105*adversaire.perso.sens,adversaire.perso.y))
        pygame.draw.rect(fenetre,(43,43,43),(40,60,500,30))
        pygame.draw.rect(fenetre,(43,43,43),(735,60,500,30))
        for i in range (int(combattant.hp/combattant.pv_totaux*100)):
            pygame.draw.rect(fenetre,(255,0,0),(40+i*5+5*(100-int(combattant.hp/combattant.pv_totaux*100)),60,5,30))
        for i in range(int(combattant.energy)):
            e = pygame.Surface((10,8),pygame.SRCALPHA)
            pygame.draw.rect(e,(230,230,230,190),e.get_rect())
            fenetre.blit(e,(40+i*10,690))
        if combattant.energy==20:
            pygame.draw.circle(fenetre,(220,220,220),(250,694),5)

        for i in range (int(adversaire.perso.hp/adversaire.perso.pv_totaux*100)):
            pygame.draw.rect(fenetre,(255,0,0),(735+i*5,60,5,30))
        for i in range(int(adversaire.perso.energy)):
            e = pygame.Surface((10,8),pygame.SRCALPHA)
            pygame.draw.rect(e,(230,230,230,190),e.get_rect())
            fenetre.blit(e,(1040+i*10+(20-int(adversaire.perso.energy))*10,690))
        if adversaire.perso.energy==20:
            pygame.draw.circle(fenetre,(220,220,220),(1030,694),5)

        pygame.draw.rect(fenetre,(170,170,170),(40,60,500,30),3)
        pygame.draw.rect(fenetre,(170,170,170),(735,60,500,30),3)
        fenetre.blit(KO,(530,20))
        fenetre.blit(energy_icon,(0,665))
        fenetre.blit(energy_icon,(1240,665))

    if KOMBAT== True :
        b(touches_kombat, 10, 100)
    if joueur.etat == "corps" and KOMBAT== False :
        b(guidage, 20,20)
    if joueur.etat == "ombre" and resume== False:
        b(guidage_ombre, 20,20)


    if resume==True:
            b(pause,230,100)
            fenetre.blit(curseur_p,(x,y))

    if KOMBAT==False and joueur.etat=="ombre":
        b(joueur.sprite[int(joueur.indice)%3],joueur.x,joueur.y)
    pygame.display.update()





###################################################################################################################
clock = pygame.time.Clock()

stop = False

while not stop:

    for event in pygame.event.get():#la boucle de travail se lance et on surveille tous les événements : souris, clavier...
        if event.type == pygame.QUIT: #si on clique sur la croix en haut de la fenêtre, on sort de la boucle
            stop = True

        if event.type== MOUSEMOTION: #on suit le mouvement de la souris pour deplacer les palets pris
            x,y=event.pos

        if event.type == KEYUP :
            if event.key==K_ESCAPE:
                resume= not resume
            if event.key==K_c:##############KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK
                print(joueur.x,joueur.y)

        if event.type == MOUSEBUTTONUP and resume==True:
                print(x, y)
                if 335<x<943 and 265<y<391:
                    resume=False
                if 335<x<943 and 432<y<557:
                    stop=True

        if resume==False:
            if KOMBAT==False:
                if event.type == MOUSEBUTTONUP :
                    print(x, y)
                    if taille[0]-35<x<taille[0]-5 and 5<y<35:
                        stop=True
                    if event.button==3 and ombre==True:
                        joueur.acceleration+=1.5
                        #dash_sound.play()
                if event.type in (KEYUP, KEYDOWN) :
                    if joueur.etat=="corps":
                        joueur.dpl_corps(event.key,event.type)
                    joueur.interaction(event.key,event.type)


            else:
                 if event.type in (KEYUP, KEYDOWN):
                    combattant.touches_J1(event.type,event.key)

    if KOMBAT==False:
        joueur.update(x,y)
    if start_k==True:
        combattant=Personnage_vs(sexe, pv, degats, vitesses,mult, cost, 50,100,rectangles)
        if lieu=="BASE":
            adversaire = IA("soldat",pv, degats, vitesses, 850,100)
            animation("vs_s1")
        else:
            adversaire = IA("parrain",pv, degats, vitesses, 850,100)
            for i in range (2):
                animation("ecran_noir")
        indice_perso_ia = 0
        KOMBAT=True
        start_k=False

    if KOMBAT==True:
        sens(combattant,adversaire.perso)
        combattant.update(adversaire.perso)
        adversaire.update(combattant)
        if adversaire.perso.hp<=0 and tps is None or combattant.hp<=0 and tps is None:
                tps=time.time()
        if tps is not None and time.time()-tps>=1.5:
            if adversaire.perso.hp<=0:
                if lieu=="BASE":
                    animation("win_vs_s1")
                    soldat_combat.vivant=False
                else:
                    animation("fin")
                    animation("ecran_noir")
                    stop=True
            else:
                animation("perdu")
                stop=True
            joueur.droite=joueur.gauche=joueur.haut=joueur.bas=joueur.run=joueur.dash=False
            tps=None
            KOMBAT=False
    if lieu == "BASE":
        indice_base+=0.23
    if lieu == "MOON":
        indice_guidage+=0.15
        indice_comete+=0.15
        indice_x+=0.1
    if lieu == "FIRST":
        indice_guidage+=0.15
    if lieu == "CRASH":
        indice_guidage+=0.15

    map_actuelle()
    rafraichissement()
    clock.tick(60)

pygame.quit()


"""
        elif self.etat=="ombre":
            self.soldat = "soldat"
            self.d=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/soldat/s1_h"+str(i)+".png",38*2.3,33*2.3)
                    self.h.append(img)
                    i+=1
                except:
                    i=0

            self.b=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/soldat/s1_b"+str(i)+".png",38*2.3,33*2.3)
                    self.b.append(img)
                    i+=1
                except:
                    i=0


            self.g=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/soldat/s1_g"+str(i)+".png",38*2.3,33*2.3)
                    self.g.append(img)
                    i+=1
                except:
                    i=0

            self.d=[]
            i=1
            while i!=0:
                try:
                    img=t("personnages/soldat/s1_d"+str(i)+".png",38*2.3,33*2.3)
                    self.d.append(img)
                    i+=1
                except:
                    i=0


            self.sprite_direction=(self.b,self.rb,self.db)
            self.sprite= self.b
"""



