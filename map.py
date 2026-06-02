import json
from PIL import Image

img = Image.open('map.png')
pixels = img.load()
width, height = img.size

map = []
lines_x = []
lines_y = []
start_x = 28
start_y = 14
width_x = 26
width_y = 24

for row in range(31):
  line = []
  for col in range(30):
    item_x = start_x+width_x*col
    item_y = start_y+width_y*row
    pixel = pixels[item_x, item_y]
    if pixel[0] in range(0, 10): line.append('w')
    elif pixel[0] in range(170, 210): line.append('e')
    elif pixel[0] in range(210, 250): line.append('d')
    elif pixel[0] in range(128, 169): line.append('s')
    else: line.append('ERROR')
  lines_x.append(line)

start_x = 15
start_y = 26
width_x = 26
width_y = 24

for col in range(31):
  line = []
  for row in range(30):
    item_x = start_x+width_x*col
    item_y = start_y+width_y*row
    pixel = pixels[item_x, item_y]
    if pixel[0] in range(0, 12): line.append('W')
    elif pixel[0] in range(170, 194): line.append('e')
    elif pixel[0] in range(195, 250): line.append('D')
    elif pixel[0] in range(128, 169): line.append('S')
    else: line.append('ERROR')
  lines_y.append(line)

for row in range(30):
  line = []
  for col in range(30):
    if col == 0: line.append(['.', 'o', 'o', 'o', 'W'])
    up = lines_x[row][col]
    down = lines_x[row+1][col]
    left = lines_y[col][row]
    right = lines_y[col+1][row]
    line.append(['.', up, down, left, right])
  if row == 0: map.append([['.', 'o', 'w', 'o', 'o'] for i in range(32)])
  line.append(['.', 'o', 'o', 'W', 'o'])
  map.append(line)
map.append([['.', 'w', 'o', 'o', 'o'] if i in range(1, 31) else ['.', 'o', 'o', 'o', 'o' ] for i in range(32)])
map[-1][16] = ['x', 'e', 'o', 'o', 'o']

for row in range(32):
  for col in range(32):
    if map[row][col][1] and map[row][col][2] != 'e': map[row][col][0] = '^'
    if map[row][col][3] and map[row][col][4] != 'e': map[row][col][0] = '^'

with open('map.json', 'w') as f: f.write(json.dumps(map, indent=2))
