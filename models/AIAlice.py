#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
PyAISnake - 2018/2020 - by psy (epsylon@riseup.net)

You should have received a copy of the GNU General Public License along
with PyAISnake; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
import random

# movements strategy (evading suicidal behavior) and trying to identify next location...
class AIAlice(object):
    def extractName(self):
        name = "AliC3"
        return name

    def makeStrategy(self, allowed_moves, food, snake):
        if snake[0][0] == food[0]:
            if snake[0][1] < food[1]:
                    move = KEY_RIGHT
                    if move not in allowed_moves:
                        move = KEY_LEFT
            else:
                move = KEY_LEFT
                if move not in allowed_moves:
                    move = KEY_RIGHT
        else:
            if snake[0][0] < food[0]: 
                move = KEY_UP
                if move not in allowed_moves:
                    move = KEY_DOWN
            else:
                move = KEY_DOWN
                if move not in allowed_moves:
                    move = KEY_UP
        return move

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
        move = self.makeStrategy(allowed_moves, food, snake)
        return move
