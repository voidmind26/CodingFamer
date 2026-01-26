from move import set_do_ending, moveTo
import solve_puzzle

swapped = False

# Global memory to track pumpkin grid status
# 0: Unknown/Empty, 1: Growing, 2: Ready, 3: Dead
# We'll use a dictionary for sparse updates or list for full grid. List is faster for dense grid.
pumpkin_grid_memory = None 

def plantPumpkin():
	# Deprecated: Old pumpkin logic
	pass

def plantCarrot():
	set_do_ending(False)
	if get_ground_type() == Grounds.Grassland:
		till()
		plant(Entities.Carrot)
	if can_harvest():
		harvest()
		plant(Entities.Carrot)

def plantTree():
	if (get_pos_x()+get_pos_y())%2 == 0:
		if get_ground_type() == Grounds.Grassland:
			till()
			plant(Entities.Tree)
		if can_harvest():
			harvest()
			plant(Entities.Tree)
	else:
		if can_harvest():
			harvest()

def plantGrass():
	if can_harvest():
		harvest()

def pumpkinEnding():
	use_item(Items.Weird_Substance)
	harvest()

def plantCactus():
	# This function is deprecated in favor of farmCactus
	pass

def harvestCactus():
	# This function is deprecated in favor of farmCactus
	pass

# --- Efficient In-Memory Sorting Implementation ---

def scan_grid():
	size = get_world_size()
	grid_data = []
	for x in range(size):
		row = []
		for y in range(size):
			row.append(0)
		grid_data.append(row)
		
	for y in range(size):
		if y % 2 == 0:
			for x in range(size):
				moveTo(x, y)
				if get_ground_type() == Grounds.Grassland:
					till()
				if get_entity_type() != Entities.Cactus:
					plant(Entities.Cactus)
				grid_data[x][y] = measure()
		else:
			for x in range(size - 1, -1, -1):
				moveTo(x, y)
				if get_ground_type() == Grounds.Grassland:
					till()
				if get_entity_type() != Entities.Cactus:
					plant(Entities.Cactus)
				grid_data[x][y] = measure()
			
	return grid_data

def simulate_shear_sort(grid_data):
	size = len(grid_data)
	plan = [] 
	
	sorted_grid = False
	loop_limit = 1000 
	loop_count = 0
	
	while not sorted_grid and loop_count < loop_limit:
		sorted_grid = True
		loop_count += 1
		
		# Row Pass (Snake)
		for y in range(size):
			if y % 2 == 0:
				for x in range(size - 1):
					val_curr = grid_data[x][y]
					val_east = grid_data[x+1][y]
					if val_curr > val_east:
						plan.append({'x': x, 'y': y, 'dir': East})
						grid_data[x][y] = val_east
						grid_data[x+1][y] = val_curr
						sorted_grid = False
			else:
				for x in range(size - 1, 0, -1):
					val_curr = grid_data[x][y]
					val_west = grid_data[x-1][y]
					if val_curr < val_west:
						plan.append({'x': x, 'y': y, 'dir': West})
						grid_data[x][y] = val_west
						grid_data[x-1][y] = val_curr
						sorted_grid = False
						
		# Column Pass
		for x in range(size):
			for y in range(size - 1):
				val_curr = grid_data[x][y]
				val_north = grid_data[x][y+1]
				if val_curr > val_north:
					plan.append({'x': x, 'y': y, 'dir': North})
					grid_data[x][y] = val_north
					grid_data[x][y+1] = val_curr
					sorted_grid = False
					
	return plan

def execute_plan(plan):
	for op in plan:
		moveTo(op['x'], op['y'])
		swap(op['dir'])

def farmCactus():
	grid_data = scan_grid()
	swap_ops = simulate_shear_sort(grid_data)
	execute_plan(swap_ops)
	moveTo(0, 0)
	harvest()

# --- Optimized Pumpkin Logic with Memory ---

def init_pumpkin_memory(size):
	global pumpkin_grid_memory
	if pumpkin_grid_memory == None or len(pumpkin_grid_memory) != size:
		pumpkin_grid_memory = []
		for x in range(size):
			row = []
			for y in range(size):
				# Initial state: Assume needs checking (0)
				row.append(0) 
			pumpkin_grid_memory.append(row)

def farmPumpkin():
	size = get_world_size()
	init_pumpkin_memory(size)
	
	all_ready = True
	
	# Check Phase: Only visit cells that need attention based on memory
	check_list = []
	
	for x in range(size):
		for y in range(size):
			status = pumpkin_grid_memory[x][y]
			if status != 2: # 2 means Ready
				check_list.append((x, y))
	
	if len(check_list) == 0:
		pass
	
	# 2. Visit targets using Snake Path for efficiency
	for y in range(size):
		# Determine x range based on row parity (Snake)
		if y % 2 == 0:
			xs = range(size)
		else:
			xs = range(size - 1, -1, -1)
			
		for x in xs:
			# Skip if we think it's ready
			if pumpkin_grid_memory[x][y] == 2:
				continue
				
			moveTo(x, y)
			
			# Update memory and take action
			if get_ground_type() == Grounds.Grassland:
				till()
				
			entity = get_entity_type()
			
			if entity == Entities.Dead_Pumpkin or entity == None:
				# Plant new
				if num_items(Items.Carrot) > 0:
					plant(Entities.Pumpkin)
					pumpkin_grid_memory[x][y] = 1 # Growing
					all_ready = False
				else:
					# No seeds, can't fix. Mark as empty/dead
					pumpkin_grid_memory[x][y] = 0 # Check again later
					all_ready = False
			elif can_harvest():
				# It is ready!
				pumpkin_grid_memory[x][y] = 2 # Ready
			else:
				# It is growing
				pumpkin_grid_memory[x][y] = 1 # Growing
				all_ready = False

	# 3. Final Check
	if all_ready:
		harvest()
		# Reset memory after harvest
		for x in range(size):
			for y in range(size):
				pumpkin_grid_memory[x][y] = 0 # Reset to unknown/empty

# --- Polyculture Logic ---

def farmPolyculture():
	size = get_world_size()
	
	# Step 1: Base Fill (Skipped as per user feedback)
	pass

	# Step 2: Dynamic Satisfaction Loop
	# Iterate multiple times to build a complex companion network
	for _ in range(3): 
		for x in range(size):
			for y in range(size):
				moveTo(x, y)
				
				# Ask current plant what it wants
				companion = get_companion()
				
				if companion != None:
					target_type, (tx, ty) = companion
					
					# Go to target location and plant what is requested
					moveTo(tx, ty)
					
					# Only replant if it's not already the correct plant
					if get_entity_type() != target_type:
						if get_ground_type() == Grounds.Grassland:
							till()
						plant(target_type)

	# Step 3: Harvest
	for x in range(size):
		for y in range(size):
			moveTo(x, y)
			harvest()

# --- Unified Entry Points ---

def farmTree():
	size = get_world_size()
	for y in range(size):
		if y % 2 == 0:
			xs = range(size)
		else:
			xs = range(size - 1, -1, -1)
		for x in xs:
			moveTo(x, y)
			plantTree()

def farmCarrot():
	size = get_world_size()
	for y in range(size):
		if y % 2 == 0:
			xs = range(size)
		else:
			xs = range(size - 1, -1, -1)
		for x in xs:
			moveTo(x, y)
			plantCarrot()

def farmMaze():
	# Clear board first to ensure space for maze
	clear()
	
	# Plant a bush at 0,0 and evolve it into a maze
	moveTo(0, 0)
	plant(Entities.Bush)
	
	# Use substance until it transforms
	while get_entity_type() == Entities.Bush:
		substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
		use_item(Items.Weird_Substance, substance)
	
	# Solve the maze
	solve_puzzle.solve()
	
	# Harvest the treasure
	harvest()
	
	# Reset for next crop
	clear()
