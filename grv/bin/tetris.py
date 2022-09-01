# ....................................................................................................#

    # create_tetris__ : create screen with width, height and title

    # get_input__ : polls event one by one (try to make it string type)

    # row_cleared__ : number of rows cleared 

    # get_block__ : new block of desired shape, color, rotation
    # block_fixed__ : tells wheater block has been fixed or not

    # move_down__ : moves current block on screen down
    # move_left__ : moves current block to left 
    # move_right__ : moves current block to right 
    # rotate__ : rotates piece

    # game_ended__ : tells if game has ended or not

    # game_time__ : gets clock of game

    # get_random__ : gives random number in range l to r

    # print_grid__ : prints grid

# ....................................................................................................#

    # Block Class:
        # block corrdinates 
        # block color
        # block rotation
        # block type

    # Grid Mainpulation Class : 
        # grid structure, 
        # current block, 
        # move / rotate block method
        # clear block (called automatically after move or rotate and update cleared rows)

    # Update Screen Methods
        # draw grid on screen with border and lines 

    # create_tetris__ :
        # create screen of desired size and name
        # create global grid object
        # create global constants (like play size, etc)
        # start clock

    # get_block__ : 
        # gets new block in grid object (changes current block)
        # can get block of desired shape and size

    # get_time__ : tells game time

    # game_ended__ : tells if game has ended or not
    
# ....................................................................................................#

import pygame
import random

# utility function
def get_random__(l, r):
    return random.randint(l, r)

#Shapes of the blocks
shapes = {
        'I' : [[1, 5, 9, 13], [4, 5, 6, 7]],
        'Z' : [[4, 5, 9, 10], [2, 6, 5, 9]],
        'S' : [[6, 7, 9, 10], [1, 5, 6, 10]],
        'J' : [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        'L' : [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        'T' : [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        'O' : [[1, 2, 5, 6]]
}
shape_letters = [
    'I', 'Z', 'S', 'J', 'L', 'T', 'O'
]

#Colors of the blocks
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

# number of blocks vertically and horizontally
blocks_horz = 10
blocks_vert = 20

# x, y corrdinates 
top_left_x = 0
top_left_y = 0

# Block Class
class Block:
    def __init__(self, row, col, rotation, color, type):
        self.x = col
        self.y = row
        self.type = shape_letters[type]
        self.color = shape_colors[color]
        self.cleared = 0
        self.rotation = rotation

# Grid Class
class Grid:
    def __init__(self):
        # col then row
        self.grid = []
        for _ in range(20):
            row = []
            for _ in range(10):
                row.append((0,0,0))
            self.grid.append(row)
        self.current_block = None
        self.cleared = 0
        self.locked_positions = {}
    
    # move within boundry and no clashes with already present blocks
    def valid_space(self):
        accepted_positions = []
        for i in range(20):
            for j in range(10):
                if((i, j) not in self.locked_positions):
                    accepted_positions.append((i, j))
        formatted = self.get_corrdinates()
    
        for pos in formatted:
            if pos not in accepted_positions:
                    return False
        return True

    # move current block to left if possible
    def move_left(self):
        self.current_block.x -= 1
        if not self.valid_space():
            self.current_block.x += 1
        return 

    # move current block to right if possible
    def move_right(self):
        self.current_block.x += 1
        if not self.valid_space():
            self.current_block.x -= 1
        return 

    # move current block down if possible
    def move_down(self):
        self.current_block.y += 1
        if not self.valid_space():
            self.current_block.y -= 1
            self.block_fixed = True
        return

    # rotate current block if possible
    def rotate(self):
        self.current_block.rotation = (self.current_block.rotation + 1)% len(shapes[self.current_block.type])
        if not self.valid_space():
            self.current_block.rotation = (self.current_block.rotation - 1)% len(shapes[self.current_block.type])
        return
    
    # get corrdinates of shape
    def get_corrdinates(self):
        positions = []
        for i in range(4):
            for j in range(4):
                if(4*i + j in shapes[self.current_block.type][self.current_block.rotation]):
                    positions.append((self.current_block.y + i, self.current_block.x + j))
        return positions

    # check if current block has been fixed
    def fixed(self):
        self.current_block.y += 1
        if not self.valid_space():
            self.current_block.y -= 1
            # (col, row)
            for pos in self.get_corrdinates():
                self.locked_positions[pos] = self.current_block.color
                self.grid[pos[0]][pos[1]] = self.current_block.color
            self.current_block = None
            for _ in range(20):
                self.clear_rows()
            return True
        self.current_block.y -= 1
        return False
    
    # get new block once fixed and cleared rows
    def new_block(self, rotation, color, type):
        self.current_block = Block(0, 5, rotation, color, type)
        return
    
    # clear rows 
    def clear_rows(self):
        idx = -1
        blocks_above = []
        # need to see if row is clear the shift every other row above down one
        for i in range(len(self.grid)-1,-1,-1):
            row = self.grid[i]
            if (0, 0, 0) not in row:
                self.cleared += 1
                idx = i
                self.cleared += 1
                # add positions to remove from locked
                for j in range(len(row)):
                    try:
                        del self.locked_positions[(i, j)]
                    except:
                        continue
                # decrease all the indexes in locked where row number is smaller than i
                for pos in self.locked_positions:
                    if(pos[0] < i):
                        blocks_above.append(pos)
                break
        
        blocks_above.sort(reverse=True)
        for pos in blocks_above:
            try:
                self.locked_positions[(pos[0]+1, pos[1])] = self.locked_positions[pos]
                del self.locked_positions[(pos[0], pos[1])]
            except:
                continue

        for i in range(idx, -1, -1):
            for j in range(10):
                self.grid[i][j] = (0, 0, 0)

        for pos in blocks_above:
            self.grid[pos[0]+1][pos[1]] = self.locked_positions[(pos[0]+1, pos[1])]
    
    def check_lost(self):
        for pos in self.locked_positions:
            if pos[0] < 1:
                return True
        return False

#.....................................................................................................#

def get_inputs__():
    # for loop through the event queue 
    ip = pygame.event.poll()
    if(ip.type == pygame.QUIT):
        return 'QUIT'
    
    if(ip.type == pygame.KEYDOWN):
        if(pygame.key.get_mods() & pygame.KMOD_SHIFT):
            if(ip.key == pygame.K_UP):
                return 'SHIFT + K_UP'
            elif(ip.key == pygame.K_LEFT):
                return 'SHIFT + K_LEFT'
            elif(ip.key == pygame.K_RIGHT):
                return 'SHIFT + K_RIGHT'
            elif(ip.key == pygame.K_DOWN):
                return 'SHIFT + K_DOWN'
        else:
            if(ip.key == pygame.K_UP):
                return 'K_UP'
            elif(ip.key == pygame.K_LEFT):
                return 'K_LEFT'
            elif(ip.key == pygame.K_RIGHT):
                return 'K_RIGHT'
            elif(ip.key == pygame.K_DOWN):
                return 'K_DOWN'
    
    return 'OTHERS'

def get_block__(r=None, c=None, t=None):
    if(r != None):
        rotation = r
    else:
        rotation = 0
    if(c != None):
        color = c
    else:
        color = random.randint(0, 6)
    if(t != None):
        type = t
    else:
        type = random.randint(0, 6)
    grid.new_block(rotation, color, type)

def block_fixed__():
    return grid.fixed()

def move_down__():
    grid.move_down()
    return

def move_left__():
    grid.move_left()
    return 

def move_right__():
    grid.move_right()
    return

def rotate__():
    grid.rotate()
    return

def lost_game__():
    return grid.check_lost()

def rows_cleared__():
    return grid.cleared
    
def end_game__():
    pygame.display.quit()
    return

def print_grid__():
    g = grid.grid
    for x in range(20):
        for y in range(10):
            print(g[x][y], end=' ')
        print(end='\n')
    return

# ....................................................................................................#

# draw horizontal and vertical lines
def draw_grid(row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(screen, (128,128,128), (sx, sy+ i*block_size), (sx + s_width, sy + i * block_size))  # horizontal lines
    for j in range(col):
        pygame.draw.line(screen, (128,128,128), (sx + j * block_size, sy), (sx + j * block_size, sy + s_height))  # vertical lines

# draw color at each block
def draw_window():
    screen.fill((0,0,0))
    
    # color grid
    g = grid.grid
    for i in range(len(g)):
        for j in range(len(g[i])):
            pygame.draw.rect(screen, g[i][j], (top_left_x + j* block_size, top_left_y + i * block_size, block_size, block_size), 0)

    # draw block
    pos = grid.get_corrdinates()
    for p in pos:
        pygame.draw.rect(screen, grid.current_block.color, (top_left_x + p[1]* block_size, top_left_y + p[0] * block_size, block_size, block_size), 0)

    # draw grid boundaries
    draw_grid(20, 10)
    pygame.draw.rect(screen, (255, 0, 0), (top_left_x, top_left_y, s_width, s_height), 1)

# render game
def render_game__():
    draw_window()
    pygame.display.update()

# creates screen and blocks and grid
def create_tetris__(width, game_name='Tetris'):    
    # number of rows cleared
    global cleared
    cleared = 0

    # keep aspect ratio (2:1)
    height = 2*width

    # make global screen
    global screen
    screen = pygame.display.set_mode((width, height))

    # set some global variables
    global s_width
    s_width = width
    global s_height
    s_height = height
    global block_size
    block_size = s_width / 10

    # set game name
    pygame.display.set_caption(game_name)

    # grid object
    global grid
    grid = Grid()
