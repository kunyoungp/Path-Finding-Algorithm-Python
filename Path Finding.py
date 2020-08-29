import pygame as pg
vec = pg.math.Vector2

TILESIZE = 12
GRIDWIDTH = 48
GRIDHEIGHT = 36
WIDTH = TILESIZE * GRIDWIDTH
HEIGHT = TILESIZE * GRIDHEIGHT
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
DARKGRAY = (40, 40, 40)
LIGHTGRAY = (140, 140, 140)
EMPTY = []

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []
        self.start = []
        self.finish = []
        self.exploring = []
        self.explored = []
        self.to_explore = []
        self.solution = []
        self.path = []
        self.connections = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1)]

    def in_bounds(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    def passable(self, node):
        return node not in self.walls

    def find_neighbors(self, node):
        neighbors = [node + connection for connection in self.connections]
        neighbors = filter(self.in_bounds, neighbors)
        neighbors = filter(self.passable, neighbors)
        return neighbors

    def draw(self):
        for wall in self.walls:
            rect = pg.Rect(wall * TILESIZE, (TILESIZE, TILESIZE))
            pg.draw.rect(screen, LIGHTGRAY, rect)
        for start in self.start:
            rect = pg.Rect(start * TILESIZE, (TILESIZE, TILESIZE))
            pg.draw.rect(screen, RED, rect)
        for finish in self.finish:
            rect = pg.Rect(finish * TILESIZE, (TILESIZE, TILESIZE))
            pg.draw.rect(screen, GREEN, rect)
        for exploring in self.exploring:
            rect = pg.Rect(exploring * TILESIZE, (TILESIZE, TILESIZE))
            pg.draw.rect(screen, YELLOW, rect)
        for explored in self.explored:
            rect = pg.Rect(explored * TILESIZE, (TILESIZE, TILESIZE))
            pg.draw.rect(screen, CYAN, rect)
        for to_explore in self.to_explore:
            rect = pg.Rect(to_explore * TILESIZE, (TILESIZE, TILESIZE))
            pg.draw.rect(screen, MAGENTA, rect)
        for solution in self.solution:
            rect = pg.Rect(solution * TILESIZE, (TILESIZE, TILESIZE))
            pg.draw.rect(screen, RED, rect)

def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(screen, LIGHTGRAY, (0, y), (WIDTH, y))

g = SquareGrid(GRIDWIDTH, GRIDHEIGHT)

def path_finding():
    g.exploring.append(g.start[0])
    path_counter = 1
    path=[g.start]
    Found=False
    while(not Found):
        for node in g.exploring:
            next_node1 = vec(int(node[0]) + 1, int(node[1]))
            next_node2 = vec(int(node[0]), int(node[1]) + 1)
            next_node3 = vec(int(node[0]) - 1, int(node[1]))
            next_node4 = vec(int(node[0]), int(node[1]) - 1)

            if next_node1 in g.finish:
                for solution in path:
                    if solution[-1]==node:
                        g.solution = solution
                Found=True
            elif next_node2 in g.finish:
                for solution in path:
                    if solution[-1]==node:
                        g.solution = solution
                Found=True
            elif next_node3 in g.finish:
                for solution in path:
                    if solution[-1]==node:
                        g.solution = solution
                Found=True
            elif next_node4 in g.finish:
                for solution in path:
                    if solution[-1]==node:
                        g.solution = solution
                Found=True
            else:
                g.explored.append(node)
                if next_node1 not in g.to_explore:
                    if next_node1 not in g.walls and next_node1 not in g.explored:
                        g.to_explore.append(next_node1)
                        for i in path:
                            if i[-1]==node:
                                j=[]
                                for item in i:
                                    j.append(item)
                                j.append(next_node1)
                                path.append(j)
                                break
                if next_node2 not in g.to_explore:
                    if next_node2 not in g.walls and next_node2 not in g.explored:
                        g.to_explore.append(next_node2)
                        for i in path:
                            if i[-1]==node:
                                j = []
                                for item in i:
                                    j.append(item)
                                j.append(next_node2)
                                path.append(j)
                                break
                if next_node3 not in g.to_explore:
                    if next_node3 not in g.walls and next_node3 not in g.explored:
                        g.to_explore.append(next_node3)
                        for i in path:
                            if i[-1]==node:
                                j = []
                                for item in i:
                                    j.append(item)
                                j.append(next_node3)
                                path.append(j)
                                break
                if next_node4 not in g.to_explore:
                    if next_node4 not in g.walls and next_node4 not in g.explored:
                        g.to_explore.append(next_node4)
                        for i in path:
                            if i[-1]==node:
                                j = []
                                for item in i:
                                    j.append(item)
                                j.append(next_node4)
                                path.append(j)
                                break
        g.exploring = g.to_explore
        g.to_explore=[]
        path_counter += 1
        temp_path = []
        for paths in path:
            if len(paths)==path_counter:
                temp_path.append(paths)
        path = temp_path
    print(path_counter)

walls = []
for i in range(GRIDWIDTH):
    walls.append((i,0))
    walls.append((i,GRIDHEIGHT-1))

for i in range(GRIDHEIGHT-2):
    walls.append((0,i+1))
    walls.append((GRIDWIDTH-1,i+1))

startingPos = []
for wall in walls:
    g.walls.append(vec(wall))
running = True
while running:
    clock.tick(FPS)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_m:
                # dump the wall list for saving
                print([(int(loc.x), int(loc.y)) for loc in g.walls])
            if event.key == pg.K_s:
                mpos = vec(pg.mouse.get_pos()) // TILESIZE
                if mpos in g.walls:
                    g.walls.remove(mpos)
                if g.start!=EMPTY:
                    g.start.pop()
                g.start.append(mpos)
            if event.key == pg.K_f:
                mpos = vec(pg.mouse.get_pos()) // TILESIZE
                if mpos in g.walls:
                    g.walls.remove(mpos)
                if g.finish!=EMPTY:
                    g.finish.pop()
                g.finish.append(mpos)
            if event.key == pg.K_g:
                path_finding()

        if event.type == pg.MOUSEBUTTONDOWN:
            mpos = vec(pg.mouse.get_pos()) // TILESIZE
            if event.button == 1:
                if mpos in g.walls:
                    g.walls.remove(mpos)
                else:
                    g.walls.append(mpos)

    pg.display.set_caption("{:.2f}".format(clock.get_fps()))
    screen.fill(DARKGRAY)
    draw_grid()
    g.draw()
    pg.display.flip()