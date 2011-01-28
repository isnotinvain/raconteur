'''
Created on Jan 27, 2011

@author: Alex Levenson (alex@isnotinvain.com)
'''
import pygame
class ProgressWindow(object):
    
    def __init__(self,name,size=(800,25)):
        pygame.init()
        self.name = name
        self.size = size
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption(name)
        self.progress = 0.0
        self.rect = pygame.Rect(0,0,0,size[1])
        
        self.font = pygame.font.Font(None, 25)
        self.quit = False
                
    def set_progress(self,progress):
        if progress < 0: progress = 0.0
        if progress > 1: progress = 1.0
        self.progress = progress
        self.rect.width = self.size[0] * progress
    
    def get_quit(self):
        return self.quit
    
    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
        
        text = self.font.render(str(int(self.progress*100))+"%", True, (255,255, 255), (159, 182, 205))
        textRect = text.get_rect()
        textRect.centerx = self.screen.get_rect().centerx
        textRect.centery = self.screen.get_rect().centery        

        self.screen.fill((255,255,255))
        pygame.draw.rect(self.screen,(0,255,0),self.rect)
        self.screen.blit(text, textRect)
        pygame.display.flip()