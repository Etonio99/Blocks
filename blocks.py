import pygame, random, math

pygame.init()
pygame.display.set_caption('Blocks')

class Block:
    def __init__(self, x_position, y_position):
        self.x_position = x_position
        self.y_position = y_position

class BG_Block(Block):
    def __init__(self, x_position, y_position, rect):
        super().__init__(x_position, y_position)
        self.rect = rect

class Block_Formation:
    def __init__(self, x_current_tile, y_current_tile, formation):
        self.x_current_tile = x_current_tile
        self.y_current_tile = y_current_tile
        
        self.formation = formation
        self.blocks = []
        
        self.width = len(self.formation[0])
        self.height = len(self.formation)

        self.can_place = False
        
        line_counter = 0
        for line in self.formation:
            for i in range(self.width):
                if line[i] == "X":
                    self.blocks.append(Block(i, line_counter))    
            line_counter += 1
            
    def move(self, x_tiles, y_tiles):
        if self.x_current_tile + x_tiles < 0 or self.x_current_tile + x_tiles + self.width - 1 >= BOARD_WIDTH:
            return
        if self.y_current_tile + y_tiles < 0 or self.y_current_tile + y_tiles + self.height - 1 >= BOARD_WIDTH:
            return
        
        self.x_current_tile += x_tiles
        self.y_current_tile += y_tiles

        self.can_place = False
        
        block_in_way = False
        for BLOCK in self.blocks:
            if placed_blocks[BLOCK.x_position + self.x_current_tile][BLOCK.y_position + self.y_current_tile]:
                block_in_way = True
        if not block_in_way:
            self.can_place = True  
        
    def draw(self):
        for BLOCK in self.blocks:
            block_color = WHITE
            if placed_blocks[BLOCK.x_position + self.x_current_tile][BLOCK.y_position + self.y_current_tile]:
                block_color = RED
            X_POSITION = GAME_VIEW_X + BLOCK_WIDTH * (BLOCK.x_position + self.x_current_tile) + BLOCK_PADDING * (BLOCK.x_position + self.x_current_tile + 1)
            Y_POSITION = GAME_VIEW_Y + BLOCK_WIDTH * (BLOCK.y_position + self.y_current_tile) + BLOCK_PADDING * (BLOCK.y_position + self.y_current_tile + 1)
            pygame.draw.rect(SURFACE, block_color, (X_POSITION, Y_POSITION, BLOCK_WIDTH, BLOCK_WIDTH))
        

BLOCK_SHAPES = [
    [
        "X"
    ],
    [
        "XX"
    ],
    [
        "X",
        "X"
    ],
    [
        "-X-",
        "XXX",
        "-X-"
    ],
    [
        "X",
        "X",
        "X",
        "X",
        "X"
    ],
    [
        "XXXXX"
    ],
    [
        "X-",
        "XX"
    ],
    [
        "-X",
        "XX"
    ],
    [
        "XX",
        "-X"
    ],
    [
        "XX",
        "X-"
    ],
    [
        "X-",
        "XX",
        "X-"
    ],
    [
        "-X-",
        "XXX"
    ],
    [
        "-X",
        "XX",
        "-X"
    ],
    [
        "XXX",
        "-X-"
    ],
    [
        "XX",
        "XX"
    ],
    [
        "-X",
        "X-"
    ],
    [
        "X-",
        "-X"
    ],
    [
        "X--",
        "-X-",
        "--X"
    ],
    [
        "--X",
        "-X-",
        "X--"
    ]
]

CLOCK = pygame.time.Clock()
FRAME_RATE = 30
SCREEN_WIDTH, SCREEN_HEIGHT = (1920, 1080)
SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RED = 255, 0, 0
ORANGE = 255, 128, 0
YELLOW = 255, 255, 0
GREEN = 0, 255, 0
AQUA = 0, 255, 255
WHITE = 255, 255, 255
GRAY = 128, 128, 128
BLACK = 0, 0, 0

joysticks = {}

BLOCK_WIDTH = 50 # In pixels
BLOCK_PADDING = 5 # In pixels
BOARD_WIDTH = 9 # In blocks

GAME_VIEW_X = SCREEN_WIDTH * 0.5 - BLOCK_WIDTH * BOARD_WIDTH * 0.5 - BLOCK_PADDING * (BOARD_WIDTH + 1) * 0.5
GAME_VIEW_Y = SCREEN_HEIGHT * 0.5 - BLOCK_WIDTH * BOARD_WIDTH * 0.5 - BLOCK_PADDING * (BOARD_WIDTH + 1) * 0.5
GAME_VIEW_WIDTH = BLOCK_WIDTH * BOARD_WIDTH + BLOCK_PADDING * (BOARD_WIDTH + 1)

GAME_VIEW_COLOR = 80, 40, 20
GAME_VIEW_RECT = pygame.rect.Rect(GAME_VIEW_X, GAME_VIEW_Y, GAME_VIEW_WIDTH, GAME_VIEW_WIDTH,)

BG_BLOCK_BRIGHT = 150, 110, 60
BG_BLOCK_DARK = 130, 80, 50
BG_BLOCKS = []

active_block_formation = Block_Formation(0, 0, BLOCK_SHAPES[random.randint(0, len(BLOCK_SHAPES) - 1)])
available_block_formations = []
current_block_formation = 0

placed_blocks = []
possible_placed_blocks = []

for y in range(BOARD_WIDTH):
    placed_blocks.append([])
    possible_placed_blocks.append([])
    for x in range(BOARD_WIDTH):
        placed_blocks[y].append(False)
        possible_placed_blocks[y].append(False)
        BG_BLOCKS.append(BG_Block(x, y, pygame.rect.Rect(GAME_VIEW_X + BLOCK_WIDTH * x + BLOCK_PADDING * (x + 1), GAME_VIEW_Y + BLOCK_WIDTH * y + BLOCK_PADDING * (y + 1), BLOCK_WIDTH, BLOCK_WIDTH)))

columns = []
rows = []
squares = []

possible_columns = []
possible_rows = []
possible_squares = []

score = 0

def update_possible_placed_blocks():
    for y in range(BOARD_WIDTH):
        for x in range(BOARD_WIDTH):
            possible_placed_blocks[x][y] = False
            
    for block in active_block_formation.blocks:
        possible_placed_blocks[block.x_position + active_block_formation.x_current_tile][block.y_position + active_block_formation.y_current_tile] = True

def check_for_groups():
    global columns
    global rows
    global squares

    for y in range(len(placed_blocks)): # Check for columns
        column = True
        for x in range(len(placed_blocks)):
            if not placed_blocks[y][x]:
                column = False
        if column:
            columns.append(y)

    for x in range(len(placed_blocks)): # Check for rows
        row = True
        for y in range(len(placed_blocks)):
            if not placed_blocks[y][x]:
                row = False
        if row:
            rows.append(x)

    for y in range(3): # Check for squares
        for x in range(3):
            square = True
            for x_inner in range(3):
                for y_inner in range(3):
                    if not placed_blocks[x * 3 + x_inner][y * 3 + y_inner]:
                        square = False
            if square:
                squares.append(x + y * 3)
                
def check_for_possible_groups():
    global possible_columns
    possible_columns = []
    global possible_rows
    possible_rows = []
    global possible_squares
    possible_squares = []

    for y in range(len(possible_placed_blocks)): # Check for possible columns
        column = True
        for x in range(len(possible_placed_blocks)):
            if not possible_placed_blocks[y][x] and not placed_blocks[y][x]:
                column = False
        if column:
            possible_columns.append(y)

    for x in range(len(possible_placed_blocks)): # Check for possible rows
        row = True
        for y in range(len(possible_placed_blocks)):
            if not possible_placed_blocks[y][x] and not placed_blocks[y][x]:
                row = False
        if row:
            possible_rows.append(x)

    for y in range(3): # Check for possible squares
        for x in range(3):
            square = True
            for x_inner in range(3):
                for y_inner in range(3):
                    if not possible_placed_blocks[x * 3 + x_inner][y * 3 + y_inner] and not placed_blocks[x * 3 + x_inner][y * 3 + y_inner]:
                        square = False
            if square:
                possible_squares.append(x + y * 3)
    
def clear_groups():
    global columns
    global rows
    global squares

    for column in columns:
        for i in range(BOARD_WIDTH):
            placed_blocks[column][i] = False

    for row in rows:
        for i in range(BOARD_WIDTH):
            placed_blocks[i][row] = False

    for square in squares:
        x = square % 3
        y = math.floor(square / 3)
        for x_inner in range(3):
                for y_inner in range(3):
                    placed_blocks[x * 3 + x_inner][y * 3 + y_inner] = False

    number_of_matches = len(columns) + len(rows) + len(squares)

    global score
    score += number_of_matches * 10 * number_of_matches
    print(score)

    columns = []
    rows = []
    squares = []

def draw_all():
    SURFACE.fill(BLACK)
    
    pygame.draw.rect(SURFACE, GAME_VIEW_COLOR, GAME_VIEW_RECT)
    
    iterator = 0
    line_counter = 0
    for BLOCK in BG_BLOCKS:
        
        color_1 = BG_BLOCK_BRIGHT
        color_2 = BG_BLOCK_DARK
        
        placed_color_1 = 100, 50, 20
        placed_color_2 = 80, 30, 0
        
        GROUP_COLOR = 0, 170, 150
        
        if line_counter >= 3 and line_counter < 6:
            color_1, color_2 = color_2, color_1
            placed_color_1, placed_color_2 = placed_color_2, placed_color_1
                       
        current_square = math.floor(line_counter / 3) * 3 + math.floor(iterator / 3)

        if active_block_formation.can_place and (line_counter in possible_rows or iterator in possible_columns or current_square in possible_squares):
            color_1 = GROUP_COLOR
            color_2 = GROUP_COLOR
            placed_color_1 = GROUP_COLOR
            placed_color_2 = GROUP_COLOR

        if iterator < 3 or iterator >= 6:
            if placed_blocks[BLOCK.x_position][BLOCK.y_position]:
                pygame.draw.rect(SURFACE, placed_color_1, BLOCK.rect)
            else:
                pygame.draw.rect(SURFACE, color_1, BLOCK.rect)
        else:
            if placed_blocks[BLOCK.x_position][BLOCK.y_position]:
                pygame.draw.rect(SURFACE, placed_color_2, BLOCK.rect)
            else:
                pygame.draw.rect(SURFACE, color_2, BLOCK.rect)
        
        iterator += 1
        if iterator >= 9:
            iterator = 0
            line_counter += 1
    
    active_block_formation.draw()
    
    pygame.display.update()

wait_for_joystick_release = False

game_running = True

def main():
    global game_running

    global active_block_formation
    active_block_formation.move(0, 0)

    while game_running:
        global wait_for_joystick_release

        for joystick in joysticks.keys():
            x_joystick_input = joysticks[joystick].get_axis(0)
            y_joystick_input = joysticks[joystick].get_axis(1)
            if abs(x_joystick_input) > 0.5 or abs(y_joystick_input) > 0.5:
                if not wait_for_joystick_release: # Joystick move action
                    active_block_formation.move(round(x_joystick_input), round(y_joystick_input))
                    wait_for_joystick_release = True
                    check_for_groups()
                    update_possible_placed_blocks()
                    check_for_possible_groups()
            else:
                if wait_for_joystick_release:
                    wait_for_joystick_release = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    if not active_block_formation.can_place:
                        continue
                    global score
                    for block in active_block_formation.blocks:
                        score += 1
                        placed_blocks[block.x_position + active_block_formation.x_current_tile][block.y_position + active_block_formation.y_current_tile] = True
                    active_block_formation = Block_Formation(0, 0, BLOCK_SHAPES[random.randint(0, len(BLOCK_SHAPES) - 1)])
                    active_block_formation.move(0, 0)

                    check_for_groups()
                    clear_groups()
                    update_possible_placed_blocks()
                    check_for_possible_groups()
                elif event.button == 1:
                    active_block_formation = Block_Formation(0, 0, BLOCK_SHAPES[0])
                    active_block_formation.move(0, 0)

                    check_for_groups()
                    clear_groups()
                    update_possible_placed_blocks()
                    check_for_possible_groups()
                elif event.button == 6:
                    game_running = False
                print(f"Button {event.button} pressed")
            elif event.type == pygame.JOYDEVICEADDED:
                added_joystick = pygame.joystick.Joystick(event.device_index)
                joysticks[added_joystick.get_instance_id()] = added_joystick
            elif event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
            
        draw_all()

        CLOCK.tick(FRAME_RATE)

if __name__ == "__main__":
    main()
    pygame.quit()