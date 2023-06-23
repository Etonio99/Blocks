import pygame, random

pygame.init()
pygame.display.set_caption('Blocks')

class Block:
    def __init__(self, x_position, y_position):
        self.x_position = x_position
        self.y_position = y_position

class Block_Formation:
    def __init__(self, x_current_tile, y_current_tile, formation):
        self.x_current_tile = x_current_tile
        self.y_current_tile = y_current_tile
        
        self.formation = formation
        self.blocks = []
        
        self.width = len(self.formation[0])
        self.height = len(self.formation)
        print(self.width, self.height)
        
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
    
    def draw(self):
        for BLOCK in self.blocks:
            X_POSITION = GAME_VIEW_X + BLOCK_WIDTH * (BLOCK.x_position + self.x_current_tile) + BLOCK_PADDING * (BLOCK.x_position + self.x_current_tile + 1)
            Y_POSITION = GAME_VIEW_Y + BLOCK_WIDTH * (BLOCK.y_position + self.y_current_tile) + BLOCK_PADDING * (BLOCK.y_position + self.y_current_tile + 1)
            pygame.draw.rect(SURFACE, WHITE, (X_POSITION, Y_POSITION, BLOCK_WIDTH, BLOCK_WIDTH))

BLOCK_SHAPES = [
    [
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
        "-X-",
        "XXX"
    ]
]

CLOCK = pygame.time.Clock()
FRAME_RATE = 30
SCREEN_WIDTH, SCREEN_HEIGHT = (900, 600)
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

placed_blocks = []

for y in range(BOARD_WIDTH):
    placed_blocks.append([])
    for x in range(BOARD_WIDTH):
        placed_blocks[y].append(False)
        BG_BLOCKS.append(pygame.rect.Rect(GAME_VIEW_X + BLOCK_WIDTH * x + BLOCK_PADDING * (x + 1), GAME_VIEW_Y + BLOCK_WIDTH * y + BLOCK_PADDING * (y + 1), BLOCK_WIDTH, BLOCK_WIDTH))

def draw_all():
    SURFACE.fill(BLACK)
    
    pygame.draw.rect(SURFACE, GAME_VIEW_COLOR, GAME_VIEW_RECT)
    
    iterator = 0
    line_counter = 0
    for BLOCK in BG_BLOCKS:
        
        color_1 = BG_BLOCK_BRIGHT
        color_2 = BG_BLOCK_DARK
        
        if line_counter >= 3 and line_counter < 6:
            color_1, color_2 = color_2, color_1

        if iterator < 3 or iterator >= 6:
            pygame.draw.rect(SURFACE, color_1, BLOCK)
        else:
            pygame.draw.rect(SURFACE, color_2, BLOCK)
        
        iterator += 1
        if iterator >= 9:
            iterator = 0
            line_counter += 1
    
    active_block_formation.draw()
    
    pygame.display.update()

wait_for_joystick_release = False

def main():
    global game_running
    game_running = True

    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 6:
                    game_running = False
                print(f"Button {event.button} pressed")
            # elif event.type == pygame.JOYBUTTONUP:
                # print(f"Button {event.button} released")
            elif event.type == pygame.JOYDEVICEADDED:
                added_joystick = pygame.joystick.Joystick(event.device_index)
                joysticks[added_joystick.get_instance_id()] = added_joystick
                # print(f"Joystick {added_joystick.get_instance_id()} connected")
            elif event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                # print(f"Joystick {event.instance_id} disconnected")

        global wait_for_joystick_release

        x_joystick_input = joysticks[0].get_axis(0)
        y_joystick_input = joysticks[0].get_axis(1)
        if abs(x_joystick_input) > 0.5 or abs(y_joystick_input) > 0.5:
            if not wait_for_joystick_release:
                active_block_formation.move(round(x_joystick_input), round(y_joystick_input))
                wait_for_joystick_release = True
        else:
            if wait_for_joystick_release:
                wait_for_joystick_release = False
            
        draw_all()

        CLOCK.tick(FRAME_RATE)

if __name__ == "__main__":
    main()
    pygame.quit()