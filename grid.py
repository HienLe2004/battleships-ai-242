import random
from setting import *
from cell import *
from number_cell import *

class Grid:
    def __init__(self, screen, grid_size=(10, 10), cell_size=(50, 50), position=(300, 300)):
        self.screen = screen
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.grid_surf = pygame.Surface(((grid_size[1] + 1) * cell_size[0], (grid_size[0] + 1) * cell_size[1]))
        self.position = position
        self.grid_rect = self.grid_surf.get_frect(center=self.position) 
        self.cells = []
        self.is_generated_mines = False
        self.first_solve = True
        self.original_grid_data = None
        self.count_per_row = [Number_Cell(self, (i, -1), cell_size, 0) for i in range(grid_size[0])]
        self.count_per_col = [Number_Cell(self, (-1, i), cell_size, 0) for i in range(grid_size[1])]

        for row in range(grid_size[0]):
            cells_in_row = []
            for col in range(grid_size[1]):
                cells_in_row.append(Cell(self, (row,col), self.cell_size))
            self.cells.append(cells_in_row)

    def change_number_cell(self, grid_position, forward):
        cell = None
        limit = 100
        if grid_position[1] == -1:
            limit = self.grid_size[1]
            cell = self.count_per_row[grid_position[0]]
        elif grid_position[0] == -1:
            limit = self.grid_size[0]
            cell = self.count_per_col[grid_position[1]]
        if cell is None:
            return
        # print(f'Change cell at {grid_position} {limit}')
        if forward:
            if cell.value == limit:
                cell.value = 0
            else:
                cell.value += 1
        else:
            if cell.value == 0:
                cell.value = limit
            else:
                cell.value -= 1

    def change_cell(self, grid_position, forward):
        cell = self.cells[grid_position[0]][grid_position[1]]
        # print(f'Change cell at {grid_position}')
        if forward:
            if cell.type == Cell_Type.SHIP:
                if cell.direction.value < Ship_Part_Direction.LEFT.value:
                    cell.direction = Ship_Part_Direction(cell.direction.value + 1)
                else:
                    cell.type = Cell_Type.EMPTY
                    cell.direction = Ship_Part_Direction.CIRCLE
            else:
                cell.type = Cell_Type(cell.type.value + 1)
        else:
            if cell.type == Cell_Type.SHIP:
                if cell.direction.value > Ship_Part_Direction.CIRCLE.value:
                    cell.direction = Ship_Part_Direction(cell.direction.value - 1)
                else:
                    cell.type = Cell_Type.WATER
            else:
                if cell.type == Cell_Type.EMPTY:
                    cell.type = Cell_Type.SHIP
                    cell.direction = Ship_Part_Direction.LEFT
                else:
                    cell.type = Cell_Type(cell.type.value - 1)
        if cell.type != Cell_Type.EMPTY:
            cell.is_fixed = True
        else:
            cell.is_fixed = False


    def set_grid_data(self, data):
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                self.cells[row][col].type = Cell_Type(data[row][col])
    def set_transformed_grid_data(self, data):
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                value = data[row][col].lower()
                if value in ('.','w'):
                    self.cells[row][col].type = Cell_Type.WATER
                elif value in ('t','l','b','r','m','c'):
                    self.cells[row][col].type = Cell_Type.SHIP
                    if value == 't':
                        self.cells[row][col].direction = Ship_Part_Direction.TOP
                    elif value == 'b':
                        self.cells[row][col].direction = Ship_Part_Direction.BOTTOM
                    elif value == 'l':
                        self.cells[row][col].direction = Ship_Part_Direction.LEFT
                    elif value == 'r':
                        self.cells[row][col].direction = Ship_Part_Direction.RIGHT
                    elif value == 'm':
                        self.cells[row][col].direction = Ship_Part_Direction.MIDDLE
                    elif value == 'c':
                        self.cells[row][col].direction = Ship_Part_Direction.CIRCLE
                
    def get_grid_data(self):
        return [[cell.type.value for cell in row] for row in self.cells]
    def get_transformed_grid_data(self):
        new_grid = []
        for row in range(self.grid_size[0]):
            cells_in_row = []
            for col in range(self.grid_size[1]):
                if self.cells[row][col].type == Cell_Type.SHIP:
                    if self.cells[row][col].direction == Ship_Part_Direction.CIRCLE:
                        cells_in_row.append('C')
                    elif self.cells[row][col].direction == Ship_Part_Direction.TOP:
                        cells_in_row.append('T')
                    elif self.cells[row][col].direction == Ship_Part_Direction.BOTTOM:
                        cells_in_row.append('B')
                    elif self.cells[row][col].direction == Ship_Part_Direction.LEFT:
                        cells_in_row.append('L')
                    elif self.cells[row][col].direction == Ship_Part_Direction.RIGHT:
                        cells_in_row.append('R')
                    elif self.cells[row][col].direction == Ship_Part_Direction.MIDDLE:
                        cells_in_row.append('M')
                elif self.cells[row][col].type == Cell_Type.WATER:
                    cells_in_row.append('W')
                else:
                    cells_in_row.append('?')
            new_grid.append(cells_in_row)
        return new_grid
    
    def get_cols_data(self):
        return [cell.value for cell in self.count_per_col]
    
    def get_rows_data(self):
        return [cell.value for cell in self.count_per_row]

    def set_cols_data(self, cols):
        for i in range(self.grid_size[1]):
            self.count_per_col[i].value = cols[i]
    def set_rows_data(self, rows):
        for i in range(self.grid_size[1]):
            self.count_per_row[i].value = rows[i]
    def reset_grid(self):
        self.set_cols_data([0] * self.grid_size[1])
        self.set_rows_data([0] * self.grid_size[0])
        for row in self.cells:
            for cell in row:
                cell.is_fixed = False
                cell.type = Cell_Type.EMPTY 
    def draw(self):
        self.grid_surf.fill((250, 250, 250))
        for row in self.cells:
            for cell in row:
                cell.draw()
        for num_cell in self.count_per_row:
            num_cell.draw()
        for num_cell in self.count_per_col:
            num_cell.draw()
        border_surf = pygame.Surface((self.grid_size[1]*self.cell_size[0],self.grid_size[0]*self.cell_size[1]))
        border_rect = border_surf.get_rect(topleft=self.cell_size)
        pygame.draw.rect(surface=self.grid_surf, color=Cell.border_color, rect=border_rect, width=5)
        self.screen.blit(self.grid_surf, self.grid_rect)

    def update(self):
        for row in self.cells:
            for cell in row:
                cell.update()
        for num_cell in self.count_per_row:
            num_cell.update()
        for num_cell in self.count_per_col:
            num_cell.update()