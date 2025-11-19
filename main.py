#!/usr/bin/env python3
"""
main_turtle.py - 8 klickbare Bits mit turtle (kein pygame)

- Acht große 0/1 horizontal zentriert
- Unter jeder Ziffer eine kurze senkrechte Linie (Stummel)
- Klick auf eine Ziffer toggelt das Bit (0 <-> 1) und aktualisiert "Dezimalwert:"
- Start: python main_turtle.py
"""
import turtle
import random

# --- Konfiguration ---
N_BITS = 8
WINDOW_W, WINDOW_H = 1000, 600
TITLE_Y = 160
DIGIT_Y = 0
DIGIT_FONT = ("Arial", 72, "bold")    # große Ziffern
TITLE_FONT = ("Arial", 36, "bold")
STUMP_WIDTH = 14
DIGIT_HIT_W = 110    # Hitbox-Breite um die Ziffer
DIGIT_HIT_H = 120    # Hitbox-Höhe um die Ziffer
BG_COLOR = "black"
STUMP_COLOR_ACTIVE = "#fca139"
STUMP_COLOR_INACTIVE = "#a68046"

# --- Setup ---
screen = turtle.Screen()
screen.setup(WINDOW_W, WINDOW_H)
screen.title("Bits - Klick zum Umschalten")
screen.bgcolor(BG_COLOR)
screen.tracer(0)  # manuelles update für sauberes Redraw
screen.bgpic("files/img/background.png")

drawer = turtle.Turtle(visible=False)
drawer.penup()
drawer.speed(0)

random_pairs = []
for i in range(N_BITS):
    randomInt1 = random.randint(-40, 40)
    randomInt2 = random.randint(-40, 40)
    random_pairs.append((randomInt1, randomInt2))

# initial bits (alle 0)
bits = [0] * N_BITS

# berechne x-positionen zentriert
total_width = WINDOW_W * 0.75  # belegter Bereich für die Bits
start_x = - total_width / 2
if N_BITS > 1:
    spacing = total_width / (N_BITS - 1)
else:
    spacing = 0
bit_positions = [start_x + i * spacing for i in range(N_BITS)]

# mit Spielmodus erweitern
playmode = False
randomDecimal = None

# Spielmodus-Button Position und Groesse
BTN_X1, BTN_Y1 = WINDOW_W/2 - 240, WINDOW_H/2 - 40   # oben links
BTN_X2, BTN_Y2 = WINDOW_W/2 - 40, WINDOW_H/2 - 100     # unten rechts


def bits_to_decimal(b):
    # b[0] ist MSB (links)
    val = 0
    n = len(b)
    for i, bit in enumerate(b):
        val += bit << (n - 1 - i)
    return val


def draw_all():
    drawer.clear()
    # Titel
    # --- Hintergrundbox für Dezimalwert ---
    drawer.goto(0, TITLE_Y)

    # Grösse der Box (breite an Text angepasst)
    box_width = 450
    box_height = 60

    # Rechteck zeichnen
    drawer.penup()
    drawer.goto(-box_width / 2 - 10, TITLE_Y + 10)  # oben links der Box
    drawer.pendown()
    drawer.pencolor("black")
    drawer.fillcolor("#017944")
    drawer.pensize(5)
    drawer.begin_fill()
    for _ in range(2):
        drawer.forward(box_width)
        drawer.right(90)
        drawer.forward(box_height)
        drawer.right(90)
    drawer.end_fill()
    drawer.penup()

    # Text darüber schreiben
    drawer.goto(0, TITLE_Y - box_height / 2 - 5)
    drawer.pencolor("black")
    if playmode:
        if bits_to_decimal(bits) == randomDecimal:
            drawer.pencolor("red")
            screen.ontimer(regenerate_random, 2000)
        drawer.write(f"Dezimalwert:{randomDecimal}", align="center", font=TITLE_FONT)
    else:
        drawer.write(f"Dezimalwert:{bits_to_decimal(bits)}", align="center", font=TITLE_FONT)

    # Zeichne Ziffern und Stummel
    for i, x in enumerate(bit_positions):
        y = DIGIT_Y
        # Ziffer
        drawer.goto(x, y - (DIGIT_FONT[1] // 3))  # leicht zentriert, weil write an der Basis ausrichtet
        if bits[i] == 1:
            drawer.pencolor(STUMP_COLOR_ACTIVE)
        else:
            drawer.pencolor(STUMP_COLOR_INACTIVE)
        drawer.write(str(bits[i]), align="center", font=DIGIT_FONT)

        # Stummel unter der Ziffer
        stump_x = x
        # stump_y_top: etwas unterhalb der Ziffer; experimentell abgeschätzt
        stump_y_top = y - (DIGIT_FONT[1] // 1.6)
        drawer.pensize(STUMP_WIDTH)
        drawer.goto(stump_x, stump_y_top)
        drawer.pendown()
        totalHeight = WINDOW_H/-2
        # zufällig Linien zeichnen
        drawer.goto(stump_x, totalHeight / 10 * 2)
        drawer.goto(stump_x + random_pairs[i][0], totalHeight / 10 * 3)
        drawer.goto(stump_x + random_pairs[i][0], totalHeight / 10 * 4)
        drawer.goto(stump_x, totalHeight / 10 * 5)
        drawer.goto(stump_x, totalHeight / 10 * 6)
        drawer.goto(stump_x + random_pairs[i][1], totalHeight / 10 * 7)
        drawer.goto(stump_x + random_pairs[i][1], totalHeight / 10 * 8)
        drawer.goto(stump_x, totalHeight / 10 * 9)
        drawer.goto(stump_x, totalHeight / 10 * 10)
        drawer.penup()
        drawer.pensize(1)

        # --- Spielmodus-Button ---
        drawer.goto(BTN_X1, BTN_Y1)
        drawer.pendown()

        if playmode:
            drawer.fillcolor("#248f24")  # grün wenn aktiv
        else:
            drawer.fillcolor("#555555")  # grau wenn inaktiv

        drawer.begin_fill()
        for _ in range(2):
            drawer.forward(BTN_X2 - BTN_X1)
            drawer.right(90)
            drawer.forward(BTN_Y1 - BTN_Y2)
            drawer.right(90)
        drawer.end_fill()
        drawer.penup()

        # Text
        drawer.goto((BTN_X1 + BTN_X2) / 2, (BTN_Y1 + BTN_Y2) / 2 - 10)
        drawer.pencolor("white")
        drawer.write("Spielmodus", align="center", font=("Arial", 20, "bold"))

    screen.update()


def on_click(x, y):

    # prüfe ob Klick auf Spielmodus Button
    global playmode, randomDecimal

    if BTN_X1 <= x <= BTN_X2 and BTN_Y2 <= y <= BTN_Y1:
        if not playmode:  # nur beim Wechsel
            playmode = True
            randomDecimal = random.randint(0, 255)
        else:
            playmode = False
            randomDecimal = None
        draw_all()
        return

    # prüfe ob Klick in einer Ziffer-Hitbox ist; toggele erstes Treffer-Bit
    for i, bx in enumerate(bit_positions):
        if abs(x - bx) <= DIGIT_HIT_W / 2 and abs(y - DIGIT_Y) <= DIGIT_HIT_H / 2:
            bits[i] ^= 1
            draw_all()
            break

#RandomDecimal neu berechnen, falls Zahl gefunden wurde
def regenerate_random():
    global randomDecimal
    randomDecimal = random.randint(0, 255)
    draw_all()

# Zeichne das erste Mal
draw_all()

# Event-Bindung
screen.onclick(on_click)

# Keep window open
turtle.done()