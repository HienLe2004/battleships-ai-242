from sys import stdin
from search import *
import time
import tracemalloc
tracemalloc.start()

row_constraints, col_constraints = (), ()  # Lưu trữ số lượng phần tàu cần có trong mỗi hàng và cột.
ship_parts = ("t", "b", "l", "r", "c", "m", "x")  # Các giá trị đại diện cho các phần của tàu
water_symbols = ("w", ".")  # Các giá trị đại diện cho nước
incomplete_symbols = ("?", "x")  # Các giá trị chưa hoàn chỉnh.
direction_vectors = {
    "t": (1, 0, "b"),
    "b": (-1, 0, "t"),
    "l": (0, 1, "r"),
    "r": (0, -1, "l"),
    "c": (0, 0, "c"),
}  # Các vector định hướng của tàu

class GameBoard:
    def __init__(self, grid):
        self.grid = grid
        self.size = len(grid)
        self.is_invalid = False
        self.ship_counts = []  # Số lượng tàu cho từng kích thước
        self.row_ship_counts = [0] * self.size
        self.col_ship_counts = [0] * self.size
        self.row_water_counts = [0] * self.size
        self.col_water_counts = [0] * self.size

    def get_cell_value(self, row: int, col: int):
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.grid[row][col].lower()

    def set_cell_value(self, row: int, col: int, value: str, force=False):
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return
        if (not force and self.get_cell_value(row, col) == "?") or force:
            self.grid[row][col] = value
            if value == "x":
                self.isolate_ship_part(row, col, "x")
            if not force and value.lower() in water_symbols:
                self.row_water_counts[row] += 1
                self.col_water_counts[col] += 1
                if self.size - self.row_water_counts[row] < row_constraints[row]:
                    self.is_invalid = True
                if self.size - self.col_water_counts[col] < col_constraints[col]:
                    self.is_invalid = True
            elif not force and value.lower() in ship_parts:
                self.row_ship_counts[row] += 1
                self.col_ship_counts[col] += 1
                if self.row_ship_counts[row] > row_constraints[row]:
                    self.is_invalid = True
                if self.col_ship_counts[col] > col_constraints[col]:
                    self.is_invalid = True

    def get_adjacent_values(self, row: int, col: int):
        return (
            self.get_cell_value(row - 1, col),
            self.get_cell_value(row, col + 1),
            self.get_cell_value(row + 1, col),
            self.get_cell_value(row, col - 1),
        )

    def set_adjacent_values(self, row: int, col: int, top: str, right: str, bottom: str, left: str):
        self.set_cell_value(row - 1, col, top)
        self.set_cell_value(row, col + 1, right)
        self.set_cell_value(row + 1, col, bottom)
        self.set_cell_value(row, col - 1, left)

    def get_diagonal_values(self, row: int, col: int):
        return (
            self.get_cell_value(row - 1, col - 1),
            self.get_cell_value(row - 1, col + 1),
            self.get_cell_value(row + 1, col + 1),
            self.get_cell_value(row + 1, col - 1),
        )

    def set_diagonal_values(self, row: int, col: int, top_left: str, top_right: str, bottom_left: str, bottom_right: str):
        self.set_cell_value(row - 1, col - 1, top_left)
        self.set_cell_value(row - 1, col + 1, top_right)
        self.set_cell_value(row + 1, col + 1, bottom_right)
        self.set_cell_value(row + 1, col - 1, bottom_left)

    @staticmethod
    def create_from_input():
        global row_constraints, col_constraints
        row_info = stdin.readline().strip("\n")
        col_info = stdin.readline().strip("\n")
        row_constraints = tuple(map(int, row_info.split("\t")[1:]))
        col_constraints = tuple(map(int, col_info.split("\t")[1:]))
        board_size = len(row_constraints)
        grid = [["?" for _ in range(board_size)] for _ in range(board_size)]
        board = GameBoard(grid)
        boats_info = stdin.readline().strip("\n")
        board.ship_counts = list(map(int, boats_info.split("\t")[1:]))
        hint_count = int(stdin.readline())
        for _ in range(hint_count):
            hint = stdin.readline().strip("\n").split("\t")[1:]
            hint_row, hint_col = int(hint[0]), int(hint[1])
            board.set_cell_value(hint_row, hint_col, hint[2])
        for row in range(board.size):
            for col in range(board.size):
                if board.get_cell_value(row, col) in ship_parts:
                    board.isolate_ship_part(row, col, board.get_cell_value(row, col))
                if board.get_cell_value(row, col) in ("t", "l", "c"):
                    board.check_ship_completion(row, col)
        return board.simplify_board()
    
    @staticmethod
    def create_from_game_input(cells, max_ship_len, count_per_col, count_per_row):
        global row_constraints, col_constraints
        row_constraints = tuple(i for i in count_per_row)
        col_constraints = tuple(i for i in count_per_col)
        grid = [["?" for _ in row] for row in cells]
        board = GameBoard(grid)
        board.ship_counts = []
        for i in range(max_ship_len + 1):
            if i == 0:
                board.ship_counts.append(0)
            else:
                board.ship_counts.append(max_ship_len + 1 - i)
        for row in range(len(cells)):
            for col in range(len(cells[row])):
                if (cells[row][col] != "?"):
                    board.set_cell_value(row, col, cells[row][col])
        for row in range(board.size):
            for col in range(board.size):
                if board.get_cell_value(row, col) in ship_parts:
                    board.isolate_ship_part(row, col, board.get_cell_value(row, col))
                if board.get_cell_value(row, col) in ("t", "l", "c"):
                    board.check_ship_completion(row, col)
        return board.simplify_board()

    def simplify_board(self):
        changed = True
        while changed:
            changed = False
            for diag in range(self.size):
                if (
                    self.size - self.row_water_counts[diag] == row_constraints[diag]
                    and self.row_ship_counts[diag] != row_constraints[diag]
                ):
                    changed = True
                    for col in range(self.size):
                        self.set_cell_value(diag, col, "x")
                elif (
                    self.row_ship_counts[diag] == row_constraints[diag]
                    and self.size - self.row_water_counts[diag] != row_constraints[diag]
                ):
                    changed = True
                    for col in range(self.size):
                        self.set_cell_value(diag, col, ".")
                if (
                    self.size - self.col_water_counts[diag] == col_constraints[diag]
                    and self.col_ship_counts[diag] != col_constraints[diag]
                ):
                    changed = True
                    for row in range(self.size):
                        self.set_cell_value(row, diag, "x")
                elif (
                    self.col_ship_counts[diag] == col_constraints[diag]
                    and self.size - self.col_water_counts[diag] != col_constraints[diag]
                ):
                    changed = True
                    for row in range(self.size):
                        self.set_cell_value(row, diag, ".")
        for row in range(self.size):
            for col in range(self.size):
                if self.get_cell_value(row, col) == "x":
                    self.identify_ship_part(row, col)
        return self

    def check_ship_isolation(self, row: int, col: int, part_type: str):
        if any(
            val in ship_parts
            for val in self.get_diagonal_values(row, col)
        ):
            return False

        adjacent = self.get_adjacent_values(row, col)
        if part_type in ("t", "r", "b", "l"):
            d_row, d_col, opposite = direction_vectors[part_type]
            opposite_val = self.get_cell_value(row + d_row, col + d_col)
            if opposite_val not in ("?", "x", "m", opposite):
                return False
            if self.get_cell_value(row - d_row, col - d_col) in ship_parts:
                return False
            if self.get_cell_value(row + d_col, col + d_row) in ship_parts:
                return False
            if self.get_cell_value(row - d_col, col - d_row) in ship_parts:
                return False
        elif part_type == "c":
            if any(val in ship_parts for val in adjacent):
                return False
        elif part_type == "m":
            if sum(val in water_symbols for val in adjacent) >= 3:
                return False
            for i in range(3):
                if (
                    adjacent[i] in water_symbols
                    and adjacent[i + 1] in water_symbols
                ) or (
                    adjacent[i] in ship_parts
                    and adjacent[i + 1] in ship_parts
                ):
                    return False
        elif part_type == "x":
            for i in range(3):
                if (
                    adjacent[i] in ship_parts
                    and adjacent[i + 1] in ship_parts
                ):
                    return False

        return True

    def check_ship_completion(self, row: int, col: int):
        val = self.get_cell_value(row, col)
        if val == "c":
            self.ship_counts[1] -= 1
            return
        if val == "m" and self.get_cell_value(row - 1, col) in ship_parts:
            d_row, d_col = -1, 0
        elif val == "m" and self.get_cell_value(row, col - 1) in ship_parts:
            d_row, d_col = 0, -1
        elif val == "m":
            return
        while val == "m":
            row += d_row
            col += d_col
            val = self.get_cell_value(row, col)
        if val in incomplete_symbols or val in water_symbols:
            return
        d_row, d_col, opposite = direction_vectors[val]
        size = 2
        while self.get_cell_value(row + d_row, col + d_col) == "m":
            row += d_row
            col += d_col
            size += 1
        if size > len(self.ship_counts) - 1:
            self.is_invalid = True
            return
        if self.get_cell_value(row + d_row, col + d_col) == opposite:
            self.ship_counts[size] -= 1

    def isolate_ship_part(self, row: int, col: int, part_type: str):
        if not self.check_ship_isolation(row, col, part_type):
            self.is_invalid = True
            return
        self.set_diagonal_values(row, col, ".", ".", ".", ".")
        if part_type in ("t", "r", "b", "l"):
            d_row, d_col, _ = direction_vectors[part_type]
            self.set_cell_value(row + d_row, col + d_col, "x")
            self.set_adjacent_values(row, col, ".", ".", ".", ".")
        elif part_type == "c":
            self.set_adjacent_values(row, col, ".", ".", ".", ".")
        elif part_type == "m":
            adjacent = self.get_adjacent_values(row, col)
            if adjacent.count("?") == 4:
                return
            for i, adj in enumerate(adjacent):
                if adj != "?":
                    break
            if (adj in ship_parts and (i == 0 or i == 2)) or (
                adj in water_symbols and (i == 1 or i == 3)
            ):
                self.set_adjacent_values(row, col, "x", ".", "x", ".")
            elif (adj in ship_parts and (i == 1 or i == 3)) or (
                adj in water_symbols and (i == 0 or i == 2)
            ):
                self.set_adjacent_values(row, col, ".", "x", ".", "x")

    def identify_ship_part(self, row: int, col: int):
        if "?" in self.get_adjacent_values(row, col):
            return

        for part in ship_parts:
            if self.check_ship_isolation(row, col, part):
                break

        self.set_cell_value(row, col, part, True)
        self.check_ship_completion(row, col)

    def is_placement_valid(self, row: int, col: int, size: int, orientation: str):
        d_row, d_col, opposite = direction_vectors[orientation]
        i_row, i_col = row, col
        count = 0
        for _ in range(size):
            val = self.get_cell_value(i_row, i_col)
            if val != "x" and val in ship_parts:
                count += 1
            i_row += d_row
            i_col += d_col
        if count == size:
            return False
        for i in range(size):
            val = self.get_cell_value(row, col)
            if i == 0 and val not in ("?", "x", orientation):
                return False
            elif i == size - 1 and val not in ("?", "x", opposite):
                return False
            elif i != 0 and i != size - 1 and val not in ("?", "x", "m"):
                return False
            if i == 0 and not self.check_ship_isolation(row, col, orientation):
                return False
            elif i == size - 1 and not self.check_ship_isolation(row, col, opposite):
                return False
            elif (
                i != 0
                and i != size - 1
                and not self.check_ship_isolation(row, col, "m")
            ):
                return False
            row += d_row
            col += d_col

        return True

    def get_valid_placements(self, size: int):
        placements = ()
        for diag in range(self.size):
            orientation = "c"
            if size != 1:
                orientation = "l"
            if row_constraints[diag] >= size:
                for col in range(self.size - size + 1):
                    if self.is_placement_valid(diag, col, size, orientation):
                        placements += ((diag, col, size, orientation),)
            if size != 1:
                orientation = "t"
            if col_constraints[diag] >= size:
                for row in range(self.size - size + 1):
                    if self.is_placement_valid(row, diag, size, orientation):
                        placements += ((row, diag, size, orientation),)

        return placements

    def place_ship(self, row: int, col: int, size: int, orientation: str):
        new_grid = [[val for val in self.grid[row]] for row in range(self.size)]
        new_board = GameBoard(new_grid)
        new_board.row_ship_counts = self.row_ship_counts.copy()
        new_board.col_ship_counts = self.col_ship_counts.copy()
        new_board.row_water_counts = self.row_water_counts.copy()
        new_board.col_water_counts = self.col_water_counts.copy()
        new_board.ship_counts = self.ship_counts.copy()
        new_board.ship_counts[size] -= 1
        d_row, d_col, opposite = direction_vectors[orientation]
        for i in range(size):
            if i == 0:
                part_type = orientation
            elif i == size - 1:
                part_type = opposite
            else:
                part_type = "m"
            if new_board.get_cell_value(row, col) == "?":
                new_board.set_cell_value(row, col, part_type)
            elif new_board.get_cell_value(row, col) == "x":
                new_board.set_cell_value(row, col, part_type, True)
            new_board.isolate_ship_part(row, col, part_type)
            row += d_row
            col += d_col

        return new_board.simplify_board()

    def is_complete(self):
        if any(num < 0 for num in self.ship_counts):
            self.is_invalid = True
        if self.is_invalid or sum(self.ship_counts) != 0:
            return False
        self.simplify_board()
        return True

    def __repr__(self):
        return "\n".join(map(lambda val: "".join(val), self.grid))

class GameState:
    state_id = 0

    def __init__(self, board: GameBoard):
        self.board = board
        self.id = GameState.state_id
        GameState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

class BattleshipGame(Problem):
    def __init__(self, board: GameBoard):
        state = GameState(board)
        super().__init__(state)

    def actions(self, state: GameState):
        if state.board.is_invalid or sum(state.board.ship_counts) == 0:
            return ()
        for next_size in reversed(range(len(state.board.ship_counts))):
            if next_size == 0:
                return ()
            if state.board.ship_counts[next_size] != 0:
                break
        return state.board.get_valid_placements(next_size)

    def result(self, state: GameState, action):
        (row, col, size, orientation) = action
        new_state = GameState(state.board.place_ship(row, col, size, orientation))
        return new_state
    
    def goal_test(self, state: GameState):
        return state.board.is_complete()

    def h(self, node: Node):
        board, row_diff = node.state.board, 0
        for i in range(node.state.board.size):
            row_diff += row_constraints[i] - board.row_ship_counts[i]
        return row_diff

if __name__ == "__main__":
    start_time = time.time()
    gb = GameBoard.create_from_input()
    btsg = BattleshipGame(gb)
    # goalNode = depth_first_tree_search(btsg)
    goalNode = best_first_graph_search()
    end_time = time.time()
    print(f"T: {end_time - start_time:.4f} s")
    current, peak = tracemalloc.get_traced_memory()
    print(f"current: {current / 10**6} MB")
    print(f"peak: {peak / 10**6} MB")
    
    tracemalloc.stop()
    
    print(goalNode.state.board)