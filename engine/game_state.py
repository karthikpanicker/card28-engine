from enum import Enum


class GameStateConstants(Enum):
    STATE_ZERO = 1
    ROUND_ONE_BIDDING_DONE = 2
    ROUND_TWO_BIDDING_DONE = 3
    TRUMP_SHOWN = 4
    GAME_OVER = 5


class GameState():
    game_state: GameStateConstants

    def __init__(self):
        self.game_state: GameStateConstants = GameStateConstants.STATE_ZERO

    def get_game_state(self):
        return self.game_state

    def set_game_state(self, game_state: GameStateConstants):
        self.game_state = game_state