from PIL import Image, ImageTk
import random
import tkinter as tk
from tkinter import filedialog, Label
import customtkinter as ck

root = ck.CTk()
root.title("Pokemon Mystery Dungeon Map Generator")
root.geometry("1600x1000")
root.iconbitmap(r'C:\Users\relay\Downloads\PMD Generator\icon.ico')

file = []
dungeon = []

c_frame = tk.Frame(root, bg="#263D42")
c_frame.place(relheight=1, relwidth= 1, relx=0, rely=0)

l_frame = tk.Frame(root, bg="#263D42")
l_frame.pack(side="left", anchor="sw")

r_frame = tk.Frame(root, bg="#263D42")
r_frame.pack(side="right", anchor="se")

TILE_SIZE = 24
MAP_SIZE = (40, 30)  # Width and height of the map
ROOM_PLACEMENT_ATTEMPTS = 50
MIN_ROOM_SIZE = 4
MAX_ROOM_SIZE = 9
MIN_ROOM_DISTANCE = 4  # Minimum distance between room centers
HALLWAY_WIDTH = 1
HALLWAYS = 1
SEED = 0

STAIRS = tk.StringVar(value="on")
STAIR_DIR = tk.StringVar(value="on")
BERRIES = tk.StringVar(value="on")
COMMONS = tk.StringVar(value="on")
CHESTS = tk.StringVar(value="off")
GUMMIES = tk.StringVar(value="on")
UNCOMMONS = tk.StringVar(value="on")
B_NUM = 1
CH_NUM = 1
G_NUM = 2
C_NUM = 8
U_NUM = 1


def addFile():
    file.clear()
    filename = filedialog.askopenfilename(initialdir="/Downloads", title="Select File", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
    file.append(filename)
    print(filename)

def generate_dungeon():
    dungeon_map = [[0 for _ in range(MAP_SIZE[0])] for _ in range(MAP_SIZE[1])]
    rooms = []
    global HALLWAYS

    for _ in range(ROOM_PLACEMENT_ATTEMPTS):
        room_x, room_y, room_width, room_height = generate_room()

        if is_room_valid(room_x, room_y, room_width, room_height, dungeon_map, rooms):
            rooms.append((room_x, room_y, room_width, room_height))

            for x in range(room_x, room_x + room_width):
                for y in range(room_y, room_y + room_height):
                    dungeon_map[y][x] = 1

    add_water_features(dungeon_map)
    connect_rooms(dungeon_map, rooms, HALLWAYS)
    
    return dungeon_map

def generate_room():
    room_width = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
    room_height = random.randint(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
    room_x = random.randint(1, MAP_SIZE[0] - room_width - 1)
    room_y = random.randint(1, MAP_SIZE[1] - room_height - 1)
    return room_x, room_y, room_width, room_height

def is_room_valid(room_x, room_y, room_width, room_height, dungeon_map, rooms):
    for x in range(room_x - 1, room_x + room_width + 1):
        for y in range(room_y - 1, room_y + room_height + 1):
            if dungeon_map[y][x] == 1:
                return False

    for other_room in rooms:
        other_center_x = other_room[0] + other_room[2] // 2
        other_center_y = other_room[1] + other_room[3] // 2
        dist = ((other_center_x - (room_x + room_width // 2)) ** 2 +
                (other_center_y - (room_y + room_height // 2)) ** 2) ** 0.5
        if dist < MIN_ROOM_DISTANCE:
            return False

    return True

def connect_rooms(dungeon_map, rooms, HALLWAYS):
    for i in range(len(rooms) - HALLWAYS):
        room1 = rooms[i]
        room2 = rooms[i + 1]

        center1_x = room1[0] + room1[2] // 2
        center1_y = room1[1] + room1[3] // 2
        center2_x = room2[0] + room2[2] // 2
        center2_y = room2[1] + room2[3] // 2

        current_x = center1_x
        current_y = center1_y

        while current_x != center2_x or current_y != center2_y:
            dungeon_map[current_y][current_x] = 1 

            if current_x < center2_x:
                current_x += 1
            elif current_x > center2_x:
                current_x -= 1
            elif current_y < center2_y:
                current_y += 1
            elif current_y > center2_y:
                current_y -= 1

def add_water_features(dungeon_map):
    for _ in range(max(0,(3 * random.randint(1,4)) - random.randint(0,2))):
        water_x = random.randint(2, MAP_SIZE[0] - 3)
        water_y = random.randint(2, MAP_SIZE[1] - 3)
        dungeon_map[water_y][water_x] = 2

def spread_water(dungeon_map, num_iterations, water_threshold=0.23):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for _ in range(num_iterations):
        new_dungeon_map = [[cell for cell in row] for row in dungeon_map]

        for y in range(MAP_SIZE[1]):
            for x in range(MAP_SIZE[0]):
                if dungeon_map[y][x] == 2:
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < MAP_SIZE[0] and 0 <= ny < MAP_SIZE[1]:
                            if dungeon_map[ny][nx] != 2:
                                if random.random() < water_threshold:
                                    new_dungeon_map[ny][nx] = 2
        dungeon_map = new_dungeon_map

    return dungeon_map

tileset_coordinates = {
    "000011011": (0, 0),
    "101011011": (0, 0),
    "001011011": (0, 0),
    "001011111": (0, 0),
    "101011111": (0, 0),
    "000011111": (0, 0),
    "100011111": (0, 0),
    "011011011": (0, 1),
    "111011111": (0, 1),
    "111011011": (0, 1),
    "011011111": (0, 1),
    "011011000": (0, 2),
    "111011001": (0, 2),
    "011011100": (0, 2),
    "011011001": (0, 2),
    "111011000": (0, 2),
    "111011100": (0, 2),
    "011011101": (0, 2),
    "111011101": (0, 2),
    "110111110": (0, 3),
    "010111111": (0, 4),
    "111111110": (0, 5),
    "110111111": (0, 6),
    "010111011": (0, 7),
    "101111111": (1, 0),
    "001111111": (1, 0),
    "000111111": (1, 0),
    "100111111": (1, 0),
    "111111001": (1, 2),
    "111111000": (1, 2),
    "111111101": (1, 2),
    "111111100": (1, 2),     
    "011111011": (1, 3),
    "111111010": (1, 4),
    "111111011": (1, 5),
    "011111111": (1, 6),
    "010111110": (1, 7),
    "000110110": (2, 0),
    "100110110": (2, 0),
    "100110111": (2, 0),
    "000110111": (2, 0),
    "101110111": (2, 0),
    "101110110": (2, 0),
    "001110111": (2, 0),
    "001110110": (2, 0),
    "110110110": (2, 1),
    "111110111": (2, 1),
    "110110111": (2, 1),
    "111110110": (2, 1),
    "111110000": (2, 2),
    "110110100": (2, 2),
    "110110101": (2, 2),
    "110110000": (2, 2),
    "111110100": (2, 2),
    "111110001": (2, 2),
    "110110001": (2, 2),
    "111110101": (2, 2),
    "000111010": (2, 3),
    "101111010": (2, 3),
    "001111010": (2, 3),
    "100111010": (2, 3),
    "010111000": (2, 4),
    "010111101": (2, 4),
    "010111100": (2, 4),
    "010111001": (2, 4),
    "011011010": (2, 5),
    "111011010": (2, 5),
    "111011110": (2, 5),
    "011011110": (2, 5),
    "010011111": (2, 6),
    "010011011": (2, 6),
    "110011111": (2, 6),
    "110011011": (2, 6),
    "011111010": (2, 7),
    "000011010": (3, 0),
    "000011110": (3, 0),
    "001011110": (3, 0),
    "101011110": (3, 0),
    "001011010": (3, 0),
    "101011010": (3, 0),
    "100011110": (3, 0),
    "100011010": (3, 0),
    "011010111": (3, 1),
    "111010111": (3, 1),
    "110010111": (3, 1),
    "111010011": (3, 1),
    "010010010": (3, 1),
    "111010110": (3, 1),
    "111010010": (3, 1),
    "010010011": (3, 1),
    "110010010": (3, 1),
    "010010111": (3, 1),
    "011010010": (3, 1),
    "011010011": (3, 1),
    "011010110": (3, 1),
    "110010110": (3, 1),
    "110010011": (3, 1),
    "010010110": (3, 1),
    "010011000": (3, 2),
    "110011101": (3, 2),
    "010011101": (3, 2),
    "010011100": (3, 2),
    "010011001": (3, 2),
    "110011000": (3, 2),
    "110011100": (3, 2),
    "110011001": (3, 2),
    "001011001": (3, 3),
    "000011000": (3, 3),
    "000011101": (3, 3),
    "001011000": (3, 3),
    "100011001": (3, 3),
    "001011101": (3, 3),
    "000011100": (3, 3),
    "001110000": (3, 3),
    "000011001": (3, 3),
    "001011100": (3, 3),
    "101011101": (3, 3),
    "100011000": (3, 3),
    "101011000": (3, 3),
    "010011110": (3, 4),
    "110011010": (3, 4),
    "110011110": (3, 4),
    "010011010": (3, 4),
    "110110010": (3, 5),
    "111110010": (3, 5),
    "110110011": (3, 5),
    "111110011": (3, 5),
    "010110111": (3, 6),
    "011110111": (3, 6),
    "011110110": (3, 6),
    "010110110": (3, 6),
    "110111010": (3, 7),
    "101111101": (4, 0),
    "101111001": (4, 0),
    "101111100": (4, 0),
    "101111000": (4, 0),
    "000111101": (4, 0),
    "000111000": (4, 0),
    "000111100": (4, 0),
    "000111001": (4, 0),
    "100111101": (4, 0),
    "100111001": (4, 0),
    "100111000": (4, 0),
    "100111100": (4, 0),
    "001111101": (4, 0),
    "001111001": (4, 0),
    "001111100": (4, 0),
    "001111000": (4, 0),
    "000010000": (4, 1),
    "000010101": (4, 1),
    "000010100": (4, 1),
    "000010001": (4, 1),
    "001010000": (4, 1),
    "001010101": (4, 1),
    "001010100": (4, 1),
    "001010001": (4, 1),
    "100010000": (4, 1),
    "100010101": (4, 1),
    "100010100": (4, 1),
    "100010001": (4, 1),
    "101010000": (4, 1),
    "101010101": (4, 1),
    "101010100": (4, 1),
    "101010001": (4, 1),
    "000010111": (4, 2),
    "000010010": (4, 2),
    "000010011": (4, 2),
    "000010110": (4, 2),
    "001010111": (4, 2),
    "001010010": (4, 2),
    "001010011": (4, 2),
    "001010110": (4, 2),
    "100010111": (4, 2),
    "100010010": (4, 2),
    "100010011": (4, 2),
    "100010110": (4, 2),
    "101010111": (4, 2),
    "101010010": (4, 2),
    "101010011": (4, 2),
    "101010110": (4, 2),
    "010111010": (4, 3),
    "010010101": (4, 4),
    "010010000": (4, 4),
    "010010001": (4, 4),
    "010010100": (4, 4),
    "011010101": (4, 4),
    "011010000": (4, 4),
    "011010001": (4, 4),
    "011010100": (4, 4),
    "110010101": (4, 4),
    "110010000": (4, 4),
    "110010001": (4, 4),
    "110010100": (4, 4),
    "111010101": (4, 4),
    "111010000": (4, 4),
    "111010001": (4, 4),
    "111010100": (4, 4),
    "000111110": (4, 5),
    "100111110": (4, 5),
    "001111110": (4, 5),
    "101111110": (4, 5),
    "110111000": (4, 6),
    "110111100": (4, 6),
    "110111001": (4, 6),
    "110111101": (4, 6),
    "011111110": (4, 7),
    "000110010": (5, 0),
    "000110011": (5, 0),
    "001110010": (5, 0),
    "001110011": (5, 0),
    "100110010": (5, 0),
    "100110011": (5, 0),
    "101110010": (5, 0),
    "101110011": (5, 0),
    "010110000": (5, 1),
    "010110001": (5, 1),
    "011110000": (5, 1),
    "011110001": (5, 1),
    "011110101": (5, 1),
    "010110100": (5, 1),
    "011110100": (5, 3),
    "001110100": (5, 3),
    "100110100": (5, 3),
    "001110101": (5, 3),
    "100110000": (5, 3),
    "000110000": (5, 3),
    "101110000": (5, 3),
    "101110100": (5, 3),
    "000110100": (5, 3),
    "010110101": (5, 3),
    "000110100": (5, 3),
    "100110001": (5, 3),
    "100110101": (5, 3),
    "010110010": (5, 4),
    "011110011": (5, 4),
    "010110011": (5, 4),
    "011110010": (5, 4),
    "000111011": (5, 5),
    "001111011": (5, 5),
    "100111011": (5, 5),
    "101111011": (5, 5),
    "011111000": (5, 6),
    "011111001": (5, 6),
    "011111100": (5, 6),
    "011111101": (5, 6),
    "110111011": (5, 7)
}

def generate_identifier(dungeon_map, x, y, z):
    identifier = ""
    search = z
    for j in range(y - 1, y + 2):
        for i in range(x - 1, x + 2):
            i_clamped = max(0, min(i, MAP_SIZE[0] - 1))
            j_clamped = max(0, min(j, MAP_SIZE[1] - 1))
            
            if dungeon_map[j_clamped][i_clamped] == search: 
                    identifier += "1"
            else:
                    identifier += "0"
    return identifier

    identifier = ""
    for j in range(y - 1, y + 2):
        for i in range(x - 1, x + 2):
            i_clamped = max(0, min(i, MAP_SIZE[0] - 1))
            j_clamped = max(0, min(j, MAP_SIZE[1] - 1))
            
            if dungeon_map[j_clamped][i_clamped] == 2: 
                    identifier += "1"
            else:
                    identifier += "0"
    return identifier

def extras(dungeon_map, image):
    global STAIRS, STAIR_DIR, COMMONS, GUMMIES, UNCOMMONS, CHESTS, BERRIES, TILE_SIZE, MAP_SIZE, B_NUM, G_NUM, U_NUM, CH_NUM, C_NUM
    
    stairs = Image.open("stairs.png")
    gummies = Image.open("gummies.png")
    commons = Image.open("commons.png")
    uncommons = Image.open("uncommons.png")
    chests = Image.open("chests.png")
    berries = Image.open("berries.png")
    
    if GUMMIES.get() == "on":
        gummies_placed = 0
        for y in range(len(dungeon_map)):
            for x in range(len(dungeon_map[0])):
                if dungeon_map[y][x] == 1:
                    j = random.randint(0, 8)
                    i = random.randint(0, 1)
                    gummy = gummies.crop((j * TILE_SIZE, i * TILE_SIZE, (j + 1) * TILE_SIZE, (i + 1) * TILE_SIZE))
                    gx = random.randint(0, MAP_SIZE[0] - 1) * TILE_SIZE
                    gy = random.randint(0, MAP_SIZE[1] - 1) * TILE_SIZE
                    if gummies_placed < G_NUM:
                        if dungeon_map[gy // TILE_SIZE][gx // TILE_SIZE] == 1:
                            image.alpha_composite(gummy, (gx, gy))
                            gummies_placed += 1

    if COMMONS.get() == "on":
        commons_placed = 0
        for y in range(len(dungeon_map)):
            for x in range(len(dungeon_map[0])):
                if dungeon_map[y][x] == 1:
                    i = random.randint(0, 9)
                    common = commons.crop((i * TILE_SIZE, 0, (i + 1) * TILE_SIZE, TILE_SIZE))
                    gx = random.randint(0, MAP_SIZE[0] - 1) * TILE_SIZE
                    gy = random.randint(0, MAP_SIZE[1] - 1) * TILE_SIZE
                    if commons_placed < C_NUM:
                        if dungeon_map[gy // TILE_SIZE][gx // TILE_SIZE] == 1:
                            image.alpha_composite(common, (gx, gy))
                            commons_placed += 1
                
    if UNCOMMONS.get() == "on":
        uncommons_placed = 0
        for y in range(len(dungeon_map)):
            for x in range(len(dungeon_map[0])):
                if dungeon_map[y][x] == 1:
                    i = random.randint(0, 8)
                    uncommon = uncommons.crop((i * TILE_SIZE, 0, (i + 1) * TILE_SIZE, TILE_SIZE))
                    gx = random.randint(0, MAP_SIZE[0] - 1) * TILE_SIZE
                    gy = random.randint(0, MAP_SIZE[1] - 1) * TILE_SIZE
                    if uncommons_placed < U_NUM:
                        if dungeon_map[gy // TILE_SIZE][gx // TILE_SIZE] == 1:
                            image.alpha_composite(uncommon, (gx, gy))
                            uncommons_placed += 1              

    if BERRIES.get() == "on":
        berries_placed = 0
        for y in range(len(dungeon_map)):
            for x in range(len(dungeon_map[0])):
                if dungeon_map[y][x] == 1:
                    j = random.randint(0, 7)
                    i = random.randint(0, 9)
                    berry = berries.crop((i * TILE_SIZE, j * TILE_SIZE, (i + 1) * TILE_SIZE, (j + 1) * TILE_SIZE))
                    gx = random.randint(0, MAP_SIZE[0] - 1) * TILE_SIZE
                    gy = random.randint(0, MAP_SIZE[1] - 1) * TILE_SIZE
                    if berries_placed < B_NUM:
                        if dungeon_map[gy // TILE_SIZE][gx // TILE_SIZE] == 1:
                            image.alpha_composite(berry, (gx, gy))
                            berries_placed += 1

    if CHESTS.get() == "on":
        chests_placed = 0
        for y in range(len(dungeon_map)):
            for x in range(len(dungeon_map[0]) ):
                if dungeon_map[y][x] == 1:
                    i = random.randint(0, 2)
                    chest = chests.crop((i * TILE_SIZE, 0, (i + 1) * TILE_SIZE, TILE_SIZE))
                    gx = random.randint(0, MAP_SIZE[0] - 1) * TILE_SIZE
                    gy = random.randint(0, MAP_SIZE[1] - 1) * TILE_SIZE
                    if chests_placed < CH_NUM:
                        if dungeon_map[gy // TILE_SIZE][gx // TILE_SIZE] == 1:
                            image.alpha_composite(chest, (gx, gy))
                            chests_placed += 1
                    else:
                        break
    
    if STAIRS.get() == "on":
        stair_placed = False
        for y in range(len(dungeon_map) - 1):
            for x in range(len(dungeon_map[0]) - 1):
                if dungeon_map[y][x] == 1:
                    if stair_placed == False:
                        if STAIR_DIR.get() == "on":
                            stair = stairs.crop((0, 0, TILE_SIZE, TILE_SIZE))
                            image.paste(stair, (x * TILE_SIZE, y * TILE_SIZE))
                            stair_placed = True
                        else:  
                            stair = stairs.crop((TILE_SIZE, 0, 2 * TILE_SIZE, TILE_SIZE))
                            image.paste(stair, (x * TILE_SIZE, y * TILE_SIZE))
                            stair_placed = True
                        break
    
    return image

def main():
    global STAIRS
    global SEED
    if SEED == 0:
        random_seed()
        random.seed(SEED)
    else:
        random.seed(SEED)
    
    tileset = Image.open(f"{file[0]}")
    if tileset.mode != 'RGBA':
        tileset = tileset.convert('RGBA')
    dungeon_map = generate_dungeon()
    
    dungeon_map = spread_water(dungeon_map, num_iterations=8)
    image = Image.new("RGBA", (MAP_SIZE[0] * TILE_SIZE, MAP_SIZE[1] * TILE_SIZE), color=(0,0,0))

    for y in range(MAP_SIZE[1]):
        for x in range(MAP_SIZE[0]):
            if dungeon_map[y][x] == 1:
                id = generate_identifier(dungeon_map, x, y, 1)
                tile_x, tile_y = tileset_coordinates.get(id, (1, 1))
                
                tile = tileset.crop(((tile_x + 12) * TILE_SIZE, tile_y * TILE_SIZE, (tile_x + 13) * TILE_SIZE, (tile_y + 1) * TILE_SIZE))
                image.paste(tile, (x * TILE_SIZE, y * TILE_SIZE))

            if dungeon_map[y][x] == 2:
                id = generate_identifier(dungeon_map, x, y, 2)
                tile_x, tile_y = tileset_coordinates.get(id, (1, 1))
                                
                tile = tileset.crop(((tile_x + 6) * TILE_SIZE, tile_y * TILE_SIZE, (tile_x + 7) * TILE_SIZE, (tile_y + 1) * TILE_SIZE))
                image.paste(tile, (x * TILE_SIZE, y * TILE_SIZE))
                
            if dungeon_map[y][x] == 0:
                floor = tileset.crop((0, 0, TILE_SIZE, TILE_SIZE))
                image.paste(floor, (x * TILE_SIZE, y * TILE_SIZE))
            
                id = generate_identifier(dungeon_map, x, y, 0)
                tile_x, tile_y = tileset_coordinates.get(id, (1, 1))
            
                wall = tileset.crop((tile_x * TILE_SIZE, tile_y * TILE_SIZE, (tile_x + 1) * TILE_SIZE, (tile_y + 1) * TILE_SIZE))
                image.alpha_composite(wall, (x * TILE_SIZE, y * TILE_SIZE))

    
    extras(dungeon_map, image)

    global dungeon
    dungeon = image   
    photo = ImageTk.PhotoImage(image)
    image_label.configure(image=photo,width=(photo.width() * .4), height=(photo.height() * .4))
    image_label.image = photo
    print(f"Dungeon generated. {SEED}")

def Save():
    global dungeon
    dungeon.save(f"dungeon{SEED}.png")
    print(f"Seed= {SEED}")


#----------------


def switcher():
    pass

def update_seed(*args):
    global SEED
    SEED = int(seed_var.get())

def random_seed():
    seed_var.set(random.randint(-10000, 10000))
    update_seed()

def update_min_room(*args):
    global MIN_ROOM_SIZE
    MIN_ROOM_SIZE = int(min_var.get())

def update_max_room(*args):
    global MAX_ROOM_SIZE
    MAX_ROOM_SIZE = int(max_var.get())

def update_map_height(*args):
    global MAP_SIZE
    MAP_SIZE = (int(height_var.get()), MAP_SIZE[1])

def update_map_width(*args):
    global MAP_SIZE
    MAP_SIZE = (MAP_SIZE[0], int(width_var.get()))

def update_hallway(*args):
    global HALLWAYS
    HALLWAYS = tk.StringVar(hall_var.get())

def update_berries(*args):
    global BERRIES
    BERRIES = tk.StringVar(ber_var.get())
    
def update_commons(*args):
    global COMMONS
    COMMONS = tk.StringVar(com_var.get())

def update_uncommons(*args):
    global UNCOMMONS
    UNCOMMONS = tk.StringVar(unc_var.get())
    
def update_chests(*args):
    global CHESTS
    CHESTS = tk.StringVar(che_var.get())
    
def update_gummies(*args):
    global GUMMIES
    GUMMIES = tk.StringVar(gum_var.get())

#SEED
seed_var = tk.StringVar()
seed_frame = ck.CTkFrame(l_frame, fg_color="#638991", corner_radius=5)
seed_frame.pack(side="bottom", anchor="w", pady=5, padx=10)
seed_label = ck.CTkLabel(seed_frame, text="Seed:", width= 110, height=25, corner_radius=6)
seed_label.pack(side="left", padx=10)
seed_entry = ck.CTkEntry(seed_frame, width= 60, textvariable=seed_var)
seed_entry.insert(0, SEED)                                                                         
seed_entry.pack(side="left", padx=10)
seed_var.trace_add("write", update_seed) 
seed_button2 = ck.CTkButton(seed_frame, text="Random", fg_color="#21515c", hover_color="#17282b", width=80, command=lambda: random_seed())
seed_button2.pack(side="left", padx=5)

#MIN_ROOM_SIZE
min_var = tk.StringVar()
min_room_frame = ck.CTkFrame(l_frame, fg_color="#638991", corner_radius=5)
min_room_frame.pack(side="bottom", anchor="w", pady=5, padx=10)
min_room_label = ck.CTkLabel(min_room_frame, text="Min Room Size:", width= 110, height=25, corner_radius=6)
min_room_label.pack(side="left", padx=10)
min_room_entry = ck.CTkEntry(min_room_frame, width= 60, textvariable=min_var)
min_room_entry.insert(0, MIN_ROOM_SIZE)
min_room_entry.pack(side="left", padx=10)
min_var.trace_add("write", update_min_room) 


#MAX_ROOM_SIZE
max_var = tk.StringVar()
max_room_frame = ck.CTkFrame(l_frame, fg_color="#638991", corner_radius=5)
max_room_frame.pack(side="bottom", anchor="w", pady=5, padx=10)
max_room_label = ck.CTkLabel(max_room_frame, text="Max Room Size:", width= 110, height=25, corner_radius=6)
max_room_label.pack(side="left", padx=10)
max_room_entry = ck.CTkEntry(max_room_frame, width= 60, textvariable=max_var)
max_room_entry.insert(0, MAX_ROOM_SIZE)
max_room_entry.pack(side="left", padx=10)
max_var.trace_add("write", update_max_room) 

#HALLWAYS
hall_var = tk.StringVar()
hallway_frame = ck.CTkFrame(l_frame, fg_color="#638991", corner_radius=5)
hallway_frame.pack(side="bottom", anchor="w", pady=5, padx=10)
hallway_label = ck.CTkLabel(hallway_frame, text="Hallway Limit:", width= 110, height=25, corner_radius=6)
hallway_label.pack(side="left", padx=10)
hallway_entry = ck.CTkEntry(hallway_frame, width= 60, textvariable=hall_var)
hallway_entry.insert(1, HALLWAYS)                                                                              
hallway_entry.pack(side="left", padx=10)
hall_var.trace_add("write", update_hallway) 

#MAP_WIDTH
width_var = tk.StringVar()
map_width_frame = ck.CTkFrame(l_frame, fg_color="#638991", corner_radius=5)
map_width_frame.pack(side="bottom", anchor="w", pady=5, padx=10)
map_width_label = ck.CTkLabel(map_width_frame, text="Map Width:", width= 110, height=25, corner_radius=6)
map_width_label.pack(side="left", padx=10)
map_width_entry = ck.CTkEntry(map_width_frame, width= 60, textvariable=width_var)
map_width_entry.insert(40, MAP_SIZE[1])
map_width_entry.pack(side="left", padx=10)
width_var.trace_add("write", update_map_width) 

#MAP_HEIGHT
height_var = tk.StringVar()
map_height_frame = ck.CTkFrame(l_frame, fg_color="#638991", corner_radius=5)
map_height_frame.pack(side="bottom", anchor="w", pady=5, padx=10)
map_height_label = ck.CTkLabel(map_height_frame, text="Map Height:", width= 110, height=25, corner_radius=6)
map_height_label.pack(side="left", padx=10)
map_height_entry = ck.CTkEntry(map_height_frame, width= 60, textvariable=height_var)
map_height_entry.insert(30, MAP_SIZE[0])
map_height_entry.pack(side="left", padx=10)
height_var.trace_add("write", update_map_height) 


#---------------


#STAIRS
str_var = tk.StringVar()
stair_frame = ck.CTkFrame(r_frame, fg_color="#638991", corner_radius=5)
stair_frame.pack(side="bottom", anchor="e", pady=5, padx=10)
stair_button2 = ck.CTkSwitch(stair_frame, text="UP/DOWN", command=switcher, variable=STAIR_DIR, onvalue="on", offvalue="off", corner_radius=4)
stair_button2.pack(side="left", padx=5)
stair_button = ck.CTkSwitch(stair_frame, text="Stairs", command=switcher, variable=STAIRS, onvalue="on", offvalue="off")
stair_button.pack(side="left", padx=5)
str_var.trace_add("write", update_map_height) 

#BERRIES
ber_var = tk.StringVar()
berries_frame = ck.CTkFrame(r_frame, fg_color="#638991", corner_radius=5)
berries_frame.pack(anchor="e", pady=5, padx=10)
berries_entry = ck.CTkEntry(berries_frame, width= 60, textvariable=ber_var)
berries_entry.insert(1, B_NUM)
berries_entry.pack(side="left")
berries_button = ck.CTkSwitch(berries_frame, text="Berries", command=switcher, variable=BERRIES, onvalue="on", offvalue="off", width= 140)
berries_button.pack(side="left", padx=5)
ber_var.trace_add("write", update_berries) 

#CHESTS
che_var = tk.StringVar()
chest_frame = ck.CTkFrame(r_frame, fg_color="#638991", corner_radius=5)
chest_frame.pack(anchor="e", pady=5, padx=10)
chest_entry = ck.CTkEntry(chest_frame, width= 60, textvariable=che_var)
chest_entry.insert(1, CH_NUM)
chest_entry.pack(side="left")
chest_button = ck.CTkSwitch(chest_frame, text="Chests", command=switcher, variable=CHESTS, onvalue="on", offvalue="off", width= 140)
chest_button.pack(side="left", padx=5)
che_var.trace_add("write", update_chests) 

#GUMMIES
gum_var = tk.StringVar()
gummies_frame = ck.CTkFrame(r_frame, fg_color="#638991", corner_radius=5)
gummies_frame.pack(anchor="e", pady=5, padx=10)
gummies_entry = ck.CTkEntry(gummies_frame, width= 60, textvariable=gum_var)
gummies_entry.insert(1, G_NUM)
gummies_entry.pack(side="left")
gummies_button = ck.CTkSwitch(gummies_frame, text="Gummies", command=switcher, variable=GUMMIES, onvalue="on", offvalue="off", width= 140)
gummies_button.pack(side="left", padx=5)
gum_var.trace_add("write", update_gummies) 

#COMMONS
com_var = tk.StringVar()
common_frame = ck.CTkFrame(r_frame, fg_color="#638991", corner_radius=5)
common_frame.pack(anchor="e", pady=5, padx=10)
common_entry = ck.CTkEntry(common_frame, width= 60, textvariable=com_var)
common_entry.insert(1, C_NUM)
common_entry.pack(side="left")
common_button = ck.CTkSwitch(common_frame, text="Commons", command=switcher, variable=COMMONS, onvalue="on", offvalue="off", width= 140)
common_button.pack(side="left", padx=5)
com_var.trace_add("write", update_commons) 

#UNCOMMONS
unc_var = tk.StringVar()
uncommon_frame = ck.CTkFrame(r_frame, fg_color="#638991", corner_radius=5)
uncommon_frame.pack(anchor="e", pady=5, padx=10)
uncommon_entry = ck.CTkEntry(uncommon_frame, width= 60, textvariable=unc_var)
uncommon_entry.insert(1, U_NUM)
uncommon_entry.pack(side="left")
uncommon_button = ck.CTkSwitch(uncommon_frame, text="Uncommons", command=switcher, variable=UNCOMMONS, onvalue="on", offvalue="off", width= 140)
uncommon_button.pack(side="left", padx=5)
unc_var.trace_add("write", update_uncommons) 


#-----------------


#move buttons up
blank = ck.CTkLabel(c_frame, bg_color="#263D42", text="")
blank.pack(side="bottom", pady=10)

save = ck.CTkButton(c_frame, text="Save Dungeon", fg_color="#21515c", hover_color="#17282b", corner_radius=6, command=Save)
save.pack(side="bottom", pady=10)

Run = ck.CTkButton(c_frame, text="Generate Dungeon", fg_color="#21515c", hover_color="#17282b", corner_radius=6, command=main)
Run.pack(side="bottom", pady=10)

openFile = ck.CTkButton(c_frame, text="Open Tileset", fg_color="#21515c", hover_color="#17282b", corner_radius=6, command=addFile)
openFile.pack(side="bottom", pady=10)

#dungeon image preview
image_label = ck.CTkLabel(c_frame, bg_color="#17282b", text="")
image_label.pack(side="top", padx=10, fill="both", pady=50, anchor="n", expand=True)


root.mainloop()