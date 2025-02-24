from setting import *
class Checkbox:
    light_color = (200, 200, 200)
    medium_color = (150, 150, 150)
    medium_dark_color = (100, 100, 100)
    dark_color = (50, 50, 50)
    def __init__(self, screen, position, size=(50, 50)):
        self.size = size
        self.screen = screen
        self.position = position
        self.box_surf = pygame.Surface(self.size)
        self.box_rect = self.box_surf.get_frect(center=self.position)
        self.is_hovered = False
        self.is_checked = False

    def input(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_just_released()
        self.is_hovered = self.box_rect.collidepoint(mouse_pos)
        if self.is_hovered:
            if mouse_buttons[0]:
                self.is_checked = not self.is_checked

    def draw(self):
        pygame.draw.rect(surface=self.screen, color=Checkbox.medium_color, rect=self.box_rect)
        pygame.draw.rect(surface=self.screen, color=Checkbox.medium_dark_color, rect=self.box_rect, width=1)
        if self.is_checked:
            font = pygame.font.Font('freesansbold.ttf', int(self.size[0]*0.8))
            text = font.render("X", True, Checkbox.dark_color)
            text_rect = text.get_frect(center=self.position).move(0, int(self.size[0]*0.08))
            self.screen.blit(text, text_rect)
          
    def update(self):
        self.input()