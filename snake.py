#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
PyAISnake - 2018/2020 - by psy (epsylon@riseup.net)

You should have received a copy of the GNU General Public License along
with PyAISnake; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import curses, random, time
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

######################################################################3

# import AI models into sandbox
from models.AIBob import AIBob
AIBob = AIBob() # BoB

# extract name from players
def extract_name(p):
    name = AIBob.extractName() # BoB
    return name

######################################################################3

# translate a thought into a text
def text_to_thought(move):
    if move == KEY_UP:
        thought = "UP"
    elif move == KEY_LEFT:
        thought = "LEFT"
    elif move == KEY_RIGHT:
        thought = "RIGHT"
    elif move == KEY_DOWN:
        thought = "DOWN"
    else:
        thought = "LEARNING..."
    return thought

# create matrix (with some random init values)
def init(evol, record, max_moves):
    curses.initscr()
    x_height = 0
    y_height = 20
    x_width = 60
    y_width = 0
    win = curses.newwin(y_height, x_width, x_height, y_width)
    win.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    win.border(0)
    win.nodelay(1)
    food = [random.randint(1, 18), random.randint(1, 58)] # set resources into matrix
    win.addch(food[0], food[1], '*')
    p1_a1 = random.randint(1, 10)
    p1_a2 = random.randint(1, 10)
    p1_b1 = random.randint(1, 10)
    p1_b2 = random.randint(1, 10)
    p1_c1 = random.randint(1, 10)
    p1_c2 = random.randint(1, 10)
    snake = [[p1_a1,p1_a2], [p1_b1,p1_b2], [p1_c1,p1_c2]] # generate starting point
    startGame(win, food, snake, evol, record, max_moves) # start NEW GAME!

# start a new game simulation
def startGame(win, food, snake, evol, record, max_moves):
    moves = 0
    score = 0
    thought = "WAKING UP..."

######################################################################3

    name = AIBob.extractName() # BoB
    move = AIBob.makeMove(win, None, food, snake) # BoB

######################################################################3

    moves += 1
    thought = text_to_thought(move)
    # build game
    while move != 27: # SPACEBAR
        win.border(0)
        win.addstr(0, 4, '| Moves: '+str(moves)+' - Max: '+str(max_moves)+' | Score: '+str(score)+' - Record: '+str(record)+' |')
        win.addstr(19, 4, '| '+str(name)+' -> GENERATION: '+str(evol)+' [IDEA: '+str(thought)+'] |')
        win.timeout(150 - int((len(snake)/5) + int(len(snake)/10)%120)) # if > length: > speed
        prevMove = move  
        event = win.getch()

######################################################################3

        move = AIBob.makeMove(win, prevMove, food, snake) # BoB

######################################################################3

        moves += 1
        thought = text_to_thought(move)
        move = move if event == -1 else event
        if move != KEY_UP and move != KEY_DOWN and move != KEY_LEFT and move != KEY_RIGHT : # ANY KEY for pause
            move = -1 # pause
            paused = ' GAME PAUSED: PRESS -SPACEBAR- TO RESTORE'
            win.addstr(9, 9, paused)
            while move != ord(' '):
                paused = '                                          ' # 42
                move = win.getch()
            win.addstr(9, 9, paused)
            win.addch(food[0], food[1], '*')
            move = prevMove
            continue
        if score >= record: # NEW record!
            record = score
        if moves >= max_moves: # NEW max moves!
            max_moves = moves
        snake.insert(0, [snake[0][0] + (move == KEY_DOWN and 1) + (move == KEY_UP and -1), snake[0][1] + (move == KEY_LEFT and -1) + (move == KEY_RIGHT and 1)])
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
