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
from models.AIAlice import AIAlice

bots = ['AIBoB','AIAlice']

######################################################################3

class BoxSelector:
    def __init__(self, bots):
        self.TEXTBOX_WIDTH = 50
        self.TEXTBOX_HEIGHT = 6
        self.PAD_WIDTH = 400
        self.PAD_HEIGHT = 10000

    def pick(self):
        self._init_curses()
        self._create_pad()
        windows = self._make_textboxes()
        picked = self._select_textbox(windows)
        self._end_curses()
        return picked

    def _init_curses(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.keypad(1)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.stdscr.bkgd(curses.color_pair(2))
        self.stdscr.refresh()

    def _end_curses(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

    def _create_pad(self):
        self.pad = curses.newpad(self.PAD_HEIGHT, self.PAD_WIDTH)
        self.pad.box()

    def _make_textboxes(self):
        maxy, maxx = self.stdscr.getmaxyx()
        windows = []
        i = 1
        for s in bots:
            windows.append(self.pad.derwin(self.TEXTBOX_HEIGHT,
                    self.TEXTBOX_WIDTH, i, self.PAD_WIDTH//2-self.TEXTBOX_WIDTH//2))
            i += self.TEXTBOX_HEIGHT
        for k in range(len(windows)):
            windows[k].box()
            windows[k].addstr(4, 4, '{0:X} - {1}'.format(k, bots[k]))
        return windows

    def _center_view(self, window):
        cy, cx = window.getbegyx()
        maxy, maxx = self.stdscr.getmaxyx()
        self.pad.refresh(cy, cx, 1, maxx//2 - self.TEXTBOX_WIDTH//2, maxy-1, maxx-1)
        return (cy, cx)

    def _select_textbox(self, windows):
        topy, topx = self._center_view(windows[0])
        current_selected = 0
        last = 1
        top_textbox = windows[0]
        while True:
            windows[current_selected].bkgd(curses.color_pair(1))
            windows[last].bkgd(curses.color_pair(2))
            maxy, maxx = self.stdscr.getmaxyx()
            cy, cx = windows[current_selected].getbegyx()
            if ((topy + maxy - self.TEXTBOX_HEIGHT) <= cy):
                top_textbox = windows[current_selected]
            if topy >= cy + self.TEXTBOX_HEIGHT:
                top_textbox = windows[current_selected]
            if last != current_selected:
                last = current_selected
            topy, topx = self._center_view(top_textbox)
            c = self.stdscr.getch()
            if c == ord('0') or c == 258: # KEY_UP
                if current_selected >= len(windows)-1:
                    current_selected = 0 
                else:
                    current_selected += 1
            elif c == ord('1') or c == 259: # KEY_DOWN
                if current_selected <= 0:
                    current_selected = len(windows)-1
                else:
                    current_selected -= 1
            elif c == ord('q') or c == 27: # ESC
                break
            elif c == curses.KEY_ENTER or c == 10:
                return int(current_selected)

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
    choice = BoxSelector(bots).pick()
    if not choice:
        choice = 0 # BoB
    name = bots[choice]
    if name == "AIBoB":
        bot = AIBob() # BoB
    else:
        bot = AIAlice() #Alice
    move = bot.makeMove(win, None, food, snake) # first move
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
        move = bot.makeMove(win, prevMove, food, snake) # rest of movements
        moves += 1
        thought = text_to_thought(move)
        move = move if event == -1 else event
        if move != KEY_UP and move != KEY_DOWN and move != KEY_LEFT and move != KEY_RIGHT : # ANY KEY for pause
            if move == 27: # ESC
                breaked = ' GAME FINISHED: GOOD BYE! ;-)'
                win.addstr(9, 9, breaked)
                win.getch()
                curses.nocbreak()
                curses.echo()
                curses.endwin()
                break
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
