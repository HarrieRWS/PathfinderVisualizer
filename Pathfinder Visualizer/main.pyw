##########################################
#        Author: Harrie Spurway          #
##########################################

##########################################
#               Imports                  # 
##########################################
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import tkinter as tk
import time
from queue import PriorityQueue
from collections import deque
import random

##########################################
# Node Colours/Window Width/Alg Records  # 
##########################################
#Window width and number of rows
ROWS = 40
width = ROWS * 17

#Colours
red, green, white, black, purple, orange, grey, pink = (255, 0, 0), (0, 255, 0), (255, 255, 255), (0, 0, 0), (128, 0, 128), (255, 165 ,0), (128, 128, 128), (255,105,180)

#Dictionairy recording of all alogrithms, this will be displayed on the report page
bfsDict = {"endNode": "Not Found","pathSuccess": "None","time" : 0,	"lenPath" : 0, "nodesTraverse" : 0}
dfsDict = {"endNode": "Not Found","pathSuccess": "None","time" : 0,"lenPath" : 0,"nodesTraverse" : 0}
aStarDict = {"endNode": "Not Found","pathSuccess": "None","time" : 0,"lenPath" : 0,"nodesTraverse" : 0}
dijkstraDict = {"endNode": "Not Found","pathSuccess": "None","time" : 0,"lenPath" : 0,"nodesTraverse" : 0}	

##########################################
#           Node Placement Class         # 
##########################################
class Node:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.colour = white
		self.neighbours = []
		self.width = width
		self.total_rows = total_rows
		self.prev = None
		self.visited = False

	def get_pos(self):
		return self.row, self.col

	def up (self):
		self.col -= 1
	def down(self):
		self.col == 1
	def left(self):
		self.row -= 1
	def right(self):
		self.row += 1

	def is_closed(self):
		return self.colour== red

	def is_open(self):
		return self.colour== green

	def is_barrier(self):
		return self.colour== black

	def is_start(self):
		return self.colour== orange

	def is_end(self):
		return self.colour == pink

	def is_path(self):
		return self.colour == purple

	def reset(self):
		self.colour= white

	def make_start(self):
		self.colour= orange

	def make_barrier(self):
		self.colour= black

	def make_closed(self):
		self.colour= red

	def make_open(self):
		self.colour= green

	def make_end(self):
		self.colour = pink

	def make_path(self):
		self.colour = purple

	def draw(self, win):
		pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

	def update_neighbours(self, grid):
		self.neighbours = []
		#Check for left neighbour
		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
			self.neighbours.append(grid[self.row][self.col - 1])
		#Check for below neighbour
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
			self.neighbours.append(grid[self.row + 1][self.col])
		#Check for above neighbour
		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
			self.neighbours.append(grid[self.row - 1][self.col])
		#Check for right neighbour
		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
			self.neighbours.append(grid[self.row][self.col + 1])
	
	def __lt__(self, other):
		return False

##########################################
#              Grid Options              #
##########################################

#Grid Creation
def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, grey, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, grey, (j * gap, 0), (j * gap, width))

#To update the grid
def draw(win, grid, rows, width):
	win.fill(white)
	for row in grid:
		for nodePlacement in row:
			nodePlacement.draw(win)
	draw_grid(win, rows, width)
	pygame.display.update()

#To clear the grid
def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			nodePlacement = Node(i, j, gap, rows)
			grid[i].append(nodePlacement)
	return grid

#To clear the grid, does not clear obstacles / barriers / start node / end node
def resetGrid(grid, rows):
	for i in range(rows):
		for j in range(rows):
			if grid[i][j].is_path() or grid[i][j].is_open() or grid[i][j].is_closed():
				grid[i][j].reset()
			grid[i][j].visited = False
	return grid

##########################################
#              Map Creation              # 
##########################################
#Creates a random map
def randomMap(draw, rows, width):
	grid = make_grid(rows, width)
	numbers = [0, 1, 2, 3, 4, 5]
	#Creates a wall around the grid
	for i in range(rows):
		grid[0][i].make_barrier()
		grid[rows - 1][i].make_barrier()
		grid[i][0].make_barrier()
		grid[i][rows - 1].make_barrier()
		draw()

	for i in range(rows):
		for j in range(rows):
			x = random.choice(numbers)
			#Will provide a 1 in 3 chance of creating a barrier for each node
			if x is numbers[0] or x is numbers[1]:
				grid[i][j].make_barrier()
			
	return grid

##########################################
#            Node placement              #
##########################################
def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	#Using integer division for row and column
	row = y // gap
	col = x // gap

	return row, col
				
##########################################
#        Breadth First Search            #
##########################################
def bfs(draw, start, end):
	bfsDict["endNode"], bfsDict["nodesTraverse"] = "Not Found", 0
	queue, path, visited = deque(), [], []
	queue.append(start)
	visited.append(start)
	x = 0
	flag= False
	
	while len(queue) > 0:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		current = queue.popleft()
		if flag == False:
			for i in current.neighbours:
				if current == end:
					#For the report
					bfsDict["endNode"] = "Found"		
					return True
				if not i in visited and not i.is_barrier():
						visited.append(i)
						i.prev = current
						queue.append(i)
						i.make_open()
						#For the report
						bfsDict["nodesTraverse"] += 1
				else:
					i.make_closed()
				end.make_end()
				start.make_start()
		x += 1
		if x % 6 ==0:
			draw()
	draw()
	return False
		

##########################################
#           A* algorithm                 #
##########################################
#The A* Heuristic
def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

#The A* Path Maker
def reconstruct_path(came_from, current, draw, alg):
	x = 0
	aStarDict["lenPath"], aStarDict["pathSuccess"] = x, "None"
	
	while current in came_from:
		current = came_from[current]
		current.make_path()
		x += 1
	draw()
	#For the report
	if alg == "aStar":
		aStarDict["lenPath"] = x
		aStarDict["pathSuccess"] = "Success"

#A star algorithm
def aStar(draw, grid, start, end):
	aStarDict["endNode"], aStarDict["nodesTraverse"] = "Not Found", 0
	start.make_start()
	end.make_end()
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {nodePlacement: float("inf") for row in grid for nodePlacement in row}
	g_score[start] = 0
	f_score = {nodePlacement: float("inf") for row in grid for nodePlacement in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw, "aStar")
			end.make_end()
			start.make_start()
			#For the report
			aStarDict["endNode"] = "Found"
			aStarDict["nodesTraverse"] += 1
			return True

		for neighbour in current.neighbours:
			temp_g_score = g_score[current] + 1
			if temp_g_score < g_score[neighbour]:
				came_from[neighbour] = current
				g_score[neighbour] = temp_g_score
				f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
				if neighbour not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbour], count, neighbour))
					open_set_hash.add(neighbour)
					neighbour.make_open()
					#For the report
					aStarDict["nodesTraverse"] += 1
		draw()
		if current != start:
			current.make_closed()
	return False

##########################################
#              Dijkstra                  #
##########################################
def dijkstra(draw, start, end):
	#Reset the dictionary values
	dijkstraDict["endNode"], dijkstraDict["lenPath"], dijkstraDict["pathSuccess"], dijkstraDict["nodesTraverse"]  = "Not Found", 0, "None", 0
	x = 0
	queue, path, visited,flag = deque(), [], [], False

	queue.append(start)
	visited.append(start)
 
	while len(queue) > 0:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		current = queue.popleft()
		if current == end:
			temp = current
			dijkstraDict["endNode"] = "Found"
			while temp.prev:
				path.append(temp.prev)
				temp.prev.make_path()
				temp = temp.prev
				#For the report
				dijkstraDict["pathSuccess"] = "Success"
				dijkstraDict["lenPath"] += 1
			return True
		if flag == False:
			for i in current.neighbours:
				if current == end:
					temp = current
					dijkstraDict["endNode"] = "Found"
					while temp.prev:
						path.append(temp.prev)
						temp.prev.make_path()
						temp = temp.prev
						#For the report
						dijkstraDict["pathSuccess"] = "Success"
						dijkstraDict["lenPath"] += 1
					return True
				if not i in visited and not i.is_barrier():
						visited.append(i)
						i.prev = current
						queue.append(i)
						i.make_open()
						dijkstraDict["nodesTraverse"] += 1
				else:
					i.make_closed()
				end.make_end()
				start.make_start()
		x += 1
		if x % 6 ==0:
			draw()
	draw()		
	return False

##########################################
#          Depth First Search            #
##########################################
def dfs(draw, grid, start, end):
	dfsDict["endNode"], dfsDict["nodesTraverse"],  dfsDict["lenPath"], dfsDict["pathSuccess"] = "Not Found", 0, 0, "None"
	path, st = [], []
	st.append(start)

	while len(st) > 0:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		current = st[len(st) - 1]
		st.remove(st[len(st) - 1])
		if current == end:
			dfsDict["endNode"] = "Found"
			temp = current
			while temp.prev:
				path.append(temp.prev)
				temp.prev.make_path()
				temp = temp.prev
				#For the report
				dfsDict["pathSuccess"] = "Success"
				dfsDict["lenPath"] += 1
			draw()
			return True

		current.visited = True
		for i in current.neighbours:		
			if i == end:
				dfsDict["endNode"] = "Found"
				temp = current
				while temp.prev:
					path.append(temp.prev)
					temp.make_path()
					temp = temp.prev
					#For the report
					dfsDict["pathSuccess"] = "Success"
					dfsDict["lenPath"] += 1
				draw()
				return True
			if i.visited == False and not i.is_barrier():
				st.append(i)
				i.prev = current
				i.make_open()
				i.visited = True
				dfsDict["nodesTraverse"] += 1
			else:
				i.make_closed()

		draw()
		start.make_start()
		end.make_end()
	return False


##########################################
#      Time Conversion Formatting        #
##########################################
def time_convert(sec):
	sec = sec % 60
	return "{0}".format(round(sec, 5))

##########################################
#        Main for algorithm              #
##########################################
def main(win, width, bfsBool, dfsBool, aBool, dijkstraBool):
	grid = make_grid(ROWS, width)
	start, end, run, numOfAlg= None, None, True, 0
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				nodePlacement = grid[row][col]
				if not start and nodePlacement != end:
					start = nodePlacement
					start.make_start()
				elif not end and nodePlacement != start:
					end = nodePlacement
					end.make_end()
				elif nodePlacement != end and nodePlacement != start:
					nodePlacement.make_barrier()
			elif pygame.mouse.get_pressed()[2]: # Right click
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				nodePlacement = grid[row][col]
				nodePlacement.reset()
				if nodePlacement == start:
					start = None
				elif nodePlacement == end:
					end = None
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for nodePlacement in row:
							nodePlacement.update_neighbours(grid)
					if bfsBool.get():
						start_time = time.time()
						x = bfs(lambda: draw(win, grid, ROWS, width), start, end)
						messageBox(x, "BFS")
						start.make_start(), end.make_end()
						numOfAlg += 1
						end_time = time.time()
						times = time_convert((end_time - start_time))
						bfsDict["time"] = times
						pygame.time.wait(1000)
						resetGrid( grid, ROWS)
					if dfsBool.get():
						start_time = time.time()
						x = dfs(lambda: draw(win, grid, ROWS, width), grid, start, end)
						messageBox(x, "DFS")
						start.make_start(), end.make_end()
						numOfAlg += 1
						end_time = time.time()
						times = time_convert((end_time - start_time))
						dfsDict["time"] = times
						pygame.time.wait(1000)	
						resetGrid(grid, ROWS)
					if aBool.get():
						start_time = time.time()				
						x = aStar(lambda: draw(win, grid, ROWS, width), grid, start, end)
						messageBox(x, "A*")
						start.make_start(), end.make_end()
						numOfAlg += 1
						end_time = time.time() 
						times = time_convert((end_time - start_time))
						aStarDict["time"] = times
						pygame.time.wait(1000)
						resetGrid(grid, ROWS)			
					if dijkstraBool.get():
						start_time = time.time()
						x = dijkstra(lambda: draw(win, grid, ROWS, width), start, end)
						messageBox(x, "Dijkstra")
						start.make_start(), end.make_end()
						numOfAlg += 1
						end_time = time.time()
						times = time_convert((end_time - start_time))
						dijkstraDict["time"] = times
						pygame.time.wait(1000)
						resetGrid(grid, ROWS)
					report(bfsBool.get(), dfsBool.get(), aBool.get(), dijkstraBool.get())
				#Clear the visualizer screen
				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)
				#Return to the menu, closing the visualizer
				if event.key == pygame.K_m:
					pygame.quit()
					algMenu()
				#Creates a random map, start and end nodes are set to none				
				if event.key == pygame.K_r:
					start = None
					end = None
					grid = make_grid(ROWS, width)
					grid = randomMap(lambda: draw(win, grid, ROWS, width), ROWS, width)
	pygame.quit()
##########################################
#              Message Box               #
##########################################
def destoryMessage(window):
		window.destroy()

def messageBox(completion, algorithm):
	window = tk.Tk()
	window.title("Report Page")
	window.geometry("200x100")
	window['bg'] = "#1f1f1f"
	if completion == False:
		alg = algorithm + " No End Node"
		tk.Label(window, text= alg, bg="#1f1f1f", fg="White",font=("Courier", 10)).pack()
	else:
		alg = algorithm + " End Node Found"
		tk.Label(window, text= alg, bg="#1f1f1f", fg="White",font=("Courier", 10)).pack()


	tk.Label(window, bg="#1f1f1f").pack()
	tk.Button(width=20, height= 1,text="Submit", bg="black", fg="white",  command = lambda : destoryMessage(window)).pack()   
	window.mainloop()
##########################################
#             Report page                #
##########################################
def report(bfs, dfs, aStar, dijkstra):
	algList = [('Algorithm', 'End Node Search', 'Successful Path', 'Time to Complete', 'Length of Path', "Nodes Traversed")]

	if bfs:
		algList.append(('Breadth-First Search', bfsDict["endNode"], bfsDict["pathSuccess"], bfsDict["time"], bfsDict["lenPath"], bfsDict["nodesTraverse"]))
	if dfs:
		algList.append(('Depth-First Search', dfsDict["endNode"], dfsDict["pathSuccess"], dfsDict["time"], dfsDict["lenPath"], dfsDict["nodesTraverse"]))
	if aStar:
		algList.append(('A*', aStarDict["endNode"], aStarDict["pathSuccess"], aStarDict["time"], aStarDict["lenPath"], aStarDict["nodesTraverse"]))
	if dijkstra:
		algList.append(('Dijkstra', dijkstraDict["endNode"], dijkstraDict["pathSuccess"], dijkstraDict["time"], dijkstraDict["lenPath"], dijkstraDict["nodesTraverse"]))

	total_rows = len(algList)
	total_col = len(algList[0])
	
	#Root window
	window = tk.Tk()
	window.title("Report Page")
	geoStr = str((total_rows * 20) + 12)
	window.geometry("1090x"+geoStr)
	window['bg'] = "#1f1f1f"

	for i in range(total_rows):
		for j in range(total_col):
			if i ==0:
				entry = tk.Entry(window, width=20, bg='#1f1f1f',fg='White', font=('Arial', 12, 'bold'))
			else:
				entry = tk.Entry(window, width=20, fg='Black', font=('Arial', 12, ''))
			entry.grid(row=i, column=j)
			entry.insert(tk.END, algList[i][j])

	window.mainloop()
##########################################
#      Algorithm Menu Selection page     #
##########################################
def submitAction(window, bfsBool, dfsBool, aBool, dijkstraBool):
	if bfsBool.get() or dfsBool.get() or aBool.get() or dijkstraBool.get():
		window.destroy()
		WIN = pygame.display.set_mode((width, width))
		pygame.display.set_caption("Path Finder")
		main(WIN, width, bfsBool, dfsBool, aBool, dijkstraBool)

def algMenu():			
    #Window
	window = tk.Tk()
	window.title("Algorithm Selection")
	window.geometry("300x350")
	window['bg'] = "#1f1f1f"
	
	bfsBool,dfsBool, aBool, dijkstraBool = tk.BooleanVar(),tk.BooleanVar(),tk.BooleanVar(),tk.BooleanVar()
	tk.Label(window, bg="#1f1f1f").pack()
	tk.Label(window, text="TurnBotic",  bg="black", fg="white", font=("Courier", 20), pady=5, padx=20).pack()
	tk.Label(window, bg="#1f1f1f").pack()
	#Check what algorithm is wanted by the user
	tk.Checkbutton(window, text="Breadth First Search", bg="#1f1f1f", fg="white", selectcolor="black", font=("Courier", 15),variable=bfsBool, onvalue=True, offvalue=False ).pack()
	tk.Label(window, bg="#1f1f1f").pack()
	tk.Checkbutton(window, text="Depth First Search", bg="#1f1f1f", fg="white", selectcolor="black", font=("Courier", 15), variable=dfsBool, onvalue=True, offvalue=False).pack()
	tk.Label(window, bg="#1f1f1f").pack()
	tk.Checkbutton(window, text="A*", bg="#1f1f1f", fg="white", selectcolor="black",font=("Courier", 15), variable=aBool, onvalue=True, offvalue=False).pack()
	tk.Label(window, bg="#1f1f1f").pack()
	tk.Checkbutton(window, text="Dijkstra", bg="#1f1f1f",fg="white", selectcolor="black", font=("Courier", 15), variable=dijkstraBool, onvalue=True, offvalue=False).pack()
		
    #Main Menu Buttons
	tk.Label(window, bg="#1f1f1f").pack()
	tk.Button(width=50, height= 3,text="Submit", bg="black", fg="white", command = lambda : submitAction(window, bfsBool, dfsBool, aBool, dijkstraBool)).pack()   
    #Running the main menu
	window.mainloop()

algMenu()

