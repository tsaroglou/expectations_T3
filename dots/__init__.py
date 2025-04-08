# models.py

from otree.api import *


import random

class Constants(BaseConstants):
    name_in_url = 'dot_stimulus_experiment'
    players_per_group = None
    num_rounds = 8  # We have 8 trials

class Subsession(BaseSubsession):
    def creating_session(self):
        patterns = [
            {'left': 46, 'right': 42},  # 4 more dots on the left
            {'left': 42, 'right': 46},  # 4 more dots on the right
            {'left': 50, 'right': 42},  # 8 more dots on the left
            {'left': 42, 'right': 50},  # 8 more dots on the right
            {'left': 54, 'right': 42},  # 12 more dots on the left
            {'left': 42, 'right': 54},  # 12 more dots on the right
            {'left': 58, 'right': 42},  # 16 more dots on the left
            {'left': 42, 'right': 58},  # 16 more dots on the right
        ]

        for player in self.get_players():
            pattern = patterns[player.round_number - 1]  # Access pattern based on round_number
            player.dots_left = pattern['left']
            player.dots_right = pattern['right']
            player.correct_answer = 'left' if pattern['left'] > pattern['right'] else 'right'



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    side_identified = models.StringField(
        choices=['Left', 'Right'],
        widget=widgets.RadioSelectHorizontal
    )
    choice_decision = models.StringField(
        choices=['A', 'B'],
        widget=widgets.RadioSelectHorizontal
    )
    group_type = models.StringField()
    response_correct = models.BooleanField()
    decision = models.StringField(choices=['A', 'B'])
    side_identified = models.StringField(choices=['Left', 'Right'])

    # These fields should align with those used in creating_session
    dots_left = models.IntegerField(initial=42)  # If you use these in the session setup
    dots_right = models.IntegerField(initial=42)
    correct_answer = models.StringField()

    # Remove or rename these if they are not used or are duplicates
    dot_count_left = models.IntegerField()
    dot_count_right = models.IntegerField()

    def set_dot_counts(self):
        # Randomly generate dots count for left and right, based on experimental needs
        self.dot_count_left = random.randint(1, 50)
        self.dot_count_right = random.randint(1, 50)


class WelcomePage(Page):
    def before_next_page(self, **kwargs):
            self.group_type = 'Conflict_Left' if self.id_in_group % 2 == 0 else 'Conflict_Right'

class Instructions(Page):
    pass

class DotStimuli(Page):
    form_model = 'player'
    form_fields = ['side_identified', 'choice_decision']

    def vars_for_template(self):
        # Provide data for the template to adjust the table based on group_type
        return {
            'table_data': self.group_type
        }


class MainExperiment(Page):
    form_model = 'player'
    form_fields = ['allocation_choice']

class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['dot_identification_correct', 'understanding_questions_correct']

class Results(Page):
    pass

page_sequence = [WelcomePage, Instructions] + [DotStimuli]*Constants.num_rounds + [Questionnaire, Results]
