import sys
import json
import curses
import string
from random import randrange, choice

ROWS = 24
COLS = 80
OFFSET_X = 32
OFFSET_Y = 7
FLOOR = '.'
PLAYER = [
  '!_o_',
  ' _|*',
]

with open('./map/map.json') as f: dungeon = json.loads(f.read())
hidden_doors = [
  [[14, 1, 4], [15, 1, 3]],
  [[21, 2, 4], [22, 2, 3]],
  [[7, 5, 4], [8, 5, 3]],
  [[26, 12, 2], [26, 13, 1]],
  [[7, 14, 2], [7, 15, 1]],
  [[9, 16, 4], [10, 16, 3]],
  [[10, 16, 4], [11, 16, 3]],
  [[7, 19, 2], [7, 20, 1]],
  [[27, 19, 4], [28, 19, 3]],
  [[20, 22, 2], [20, 23, 1]],
  [[5, 24, 4], [6, 24, 3]],
  [[24, 25, 2], [24, 26, 1]],
  [[11, 29, 2], [11, 30, 1]],
  [[15, 29, 4], [16, 29, 3]],
  [[28, 30, 4], [29, 30, 3]]
]
player_x = 15
player_y = 29

def render_char(c):
  return {
    'w': '#',
    'd': '+',
    's': '*',
    'W': '#',
    'D': '+',
    'S': '*',
    '^': '#',
    'e': ' ',
    'o': ' '
  }[c]

def print_cell(col, row, x, y):
  for r in range(4):
    for c in range(6):
      if row == player_y+1 and \
         col == player_x and \
         dungeon[row][col][4] != 'e' and \
         c in range(0, 5):
        screen.addch(r+y, c+x, ' ')
      elif row == player_y+1 and \
           col == player_x+2 and \
           dungeon[row][col][3] != 'e' and \
           c in range(1, 6):
        screen.addch(r+y, c+x, ' ')
      elif row == player_y and \
           col == player_x+1 and \
           dungeon[row][col][2] != 'e' and \
           r in range(0, 3):
        screen.addch(r+y, c+x, ' ')
      elif row == player_y+2 and \
           col == player_x+1 and \
           dungeon[row][col][1] != 'e' and \
           r in range(1, 4):
        screen.addch(r+y, c+x, ' ')
      else:
        if r == 2 and c == 1: screen.addstr(r+y, r+x-1, 'EXIT' if dungeon[row][col][0] == 'x' else '    ')
        else:
          if r == 0 and c in range(1, 5): screen.addch(r+y, c+x, render_char(dungeon[row][col][1]))
          if r == 3 and c in range(1, 5): screen.addch(r+y, c+x, render_char(dungeon[row][col][2]))
          if c == 0 and r in range(1, 3): screen.addch(r+y, c+x, render_char(dungeon[row][col][3]))
          if c == 5 and r in range(1, 3): screen.addch(r+y, c+x, render_char(dungeon[row][col][4]))
          if r == 0 and c == 0: screen.addch(r+y, c+x, '#')
          if r == 0 and c == 5: screen.addch(r+y, c+x, '#')
          if r == 3 and c == 0: screen.addch(r+y, c+x, '#')
          if r == 3 and c == 5: screen.addch(r+y, c+x, '#')
          try:
            if r == 0 and c == 0:
              if dungeon[row][col][1] in 'eo' and \
                 dungeon[row][col][3] in 'eo' and \
                 dungeon[row-1][col][2] in 'eo' and \
                 dungeon[row][col-1][1] in 'eo':
                screen.addch(r+y, c+x, ' ')
            if r == 0 and c == 5:
              if dungeon[row][col][1] in 'eo' and \
                 dungeon[row][col][4] in 'eo' and \
                 dungeon[row-1][col][4] in 'eo' and \
                 dungeon[row][col+1][1] in 'eo':
                screen.addch(r+y, c+x, ' ')
            if r == 3 and c == 0:
              if dungeon[row][col][2] in 'eo' and dungeon[row][col][3] in 'eo':
                screen.addch(r+y, c+x, ' ')
            if r == 3 and c == 5:
              if dungeon[row][col][2] in 'eo' and dungeon[row][col][4] in 'eo':
                screen.addch(r+y, c+x, ' ')
          except: pass

def print_player(x, y):
  for r in range(2):
    for c in range(4):
      screen.addch(r+y+1, c+x+1, PLAYER[r][c])

def render_dungeon():
  if dungeon[player_y+1][player_x+1][0] == '.':
    screen.addstr(OFFSET_Y-5, OFFSET_X+3,     '   ROOM  ')
  else: screen.addstr(OFFSET_Y-5, OFFSET_X+3, ' CORRIDOR')
  for row in range(3):
    for col in range(3):
      if row == 0 and col == 0 or \
         row == 0 and col == 2 or \
         row == 2 and col == 0 or \
         row == 2 and col == 2: continue
      elif row == 1 and col == 1: print_player(OFFSET_X+col*5, OFFSET_Y+row*3)
      else: print_cell(col+player_x, row+player_y, OFFSET_X+col*5, OFFSET_Y+row*3)
  screen.refresh()

def read_key():
  global player_x, player_y
  ch = -1
  while ch == -1: ch = screen.getch()
  if ch == curses.KEY_DOWN and player_y < len(dungeon)-3 and dungeon[player_y+1][player_x+1][2] in 'eds^': player_y += 1
  elif ch == curses.KEY_UP and player_y > 0 and dungeon[player_y+1][player_x+1][1] in 'eds^': player_y -= 1
  elif ch == curses.KEY_LEFT and player_x > 0 and dungeon[player_y+1][player_x+1][3] in 'eDS^': player_x -= 1
  elif ch == curses.KEY_RIGHT and player_x < len(dungeon[0])-3 and dungeon[player_y+1][player_x+1][4] in 'eDS^': player_x += 1
  if ch == ord('q'):
    curses.endwin()
    sys.exit()

screen = curses.initscr()
screen.nodelay(1)
curses.noecho()
curses.raw()
screen.keypad(1)
curses.start_color()
curses.use_default_colors()
curses.curs_set(0)

def init_level():
  for door_pair in hidden_doors:
    if randrange(0, 7) != 3:
      for door in door_pair:
        dungeon[door[1]][door[0]][door[2]] = '^'

init_level()
while True:
  render_dungeon()
  read_key()
