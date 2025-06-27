from otree.api import *
from otree.api import Currency as c
import random

doc = """
Cooperation under Agreed Risk Experiment
"""
import json

class Constants(BaseConstants):
    name_in_url = 'CY_pre'
    players_per_group = None
    num_rounds = 100    # Maximum rounds; experiment will end early once the lottery triggers.
    min_rounds = 20     # Must play at least 20 rounds before the lottery may end the game.
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


class Subsession(BaseSubsession):


    def creating_session(self):
        if self.round_number == 1:
            for player in self.get_players():
                player.group = None  # <<< MANUALLY ungroup everyone!


class Group(BaseGroup):
    game_over = models.BooleanField(initial=False)
    finished = models.BooleanField(initial=False)

class Player(BasePlayer):
    first_attempt_passed = models.BooleanField(initial=False)
    second_attempt_passed = models.BooleanField(initial=False)
    first_wrong_questions = models.LongStringField()
    second_wrong_questions = models.LongStringField()


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
    treatment = models.StringField(initial='T1a')
    remove = models.BooleanField(initial=False)
    # Comprehension check questions:

    comprehension_q3 = models.StringField(
        choices=[
            "I receive 5 points and my paired participant also receives 5 points.",
            "I receive 6 points and my paired participant receives 3 points.",
            "I receive 4 points and my paired participant also receives 4 point."
        ],
        widget=widgets.RadioSelect,
        label="1. In Game 1, if you choose Option A and your paired participant also chooses Option A, what are the points?"
    )
    comprehension_q4 = models.StringField(
        choices=[
            "I receive 7 points and my paired participant also receives 7 points.",
            "I receive 0 points and my paired participant receives 12 points.",
            "I receive 12 points and my paired participant receives 0 points."
        ],
        widget=widgets.RadioSelect,
        label="2. In Game 2, if you choose Option A and your partner chooses Option B, what are the points?"
    )
    comprehension_q5 = models.StringField(
        choices=[
            "I receive 3 points and my paired participant receives 3 points.",
            "I receive 0 points and my paired participant receives 12 points.",
            "I receive 7 points and my paired participant receives 7 point."
        ],
        widget=widgets.RadioSelect,
        label="3. In Game 2, if you both choose Option B, what are the points?"
    )

    comprehension_q8 = models.StringField(
        choices=[
            "I receive 6 points and my paired participant receives 3 points.",
            "I receive 4 points and my paired participant also receives 4 points.",
            "I receive 5 points and my paired participant also receives 5 points."
        ],
        widget=widgets.RadioSelect,
        label="4. In Game 1, if you choose Option B and your paired participant chooses Option A, what are the points?"
    )
    comprehension_q9 = models.StringField(
        choices=[
            "I receive 0 points and my paired participant receives 12 points.",
            "I receive 3 points and my paired participant receives 3 points.",
            "I receive 3 points and my paired participant receives 6 points."
        ],
        widget=widgets.RadioSelect,
        label="5. In Game 2, if both choose Option B, what are the points?"
    )
    comprehension_q10 = models.StringField(
        choices=[
            "I receive 12 points and my paired participant receives 0 points.",
            "I receive 0 points and my paired participant receives 12 points.",
            "I receive 3 points and my paired participant receives 3 points."
        ],
        widget=widgets.RadioSelect,
        label="6. In Game 2, if you choose Option B and your partner chooses Option A, what are the points?"
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
    form_fields = ['comprehension_q3', 'comprehension_q4', 'comprehension_q5']

    def is_displayed(self):
        return self.consent and not self.remove and self.round_number == 1

    def before_next_page(self, timeout_happened):
        correct_answers = {
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
            'comprehension_q3': {
                'label': "1. In Game 1, if you choose Option A and your paired participant also chooses Option A, what are the points?",
                'correct': "I receive 5 points and my paired participant also receives 5 points.",
                'explanation': "In Game 1, the A–A cell yields you 5 and them also 5."
            },
            'comprehension_q4': {
                'label': "2. In Game 2, if you choose Option A and your paired participant chooses Option B, what are the points?",
                'correct': "I receive 0 points and my paired participant receives 12 points.",
                'explanation': "In Game 2, the A–B cell yields you 0 and them 12."
            },
            'comprehension_q5': {
                'label': "3. In Game 2, if you choose Option B and your paired participant chooses Option B, what are the points?",
                'correct': "I receive 3 points and my paired participant receives 3 points.",
                'explanation': "In Game 2, the B-B cell yields you 3 and them also 3."
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
    form_fields = ['comprehension_q8', 'comprehension_q9', 'comprehension_q10']

    def is_displayed(self):
        return self.round_number == 1 and not self.first_attempt_passed

    def before_next_page(self, timeout_happened):
        correct_answers = {
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

    def before_next_page(self, timeout_happened):
        self.participant.vars['passed_comprehension'] = True

    # You may include additional instructions or simply a congratulatory message.
    def app_after_this_page(self, upcoming_apps, **kwargs):
        return 'VR_C_y_part2'


class FailedComprehension(Page):
    def is_displayed(self):
        return self.round_number == 1 and not (self.first_attempt_passed or self.second_attempt_passed)

    def before_next_page(self, timeout_happened):
        self.participant.vars['passed_comprehension'] = False

    def app_after_this_page(self, upcoming_apps, **kwargs):
        return 'end'


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

