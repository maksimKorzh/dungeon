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

WALL_H = 'w'
WALL_V = 'W'
DOOR_H = 'd'
DOOR_V = 'D'
EMPTY = 'e'

FLOOR = '.'

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

dungeon = [
  [
    [FLOOR, WALL_H, EMPTY, WALL_V, EMPTY],
    [FLOOR, WALL_H, EMPTY, EMPTY, WALL_V],
    [FLOOR, WALL_H, EMPTY, WALL_V, EMPTY],
    [FLOOR, WALL_H, EMPTY, EMPTY, DOOR_V],
    [FLOOR, WALL_H, EMPTY, DOOR_V, EMPTY], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [FLOOR, EMPTY, EMPTY, WALL_V, EMPTY],
    [FLOOR, EMPTY, EMPTY, EMPTY, DOOR_V],
    [FLOOR, EMPTY, WALL_H, DOOR_V, EMPTY],
    [FLOOR, EMPTY, WALL_H, EMPTY, WALL_V],
    [FLOOR, EMPTY, WALL_H, WALL_V, EMPTY], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [FLOOR, EMPTY, EMPTY, WALL_V, EMPTY],
    [FLOOR, EMPTY, EMPTY, EMPTY, DOOR_V],
    [FLOOR, WALL_H, WALL_H, DOOR_V, EMPTY],
    [FLOOR, WALL_H, EMPTY, EMPTY, EMPTY],
    [FLOOR, WALL_H, EMPTY, EMPTY, WALL_V], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [FLOOR, EMPTY, WALL_H, WALL_V, EMPTY],
    [FLOOR, EMPTY, WALL_H, EMPTY, DOOR_V],
    [FLOOR, WALL_H, EMPTY, DOOR_V, WALL_V],
    [FLOOR, EMPTY, DOOR_H, WALL_V, EMPTY],
    [FLOOR, EMPTY, WALL_H, EMPTY, WALL_V], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [FLOOR, WALL_H, EMPTY, WALL_V, EMPTY],
    [FLOOR, WALL_H, EMPTY, EMPTY, WALL_V],
    [FLOOR, EMPTY, EMPTY, WALL_V, WALL_V],
    [FLOOR, DOOR_H, EMPTY, WALL_V, EMPTY],
    [FLOOR, WALL_H, EMPTY, EMPTY, DOOR_V], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [FLOOR, EMPTY, WALL_H, WALL_V, EMPTY],
    [FLOOR, EMPTY, DOOR_H, EMPTY, WALL_V],
    [FLOOR, EMPTY, EMPTY, WALL_V, WALL_V], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [FLOOR, WALL_H, EMPTY, WALL_V, EMPTY],
    [FLOOR, DOOR_H, EMPTY, EMPTY, WALL_V],
    [FLOOR, EMPTY, EMPTY, WALL_V, WALL_V], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [FLOOR, EMPTY, DOOR_H, WALL_V, EMPTY],
    [FLOOR, EMPTY, WALL_H, EMPTY, WALL_V],
    [FLOOR, EMPTY, EMPTY, WALL_V, EMPTY], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [FLOOR, DOOR_H, EMPTY, WALL_V, EMPTY],
    [FLOOR, WALL_H, WALL_H, EMPTY, EMPTY],
    [FLOOR, EMPTY, WALL_H, EMPTY, WALL_V], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [FLOOR, EMPTY, EMPTY, WALL_V, WALL_V],
    [FLOOR, WALL_H, EMPTY, WALL_V, EMPTY],
    [FLOOR, WALL_H, EMPTY, EMPTY, DOOR_V], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [FLOOR, EMPTY, DOOR_H, WALL_V, WALL_V],
    [FLOOR, EMPTY, DOOR_H, WALL_V, EMPTY],
    [FLOOR, EMPTY, WALL_H, EMPTY, WALL_V], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [FLOOR, DOOR_H, EMPTY, WALL_V, EMPTY],
    [FLOOR, DOOR_H, EMPTY, EMPTY, DOOR_V],
    [FLOOR, WALL_H, WALL_H, DOOR_V, EMPTY], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [FLOOR, EMPTY, DOOR_H, WALL_V, EMPTY],
    [FLOOR, EMPTY, WALL_H, EMPTY, DOOR_V],
    [FLOOR, WALL_H, WALL_H, DOOR_V, EMPTY], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [FLOOR, DOOR_H, EMPTY, WALL_V, EMPTY],
    [FLOOR, WALL_H, WALL_H, EMPTY, EMPTY],
    [FLOOR, WALL_H, WALL_H, EMPTY, EMPTY], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [FLOOR, EMPTY, EMPTY, WALL_V, WALL_V],
    [FLOOR, WALL_H, EMPTY, WALL_V, EMPTY],
    [FLOOR, WALL_H, EMPTY, EMPTY, EMPTY], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [FLOOR, EMPTY, EMPTY, WALL_V, WALL_V],
    [FLOOR, EMPTY, WALL_H, WALL_V, EMPTY],
    [FLOOR, EMPTY, DOOR_H, EMPTY, WALL_V], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [FLOOR, EMPTY, EMPTY, WALL_V, WALL_V],
    [FLOOR, WALL_H, EMPTY, WALL_V, EMPTY],
    [FLOOR, DOOR_H, EMPTY, EMPTY, WALL_V], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
  [
    [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
  ],
]

offset_x = 0
offset_y = 0

#########################
#
#       FUNCTIONS
#
#########################

def render_char(c):
  return {
    'w': 'w',
    'd': 'd',
    'W': 'W',
    'D': 'D',
    'e': '.'
  }[c]

def print_cell(col, row, x, y):
  for r in range(4):
    for c in range(6):
      if r == 0 and c in range(1, 5): screen.addch(r+y, c+x, render_char(dungeon[row][col][1]))
      if r == 3 and c in range(1, 5): screen.addch(r+y, c+x, render_char(dungeon[row][col][2]))
      if c == 0 and r in range(1, 3): screen.addch(r+y, c+x, render_char(dungeon[row][col][3]))
      if c == 5 and r in range(1, 3): screen.addch(r+y, c+x, render_char(dungeon[row][col][4]))
      #if r in range(1, 3) and c in range(1, 5): screen.addch(r+y, c+x, dungeon[row][col][0])

def render_dungeon():
  for row in range(3):
    for col in range(3):
      print_cell(col+offset_x, row+offset_y, 10+col*5, 3+row*3)
      #print_cell(col+offset_x, row+offset_y, 10+col*7, 3+row*4)
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
  global offset_x, offset_y
  ch = -1
  while ch == -1: ch = screen.getch()
  if ch == ord('j'): offset_y += 1
  elif ch == ord('k'): offset_y -= 1
  elif ch == ord('h'): offset_x -= 1
  elif ch == ord('l'): offset_x += 1
  if ch == ord('q'):
    curses.endwin()
    sys.exit()

while True:
  render_dungeon()
  read_key()
