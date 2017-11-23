#!/usr/bin/python
# BFS search algorithm for pacman, by Matthew Schieber

#!/usr/bin/python
def bfs(r, c, pacman_r, pacman_c, food_r, food_c, grid):

    # setup
    search_stack = [(pacman_r, pacman_c)]
    bfs = []
    found = False
    paths = {}
    paths[pacman_r, pacman_c] = [(pacman_r, pacman_c)]
    
    # search
    while(not found):
        
        location = search_stack[0]
        del search_stack[0]
        path = paths[location]       
        
        if(not (location in bfs)):
            bfs.append(location)
            lr = location[0]
            lc = location[1]
            if(grid[lr][lc] == '.'):
                found = True
                continue
            
            # up
            if(lr - 1 >= 0):
                dest = (lr - 1, lc)
                val = grid[dest[0]][dest[1]]
                if(val != '%' and (not (dest in search_stack))):
                    paths[dest] = path + [dest]
                    search_stack.append(dest)
        
            # left
            if(lc - 1 >= 0):
                dest = (lr, lc - 1)        
                val = grid[dest[0]][dest[1]]
                if(val != '%' and (not (dest in search_stack))):
                    paths[dest] = path + [dest]
                    search_stack.append(dest)
         
            # right
            if(lc + 1 < c):
                dest = (lr, lc + 1)        
                val = grid[dest[0]][dest[1]]
                if(val != '%' and (not (dest in search_stack))):
                    paths[dest] = path + [dest]
                    search_stack.append(dest)
        
            # down
            if(lr + 1 < r):
                dest = (lr + 1, lc)        
                val = grid[dest[0]][dest[1]]
                if(val != '%' and (not (dest in search_stack))):
                    paths[dest] = path + [dest]
                    search_stack.append(dest)
        
    # workup
    print (len(bfs))
    for i in bfs:
        print ("%d %d" % (i[0], i[1]))
        
    destination = (food_r, food_c)
    print (len(paths[destination]) - 1)
    for i in paths[destination]:
        print ("%d %d" % (i[0], i[1]))
    return


pacman_r, pacman_c = [ int(i) for i in raw_input().strip().split() ]
food_r, food_c = [ int(i) for i in raw_input().strip().split() ]
r,c = [ int(i) for i in raw_input().strip().split() ]

grid = []
for i in xrange(0, r):
    grid.append(raw_input().strip())

bfs(r, c, pacman_r, pacman_c, food_r, food_c, grid)

