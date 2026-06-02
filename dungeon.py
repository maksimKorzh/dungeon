#########################
#
#        PACKAGES
#
#########################

import sys
import json
import curses
import string
from random import randrange, choice

#########################
#
#       CONSTANTS
#
#########################

ROWS = 24
COLS = 80
OFFSET_X = 32
OFFSET_Y = 7

WALL_H = 'w'
WALL_V = 'W'
DOOR_H = 'd'
DOOR_V = 'D'
EMPTY = 'e'

FLOOR = '.'

PLAYER = [
  '!_o_',
  ' _|*',
]

#########################
#
#        VARIABLES
#
#########################

# ================
#  Encoding order
# ================
#
# [content, up, down, left, right]

with open('map.json') as f: dungeon = json.loads(f.read())

player_x = 15
player_y = 29

#########################
#
#       FUNCTIONS
#
#########################

def render_char(c):
  return {
    'w': '#',
    'd': '+',
    's': '*',
    'W': '#',
    'D': '+',
    'S': '*',
    'e': ' ',
    'o': ' '
  }[c]

def print_cell(col, row, x, y):
  for r in range(4):
    for c in range(6):
      if r == 2 and c == 1: screen.addstr(r+y, r+x-1, 'EXIT' if dungeon[row][col][0] == 'x' else '    ')
      else:
        if r == 0 and c in range(1, 5): screen.addch(r+y, c+x, render_char(dungeon[row][col][1]))
        if r == 3 and c in range(1, 5): screen.addch(r+y, c+x, render_char(dungeon[row][col][2]))
        if c == 0 and r in range(1, 3): screen.addch(r+y, c+x, render_char(dungeon[row][col][3]))
        if c == 5 and r in range(1, 3): screen.addch(r+y, c+x, render_char(dungeon[row][col][4]))
        #if r in range(1, 3) and c in range(1, 5): screen.addch(r+y, c+x, dungeon[row][col][0])

def print_player(x, y):
  for r in range(2):
    for c in range(4):
      screen.addch(r+y+1, c+x+1, PLAYER[r][c])

def render_dungeon():
  for row in range(3):
    for col in range(3):
      if row == 1 and col == 1: print_player(OFFSET_X+col*5, OFFSET_Y+row*3)
      else: print_cell(col+player_x, row+player_y, OFFSET_X+col*5, OFFSET_Y+row*3)
            #print_cell(col+player_x, row+player_y, col*7, row*4) cell spacing
  screen.refresh()

#########################
#
#          MAIN
#
#########################

# Init curses
screen = curses.initscr()
screen.nodelay(1)
curses.noecho()
curses.raw()
screen.keypad(1)
curses.start_color()
curses.use_default_colors()
curses.curs_set(0)

def read_key():
  global player_x, player_y
  ch = -1
  while ch == -1: ch = screen.getch()
  if ch == ord('j') and player_y < len(dungeon)-3 and dungeon[player_y+1][player_x+1][2] in 'ed': player_y += 1
  elif ch == ord('k') and player_y > 0 and dungeon[player_y+1][player_x+1][1] in 'ed': player_y -= 1
  elif ch == ord('h') and player_x > 0 and dungeon[player_y+1][player_x+1][3] in 'eD': player_x -= 1
  elif ch == ord('l') and player_x < len(dungeon[0])-3 and dungeon[player_y+1][player_x+1][4] in 'eD': player_x += 1
  if ch == ord('q'):
    curses.endwin()
    print(len(dungeon[0]), len(dungeon[1]), len(dungeon[-1]))
    sys.exit()

while True:
  render_dungeon()
  read_key()
