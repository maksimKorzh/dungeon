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

with open('map.json') as f: dungeon = json.loads(f.read())
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
  if ch == ord('j') and player_y < len(dungeon)-3 and dungeon[player_y+1][player_x+1][2] in 'ed': player_y += 1
  elif ch == ord('k') and player_y > 0 and dungeon[player_y+1][player_x+1][1] in 'ed': player_y -= 1
  elif ch == ord('h') and player_x > 0 and dungeon[player_y+1][player_x+1][3] in 'eD': player_x -= 1
  elif ch == ord('l') and player_x < len(dungeon[0])-3 and dungeon[player_y+1][player_x+1][4] in 'eD': player_x += 1
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

while True:
  render_dungeon()
  read_key()
