import pygame as pg
import random
import time
from datetime import datetime
import math

pg.init()

scale = 9                                           # size of a cell
maze_size = (192,108)                               # full size of the maze (x,y)
randomize_starting_point = True                     # start in the upper left corner, or in a random point in the maze
fullscreen = False                                  # pretty self explainatory                                
rainbowmode = True                                  # randomize the color for each cell
show_generation = True                              # the program shows the generation progress while it's happening. slower.
generation_delay = 0.01                             # GD: how much time does the program wait before calculating the next move       
wallpaper_mode = True                               # GD: if the generation should restart as soon as the maze is completed
frameskips = 5                                      # GD: when skipping (SPACE), how many frames does the program jump
save_screenshot = False                             # GD: save a screenshot when the maze has been completed
background_color = (0,0,0)                          # pretty self explainatory
wall_color = (255,255,255)                          # pretty self explainatory 
background_color2 = (255,255,255)                   # GD: the generator "head"'s color


if not show_generation:
    wallpaper_mode = False   
displaysize = (maze_size[0]*scale+3,maze_size[1]*scale+3)
if fullscreen:
    display = pg.display.set_mode(displaysize,flags=pg.FULLSCREEN)
else:
    display = pg.display.set_mode(displaysize)
pg.mouse.set_visible(False)
cur_color = wall_color
frameskip_counter = [0,frameskips]


def generate_maze():
    global cells,wall_color,frameskip_counter
    cells = [[maze_piece(row, col) for col in range(maze_size[0])] for row in range(maze_size[1])]
    stack = []
    if randomize_starting_point:
        starting_cell = cells[random.randint(0,maze_size[1]-1)][random.randint(0,maze_size[0]-1)]
    else:
        starting_cell = cells[0][0]
    starting_cell.visited = True
    stack.append(starting_cell)
    
    while stack:
        cur_cell = stack[-1]
        neighbors = check_neighbors(cur_cell)
        if neighbors:
            target = random.choice(neighbors)
            unwall(cur_cell,target)
            target.visited = True
            stack.append(target)
        else:
            stack.pop()

        if show_generation:

            x = cur_cell.col * scale+1
            y = cur_cell.row * scale+1
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    dead = True


            if pg.key.get_pressed()[pg.K_SPACE]:
                if frameskip_counter[0]==frameskip_counter[1]:
                    frameskip_counter[0]=0
                    display.fill(background_color)
                    draw_maze()
                    pg.draw.rect(display,background_color2,(x,y,scale,scale))
                    pg.display.update()
                    time.sleep(generation_delay)
                else:
                    frameskip_counter[0]+=1
            else:
                display.fill(background_color)
                draw_maze()
                pg.draw.rect(display,background_color2,(x,y,scale,scale))
                pg.display.update()
                time.sleep(generation_delay)            


    if save_screenshot:
        display.fill(background_color)
        draw_maze()
        pg.display.update()                
        img_name = "mazes/Maze - "+str(random.randint(0,99999999))+".png"
        pg.image.save(display,img_name)
        print(img_name,"saved.")


def draw_maze():
    for row in cells:
        for cell in row:
            cell.draw_self()

        

def check_neighbors(cell):
    neighbors = []
    if cell.row > 0 and not cells[cell.row - 1][cell.col].visited: # up
        neighbors.append(cells[cell.row - 1][cell.col])
        
    if cell.col > 0 and not cells[cell.row][cell.col - 1].visited: # left
        neighbors.append(cells[cell.row][cell.col - 1])

    if cell.row < maze_size[1] - 1 and not cells[cell.row + 1][cell.col].visited: # down
        neighbors.append(cells[cell.row + 1][cell.col])

    if cell.col < maze_size[0] - 1 and not cells[cell.row][cell.col + 1].visited: # right
        neighbors.append(cells[cell.row][cell.col + 1])
    return neighbors

def unwall(start, goal):
    if start.col == goal.col:  # same column
        if start.row > goal.row:  # below
            start.walls[0] = False
            goal.walls[2] = False
        else:  # above
            start.walls[2] = False
            goal.walls[0] = False
    elif start.row == goal.row:  # same row
        if start.col > goal.col:  # right
            start.walls[1] = False
            goal.walls[3] = False
        else:  # left
            start.walls[3] = False
            goal.walls[1] = False

def next_color(rgb): #bygpt
    r, g, b = rgb
    
    # Convert RGB to a single angle in radians
    angle = math.atan2(math.sqrt(3) * (g - b), 2 * r - g - b)
    
    # Adjust the angle to move to the next color in the rainbow sequence
    angle += math.radians(15)  # 15 degrees per color
    
    # Convert back to RGB
    r_new = (math.cos(angle) + 1) * 127.5
    g_new = (math.cos(angle - 2 * math.pi / 3) + 1) * 127.5
    b_new = (math.cos(angle + 2 * math.pi / 3) + 1) * 127.5
    return int(r_new), int(g_new), int(b_new)



class maze_piece:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.walls = [True, True, True, True]  # Up, Left, Down, Right
        self.visited = False
        self.colorwall = wall_color
        self.solved = False

        

    def draw_self(self):
        global cur_color
        x = self.col * scale+1
        y = self.row * scale+1
        if rainbowmode:
            self.colorwall = next_color(cur_color)
            cur_color = self.colorwall
        if self.visited:
#            pg.draw.rect(display,colorback,(x,y,scale,scale))
            if self.walls[0]:
                pg.draw.line(display, self.colorwall, (x, y), (x + scale, y), 1)  # Up
            if self.walls[1]:
                pg.draw.line(display, self.colorwall, (x, y), (x, y + scale), 1)  # Left
            if self.walls[2]:
                pg.draw.line(display, self.colorwall, (x, y + scale), (x + scale, y + scale), 1)  # Down
            if self.walls[3]:
                pg.draw.line(display, self.colorwall, (x + scale, y), (x + scale, y + scale), 1)  # Right


     



def main():
    global dead,cells
    dead = False
    roundCount = -1
    generate_maze()

    if wallpaper_mode:
        while True:
            roundCount += 1
            generate_maze()
##            print("Done!")
##            if save_screenshot:
##                img_name = "Maze - "+str(roundCount)+".png"
##                pg.image.save(display,img_name)
##                print(img_name,"saved.")

    else:    
        while not dead:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    dead = True
                if event.type == pg.KEYDOWN and event.key == pg.K_r:
                    
                    generate_maze()


                display.fill(background_color)
                draw_maze()
                pg.display.update()
            
            


main()




