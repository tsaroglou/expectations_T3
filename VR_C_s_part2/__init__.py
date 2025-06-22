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
    min_rounds = 1     # Must play at least 20 rounds before the lottery may end the game.
    # Payoff matrices:
    matrix_A = {
        ('C', 'C'): (5, 5),
        ('C', 'D'): (3, 6),
        ('D', 'C'): (6, 3),
        ('D', 'D'): (4, 4),
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

    treatment_choices = ['T1', 'T2']

class Subsession(BaseSubsession):

    def group_by_arrival_time_method(self, waiting_players):
        eligible = [p for p in waiting_players if p.participant.vars.get('passed_comprehension') is True]
        if len(eligible) >= 2:
            return eligible[:2]  # Match two eligible players
        return


    def creating_session(self):
        if self.round_number == 1:
            # Assign treatment once
            treatment = random.choice(Constants.treatment_choices)
            self.session.vars['treatment'] = treatment
            self.session.vars['game_sequences'] = {}

        for player in self.get_players():
            player.treatment = self.session.vars['treatment']


class Group(BaseGroup):
    current_game = models.StringField(initial='B')  # "A" for Matrix A, "B" for Matrix B.
    game_over = models.BooleanField(initial=False)
    finished = models.BooleanField(initial=False)
    display_group_id = models.IntegerField()
    pair_id = models.IntegerField()

    def set_payoffs(self):
        players = sorted(self.get_players(), key=lambda p: p.id_in_group)
        if any(p.action == "" for p in players):
            return
        current_game = self.field_maybe_none('current_game')
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
    first_wrong_questions = models.LongStringField()
    second_wrong_questions = models.LongStringField()
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
    comprehension_answer = models.StringField(
        label="Based on the matrices shown, which matrix would be used if participants vote differently?",
        initial=""
    )
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
    treatment = models.StringField()
    remove = models.BooleanField(initial=False)
    # Comprehension check questions:
    comprehension_q1 = models.StringField(
        choices=["Game 1", "Game 2"],
        widget=widgets.RadioSelect,
        label="1. If one participant votes for Game 1 and the other for Game 2, which game is played?"
    )
    comprehension_q2 = models.StringField(
        choices=["Game 1", "Game 2"],
        widget=widgets.RadioSelect,
        label="2. Which game is played if both participants choose Game 2?"
    )
    comprehension_q3 = models.StringField(
        choices=[
            "I receive 5 points and my paired participant also receives 5 points.",
            "I receive 6 points and my paired participant receives 3 points.",
            "I receive 4 points and my paired participant also receives 4 point."
        ],
        widget=widgets.RadioSelect,
        label="3. In Game 1, if you choose Option A and your paired participant chooses Option A, what are the points?"
    )
    comprehension_q4 = models.StringField(
        choices=[
            "I receive 0 points and my paired participant receives 12 points.",
            "I receive 7 points and my paired participant also receives 7 points.",
            "I receive 12 points and my paired participant receives 0 points."
        ],
        widget=widgets.RadioSelect,
        label="4. In Game 2, if you choose Option A and your partner chooses Option B, what are the points?"
    )
    comprehension_q5 = models.StringField(
        choices=[
            "I receive 3 points and my paired participant receives 3 points.",
            "I receive 0 points and my paired participant receives 12 points.",
            "I receive 7 points and my paired participant receives 7 point."
        ],
        widget=widgets.RadioSelect,
        label="5. In Game 2, if you both choose Option B, what are the points?"
    )

    comprehension_q6 = models.StringField(
        choices=["Game 1", "Game 2"],
        widget=widgets.RadioSelect,
        label="6. If you and your paired participant both vote for Game 2, which game is played?"
    )
    comprehension_q7 = models.StringField(
        choices=["Game 1", "Game 2"],
        widget=widgets.RadioSelect,
        label="7. If one participant votes for Game 1 and the other for Game 2, which game is played?"
    )
    comprehension_q8 = models.StringField(
        choices=[
            "I receive 6 points and my paired participant receives 3 points.",
            "I receive 4 points and my paired participant also receives 4 points.",
            "I receive 5 points and my paired participant also receives 5 points."
        ],
        widget=widgets.RadioSelect,
        label="8. In Game 1, if you choose Option B and your paired participant chooses Option A, what are the points?"
    )
    comprehension_q9 = models.StringField(
        choices=[
            "I receive 3 points and my paired participant receives 3 points.",
            "I receive 0 points and my paired participant receives 12 points.",
            "I receive 3 points and my paired participant receives 6 points."
        ],
        widget=widgets.RadioSelect,
        label="9. In Game 2, if both choose Option B, what are the points?"
    )
    comprehension_q10 = models.StringField(
        choices=[
            "I receive 12 points and my paired participant receives 0 points.",
            "I receive 0 points and my paired participant receives 12 points.",
            "I receive 3 points and my paired participant receives 3 points."
        ],
        widget=widgets.RadioSelect,
        label="10. In Game 2, if you choose Option B and your partner chooses Option A, what are the points?"
    )
#
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
    template_name = 'VR_C_r_part2/WaitToBeGrouped.html'


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


# Action – main game loop page; displays vote info and both matrices with the selected one highlighted.
class Action(BaseGamePage):
    form_model = 'player'
    form_fields = ['action']

    def is_displayed(self):
        if self.round_number <= Constants.min_rounds:
            return not self.remove
        else:
            return not self.remove and not self.group.game_over

    def vars_for_template(self):
        partner = self.get_others_in_group()[0]
        return {
            'player_vote': self.vote,
            'partner_vote': partner.vote,
            'current_matrix': "Matrix B",
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

    def before_next_page(self, timeout_happened, **kwargs):
        if timeout_happened:
            self.action = 'C'


class ActionWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()

# Results – displays votes, actions, and both players' payoffs.
class Results(BaseGamePage):
    def is_displayed(self):
        if self.round_number <= Constants.min_rounds:
            return not self.remove
        else:
            return not self.remove and not self.group.game_over
    def vars_for_template(self):
        partner = self.get_others_in_group()[0]
        return {
            'player_vote': self.vote,
            'partner_vote': partner.vote,
            'current_matrix': "Matrix B",
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
    wait_for_all_groups = False
    def after_all_players_arrive(self):
        if self.round_number > Constants.min_rounds:
            if random.random() < 0.5:
                self.group.game_over = True
                for p in self.group.get_players():
                    p.participant.vars["finished_round"] = self.round_number
            else:
                self.group.game_over = False

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
        total_payoff = sum([p.payoff for p in self.in_all_rounds()])/25

        return {
            'final_payment': c(total_payoff)
        }
    def before_next_page(self, timeout_happened):
        self.group.finished = True


    def app_after_this_page(self, upcoming_apps, **kwargs):
        return None

page_sequence = [
    WaitToBeGrouped,
    Action,
    ActionWaitPage,
    Results,
    LotteryWaitPage,
    Investment,
    AdditionalMeasurements,
    PaymentAndDebrief,
]