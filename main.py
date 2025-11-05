import pygame
pygame.init()

# Fenster auf volle Bildschirmgrösse (nicht Vollbild)
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h))
pygame.display.set_caption("Binärsystem-Visualisierung")

# Schrift definieren
font = pygame.font.SysFont(None, 100)
small_font = pygame.font.SysFont(None, 60)

# Startzustand: 8 Bits auf 0
bits = [0] * 8

# Position der Bits berechnen
bit_spacing = 120
start_x = (info.current_w - bit_spacing * 7) // 2
y_pos = info.current_h // 2

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            # prüfen, ob auf eine Zahl geklickt wurde
            for i in range(8):
                x = start_x + i * bit_spacing
                bit_rect = pygame.Rect(x - 40, y_pos - 60, 80, 120)
                if bit_rect.collidepoint(mouse_x, mouse_y):
                    bits[i] = 1 - bits[i]  # zwischen 0 und 1 wechseln

    # Hintergrund weiss
    screen.fill((255, 255, 255))

    # Dezimalwert berechnen
    bit_string = "".join(str(b) for b in bits)
    decimal_value = int(bit_string, 2)

    # Dezimalwert anzeigen
    text_surface = small_font.render(f"Dezimalwert: {decimal_value}", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(info.current_w // 2, y_pos - 150))
    screen.blit(text_surface, text_rect)

    # Bits anzeigen
    for i, bit in enumerate(bits):
        x = start_x + i * bit_spacing
        bit_surface = font.render(str(bit), True, (0, 0, 0))
        bit_rect = bit_surface.get_rect(center=(x, y_pos))
        screen.blit(bit_surface, bit_rect)

    pygame.display.flip()

pygame.quit()
