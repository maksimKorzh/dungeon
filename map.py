# Packages
import json
from PIL import Image

# Load image
img = Image.open('map.png')

# Get pixel data
pixels = img.load()

# Get image size
width, height = img.size

# Constants
WALL_H = 'w'
WALL_V = 'W'
DOOR_H = 'd'
DOOR_V = 'D'
SECRET_H = 's'
SECRET_V = 'S'
EMPTY = 'e'
FLOOR = '.'

# Map
map = []

# Parsed lines
lines_x = []
lines_y = []

# Horizontal items
start_x = 28
start_y = 14
width_x = 26
width_y = 24

# Loop over vertical cells
for row in range(31):
  # List of horizontal items
  line = []
  
  # Loop over horizontal cells
  for col in range(30):
    item_x = start_x+width_x*col
    item_y = start_y+width_y*row
    pixel = pixels[item_x, item_y]
    if pixel[0] in range(0, 10):
      line.append(WALL_H)
    elif pixel[0] in range(170, 210):
      #print('WALL_H', item_x, item_y, pixels[item_x, item_y])
      line.append(EMPTY)
    elif pixel[0] in range(210, 250):
      line.append(DOOR_H)
    elif pixel[0] in range(128, 169):
      line.append(SECRET_H)
    else:
      print('WALL_H', item_x, item_y, pixels[item_x, item_y])
      line.append('ERROR')
 
  # Populate lines X
  lines_x.append(line)

# Vertical items
start_x = 15
start_y = 26
width_x = 26
width_y = 24

# Loop over horizontal cells
for col in range(31):
  # List of vertical items
  line = []

  # Loop over vertical cells
  for row in range(30):
    item_x = start_x+width_x*col
    item_y = start_y+width_y*row
    pixel = pixels[item_x, item_y]
    if pixel[0] in range(0, 12):
      line.append(WALL_V)
      #print('WALL_V', item_x, item_y, pixels[item_x, item_y])
    elif pixel[0] in range(170, 194):
      line.append(EMPTY)
      #print('EMPTY', item_x, item_y, pixels[item_x, item_y])
    elif pixel[0] in range(195, 250):
      line.append(DOOR_V)
      #print('DOOR_V', item_x, item_y, pixels[item_x, item_y])
    elif pixel[0] in range(128, 169):
      line.append(SECRET_V)
      #print('SECRET_V', item_x, item_y, pixels[item_x, item_y])
    else:
      print('ERROR', item_x, item_y, pixels[item_x, item_y])
      line.append('ERROR')
    
  # Populate lines Y
  lines_y.append(line)

# Create map dataset
for row in range(30):
  line = []
  for col in range(30):
    up = lines_x[row][col]
    down = lines_x[row+1][col]
    left = lines_y[col][row]
    right = lines_y[col+1][row]
    line.append([FLOOR, up, down, left, right])
  map.append(line)

# Write dataset to JSON
with open('map.json', 'w') as f: f.write(json.dumps(map, indent=2))
