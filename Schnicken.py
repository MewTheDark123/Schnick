import pygame
import constants 
from states import MenuState


def main():
    pygame.init()        
    # Initialisierung von Fenster und Taktung
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    # Start-State des Spiels
    current_state = MenuState()
    running = True

    while running:
        dt = clock.tick(constants.FRAME_RATE)/1000    #Sekunden seit dem letzten frame
        
        events = pygame.event.get()

        # Globale Quit-Abfrage
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
        # State-Wechsel nur wenn neuer State zurückgegeben wird
        new_state = current_state.handle_events(events)
        if new_state != None:
            current_state = new_state

        #Hover-Check
        current_state.update(dt)
        # Zeichnet aktuellen State   
        current_state.draw(screen)

        pygame.display.flip()
        clock.tick(constants.FRAME_RATE)
    pygame.quit()


def toggle_fullscreen():
    is_fullscreen = bool(pygame.display.get_surface().get_flags() & pygame.FULLSCREEN)
    if is_fullscreen:
        screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    else:
        screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.FULLSCREEN)

if __name__ == "__main__":
    main()
