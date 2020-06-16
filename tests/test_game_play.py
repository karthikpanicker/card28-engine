import random
from unittest import TestCase

from pydealer import Card, VALUES, SUITS

from engine import constants
from engine.game28.game28_state import Game28State
from engine.game_engine_exception import GameEngineException
from engine.game_factory import GameFactory, GameType
from engine.player import Player, PlayerAction
from tests.test_round_one_bidding import TestRoundOneBidding


class TestGamePlay(TestCase):
    def test_game_play_all_player_same_suit(self):
        game = TestGamePlay.create_game_for_testing()
        game.player_action('player2', PlayerAction.CARD_PLAY_ACTION,
                           {constants.CARD_ABBREVIATION: Card("Jack", "Hearts").abbrev})
        game.player_action('player3', PlayerAction.CARD_PLAY_ACTION,
                           {constants.CARD_ABBREVIATION: Card("7", "Hearts").abbrev})
        game.player_action('player4', PlayerAction.CARD_PLAY_ACTION,
                           {constants.CARD_ABBREVIATION: Card("10", "Hearts").abbrev})
        game.player_action('player1', PlayerAction.CARD_PLAY_ACTION,
                           {constants.CARD_ABBREVIATION: Card("8", "Hearts").abbrev})

    def test_game_play_player3_cheating_wrong_suite(self):
        game = TestGamePlay.create_game_for_testing()
        game.player_action('player2', PlayerAction.CARD_PLAY_ACTION,
                           {constants.CARD_ABBREVIATION: Card("Jack", "Hearts").abbrev})
        with self.assertRaises(GameEngineException) as context:
            game.player_action('player3', PlayerAction.CARD_PLAY_ACTION,
                        {constants.CARD_ABBREVIATION: Card("8", "Diamond").abbrev})
        self.assertTrue("Player has another card of the same suit as the current round" in str(context.exception))

    def test_game_play_player4_play_card_not_in_hand(self):
        game = TestGamePlay.create_game_for_testing()
        game.player_action('player2', PlayerAction.CARD_PLAY_ACTION,
                           {constants.CARD_ABBREVIATION: Card("Jack", "Hearts").abbrev})
        game.player_action('player3', PlayerAction.CARD_PLAY_ACTION,
                           {constants.CARD_ABBREVIATION: Card("7", "Hearts").abbrev})
        with self.assertRaises(GameEngineException) as context:
            game.player_action('player4', PlayerAction.CARD_PLAY_ACTION,
                           {constants.CARD_ABBREVIATION: Card("9", "Hearts").abbrev})
        self.assertTrue("Card doesnt belong to this player" in str(context.exception))

    def test_game_play_player1_asks_for_trump(self):
        game = TestGamePlay.create_game_for_testing()
        game.player_action('player2', PlayerAction.CARD_PLAY_ACTION,
                           {constants.CARD_ABBREVIATION: Card("7", "Spades").abbrev})
        game.player_action('player3', PlayerAction.CARD_PLAY_ACTION,
                           {constants.CARD_ABBREVIATION: Card("King", "Spades").abbrev})
        game.player_action('player4', PlayerAction.CARD_PLAY_ACTION,
                           {constants.CARD_ABBREVIATION: Card("Jack", "Spades").abbrev})
        game.player_action('player1', PlayerAction.SHOW_TRUMP_ACTION,None)
        self.assertEqual(game.state, Game28State.TRUMP_SHOWN)

    def test_game_play_cheating_player4_asks_for_trump(self):
        game = TestGamePlay.create_game_for_testing()
        game.player_action('player2', PlayerAction.CARD_PLAY_ACTION,
                           {constants.CARD_ABBREVIATION: Card("7", "Spades").abbrev})
        game.player_action('player3', PlayerAction.CARD_PLAY_ACTION,
                           {constants.CARD_ABBREVIATION: Card("King", "Spades").abbrev})
        with self.assertRaises(GameEngineException) as context:
            game.player_action('player4', PlayerAction.SHOW_TRUMP_ACTION,None)
        self.assertTrue("Can't ask to show trump when the player has the same suite" in str(context.exception))

    def test_game_play_two_rounds(self):
        game = TestGamePlay.create_game_for_testing()
        game.player_action('player2', PlayerAction.CARD_PLAY_ACTION,
                           {constants.CARD_ABBREVIATION: Card("7", "Diamonds").abbrev})
        game.player_action('player3', PlayerAction.CARD_PLAY_ACTION,
                           {constants.CARD_ABBREVIATION: Card("Jack", "Diamonds").abbrev})
        game.player_action('player4', PlayerAction.CARD_PLAY_ACTION,
                           {constants.CARD_ABBREVIATION: Card("Queen", "Diamonds").abbrev})
        game.player_action('player1', PlayerAction.CARD_PLAY_ACTION,
                           {constants.CARD_ABBREVIATION: Card("10", "Diamonds").abbrev})
        game.player_action('player3', PlayerAction.CARD_PLAY_ACTION,
                           {constants.CARD_ABBREVIATION: Card("Jack", "Clubs").abbrev})
        game.player_action('player4', PlayerAction.CARD_PLAY_ACTION,
                           {constants.CARD_ABBREVIATION: Card("9", "Clubs").abbrev})
        game.player_action('player1', PlayerAction.CARD_PLAY_ACTION,
                           {constants.CARD_ABBREVIATION: Card("Ace", "Clubs").abbrev})
        game.player_action('player2', PlayerAction.CARD_PLAY_ACTION,
                           {constants.CARD_ABBREVIATION: Card("Queen", "Clubs").abbrev})



    @staticmethod
    def create_game_for_testing():
        player_dict = {1: Player('player1', 1), 2: Player('player2', 2), 3: Player('player3', 3),
                       4: Player('player4', 4), }
        game = GameFactory.get_game_implementation(GameType.TWENTY_EIGHT, player_dict, None)
        TestGamePlay.add_cards_without_dealing(player_dict)
        game.state = Game28State.ROUND_ONE_DEALING_DONE
        game.player_action('player2', PlayerAction.BIDDING_ACTION,
                           {constants.BID_VALUE: game.settings.get_setting_value(constants.MIN_BID_VALUE),
                            constants.TRUMP_CARD_ABBREVIATION: Card("7", "Spades").abbrev})
        game.player_action('player3', PlayerAction.BIDDING_ACTION,
                           {constants.BID_VALUE: game.settings.get_setting_value(constants.MIN_BID_VALUE) + 1,
                            constants.TRUMP_CARD_ABBREVIATION: Card("Jack", "Clubs").abbrev})
        game.player_action('player4', PlayerAction.BIDDING_ACTION,
                           {constants.BID_VALUE: game.settings.get_setting_value(constants.MIN_BID_VALUE) + 2,
                            constants.TRUMP_CARD_ABBREVIATION: Card("8", "Spades").abbrev})
        game.player_action('player1', PlayerAction.BIDDING_ACTION,
                           {constants.BID_VALUE: game.settings.get_setting_value(constants.MIN_BID_VALUE) + 3,
                            constants.TRUMP_CARD_ABBREVIATION: Card("9", "Hearts").abbrev})
        game.state = Game28State.ROUND_TWO_DEALING_DONE
        game.player_action('player2', PlayerAction.BIDDING_ACTION, {constants.BID_VALUE: constants.PASS})
        game.player_action('player3', PlayerAction.BIDDING_ACTION, {constants.BID_VALUE: constants.PASS})
        game.player_action('player4', PlayerAction.BIDDING_ACTION, {constants.BID_VALUE: constants.PASS})
        game.player_action('player1', PlayerAction.BIDDING_ACTION, {constants.BID_VALUE: constants.PASS})
        return game

    @staticmethod
    def get_random_card_abbreviation_for_next_player(game):
        player = game.player_pos_dict[game.get_next_player_pos()]
        card = random.choice(player.cards)
        return card.abbrev

    @staticmethod
    def add_cards_without_dealing(player_dict):
        for pos, player in player_dict.items():
            if pos == 2:
                player.add_cards([Card("7", "Diamonds"), Card("10", "Clubs"), Card("Queen", "Spades"),
                                  Card("Jack", "Hearts"), Card("King", "Diamonds"), Card("Queen", "Clubs"),
                                  Card("7", "Spades"), Card("10", "Spades")])
            elif pos == 3:
                player.add_cards([Card("7", "Hearts"), Card("Ace", "Hearts"), Card("8", "Diamonds"),
                                  Card("Jack", "Diamonds"), Card("King", "Clubs"), Card("Jack", "Clubs"),
                                  Card("9", "Spades"), Card("King", "Spades")])
            elif pos == 4:
                player.add_cards([Card("9", "Diamonds"), Card("Queen", "Diamonds"), Card("Queen", "Hearts"),
                                  Card("9", "Clubs"), Card("Ace", "Spades"), Card("8", "Spades"),
                                  Card("Jack", "Spades"), Card("10", "Hearts")])
            elif pos == 1:
                player.add_cards([Card("10", "Diamonds"), Card("Ace", "Diamonds"), Card("7", "Clubs"),
                                  Card("8", "Clubs"), Card("Ace", "Clubs"), Card("8", "Hearts"),
                                  Card("9", "Hearts"), Card("King", "Hearts")])



































