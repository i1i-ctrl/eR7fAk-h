import turtle
import math
import random
import time

# --- 1. Screen Setup ---
wn = turtle.Screen()
wn.title("3D Turtle Raycaster - 12 Level Megapack")
wn.setup(width=800, height=600) 
wn.tracer(0)
wn.colormode(255)

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()

map_pen = turtle.Turtle()
map_pen.speed(0)
map_pen.hideturtle()

canvas = wn.getcanvas()

# --- 2. Game Map & Global Settings ---
current_level_name = ""
level_type = "infinite" 
world_map = {}
CHUNK_SIZE = 6 
generated_chunks = set()

wall_colors = {}
floor_color = (0, 0, 0)
min_walls_per_chunk = 2
max_walls_per_chunk = 3
MAX_DEPTH = 6.0 

# --- 3. Entity Variables ---
px, py = 1.5, 1.5
pa = 0.0
walk_cycle = 0.0 
orbs = []

smiler_x, smiler_y = 0.0, 0.0
smiler_active = False
has_smiler = False
smiler_trigger_time = 10
smiler_speed = 0.18
level_start_time = 0.0

# --- 4. The Level System ---
def teleport_to_random_level():
    global current_level_name
    # ALL 12 LEVELS
    levels = ["lobby", "poolrooms", "pipedreams", "run", "warehouse", 
              "office", "lightsout", "levelfun", "hotel", "ocean", "the_end", "true_ending"]
    
    if current_level_name in levels:
        levels.remove(current_level_name)
    next_level = random.choice(levels)
    
    if next_level == "lobby": load_lobby()
    elif next_level == "poolrooms": load_poolrooms()
    elif next_level == "pipedreams": load_pipe_dreams()
    elif next_level == "run": load_level_run()
    elif next_level == "warehouse": load_warehouse()
    elif next_level == "office": load_office()
    elif next_level == "lightsout": load_lights_out()
    elif next_level == "levelfun": load_level_fun()
    elif next_level == "hotel": load_hotel()
    elif next_level == "ocean": load_ocean()
    elif next_level == "the_end": load_the_end()
    elif next_level == "true_ending": load_true_ending()

def reset_engine_for_new_level():
    global smiler_active, level_start_time, orbs, MAX_DEPTH, has_smiler
    world_map.clear()
    generated_chunks.clear()
    orbs.clear() 
    smiler_active = False
    has_smiler = False 
    MAX_DEPTH = 6.0    
    level_start_time = time.time() 

def setup_infinite_player_and_orbs():
    global px, py, pa
    px, py = 1.5, 1.5
    pa = 0.0
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            world_map[(1 + dx, 1 + dy)] = 0
            
    guaranteed_x = random.randint(15, 30) + 0.5
    guaranteed_y = random.randint(15, 30) + 0.5
    world_map[(int(guaranteed_x), int(guaranteed_y))] = 0 
    orbs.append((guaranteed_x, guaranteed_y))

# --- LEVEL DEFINITIONS ---
def load_lobby():
    global current_level_name, level_type, floor_color, min_walls_per_chunk, max_walls_per_chunk
    reset_engine_for_new_level()
    current_level_name = "lobby"; level_type = "infinite"
    wn.bgcolor((89, 80, 29)); floor_color = (128, 110, 8) 
    for i in range(1, 5): wall_colors[i] = (145, 132, 35)
    min_walls_per_chunk, max_walls_per_chunk = 2, 3
    setup_infinite_player_and_orbs()

def load_poolrooms():
    global current_level_name, level_type, floor_color, min_walls_per_chunk, max_walls_per_chunk
    reset_engine_for_new_level()
    current_level_name = "poolrooms"; level_type = "infinite"
    wn.bgcolor((220, 240, 255)); floor_color = (30, 160, 170) 
    wall_colors[1] = (200, 230, 230); wall_colors[2] = (180, 210, 220)
    wall_colors[3] = (210, 240, 240); wall_colors[4] = (190, 220, 230)
    min_walls_per_chunk, max_walls_per_chunk = 0, 2
    setup_infinite_player_and_orbs()

def load_pipe_dreams():
    global current_level_name, level_type, floor_color, min_walls_per_chunk, max_walls_per_chunk
    reset_engine_for_new_level()
    current_level_name = "pipedreams"; level_type = "infinite"
    wn.bgcolor((10, 10, 10)); floor_color = (30, 30, 30) 
    wall_colors[1] = (70, 60, 50); wall_colors[2] = (50, 40, 30)
    wall_colors[3] = (80, 70, 60); wall_colors[4] = (60, 50, 40)
    min_walls_per_chunk, max_walls_per_chunk = 4, 6
    setup_infinite_player_and_orbs()

def load_warehouse():
    global current_level_name, level_type, floor_color, min_walls_per_chunk, max_walls_per_chunk
    reset_engine_for_new_level()
    current_level_name = "warehouse"; level_type = "infinite"
    wn.bgcolor((40, 40, 45)); floor_color = (60, 60, 65) 
    wall_colors[1] = (100, 100, 100); wall_colors[2] = (90, 95, 90)
    wall_colors[3] = (110, 110, 110); wall_colors[4] = (80, 80, 80)
    min_walls_per_chunk, max_walls_per_chunk = 2, 4
    setup_infinite_player_and_orbs()

def load_office():
    global current_level_name, level_type, floor_color, min_walls_per_chunk, max_walls_per_chunk
    reset_engine_for_new_level()
    current_level_name = "office"; level_type = "infinite"
    wn.bgcolor((200, 200, 190)); floor_color = (150, 140, 120) 
    wall_colors[1] = (220, 220, 210); wall_colors[2] = (240, 240, 230)
    wall_colors[3] = (210, 210, 200); wall_colors[4] = (230, 230, 220)
    min_walls_per_chunk, max_walls_per_chunk = 1, 3
    setup_infinite_player_and_orbs()

def load_lights_out():
    global current_level_name, level_type, floor_color, min_walls_per_chunk, max_walls_per_chunk, MAX_DEPTH
    reset_engine_for_new_level()
    current_level_name = "lightsout"; level_type = "infinite"
    MAX_DEPTH = 3.0 # Murky Fog
    wn.bgcolor((5, 5, 5)); floor_color = (10, 10, 10) 
    wall_colors[1] = (40, 40, 40); wall_colors[2] = (30, 30, 30)
    wall_colors[3] = (50, 50, 50); wall_colors[4] = (35, 35, 35)
    min_walls_per_chunk, max_walls_per_chunk = 5, 7 
    setup_infinite_player_and_orbs()

def load_level_fun():
    global current_level_name, level_type, floor_color, min_walls_per_chunk, max_walls_per_chunk
    global has_smiler, smiler_trigger_time, smiler_speed
    reset_engine_for_new_level()
    current_level_name = "levelfun"; level_type = "infinite"
    wn.bgcolor((255, 100, 200)); floor_color = (255, 255, 100) 
    wall_colors[1] = (0, 255, 255); wall_colors[2] = (255, 0, 255)
    wall_colors[3] = (150, 255, 50); wall_colors[4] = (255, 150, 0)
    min_walls_per_chunk, max_walls_per_chunk = 1, 4
    setup_infinite_player_and_orbs()
    has_smiler = True; smiler_trigger_time = 25; smiler_speed = 0.13 

def load_hotel():
    global current_level_name, level_type, floor_color, min_walls_per_chunk, max_walls_per_chunk
    reset_engine_for_new_level()
    current_level_name = "hotel"; level_type = "infinite"
    wn.bgcolor((50, 30, 20)); floor_color = (80, 20, 20) 
    wall_colors[1] = (120, 90, 50); wall_colors[2] = (100, 70, 40)
    wall_colors[3] = (130, 100, 60); wall_colors[4] = (90, 60, 30)
    min_walls_per_chunk, max_walls_per_chunk = 2, 4
    setup_infinite_player_and_orbs()

def load_ocean():
    global current_level_name, level_type, floor_color, min_walls_per_chunk, max_walls_per_chunk, MAX_DEPTH
    reset_engine_for_new_level()
    current_level_name = "ocean"; level_type = "infinite"
    MAX_DEPTH = 4.0 
    wn.bgcolor((5, 15, 25)); floor_color = (10, 30, 50) 
    wall_colors[1] = (30, 50, 60); wall_colors[2] = (25, 45, 55)
    wall_colors[3] = (35, 55, 65); wall_colors[4] = (20, 40, 50)
    min_walls_per_chunk, max_walls_per_chunk = 1, 2
    setup_infinite_player_and_orbs()

def load_the_end():
    global current_level_name, level_type, floor_color, min_walls_per_chunk, max_walls_per_chunk
    global has_smiler, smiler_trigger_time, smiler_speed
    reset_engine_for_new_level()
    current_level_name = "the_end"; level_type = "infinite"
    wn.bgcolor((150, 150, 150)); floor_color = (100, 100, 100) 
    wall_colors[1] = (80, 50, 30); wall_colors[2] = (70, 40, 20) 
    wall_colors[3] = (90, 60, 40); wall_colors[4] = (60, 30, 10)
    min_walls_per_chunk, max_walls_per_chunk = 4, 6 
    setup_infinite_player_and_orbs()
    has_smiler = True; smiler_trigger_time = 15; smiler_speed = 0.20 # Aggressive Smiler

def load_true_ending():
    global current_level_name, level_type, floor_color, min_walls_per_chunk, max_walls_per_chunk
    reset_engine_for_new_level()
    current_level_name = "true_ending"; level_type = "infinite"
    wn.bgcolor((20, 0, 30)); floor_color = (50, 0, 50) 
    wall_colors[1] = (0, 255, 100); wall_colors[2] = (255, 0, 100) 
    wall_colors[3] = (0, 100, 255); wall_colors[4] = (255, 255, 0)
    min_walls_per_chunk, max_walls_per_chunk = 1, 3
    setup_infinite_player_and_orbs()

def load_level_run():
    global current_level_name, level_type, floor_color, px, py, pa, smiler_x, smiler_y
    global has_smiler, smiler_trigger_time, smiler_speed
    reset_engine_for_new_level()
    current_level_name = "run"; level_type = "fixed"
    
    wn.bgcolor((80, 10, 10)); floor_color = (40, 10, 10) 
    wall_colors[1] = (150, 30, 30); wall_colors[2] = (180, 40, 40)
    wall_colors[3] = (120, 20, 20); wall_colors[4] = (200, 50, 50)
    
    for y in range(-2, 100):
        world_map[(0, y)] = random.randint(1, 4) 
        world_map[(4, y)] = random.randint(1, 4) 
    for x in range(0, 5): world_map[(x, -2)] = random.randint(1, 4)
        
    for y in range(10, 90, 6):
        obs_x = random.choice([1, 2, 3])
        world_map[(obs_x, y)] = random.randint(1, 4)
        
    px, py = 2.0, 0.0
    pa = math.pi / 2 
    orbs.append((2.0, 95.0))
    
    has_smiler = True; smiler_trigger_time = 10; smiler_speed = 0.18
    smiler_x, smiler_y = 2.0, -1.0

# --- 5. Chunk Generation (For Infinite Levels) ---
def generate_chunk(cx, cy):
    generated_chunks.add((cx, cy))
    for y in range(cy * CHUNK_SIZE, (cy + 1) * CHUNK_SIZE):
        for x in range(cx * CHUNK_SIZE, (cx + 1) * CHUNK_SIZE):
            world_map[(x, y)] = 0
            
    num_walls = random.randint(min_walls_per_chunk, max_walls_per_chunk)
    for _ in range(num_walls):
        length = random.randint(3, 6)
        is_horizontal = random.choice([True, False])
        start_x = random.randint(cx * CHUNK_SIZE, (cx + 1) * CHUNK_SIZE - 1)
        start_y = random.randint(cy * CHUNK_SIZE, (cy + 1) * CHUNK_SIZE - 1)
        color = random.randint(1, 4)
        
        for i in range(length):
            if is_horizontal: world_map[(start_x + i, start_y)] = color
            else: world_map[(start_x, start_y + i)] = color
                
    if cx == 0 and cy == 0:
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                world_map[(1 + dx, 1 + dy)] = 0
                
    if (abs(cx) > 1 or abs(cy) > 1) and random.random() < 0.05:
        orb_x = (cx * CHUNK_SIZE) + random.randint(1, CHUNK_SIZE - 2) + 0.5
        orb_y = (cy * CHUNK_SIZE) + random.randint(1, CHUNK_SIZE - 2) + 0.5
        world_map[(int(orb_x), int(orb_y))] = 0 
        orbs.append((orb_x, orb_y))

# --- 6. Engine & Mouse Settings ---
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 100 

keys = {"forward": False, "backward": False, "strafe_left": False, "strafe_right": False, 
        "turn_left": False, "turn_right": False, "shift": False}

def press(action): keys[action] = True
def release(action): keys[action] = False

mouse_locked = False
last_mouse_x = 400

def toggle_mouse():
    global mouse_locked, last_mouse_x
    mouse_locked = not mouse_locked

def on_mouse_move(event):
    global pa, last_mouse_x
    if not mouse_locked: 
        last_mouse_x = event.x
        return
    delta_x = event.x - last_mouse_x
    if delta_x != 0: pa += delta_x * 0.005 
    last_mouse_x = event.x

canvas.bind('<Motion>', on_mouse_move)

# --- 7. Draw Floor & Minimap ---
def draw_floor(width, height, bob_offset):
    pen.penup()
    pen.goto(-width / 2, bob_offset)
    pen.pendown()
    pen.color(floor_color) 
    pen.begin_fill()
    pen.goto(width / 2, bob_offset)
    pen.goto(width / 2, -height / 2)
    pen.goto(-width / 2, -height / 2)
    pen.goto(-width / 2, bob_offset)
    pen.end_fill()

def draw_minimap(width, height):
    map_pen.clear()
    map_scale = 8          
    map_x_offset = (-width / 2) + 20    
    map_y_offset = (height / 2) - 20     
    radar_radius = 6       
    
    p_grid_x = int(px)
    p_grid_y = int(py)
    
    for y in range(p_grid_y - radar_radius, p_grid_y + radar_radius):
        for x in range(p_grid_x - radar_radius, p_grid_x + radar_radius):
            block = world_map.get((x, y), 0)
            if block > 0:
                draw_x = map_x_offset + (x - px + radar_radius) * map_scale
                draw_y = map_y_offset - (y - py + radar_radius) * map_scale
                color = wall_colors.get(block, (255, 255, 255))
                map_pen.color(color)
                map_pen.penup()
                map_pen.goto(draw_x, draw_y)
                map_pen.pendown()
                map_pen.begin_fill()
                for _ in range(4):
                    map_pen.forward(map_scale)
                    map_pen.right(90)
                map_pen.end_fill()
                
    for ox, oy in orbs:
        if abs(ox - px) <= radar_radius and abs(oy - py) <= radar_radius:
            orb_draw_x = map_x_offset + (ox - px + radar_radius) * map_scale
            orb_draw_y = map_y_offset - (oy - py + radar_radius) * map_scale
            map_pen.color((50, 255, 100))
            map_pen.penup()
            map_pen.goto(orb_draw_x, orb_draw_y)
            map_pen.dot(8)
        
    if has_smiler and smiler_active:
        if abs(smiler_x - px) <= radar_radius and abs(smiler_y - py) <= radar_radius:
            smiler_draw_x = map_x_offset + (smiler_x - px + radar_radius) * map_scale
            smiler_draw_y = map_y_offset - (smiler_y - py + radar_radius) * map_scale
            map_pen.color("white")
            map_pen.penup()
            map_pen.goto(smiler_draw_x, smiler_draw_y)
            map_pen.dot(8)

    player_draw_x = map_x_offset + (radar_radius * map_scale)
    player_draw_y = map_y_offset - (radar_radius * map_scale)
    map_pen.color((150, 150, 255)) 
    map_pen.penup()
    map_pen.goto(player_draw_x, player_draw_y)
    map_pen.dot(6)
    map_pen.pendown()
    map_pen.goto(player_draw_x + math.cos(pa) * 10, player_draw_y - math.sin(pa) * 10)

# --- 8. The Raycaster ---
def cast_rays():
    pen.clear()
    screen_w = wn.window_width()
    screen_h = wn.window_height()
    bob_offset = math.sin(walk_cycle) * 15
    draw_floor(screen_w, screen_h, bob_offset)
    
    start_angle = pa - HALF_FOV
    step_angle = FOV / NUM_RAYS
    slice_width = screen_w / NUM_RAYS
    pen.pensize(math.ceil(slice_width) + 1) 
    screen_dist = screen_w / 2 
    
    z_buffer = []
    
    for ray in range(NUM_RAYS):
        ray_angle = start_angle + ray * step_angle
        distance = 0.0
        hit = False
        hit_color = (255, 255, 255) 
        
        eye_x = math.cos(ray_angle)
        eye_y = math.sin(ray_angle)
        
        while not hit and distance < MAX_DEPTH:
            distance += 0.1
            test_x = int(px + eye_x * distance)
            test_y = int(py + eye_y * distance)
            block_type = world_map.get((test_x, test_y), 0)
            
            if block_type > 0: 
                hit = True
                hit_color = wall_colors.get(block_type, (255, 255, 255))
                
        distance *= math.cos(pa - ray_angle)
        if distance == 0: distance = 0.1
        z_buffer.append(distance)
        
        wall_height = screen_dist / distance
        if wall_height > screen_h: wall_height = screen_h 
        
        shade = max(0, 1 - (distance / MAX_DEPTH) ** 1.5)
        r = int(hit_color[0] * shade)
        g = int(hit_color[1] * shade)
        b = int(hit_color[2] * shade)
        pen.color((r, g, b)) 
        
        screen_x = (-screen_w / 2) + (ray * slice_width) + (slice_width / 2)
        
        pen.penup()
        pen.goto(screen_x, (-wall_height / 2) + bob_offset)
        pen.pendown()
        pen.goto(screen_x, (wall_height / 2) + bob_offset)
        
    # --- DRAW THE SMILER FACE ---
    if has_smiler and smiler_active:
        dist_to_smiler = math.hypot(smiler_x - px, smiler_y - py)
        smiler_angle = math.atan2(smiler_y - py, smiler_x - px)
        diff_s = smiler_angle - pa
        while diff_s > math.pi: diff_s -= 2 * math.pi
        while diff_s < -math.pi: diff_s += 2 * math.pi
        
        if abs(diff_s) < HALF_FOV and dist_to_smiler > 0.3:
            ray_index = int((diff_s + HALF_FOV) / step_angle)
            if 0 <= ray_index < NUM_RAYS and dist_to_smiler < z_buffer[ray_index]:
                smiler_screen_x = diff_s * (screen_w / FOV)
                smiler_size = min(300, (screen_w / dist_to_smiler) * 0.15)
                jitter_x = random.randint(-4, 4)
                jitter_y = random.randint(-4, 4)
                
                pen.penup()
                pen.goto(smiler_screen_x + jitter_x, bob_offset - smiler_size + jitter_y)
                pen.pendown()
                pen.color((255, 255, 255))
                pen.begin_fill()
                pen.circle(smiler_size)
                pen.end_fill()
                
                pen.color("black")
                eye_size = smiler_size * 0.15
                pen.penup()
                pen.goto(smiler_screen_x + jitter_x - (smiler_size * 0.4), bob_offset - smiler_size + jitter_y + (smiler_size * 1.1))
                pen.pendown()
                pen.begin_fill()
                pen.circle(eye_size)
                pen.end_fill()
                
                pen.penup()
                pen.goto(smiler_screen_x + jitter_x + (smiler_size * 0.4), bob_offset - smiler_size + jitter_y + (smiler_size * 1.1))
                pen.pendown()
                pen.begin_fill()
                pen.circle(eye_size)
                pen.end_fill()
                
                pen.penup()
                pen.goto(smiler_screen_x + jitter_x, bob_offset - smiler_size + jitter_y + (smiler_size * 0.3))
                pen.pendown()
                pen.begin_fill()
                pen.circle(smiler_size * 0.6) 
                pen.end_fill()

    # --- DRAW ALL EXIT ORBS ---
    for ox, oy in orbs:
        dist_to_orb = math.hypot(ox - px, oy - py)
        orb_angle = math.atan2(oy - py, ox - px)
        diff = orb_angle - pa
        while diff > math.pi: diff -= 2 * math.pi
        while diff < -math.pi: diff += 2 * math.pi
        
        if abs(diff) < HALF_FOV and dist_to_orb > 0.3:
            ray_index = int((diff + HALF_FOV) / step_angle)
            if 0 <= ray_index < NUM_RAYS and dist_to_orb < z_buffer[ray_index]:
                orb_screen_x = diff * (screen_w / FOV)
                orb_size = min(200, (screen_w / dist_to_orb) * 0.1)
                pulse = math.sin(walk_cycle * 2) * 5
                
                pen.penup()
                pen.goto(orb_screen_x, bob_offset - orb_size + pulse)
                pen.pendown()
                pen.color((50, 255, 100))
                pen.begin_fill()
                pen.circle(orb_size)
                pen.end_fill()
        
    draw_minimap(screen_w, screen_h)
    wn.update()

# --- 9. Smooth Game Loop ---
def game_loop():
    global px, py, pa, walk_cycle
    global smiler_x, smiler_y, smiler_active
    
    moved = False 
    is_walking = False 
    
    # --- ENDLESS TELEPORTER OR TRUE ENDING ---
    for ox, oy in orbs:
        if math.hypot(ox - px, oy - py) < 0.8:
            if current_level_name == "true_ending":
                pen.clear()
                wn.bgcolor("white")
                pen.goto(0, 0)
                pen.color("black")
                pen.write("YOU FINALLY ESCAPED.", align="center", font=("Arial", 36, "bold"))
                wn.update()
                return # Game completely over, you won!
            else:
                teleport_to_random_level()
                moved = True
                break 
            
    # --- UNIVERSAL SMILER LOGIC ---
    if has_smiler:
        if not smiler_active and time.time() - level_start_time >= smiler_trigger_time:
            smiler_active = True
            if level_type == "infinite":
                smiler_x = px - math.cos(pa) * 5
                smiler_y = py - math.sin(pa) * 5
            
        if smiler_active:
            angle_to_player = math.atan2(py - smiler_y, px - smiler_x)
            smiler_x += math.cos(angle_to_player) * smiler_speed
            smiler_y += math.sin(angle_to_player) * smiler_speed
            moved = True 
            
            if math.hypot(smiler_x - px, smiler_y - py) < 0.8:
                pen.clear()
                wn.bgcolor("black")
                pen.goto(0, 0)
                pen.color("red")
                pen.write("THE SMILER CAUGHT YOU.", align="center", font=("Arial", 36, "bold"))
                wn.update()
                return 
    
    if level_type == "infinite":
        current_chunk_x = int(px) // CHUNK_SIZE
        current_chunk_y = int(py) // CHUNK_SIZE
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if (current_chunk_x + dx, current_chunk_y + dy) not in generated_chunks:
                    generate_chunk(current_chunk_x + dx, current_chunk_y + dy)
                    moved = True 
    
    if keys["turn_left"]: pa -= 0.1; moved = True
    if keys["turn_right"]: pa += 0.1; moved = True
        
    if keys["shift"]:
        move_step = 0.25  
        bob_speed = 0.5   
    else:
        move_step = 0.12  
        bob_speed = 0.3   

    if keys["forward"]:
        new_x = px + math.cos(pa) * move_step
        new_y = py + math.sin(pa) * move_step
        if world_map.get((int(new_x), int(new_y)), 0) == 0:
            px, py = new_x, new_y
            moved = True
            is_walking = True
            
    if keys["backward"]:
        new_x = px - math.cos(pa) * move_step
        new_y = py - math.sin(pa) * move_step
        if world_map.get((int(new_x), int(new_y)), 0) == 0:
            px, py = new_x, new_y
            moved = True
            is_walking = True

    if keys["strafe_left"]:
        new_x = px + math.cos(pa - math.pi / 2) * move_step
        new_y = py + math.sin(pa - math.pi / 2) * move_step
        if world_map.get((int(new_x), int(new_y)), 0) == 0:
            px, py = new_x, new_y
            moved = True
            is_walking = True

    if keys["strafe_right"]:
        new_x = px + math.cos(pa + math.pi / 2) * move_step
        new_y = py + math.sin(pa + math.pi / 2) * move_step
        if world_map.get((int(new_x), int(new_y)), 0) == 0:
            px, py = new_x, new_y
            moved = True
            is_walking = True
            
    if is_walking:
        walk_cycle += bob_speed
    else:
        if walk_cycle % math.pi > 0.1:
            walk_cycle += 0.1
            moved = True
            
    if moved or wn.window_width() != last_w or wn.window_height() != last_h:
        update_last_size()
        cast_rays()
        
    wn.ontimer(game_loop, 30)

last_w, last_h = 0, 0
def update_last_size():
    global last_w, last_h
    last_w = wn.window_width()
    last_h = wn.window_height()

# --- 10. Bind Keys & Start ---
turtle.listen()

for key in ["w", "W", "Up"]: turtle.onkeypress(lambda: press("forward"), key)
for key in ["s", "S", "Down"]: turtle.onkeypress(lambda: press("backward"), key)
for key in ["a", "A"]: turtle.onkeypress(lambda: press("strafe_left"), key)
for key in ["d", "D"]: turtle.onkeypress(lambda: press("strafe_right"), key)
for key in ["Left"]: turtle.onkeypress(lambda: press("turn_left"), key)
for key in ["Right"]: turtle.onkeypress(lambda: press("turn_right"), key)
for key in ["Shift_L", "Shift_R", "space"]: turtle.onkeypress(lambda: press("shift"), key)

for key in ["w", "W", "Up"]: turtle.onkeyrelease(lambda: release("forward"), key)
for key in ["s", "S", "Down"]: turtle.onkeyrelease(lambda: release("backward"), key)
for key in ["a", "A"]: turtle.onkeyrelease(lambda: release("strafe_left"), key)
for key in ["d", "D"]: turtle.onkeyrelease(lambda: release("strafe_right"), key)
for key in ["Left"]: turtle.onkeyrelease(lambda: release("turn_left"), key)
for key in ["Right"]: turtle.onkeyrelease(lambda: release("turn_right"), key)
for key in ["Shift_L", "Shift_R", "space"]: turtle.onkeyrelease(lambda: release("shift"), key)

turtle.onkeypress(toggle_mouse, "q")
turtle.onkeypress(toggle_mouse, "Q")

load_lobby()

update_last_size()
cast_rays() 
game_loop() 
turtle.done()