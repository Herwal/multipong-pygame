# -*- coding: utf-8 -*-

import pygame as pg
from pygame.locals import (K_LEFT, K_RIGHT, K_SPACE)
import random as rd

# Initialiserer/starter pygame
pg.init()

# Oppretter et vindu der vi skal "tegne" innholdet vårt
VINDU_BREDDE = 800
VINDU_HOYDE  = 500
vindu = pg.display.set_mode([VINDU_BREDDE, VINDU_HOYDE])
font = pg.font.SysFont("Arial", 40) 

class Spill:
    """
    Klasse for å representere spillet
    """
    def __init__(self, farge, vindusobjekt):
        self.farge = farge
        self.vindusobjekt = vindusobjekt

    def Farge(r, g, b):
        return r, g, b

class Klosse(Spill):
    def __init__(self, x, y, farge, xFart, yFart, vindusobjekt, bredd, høgd):
        super().__init__(farge, vindusobjekt)
        self.x = x
        self.y = y
        self.xFart = xFart
        self.yFart = yFart
        self.bredd = bredd
        self.høgd = høgd
        self.rect = pg.Rect(self.x, self.y, self.bredd, self.høgd)
        
    def tegn(self):
      """
      Metode for å tegne klossen

      vindusobjekt: vindus størrelsen
      farge: rgb
      rect: pygame rektangel objekt
      """
      pg.draw.rect(self.vindusobjekt, self.farge, self.rect)

    def flytt(self, padde):
        """
        Metode for å flytte det firkanta hinderet
        styrer kollisjon mellom veggane, taket og botnen av vinduet og spiller objektet

        x og y er int koordinatar for posisjonen i vinduet
        xFart og yFart er int hastigheten objektet beveger seg med
        """
        
        # Flytter objektet
        self.x += self.xFart
        self.y += self.yFart
        self.rect.x = self.x
        self.rect.y = self.y
        
        # Sjekker om objektet er utenfor høyre/venstre vegg
        if ((self.x) <= 0) or ((self.x + self.bredd) >= self.vindusobjekt.get_width()):
          self.xFart = -self.xFart
          self.rect.x = self.x

        # Sjekker om objektet treffer taket eller golvet 
        if ((self.y) <= 0) or ((self.y + self.høgd) >= self.vindusobjekt.get_height()):
            self.yFart = -self.yFart
            self.rect.y = self.y
            
        if self.rect.colliderect(padde.rect):
            self.yFart = -self.yFart 
            treff = "treff"

        else:
            treff = "0"

        return treff

class Padde(Spill):
    """
    Klasse for å representere spiller objektet, en rektangulær padde

    x, y er int koordinater for paddens lokasjon i vinduet
    bredd og høgd er int verdiar for paddens areal
    fart er int verdien for paddens sidelangs bevegelse
    rect er paddens pygame rect objekt for kollisjon 
    """
    def __init__(self, x, y, bredd, høgd, farge, vindusobjekt):
        super().__init__(farge, vindusobjekt)
        self.x = x
        self.y = y
        self.bredd = bredd
        self.høgd = høgd
        self.fart = 0.1
        self.rect = pg.Rect(self.x, self.y, self.bredd, self.høgd)
        
    def tegn(self):
      """Metode for å tegne ballen"""
      pg.draw.rect(self.vindusobjekt, self.farge, self.rect)
        
    def flytt(self, taster):
        """Metode for å flytte padda"""
        if taster[K_LEFT]:
             self.x -= self.fart
             self.rect.x = self.x
             self.rect.y = self.y
             self.rect.width = self.bredd
             self.rect.height = self.høgd
             
        if taster[K_RIGHT]:
             self.x += self.fart
             self.rect.x = self.x
             self.rect.y = self.y
             self.rect.width = self.bredd
             self.rect.height = self.høgd
 
        if (self.x <= 0):
            self.x += self.fart
            self.rect.y = self.y
            self.rect.x = self.x
            self.rect.width = self.bredd
            self.rect.height = self.høgd
            
        if ((self.x + self.bredd) >= self.vindusobjekt.get_width()):
          self.x -= self.fart
          self.rect.x = self.x
          self.rect.y = self.y
          self.rect.width = self.bredd
          self.rect.height = self.høgd

def nyBall(vindu):  # Lag ny ball med tilfeldig oppsett:
    x = rd.randint(0, int(VINDU_BREDDE-100))
    y = rd.randint(0, int(VINDU_HOYDE/3))
    farge = Spill.Farge(0, 0, 255)
    return Klosse(x, y, farge, 0.05, 0.05, vindu, 20, 20)

# Lager et Ball-objekt
baller = []
baller.append(nyBall(vindu))

farge = Spill.Farge(255, 0, 0)
padde1 = Padde((VINDU_BREDDE/3 + 100), (VINDU_HOYDE - 60), 100, 20, farge, vindu)

# Gjenta helt til brukeren lukker vinduet
fortsett = True
game_over = False
while fortsett:
    
    # Sjekker om brukeren har lukket vinduet
    for event in pg.event.get():
        if event.type == pg.QUIT:
            fortsett = False
    
    # Farger bakgrunnen svart
    vindu.fill((0, 0, 0))
    
    # Henter en ordbok med status for alle tastatur-taster
    trykkede_taster = pg.key.get_pressed()

    # Tegner og flytter ballene
    padde1.tegn()
    padde1.flytt(trykkede_taster)
    
    for b in baller:
        b.tegn()
        treff = b.flytt(padde1)

        if treff == "treff":
            ny_ball = nyBall(vindu)
            baller.append(ny_ball)
            treff = "0"
        if b.rect.y + b.høgd >= VINDU_HOYDE:
            game_over = True

    if game_over:
        tekst = font.render("Game Over", True, (255, 255, 255))
        vindu.blit(tekst, (VINDU_BREDDE // 2 - tekst.get_width() // 2,
                            VINDU_HOYDE // 2 - tekst.get_height() // 2)
                    )
        tekst2 = font.render("Press space to restart", True, (255, 255, 255))
        vindu.blit(tekst2, (VINDU_BREDDE // 2 - tekst.get_width() // 2 - 70,
                            VINDU_HOYDE // 2 - tekst.get_height() // 2 - 50)
                    )
        pg.display.flip()
        baller = []

    if trykkede_taster[K_SPACE]:
        game_over = False
        baller = [nyBall(vindu)]
        padde1 = Padde((VINDU_BREDDE/3 - 20), (VINDU_HOYDE - 60), 100, 20, farge, vindu)

    # Oppdaterer alt innholdet i vinduet
    pg.display.flip()

# Avslutter pygame
pg.quit()
