import pygame
import sys
from assets import MENU_IMG


class MenuManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_menu = "main"
        self.selected_option = 0
        self.image_original = MENU_IMG
        self.image = pygame.transform.scale(self.image_original, (self.screen_height, self.screen_height))

        # Kolory
        self.colors = {
            'background': (20, 20, 20),
            'title': (255, 255, 100),
            'text': (200, 200, 200),
            'selected': (100, 150, 255),
            'button': (40, 50, 70),
            'button_hover': (60, 70, 90)
        }

        # Czcionki
        self.fonts = {
            'title': self.load_font( 'impact', 72),
            'menu': self.load_font('trebuchetms', 48),
            'small': self.load_font('calibri', 36)
        }

        # Opcje menu
        self.menus = {
            'main': {
                'title': 'Flora Castle',
                'options': ['Nowa Gra', 'Kontynuuj', 'Ustawienia', 'Wyjście']
            },
            'settings': {
                'title': 'USTAWIENIA',
                'options': ['Dźwięk', 'Grafika', 'Sterowanie', 'Powrót']
            },
            'pause': {
                'title': 'PAUZA',
                'options': ['Kontynuuj', 'Ustawienia', 'Menu Główne', 'Wyjście']
            }
        }

        self.button_rects = []
        self.recalc_layout()

    def load_font(self, font_name, size):
        """Ładuje czcionkę systemową lub z pliku"""
        try:
            if font_name:
                # Najpierw spróbuj jako czcionka systemowa
                font = pygame.font.SysFont(font_name, size)
                if font:
                    return font
                # Jeśli nie ma systemowej, spróbuj jako plik
                return pygame.font.Font(font_name, size)
            else:
                return pygame.font.Font(None, size)
        except:
            print(f"Nie można załadować czcionki: {font_name}, używam domyślnej")
            return pygame.font.Font(None, size)

    def recalc_layout(self):
        """Przelicza pozycje elementów menu po zmianie rozdzielczości"""
        self.button_rects = []
        current_menu_data = self.menus[self.current_menu]

        self.image = pygame.transform.scale(self.image_original, (self.screen_height, self.screen_height))

        # Oblicz pozycje przycisków
        button_height = 60
        button_width = 300
        total_height = len(current_menu_data['options']) * (button_height + 20)
        start_y = (self.screen_height - total_height) // 2 + 100

        for i, option in enumerate(current_menu_data['options']):
            x = (self.screen_width - button_width) // 6
            y = start_y + i * (button_height + 20)
            self.button_rects.append(pygame.Rect(x, y, button_width, button_height))

    def handle_event(self, event):
        """Obsługuje zdarzenia w menu"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menus[self.current_menu]['options'])
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menus[self.current_menu]['options'])
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self.select_option()

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for i, rect in enumerate(self.button_rects):
                if rect.collidepoint(mouse_pos):
                    self.selected_option = i

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Lewy przycisk myszy
                return self.select_option()

        return None

    def select_option(self):
        """Obsługuje wybór opcji menu"""
        current_menu_data = self.menus[self.current_menu]
        selected_text = current_menu_data['options'][self.selected_option]

        if self.current_menu == "main":
            if selected_text == "Nowa Gra":
                return "start_game"
            elif selected_text == "Kontynuuj":
                return "continue_game"
            elif selected_text == "Ustawienia":
                self.change_menu("settings")
            elif selected_text == "Wyjście":
                return "quit"

        elif self.current_menu == "settings":
            if selected_text == "Dźwięk":
                # Tutaj możesz dodać menu dźwięku
                pass
            elif selected_text == "Grafika":
                # Tutaj możesz dodać menu grafiki
                pass
            elif selected_text == "Sterowanie":
                # Tutaj możesz dodać menu sterowania
                pass
            elif selected_text == "Powrót":
                self.change_menu("main")

        elif self.current_menu == "pause":
            if selected_text == "Kontynuuj":
                return "resume_game"
            elif selected_text == "Ustawienia":
                self.change_menu("settings")
            elif selected_text == "Menu Główne":
                return "main_menu"
            elif selected_text == "Wyjście":
                return "quit"

        return None

    def change_menu(self, new_menu):
        """Zmienia aktywne menu"""
        self.current_menu = new_menu
        self.selected_option = 0
        self.recalc_layout()

    def draw(self, screen):
        """Rysuje menu"""
        screen.fill(self.colors['background'])
        if self.current_menu == "main":
            image_rect = self.image.get_rect(center=((self.screen_width //4) *3 , self.screen_height//2))
            screen.blit(self.image, image_rect)

        # Tło


        current_menu_data = self.menus[self.current_menu]

        # Tytuł
        title_text = self.fonts['title'].render(current_menu_data['title'], True, self.colors['title'])
        title_rect = title_text.get_rect(center=(self.screen_width // 4, 150))
        screen.blit(title_text, title_rect)

        # Opcje menu
        mouse_pos = pygame.mouse.get_pos()

        for i, (option, rect) in enumerate(zip(current_menu_data['options'], self.button_rects)):
            # Kolor przycisku
            if i == self.selected_option or rect.collidepoint(mouse_pos):
                button_color = self.colors['button_hover']
                text_color = self.colors['selected']
            else:
                button_color = self.colors['button']
                text_color = self.colors['text']

            # Rysuj przycisk
            pygame.draw.rect(screen, button_color, rect, border_radius=10)
            pygame.draw.rect(screen, text_color, rect, 2, border_radius=10)

            # Tekst opcji
            text = self.fonts['menu'].render(option, True, text_color)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        # Instrukcje
        if self.current_menu == "main":


            instructions = [
                "Użyj strzałek lub myszy do nawigacji",
                "Enter/Spacja lub klik aby wybrać",
                "F1 - Pełny ekran, ESC - Wyjście"
            ]

            for i, instruction in enumerate(instructions):
                text = self.fonts['small'].render(instruction, True, self.colors['text'])
                text_rect = text.get_rect(center=(self.screen_width // 4, self.screen_height - 100 + i * 25))
                screen.blit(text, text_rect)