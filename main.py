
import pygame
from level_manager import LevelManager
from Menu_Manager import MenuManager
from music_manager import Music_Manager

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Moja Gra")

clock = pygame.time.Clock()
running = True
fullscreen = False

# Stany gry
MENU = "menu"
GAME = "game"
PAUSE = "pause"

WON = "WON"

current_state = MENU
level_manager = LevelManager()
menu_manager = MenuManager(screen.get_width(), screen.get_height())


#Muzyka
music = Music_Manager()
dt = 0

while running:
    #screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_state == MENU:
            music.play_track("assets/menu_Soundtrack.mp3")

        # Obsługa ESC - różnie w zależności od stanu
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if current_state == GAME:
                current_state = PAUSE
                menu_manager.change_menu("pause")
            elif current_state == PAUSE:
                current_state = GAME
            else:
                running = False

        # Obsługa F1 - pełny ekran
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
            fullscreen = not fullscreen
            if fullscreen:
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                # Pobierz aktualną rozdzielczość
                screen_info = pygame.display.Info()
                menu_manager.screen_width = screen_info.current_w
                menu_manager.screen_height = screen_info.current_h
            else:
                screen = pygame.display.set_mode((1280, 720))
                menu_manager.screen_width = 1280
                menu_manager.screen_height = 720

            level_manager.recalc_layout()
            menu_manager.recalc_layout()

        # Obsługa zdarzeń w zależności od stanu gry
        if current_state == MENU or current_state == PAUSE or current_state == WON:
            action = menu_manager.handle_event(event)

            if action == "start_game":
                #Nowa Gra
                current_state = GAME

                level_manager = LevelManager()

            elif action == "continue_game":
                current_state = GAME
                # Kontynuuj istniejącą grę

            elif action == "resume_game":
                current_state = GAME

            elif action == "main_menu":
                current_state = MENU
                menu_manager.change_menu("main")

            elif action == "quit":
                running = False


        elif current_state == GAME:
            # Przekaż zdarzenia do gry
            level_manager.player.handle_event(event)




    # Aktualizacja w zależności od stanu
    if current_state == GAME:
        level_manager.update(dt)
        if level_manager.player.harvested == 3:
            menu_manager.change_menu(WON)
            current_state = WON



        music.play_track("assets/soundtrack.mp3")

    # Rysowanie w zależności od stanu
    if current_state == MENU or current_state == PAUSE:
        menu_manager.draw(screen)
    elif current_state == GAME:
        level_manager.draw(screen)

        #Informacja O tym jak wyjść
        if current_state == GAME:
            font = pygame.font.Font(None, 36)
            pause_text = font.render("ESC - Pauza", True, (255, 255, 255))
            screen.blit(pause_text, (10, 10))

            Energy_level = font.render("Energy: " + str(level_manager.player.energy),True, (0, 150, 240) )
            screen.blit(Energy_level, (10, 50))

            How_many_Flowers = font.render( "Zebrane Kwiatki: " +str(level_manager.player.harvested) + "/3", True, (0, 255, 240))
            screen.blit(How_many_Flowers, (10, 100))
    if current_state == WON:

        menu_manager.draw(screen)


    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
