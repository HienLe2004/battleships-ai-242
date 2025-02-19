from setting import *
from game import *
import time
import pygame_gui

class Setting:
    def __init__(self):
        self.running = True
        pygame.init()
        self.screen = pygame.display.set_mode((SETTING_SCREEN_WIDTH, SETTING_SCREEN_HEIGHT))
        pygame.display.set_caption('Battleships AI')
        self.clock = pygame.time.Clock()
        self.input_row_rect = pygame.Rect()
        self.font = pygame.font.Font('fonts/Electrolize-Regular.ttf', 30)
        self.small_font = pygame.font.Font('fonts/Electrolize-Regular.ttf', 16)
        self.is_done = False
        self.is_invalid = False

        self.manager = pygame_gui.UIManager((SETTING_SCREEN_WIDTH, SETTING_SCREEN_HEIGHT))
        self.manager.get_theme().load_theme('themes/setting_theme.json')
        row_rect_surf = pygame.Surface((100,50))
        row_rect = row_rect_surf.get_rect(midbottom=(SETTING_SCREEN_WIDTH/2, SETTING_SCREEN_HEIGHT/2)).move(-200,-20)
        self.row_input = pygame_gui.elements.UITextEntryLine(relative_rect=row_rect,
                                                             manager=self.manager, object_id="#row_input",
                                                             initial_text='6')
        self.row_input.set_allowed_characters('numbers')

        col_rect_surf = pygame.Surface((100,50))
        col_rect = col_rect_surf.get_rect(midbottom=(SETTING_SCREEN_WIDTH/2, SETTING_SCREEN_HEIGHT/2)).move(80,-20)
        self.col_input = pygame_gui.elements.UITextEntryLine(relative_rect=col_rect,
                                                             manager=self.manager, object_id="#col_input",
                                                             initial_text='6')
        self.col_input.set_allowed_characters('numbers')

        max_ship_len_rect_surf = pygame.Surface((100,50))
        max_ship_len_rect = max_ship_len_rect_surf.get_rect(midbottom=(SETTING_SCREEN_WIDTH/2, SETTING_SCREEN_HEIGHT/2)).move(200,60)
        self.max_ship_len_input = pygame_gui.elements.UITextEntryLine(relative_rect=max_ship_len_rect,
                                                             manager=self.manager, object_id="#max_ship_len_input",
                                                             initial_text='3')
        self.max_ship_len_input.set_allowed_characters('numbers')

        button_surf = pygame.Surface((200,50))
        button_rect = button_surf.get_rect(midbottom=(SETTING_SCREEN_WIDTH/2, SETTING_SCREEN_HEIGHT/2)).move(0,150)
        self.confirm_button = pygame_gui.elements.UIButton(relative_rect=button_rect, text="OK", 
                                                           object_id="#confirm_btn")
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            if self.is_done:
                self.running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.manager.process_events(event)
                if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.confirm_button:
                    if self.row_input.get_text() == '' or self.col_input.get_text() == '':
                        self.is_invalid = True
                    else:
                        row = int(self.row_input.get_text())
                        col = int(self.col_input.get_text())
                        max_len = int(self.max_ship_len_input.get_text())
                        if row == 0 or col == 0 or max_len == 0:
                            self.is_invalid = True
                        else:
                            self.is_invalid = False
                            print(f"{row} {col} {max_len}")
                            global nb_of_rows, nb_of_cols, max_ship_len
                            nb_of_rows = row
                            nb_of_cols = col
                            max_ship_len = max_len
                            self.is_done = True
                                
            self.manager.update(dt)

            self.screen.fill((100,100,100))
            text = self.font.render("Please type your game board information", True, (10,10,10))
            text_rect = text.get_frect(midbottom=(SETTING_SCREEN_WIDTH/2,SETTING_SCREEN_HEIGHT/2)).move(0,-120)
            self.screen.blit(text, text_rect)

            row_text = self.font.render("rows", True, (10,10,10))
            row_text_rect = row_text.get_frect(midbottom=(SETTING_SCREEN_WIDTH/2,SETTING_SCREEN_HEIGHT/2)).move(-100,-20)
            self.screen.blit(row_text, row_text_rect)

            x_text = self.font.render("X", True, (10,10,10))
            x_text_rect = x_text.get_frect(midbottom=(SETTING_SCREEN_WIDTH/2,SETTING_SCREEN_HEIGHT/2)).move(0,-20)
            self.screen.blit(x_text, x_text_rect)

            col_text = self.font.render("columns", True, (10,10,10))
            col_text_rect = col_text.get_frect(midbottom=(SETTING_SCREEN_WIDTH/2,SETTING_SCREEN_HEIGHT/2)).move(200,-20)
            self.screen.blit(col_text, col_text_rect)

            ship_max_len_text = self.font.render("Length of the longest ship", True, (10,10,10))
            ship_max_len_text_rect = ship_max_len_text.get_frect(midbottom=(SETTING_SCREEN_WIDTH/2,SETTING_SCREEN_HEIGHT/2)).move(-50,60)
            self.screen.blit(ship_max_len_text, ship_max_len_text_rect)

            if self.is_invalid:
                error_text = self.font.render("Invalid input!", True, (255,10,10))
                error_text_rect = error_text.get_frect(midbottom=(SETTING_SCREEN_WIDTH/2,SETTING_SCREEN_HEIGHT/2)).move(0,50)
                self.screen.blit(error_text, error_text_rect)

            self.manager.draw_ui(self.screen)
            pygame.display.update()
        pygame.quit()
if __name__ == '__main__':
    setting = Setting()
    setting.run()
    print("Finished setting!")
    print(f"The longest ship has a length of {max_ship_len}.")
    print(f"Generating grid size {nb_of_rows}x{nb_of_cols}...")
    if nb_of_cols != 0 and nb_of_rows != 0:
        game = Game(nb_of_rows, nb_of_cols, max_ship_len)
        game.run()