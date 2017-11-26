#!/usr/bin/env python
from __future__ import division
import pygame
import time
import random 
import cctalk

mech=cctalk.Coin()

if not mech.connect_mech() :
    print "Coin mech not found"

pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()

screen = pygame.display.set_mode((1024, 768),pygame.HWSURFACE)
background = pygame.image.load('./graphics/background.png').convert()
font=pygame.font.Font("./graphics/segment.ttf",30)
screen.blit(background, (0, 0)) 
pygame.display.flip()
clock = pygame.time.Clock() # Create a clock object
FPS = 60

class Sounds () :
    """This will simply load sounds from config
       and provide play facility for other classes """
       
    def __init__(self) :
        
        self.win_snd = pygame.mixer.Sound("./sounds/win.wav")
        self.spin_snd = pygame.mixer.Sound("./sounds/spin.wav")
        self.stop_snd = pygame.mixer.Sound("./sounds/stop.wav")
        self.coin_snd = pygame.mixer.Sound("./sounds/coin.wav")
        self.music_playing = 0
        pygame.mixer.music.load("./sounds/blues.mid")
        pygame.mixer.music.set_volume(0.1)

        
    def win (self) :
        self.win_snd.play()

    def spin (self) :
        self.spin_snd.play()

    def stop (self) :
        self.stop_snd.play()

    def coin (self) :
        self.coin_snd.play()

    def start_bgm (self) :
        if self.music_playing == 0 :
            pygame.mixer.music.play(-1)
            self.music_playing = 1

    def stop_bgm (self) :
        pygame.mixer.music.stop()
        self.music_playing = 0

            
class Reels () :
    """
    This will setup a reel and track position and draw
    Symbols displayed in window must be 3 
    """ 

    def __init__(self):
        """
        I will load a config file here to sort reels out at some stage
        """
        self.number_of_reels = 2
        self.y_pos = []
        self.default_x = 100
        self.default_y = 100
        self.symbol_width = 150
        self.symbol_height = 150
        self.gap = 2 #this is space between reel bands

        self.velocity = 50

        self.reel_layout = []
        self.reel_bands = []
        self.reel_images = []

        self.reel_layout.append([3,0,2,0,4,0,2,0,1,0,2,0,2,0,2,0,1,0,2,0,1,0,2,0])
        self.reel_layout.append([2,0,3,0,1,0,3,0,3,0,1,0,3,0,4,0,1,0,3,0,1,0,1,0])

        self.reel_images.append(pygame.image.load("./graphics/blank.png").convert())
        self.reel_images.append(pygame.image.load("./graphics/club.png").convert())      
        self.reel_images.append(pygame.image.load("./graphics/heart.png").convert())     
        self.reel_images.append(pygame.image.load("./graphics/spade.png").convert())  
        self.reel_images.append(pygame.image.load("./graphics/diamond.png").convert()) 

        for i in range(0,self.number_of_reels) :

          self.y_pos.append(0)
          self.reel_bands.append(pygame.image.load("./graphics/reel.png").convert())
          self.reel_bands[i].blit(self.reel_images[self.reel_layout[i][len(self.reel_layout[i])-1]],(0,0) ,(0,0,self.symbol_width,self.symbol_height))

          for ri in range(0,len(self.reel_layout[i])) :
            self.reel_bands[i].blit(self.reel_images[self.reel_layout[i][ri]],(0,(ri*self.symbol_height)+self.symbol_height) ,(0,0,self.symbol_width,self.symbol_height))

          self.reel_bands[i].blit(self.reel_images[self.reel_layout[i][0]],(0,(len(self.reel_layout[i])+1)*self.symbol_height) ,(0,0,self.symbol_width,self.symbol_height))
          self.reel_bands[i].blit(self.reel_images[self.reel_layout[i][1]],(0,(len(self.reel_layout[i])+2)*self.symbol_height) ,(0,0,self.symbol_width,self.symbol_height))

        for i in range(0,self.number_of_reels) :
            screen.blit( self.reel_bands[i], (i*(self.symbol_width+self.gap)+self.default_x, self.default_y), (0, 0, self.symbol_width,self.symbol_height*3) )
            pygame.display.update( pygame.Rect(i*(self.symbol_width+self.gap)+self.default_x,self.default_y, self.symbol_width, self.symbol_height*3) )       

    def get_number_reels(self) :
        return self.number_of_reels
        
    def spin(self) :
        finished = 0
        stopped = []
        moves = []
        ret_info = []
        stops = []
        for i in range(0,self.number_of_reels) :
          stopped.append(0)
          moves.append(0)
          stops.append(random.randint(0,23))
        while 1 :

          for ri in range(0,self.number_of_reels) :

            screen.blit(self.reel_bands[ri], (ri*(self.symbol_width+self.gap)+self.default_x, self.default_y), (0, self.y_pos[ri],self.symbol_width,self.symbol_height*3 ) )
            pygame.display.update(pygame.Rect(ri*(self.symbol_width+self.gap)+self.default_x,self.default_y, self.symbol_width,self.symbol_height*3) )

            if (abs(self.y_pos[ri] - stops[ri]*self.symbol_height))<self.velocity and stopped[ri]==0 and moves[ri]>8 : ###rework minumum moves please

              if (stopped[ri-1]==1) or ri==0 :
                self.y_pos[ri] = stops[ri]*self.symbol_height
                screen.blit(self.reel_bands[ri], (ri*(self.symbol_width+self.gap)+self.default_x, self.default_y), (0, self.y_pos[ri],self.symbol_width,self.symbol_height*3 ) )
                pygame.display.update(pygame.Rect(ri*(self.symbol_width+self.gap)+self.default_x,self.default_y,self.symbol_width,self.symbol_height*3) )
                stopped[ri]=1
                finished+=1
                sound.stop()######might need to clean this up
                moves[ri]=0

            diff=abs(self.y_pos[ri] -0 )
            if (abs(self.y_pos[ri]- 0))<self.velocity :
              self.y_pos[ri]=len(self.reel_layout[ri])*self.symbol_height
            clock.tick(FPS)
            if (stopped[ri]==0) :
              self.y_pos[ri]-=self.velocity
              moves[ri]+=self.velocity/self.symbol_height  #counting the number of symbols moved to help control reel spin 
          if (finished == self.number_of_reels) :
             for i in range(0,self.number_of_reels) : 
               ret_info.append(self.reel_layout[i][stops[i]])
             return ret_info

class Math () :
    def __init__(self) :
        
        self.wins = [(5,[4,4]),
	                 (2,[2,2]),
	                 (1,[1,1]),
                     (3,[3,3])]
        self.bank = 0
        self.credit = 0.00
        self.pop=0.1
        """
        I will be re designing credit and bank display and loading settings here"""
        

    def check_win (self,payline) :
        for i in range(0,len(self.wins)):
            if self.wins[i][1] == payline:
                self.bank+=self.wins[i][0]
                sound.win()
                self.update_bank()

    def update_bank (self) :

        display=font.render("CREDIT "+str(self.credit)+"0  BANK "+str(self.bank)+".00",True,(0,191,255))
        screen.blit(background, (630,345), (630, 345,350,80 ) )
        screen.blit(display, [640, 360])
        pygame.display.update(pygame.Rect(640,360, 350,80))
        
    def add_credit (self,credit) :
        if (credit>0) :
          self.credit+=credit
          self.credit=round(self.credit,2)
          sound.coin()
          sound.start_bgm()
        self.update_bank()

    def charge_spin(self) :
        self.credit-=self.pop
        self.credit=round(self.credit,2)
        self.update_bank()
        if self.credit<self.pop :
            sound.stop_bgm()

def game_loop () :
    done = False
    while not done:
            math.add_credit(mech.get_credit())
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            mech.stop_accepting()
                            done = True

                    if event.type == pygame.KEYDOWN :

                      if event.key == pygame.K_ESCAPE :
                        mech.stop_accepting()
                        done = True

                      if event.key == pygame.K_1 :
                        math.add_credit(0.10)

                      if event.key == pygame.K_SPACE :
                        if(math.credit>=math.pop) :
                          sound.spin()
                          math.charge_spin()
                          math.check_win(my_reels.spin())
                          
sound=Sounds()
my_reels=Reels()
math=Math()
game_loop()
