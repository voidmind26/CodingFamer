global DoEnding

def moveTo(x, y):
	# 将玩家移动到坐标 (x, y)
	while get_pos_x() != x or get_pos_y() != y:
		if get_pos_x() < x:
			move(East)
		elif get_pos_x() > x:
			move(West)
		elif get_pos_y() < y:
			move(North)
		elif get_pos_y() > y:
			move(South)

def moveWithDoing(x, y, doing):
	# 将玩家移动到坐标 (x, y) 并执行 doing 函数
	while get_pos_x() != x or get_pos_y() != y:
		if get_pos_x() < x:
			move(East)
		elif get_pos_x() > x:
			move(West)
		elif get_pos_y() < y:	
			move(North)
		elif get_pos_y() > y:
			move(South)
		doing()

def moveToNextCol(doing,ending):
	# 将玩家移动到下一列
	if get_pos_x() != get_world_size() - 1:
		moveWithDoing(get_pos_x() + 1, get_pos_y(), doing)
	else:
		if DoEnding:
			ending()
		moveTo(0, get_pos_y())

def moveToAllTile(doing,ending):
	global DoEnding 
	DoEnding = True
	# 将玩家移动到所有瓷砖
	size = get_world_size()
	doing()
	for i in range(size):
		if i % 2 == 0:
			moveWithDoing(i, size - 1, doing)
			moveToNextCol(doing,ending)
		else:
			moveWithDoing(i, 0, doing)
			moveToNextCol(doing,ending)
