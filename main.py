import pygame
pygame.init()

screen = pygame.display.set_mode((1200, 900))
pygame.display.set_caption("Projekt Applikation Binärsystem")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))                          # Hintergrund weiss
    pygame.draw.line(screen, (0, 0, 0), (100, 100), (400, 300), 3)  # Linie zeichnen

    pygame.display.flip()  # <- Bildschirm aktualisieren!

pygame.quit()
