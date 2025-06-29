from otree.api import *
from otree.api import Currency as c
import random

doc = """
Cooperation under Agreed Risk Experiment
"""
import json

class Constants(BaseConstants):
    name_in_url = 'cooperation_risk_'
    players_per_group = None
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

    def determine_special_payoffs(self):
        players = self.get_players()
        # Randomly select one participant for a special payout based on their decisions
        special_paying_player = random.choice(players)
        special_paying_player.is_paid = True  # Necesitarás un campo para rastrear quién recibe el pago
        special_paying_player.paying_player = True

        decision_num = random.choice(['1', '2', '3', '4'])

        # Access the decision attribute dynamically based on the chosen decision number
        decision_selected = getattr(special_paying_player, f'decision_{decision_num}')

        # Randomly select another participant
        other_player = random.choice([p for p in players if p != special_paying_player])
        other_player.is_paid = True  # Necesitarás un campo para rastrear quién recibe el pago
        other_player.other_player = True

        # Update database fields
        special_paying_player.special_paying_player_id = special_paying_player.unique_in_session_id
        special_paying_player.decision_num = decision_num
        special_paying_player.decision_selected = decision_selected
        special_paying_player.other_player_id = other_player.unique_in_session_id

        # Store similar info for the other player if necessary (optional)
        other_player.other_player_id = other_player.unique_in_session_id  # This might be redundant

        # Calculate payoffs based on the selected decision
        if decision_selected == 'L':
            special_paying_player.payoff += c(2)  # both get 2
            other_player.payoff += c(2)
        else:
            if decision_num == '1':
                special_paying_player.payoff += c(2)  # payer gets 2, other gets 1
                other_player.payoff += c(1)
            elif decision_num == '2':
                special_paying_player.payoff += c(3)  # payer gets 3, other gets 1
                other_player.payoff += c(1)
            elif decision_num == '3':
                special_paying_player.payoff += c(4)  # payer gets 4, other gets 2
                other_player.payoff += c(2)
            elif decision_num == '4':
                special_paying_player.payoff += c(3)  # payer gets 3, other gets 5
                other_player.payoff += c(5)

    def creating_session(self):
        if self.round_number == 1:
            treatment = random.choice(Constants.treatment_choices)
            self.session.vars['treatment'] = treatment

        for player in self.get_players():
            player.treatment = self.session.vars['treatment']

        if self.round_number == 1:
            for player in self.get_players():
                player.group = None  # <<< MANUALLY ungroup everyone!


class Group(BaseGroup):
    current_game = models.StringField(initial='A')  # "A" for Matrix A, "B" for Matrix B.
    game_over = models.BooleanField(initial=False)
    finished = models.BooleanField(initial=False)

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
        if any(p.consent and p.action == "" for p in players):
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
            self.consent = self.participant.vars.get("consent", False)
        return self.consent and not self.remove and not self.group.game_over

#
# PAGES
#

# Consent – shown only in round 1.
class Consent(Page):
    form_model = 'player'
    form_fields = ['consent']
    def is_displayed(self):
        return self.round_number == 1
    def before_next_page(self, timeout_happened):
        self.participant.vars["consent"] = self.consent
        if not self.consent:
            self.remove = True

# NoConsent – for non-consenting players.
class NoConsent(Page):
    def is_displayed(self):
        if self.round_number > 1:
            self.consent = self.participant.vars.get("consent", False)
        return not self.consent or self.remove
    def vars_for_template(self):
        return {'message': "You have chosen not to participate. Thank you for your time."}

# Instructions – shown only in round 1.
class Instructions(Page):
    def is_displayed(self):
        return self.consent and not self.remove and self.round_number == 1
    def vars_for_template(self):
        return {
            'C': Constants,
            'delta': 50,  # example lottery probability percentage
            'A1aa': Constants.A1aa,
            'A1ab': Constants.A1ab,
            'A1ba': Constants.A1ba,
            'A1bb': Constants.A1bb,
            'A2aa': Constants.A2aa,
            'A2ab': Constants.A2ab,
            'A2ba': Constants.A2ba,
            'A2bb': Constants.A2bb,
        }

class Instructions2(Page):
    def is_displayed(self):
        return self.consent and not self.remove and self.round_number == 1
    def vars_for_template(self):
        return {
            'C': Constants,
            'delta': 50,  # example lottery probability percentage
            'A1aa': Constants.A1aa,
            'A1ab': Constants.A1ab,
            'A1ba': Constants.A1ba,
            'A1bb': Constants.A1bb,
            'A2aa': Constants.A2aa,
            'A2ab': Constants.A2ab,
            'A2ba': Constants.A2ba,
            'A2bb': Constants.A2bb,
        }

class instructions_snippet(Page):
    def is_displayed(self):
        return self.consent and not self.remove and self.round_number == 1
    def vars_for_template(self):
        return {
            'C': Constants,
            'delta': 50,  # example lottery probability percentage
            'A1aa': Constants.A1aa,
            'A1ab': Constants.A1ab,
            'A1ba': Constants.A1ba,
            'A1bb': Constants.A1bb,
            'A2aa': Constants.A2aa,
            'A2ab': Constants.A2ab,
            'A2ba': Constants.A2ba,
            'A2bb': Constants.A2bb,
        }

# ComprehensionCheck – shown only in round 1.
class ComprehensionCheck(Page):
    form_model = 'player'
    form_fields = ['comprehension_q1', 'comprehension_q2', 'comprehension_q3', 'comprehension_q4', 'comprehension_q5']

    def is_displayed(self):
        return self.consent and not self.remove and self.round_number == 1

    def before_next_page(self, timeout_happened):
        correct_answers = {
            'comprehension_q1': 'Game 1',
            'comprehension_q2': 'Game 2',
            'comprehension_q3': 'I receive 5 points and my paired participant also receives 5 points.',
            'comprehension_q4': 'I receive 0 points and my paired participant receives 12 points.',
            'comprehension_q5': 'I receive 3 points and my paired participant receives 3 points.',
        }
        wrong = []
        for field, correct in correct_answers.items():
            if getattr(self, field) != correct:
                wrong.append(field)
        self.first_wrong_questions = json.dumps(wrong)
        self.first_attempt_passed = (len(wrong) == 0)

    def vars_for_template(self):
        return {
            'C': Constants,
            'app_name': Constants.name_in_url,
            'A1aa': Constants.A1aa,
            'A1ab': Constants.A1ab,
            'A1ba': Constants.A1ba,
            'A1bb': Constants.A1bb,
            'A2aa': Constants.A2aa,
            'A2ab': Constants.A2ab,
            'A2ba': Constants.A2ba,
            'A2bb': Constants.A2bb,
        }



class ComprehensionFeedback(Page):
    """
    After ComprehensionCheck, show each answer,
    highlight correct/incorrect and give explanations.
    """
    def is_displayed(self):
        # show to everyone (even if they failed) on round 1
        return self.consent and self.round_number == 1

    def vars_for_template(self):
        # maps your field → correct answer + explanation + label
        feedback_map = {
            'comprehension_q1': {
                'label': "1. If you vote for Game 1 and your paired participant votes for Game 2, which game is used?",
                'correct': "Game 1",
                'explanation': "When votes differ, Game 1 is selected by default."
            },
            'comprehension_q2': {
                'label': "2. If both you and your paired participant vote for Game 2, which game is used?",
                'correct': "Game 2",
                'explanation': "If both vote for Game 2, you play Game 2."
            },
            'comprehension_q3': {
                'label': "3. In Game 1, if you choose Option A and your paired participant chooses Option B, what are the points?",
                'correct': "I receive 5 points and my paired participant also receives 5 points.",
                'explanation': "In Game 1, the A–A cell yields you 5 and them also 5."
            },
            'comprehension_q4': {
                'label': "4. In Game 2, if you choose Option A and your paired participant chooses Option B, what are the points?",
                'correct': "I receive 0 points and my paired participant receives 12 points.",
                'explanation': "In Game B, the A–B cell yields you 0 and them 12."
            },
            'comprehension_q5': {
                'label': "5. In Game 1, if you choose Option B and your paired participant chooses Option B, what are the points?",
                'correct': "I receive 4 points and my paired participant receives 4 points.",
                'explanation': "In Game 1, the B-B cell yields you 4 and them also 4."
            },
        }
        questions = []
        for field, info in feedback_map.items():
            selected = getattr(self, field)
            questions.append({
                'label':       info['label'],
                'selected':    selected,
                'correct':     info['correct'],
                'explanation': info['explanation'],
            })
        # also show the games again:
        return {
            'questions':      questions,
            'matrix_A':       Constants.matrix_A,
            'matrix_B':       Constants.matrix_B,
            'C': Constants,
            'app_name': Constants.name_in_url,
            'A1aa': Constants.A1aa,
            'A1ab': Constants.A1ab,
            'A1ba': Constants.A1ba,
            'A1bb': Constants.A1bb,
            'A2aa': Constants.A2aa,
            'A2ab': Constants.A2ab,
            'A2ba': Constants.A2ba,
            'A2bb': Constants.A2bb,
        }


class AfterFeedback(Page):
    def is_displayed(self):
        return self.round_number == 1 and self.consent and not self.remove  and not self.first_attempt_passed

    def app_after_this_page(self, upcoming_apps, **kwargs):
        if self.first_attempt_passed:
            return None
        else:
            return None

# Second ComprehensionCheck
class ComprehensionCheck2(Page):
    form_model = 'player'
    form_fields = ['comprehension_q6', 'comprehension_q7', 'comprehension_q8', 'comprehension_q9', 'comprehension_q10']

    def is_displayed(self):
        return self.round_number == 1 and not self.first_attempt_passed

    def before_next_page(self, timeout_happened):
        correct_answers = {
            'comprehension_q6': 'Game 2',
            'comprehension_q7': 'Game 1',
            'comprehension_q8': 'I receive 6 points and my paired participant receives 3 points.',
            'comprehension_q9': 'I receive 3 points and my paired participant receives 3 points.',
            'comprehension_q10': 'I receive 12 points and my paired participant receives 0 points.',
        }
        wrong = []
        for field, correct in correct_answers.items():
            if getattr(self, field) != correct:
                wrong.append(field)
        self.second_wrong_questions = json.dumps(wrong)
        self.second_attempt_passed = (len(wrong) == 0)

    def vars_for_template(self):
        return {
            'C': Constants,
            'app_name': Constants.name_in_url,
            'A1aa': Constants.A1aa,
            'A1ab': Constants.A1ab,
            'A1ba': Constants.A1ba,
            'A1bb': Constants.A1bb,
            'A2aa': Constants.A2aa,
            'A2ab': Constants.A2ab,
            'A2ba': Constants.A2ba,
            'A2bb': Constants.A2bb,
        }

# PassedComprehension – a new page to inform participants that they passed.
class PassedComprehension(Page):
    def is_displayed(self):
        # Only show in round 1 after comprehension check if participant is not removed.
        return self.round_number == 1 and self.consent and not self.remove and  (self.first_attempt_passed or self.second_attempt_passed)
    def vars_for_template(self):
        return {}

    def app_after_this_page(self, upcoming_apps, **kwargs):
        return 'MainExperiment'
    # You may include additional instructions or simply a congratulatory message.


class FailedComprehension(Page):
    def is_displayed(self):
        return self.round_number == 1 and not (self.first_attempt_passed or self.second_attempt_passed)

    def app_after_this_page(self, upcoming_apps, **kwargs):
        return 'end'


class GroupAfterPassedComprehension(WaitPage):
    def after_all_players_arrive(self):
        eligible_players = [p for p in self.subsession.get_players() if
                            p.pair is None and (p.first_attempt_passed or p.second_attempt_passed)]
        pair_id = 1
        while len(eligible_players) >= 2:
            p1, p2 = eligible_players[0], eligible_players[1]
            p1.pair = pair_id
            p2.pair = pair_id
            pair_id += 1
            eligible_players = eligible_players[2:]


# Voting – main game loop page.
class Voting(BaseGamePage):
    form_model = 'player'
    form_fields = ['vote']

    def is_displayed(self):
        if self.round_number <= Constants.min_rounds:
            return self.consent and not self.remove and (self.first_attempt_passed or self.second_attempt_passed)
        else:
            return self.consent and not self.remove and not self.group.game_over and (self.first_attempt_passed or self.second_attempt_passed)

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
    form_fields = ['action']
    def is_displayed(self):
        if self.round_number <= Constants.min_rounds:
            return self.consent and not self.remove
        else:
            return self.consent and not self.remove and not self.group.game_over
    def vars_for_template(self):
        partner = self.get_others_in_group()[0]
        return {
            'player_vote': self.vote,
            'partner_vote': partner.vote,
            'current_matrix': "Matrix B" if self.group.current_game == 'B' else "Matrix A",
            'matrix_A': Constants.matrix_A,
            'matrix_B': Constants.matrix_B,   'A1aa': Constants.A1aa,
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
            return self.consent and not self.remove
        else:
            return self.consent and not self.remove and not self.group.game_over
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
    wait_for_all_groups = False
    def after_all_players_arrive(self):
        if self.round_number > Constants.min_rounds:
            if random.random() < 0.5:
                self.group.game_over = True
                for p in self.group.get_players():
                    p.participant.vars["finished_round"] = self.round_number
            else:
                self.group.game_over = False

# AdditionalMeasurements – final additional page shown on the finished round.
class AdditionalMeasurements(Page):
    form_model = 'player'
    form_fields = ['decision_1', 'decision_2', 'decision_3', 'decision_4']

    def is_displayed(self):
        finished_round = self.participant.vars.get("finished_round")
        return self.consent and not self.remove and finished_round is not None and self.round_number == finished_round


class CalculatePayoffs(WaitPage):
    def is_displayed(self):
        finished_round = self.participant.vars.get("finished_round")
        return self.consent and not self.remove and ((finished_round is not None and self.round_number == finished_round) or self.round_number == Constants.num_rounds)
    def vars_for_template(self):
        total_payoff = sum([p.payoff for p in self.in_all_rounds()]) / 25

        self.subsession.determine_special_payoffs()

# PaymentAndDebrief – final page; shows accumulated payoff and ends experiment.
class PaymentAndDebrief(Page):
    def is_displayed(self):
        finished_round = self.participant.vars.get("finished_round")
        return self.consent and not self.remove and ((finished_round is not None and self.round_number == finished_round) or self.round_number == Constants.num_rounds)
    def vars_for_template(self):
        total_payoff = sum([p.payoff for p in self.in_all_rounds()])/25

        self.subsession.determine_special_payoffs()

        return {
            'final_payment': c(total_payoff)
        }
    def before_next_page(self, timeout_happened):
        self.group.finished = True
    def app_after_this_page(self, upcoming_apps, **kwargs):
        return None


page_sequence = [
    Consent,
    NoConsent,
    Instructions,
    Instructions2,
    ComprehensionCheck,
    ComprehensionFeedback,
    AfterFeedback,
    ComprehensionCheck2,
    PassedComprehension,
    FailedComprehension,
]

