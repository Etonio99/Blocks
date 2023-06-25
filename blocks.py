import pygame, random, math, os

pygame.init()
pygame.mixer.init()
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
            pygame.mixer.Sound.play(STUCK_SOUND)
            return
        if self.y_current_tile + y_tiles < 0 or self.y_current_tile + y_tiles + self.height - 1 >= BOARD_WIDTH:
            pygame.mixer.Sound.play(STUCK_SOUND)
            return
        
        pygame.mixer.Sound.play(MOVE_SOUND)
        
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
        "X"
    ],
    [
        "XXXX"
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
    ],
    [
        "XX",
        "X-",
        "XX"
    ],
    [
        "XX",
        "-X",
        "XX"
    ],
    [
        "X-X",
        "XXX"
    ],
    [
        "XXX",
        "X-X"
    ],
    [
        "-XX",
        "XX-"
    ],
    [
        "XX-",
        "-XX"
    ],
    [
        "X-",
        "XX",
        "-X"
    ],
    [
        "-X",
        "XX",
        "X-"
    ],
    [
        "X-",
        "X-",
        "XX"
    ],
    [
        "XX",
        "X-",
        "X-"
    ],
    [
        "-X",
        "-X",
        "XX"
    ],
    [
        "XX",
        "-X",
        "-X"
    ],
    [
        "--X",
        "XXX"
    ],
    [
        "X--",
        "XXX"
    ],
    [
        "XXX",
        "--X"
    ],
    [
        "XXX",
        "X--"
    ],
    [
        "XXX",
        "X--",
        "X--"
    ],
    [
        "XXX",
        "--X",
        "--X"
    ],
    [
        "--X",
        "--X",
        "XXX"
    ],
    [
        "X--",
        "X--",
        "XXX"
    ],
    [
        "XXX",
        "-X-",
        "-X-"
    ],
    [
        "--X",
        "XXX",
        "--X"
    ],
    [
        "-X-",
        "-X-",
        "XXX"
    ],
    [
        "X--",
        "XXX",
        "X--"
    ]
]

HARD_BLOCK_SHAPES = [
    [
        "X-X",
        "-X-",
        "X-X"   
    ],
    [
        "X-X",
        "---",
        "X-X"
    ],
    [
        "-X-",
        "X-X"
    ],
    [
        "X-X",
        "-X-"
    ],
    [
        "X-",
        "-X",
        "X-"
    ],
    [
        "-X",
        "X-",
        "-X"
    ],
    [
        "-X",
        "X-X",
        "-X"
    ],
    [
        "X-X",
        "X-X"
    ],
    [
        "XX",
        "--",
        "XX"
    ],
    [
        "--X",
        "XX-"
    ],
    [
        "X--",
        "-XX"
    ],
    [
        "XX-",
        "--X"
    ],
    [
        "-XX",
        "X--"
    ],
    [
        "XXX",
        "XXX",
        "XXX"
    ]
]

class Available_Block_Formation:
    def __init__(self, formation, x_current_tile, y_current_tile, id):
        self.formation = formation
        self.x_current_tile = x_current_tile
        self.y_current_tile = y_current_tile
        
        self.id = id

        self.width = len(self.formation[0])
        self.height = len(self.formation)

        self.can_fit = False

        self.blocks = []
        line_counter = 0
        for line in self.formation:
            for i in range(self.width):
                if line[i] == "X":
                    self.blocks.append(Block(i, line_counter))    
            line_counter += 1
        
    def draw(self):
        for BLOCK in self.blocks:
            color = WHITE
            if current_block_formation == self.id:
                if not self.can_fit:
                    color = ACTIVE_NO_FIT_COLOR
                else:
                    color = ACTIVE_COLOR
            elif not self.can_fit:
                color = NO_FIT_COLOR
            X_POSITION = GAME_VIEW_X + BLOCK_WIDTH * 0.5 * (BLOCK.x_position + self.x_current_tile) + BLOCK_PADDING * 0.5 * (BLOCK.x_position + self.x_current_tile + 1)
            Y_POSITION = GAME_VIEW_Y + BLOCK_WIDTH * 0.5 * (BLOCK.y_position + self.y_current_tile) + BLOCK_PADDING * 0.5 * (BLOCK.y_position + self.y_current_tile + 1)
            pygame.draw.rect(SURFACE, color, (X_POSITION - BLOCK_WIDTH * 0.5 * self.width * 0.5, Y_POSITION - BLOCK_WIDTH * 0.5 * self.width * 0.5, BLOCK_WIDTH * 0.5, BLOCK_WIDTH * 0.5))

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

FG_BLOCK_BRIGHT = 240, 200, 60
FG_BLOCK_DARK = 240, 180, 60

ACTIVE_COLOR = 0, 200, 180
ACTIVE_NO_FIT_COLOR = 0, 148, 128
NO_FIT_COLOR = 128, 128, 128

active_block_formation = None
available_block_formations = []
current_block_formation = 0

placed_blocks = []
possible_placed_blocks = []

difficulty = 0

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
SCORE_FONT = pygame.font.Font(None, 64)

MOVE_SOUND = pygame.mixer.Sound("sounds/Menu_Click.wav")
STUCK_SOUND = pygame.mixer.Sound("sounds/Menu_End.wav")

GROUP_SOUNDS = [
    pygame.mixer.Sound("sounds/Success_1.wav"),
    pygame.mixer.Sound("sounds/Success_2.wav"),
    pygame.mixer.Sound("sounds/Success_3.wav"),
    pygame.mixer.Sound("sounds/Success_4.wav"),
    pygame.mixer.Sound("sounds/Success_5.wav"),
    pygame.mixer.Sound("sounds/Success_6.wav"),
    pygame.mixer.Sound("sounds/Success_7.wav")
]

PLACE_SOUND = pygame.mixer.Sound("sounds/Place.wav")
ERROR_SOUND = pygame.mixer.Sound("sounds/Error.wav")

high_scores = []

def load_high_scores():
    global high_scores
    if os.path.isfile(f"high_scores_{difficulty}.txt"):
        with open(f"high_scores_{difficulty}.txt", "r") as file:
            contents = file.read()
            for line in contents.split("\n"):
                high_scores.append(int(line))
        high_scores.sort()
    else:
        high_scores.append(0)
        high_scores.append(1)
        high_scores.append(2)
        high_scores.append(3)
        high_scores.append(4)
        high_scores.sort()
        with open("high_scores.txt", "w") as file:
            file.write(str(high_scores[4]) + "\n")
            file.write(str(high_scores[3]) + "\n")
            file.write(str(high_scores[2]) + "\n")
            file.write(str(high_scores[1]) + "\n")
            file.write(str(high_scores[0]))

def check_high_scores():
    global high_scores

    high_scores.append(score)
    high_scores.sort()
    del high_scores[0]

def save_high_scores():
    global high_scores
    high_scores.sort()
    with open(f"high_scores_{difficulty}.txt", "w") as file:
        file.write(str(high_scores[4]) + "\n")
        file.write(str(high_scores[3]) + "\n")
        file.write(str(high_scores[2]) + "\n")
        file.write(str(high_scores[1]) + "\n")
        file.write(str(high_scores[0]))

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

    if number_of_matches > 0:
        pygame.mixer.Sound.play(GROUP_SOUNDS[number_of_matches - 1])
    else:
        pygame.mixer.Sound.play(PLACE_SOUND)

    global score
    score += number_of_matches * 10 * number_of_matches
    # print(score)

    columns = []
    rows = []
    squares = []

def get_random_formation():
    formation = "X"
    if difficulty == 1:
        chance = random.randint(0, 10)
        if chance >= 7:
            formation = HARD_BLOCK_SHAPES[random.randint(0, len(HARD_BLOCK_SHAPES) - 1)]
            return formation
    formation = BLOCK_SHAPES[random.randint(0, len(BLOCK_SHAPES) - 1)]
    return formation

def check_if_game_over():
    for FORMATION in available_block_formations:
        if FORMATION.can_fit:
            return
    
    check_high_scores()
    save_high_scores()

def fill_available_formations():
    global available_block_formations
    available_block_formations = [
        Available_Block_Formation(get_random_formation(), -4, 0, 0),
        Available_Block_Formation(get_random_formation(), -4, 8, 1),
        Available_Block_Formation(get_random_formation(), -4, 16, 2)
    ]
    check_available_formations_for_fit()

def check_available_formations_for_fit():
    for formation in available_block_formations:
        formation.can_fit = False
        for y in range(BOARD_WIDTH):
            if formation.can_fit:
                continue
            for x in range(BOARD_WIDTH):
                if formation.can_fit:
                    continue
                blocks_that_fit = 0
                for BLOCK in formation.blocks:
                    if x + BLOCK.x_position >= BOARD_WIDTH or y + BLOCK.y_position >= BOARD_WIDTH:
                        continue
                    if not placed_blocks[x + BLOCK.x_position][y + BLOCK.y_position]:
                        blocks_that_fit += 1
                    else:
                        continue
                if blocks_that_fit == len(formation.blocks):
                    formation.can_fit = True

    check_if_game_over()

def draw_all():
    SURFACE.fill(BLACK)
    
    pygame.draw.rect(SURFACE, GAME_VIEW_COLOR, GAME_VIEW_RECT)
    
    iterator = 0
    line_counter = 0
    for BLOCK in BG_BLOCKS:
        
        color_1 = BG_BLOCK_BRIGHT
        color_2 = BG_BLOCK_DARK
        
        placed_color_1 = FG_BLOCK_BRIGHT
        placed_color_2 = FG_BLOCK_DARK
        
        if line_counter >= 3 and line_counter < 6:
            color_1, color_2 = color_2, color_1
            placed_color_1, placed_color_2 = placed_color_2, placed_color_1
                       
        current_square = math.floor(line_counter / 3) * 3 + math.floor(iterator / 3)

        if active_block_formation.can_place and (line_counter in possible_rows or iterator in possible_columns or current_square in possible_squares):
            color_1 = ACTIVE_COLOR
            color_2 = ACTIVE_COLOR
            placed_color_1 = ACTIVE_COLOR
            placed_color_2 = ACTIVE_COLOR

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
    
    if active_block_formation != None:
        active_block_formation.draw()
    
    for formation in available_block_formations:
        formation.draw()
    
    score_text = SCORE_FONT.render(f"{score}", False, WHITE)
    score_text_rect = score_text.get_rect(center = (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.5 - BOARD_WIDTH * 0.5 * BLOCK_WIDTH - BLOCK_PADDING * BOARD_WIDTH))

    SURFACE.blit(score_text, score_text_rect)
    
    pygame.display.update()

wait_for_joystick_release = False

in_menu = True
in_game = False
game_running = True

def start_game():
    global in_game
    in_game = True

    global active_block_formation

    fill_available_formations()
    active_block_formation = Block_Formation(0, 0, available_block_formations[0].formation)
    active_block_formation.move(0, 0)

def handle_in_game_events():
    global game_running
    global in_game

    global active_block_formation
    global current_block_formation

    global wait_for_joystick_release

    for joystick in joysticks.keys():
        x_joystick_input = joysticks[joystick].get_axis(0)
        y_joystick_input = joysticks[joystick].get_axis(1)
        if abs(x_joystick_input) > 0.5 or abs(y_joystick_input) > 0.5:
            if not wait_for_joystick_release: # Joystick move action
                if active_block_formation != None:
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
            in_game = False
            game_running = False
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                if not active_block_formation.can_place:
                    pygame.mixer.Sound.play(ERROR_SOUND)
                    continue
                global score
                for block in active_block_formation.blocks:
                    score += 1
                    placed_blocks[block.x_position + active_block_formation.x_current_tile][block.y_position + active_block_formation.y_current_tile] = True
                available_block_formations[current_block_formation] = Available_Block_Formation(get_random_formation(), -4, 8 * current_block_formation, current_block_formation)

                active_block_formation = Block_Formation(0, 0, available_block_formations[current_block_formation].formation)
                active_block_formation.move(0, 0)

                check_for_groups()
                clear_groups()
                update_possible_placed_blocks()
                check_for_possible_groups()
                check_available_formations_for_fit()
            elif event.button == 1:
                current_block_formation += 1
                if current_block_formation >= len(available_block_formations):
                    current_block_formation = 0
                active_block_formation = Block_Formation(0, 0, available_block_formations[current_block_formation].formation)
                active_block_formation.move(0, 0)

                check_for_groups()
                clear_groups()
                update_possible_placed_blocks()
                check_for_possible_groups()
            elif event.button == 8:
                in_game = False
                game_running = False
            # print(f"Button {event.button} pressed")
        elif event.type == pygame.JOYDEVICEADDED:
            added_joystick = pygame.joystick.Joystick(event.device_index)
            joysticks[added_joystick.get_instance_id()] = added_joystick
        elif event.type == pygame.JOYDEVICEREMOVED:
            del joysticks[event.instance_id]
        
    draw_all()

def draw_menu():
    SURFACE.fill(BLACK)
    
    pygame.draw.rect(SURFACE, GAME_VIEW_COLOR, GAME_VIEW_RECT)
    
    easy_color = WHITE
    if difficulty == 0:
        easy_color = ACTIVE_COLOR
    easy_text = SCORE_FONT.render("Easy", False, easy_color)
    easy_text_rect = easy_text.get_rect(center = (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.5 - 30))
    SURFACE.blit(easy_text, easy_text_rect)

    hard_color = WHITE
    if difficulty == 1:
        hard_color = ACTIVE_COLOR
    hard_text = SCORE_FONT.render("Hard", False, hard_color)
    hard_text_rect = hard_text.get_rect(center = (SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.5 + 30))
    SURFACE.blit(hard_text, hard_text_rect)
    
    pygame.display.update()

def handle_menu_events():
    global game_running
    global in_menu

    global wait_for_joystick_release

    for joystick in joysticks.keys():
        x_joystick_input = joysticks[joystick].get_axis(0)
        y_joystick_input = joysticks[joystick].get_axis(1)
        if abs(x_joystick_input) > 0.5 or abs(y_joystick_input) > 0.5:
            if not wait_for_joystick_release: # Joystick move action
                wait_for_joystick_release = True

                global difficulty
                difficulty += math.ceil(y_joystick_input)
                if difficulty > 1:
                    difficulty = 0
                elif difficulty < 0:
                    difficulty = 1
        else:
            if wait_for_joystick_release:
                wait_for_joystick_release = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            in_menu = False
            game_running = False
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                in_menu = False
            elif event.button == 8:
                in_menu = False
                game_running = False
        elif event.type == pygame.JOYDEVICEADDED:
            added_joystick = pygame.joystick.Joystick(event.device_index)
            joysticks[added_joystick.get_instance_id()] = added_joystick
        elif event.type == pygame.JOYDEVICEREMOVED:
            del joysticks[event.instance_id]
        
    draw_menu()

def main():
    global game_running
    global in_menu

    global active_block_formation
    global current_block_formation

    while game_running:

        in_menu = True

        while in_menu:
            handle_menu_events()

            CLOCK.tick(FRAME_RATE)

        load_high_scores()
        start_game()

        while in_game:
            handle_in_game_events()

            CLOCK.tick(FRAME_RATE)

if __name__ == "__main__":
    main()
    pygame.quit()