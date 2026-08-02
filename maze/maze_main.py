from maze.maze_engine import MazeEngine
from time import sleep_ms

game = MazeEngine()

while True:

    game.update()

    sleep_ms(30)