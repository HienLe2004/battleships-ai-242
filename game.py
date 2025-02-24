from setting import *
import setting
import pygame_gui
from cell import *
from grid import *
from battleships import *
from checkbox import *
import time
import tracemalloc

class Game:
    def __init__(self, row, col, nb_of_ships):
        self.ROW = row
        self.COL = col
        self.nb_of_ships = nb_of_ships
        self.CELL_SIZE = min(MAX_MAIN_SCREEN_HEIGHT//row, MAX_MAIN_SCREEN_WIDTH//col)
        self.SCREEN_WIDTH_OFFSET = 300
        self.MAIN_SCREEN_WIDTH = self.CELL_SIZE * (col + 1) + self.SCREEN_WIDTH_OFFSET
        self.MAIN_SCREEN_HEIGH = self.CELL_SIZE * (row + 1)
        self.running = True
        self.is_solved = False
        pygame.init()
        self.screen = pygame.display.set_mode((self.MAIN_SCREEN_WIDTH, self.MAIN_SCREEN_HEIGH))
        pygame.display.set_caption('Battleships AI')
        self.clock = pygame.time.Clock()
        self.grid = Grid(self.screen, (self.ROW, self.COL), 
                         (self.CELL_SIZE, self.CELL_SIZE),
                         (self.MAIN_SCREEN_WIDTH/2 - self.SCREEN_WIDTH_OFFSET/2, self.MAIN_SCREEN_HEIGH/2))
        self.manager = pygame_gui.UIManager((self.MAIN_SCREEN_WIDTH, self.MAIN_SCREEN_HEIGH))
        self.manager.get_theme().load_theme('themes/game_theme.json')
        bfs_btn_surf = pygame.Surface((200,50))
        bfs_btn_rect = bfs_btn_surf.get_rect(topleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 10, 10))
        self.bfs_button = pygame_gui.elements.UIButton(relative_rect=bfs_btn_rect, text="BFS", 
                                                       manager=self.manager,
                                                       object_id="#bfs_btn")
        dfs_btn_surf = pygame.Surface((200,50))
        dfs_btn_rect = dfs_btn_surf.get_rect(topleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 10, 60))
        self.dfs_button = pygame_gui.elements.UIButton(relative_rect=dfs_btn_rect, text="DFS", 
                                                       manager=self.manager,
                                                       object_id="#dfs_btn")
        heuristic_btn_surf = pygame.Surface((200,50))
        heuristic_btn_rect = heuristic_btn_surf.get_rect(topleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 10, 110))
        self.heuristic_button = pygame_gui.elements.UIButton(relative_rect=heuristic_btn_rect, text="Heuristic", 
                                                       manager=self.manager,
                                                       object_id="#heuristic_btn")
        row_rect_surf = pygame.Surface((150,50))
        row_rect = row_rect_surf.get_rect(topleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 110, 160))
        self.row_input = pygame_gui.elements.UITextEntryLine(relative_rect=row_rect,
                                                             manager=self.manager, object_id="#row_input",
                                                             initial_text=" ".join(["0"] * self.ROW))
        row_button_surf = pygame.Surface((100,50))
        row_button_rect = row_button_surf.get_rect(topleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 10, 160))
        self.confirm_row_button = pygame_gui.elements.UIButton(relative_rect=row_button_rect, text="row", 
                                                               manager=self.manager,
                                                               object_id="#confirm_row_btn")
        col_rect_surf = pygame.Surface((150,50))
        col_rect = col_rect_surf.get_rect(topleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 110, 210))
        self.col_input = pygame_gui.elements.UITextEntryLine(relative_rect=col_rect,
                                                             manager=self.manager, object_id="#col_input",
                                                             initial_text=" ".join(["0"] * self.COL))
        col_button_surf = pygame.Surface((100,50))
        col_button_rect = col_button_surf.get_rect(topleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 10, 210))
        self.confirm_col_button = pygame_gui.elements.UIButton(relative_rect=col_button_rect, text="column", 
                                                               manager=self.manager,
                                                               object_id="#confirm_col_btn")
        reset_button_surf = pygame.Surface((100,50))
        reset_button_rect = reset_button_surf.get_rect(bottomleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 10, self.MAIN_SCREEN_HEIGH))
        self.confirm_reset_button = pygame_gui.elements.UIButton(relative_rect=reset_button_rect, text="Reset", 
                                                               manager=self.manager,
                                                               object_id="#confirm_reset_btn")
        self.checkbox = Checkbox(self.screen, (self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 20, 280), (20,20))
    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.bfs_button:
                    self.is_solved = False
                    print("Solving by BFS algorithm...")
                    print("Input grid:")
                    grid_data = self.grid.get_transformed_grid_data()
                    for row in grid_data:
                        print(row)
                    # if self.grid.first_solve:
                    #     self.grid.first_solve = False
                    #     self.grid.original_grid_data = grid_data
                    # else:
                    #     grid_data = self.grid.original_grid_data
                    start_time = time.time()  # Lấy thời gian bắt đầu
                    tracemalloc.start() # Bắt đầu theo dõi
                    gb = GameBoard.create_from_game_input(grid_data, self.nb_of_ships, self.grid.get_cols_data(), self.grid.get_rows_data())
                    btsg = BattleshipGame(gb)
                    if self.checkbox.is_checked:
                        goalNode = breadth_first_tree_search(btsg, self)  
                    else:
                        goalNode = breadth_first_tree_search(btsg)
                    current, peak = tracemalloc.get_traced_memory() # Lấy thông tin bộ nhớ
                    end_time = time.time()  # Lấy thời gian kết thúc
                    execution_time = end_time - start_time  # Thời gian thực thi
                    self.is_solved = True
                    self.execution_time = execution_time
                    self.current_capacity = current
                    self.peak_capacity = peak
                    print("Output grid:")
                    print(goalNode.state.board)
                    self.grid.set_transformed_grid_data(goalNode.state.board.grid)
                elif event.ui_element == self.dfs_button:
                    self.is_solved = False
                    print("Solving by DFS algorithm...")
                    print("Input grid:")
                    grid_data = self.grid.get_transformed_grid_data()
                    for row in grid_data:
                        print(row)
                    # if self.grid.first_solve:
                    #     self.grid.first_solve = False
                    #     self.grid.original_grid_data = grid_data
                    # else:
                    #     grid_data = self.grid.original_grid_data
                    start_time = time.time()  # Lấy thời gian bắt đầu
                    tracemalloc.start() # Bắt đầu theo dõi
                    gb = GameBoard.create_from_game_input(grid_data, self.nb_of_ships, self.grid.get_cols_data(), self.grid.get_rows_data())
                    btsg = BattleshipGame(gb)
                    if self.checkbox.is_checked:
                        goalNode = depth_first_tree_search(btsg, self)
                    else:
                        goalNode = depth_first_tree_search(btsg)
                    current, peak = tracemalloc.get_traced_memory() # Lấy thông tin bộ nhớ
                    end_time = time.time()  # Lấy thời gian kết thúc
                    execution_time = end_time - start_time  # Thời gian thực thi
                    self.is_solved = True
                    self.execution_time = execution_time
                    self.current_capacity = current
                    self.peak_capacity = peak
                    print("Output grid:")
                    print(goalNode.state.board)
                    self.grid.set_transformed_grid_data(goalNode.state.board.grid)
                elif event.ui_element == self.heuristic_button:
                    self.is_solved = False
                    print("Solving by A* algorithm...")
                    print("Input grid:")
                    grid_data = self.grid.get_transformed_grid_data()
                    for row in grid_data:
                        print(row)
                    # if self.grid.first_solve:
                    #     self.grid.first_solve = False
                    #     self.grid.original_grid_data = grid_data
                    # else:
                    #     grid_data = self.grid.original_grid_data
                    start_time = time.time()  # Lấy thời gian bắt đầu
                    tracemalloc.start() # Bắt đầu theo dõi
                    gb = GameBoard.create_from_game_input(grid_data, self.nb_of_ships, self.grid.get_cols_data(), self.grid.get_rows_data())
                    btsg = BattleshipGame(gb)
                    if self.checkbox.is_checked:
                        goalNode = astar_search(btsg, game = self)
                    else:
                        goalNode = astar_search(btsg)
                    current, peak = tracemalloc.get_traced_memory() # Lấy thông tin bộ nhớ
                    end_time = time.time()  # Lấy thời gian kết thúc
                    execution_time = end_time - start_time  # Thời gian thực thi
                    self.is_solved = True
                    self.execution_time = execution_time
                    self.current_capacity = current
                    self.peak_capacity = peak
                    print("Output grid:")
                    print(goalNode.state.board)
                    self.grid.set_transformed_grid_data(goalNode.state.board.grid)
                elif event.ui_element == self.confirm_row_button:
                    row_input = self.row_input.get_text().split(' ')
                    row_input = [int(i) for i in row_input]
                    while (len(row_input) < self.ROW):
                        row_input.append(0)
                    while (len(row_input) > self.ROW):
                        row_input.pop()
                    self.grid.set_rows_data(row_input)
                elif event.ui_element == self.confirm_col_button:
                    col_input = self.col_input.get_text().split(' ')
                    col_input = [int(i) for i in col_input]
                    while (len(col_input) < self.COL):
                        col_input.append(0)
                    while (len(col_input) > self.COL):
                        col_input.pop()
                    self.grid.set_cols_data(col_input)
                elif event.ui_element == self.confirm_reset_button:
                    self.grid.reset_grid()
                    self.is_solved = False
                    setting.current_state = 0

    def draw(self):
        self.screen.fill((200,200,200))
        self.grid.draw()
        if self.is_solved:
            self.show_result()
        self.checkbox.draw()
        #show current state
        font = pygame.font.Font('fonts/Electrolize-Regular.ttf', 16)
        text = font.render(f"State #{setting.current_state}", True, (10,10,10))
        text_rect = text.get_frect(bottomleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 10, 550))
        self.screen.blit(text, text_rect)

    def draw_every_states(self):
        self.screen.fill((200,200,200))
        self.grid.draw()
        #show current state
        font = pygame.font.Font('fonts/Electrolize-Regular.ttf', 16)
        text = font.render(f"State #{setting.current_state}", True, (10,10,10))
        text_rect = text.get_frect(bottomleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 10, 550))
        self.screen.blit(text, text_rect)
        pygame.display.update()

    def show_result(self):
        font = pygame.font.Font('fonts/Electrolize-Regular.ttf', 16)
        text_1 = font.render(f"Execution time: {self.execution_time:.4f} s", True, (20,20,20))
        text_2 = font.render(f"Current cap: {self.current_capacity / 1024:.2f} KB", True, (20,20,20))
        text_3 = font.render(f"Peak cap: {self.peak_capacity / 1024:.2f} KB", True, (20,20,20))
        text_rect_1 = text_1.get_frect(topleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 10, 380))
        text_rect_2 = text_2.get_frect(topleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 10, 410))
        text_rect_3 = text_3.get_frect(topleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 10, 440))
        self.screen.blit(text_1, text_rect_1)
        self.screen.blit(text_2, text_rect_2)
        self.screen.blit(text_3, text_rect_3)

    def update(self):
        self.input()
        self.grid.update()
        self.checkbox.update()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            self.update()
            self.draw()
            self.manager.update(dt)
            self.manager.draw_ui(self.screen)
            pygame.display.update()
        pygame.quit()
