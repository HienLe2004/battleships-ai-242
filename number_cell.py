from setting import *
class Number_Cell:
    def __init__(self, grid, grid_position=(0, 0), size=(50, 50), value=0):
        self.size = size
        self.grid = grid
        self.grid_position = grid_position
        self.position = ((self.grid_position[1] + 1.5)*self.size[0], (self.grid_position[0] + 1.5)*self.size[1])
        self.value = value
        self.Number_Cell_surf = pygame.Surface(self.size)
        self.Number_Cell_rect = self.Number_Cell_surf.get_frect(center=self.position)
        self.is_hovered = False

    def input(self):
        mouse_pos = pygame.mouse.get_pos()
        modified_mouse_pos = (mouse_pos[0] - self.grid.grid_rect.left, mouse_pos[1] - self.grid.grid_rect.top)
        mouse_buttons = pygame.mouse.get_just_released()
        self.is_hovered = self.Number_Cell_rect.collidepoint(modified_mouse_pos)
        if self.is_hovered:
            if mouse_buttons[0]:
                self.grid.change_number_cell(self.grid_position, True)
            elif mouse_buttons[2]:
                self.grid.change_number_cell(self.grid_position, False)

    def draw(self):
        font = pygame.font.Font('freesansbold.ttf', int(self.size[0]*0.8))
        text = font.render(str(self.value), True, (10,10,10))
        text_rect = text.get_frect(center=self.position).move(0, int(self.size[0]*0.08))
        self.grid.grid_surf.blit(text, text_rect)
           
    
    def update(self):
        self.input()