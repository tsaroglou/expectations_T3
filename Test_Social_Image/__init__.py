from otree.api import *
import random
from otree.api import Page
import string


def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return str(n) + suffix


class Constants(BaseConstants):
    country_choices = [
        ('AF', 'Afganistán'), ('AL', 'Albania'), ('DE', 'Alemania'), ('AD', 'Andorra'), ('AO', 'Angola'),
        ('AI', 'Anguila'), ('AQ', 'Antártida'), ('AG', 'Antigua y Barbuda'), ('SA', 'Arabia Saudita'),
        ('DZ', 'Argelia'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'),
        ('AT', 'Austria'), ('AZ', 'Azerbaiyán'), ('BS', 'Bahamas'), ('BD', 'Bangladés'), ('BB', 'Barbados'),
        ('BH', 'Baréin'), ('BE', 'Bélgica'), ('BZ', 'Belice'), ('BJ', 'Benín'), ('BM', 'Bermudas'),
        ('BY', 'Bielorrusia'), ('BO', 'Bolivia'), ('BA', 'Bosnia y Herzegovina'), ('BW', 'Botsuana'),
        ('BR', 'Brasil'), ('BN', 'Brunéi'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'),
        ('BT', 'Bután'), ('CV', 'Cabo Verde'), ('KH', 'Camboya'), ('CM', 'Camerún'), ('CA', 'Canadá'),
        ('QA', 'Catar'), ('EA', 'Ceuta y Melilla'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'),
        ('CY', 'Chipre'), ('VA', 'Ciudad del Vaticano'), ('CO', 'Colombia'), ('KM', 'Comoras'),
        ('KP', 'Corea del Norte'), ('KR', 'Corea del Sur'), ('CR', 'Costa Rica'), ('CI', 'Costa de Marfil'),
        ('HR', 'Croacia'), ('CU', 'Cuba'), ('CW', 'Curazao'), ('DK', 'Dinamarca'), ('DM', 'Dominica'),
        ('EC', 'Ecuador'), ('EG', 'Egipto'), ('SV', 'El Salvador'), ('AE', 'Emiratos Árabes Unidos'),
        ('ER', 'Eritrea'), ('SK', 'Eslovaquia'), ('SI', 'Eslovenia'), ('ES', 'España'), ('US', 'Estados Unidos'),
        ('EE', 'Estonia'), ('ET', 'Etiopía'), ('PH', 'Filipinas'), ('FI', 'Finlandia'), ('FJ', 'Fiyi'),
        ('FR', 'Francia'), ('GA', 'Gabón'), ('GM', 'Gambia'), ('GE', 'Georgia'), ('GH', 'Ghana'),
        ('GI', 'Gibraltar'), ('GD', 'Granada'), ('GR', 'Grecia'), ('GL', 'Groenlandia'), ('GP', 'Guadalupe'),
        ('GU', 'Guam'), ('GT', 'Guatemala'), ('GF', 'Guayana Francesa'), ('GG', 'Guernsey'), ('GN', 'Guinea'),
        ('GQ', 'Guinea Ecuatorial'), ('GW', 'Guinea-Bisáu'), ('GY', 'Guyana'), ('HT', 'Haití'), ('HN', 'Honduras'),
        ('HU', 'Hungría'), ('IN', 'India'), ('ID', 'Indonesia'), ('IQ', 'Irak'), ('IR', 'Irán'),
        ('IE', 'Irlanda'), ('BV', 'Isla Bouvet'), ('IM', 'Isla de Man'), ('CX', 'Isla de Navidad'),
        ('NF', 'Isla Norfolk'),
        ('IS', 'Islandia'), ('AX', 'Islas Åland'), ('KY', 'Islas Caimán'), ('CC', 'Islas Cocos'), ('CK', 'Islas Cook'),
        ('FO', 'Islas Feroe'), ('GS', 'Islas Georgia del Sur y Sandwich del Sur'), ('HM', 'Islas Heard y McDonald'),
        ('MV', 'Islas Maldivas'), ('FK', 'Islas Malvinas'), ('MP', 'Islas Marianas del Norte'),
        ('MH', 'Islas Marshall'),
        ('UM', 'Islas menores alejadas de los EE. UU.'), ('PN', 'Islas Pitcairn'), ('SB', 'Islas Salomón'),
        ('TC', 'Islas Turcas y Caicos'),
        ('VG', 'Islas Vírgenes Británicas'), ('VI', 'Islas Vírgenes de los EE. UU.'), ('IL', 'Israel'),
        ('IT', 'Italia'),
        ('JM', 'Jamaica'), ('JP', 'Japón'), ('JE', 'Jersey'), ('JO', 'Jordania'), ('KZ', 'Kazajistán'), ('KE', 'Kenia'),
        ('KG', 'Kirguistán'), ('KI', 'Kiribati'), ('XK', 'Kosovo'), ('KW', 'Kuwait'), ('LA', 'Laos'), ('LS', 'Lesoto'),
        ('LV', 'Letonia'), ('LB', 'Líbano'), ('LR', 'Liberia'), ('LY', 'Libia'), ('LI', 'Liechtenstein'),
        ('LT', 'Lituania'),
        ('LU', 'Luxemburgo'), ('MK', 'Macedonia del Norte'), ('MG', 'Madagascar'), ('MY', 'Malasia'), ('MW', 'Malaui'),
        ('ML', 'Malí'), ('MT', 'Malta'), ('MA', 'Marruecos'), ('MQ', 'Martinica'), ('MU', 'Mauricio'),
        ('MR', 'Mauritania'),
        ('YT', 'Mayotte'), ('MX', 'México'), ('FM', 'Micronesia'), ('MD', 'Moldavia'), ('MC', 'Mónaco'),
        ('MN', 'Mongolia'),
        ('ME', 'Montenegro'), ('MS', 'Montserrat'), ('MZ', 'Mozambique'), ('MM', 'Myanmar (Birmania)'),
        ('NA', 'Namibia'),
        ('NR', 'Nauru'), ('NP', 'Nepal'), ('NI', 'Nicaragua'), ('NE', 'Níger'), ('NG', 'Nigeria'), ('NU', 'Niue'),
        ('NO', 'Noruega'), ('NC', 'Nueva Caledonia'), ('NZ', 'Nueva Zelanda'), ('OM', 'Omán'), ('NL', 'Países Bajos'),
        ('PK', 'Pakistán'), ('PW', 'Palaos'), ('PS', 'Palestina'), ('PA', 'Panamá'), ('PG', 'Papúa Nueva Guinea'),
        ('PY', 'Paraguay'), ('PE', 'Perú'), ('PF', 'Polinesia Francesa'), ('PL', 'Polonia'), ('PT', 'Portugal'),
        ('PR', 'Puerto Rico'), ('GB', 'Reino Unido'), ('CF', 'República Centroafricana'), ('CZ', 'República Checa'),
        ('CG', 'República del Congo'), ('CD', 'República Democrática del Congo'), ('DO', 'República Dominicana'),
        ('RE', 'Reunión'),
        ('RW', 'Ruanda'), ('RO', 'Rumanía'), ('RU', 'Rusia'), ('EH', 'Sáhara Occidental'), ('WS', 'Samoa'),
        ('AS', 'Samoa Americana'),
        ('BL', 'San Bartolomé'), ('KN', 'San Cristóbal y Nieves'), ('SM', 'San Marino'), ('MF', 'San Martín'),
        ('PM', 'San Pedro y Miquelón'),
        ('VC', 'San Vicente y las Granadinas'), ('SH', 'Santa Elena'), ('LC', 'Santa Lucía'),
        ('ST', 'Santo Tomé y Príncipe'), ('SN', 'Senegal'),
        ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leona'), ('SG', 'Singapur'), ('SX', 'Sint Maarten'),
        ('SY', 'Siria'),
        ('SO', 'Somalia'), ('LK', 'Sri Lanka'), ('SZ', 'Suazilandia'), ('ZA', 'Sudáfrica'), ('SD', 'Sudán'),
        ('SS', 'Sudán del Sur'),
        ('SE', 'Suecia'), ('CH', 'Suiza'), ('SR', 'Surinam'), ('SJ', 'Svalbard y Jan Mayen'), ('TH', 'Tailandia'),
        ('TW', 'Taiwán'),
        ('TZ', 'Tanzania'), ('TJ', 'Tayikistán'), ('IO', 'Territorio Británico del Océano Índico'),
        ('TF', 'Territorios Australes Franceses'),
        ('TL', 'Timor-Leste'), ('TG', 'Togo'), ('TK', 'Tokelau'), ('TO', 'Tonga'), ('TT', 'Trinidad y Tobago'),
        ('TN', 'Túnez'),
        ('TM', 'Turkmenistán'), ('TR', 'Turquía'), ('TV', 'Tuvalu'), ('UA', 'Ucrania'), ('UG', 'Uganda'),
        ('UY', 'Uruguay'),
        ('UZ', 'Uzbekistán'), ('VU', 'Vanuatu'), ('VE', 'Venezuela'), ('VN', 'Vietnam'), ('WF', 'Wallis y Futuna'),
        ('YE', 'Yemen'), ('DJ', 'Yibuti'), ('ZM', 'Zambia'), ('ZW', 'Zimbabue')
    ]

    name_in_url = 'my_experiment'
    players_per_group = 5  # Set to 5 as you need groups of 5
    num_rounds = 1
    participation_fee = cu(5)
    box_with_money_reward = cu(12)
    box_money = cu(12)
    no_money_reward = cu(0)
    stay_out_reward_A = cu(4)
    stay_out_reward_B = cu(6)
    decision_B_allow = "Allow Role A participants to Decide"
    decision_B_stay_out = "Stay Out"
    decision_A_stay_out = "Stay Out"
    chance_box_with_money = 0.75  # 75% chance


class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()

    def set_final_payoffs(self):
        players = self.get_players()

        # Randomly choose one player from the session to receive the lottery outcome as additional payoff
        winner = random.choice(players)
        winner.payoff += winner.lottery_outcome  # Add the lottery outcome to the winner's payoff



    def determine_special_payoffs(self):
        players = self.get_players()

        # Randomly select one participant for a special payout based on their decisions
        special_paying_player = random.choice(players)
        decision_num = random.choice(['1', '2', '3', '4'])

        # Randomly select one of the four decisions made by the special paying player
        decision_selected = getattr(special_paying_player, f'decision_{decision_num}')

        # Randomly select another participant to receive the payout corresponding
        # to the option not chosen by the first participant
        other_player = random.choice([p for p in players if p != special_paying_player])

        # Assign the payouts based on the decision
        if decision_num == '1':
            if decision_selected == 'L':
                special_paying_player.payoff += c(2)  # both get 2
                other_player.payoff += c(2)
            else:
                special_paying_player.payoff += c(2)  # payer gets 2, other gets 1
                other_player.payoff += c(1)
        elif decision_num == '2':
            if decision_selected == 'L':
                special_paying_player.payoff += c(2)  # both get 2
                other_player.payoff += c(2)
            else:
                special_paying_player.payoff += c(3)  # payer gets 3, other gets 1
                other_player.payoff += c(1)
        elif decision_num == '3':
            if decision_selected == 'L':
                special_paying_player.payoff += c(2)  # both get 2
                other_player.payoff += c(2)
            else:
                special_paying_player.payoff += c(4)  # payer gets 4, other gets 2
                other_player.payoff += c(2)
        elif decision_num == '4':
            if decision_selected == 'L':
                special_paying_player.payoff += c(2)  # both get 2
                other_player.payoff += c(2)
            else:
                special_paying_player.payoff += c(3)  # payer gets 3, other gets 5
                other_player.payoff += c(5)



from otree.api import Currency as c

class Group(BaseGroup):
    box_with_money = models.IntegerField()  # Store which box has money for each group

class Player(BasePlayer):

    image_path = models.StringField(blank=True)


    exchange_for_info = models.BooleanField(initial=False)  # Assuming False as default, adjust as needed
    opt_out_code = models.StringField()
    action_choice = models.StringField()
    is_paid = models.BooleanField(initial=False)
    typed_code = models.StringField(blank=True)
    wants_to_see_results = models.BooleanField(initial=True)  # Default to True, assuming they want to see results unless they opt out
    decision_made = models.StringField(
        choices=[['see_score', 'Show my percentage of correct answers and my ranking'], ['opt_out', 'Proceed without showing my results']],
        widget=widgets.RadioSelect
    )
    lottery_outcome = models.CurrencyField(initial=0)
    investment = models.CurrencyField(
        min=0,
        max=2,
        doc="""The amount the participant decides to invest""",
    )

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


    @staticmethod
    def get_random_code(length=20):
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    decision_a = models.StringField(
        choices=[
            ('Red', 'Red Box'),
            ('Blue', 'Blue Box'),
            ('Green', 'Green Box'),
            ('Stay Out', 'Stay Out')
        ],
        widget=widgets.RadioSelectHorizontal,
        blank=False
    )
    decision_b = models.StringField(choices=['Allow Role A participants to Decide', 'Stay Out'], widget=widgets.RadioSelectHorizontal, blank=False)
    exchange_for_info = models.BooleanField(
        label="Do you want to exchange €0.20 for information about your test score and position?",
        widget=widgets.RadioSelectHorizontal,
        choices=[
            [True, "Yes, show me my test score and position"],
            [False, "No, I'll keep the €0.20"]
        ]
    )


    box_choice = models.IntegerField()
    chosen_for_b_id = models.IntegerField(blank=True)  # For Role A, ID of the Role B player they're chosen for
    matched_b_id = models.IntegerField(blank=True)  # For Role A, ID of the matched Role B player
    matched_a_ids = models.StringField(blank=True)  # For Role B, comma-separated IDs of matched Role A players
    name_in_group = models.StringField()
    test_completion_time = models.FloatField()
    participant_role = models.StringField()
    test_score = models.IntegerField()
    matched_participant = models.StringField()
    box_with_money = models.StringField()
    matched_participants = models.StringField()
    payoff_before = models.CurrencyField(initial=0)
    uq1 = models.IntegerField(initial=0)
    uq2 = models.IntegerField(initial=0)
    uq3 = models.IntegerField(initial=0)
    uq4 = models.IntegerField(initial=0)
    uq5 = models.IntegerField(initial=0)
    uq6 = models.IntegerField(initial=0)
    uq7 = models.IntegerField(initial=0)
    uq8 = models.IntegerField(initial=0)
    hasmistake = models.IntegerField(initial=0)


    # New fields for understanding questions
    understanding_q1 = models.IntegerField(
        choices=[
            [1, "No"],
            [2, "Yes"]
        ],
        label="Do participants in role B find out which participants in role A scored in the top 50% in the test?",
        widget=widgets.RadioSelect
    )

    understanding_q2 = models.IntegerField(
        choices=[
            [1, "Whether they opened a box and whether the box contained contained money."],
            [2, "Their test score."],
            [3, "Their true identities."]
        ],
        label="What do participants in Role B know about the each of their matched Role A participants?",
        widget=widgets.RadioSelect
    )

    understanding_q3 = models.IntegerField(
        choices=[
            [1, "No"],
            [2, "If they scored in the top 50% in the test."],
            [3, "Yes"]
        ],
        label="Do participants in Role B find out which box holds the money?",
        widget=widgets.RadioSelect
    )

    understanding_q4 = models.IntegerField(
        choices=[
            [1, "No"],
            [2, "Yes"]
        ],
        label="Can participants in Role A choose a box even if they do not know which box contains the money?",
        widget=widgets.RadioSelect
    )

    understanding_q5 = models.IntegerField(
        choices=[
            [1, "€12"],
            [2, "€10"],
            [3, "It depends on whether the box contains the money"],
            [4,
             "It depends on whether the box contains the money, on whether the box is locked, and on which A participant is selected for payment"]
        ],
        label="How much does a B participant earn when they let their A participants make a choice, and they choose a box?",
        widget=widgets.RadioSelect
    )

    understanding_q6 = models.IntegerField(
        choices=[
            [1, "€4"],
            [2, "€10"],
            [3, "It depends on whether the box contains the money"],
            [4, "It depends on whether the box contains the money and on whether the box is locked"]
        ],
        label="How much does an A participant earn when their B participant lets them make a choice and they choose a box?",
        widget=widgets.RadioSelect
    )

    understanding_q7 = models.IntegerField(
        choices=[
            [1, "€4"],
            [2, "€6"],
            [3, "€0"]
        ],
        label="How much does an A participant earn when they stay out?",
        widget=widgets.RadioSelect
    )

    understanding_q8 = models.IntegerField(
        choices=[
            [1, "€4"],
            [2, "€6"],
            [3, "€0"]
        ],
        label="How much does a B participant earn when they stay out?",
        widget=widgets.RadioSelect
    )

    def set_feedback_messages(self):
        feedback_messages = []  # Initialize as a list
        correct_answers = [1, 1, 1, 2, 4, 4, 1, 2]
        user_answers = [self.understanding_q1, self.understanding_q2, self.understanding_q3, self.understanding_q4,
                        self.understanding_q5, self.understanding_q6, self.understanding_q7, self.understanding_q8]

        for i, (user_answer, correct_answer) in enumerate(zip(user_answers, correct_answers), start=1):
            if user_answer != correct_answer:
                # Customize your feedback message for each question
                feedback_messages.append(f"Feedback for question {i}: [Your custom feedback here].")

        # Convert the list to a newline-separated string and store it in the player instance
        self.feedback_messages = '\n'.join(feedback_messages) if feedback_messages else ''


        # Other fields remain unchanged

        # Role A decision field (keep existing 'decision' field or rename for clarity)
    decision_a = models.StringField(
        choices=['Red', 'Blue', 'Green', 'Stay Out'],
        widget=widgets.RadioSelect,
        blank=False  # Allow blank submissions if you use this field for Role B participants
        )

        # Role B decision field
    decision_b = models.StringField(
        choices=['Allow Role A participants to Decide', 'Stay Out'],
        widget=widgets.RadioSelect
        )
    # Adding individual question fields
    q1 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6], blank=True)
    q2 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6], blank=True)
    q3 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6], blank=True)
    q4 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6], blank=True)
    q5 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6], blank=True)
    q6 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6], blank=True)
    q7 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6], blank=True)
    q8 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6], blank=True)
    q9 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6], blank=True)
    q10 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6], blank=True)
    q11 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6], blank=True)
    q12 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6], blank=True)
    q13 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q14 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q15 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q16 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q17 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q18 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q19 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q20 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q21 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q22 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q23 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q24 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q25 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q26 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q27 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q28 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q29 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)
    q30 = models.IntegerField(choices=[1, 2, 3, 4, 5, 6, 7, 8], blank=True)

    question_1 = models.StringField()
    question_2 = models.StringField()
    question_3 = models.StringField()
    question_4 = models.StringField()
    question_5 = models.StringField()
    question_6 = models.StringField()
    question_7 = models.StringField()
    question_8 = models.StringField()

    def calculate_test_score(self):
        correct_answers = [4, 5, 1, 2, 6, 3, 6, 2, 1, 3, 4, 5, 8, 2, 3, 8, 7, 4, 7, 6, 8, 2, 1, 5, 1, 6, 3, 2, 4,
                           5]  # correct answers

        # Retrieve question responses, safely handling potential None values
        questions = [
            self.field_maybe_none('q1'), self.field_maybe_none('q2'), self.field_maybe_none('q3'),
            self.field_maybe_none('q4'), self.field_maybe_none('q5'), self.field_maybe_none('q6'),
            self.field_maybe_none('q7'), self.field_maybe_none('q8'), self.field_maybe_none('q9'),
            self.field_maybe_none('q10'), self.field_maybe_none('q11'), self.field_maybe_none('q12'),
            self.field_maybe_none('q13'), self.field_maybe_none('q14'), self.field_maybe_none('q15'),
            self.field_maybe_none('q16'), self.field_maybe_none('q17'), self.field_maybe_none('q18'),
            self.field_maybe_none('q19'), self.field_maybe_none('q21'), self.field_maybe_none('q22'),
            self.field_maybe_none('q23'), self.field_maybe_none('q24'), self.field_maybe_none('q25'),
            self.field_maybe_none('q26'), self.field_maybe_none('q27'), self.field_maybe_none('q28'),
            self.field_maybe_none('q29'), self.field_maybe_none('q30')
        ]

        # Calculate the score
        score = sum(1 for user_ans, correct_ans in zip(questions, correct_answers) if user_ans == correct_ans)
        self.test_score = int((score / 30) * 100)  # Convert to percentage and ensure it's an integer

test_answers = models.LongStringField()
privileged_info = models.BooleanField(initial=False)
final_payoff = models.CurrencyField()



# PAGES
class Introduction(Page):
    pass




import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
class UploadImagePage(Page):
    form_model = 'player'

    def post(self):
        # Handle image file from the request
        uploaded_file = self.request.FILES.get('image_upload')

        if uploaded_file:
            # Define the file path for the uploaded image
            path = f'participant_images/{self.player.id_in_group}_{uploaded_file.name}'

            # Save the uploaded image to the filesystem
            file_path = default_storage.save(path, ContentFile(uploaded_file.read()))

            # Store the file path in the player model
            self.player.image_path = file_path

        # Proceed with the normal post handling
        return super().post()



class AssignRolesWaitPage(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):
        for group in self.subsession.get_groups():
            players = group.get_players()
            roles = ['B'] + ['A'] * (Constants.players_per_group - 1)
            random.shuffle(roles)
            a_counter = 1  # Initialize a counter for Role A participants

            for player, role in zip(players, roles):
                player.participant_role = role
                player.participant.vars['participant_role'] = role  # Store role in participant vars for later use
                group_id = group.id_in_subsession  # Get the group's ID for naming

                # Assign box_with_money for Role A participants and set name_in_group
                if role == 'A':
                    player.box_with_money = random.choice(['Red', 'Blue', 'Green'])
                    player.name_in_group = f'Participant A{a_counter}'
                    a_counter += 1  # Increment Role A counter for each Role A participant
                else:  # For Role B participant
                    player.name_in_group = f'Participant B{group_id}    '

class RoleReveal(Page):
    def vars_for_template(self):
        participant_role = self.participant.vars.get('participant_role', 'Not Assigned')
        matched_names = []

        if participant_role == 'A':
            # For Role A, find the matched Role B participant in the group
            role_b_player = next(p for p in self.group.get_players() if p.participant_role == 'B')
            matched_names.append(role_b_player.name_in_group)
        elif participant_role == 'B':
            # For Role B, find all Role A participants in the group and get their names
            role_a_players = [p for p in self.group.get_players() if p.participant_role == 'A']
            matched_names = [p.name_in_group for p in role_a_players]

        return {
            'participant_role': participant_role,
            'matched_names': matched_names
        }

from time import time

from otree.api import Page
import time


class RavenTest(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11', 'q12', 'q13', 'q14', 'q15', 'q16', 'q17', 'q18', 'q19', 'q20', 'q21', 'q22', 'q23', 'q24', 'q25', 'q26', 'q27', 'q28', 'q29', 'q30']
    timeout_seconds = 10 * 60  # 10 minutes

    def vars_for_template(self):
        # Set the start time at the beginning of the page
        self.participant.vars.setdefault('test_start_time', time.time())
        return {self.image_path}

    def before_next_page(self, **kwargs):
        self.calculate_test_score()  # Assuming this method is implemented in your Player class

        # Calculate the elapsed time
        start_time = self.participant.vars.get('test_start_time', time.time())
        elapsed_time = time.time() - start_time

        # Check if the page transition was due to a timeout using kwargs
        if 'timeout_happened' in kwargs and kwargs['timeout_happened']:
            self.test_completion_time = 600
        else:
            self.test_completion_time = min(elapsed_time, 600)




class UnderstandingQuestions(Page):
    form_model = 'player'
    form_fields = ['understanding_q1', 'understanding_q2', 'understanding_q3', 'understanding_q4',
                   'understanding_q5', 'understanding_q6', 'understanding_q7', 'understanding_q8']

    def before_next_page(self, **kwargs):  # Accept any additional keyword arguments
        correct_answers = [1, 1, 1, 2, 4, 4, 1, 2]  # Assuming these are the correct options for each question

        # Set uqX variables based on participant responses
        responses = [
            self.understanding_q1, self.understanding_q2, self.understanding_q3,
            self.understanding_q4, self.understanding_q5, self.understanding_q6,
            self.understanding_q7, self.understanding_q8
        ]

        for i, response in enumerate(responses):
            setattr(self, f'uq{i+1}', 1 if response != correct_answers[i] else 0)

        # Calculate 'hasmistake'
        self.hasmistake = sum(getattr(self, f'uq{i+1}') for i in range(len(responses)))


class ReviewMistakes(Page):
    def vars_for_template(self):
        mistakes = self.participant.vars.get('mistakes', [])
        feedback = []

        # Feedback messages for each question
        question_feedback = {
            'understanding_q1': "Explanation for Q1: No, participants in role B do not find out which participants in role A scored in the top 50% in the test.",
            'understanding_q2': "Explanation for Q2: Participants in Role B only learn whether each of their matched role A participants opened a box and whether the box contained money. Therefore, they do not know the identity of the role A participants or whether they scored in the top 50% of the session. ",
            'understanding_q3': "Explanation for Q3: No, participants in role B do not receive any information regarding the test results. ",
            'understanding_q4': "Explanation for Q4: Yes, participants in Role A can choose a box even if they do not know which one contains the money. ",
            'understanding_q5': "Explanation for Q5: The payment of participants in Role B depends on whether the box opened by the Role A participant contained the money and whether the box is locked. Additionally, only one out of the four matched Role A participants is chosen to determine the payoff of the participant in Role B.",
            'understanding_q6': "Explanation for Q6: The payment of participants in Role A depends on whether the box they opened contained the money and whether the box is locked.",
            'understanding_q7': "Explanation for Q7: A participant in role A earns 4 Euros when they choose to stay out, regardless of other game conditions.",
            'understanding_q8': "Explanation for Q8: A participant in role B earns 6 Euros when they decide to stay out. This decision is independent of other participants' actions."
        }

        for mistake in mistakes:
            feedback.append(question_feedback.get(mistake, "No feedback available."))

        return {'feedback': feedback,
                'hasmistake': self.hasmistake,
                'uq1': self.uq1,
                'uq2': self.uq2,
                'uq3': self.uq3,
                'uq4': self.uq4,
                'uq5': self.uq5,
                'uq6': self.uq6,
                'uq7': self.uq7,
                'uq8': self.uq8}



def before_next_page(self):
        # Logic to check answers...
        self.participant.vars['has_incorrect_answers'] = False  # Default to False

        # Example logic for checking one answer
        if self.understanding_q1 != 1:  # Assuming 1 is the correct answer for q1
            self.participant.vars['has_incorrect_answers'] = True
            # Generate feedback and store it in participant vars
            self.participant.vars['feedback'] = [
                {"question": "Your question text", "selected": "Selected answer", "correct": "Correct answer",
                 "explanation": "Explanation"}]

            return {'incorrect_found': self.incorrect_found,
                    'feedback': self.feedback}



class UnderstandingQuestionsPage(Page):
    form_model = 'player'
    form_fields = ['question_1', 'question_2', 'question_3', 'question_4', 'question_5', 'question_6', 'question_7', 'question_8']



class Instructions(Page):
    def vars_for_template(player):
        return {
             'participant_role':  player.participant_role
        }


class RoleBDecision(Page):
    form_model = 'player'
    form_fields = ['decision_b']  # Use the decision field specific to Role B

    def is_displayed(self):
        return self.participant.vars.get('participant_role', 'Unknown') == 'B'

class AllRoleAWaitPage(WaitPage):
    # Only wait for players with Role A
    wait_for_all_groups = True

    def is_displayed(self):
        return self.participant.vars.get('participant_role') == 'A'

    def after_all_players_arrive(self):
        pass  # You don't need to do anything here; just wait for all Role A players.

class ReviewAnswers(Page):
    class ReviewAnswers(Page):

        def is_displayed(self):
            player = self
            incorrect_found = False

            questions_feedback = [
                {'field': 'understanding_q1', 'correct': 1},
                {'field': 'understanding_q2', 'correct': 1},
                {'field': 'understanding_q3', 'correct': 1},
                {'field': 'understanding_q4', 'correct': 2},
                {'field': 'understanding_q5', 'correct': 4},
                {'field': 'understanding_q6', 'correct': 4},
                {'field': 'understanding_q7', 'correct': 1},
                {'field': 'understanding_q8', 'correct': 2},
            ]



    questions_feedback = [
            {
                'field': 'understanding_q1',
                'question': "Do participants in role B find out which participants in role A scored in the top 50% in the test?",
                'correct': 1,  # "No" is the correct answer
                'explanation': "No, participants in role B are not provided with this information."
            },
            {
                'field': 'understanding_q2',
                'question': "Do participants know the identity of other participants?",
                'correct': 1,  # "No" is the correct answer
                'explanation': "No, the identity of other participants remains anonymous."
            },
            {
                'field': 'understanding_q3',
                'question': "Do participants in Role B find out which box holds the money?",
                'correct': 1,  # "No" is the correct answer
                'explanation': "No, participants in Role B do not find out which box holds the money unless they scored in the top 50%."
            },
            {
                'field': 'understanding_q4',
                'question': "Can participants in Role A choose a box even if they do not know which one contains the money?",
                'correct': 2,  # "Yes" is the correct answer
                'explanation': "Yes, participants in Role A can choose a box even without knowing which one contains the money."
            },
            {
                'field': 'understanding_q5',
                'question': "How much is a participant in role B earning when they let the participants in role A choose and they choose a box?",
                'correct': 4,  # "It depends on several factors" is the correct answer
                'explanation': "The earnings depend on various factors, including whether the box holds the money, whether the money disappears, and which participant in role A is selected for payment."
            },
            {
                'field': 'understanding_q6',
                'question': "How much is a participant in role A earning when the participant in role B lets them choose and they choose a box?",
                'correct': 4,  # "It depends on several factors" is the correct answer
                'explanation': "The earnings depend on whether the box holds the money and on whether the money disappears."
            },
            {
                'field': 'understanding_q7',
                'question': "How much is a participant in role A earning when they stay out?",
                'correct': 1,  # "4 Euros" is the correct answer
                'explanation': "A participant in role A earns 4 Euros when they decide to stay out."
            },
            {
                'field': 'understanding_q8',
                'question': "How much is a participant in role B earning when they stay out?",
                'correct': 2,  # "6 Euro" is the correct answer
                'explanation': "A participant in role B earns 6 Euro when they decide to stay out."
            },
        ]




class RoleAPrivilege(Page):
    def is_displayed(self):
        # Display this page only to Role A participants
        return self.participant.vars.get('participant_role', 'Unknown') == 'A'

    def vars_for_template(self):
        players = self.group.get_players()
        A_players = [p for p in players if p.participant.vars.get('participant_role') == 'A']

        # Sort Role A players first by their test score in descending order, then by their test completion time in ascending order
        A_players_sorted = sorted(A_players, key=lambda p: (-p.test_score, p.test_completion_time))

        # Calculate the index for splitting the group into top 50%
        top_50_cutoff_index = len(A_players_sorted) // 2

        # Determine if the current player is in the top 50%
        in_top_50 = A_players_sorted.index(self) < top_50_cutoff_index

        # Assign privileged information if in top 50%
        self.privileged_info = in_top_50
        box_with_money = self.box_with_money if in_top_50 else None  # Directly use self.box_with_money with the adjusted logic

        return {
            'in_top_50': in_top_50,
            'box_with_money': box_with_money
        }


class RoleADecision(Page):
    form_model = 'player'
    form_fields = ['decision_a']

    def is_displayed(self):
        return self.participant.vars['participant_role'] == 'A'  # Updated from 'role' to 'participant_role'


class ResultsWaitPage(WaitPage):

    after_all_players_arrive = 'set_payoffs'

    def set_payoffs(group: Group):
        players_A = [p for p in group.get_players() if p.participant_role == 'A']
        player_B = [p for p in group.get_players() if p.participant_role == 'B'][0]

        # Store matched IDs for Role B
        player_B.matched_a_ids = ','.join(str(p.id_in_group) for p in players_A)

        for player_A in players_A:
            # Store matched ID for Role A
            player_A.matched_b_id = player_B.id_in_group

            # Calculate payoff including participation fee
            if player_A.decision_a == 'Stay Out':
                player_A.payoff = Constants.stay_out_reward_A + Constants.participation_fee
            elif player_A.decision_a == player_A.box_with_money and random.random() <= Constants.chance_box_with_money:
                player_A.payoff = Constants.box_with_money_reward + Constants.participation_fee
            else:
                player_A.payoff = Constants.no_money_reward + Constants.participation_fee

        if player_B.decision_b == Constants.decision_B_stay_out:
            player_B.payoff = Constants.stay_out_reward_B + Constants.participation_fee
            for player_A in players_A:
                player_A.payoff = Constants.stay_out_reward_A + Constants.participation_fee
        else:
            chosen_A = random.choice(players_A)
            chosen_A.chosen_for_b_id = player_B.id_in_group  # Store chosen Role A's ID in Role B

            # Adjust Role B's payoff based on the payoff of the chosen Role A participant
            if chosen_A.payoff == Constants.stay_out_reward_A + Constants.participation_fee:
                # When the chosen Role A participant decided to "Stay Out"
                player_B.payoff = Constants.stay_out_reward_B + Constants.participation_fee
            elif chosen_A.payoff == Constants.box_with_money_reward + Constants.participation_fee:
                # When the chosen Role A participant chose the box with money and won the lottery
                player_B.payoff = (Constants.box_with_money_reward - cu(2)) + Constants.participation_fee
            else:
                # When the chosen Role A participant chose a box but didn't win or chose the wrong box
                player_B.payoff = Constants.no_money_reward + Constants.participation_fee


class ExchangeDecision(Page):
    form_model = 'player'
    form_fields = ['typed_code']

    def is_displayed(self):
        return self.participant.vars['participant_role'] == 'A'

    def vars_for_template(self):
        # Ensure this method returns a dictionary with 'opt_out_code'
        opt_out_code = "Ab3dEfGh4IjKl5MnOp6Q"  # Define your opt-out code here
        return {
            'opt_out_code': opt_out_code  # This is the correct way to pass variables to your template
        }

    def before_next_page(self, **kwargs):
        correct_opt_out_code = "Ab3dEfGh4IjKl5MnOp6Q"

        # Determine action based on the typed code
        if self.typed_code == correct_opt_out_code:
            self.wants_to_see_results = False
        else:
            self.wants_to_see_results = True



class Decision(Page):
    form_model = 'player'
    form_fields = ['decision_made']

    def is_displayed(self):
        # Display only for Group A participants who chose to opt out
        return self.participant_role == 'A'

    def vars_for_template(self):
        return {'opt_out_code': "Ab3dEfGh4IjKl5MnOp6Q"}

    def before_next_page(self, **kwargs):
        if self.decision_made == 'see_score':
            self.exchange_for_info = True
        elif self.decision_made == 'opt_out':
            # Assume False until they successfully enter the opt-out code
            self.exchange_for_info = False

class OptOutVerification(Page):
    form_model = 'player'
    form_fields = ['typed_code']

    def is_displayed(self):
        # Logic to determine if this page should be displayed
        return self.participant_role == 'A' and self.decision_made == 'opt_out'

    def vars_for_template(self):
        # Initialize error_message to None or an empty string if no error has occurred
        error_message = self.session.vars.get('error_message', '')
        # Clear the error message after it's been retrieved to prevent it from persisting incorrectly
        self.session.vars['error_message'] = ''
        return {
            'error_message': error_message
        }

    def before_next_page(self, **kwargs):
        correct_opt_out_code = "Ab3dEfGh4IjKl5MnOp6Q"
        if self.typed_code != correct_opt_out_code:
            # Set the error message if the opt-out code is incorrect
            self.session.vars['error_message'] = "Incorrect opt-out code. Please try again."
            # Redirect back to this page or indicate the need for correction
            self._is_frozen = False  # Unfreeze this page to allow re-entry





class Results(Page):
    def is_displayed(self):
        # Only display if the participant is in Group A
        return self.participant_role == 'A' and self.decision_made == 'see_score'
    def get_random_code(self):
        # Generates a random 20-character alphanumeric code
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(20))

    def vars_for_template(self):
        chosen_for_b = None
        matched_b = None
        matched_as = []
        display_info = False
        test_score = None
        rank = None
        total_A = None

        if self.participant_role == 'A':
            matched_b = self.matched_b_id
            chosen_for_b_id = self.field_maybe_none('chosen_for_b_id')
            if chosen_for_b_id is not None:
                chosen_for_b = chosen_for_b_id

            # Check if the player chose to exchange for info
            display_info = self.exchange_for_info
            if display_info:
                test_score = self.test_score
                players_A = [p for p in self.group.get_players() if p.participant_role == 'A']
                ranked_players_A = sorted(players_A, key=lambda x: x.test_score, reverse=True)
                rank = ranked_players_A.index(self) + 1
                total_A = len(players_A)

        elif self.participant_role == 'B':
            matched_as = self.matched_a_ids.split(',') if self.matched_a_ids else []

        return {
            'final_payoff': self.payoff,
            'opt_out_code': self.get_random_code(),
            'chosen_for_b': chosen_for_b,
            'matched_b': matched_b,
            'matched_as': matched_as,
            'display_info': display_info,
            'participant_role': self.participant_role,  # Ensure this line is added
            'test_score': test_score,
            'rank': rank,
            'total_A': total_A
        }



class InvestmentDecision(Page):
    form_model = 'player'
    form_fields = ['investment']

    def before_next_page(self, **kwargs):
        # Store the potential lottery outcome without affecting the actual payoff
        if random.choice([True, False]):  # 50% chance to win the lottery
            self.lottery_outcome = self.investment * 2.5
        else:
            self.lottery_outcome = 0


class ExchangeForInfo(Page):
    form_model = 'player'
    form_fields = ['exchange_for_info']

    # This page is only displayed for Role A participants
    def is_displayed(self):
        return self.participant.vars['participant_role'] == 'A'

    def before_next_page(self, **kwargs):
        # If the participant chooses to keep the €0.20, add it to their payoff
        if not self.exchange_for_info:
            self.payoff += cu(0.20)

# FUNCTIONS
def set_payoffs(group: Group):
    players_A = [p for p in group.get_players() if p.participant_role == 'A']
    player_B = [p for p in group.get_players() if p.participant_role == 'B'][0]

    # Store matched IDs for Role B
    player_B.matched_a_ids = ','.join(str(p.id_in_group) for p in players_A)

    for player_A in players_A:
        # Store matched ID for Role A
        player_A.matched_b_id = player_B.id_in_group

        # Calculate payoff including participation fee
        if player_A.decision_a == 'Stay Out':
            player_A.payoff = Constants.stay_out_reward_A + Constants.participation_fee
        elif player_A.decision_a == player_A.box_with_money and random.random() <= Constants.chance_box_with_money:
            player_A.payoff = Constants.box_with_money_reward + Constants.participation_fee
        else:
            player_A.payoff = Constants.no_money_reward + Constants.participation_fee

    if player_B.decision_b == Constants.decision_B_stay_out:
        player_B.payoff = Constants.stay_out_reward_B + Constants.participation_fee
        for player_A in players_A:
            player_A.payoff = Constants.stay_out_reward_A + Constants.participation_fee
    else:
        chosen_A = random.choice(players_A)
        chosen_A.chosen_for_b_id = player_B.id_in_group  # Store chosen Role A's ID in Role B

        # Adjust Role B's payoff based on the payoff of the chosen Role A participant
        if chosen_A.payoff == Constants.stay_out_reward_A + Constants.participation_fee:
            # When the chosen Role A participant decided to "Stay Out"
            player_B.payoff = Constants.stay_out_reward_B + Constants.participation_fee
        elif chosen_A.payoff == Constants.box_with_money_reward + Constants.participation_fee:
            # When the chosen Role A participant chose the box with money and won the lottery
            player_B.payoff = (Constants.box_with_money_reward - cu(2)) + Constants.participation_fee
        else:
            # When the chosen Role A participant chose a box but didn't win or chose the wrong box
            player_B.payoff = Constants.no_money_reward + Constants.participation_fee


class RoleBInformation(Page):
    def is_displayed(self):
        return self.participant.vars.get('participant_role') == 'B'

    def vars_for_template(self):
        role_a_info = []
        chosen_a_info = None

        # Retrieve the matched Role A participants from the same group
        matched_as = [p for p in self.group.get_players() if p.participant.vars.get('participant_role') == 'A']

        # Get the ID of the chosen Role A participant for the current Role B participant
        chosen_a_id = self.field_maybe_none('chosen_for_b_id')


        for a in matched_as:
            decision = "decided to choose a box" if a.decision_a != 'Stay Out' else "decided to 'stay out'"
            payoff = a.payoff - Constants.participation_fee
            istheone = "This participant was randomly chosen to determine your payoff." if a.field_maybe_none('chosen_for_b_id') else " "
            role_a_info.append({
                'name': a.name_in_group,
                'decision': decision,
                'payoff': payoff,
                'istheone': istheone
            })

            if a.id_in_group == chosen_a_id:
                chosen_a_info = {
                    'name': a.name_in_group,
                    'payoff': payoff
                }

        # Calculate Role B's payoff without the participation fee
        role_b_payoff = self.payoff - Constants.participation_fee

        return {
            'role_a_info': role_a_info,
            'chosen_a_info': chosen_a_info,
            'role_b_payoff': role_b_payoff  # Make sure this is included
        }





class SelectOneForPayment(WaitPage):

    def after_all_players_arrive(self):
        # Select one player at random for payment
        paying_player = random.choice(self.subsession.get_players())
        paying_player.is_paid = True  # You'd need a field to track who gets paid

        # Set payoffs to 0 for all other players
        for p in self.subsession.get_players():
            if p != paying_player:
                p.payoff += 0

class WaitForRoleBInformation(WaitPage):
    title_text = "Please wait"
    body_text = "Waiting for other participants to complete their part."

    def is_displayed(self):
        # This WaitPage is only displayed to Role A participants
        return self.participant_role == 'A'

    def after_all_players_arrive(self):
        pass  # You don't necessarily need to do anything here

    # Repeat for decision_2, decision_3, decision_4

class DecisionPage(Page):
    form_model = 'player'
    form_fields = ['decision_1', 'decision_2', 'decision_3', 'decision_4']



class SpecialPaymentWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.determine_special_payoffs()
        self.set_final_payoffs()


class Money(Page):

    def vars_for_template(self):
        chosen_for_b = None
        matched_b = None
        matched_as = []
        display_info = False
        test_score = None
        rank = None
        total_A = None

        if self.participant_role == 'A':
            matched_b = self.matched_b_id
            chosen_for_b_id = self.field_maybe_none('chosen_for_b_id')
            if chosen_for_b_id is not None:
                chosen_for_b = chosen_for_b_id

            # Check if the player chose to exchange for info
            display_info = self.exchange_for_info
            if display_info:
                test_score = self.test_score
                players_A = [p for p in self.group.get_players() if p.participant_role == 'A']
                ranked_players_A = sorted(players_A, key=lambda x: x.test_score, reverse=True)
                rank = ranked_players_A.index(self) + 1
                total_A = len(players_A)

        elif self.participant_role == 'B':
            matched_as = self.matched_a_ids.split(',') if self.matched_a_ids else []

        return {
            'final_payoff': self.payoff,
            'opt_out_code': self.get_random_code(),
            'chosen_for_b': chosen_for_b,
            'matched_b': matched_b,
            'matched_as': matched_as,
            'display_info': display_info,
            'participant_role': self.participant_role,  # Ensure this line is added
            'test_score': test_score,
            'rank': rank,
            'total_A': total_A
        }




page_sequence = [Introduction, AssignRolesWaitPage, RoleReveal, UploadImagePage, RavenTest, Instructions, UnderstandingQuestions, ReviewMistakes,  RoleBDecision, AllRoleAWaitPage, RoleAPrivilege, RoleADecision, ResultsWaitPage, RoleBInformation,  WaitForRoleBInformation, Decision, Results, InvestmentDecision, SelectOneForPayment, DecisionPage, SpecialPaymentWaitPage, Money]
