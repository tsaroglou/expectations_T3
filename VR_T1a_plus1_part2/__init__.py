from otree.api import *
from otree.api import Currency as c
import random

doc = """
Cooperation under Agreed Risk Experiment
"""
import json

class Constants(BaseConstants):
    name_in_url = 'cooperation_risk_main'
    players_per_group = 2
    num_rounds = 100    # Maximum rounds; experiment will end early once the lottery triggers.
    min_rounds = 20     # Must play at least 20 rounds before the lottery may end the game.
    # Payoff matrices:
    matrix_A = {
        ('C', 'C'): (6, 6),
        ('C', 'D'): (4, 7),
        ('D', 'C'): (7, 4),
        ('D', 'D'): (5, 5),
    }

    A1aa = matrix_A[('C', 'C')][0]
    A1ab = matrix_A[('C', 'D')][0]
    A1ba = matrix_A[('D', 'C')][0]
    A1bb = matrix_A[('D', 'D')][0]

    matrix_B = {
        ('C', 'C'): (7, 7),
        ('C', 'D'): (0, 12),
        ('D', 'C'): (12, 0),
        ('D', 'D'): (3, 3),
    }
    A2aa = matrix_B[('C', 'C')][0]
    A2ab = matrix_B[('C', 'D')][0]
    A2ba = matrix_B[('D', 'C')][0]
    A2bb = matrix_B[('D', 'D')][0]

class Subsession(BaseSubsession):

    def group_by_arrival_time_method(self, waiting_players):
        eligible = [p for p in waiting_players if p.participant.vars.get('passed_comprehension') is True]
        if len(eligible) >= 2:
            return eligible[:2]  # Match two eligible players
        return


    def creating_session(self):
        if self.round_number == 1:
            self.session.vars['game_sequences'] = {}


class Group(BaseGroup):
    current_game = models.StringField(initial='A')  # "A" for Matrix A, "B" for Matrix B.
    game_over = models.BooleanField(initial=False)
    finished = models.BooleanField(initial=False)
    display_group_id = models.IntegerField()
    pair_id = models.IntegerField()

    def set_game(self):
        votes = [p.field_maybe_none('vote') for p in self.get_players()]
        if any(vote is None for vote in votes):
            return
        if all(vote == 'Matrix B' for vote in votes):
            self.current_game = 'B'
        else:
            self.current_game = 'A'

    def set_payoffs(self):
        players = sorted(self.get_players(), key=lambda p: p.id_in_group)
        if any(p.action == "" for p in players):
            return
        current_game = self.field_maybe_none('current_game') or 'A'
        action_tuple = (players[0].action, players[1].action)
        if current_game == 'B':
            payoff_tuple = Constants.matrix_B.get(action_tuple)
        else:
            payoff_tuple = Constants.matrix_A.get(action_tuple)
        if payoff_tuple is None:
            return
        players[0].payoff = c(payoff_tuple[0])
        players[1].payoff = c(payoff_tuple[1])

class Player(BasePlayer):

    display_group_id = models.IntegerField()
    investment = models.CurrencyField(
        min=0, max=2,
        doc="""How much would you like to invest?"""
    )
    matrix_sequence = models.LongStringField()
    lottery_outcome = models.CurrencyField()
    investment_total = models.CurrencyField()


    first_attempt_passed = models.BooleanField(initial=False)
    second_attempt_passed = models.BooleanField(initial=False)

    pair = models.IntegerField()
    def find_partner(self):
        """Find the player in the same pair."""
        others = [p for p in self.subsession.get_players() if p.pair == self.pair and p.id_in_subsession != self.id_in_subsession]
        return others[0] if others else None

    decision_1 = models.StringField(
        choices=[
            ('L', '2€ for you  <br> 2€ for the other participant'),
            ('R', '2€ for you  <br> 1€ for the other participant')
        ],
        widget=widgets.RadioSelectHorizontal
    )
    decision_2 = models.StringField(
        choices=[
            ('L', '2€ for you <br> 2€ for the other participant'),
            ('R', '3€ for you  <br> 1€ for the other participant')
        ],
        widget=widgets.RadioSelectHorizontal
    )
    decision_3 = models.StringField(
        choices=[
            ('L', '2€ for you  <br> 2€ for the other participant'),
            ('R', '2€ for you  <br> 4€ for the other participant')
        ],
        widget=widgets.RadioSelectHorizontal
    )
    decision_4 = models.StringField(
        choices=[
            ('L', '2€ for you  <br> 2€ for the other participant'),
            ('R', '3€ for you  <br> 5€ for the other participant')
        ],
        widget=widgets.RadioSelectHorizontal
    )

    consent = models.BooleanField(label="Do you consent to participate?")

    vote = models.StringField(
        choices=['Matrix A', 'Matrix B'],
        label="Select the payoff matrix you prefer for this round",
        initial=""
    )
    action = models.StringField(
        choices=['C', 'D'],
        label="Choose your action: Action C or Action D",
        initial=""
    )
    treatment = models.StringField(initial="T1a")

    remove = models.BooleanField(initial=False)
    partner_removed = models.BooleanField(initial=False)


# BaseGamePage: All main pages check if the experiment is finished.
#
class BaseGamePage(Page):
    def is_displayed(self):
        # If the group is marked finished, skip.
        if self.group.finished:
            return False
        # If finished_round is recorded and current round is greater, skip.
        finished_round = self.participant.vars.get("finished_round")
        if finished_round is not None and self.round_number > finished_round:
            return False
        if self.round_number > 1:
            return not self.remove and not self.group.game_over


class WaitToBeGrouped(WaitPage):
    group_by_arrival_time = True
    template_name = 'Voted_Risk_T1a_MAIN/WaitToBeGrouped.html'


    @staticmethod
    def is_displayed(player):
        return player.participant.vars.get('passed_comprehension', False) and player.round_number == 1

    @staticmethod
    def after_all_players_arrive(group):
        session = group.session

        if 'pair_id_counter' not in session.vars:
            session.vars['pair_id_counter'] = 1

        group.display_group_id = session.vars['pair_id_counter']
        session.vars['pair_id_counter'] += 1

        for p in group.get_players():
            p.participant.vars['display_group_id'] = group.display_group_id
            p.display_group_id = group.display_group_id  # ✅ Set field so monitor shows it



# Voting – main game loop page.
class Voting(BaseGamePage):
    form_model = 'player'
    form_fields = ['vote', 'remove']
    def is_displayed(self):
        # only show if neither you nor your partner have been removed
        return not (self.remove or self.partner_removed or self.group.game_over)

    def before_next_page(self, timeout_happened, **kwargs):
        if timeout_happened:
            # you get removed on timeout
            self.remove = True
            partner = [p for p in self.group.get_players() if p != self][0]
            partner.partner_removed = True
        if self.remove and not self.partner_removed:
            other = [p for p in self.group.get_players() if p != self][0]
            # mark partner as removed as well so they skip ActionWaitPage
            other.remove = True
            other.partner_removed = True


    def vars_for_template(self):
        return {
            'matrix_A': Constants.matrix_A,
            'matrix_B': Constants.matrix_B,
            'A1aa': Constants.A1aa,
            'A1ab': Constants.A1ab,
            'A1ba': Constants.A1ba,
            'A1bb': Constants.A1bb,
            'A2aa': Constants.A2aa,
            'A2ab': Constants.A2ab,
            'A2ba': Constants.A2ba,
            'A2bb': Constants.A2bb,
        }


class VoteWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_game()

# Action – main game loop page; displays vote info and both matrices with the selected one highlighted.
class Action(BaseGamePage):
    form_model = 'player'
    form_fields = ['action', 'remove']

    def is_displayed(self):
        # show only if neither player nor partner has been removed, and game not over
        return not (self.remove or self.partner_removed or self.group.game_over)

    def before_next_page(self, timeout_happened, **kwargs):
        # Always default to C on natural timeout


        if timeout_happened:
            self.action = 'C'
        # If this player was flagged for removal via modal expiry, notify partner once
        if self.remove and not self.partner_removed:
            other = [p for p in self.group.get_players() if p != self][0]
            # mark partner as removed as well so they skip ActionWaitPage
            other.remove = True
            other.partner_removed = True
            # do not mark other.remove so they only see PartnerRemoved
            # partner_removed flag will route them to PartnerRemoved page

    def vars_for_template(self):
        partner = self.get_others_in_group()[0]
        return {
            'player_vote': self.vote,
            'partner_vote': partner.vote,
            'current_matrix': "Matrix B" if self.group.current_game == 'B' else "Matrix A",
            'matrix_A': Constants.matrix_A,
            'matrix_B': Constants.matrix_B,
            'A1aa': Constants.A1aa,
            'A1ab': Constants.A1ab,
            'A1ba': Constants.A1ba,
            'A1bb': Constants.A1bb,
            'A2aa': Constants.A2aa,
            'A2ab': Constants.A2ab,
            'A2ba': Constants.A2ba,
            'A2bb': Constants.A2bb,
        }


class ClearingOut(WaitPage):
    pass
class RemovalTimeout(Page):
    def is_displayed(self):
        return self.remove and not self.partner_removed

class PartnerRemoved(Page):
    def is_displayed(self):
        return self.partner_removed

class ActionWaitPage(WaitPage):
    timeout_seconds = 5

    def is_displayed(self):
        # show only if neither removed nor partner removed
        return not (self.remove or self.partner_removed)

    def next_page(self):
        # If this player was the one who timed out, send to RemoveTimeout
        if self.remove and not self.partner_removed:
            return 'RemoveTimeout'
        # If this player is the partner, send to PartnerRemoved
        if self.partner_removed:
            return 'PartnerRemoved'
        # Otherwise go to Results
        return 'Results'
    def after_all_players_arrive(self):
        self.group.set_payoffs()

# Results – displays votes, actions, and both players' payoffs.
class Results(BaseGamePage):
    form_model = 'player'
    form_fields = ['remove']  # we need remove here to catch timeout

    def is_displayed(self):
        # only show if neither you nor your partner have been removed
        return not (self.remove or self.partner_removed or self.group.game_over)

    def before_next_page(self, timeout_happened, **kwargs):
        if timeout_happened:
            # mark you removed
            self.remove = True
            # alert partner
            partner = [p for p in self.group.get_players() if p != self][0]
            partner.partner_removed = True

        if self.remove and not self.partner_removed:
            other = [p for p in self.group.get_players() if p != self][0]
            # mark partner as removed as well so they skip ActionWaitPage
            other.remove = True
            other.partner_removed = True
    def vars_for_template(self):
        partner = self.get_others_in_group()[0]
        return {
            'player_vote': self.vote,
            'partner_vote': partner.vote,
            'current_matrix': "Matrix B" if self.group.current_game == 'B' else "Matrix A",
            'player_action': self.action,
            'partner_action': partner.action,
            'payoff': self.payoff,
            'payoff_points': int(self.payoff),
            'partner_payoff_points': int(partner.payoff),
            'partner_payoff': partner.payoff,
            'matrix_A': Constants.matrix_A,
            'matrix_B': Constants.matrix_B,
            'A1aa': Constants.A1aa,
            'A1ab': Constants.A1ab,
            'A1ba': Constants.A1ba,
            'A1bb': Constants.A1bb,
            'A2aa': Constants.A2aa,
            'A2ab': Constants.A2ab,
            'A2ba': Constants.A2ba,
            'A2bb': Constants.A2bb,
        }

# LotteryWaitPage – group-level lottery to decide if the game should end.
class LotteryWaitPage(WaitPage):
    wait_for_all_players = True  # wait for your pair

    def is_displayed(self):
        # Only run the lottery once min_rounds is reached, and only if the game isn't already over.
        return (self.round_number >= Constants.min_rounds) and (not self.group.game_over)

    def after_all_players_arrive(self):
        # 50% chance to end the game this round
        if random.random() < 0.5:
            self.group.game_over = True
            for p in self.group.get_players():
                p.participant.vars["finished_round"] = self.round_number
        # If we "lose" the lottery, we leave game_over=False
        # and next round we'll come back here again until it finally hits.

class Investment(Page):
    form_model = 'player'
    form_fields = ['investment']

    def is_displayed(self):
        finished_round = self.participant.vars.get("finished_round")
        return not self.remove and finished_round is not None and self.round_number == finished_round

    def before_next_page(self, **kwargs):
        # Store the potential lottery outcome without affecting the actual payoff
        if random.choice([True, False]):  # 50% chance to win the lottery
            self.lottery_outcome = self.investment * 2.5
            self.investment_total =  self.lottery_outcome + 2-self.investment

        else:
            self.lottery_outcome = 0
            self.investment_total =  self.lottery_outcome + 2-self.investment

            # Only for player 1: collect matrix sequence from all rounds
        if self.id_in_group == 1:
            matrix_sequence = [p.group.current_game for p in self.in_all_rounds()]
            self.participant.vars['matrix_sequence'] = matrix_sequence
            self.matrix_sequence = json.dumps(matrix_sequence)


# AdditionalMeasurements – final additional page shown on the finished round.
class AdditionalMeasurements(Page):
    form_model = 'player'
    form_fields = ['decision_1', 'decision_2', 'decision_3', 'decision_4']

    def is_displayed(self):
        finished_round = self.participant.vars.get("finished_round")
        return not self.remove and finished_round is not None and self.round_number == finished_round


# PaymentAndDebrief – final page; shows accumulated payoff and ends experiment.
class PaymentAndDebrief(Page):
    def is_displayed(self):
        finished_round = self.participant.vars.get("finished_round")
        return not self.remove and ((finished_round is not None and self.round_number == finished_round) or self.round_number == Constants.num_rounds)
    def vars_for_template(self):
        total_payoff = sum([p.payoff for p in self.in_all_rounds()])/30

        return {
            'final_payment': c(total_payoff)
        }
    def before_next_page(self, timeout_happened):
        self.group.finished = True


    def app_after_this_page(self, upcoming_apps, **kwargs):
        return None



page_sequence = [
    WaitToBeGrouped,
    Voting,
    ClearingOut,
    RemovalTimeout,
    PartnerRemoved,
    VoteWaitPage,
    Action,
    ClearingOut,
    RemovalTimeout,
    PartnerRemoved,
    ActionWaitPage,
    Results,
    ClearingOut,
    RemovalTimeout,
    PartnerRemoved,
    LotteryWaitPage,
    Investment,
    AdditionalMeasurements,
    PaymentAndDebrief,
]