from setting import *
from enum import Enum
class Cell_Type(Enum):
    EMPTY = -1
    WATER = 0
    SHIP = 1
class Ship_Part_Direction(Enum):
    UNKNOWN = -2
    CIRCLE = -1
    MIDDLE = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4

class Cell:
    empty_color = (250, 250, 250)
    border_color = (20, 20, 20)
    ship_color = (50, 50, 50)
    water_color = (0, 128, 255)
    hightlight_color = (102, 255, 255)
    wrong_color = (200, 0, 0)
    def __init__(self, grid, grid_position=(0, 0), size=(50, 50)):
        self.size = size
        self.grid = grid
        self.grid_position = grid_position
        self.position = ((self.grid_position[1] + 1.5)*self.size[0], (self.grid_position[0] + 1.5)*self.size[1])
        self.type = Cell_Type.EMPTY
        self.direction = Ship_Part_Direction.CIRCLE
        self.cell_surf = pygame.Surface(self.size)
        self.cell_rect = self.cell_surf.get_frect(center=self.position)
        self.is_fixed = False
        self.is_hovered = False

    def input(self):
        mouse_pos = pygame.mouse.get_pos()
        modified_mouse_pos = (mouse_pos[0] - self.grid.grid_rect.left, mouse_pos[1] - self.grid.grid_rect.top)
        mouse_buttons = pygame.mouse.get_just_released()
        self.is_hovered = self.cell_rect.collidepoint(modified_mouse_pos)
        if self.is_hovered:
            if mouse_buttons[0]:
                self.grid.change_cell(self.grid_position, True)
            elif mouse_buttons[2]:
                self.grid.change_cell(self.grid_position, False)

    def draw(self):
        if self.type == Cell_Type.SHIP or self.type == Cell_Type.WATER:    
            #water
            pygame.draw.rect(surface=self.grid.grid_surf, color=Cell.water_color, rect=self.cell_rect)
        elif self.type == Cell_Type.EMPTY:
            #empty
            pygame.draw.rect(surface=self.grid.grid_surf, color=Cell.empty_color, rect=self.cell_rect)
        if self.is_hovered:
            #hover
            pygame.draw.rect(surface=self.grid.grid_surf, color=Cell.hightlight_color, rect=self.cell_rect, width=1)
        #border
        pygame.draw.rect(surface=self.grid.grid_surf, color=Cell.border_color, rect=self.cell_rect, width=1)
        if self.type == Cell_Type.SHIP:
            #ship
            if self.direction == Ship_Part_Direction.MIDDLE:
                pygame.draw.rect(surface=self.grid.grid_surf, color=Cell.ship_color, rect=self.cell_rect.scale_by(0.8))
            elif self.direction == Ship_Part_Direction.CIRCLE:
                pygame.draw.circle(surface=self.grid.grid_surf, color=Cell.ship_color, center=self.position, radius=self.size[0]*0.4)
            elif self.direction == Ship_Part_Direction.TOP:
                pygame.draw.circle(surface=self.grid.grid_surf, color=Cell.ship_color, center=self.position, radius=self.size[0]*0.4)
                pygame.draw.rect(surface=self.grid.grid_surf, color=Cell.ship_color, rect=self.cell_rect.scale_by(0.8, 0.4).move(0,self.size[0]*0.2))
            elif self.direction == Ship_Part_Direction.BOTTOM:
                pygame.draw.circle(surface=self.grid.grid_surf, color=Cell.ship_color, center=self.position, radius=self.size[0]*0.4)
                pygame.draw.rect(surface=self.grid.grid_surf, color=Cell.ship_color, rect=self.cell_rect.scale_by(0.8, 0.4).move(0,-self.size[0]*0.2))
            elif self.direction == Ship_Part_Direction.RIGHT:
                pygame.draw.circle(surface=self.grid.grid_surf, color=Cell.ship_color, center=self.position, radius=self.size[0]*0.4)
                pygame.draw.rect(surface=self.grid.grid_surf, color=Cell.ship_color, rect=self.cell_rect.scale_by(0.4, 0.8).move(-self.size[0]*0.2,0))
            elif self.direction == Ship_Part_Direction.LEFT:
                pygame.draw.circle(surface=self.grid.grid_surf, color=Cell.ship_color, center=self.position, radius=self.size[0]*0.4)
                pygame.draw.rect(surface=self.grid.grid_surf, color=Cell.ship_color, rect=self.cell_rect.scale_by(0.4, 0.8).move(self.size[0]*0.2,0))
        if self.is_fixed:
            pygame.draw.circle(surface=self.grid.grid_surf, color=Cell.hightlight_color, center=self.position, radius=self.size[0]*0.1)
            
    def update(self):
        self.input()
