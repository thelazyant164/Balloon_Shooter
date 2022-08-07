from content.src.game import Game


class Config:
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 600


new_game = Game(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
new_game.start_game()
