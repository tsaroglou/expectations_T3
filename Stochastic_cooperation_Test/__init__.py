from otree.api import *
import random

doc = """
Interactive experiment: Cooperation vs. Defection game in groups of 2.
"""


class Constants(BaseConstants):
    name_in_url = 'cooperation_experiment'
    players_per_group = 2
    num_rounds = 10
    payoff_matrix_high = {
        ('A', 'A'): (2, 2),
        ('A', 'B'): (0, 3),
        ('B', 'A'): (3, 0),
        ('B', 'B'): (1, 1)
    }
    payoff_matrix_low = {
        ('A', 'A'): (1.2, 1.2),
        ('A', 'B'): (0, 2.2),
        ('B', 'A'): (2.2, 0),
        ('B', 'B'): (1, 1)
    }
    payment_rounds = [9, 10]  # Participants don't know this


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    use_low_payoff = models.BooleanField(initial=False)

    def set_payoffs(self):
        players = self.get_players()
        if any(p.decision is None for p in players):
            return  # Ensure both players have made a decision before proceeding

        choices = {p.id_in_group: p.decision for p in players}
        matrix = Constants.payoff_matrix_low if self.use_low_payoff else Constants.payoff_matrix_high

        p1, p2 = players
        p1.payoff, p2.payoff = matrix[(p1.decision, p2.decision)]

        # If any player defected, switch to the low payoff matrix in the next round
        if 'B' in choices.values():
            if self.round_number < Constants.num_rounds:
                self.in_round(self.round_number + 1).use_low_payoff = True
        else:
            if self.round_number < Constants.num_rounds:
                self.in_round(self.round_number + 1).use_low_payoff = False


class Player(BasePlayer):
    decision = models.StringField(choices=['A', 'B'], doc="Player's choice: Cooperate (A) or Defect (B)")


class Instructions(Page):
    def vars_for_template(self):
        return {
            'num_rounds': Constants.num_rounds,
            'payment_rounds': Constants.payment_rounds
        }


class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']

    def vars_for_template(self):
        return {
            'round_number': self.round_number,
            'use_low_payoff': self.group.use_low_payoff
        }

    def is_displayed(self):
        return self.round_number <= Constants.num_rounds

    def before_next_page(self):
        self.group.set_payoffs()


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class RoundSummary(Page):
    def vars_for_template(self):
        return {
            'player_decision': self.decision,
            'other_decision': self.get_others_in_group()[0].decision,
            'payoff': self.payoff,
            'next_game_type': 'more profitable' if not self.group.use_low_payoff else 'less profitable'
        }

    def is_displayed(self):
        return self.round_number < Constants.num_rounds


class FinalResults(Page):
    def vars_for_template(self):
        total_payoff = sum([p.payoff for p in self.in_rounds(9, 10)])
        return {
            'total_payoff': total_payoff
        }

    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [Instructions] + [Decision, ResultsWaitPage, RoundSummary] * (Constants.num_rounds - 1) + [FinalResults]