# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 13:52:55 2023

@author: Hermann and Jonathan and Christiano
"""

import pygame as pg
import math as m
import random as rd

# Initialiserer/starter pygame
pg.init()

# Oppretter et vindu der vi skal "tegne" innholdet vårt
VINDU_BREDDE = 700
VINDU_HOYDE = 700
vindu = pg.display.set_mode([VINDU_BREDDE, VINDU_HOYDE])
pg.display.set_caption("Rock Paper Scissors")
font = pg.font.SysFont("Arial", 40)


# Lager overklasse for ball objekter
class Ball:
    """Klasse for å representere ball objekter
    Inneheld x posisjon, y posisjon og radius
    Har også ulike metoder for korleis objekta skal oppføre seg
    """

    def __init__(self, x, y, radius, vindusobjekt):
        """Konstruktør"""
        self.x = x
        self.y = y
        self.radius = radius
        self.vindusobjekt = vindusobjekt

    def tegn(self):
        """Metode for å tegne steinen innanfor vindauget"""
        self.vindusobjekt.blit(self.img, (self.x - self.radius, self.y - self.radius))

    def finnAvstand(self, annanBall):
        """Metode for å regne ut avstand mellom 2 baller og returnerer den"""
        xAvstand = (self.x - annanBall.x) ** 2  # Finner x avstand
        yAvstand = (self.y - annanBall.y) ** 2  # Finner y avstand
        sentrumavstand = m.sqrt(xAvstand + yAvstand)

        radiuser = self.radius + annanBall.radius

        avstand = sentrumavstand - radiuser

        return avstand

    def forandre(self, obj):
        """Metode for å forandre objektet til eit anna objekt i spelet"""
        if self.finnAvstand(obj) <= 0:
            self.xFart = -self.xFart
            self.yFart = -self.yFart
            obj.xFart = -obj.xFart
            obj.yFart = -obj.yFart
            return True

    def flytt(self):
        """Metode for å flytte hinderet på vindauget, sjekker kollisjon mot kantane av vindauget"""
        # Sjekker høgre og venstre side
        if ((self.x - self.radius) <= 0) or (
            (self.x + self.radius) >= self.vindusobjekt.get_width()
        ):
            self.xFart = -self.xFart

        # Sjekker topp og botn
        if ((self.y - self.radius) <= 70) or (
            (self.y + self.radius) >= self.vindusobjekt.get_height()
        ):
            self.yFart = -self.yFart

        # Flytter hinderet
        self.x += self.xFart
        self.y += self.yFart


# Lager underklasser som arver fra ball
class Stein(Ball):
    """Klasse for å representere steinar, arvar frå ball klassa og har attributa
    xFart og yFart, og bilde som representerer objektet
    """

    def __init__(self, x, y, radius, img_file, vindusobjekt, xFart, yFart):
        super().__init__(x, y, radius, vindusobjekt)
        self.xFart = xFart
        self.yFart = yFart
        self.img = pg.image.load("stein.png")  # Load the image file
        self.img = pg.transform.scale(self.img, (2 * radius, 2 * radius))


class Saks(Ball):
    """Klasse for å representere sakser, arvar frå ball klassa og har attributa
    xFart og yFart, og bilde som representerer objektet
    """

    def __init__(self, x, y, radius, img_file, vindusobjekt, xFart, yFart):
        super().__init__(x, y, radius, vindusobjekt)
        self.xFart = xFart
        self.yFart = yFart
        self.img = pg.image.load("saks.png")  # Load the image file
        self.img = pg.transform.scale(self.img, (2 * radius, 2 * radius))


class Papir(Ball):
    """Klasse for å representere papir, arvar frå ball klassa og har attributa
    xFart og yFart, og bilde som representerer objektet
    """

    def __init__(self, x, y, radius, img_file, vindusobjekt, xFart, yFart):
        super().__init__(x, y, radius, vindusobjekt)
        self.xFart = xFart
        self.yFart = yFart
        self.img = pg.image.load("papir.png")  # Load the image file
        self.img = pg.transform.scale(self.img, (2 * radius, 2 * radius))


# Lager grupper for å halde objekta
stein_gruppe = []
saks_gruppe = []
papir_gruppe = []
x_pos = []
y_pos = []


# Sjekker avstand for unike plasseringar
def avstand(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


while len(x_pos) != 30:
    vx = 0.15
    vy = 0.15
    x = rd.randint(20, 680)
    y = rd.randint(90, 680)

    unik_pos = True
    for j in range(len(x_pos)):
        if avstand(x, y, x_pos[j], y_pos[j]) < 2 * 10:
            unik_pos = False
            break

    if unik_pos:
        x_pos.append(x)
        y_pos.append(y)

# lager alle objekta ved start
for i in range(10):
    stein = Stein(x_pos[i], y_pos[i], 20, ("stein.png"), vindu, vx, vy)
    stein_gruppe.append(stein)

    saks = Saks(x_pos[i + 10], y_pos[i + 10], 20, ("saks.png"), vindu, vx, vy)
    saks_gruppe.append(saks)

    papir = Papir(x_pos[i + 20], y_pos[i + 20], 20, ("papir.png"), vindu, vx, vy)
    papir_gruppe.append(papir)


# Gjenta helt til brukeren lukker vinduet
fortsett = True
while fortsett:
    # Sjekker om brukeren har lukket vinduet
    for event in pg.event.get():
        if event.type == pg.QUIT:
            fortsett = False

    # Farger bakgrunnen kvit
    vindu.fill((255, 255, 255))
    # Lager ein svart bar på toppen av skjermen
    pg.draw.rect(vindu, (0, 0, 0), (0, 0, VINDU_BREDDE, 70))

    # Kjører til nokon vinner
    if len(stein_gruppe) < 30 or len(papir_gruppe) < 30 or len(saks_gruppe) < 30:
        tittel = "Stein Saks Papir!"
        tekst = font.render(tittel, True, (255, 255, 255))
        vindu.blit(tekst, (225, 15))

    # Lager ein vinnar tekst notifikasjon
    if len(stein_gruppe) == 30:
        vinnar = "STEIN KNUSTE ALLE"
        tekst = font.render(vinnar, True, (128, 128, 128))
        vindu.blit(tekst, (200, 80))
    elif len(papir_gruppe) == 30:
        vinnar = "PAPIR KVELTE ALLE"
        tekst = font.render(vinnar, True, (255, 255, 0))
        vindu.blit(tekst, (200, 80))
    elif len(saks_gruppe) == 30:
        vinnar = "SAKS KUTTET ALLE"
        tekst = font.render(vinnar, True, (255, 0, 0))
        vindu.blit(tekst, (200, 80))

    # Tegner og flytter alle objekta
    for stein in stein_gruppe:
        stein.tegn()
        stein.flytt()

    for papir in papir_gruppe:
        papir.tegn()
        papir.flytt()

    for saks in saks_gruppe:
        saks.tegn()
        saks.flytt()

    # Styrer kollisjonen for stein
    for stein in stein_gruppe:
        for papir in papir_gruppe:
            if stein.forandre(papir) == True:
                ny_papir = Papir(
                    stein.x, stein.y, 20, (0, 0, 255), vindu, stein.xFart, stein.yFart
                )
                papir_gruppe.append(ny_papir)
                for i, o in enumerate(stein_gruppe):
                    if o.x == stein.x and o.y == stein.y:
                        del stein_gruppe[i]
                        print("stein: ", len(stein_gruppe))
                        pass
                    pass
                break

    # Styrer kollisjonen for papir
    for papir in papir_gruppe:
        for saks in saks_gruppe:
            if papir.forandre(saks) == True:
                ny_saks = Saks(
                    papir.x, papir.y, 20, (255, 0, 0), vindu, papir.xFart, papir.yFart
                )
                saks_gruppe.append(ny_saks)
                for i, o in enumerate(papir_gruppe):
                    if o.x == papir.x and o.y == papir.y:
                        del papir_gruppe[i]
                        print("papir: ", len(papir_gruppe))
                        pass
                    pass
                break

    # Styrer kollisjonen for saks
    for saks in saks_gruppe:
        for stein in stein_gruppe:
            if saks.forandre(stein) == True:
                ny_stein = Stein(
                    saks.x, saks.y, 20, (128, 128, 128), vindu, saks.xFart, saks.yFart
                )
                stein_gruppe.append(ny_stein)
                for i, o in enumerate(saks_gruppe):
                    if o.x == saks.x and o.y == saks.y:
                        del saks_gruppe[i]
                        print("saks: ", len(saks_gruppe))
                        pass
                    pass
                break

    # Oppdaterer alt innholdet i vinduet
    pg.display.flip()

# Avslutter pygame
pg.quit()
