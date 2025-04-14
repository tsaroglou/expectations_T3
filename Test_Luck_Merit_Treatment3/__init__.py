# Remove the duplicate Subsession and Group classes
# Ensure that the Subsession and Group classes are defined only once
import json
from otree.api import *
import random  # Add this line


def format_currency(value):
    return f"{value:.2f}"

doc = """
Luck Trial
"""
from time import time
import time

from otree.api import widgets


class Constants(BaseConstants):
    name_in_url = 'Test_Luck_Merit'
    players_per_group = None
    num_rounds = 1
    initial_payment = 1.5

    investment_amount = 1.0

    # Initial payment in Euros
    bonus_for_accurate_prediction = 0.5
    correct_answers = ['1', '2', '4', '1', '5', '6', '6', '8', '2', '1', '5', '6', '3', '4', '5']

    country_choices = [
('AF', 'Afghanistan'),
('AL', 'Albania'),
('DZ', 'Algeria'),
('AS', 'American Samoa'),
('AD', 'Andorra'),
('AO', 'Angola'),
('AI', 'Anguilla'),
('AQ', 'Antarctica'),
('AG', 'Antigua and Barbuda'),
('AR', 'Argentina'),
('AM', 'Armenia'),
('AW', 'Aruba'),
('AU', 'Australia'),
('AT', 'Austria'),
('AZ', 'Azerbaijan'),
('BS', 'Bahamas'),
('BH', 'Bahrain'),
('BD', 'Bangladesh'),
('BB', 'Barbados'),
('BY', 'Belarus'),
('BE', 'Belgium'),
('BZ', 'Belize'),
('BJ', 'Benin'),
('BM', 'Bermuda'),
('BT', 'Bhutan'),
('BO', 'Bolivia'),
('BA', 'Bosnia and Herzegovina'),
('BW', 'Botswana'),
('BV', 'Bouvet Island'),
('BR', 'Brazil'),
('IO', 'British Indian Ocean Territory'),
('VG', 'British Virgin Islands'),
('BN', 'Brunei'),
('BG', 'Bulgaria'),
('BF', 'Burkina Faso'),
('BI', 'Burundi'),
('KH', 'Cambodia'),
('CM', 'Cameroon'),
('CA', 'Canada'),
('CV', 'Cape Verde'),
('KY', 'Cayman Islands'),
('CF', 'Central African Republic'),
('EA', 'Ceuta and Melilla'),
('TD', 'Chad'),
('CL', 'Chile'),
('CN', 'China'),
('CX', 'Christmas Island'),
('CC', 'Cocos Islands'),
('CO', 'Colombia'),
('KM', 'Comoros'),
('CK', 'Cook Islands'),
('CR', 'Costa Rica'),
('HR', 'Croatia'),
('CU', 'Cuba'),
('CW', 'Curaçao'),
('CY', 'Cyprus'),
('CZ', 'Czech Republic'),
('CD', 'Democratic Republic of the Congo'),
('DK', 'Denmark'),
('DJ', 'Djibouti'),
('DM', 'Dominica'),
('DO', 'Dominican Republic'),
('EC', 'Ecuador'),
('EG', 'Egypt'),
('SV', 'El Salvador'),
('GQ', 'Equatorial Guinea'),
('ER', 'Eritrea'),
('EE', 'Estonia'),
('SZ', 'Eswatini'),
('ET', 'Ethiopia'),
('FK', 'Falkland Islands'),
('FO', 'Faroe Islands'),
('FJ', 'Fiji'),
('FI', 'Finland'),
('FR', 'France'),
('GF', 'French Guiana'),
('PF', 'French Polynesia'),
('TF', 'French Southern Territories'),
('GA', 'Gabon'),
('GM', 'Gambia'),
('GE', 'Georgia'),
('DE', 'Germany'),
('GH', 'Ghana'),
('GI', 'Gibraltar'),
('GR', 'Greece'),
('GL', 'Greenland'),
('GD', 'Grenada'),
('GP', 'Guadeloupe'),
('GU', 'Guam'),
('GT', 'Guatemala'),
('GG', 'Guernsey'),
('GN', 'Guinea'),
('GW', 'Guinea-Bissau'),
('GY', 'Guyana'),
('HT', 'Haiti'),
('HM', 'Heard Island and McDonald Islands'),
('HN', 'Honduras'),
('HK', 'Hong Kong'),
('HU', 'Hungary'),
('IS', 'Iceland'),
('IN', 'India'),
('ID', 'Indonesia'),
('IR', 'Iran'),
('IQ', 'Iraq'),
('IE', 'Ireland'),
('IM', 'Isle of Man'),
('IL', 'Israel'),
('IT', 'Italy'),
('JM', 'Jamaica'),
('JP', 'Japan'),
('JE', 'Jersey'),
('JO', 'Jordan'),
('KZ', 'Kazakhstan'),
('KE', 'Kenya'),
('KI', 'Kiribati'),
('XK', 'Kosovo'),
('KW', 'Kuwait'),
('KG', 'Kyrgyzstan'),
('LA', 'Laos'),
('LV', 'Latvia'),
('LB', 'Lebanon'),
('LS', 'Lesotho'),
('LR', 'Liberia'),
('LY', 'Libya'),
('LI', 'Liechtenstein'),
('LT', 'Lithuania'),
('LU', 'Luxembourg'),
('MO', 'Macau'),
('MK', 'North Macedonia'),
('MG', 'Madagascar'),
('MW', 'Malawi'),
('MY', 'Malaysia'),
('MV', 'Maldives'),
('ML', 'Mali'),
('MT', 'Malta'),
('MH', 'Marshall Islands'),
('MR', 'Mauritania'),
('MU', 'Mauritius'),
('YT', 'Mayotte'),
('MX', 'Mexico'),
('FM', 'Micronesia'),
('MD', 'Moldova'),
('MC', 'Monaco'),
('MN', 'Mongolia'),
('ME', 'Montenegro'),
('MS', 'Montserrat'),
('MA', 'Morocco'),
('MZ', 'Mozambique'),
('MM', 'Myanmar'),
('NA', 'Namibia'),
('NR', 'Nauru'),
('NP', 'Nepal'),
('NL', 'Netherlands'),
('NC', 'New Caledonia'),
('NZ', 'New Zealand'),
('NI', 'Nicaragua'),
('NE', 'Niger'),
('NG', 'Nigeria'),
('NU', 'Niue'),
('NF', 'Norfolk Island'),
('KP', 'North Korea'),
('MP', 'Northern Mariana Islands'),
('NO', 'Norway'),
('OM', 'Oman'),
('PK', 'Pakistan'),
('PW', 'Palau'),
('PS', 'Palestine'),
('PA', 'Panama'),
('PG', 'Papua New Guinea'),
('PY', 'Paraguay'),
('PE', 'Peru'),
('PH', 'Philippines'),
('PN', 'Pitcairn Islands'),
('PL', 'Poland'),
('PT', 'Portugal'),
('PR', 'Puerto Rico'),
('QA', 'Qatar'),
('CG', 'Republic of the Congo'),
('RO', 'Romania'),
('RU', 'Russia'),
('RW', 'Rwanda'),
('RE', 'Réunion'),
('BL', 'Saint Barthélemy'),
('SH', 'Saint Helena'),
('KN', 'Saint Kitts and Nevis'),
('LC', 'Saint Lucia'),
('MF', 'Saint Martin'),
('PM', 'Saint Pierre and Miquelon'),
('VC', 'Saint Vincent and the Grenadines'),
('WS', 'Samoa'),
('SM', 'San Marino'),
('ST', 'Sao Tome and Principe'),
('SA', 'Saudi Arabia'),
('SN', 'Senegal'),
('RS', 'Serbia'),
('SC', 'Seychelles'),
('SL', 'Sierra Leone'),
('SG', 'Singapore'),
('SX', 'Sint Maarten'),
('SK', 'Slovakia'),
('SI', 'Slovenia'),
('SB', 'Solomon Islands'),
('SO', 'Somalia'),
('ZA', 'South Africa'),
('GS', 'South Georgia and the South Sandwich Islands'),
('KR', 'South Korea'),
('SS', 'South Sudan'),
('ES', 'Spain'),
('LK', 'Sri Lanka'),
('SD', 'Sudan'),
('SR', 'Suriname'),
('SJ', 'Svalbard and Jan Mayen'),
('SE', 'Sweden'),
('CH', 'Switzerland'),
('SY', 'Syria'),
('TW', 'Taiwan'),
('TJ', 'Tajikistan'),
('TZ', 'Tanzania'),
('TH', 'Thailand'),
('TL', 'Timor-Leste'),
('TG', 'Togo'),
('TK', 'Tokelau'),
('TO', 'Tonga'),
('TT', 'Trinidad and Tobago'),
('TN', 'Tunisia'),
('TR', 'Turkey'),
('TM', 'Turkmenistan'),
('TC', 'Turks and Caicos Islands'),
('TV', 'Tuvalu'),
('UG', 'Uganda'),
('UA', 'Ukraine'),
('AE', 'United Arab Emirates'),
('GB', 'United Kingdom'),
('US', 'United States'),
('UM', 'United States Minor Outlying Islands'),
('VI', 'United States Virgin Islands'),
('UY', 'Uruguay'),
('UZ', 'Uzbekistan'),
('VU', 'Vanuatu'),
('VA', 'Vatican City'),
('VE', 'Venezuela'),
('VN', 'Vietnam'),
('WF', 'Wallis and Futuna'),
('EH', 'Western Sahara'),
('YE', 'Yemen'),
('ZM', 'Zambia'),
('ZW', 'Zimbabwe'),
('AX', 'Åland Islands')
]


class Subsession(BaseSubsession):
    def creating_session(self):
        for i, player in enumerate(self.get_players()):
            player.group_type = 'A' if i % 2 == 0 else 'B'


class Group(BaseGroup):
    average_tax_vote_a = models.FloatField(initial=0)
    average_tax_vote_b = models.FloatField(initial=0)
    total_withholdings_a = models.FloatField(initial=0)
    total_withholdings_b = models.FloatField(initial=0)
    benefit_a = models.FloatField(initial=0)
    benefit_b = models.FloatField(initial=0)

    # Fields to store total deductions for each group
    total_deducted_a = models.FloatField(initial=0)
    total_deducted_b = models.FloatField(initial=0)

    # Fields to store benefits for each group
    benefit_a = models.FloatField(initial=0)
    benefit_b = models.FloatField(initial=0)



class Player(BasePlayer):
    country = models.StringField(
        choices=Constants.country_choices,
        label="Which country are you from?",
    )

    timeout_count = models.IntegerField(initial=0)

    finished = models.BooleanField(initial=False)
    major = models.StringField(
        choices=[
            'Not a student', 'Computer Science', 'Economics', 'Business', 'Psychology',
            'Engineering', 'Biology', 'Mathematics', 'Physics',
            'Philosophy', 'Political Science', 'Art', 'History',
            'Sociology', 'Law', 'Medicine', 'Education',
            'English Literature', 'Environmental Science', 'Chemistry',
            'Architecture', 'Anthropology', 'Geography', 'Linguistics',
            'Music', 'Theatre', 'Nursing', 'Public Health', 'Marketing',
            'Finance', 'Accounting', 'Communication Studies', 'Journalism',
            'Criminal Justice', 'International Relations', 'Agricultural Science',
            'Veterinary Science', 'Computer Engineering', 'Mechanical Engineering',
            'Civil Engineering', 'Electrical Engineering', 'Data Science',
            'Information Technology', 'Environmental Engineering', 'Design',
            'Graphic Design', 'Industrial Engineering', 'Urban Planning',
            'Other'
        ],
    )


    # Second tax rate voting field
    adjustment_values = models.StringField()
    bonus_gini = models.CurrencyField(initial=0)
    gini_test_score1 = models.FloatField()

    tax_rate_vote_2 = models.FloatField()
    original_gini_opposite_group = models.FloatField()
    new_gini_opposite_group = models.FloatField()

    adjustment_value = models.FloatField(initial=0)

    pay_ravens = models.FloatField()
    pay_ravens_first_show = models.CurrencyField()

    pay_ravens_original = models.FloatField()
    pay_ravens_showed = models.CurrencyField()
    bonus_guess_showed = models.CurrencyField()



    prediction_initial = models.IntegerField(min=0, max=15)
    prediction_final = models.IntegerField(min=0, max=15)
    prediction_initial_pct = models.FloatField()
    prediction_final_pct = models.FloatField()
    investment = models.CurrencyField(
        min=0,
        max=Constants.investment_amount,
        doc="""The amount the participant decides to invest""",
    )
    investment_outcome = models.CurrencyField(initial=0)
    is_investment_chosen = models.BooleanField(initial=False)
    bonus_player = models.BooleanField(initial=False)
    prediction_lottery_outcome = models.CurrencyField(initial=0)
    is_prediction_lottery_winner = models.BooleanField(initial=False)
    true_performance_estimate_pct = models.FloatField()
    is_investment_lottery_winner = models.BooleanField(initial=False)
    investment_lottery_winnings = models.CurrencyField(initial=0)
    performance_guess_correct = models.BooleanField(initial=False)

    age = models.IntegerField(label="What is your age?", min=18, max=99)
    gender = models.StringField(
        choices=['Male', 'Female', 'Other'],
        widget=widgets.RadioSelect,
        label="What is your gender?"
    )
    student = models.StringField(
        choices=['Yes undergraduate.', 'Yes graduate.', 'No.'],
        widget=widgets.RadioSelect,
        label="Are you a student?"
    )
    employed = models.StringField(
        choices=['Yes.', 'No.', 'Part-time.'],
        widget=widgets.RadioSelect,
        label="Are you employed?"
    )
    skill = models.IntegerField(
        label="The performance of myself and other participants in this experiment was a result of skill.",
        min=-10,
        max=10
    )
    luck = models.IntegerField(
        label="The performance of myself and other participants in this experiment was a result of luck.",
        min=-10,
        max=10
    )

    help_luck = models.IntegerField(
        label="In life, we should tax successful people to help unsuccessful if people's success only depends on luck.",
        min=-10,
        max=10
    )

    help_noskill = models.IntegerField(
        label="In life, we should tax successful people to help unsuccessful even if people's success only depends on skill.",
        min=-10,
        max=10
    )

    help_noeffort = models.IntegerField(
        label="In life, we should tax successful people to help unsuccessful even if people's success only depends on effort.",
        min=-10,
        max=10
    )


    hard_work = models.IntegerField(
        label="In life, hard work plays a significant role in people's economic success.",
        min=-10,
        max=10
    )

    luck_role = models.IntegerField(
        label="In life, luck plays a significant role in people's economic success.",
        min=-10,
        max=10
    )

    skill_role = models.IntegerField(
        label="In life, talent and skill play a significant role in people's economic success.",
        min=-10,
        max=10
    )

    inequality = models.IntegerField(
        label="Inequality in society should be reduced by income and/or wealth redistribution.",
        min=-10,
        max=10
    )
    political_ideology = models.IntegerField(
        label="Where would you position yourself on the political ideology spectrum?",
        min=-10,
        max=10
    )

    question1 = models.StringField(
        choices=['1.8 Euro', '1.6 Euro', '3 Euro', 'A random number between 0 and 1 Euro'],
        widget=widgets.RadioSelect
    )
    question2 = models.StringField(
        choices=['1.8 Euro', '2.8 Euro', '3 Euro', 'A random number between 0 and 1 Euro'],
        widget=widgets.RadioSelect
    )
    question3 = models.StringField(
        choices=['2.4 Euro', '0 Euro', '3 Euro', 'A random number between 0 and 1 Euro'],
        widget=widgets.RadioSelect
    )

    question4 = models.StringField(
        choices=['1 point.', '0 points.', '2 points.', '1 point with a 70% probability.',
                 '0 points with a 55% probability.'],
        widget=widgets.RadioSelect
    )
    question5 = models.StringField(
        choices=['0 points.', '0 points.', '2 points.', '1 point with a 70% probability.',
                 '0 points with a 25% probability.'],
        widget=widgets.RadioSelect
    )

    question6 = models.StringField(
        choices=['Participant A.', 'Participant B.', 'They will score the same points.',
                 'It could be either Participant A or B.'],
        widget=widgets.RadioSelect
    )

    def question1_correct(self):
        return self.question1 == '0.8 Euro'

    def question2_correct(self):
        return self.question2 == 'A random number between 0 and 0.5 Euro'

    def question3_correct(self):
        return self.question3 == '1.2 Euro'

    def question4_correct(self):
        return self.question4 == '1 point with a 70% probability.'

    def question5_correct(self):
        return self.question5 == '0 points.'

    def question6_correct(self):
        return self.question5 == 'It could be either Participant A or B.'

    tax_vote = models.FloatField()
    test_completion_time = models.FloatField()
    rank = models.IntegerField()
    tax_deduction = models.FloatField()
    applied_tax = models.FloatField()
    deduction_personal = models.FloatField()
    pay_ravens = models.FloatField()
    pay_ravens_original = models.FloatField()
    percentage_ranking_100 = models.FloatField()

    def get_rank_bin(self):
        if self.percentage_ranking < 0.20:
            return '80_100'
        elif self.percentage_ranking < 0.40:
            return '60_79'
        elif self.percentage_ranking < 0.60:
            return '40_59'
        elif self.percentage_ranking < 0.80:
            return '20_39'
        else:
            return '0_19'

    def set_applied_tax_and_deduction(self):
        rank_bin = self.get_rank_bin()  # Ensure this method exists

        if self.group_type == 'A':
            applied_tax_rate = getattr(self.group, f'average_tax_rate_b_{rank_bin}', 0)
        else:
            applied_tax_rate = getattr(self.group, f'average_tax_rate_a_{rank_bin}', 0)

        # Calculate deduction based on the applied tax rate
        deduction = (self.final_payment-1) * (applied_tax_rate / 100)

        # Update player's final payment and record the personal deduction
        self.final_payment -= deduction
        self.deduction_personal = deduction
        self.applied_tax = applied_tax_rate  # Store the applied tax rate

    percentage_ranking = models.FloatField()
    group_type = models.StringField()
    color = models.StringField()
    participant_color = models.StringField()
    consent = models.BooleanField()
    remove = models.BooleanField(initial=False)  # New field to track removal

    bin_index = models.StringField()
    test_score1_raw = models.IntegerField(min=0, max=15)
    test_score1 = models.FloatField()
    test_score2 = models.FloatField()
    test_score2_decimal = models.FloatField()
    score2 = models.IntegerField()
    tax_rate_vote = models.FloatField()
    true_performance_estimate = models.IntegerField(min=0, max=15)
    demographic_questions = models.LongStringField()
    fairness_assessment = models.LongStringField()
    final_payment = models.FloatField()
    initial_payment = models.FloatField()
    bonus_earned = models.FloatField(initial=0)

    # Questions for Raven's Test
    q1 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6], blank=True)
    q2 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6], blank=True)
    q3 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q4 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q5 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q6 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q7 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q8 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q9 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q10 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q11 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q12 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q13 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q14 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q15 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)



class EnterExperiment(Page):
    def before_next_page(player, timeout_happened):
        player.participant.vars['has_entered'] = True


class WaitingRoom(Page):
    timeout_seconds = None  # Max waiting time (10 minutes)

    def is_displayed(player):
        # The page is displayed if there are fewer than 20 participants
        return len(get_entered_participants(player)) <20

    def vars_for_template(player):
        # Provide the number of participants who have entered the experiment
        entered_count = len(get_entered_participants(player))
        return {
            'entered_count': entered_count,
        }

    def before_next_page(player, timeout_happened):
        # This logic moves players forward only if there are 20 participants
        entered_participants = get_entered_participants(player)
        if len(entered_participants) >= 20:
            player._is_ready_to_proceed = True  # Mark player as ready to proceed

def get_entered_participants(player):
    # Return participants who have clicked the button to enter the experiment
    entered_participants = [
        p for p in player.session.get_participants()
        if p.vars.get('has_entered')
    ]
    return entered_participants

# Pages
class Introduction(Page):
    timeout_seconds = 100

    form_model = 'player'
    form_fields = ['consent']

    def before_next_page(player, timeout_happened):
        # Assign group type based on even/odd id_in_subsession
        player.group_type = 'A' if player.id_in_subsession % 2 == 0 else 'B'

        # Check if the player gave consent
        if not player.consent:
            player.remove = True  # Mark player for removal if they didn't give consent

class Instructions(Page):
    timeout_seconds = 30  # Total time for the page

    def is_displayed(player):
        return player.consent and not player.remove

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            # Increment the timeout count stored in participant.vars
            player.timeout_count += 1


class SplitExplanation(Page):
    timeout_seconds = 35  # Total time for the page (3 minutes)

    def is_displayed(player):
        return player.consent and not player.remove

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            # Increment the timeout count stored in participant.vars
            player.timeout_count += 1




class SampleQuestions(Page):
    timeout_seconds = 50

    def is_displayed(player):
        return player.consent and not player.remove

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            # Increment the timeout count stored in participant.vars
            player.timeout_count += 1




class PredictionExplanation(Page):
    timeout_seconds = 90


    form_model = 'player'
    form_fields = ['question1', 'question2', 'question3']

    def is_displayed(self):
        return self.consent and not self.remove

    def before_next_page(self, timeout_happened, **kwargs):

        self.question1_correct = self.question1 == '0.8 Euro'
        self.question2_correct = self.question2 == 'A random number between 0 and 0.5 Euro'
        self.question3_correct = self.question3 == '1.2 Euro'


class InitialPrediction(Page):
    timeout_seconds = 20000
    def is_displayed(player):
        return player.consent and not player.remove
    form_model = 'player'
    form_fields = ['prediction_initial']

    def before_next_page(player: Player, timeout_happened):
        player.prediction_initial_pct = (player.prediction_initial / 15) * 100

        if timeout_happened:
            # Increment the timeout count stored in participant.vars
            player.timeout_count += 1




class GradingExplanation(Page):
    timeout_seconds = 80
    form_model = 'player'
    form_fields = ['question4', 'question5', 'question6']

    def is_displayed(self):
        return self.consent and not self.remove

    def before_next_page(self, timeout_happened, **kwargs):
        self.question4_correct = self.question4 == '1 point with a 70% probability.'
        self.question5_correct = self.question5 == '0 points.'
        self.question6_correct = self.question6 == 'It could be either Participant A or B.'




class FinalPrediction(Page):
    timeout_seconds = 100

    def is_displayed(player):
        return player.consent and not player.remove
    form_model = 'player'
    form_fields = ['prediction_final', 'prediction_initial']

    def before_next_page(player: Player, timeout_happened):
        player.prediction_final_pct = (player.prediction_final / 15) * 100
        player.prediction_initial_pct = (player.prediction_initial / 15) * 100

        if timeout_happened:
            # Increment the timeout count stored in participant.vars
            player.remove = True  # Mark player for removal


class FlashImagePage(Page):
    def get_timeout_seconds(self, **kwargs):
        # Determine the timeout based on the state
        state = self.participant.vars.get('state', 0)
        if state in [0, 2]:  # First and second cross
            return 2
        elif state == 1:  # Image display
            return 0.25

    def before_next_page(self, **kwargs):
        # Update the state to move to the next part of the sequence
        current_state = self.participant.vars.get('state', 0)
        new_state = (current_state + 1) % 3  # Cycle through the states 0, 1, 2
        self.participant.vars['state'] = new_state

    def vars_for_template(self, **kwargs):
        state = self.participant.vars.get('state', 0)
        return {
            'display_cross': state in [0, 2],  # Show cross on states 0 and 2
            'image_path': '_static/Test_Luck_Merit/Images/blue_human.png' if state == 1 else None
        }

class PaymentExplanation(Page):
    timeout_seconds = 50  # Total time for the page (3 minutes)

    def is_displayed(player):
        return player.consent and not player.remove

    def vars_for_template(player: Player):
        countdown_start_time = 60  # Countdown appears in the last 60 seconds
        return {'countdown_start_time': countdown_start_time}

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            # Increment the timeout count stored in participant.vars
            player.timeout_count += 1

            # If the participant times out 3 times, mark them for exclusion


class RavensTest(Page):
    def is_displayed(player):
        return player.consent and not player.remove
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11', 'q12', 'q13', 'q14', 'q15']
    timeout_seconds = 240

    def vars_for_template(self, **kwargs):
        # Set the start time at the beginning of the page
        self.participant.vars.setdefault('test_start_time', time.time())
        return {}

    def before_next_page(player: Player, **kwargs):
        # Manually create the list of player responses
        player_responses = [
            player.field_maybe_none('q1'),
            player.field_maybe_none('q2'),
            player.field_maybe_none('q3'),
            player.field_maybe_none('q4'),
            player.field_maybe_none('q5'),
            player.field_maybe_none('q6'),
            player.field_maybe_none('q7'),
            player.field_maybe_none('q8'),
            player.field_maybe_none('q9'),
            player.field_maybe_none('q10'),
            player.field_maybe_none('q11'),
            player.field_maybe_none('q12'),
            player.field_maybe_none('q13'),
            player.field_maybe_none('q14'),
            player.field_maybe_none('q15')
        ]

        correct_answers = Constants.correct_answers

        # Calculate test_score1
        score1 = sum(1 for player_answer, correct_answer in zip(player_responses, correct_answers) if
                     player_answer == int(correct_answer))
        player.test_score1_raw = int(score1)
        player.test_score1 = (score1 / len(correct_answers)) * 100

        # Second score calculation with lottery
        score2 = 0
        for player_answer, correct_answer in zip(player_responses, correct_answers):
            if player_answer == int(correct_answer):
                # Correct answer, run lottery with 70% chance of getting a point
                score2 += random.choices([1, 0], weights=[70, 30], k=1)[0]
            else:
                # Incorrect answer, no point
                score2 += 0

        player.test_score2 = (score2 / len(correct_answers)) * 100
        player.score2 = score2

        # Calculate the elapsed time
        start_time = player.participant.vars.get('test_start_time', time.time())
        elapsed_time = time.time() - start_time

        # Check if the page transition was due to a timeout using kwargs
        if 'timeout_happened' in kwargs and kwargs['timeout_happened']:
            player.test_completion_time = 240
        else:
            player.test_completion_time = min(elapsed_time, 240)


class ResultsWaitPage(WaitPage):
    def is_displayed(player):
        return player.consent and not player.remove

    @staticmethod
    def after_all_players_arrive(group: Group):
        players = group.subsession.get_players()

        # Define the number of bins and initialize histogram counts
        num_bins = 20  # Assuming 20 bins for scores 0-100
        all_histogram = [0] * num_bins  # Initialize histogram counts to 0

        for player in players:
            if not player.remove:
                score = player.field_maybe_none('test_score2')  # Safely access test_score2
                if score is None:
                    continue  # Skip players with None as test_score2

                # Calculate bin index based on score
                bin_index = int(min(score // 5, num_bins - 1))
                all_histogram[bin_index] += 1

        # Store the histogram data for use in templates
        group.subsession.session.vars['all_histogram'] = all_histogram


# To address the crashing issue in the TestOutcomeWaiting page, here are possible changes:

class TestOutcomeWaiting(WaitPage):
    def is_displayed(player):
        return player.consent and not player.remove

    @staticmethod
    def after_all_players_arrive(group: Group):
        # Filter out players who are removed or have None as test_score2
        active_players = [p for p in group.get_players() if not p.remove and p.test_score2 is not None]

        if not active_players:
            # Handle case where no players are eligible
            return

        # Sort active players by test_score2 in descending order
        sorted_players = sorted(active_players, key=lambda p: p.test_score2, reverse=True)
        total_players = len(sorted_players)

        last_score = None
        last_rank = 0
        skip_rank = 0

        for player in sorted_players:
            if player.test_score2 != last_score:
                last_score = player.test_score2
                last_rank += 1 + skip_rank  # Increment rank with skipped ranks
                skip_rank = 0
            else:
                skip_rank += 1  # Prepare to skip next rank

            player.rank = last_rank
            player.percentage_ranking = player.rank / total_players
            player.pay_ravens = ((player.test_score2) * 2.5) / 100
            player.pay_ravens_original = player.pay_ravens
            player.percentage_ranking_100 = round(100 - player.percentage_ranking * 100, 2)


class SelectOneForPredictionLottery(WaitPage):
    def is_displayed(player):
        return player.consent and not player.remove

    wait_for_all_groups = True

    def after_all_players_arrive(subsession: Subsession):
        # Filter out players who have been removed
        active_players = [p for p in subsession.get_players() if not p.remove]

        if not active_players:
            # Handle the case where no active players are left
            return

        chosen_player = random.choice(active_players)
        chosen_player.is_prediction_lottery_winner = True

        # Split randomly between two conditions with 50% chance each
        if random.random() < 0.5:
            if chosen_player.field_maybe_none('prediction_initial_pct') is not None and chosen_player.field_maybe_none('test_score1') is not None and chosen_player.test_score1 >= chosen_player.prediction_initial_pct:
                chosen_player.prediction_lottery_outcome = (chosen_player.prediction_initial / 15) * 3
            else:
                chosen_player.prediction_lottery_outcome = random.uniform(0, 0.5)
        else:
            if chosen_player.field_maybe_none('prediction_final_pct') is not None and chosen_player.field_maybe_none('test_score2') is not None and chosen_player.test_score2 >= chosen_player.prediction_final_pct:
                chosen_player.prediction_lottery_outcome = (chosen_player.prediction_final / 15) * 3
            else:
                chosen_player.prediction_lottery_outcome = random.uniform(0, 0.5)

        chosen_player.payoff += chosen_player.prediction_lottery_outcome



class TestOutcome(Page):
    timeout_seconds = 15
    def is_displayed(player):
        return player.consent and not player.remove
    def vars_for_template(player: Player):
        player.pay_ravens_first_show = cu(player.pay_ravens)
        player.test_score2 = round(float(player.test_score2), 2)

        # Calculate test outcome and payment based on grading structure
        return {'pay_ravens': player.pay_ravens_first_show, 'percentage_ranking_100': player.percentage_ranking_100, 'score2' : player.score2, 'test_score2': player.test_score2, 'pecentage_ranking': player.percentage_ranking}

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            # Increment the timeout count stored in participant.vars
            player.timeout_count += 1

            # If the participant times out 3 times, mark them for exclusion

class PerformanceHistogram(Page):
    timeout_seconds = 30

    def is_displayed(player):
        return player.consent and not player.remove

    def vars_for_template(player):
        current_player = player
        player.percentage_ranking_100 = round(100 - player.percentage_ranking * 100, 2)

        # Get only the players who have a valid test_score2 (not None)
        players = sorted([p for p in player.group.get_players() if p.field_maybe_none('test_score2') is not None],
                         key=lambda p: p.test_score2)

        # Proceed with valid players only
        test_scores = [p.test_score2 for p in players]
        scores2 = [p.score2 for p in players]
        id_in_group_list = [p.id_in_group for p in players]

        # Set player colors based on ranking
        for player in players:
            if player.percentage_ranking < 0.20:
                player.color = 'red_human.png'
            elif player.percentage_ranking < 0.40:
                player.color = 'yellow_human.png'
            elif player.percentage_ranking < 0.60:
                player.color = 'green_human.png'
            elif player.percentage_ranking < 0.80:
                player.color = 'orange_human.png'
            else:
                player.color = 'blue_human.png'

        player_colors = [f"/static/Test_Luck_Merit/Images/{p.color}" for p in players]

        # Calculate bar heights and format scores as percentages
        bar_heights = [score * 5 +25 for score in test_scores]
        formatted_scores = [int(score) for score in scores2]
        rankings = [f"{(1 - p.percentage_ranking) * 100:.2f}%" for p in players]
        money_earned = [f"€{(score / 100) * 2.5:.2f}" for score in test_scores]

        # Zip scores, colors, bar heights, rankings, money earned, and id_in_group together
        scores_and_colors = list(zip(formatted_scores, player_colors, bar_heights, rankings, money_earned, id_in_group_list))

        return {
            'scores_and_colors': scores_and_colors,
            'percentage_ranking_100': current_player.percentage_ranking_100,
            'participant_color': current_player.field_maybe_none('color') or 'default_icon.png',
            'specific_participant_id_in_group': current_player.id_in_group,
            'bin_index': player.get_rank_bin(),
            'all_histogram': [],  # Provide a default value for all_histogram
            'bins_labels': [str(i) for i in range(len(players))],  # Use indices as dummy labels
            'scores2': scores2
        }
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            # Increment the timeout count stored in participant.vars
            player.timeout_count += 1



class InteractiveGraph(Page):
    timeout_seconds = 110
    form_model = 'player'
    form_fields = ['tax_vote']

    def is_displayed(player):
        return player.consent and not player.remove

    def vars_for_template(player):
        current_player = player
        player_group_type = current_player.group_type
        player.percentage_ranking_100 = 100 - current_player.percentage_ranking * 100

        # Get players from the opposite group and filter out players with None in score2
        players = sorted(
            [p for p in player.group.get_players() if p.group_type != player_group_type and p.field_maybe_none('score2') is not None],
            key=lambda p: p.score2
        )

        # Now you are dealing with players who have a valid score2
        scores2 = [p.score2 for p in players]  # Raw scores to be used for bar heights and display
        id_in_group_list = [p.id_in_group for p in players]

        # Set player colors based on ranking
        for player in players:
            if player.percentage_ranking < 0.20:
                player.color = 'red_human.png'
            elif player.percentage_ranking < 0.40:
                player.color = 'yellow_human.png'
            elif player.percentage_ranking < 0.60:
                player.color = 'green_human.png'
            elif player.percentage_ranking < 0.80:
                player.color = 'orange_human.png'
            else:
                player.color = 'blue_human.png'

        player_colors = [f"/static/Test_Luck_Merit/Images/{p.color}" for p in players]

        # Calculate bar heights based on score2 (proportional to raw score)
        bar_heights = [score * 20 + 5 for score in scores2]  # Heights calculated based on score2
        rankings = [f"{(1 - p.percentage_ranking) * 100:.2f}%" for p in players]
        money_earned = [f"€{(score / 15) * 2.5:.2f}" for score in scores2]

        # Pass scores2 instead of percentage scores
        scores_and_colors = zip(scores2, player_colors, bar_heights, rankings, money_earned, id_in_group_list)

        return {
            'scores_and_colors': list(scores_and_colors),  # Convert zip to list
            'percentage_ranking_100': current_player.percentage_ranking_100,
            'participant_color': current_player.field_maybe_none('color') or 'default_icon.png',
            'specific_participant_id_in_group': current_player.id_in_group,
            'bin_index': player.get_rank_bin(),
            'all_histogram': [],  # Provide a default value for all_histogram
            'bins_labels': [str(i) for i in range(len(players))]  # Use indices as dummy labels
        }
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            # Increment the timeout count stored in participant.vars
            player.remove = True  # Mark player for removal



def get_item(dictionary, key):
    return dictionary.get(key)

class TaxRateVoting(Page):
    timeout_seconds = 1800000
    def is_displayed(self):
        return self.consent and not self.remove

    form_model = 'player'

    form_fields = ['tax_rate_vote_0_19', 'tax_rate_vote_20_39', 'tax_rate_vote_40_59', 'tax_rate_vote_60_79',
                   'tax_rate_vote_80_100']

    def vars_for_template(player):
        current_player = player
        player.percentage_ranking_100 = 100 - current_player.percentage_ranking * 100
        all_histogram = player.session.vars.get('all_histogram', [])
        # Update bin labels to reflect bins of width 5
        bins_labels = [f"{i}-{i + 4}" for i in range(0, 95, 5)]
        # Add the last bin label for 95-100
        bins_labels.append("95-100")
        rank = player.field_maybe_none('rank')  # Access the player's rank

        players = sorted(player.group.get_players(), key=lambda p: p.percentage_ranking, reverse=True)
        player_colors = []
        id_in_group_list = []

        for player in players:
            if player.percentage_ranking < 0.20:
                player.color = 'red_human.png'
            elif player.percentage_ranking < 0.40:
                player.color = 'yellow_human.png'
            elif player.percentage_ranking < 0.60:
                player.color = 'green_human.png'
            elif player.percentage_ranking < 0.80:
                player.color = 'orange_human.png'
            else:
                player.color = 'blue_human.png'

            player_colors.append(player.color)
            id_in_group_list = [p.id_in_group for p in player.group.get_players()]
            sorted_id_in_group_list = [player.id_in_group for player in players]
            sorted_role_participant = [player.group_type for player in players]

            player.bin_index = player.get_rank_bin()
            test_scores = [p.test_score2 for p in players]

        specific_participant_id_in_group = current_player.id_in_group
        specific_participant_group_type = current_player.group_type

        ranking_bins = ['0-19%', '20-39%', '40-59%', '60-79%', '80-100%']
        fields_and_bins = zip(TaxRateVoting.form_fields, ranking_bins)
        return {
            'fields_and_bins': fields_and_bins,
            'all_histogram': all_histogram,
            'group_type_list': sorted_role_participant,
            'bins_labels': bins_labels,
            'id_in_group_list': sorted_id_in_group_list,
            'test_scores': test_scores,
            'percentage_ranking_100': current_player.percentage_ranking_100,
            'player_colors': player_colors,
            'participant_color': current_player.color,
            'specific_participant_group_type': specific_participant_group_type,
            'specific_participant_id_in_group': specific_participant_id_in_group,
            'bin_index': player.get_rank_bin(),
        }

    def get_form_fields(player):
        return ['tax_rate_vote_0_19', 'tax_rate_vote_20_39', 'tax_rate_vote_40_59', 'tax_rate_vote_60_79',
                'tax_rate_vote_80_100']

    def get_form_widgets(player):
        return {
            'tax_rate_vote_0_19': widgets.SliderInput(attrs={'min': 0, 'max': 100, 'step': 1}),
            'tax_rate_vote_20_39': widgets.SliderInput(attrs={'min': 0, 'max': 100, 'step': 1}),
            'tax_rate_vote_40_59': widgets.SliderInput(attrs={'min': 0, 'max': 100, 'step': 1}),
            'tax_rate_vote_60_79': widgets.SliderInput(attrs={'min': 0, 'max': 100, 'step': 1}),
            'tax_rate_vote_80_100': widgets.SliderInput(attrs={'min': 0, 'max': 100, 'step': 1}),
        }

    def before_next_page(player, timeout_happened):
        if timeout_happened:
            # Increment the timeout count stored in participant.vars
            player.timeout_count += 1


from collections import defaultdict

class TaxRateProcessing(WaitPage):
    def is_displayed(player):
        return player.consent and not player.remove

    def after_all_players_arrive(self):
        self.calculate_average_tax_rates()
        self.aggregate_deductions()
        self.calculate_benefits()
        self.distribute_benefits_to_players()

    def calculate_average_tax_rates(self):
        group = self.group
        players = group.get_players()

        # Initialize total votes and player counts
        total_tax_vote_a = 0
        total_tax_vote_b = 0
        count_a = 0
        count_b = 0

        # Sum votes and count players in each group, skipping players with None for tax_vote
        for player in players:
            if player.group_type == 'A' and player.field_maybe_none('tax_vote') is not None:
                total_tax_vote_a += player.tax_vote
                count_a += 1
            elif player.group_type == 'B' and player.field_maybe_none('tax_vote') is not None:
                total_tax_vote_b += player.tax_vote
                count_b += 1

        # Calculate and store average votes for each group
        average_tax_vote_a = total_tax_vote_a / count_a if count_a > 0 else 0
        average_tax_vote_b = total_tax_vote_b / count_b if count_b > 0 else 0

        group.average_tax_vote_a = average_tax_vote_a
        group.average_tax_vote_b = average_tax_vote_b

    def aggregate_deductions(self):
        group = self.group
        players = [p for p in group.get_players() if not p.remove]  # Exclude removed players

        # Initialize withholding variables
        total_withholdings_a = 0
        total_withholdings_b = 0

        # Deduct average tax voted by one group from the other group
        for player in players:
            if player.pay_ravens is None:
                player.pay_ravens = 0  # Default to 0 if pay_ravens is None

            if player.group_type == 'A':
                deduction = player.pay_ravens * (group.average_tax_vote_b / 100)
                player.pay_ravens -= deduction
                total_withholdings_b += deduction
            elif player.group_type == 'B':
                deduction = player.pay_ravens * (group.average_tax_vote_a / 100)
                player.pay_ravens -= deduction
                total_withholdings_a += deduction

        group.total_withholdings_a = total_withholdings_a
        group.total_withholdings_b = total_withholdings_b

    def calculate_benefits(self):
        group = self.group
        players = [p for p in group.get_players() if not p.remove]  # Exclude removed players

        # Count the number of participants in each group
        count_a = sum(1 for p in players if p.group_type == 'A')
        count_b = sum(1 for p in players if p.group_type == 'B')

        # Calculate the benefit per participant for each group
        benefit_a = group.total_withholdings_b / count_a if count_a > 0 else 0
        benefit_b = group.total_withholdings_a / count_b if count_b > 0 else 0

        group.benefit_a = benefit_a
        group.benefit_b = benefit_b

    def distribute_benefits_to_players(self):
        group = self.group
        players = [p for p in group.get_players() if not p.remove]  # Exclude removed players

        # Add benefits to each player's payment
        for player in players:
            if player.pay_ravens is None:
                player.pay_ravens = 0  # Default to 0 if pay_ravens is None

            if player.group_type == 'A':
                player.pay_ravens += group.benefit_a
            elif player.group_type == 'B':
                player.pay_ravens += group.benefit_b


class PerformanceEstimation(Page):
    timeout_seconds = 50
    def is_displayed(player):
        return player.consent and not player.remove
    form_model = 'player'
    form_fields = ['true_performance_estimate']

    def before_next_page(player: Player, timeout_happened):
        player.payoff += player.pay_ravens + Constants.initial_payment
        player.true_performance_estimate_pct = (player.true_performance_estimate / 15) * 100




def generate_predefined_distribution(num_bars):
    initial_score = 50
    scores = [initial_score] * num_bars
    predefined_distribution = [{'score': score, 'money': (score / 100) * 2.5, 'money_height': (score / 100) * 100} for score in scores]
    return predefined_distribution


class SecondTaxRateVoting(Page):
    form_model = 'player'
    form_fields = ['adjustment_values']
    timeout_seconds = 80

    def is_displayed(player):
        return player.consent and not player.remove

    def vars_for_template(player: Player):
        current_player = player
        player_group_type = current_player.group_type

        # Get the players from the opposite group and filter out players with None test_score2
        opposite_group_players = sorted(
            [p for p in player.group.get_players() if
             p.group_type != player_group_type and p.field_maybe_none('test_score2') is not None],
            key=lambda p: p.field_maybe_none('test_score2')
        )

        num_bars = len(opposite_group_players)

        num_participants = 20

        # Store original ravens pay for opposite group
        original_ravens_pays = [p.pay_ravens_original for p in opposite_group_players]
        original_gini_opposite_group = calculate_gini(original_ravens_pays)

        # Calculate Gini based on test_score1
        test_score1_values = [p.test_score1 for p in opposite_group_players]
        gini_test_score1 = calculate_gini(test_score1_values)

        # Create the distribution using score2 (raw scores from 0 to 15)
        scores_and_colors = list(zip(
            [p.score2 for p in opposite_group_players],  # Use raw score2 values
            [f"/static/Test_Luck_Merit/Images/{p.color}" for p in opposite_group_players],
            [p.score2 * 25 + 3 for p in opposite_group_players],  # Adjust bar height for score2
            [f"€{(p.score2 / 15) * 2.5:.2f}" for p in opposite_group_players],  # Earnings based on score2
            [p.id_in_group for p in opposite_group_players]
        ))

        # Create the predefined distribution for the interactive graph (using integers from 0 to 15)
        predefined_distribution = [{'score': 8, 'money': f"€{8 / 15 * 2.5:.2f}", 'money_height': 8 * 25 + 3} for _ in range(num_bars)]

        # First distribution (fairly even)
        income_values_1 = [3, 4, 5, 6, 6, 7, 7, 8, 8, 9, 10, 11, 12, 12, 13, 13, 13, 14, 14, 15]
        income_values_1 = sorted(income_values_1)

        # Second distribution (more skewed towards lower values)
        income_values_2 = [1, 2, 2, 3, 3, 4, 4, 6, 6, 6, 7, 9, 10, 12, 12, 13, 14, 14, 15, 15]
        income_values_2 = sorted(income_values_2)

        point_distribution_example = []
        raw_distribution_example = []

        # First example (Point Score Distribution)
        for i, income in enumerate(income_values_1):
            percentile_rank = (i + 1) / num_participants
            if percentile_rank < 0.20:
                color = 'red_human.png'
            elif percentile_rank < 0.40:
                color = 'yellow_human.png'
            elif percentile_rank < 0.60:
                color = 'green_human.png'
            elif percentile_rank < 0.80:
                color = 'orange_human.png'
            else:
                color = 'blue_human.png'

            height = income * 25 + 3
            earnings = income / 15 * 2.5

            point_distribution_example.append({
                "score": income,
                "height": height,
                "money": f"€{earnings:.2f}",
                "icon": f"/static/Test_Luck_Merit/Images/{color}"
            })

        # Second example (Raw Score Distribution)
        for i, income in enumerate(income_values_2):
            percentile_rank = (i + 1) / num_participants
            if percentile_rank < 0.20:
                color = 'red_human.png'
            elif percentile_rank < 0.40:
                color = 'yellow_human.png'
            elif percentile_rank < 0.60:
                color = 'green_human.png'
            elif percentile_rank < 0.80:
                color = 'orange_human.png'
            else:
                color = 'blue_human.png'

            height = income * 25 + 3
            earnings = income / 15 * 2.5

            raw_distribution_example.append({
                "score": income,
                "height": height,
                "money": f"€{earnings:.2f}",
                "icon": f"/static/Test_Luck_Merit/Images/{color}"
            })

        ### NEW EXAMPLES (Sketch 1 and Sketch 2)

        # Sketch 1 (slightly uneven distribution)
        sketch1_income_values = [6, 6, 7, 7, 7, 7, 8, 8, 9, 9, 10, 10, 10, 11, 11, 12, 12, 12, 12, 13]
        sketch1_distribution = []
        for i, income in enumerate(sketch1_income_values):
            percentile_rank = (i + 1) / num_participants
            if percentile_rank < 0.20:
                color = 'red_human.png'
            elif percentile_rank < 0.40:
                color = 'yellow_human.png'
            elif percentile_rank < 0.60:
                color = 'green_human.png'
            elif percentile_rank < 0.80:
                color = 'orange_human.png'
            else:
                color = 'blue_human.png'

            height = income * 25 + 3
            earnings = income / 15 * 2.5

            sketch1_distribution.append({
                "score": income,
                "height": height,
                "money": f"€{earnings:.2f}",
                "icon": f"/static/Test_Luck_Merit/Images/{color}"
            })

        # Sketch 2 (more skewed distribution)
        sketch2_income_values = [1, 1, 2, 3, 3, 4, 5, 6, 7, 9, 9, 9, 10, 10, 13, 13, 13, 14, 14, 15]
        sketch2_distribution = []
        for i, income in enumerate(sketch2_income_values):
            percentile_rank = (i + 1) / num_participants
            if percentile_rank < 0.20:
                color = 'red_human.png'
            elif percentile_rank < 0.40:
                color = 'yellow_human.png'
            elif percentile_rank < 0.60:
                color = 'green_human.png'
            elif percentile_rank < 0.80:
                color = 'orange_human.png'
            else:
                color = 'blue_human.png'

            height = income * 25 + 3
            earnings = income / 15 * 2.5

            sketch2_distribution.append({
                "score": income,
                "height": height,
                "money": f"€{earnings:.2f}",
                "icon": f"/static/Test_Luck_Merit/Images/{color}"
            })

        return {
            'scores_and_colors': scores_and_colors,
            'percentage_ranking_100': current_player.percentage_ranking_100,
            'participant_color': current_player.field_maybe_none('color') or 'default_icon.png',
            'specific_participant_id_in_group': current_player.id_in_group,
            'original_gini_opposite_group': original_gini_opposite_group,
            'gini_test_score1': gini_test_score1,
            'predefined_distribution': predefined_distribution,
            'point_distribution_example': point_distribution_example,
            'raw_distribution_example': raw_distribution_example,
            'sketch1_distribution': sketch1_distribution,  # Sketch 1 example
            'sketch2_distribution': sketch2_distribution,   # Sketch 2 example
            'num_bars': num_bars  # Send the number of sliders needed
        }

    def before_next_page(player: Player, timeout_happened):
        # Handle adjustments only if there's no timeout
        if not timeout_happened:
            try:
                # Convert the comma-separated string back into a list of floats
                adjustment_values = [float(value) for value in player.adjustment_values.split(',')]
            except ValueError:
                player.participant.vars['adjustment_error'] = True
                return

            # Calculate new Gini coefficient based on the adjusted values
            new_ravens_pays = [adjustment for adjustment in adjustment_values]

            # Store the calculated Gini coefficient in the player object
            player.new_gini_opposite_group = calculate_gini(new_ravens_pays)

            # Check if the length of adjustment values matches the number of players
            opposite_group_players = [p for p in player.group.get_players() if p.group_type != player.group_type]
            if len(adjustment_values) != len(opposite_group_players):
                player.participant.vars['adjustment_error'] = True
            else:
                player.participant.vars['adjustment_error'] = False

            # Store the recalculated Gini coefficients
            player.original_gini_opposite_group = calculate_gini(
                [p.field_maybe_none('pay_ravens_original') for p in opposite_group_players if
                 p.field_maybe_none('pay_ravens_original') is not None]
            )

            player.gini_test_score1 = calculate_gini(
                [p.field_maybe_none('test_score1') for p in opposite_group_players if
                 p.field_maybe_none('test_score1') is not None]
            )

        # Handle the timeout scenario
        if timeout_happened:
            # Increment the timeout count stored in participant.vars
            player.timeout_count += 1



def calculate_gini(arr):
    """Calculate the Gini coefficient of a list of numbers using the given formula."""
    sorted_arr = sorted(arr)
    n = len(arr)
    if n == 0:
        return 0.0

    sum_of_arr = sum(sorted_arr)
    if sum_of_arr == 0:
        return 0.0

    cumulative_sum = sum((n + 1 - (i + 1)) * sorted_arr[i] for i in range(n))
    gini_coefficient = (n + 1) / n - (2 * cumulative_sum) / (n * sum_of_arr)
    return gini_coefficient

class BeforeFinalQuestions(WaitPage):
    def is_displayed(player):
        return player.consent and not player.remove
    wait_for_all_groups = True
    def after_all_players_arrive(subsession: Subsession):
        import random

        for group in subsession.get_groups():
            closest_difference = float('inf')
            candidates = []

            for p in group.get_players():
                # Safely access true_performance_estimate and test_score1_raw using field_maybe_none()
                true_performance_estimate = p.field_maybe_none('true_performance_estimate')
                test_score1_raw = p.field_maybe_none('test_score1_raw')

                # Ensure bonus is calculated only if both fields are valid (i.e., not None)
                if true_performance_estimate is not None and test_score1_raw is not None and abs(
                        true_performance_estimate - test_score1_raw) <= 1:
                    p.bonus_earned = Constants.bonus_for_accurate_prediction
                    p.performance_guess_correct = True
                else:
                    p.bonus_earned = 0
                    p.performance_guess_correct = False

                for p in group.get_players():
                    # Safely access gini_test_score1 and new_gini_opposite_group using field_maybe_none()
                    gini_test_score1 = p.field_maybe_none('gini_test_score1')
                    new_gini_opposite_group = p.field_maybe_none('new_gini_opposite_group')

                    # Ensure both values are not None before calculating the difference
                    if gini_test_score1 is not None and new_gini_opposite_group is not None:
                        difference = abs(gini_test_score1 - new_gini_opposite_group)

                        if difference < closest_difference:
                            closest_difference = difference
                            candidates = [p]
                        elif difference == closest_difference:
                            candidates.append(p)

            if candidates:
                bonus_player = random.choice(candidates)
                bonus_player.bonus_gini = 3
            else:
                for p in group.get_players():
                    p.bonus_gini = 0

            # Ensure payoff includes all components
            for p in group.get_players():
                p.payoff += p.bonus_earned
                p.payoff += p.bonus_gini
class FinalQuestions(Page):
    def is_displayed(player):
        return player.consent and not player.remove

    timeout_seconds = 70

    wait_for_all_groups = True
    form_model = 'player'
    form_fields = [
        'age', 'gender', 'student', 'employed',
        'hard_work', 'luck_role',
        'inequality', 'political_ideology', 'skill_role',
        'help_noeffort', 'help_noskill', 'help_luck', 'country', 'major'
    ]


class FinalPayment(Page):
    def is_displayed(player):
        return player.consent and not player.remove

    wait_for_all_groups = True
    # Calculate bonus based on accurate prediction
    def vars_for_template(player: Player):
        participation_fee = cu(1.5)  # Assuming this is defined in your Constants
        player.pay_ravens_showed = cu(player.pay_ravens)
        player.bonus_guess_showed = cu(player.bonus_earned)
        player.finished = True



        return {
            'final_payment': player.payoff,
            'pay_ravens': player.pay_ravens_showed,
            'participation_fee': participation_fee,
            'prediction_lottery_winner': player.is_prediction_lottery_winner,
            'prediction_lottery_winnings': player.prediction_lottery_outcome,
            'investment_lottery_winner': player.is_investment_lottery_winner,
            'investment_lottery_winnings': player.investment_lottery_winnings,
            'performance_guess_correct': player.performance_guess_correct,
            'bonus_earned': player.bonus_guess_showed,
            'bonus_gini': player.bonus_gini,
        }

class InvestmentDecision(Page):
    timeout_seconds = 45
    form_model = 'player'
    form_fields = ['investment']
    def is_displayed(player):
        return player.consent and not player.remove

    def before_next_page(player: Player, timeout_happened):
        player.is_investment_chosen = True
        if random.choice([True, False]):  # 50% chance to win the lottery
            player.investment_outcome = player.investment * 2
        else:
            player.investment_outcome = 0

        player.investment_lottery_winnings = Constants.investment_amount - player.investment + player.investment_outcome

        if timeout_happened:
            # Increment the timeout count stored in participant.vars
            player.timeout_count += 1
class SelectOneForInvestmentPayment(WaitPage):

    def is_displayed(player):
        return player.consent and not player.remove

    wait_for_all_groups = True

    def after_all_players_arrive(subsession: Subsession):
        all_players = subsession.get_players()
        chosen_player = random.choice(all_players)
        chosen_player.is_investment_lottery_winner = True
        # Only add the investment outcome for the chosen player
        chosen_player.payoff += chosen_player.investment_lottery_winnings

class NoConsent(Page):
    def is_displayed(player):
        return player.consent == 0 or player.remove


page_sequence = [
    EnterExperiment,
    WaitingRoom,
    Introduction,
    Instructions,
    SampleQuestions,
    PredictionExplanation,
    GradingExplanation,
    FinalPrediction,
    PaymentExplanation,
    RavensTest,
    ResultsWaitPage,
    TestOutcomeWaiting,
    TestOutcome,
    SelectOneForPredictionLottery,
    PerformanceHistogram,
    SplitExplanation,
    InteractiveGraph,
    TaxRateProcessing,
    PerformanceEstimation,
    InvestmentDecision,
    SelectOneForInvestmentPayment,
    SecondTaxRateVoting,
    BeforeFinalQuestions,
    FinalQuestions,
    NoConsent,
    FinalPayment
]
