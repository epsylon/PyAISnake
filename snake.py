#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
PyAISnake - 2018 - by psy (epsylon@riseup.net)

You should have received a copy of the GNU General Public License along
with PyAISnake; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import curses, random, time
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

# generate a random AI thought (evading suicidal moves)
def move(prevKey):
    if prevKey == KEY_UP:
        moves = [KEY_UP, KEY_LEFT, KEY_RIGHT]
    elif prevKey == KEY_LEFT:
        moves = [KEY_UP, KEY_LEFT, KEY_DOWN]
    elif prevKey == KEY_RIGHT:
        moves = [KEY_UP, KEY_RIGHT, KEY_DOWN]
    elif prevKey == KEY_DOWN:
        moves = [KEY_LEFT, KEY_RIGHT, KEY_DOWN]
    else:
        moves = [KEY_UP, KEY_LEFT, KEY_RIGHT, KEY_DOWN]
    key = random.choice(moves)
    return key

# translate a thought into a text
def text_to_thought(key):
    if key == KEY_UP:
        thought = "UP"
    elif key == KEY_LEFT:
        thought = "LEFT"
    elif key == KEY_RIGHT:
        thought = "RIGHT"
    elif key == KEY_DOWN:
        thought = "DOWN"
    else:
        thought = "LEARNING..."
    return thought

# create matrix (with some random init values)
def init(evol, record, max_moves):
    curses.initscr()
    win = curses.newwin(20, 60, 0, 0)
    win.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    win.border(0)
    win.nodelay(1)
    score = 0
    thought = "LEARNING..."
    moves = 0
    key = move(None)
    food = [random.randint(1, 18), random.randint(1, 58)]
    snake = [[random.randint(0, 11),random.randint(0, 11)], [random.randint(0, 11),random.randint(0, 11)], [random.randint(0, 11),random.randint(0, 11)]]
    win.addch(food[0], food[1], '*')
    # build game
    while key != 27:
        win.border(0)
        win.addstr(0, 4, '| Moves: '+str(moves)+' - Max: '+str(max_moves)+' | Score: '+str(score)+' - Record: '+str(record)+' |')
        win.addstr(19, 4, '| PyAISnake -> MUTATION: '+str(evol)+' [IDEA: '+str(thought)+'] |')
        win.timeout(150 - (len(snake)/5 + len(snake)/10)%120) # if > length: > speed
        prevKey = key  
        event = win.getch()
        key = move(prevKey) # AI model reply (Brain -> HERE!)
        moves += 1
        thought = text_to_thought(key)
        key = key if event == -1 else event
        if key == ord(' '): # SPACE BAR for pause
            key = -1 # pause
            paused = ' INFO: GAME PAUSED... '
            win.addstr(9, 18, paused)
            while key != ord(' '):
                paused = '                      '
                key = win.getch()
            win.addstr(9, 18, paused)
            win.addch(food[0], food[1], '*')
            key = prevKey
            continue
        if score >= record: # NEW record!
            record = score
        if moves >= max_moves: # NEW max moves!
            max_moves = moves
        snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])
        if snake[0][0] == 0: 
            snake[0][0] = 18
        if snake[0][1] == 0: 
            snake[0][1] = 58
        if snake[0][0] == 19: 
            snake[0][0] = 1
        if snake[0][1] == 59: 
            snake[0][1] = 1
        if snake[0] in snake[1:]: # GAME LOST ;-(
            win.addstr(9, 18, ' SORRY: GAME OVER !!!')
            win.addstr(19, 4, '| PyAISnake -> MUTATION: '+str(evol)+' [IDEA: TRYING AGAIN!] |')
            if score >= record: # NEW record!
                record = score
            if moves >= max_moves: # NEW max moves!
                max_moves = moves -1
            event = win.getch()
            time.sleep(2)
            evol += 1
            init(evol, record, max_moves)
        if snake[0] == food:
            food = []
            score += 1
            while food == []:
                food = [random.randint(1, 18), random.randint(1, 58)]
                if food in snake: food = []
            win.addch(food[0], food[1], '*')
        else:    
            last = snake.pop()
            try:
                win.addch(last[0], last[1], ' ')
            except:
                pass
        try:
            win.addch(snake[0][0], snake[0][1], '#')   
        except:
            pass
init(0, 0, 0) # start a new GAME ;-)
