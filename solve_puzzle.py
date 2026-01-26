def solve():
    # Target location from measure() (Treasure)
    tx, ty = measure()
    
    visited = set()
    
    # Coordinate offsets for directions
    # Confirmed from move.py: East(+x), North(+y)
    dir_offsets = {
        North: (0, 1),
        South: (0, -1),
        East: (1, 0),
        West: (-1, 0)
    }
    
    # Inverse directions for backtracking
    inverse_dir = {
        North: South,
        South: North,
        East: West,
        West: East
    }

    def dfs():
        cx, cy = get_pos_x(), get_pos_y()
        
        # Reached target?
        if cx == tx and cy == ty:
            return True
            
        visited.add((cx, cy))
        
        # 1. Identify valid candidates (not visited)
        candidates = []
        for d, (dx, dy) in dir_offsets.items():
            nx, ny = cx + dx, cy + dy
            if (nx, ny) not in visited:
                # Calculate Manhattan distance to target as heuristic
                dist = abs(nx - tx) + abs(ny - ty)
                candidates.append((dist, d))
        
        # 2. Sort candidates by distance (Greedy Best-First heuristic)
        # Try directions that get us closer to target first
        # Python sorts tuples by first element by default, so we can remove the lambda
        candidates.sort()
        
        # 3. Explore
        for _, d in candidates:
            # Try to move physically
            if move(d):
                # We moved! Now we are at the new position.
                # Check if this path leads to solution
                if dfs():
                    return True
                
                # If we returned False, it means dead end or cycle.
                # Backtrack physically.
                move(inverse_dir[d])
                    
        return False

    # Start search
    dfs()
