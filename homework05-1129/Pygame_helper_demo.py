from Game_helper import Player, Enemy, Cloud, Game

game_demo = Game(width = 800, width = 600)  # def __init__(self, width = 800, height = 600):

action = [False, False, False, False]  # [UP, Down, Left, Right]

while game_demo.running:
    image_name = game_demo.get_frame(action, QuitFlag = False)  # def get_frame(self, Key_press, QuitFlag = False):
    game_demo.running = False
