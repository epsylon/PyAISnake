#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
PyAISnake - 2018 - by psy (epsylon@riseup.net)

You should have received a copy of the GNU General Public License along
with PyAISnake; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
import random

# random movements strategy (but) evading suicidal behavior (you can easily identify some humans trying this way of life)
class AIBob(object):
    def extractName(self):
        name = "BoB"
        return name
    def makeMove(self, win, prev_move, food, snake):
        name = self.extractName()
        if prev_move == KEY_UP:
            allowed_moves = [KEY_UP, KEY_LEFT, KEY_RIGHT]
        elif prev_move == KEY_LEFT:
            allowed_moves = [KEY_UP, KEY_LEFT, KEY_DOWN]
        elif prev_move == KEY_RIGHT:
            allowed_moves = [KEY_UP, KEY_RIGHT, KEY_DOWN]
        elif prev_move == KEY_DOWN:
            allowed_moves = [KEY_LEFT, KEY_RIGHT, KEY_DOWN]
        else:
            allowed_moves = [KEY_UP, KEY_LEFT, KEY_RIGHT, KEY_DOWN]
        move = random.choice(allowed_moves)
        return move
