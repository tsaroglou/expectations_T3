from otree.api import *
import random
from otree.api import Page
import string
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import gettext

import datetime
from django.shortcuts import render


from django import forms

from pathlib import Path

# Assumes that settings.py is in the myproject directory,
# two levels inside the project root (pythonProject2).
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


class PaymentForm(forms.Form):
    temporary_name = forms.CharField(label='Por favor ingresa tu nombre para el procesamiento del pago:', required=True)

def payment_view(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # process the form data
            return redirect('success_url')  # Redirect to a success page
    else:
        form = PaymentForm()  # Instantiate the form for GET request

    return render(request, 'Test_Social_Image_Spanish/Money.html', {'form': form})

def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return str(n) + suffix

from django.shortcuts import render, redirect

def payment_view(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Imagine processing or saving form data here
            return redirect('success_url')  # Redirect to a URL named 'success_url' in your URLconf
    else:
        form = PaymentForm()

    return render(request, 'your_app/payment_template.html', {'form': form})
class Constants(BaseConstants):
    name_in_url = 'my_experiment'
    players_per_group = 5  # Set to 5 as you need groups of 5
    num_rounds = 1
    participation_fee = cu(5)
    box_with_money_reward = cu(12)
    box_money = cu(12)
    no_money_reward = cu(0)
    stay_out_reward_A = cu(4)
    stay_out_reward_B = cu(6)
    decision_B_allow = "Permitir que los participantes A tomen una decisión."
    decision_B_stay_out = "Abstenerse."
    decision_A_stay_out = "Abstenerse."
    chance_box_with_money = 0.75  # 75% chance
    # Assuming the country names have been manually translated and sorted
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


def get_credentials():
    """Log in to Google API and save the credentials for later re-use."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', ['https://www.googleapis.com/auth/spreadsheets'])
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def save_payment_info(name, payoff):
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet_id = '18kfQ49hdEbpI4_yJecg1ozHcc2wWnU2AX3B3yKNZRfQ'

    values = [[name, str(payoff)]]  # Removed datetime, now only saving name and payoff
    body = {'values': values}
    range_name = 'A:B'  # Adjusted the range to only include two columns A and B

    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption='USER_ENTERED', body=body).execute()

    print(f"{result.get('updates').get('updatedCells')} cells appended.")

# Example Usage
save_payment_info("John Doe", 100.50)


class Subsession(BaseSubsession):
    def creating_session(self):
        for i, player in enumerate(self.subsession.get_players(), start=1):
            self.unique_in_session_id = i

        self.group_randomly()

    def set_final_payoffs(self):
        players = self.get_players()

        # Session-wide lottery winner (rather than per group)
        winner = random.choice(players)
        winner.payoff += winner.lottery_outcome  # Assuming lottery_outcome is set up elsewhere appropriately
        winner.is_winner = True  # Make sure to define 'is_winner' in Player class


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

        # Don't forget to save the changes to the database

from otree.api import Currency as c

class Group(BaseGroup):
    pass

class Player(BasePlayer):

    ###########################################

    unique_in_session_id = models.IntegerField()
    participant_role = models.StringField()
    name_in_group = models.StringField()
    test_score = models.IntegerField()
    test_completion_time = models.FloatField()
    privileged_info = models.BooleanField()
    decision_a = models.StringField(
        choices=['Roja', 'Azul', 'Verde', 'Abstenerse.'],
        widget=widgets.RadioSelectHorizontal
    )
    box_with_money = models.StringField()
    decision_b = models.StringField(
        choices=['Permitir que los participantes A tomen una decisión.', 'Abstenerse.'],
        widget=widgets.RadioSelectHorizontal
    )
    is_chosen = models.BooleanField()
    investment = models.CurrencyField(
        min=0, max=2,
        doc="""La cantidad que el participante decide invertir"""
    )
    lottery_outcome = models.CurrencyField()
    is_winner = models.BooleanField(initial=False)
    paying_player = models.BooleanField(initial=False)
    other_player = models.BooleanField(initial=False)
    decision_num = models.StringField()
    decision_selected = models.StringField()
    wants_to_see_results = models.BooleanField(initial=True)

    age = models.IntegerField(
        label="¿Cuántos años tienes?"
    )

    is_student = models.StringField(
        choices=['Si', 'No'],
        label="¿Eres estudiante?",
        widget=widgets.RadioSelect
    )
    study_level = models.StringField(
        choices=['Pregrado', 'Posgrado'],
        label="¿Eres estudiante de pregrado o posgrado?",
        widget=widgets.RadioSelect
    )
    study_year = models.IntegerField(
        label="¿Qué año de tus estudios es este?"
    )

    major = models.StringField(
        choices=['Administracion de Empresas', 'Economía', 'Otro'],
        label="¿Cual es tu campo de estudio?",
        widget=widgets.RadioSelect
    )
    is_employed = models.StringField(
        choices=['Si', 'No'],
        label="¿Estás empleado?",
        widget=widgets.RadioSelect
    )
    people_in_room_known = models.IntegerField(
        label="¿Cuántos participantes conoces en esta aúla?"
    )

    country = models.StringField(
        choices=Constants.country_choices,
        label="¿De qué país eres?",
    )

    gender = models.StringField(
        choices=['Hombre', 'Mujer', 'Otro'],
        label="¿Cuál es tu género?",
        widget=widgets.RadioSelect
    )

    ############################################

    special_paying_player = models.BooleanField(initial=False)

    temporary_name = models.StringField()
    made_for_b = models.StringField()
    special_paying_player_id = models.IntegerField()
    other_player_id = models.IntegerField()
    opt_out_code = models.StringField()
    action_choice = models.StringField()
    is_paid = models.BooleanField(initial=False)
    typed_code = models.StringField(blank=True)
    decision_made = models.StringField(
        choices=[['see_score', 'Mostrar mi puntuación y clasificación'], ['opt_out', 'Proceder sin mostrar mis resultados']],
        widget=widgets.RadioSelect
    )



    def before_save(self):
        """Ensure investment is rounded to two decimal places before saving."""
        if self.investment is not None:
            self.investment = round(self.investment, 2)


    decision_1 = models.StringField(
        choices=[
            ('L', '2€ para ti  <br> 2€ para el otro participante'),
            ('R', '2€ para ti  <br> 1€ para el otro participante')
        ],
        widget=widgets.RadioSelectHorizontal
    )
    decision_2 = models.StringField(
        choices=[
            ('L', '2€ para ti <br> 2€ para el otro participante'),
            ('R', '3€ para ti  <br> 1€ para el otro participante')
        ],
        widget=widgets.RadioSelectHorizontal
    )
    decision_3 = models.StringField(
        choices=[
            ('L', '2€ para ti  <br> 2€ para el otro participante'),
            ('R', '2€ para ti  <br> 4€ para el otro participante')
        ],
        widget=widgets.RadioSelectHorizontal
    )
    decision_4 = models.StringField(
        choices=[
            ('L', '2€ para ti  <br> 2€ para el otro participante'),
            ('R', '3€ para ti  <br> 5€ para el otro participante')
        ],
        widget=widgets.RadioSelectHorizontal
    )

    @staticmethod
    def get_random_code(length=20):
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))


    exchange_for_info = models.BooleanField(
        label="¿Quieres intercambiar €0.20 por información sobre tu puntuación en el test y posición?",
        widget=widgets.RadioSelectHorizontal,
        choices=[
            [True, "Sí, muéstrame mi puntuación en el test y posición"],
            [False, "No, me quedo con los €0.20"]
        ],
        initial=False,  # Defaulting to False
        doc="This field is used to determine if the player wants to exchange €0.20 for test score information."
    )

    box_choice = models.IntegerField()
    chosen_for_b_id = models.IntegerField(blank=True)  # For Role A, ID of the Role B player they're chosen for
    matched_b_id = models.IntegerField(blank=True)  # For Role A, ID of the matched Role B player
    matched_a_ids = models.StringField(blank=True)  # For Role B, comma-separated IDs of matched Role A players
    matched_participant = models.StringField()
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
            [1, "Sí"],
            [2, "No"]
        ],
        label="¿Los participantes en el rol B descubren qué participantes en el rol A se clasificaron en el top 50% en el test?",
        widget=widgets.RadioSelect
    )

    understanding_q2 = models.IntegerField(
        choices=[
            [1, "Si abrieron una caja y el pago resultante."],
            [2, "Su puntuación en el examen."],
            [3, "Sus verdaderas identidades"]
        ],
        label="¿Qué saben los participantes en el rol B sobre cada uno de los participantes en el rol A?",
        widget=widgets.RadioSelect
    )

    understanding_q3 = models.IntegerField(
        choices=[
            [1, "No"],
            [2, "Si se clasificaron en el top 50% en el test."],
            [3, "Si, siempre"]
        ],
        label="¿Descubren los participantes en el Rol B qué caja contiene el dinero?",
        widget=widgets.RadioSelect
    )

    understanding_q4 = models.IntegerField(
        choices=[
            [1, "No"],
            [2, "Sí"]
        ],
        label="¿Pueden los participantes en el Rol A elegir una caja incluso si no saben qué caja contiene el dinero?",
        widget=widgets.RadioSelect
    )

    understanding_q5 = models.IntegerField(
        choices=[
            [1, "€12"],
            [2, "€10"],
            [3, "Depende de si la caja contiene el dinero"],
            [4,
             "Depende de si la caja contiene el dinero, de si la caja está bloqueada y de qué participante en el rol A es seleccionado para el pago"]
        ],
        label="¿Cuánto gana un participante en el rol B cuando permite que sus participantes en el rol A tomen una decisión y  eligen una caja?",
        widget=widgets.RadioSelect
    )

    understanding_q6 = models.IntegerField(
        choices=[
            [1, "€4"],
            [2, "€10"],
            [3, "Depende de si la caja contiene el dinero"],
            [4, "Depende de si la caja contiene el dinero y de si la caja está bloqueada"]
        ],
        label="¿Cuánto gana un participante en el rol A cuando su participante en el rol B le permite tomar una decisión y el participante A elige una caja?",
        widget=widgets.RadioSelect
    )

    understanding_q7 = models.IntegerField(
        choices=[
            [1, "€4"],
            [2, "€6"],
            [3, "€0"]
        ],
        label="¿Cuánto gana un participante en el rol A cuando se abstiene?",
        widget=widgets.RadioSelect
    )

    understanding_q8 = models.IntegerField(
        choices=[
            [1, "€4"],
            [2, "€6"],
            [3, "€0"]
        ],
        label="¿Cuánto gana un participante en el rol B cuando se abstiene?",
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
                feedback_messages.append(f"Retroalimentación para la pregunta {i}: [Tu retroalimentación personalizada aquí].")

        # Convert the list to a newline-separated string and store it in the player instance
        self.feedback_messages = '\n'.join(feedback_messages) if feedback_messages else ''


    # Other fields remain unchanged

    # Role A decision field (keep existing 'decision' field or rename for clarity)
    decision_a = models.StringField(
        choices=[
            ('Roja', 'Eligo caja roja.'),
            ('Azul', 'Eligo caja azul.'),
            ('Verde', 'Eligo caja verde.'),
            ('Abstenerse.', 'Abstenerse.')
        ],
        widget=widgets.RadioSelectHorizontal,
        blank=False)

    # Role B decision field
    decision_b = models.StringField(
        choices=['Permitir que los participantes A tomen una decisión.', 'Abstenerse.'],
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
                           5]  #  correct answers

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
    final_payoff = models.CurrencyField()




# PAGES
# PAGES
class Introduction(Page):
    pass



class AssignRolesWaitPage(WaitPage):
    wait_for_all_groups = True


    def after_all_players_arrive(self):
        for i, player in enumerate(self.subsession.get_players(), start=1):
            player.unique_in_session_id = i


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
                    player.box_with_money = random.choice(['Roja', 'Azul', 'Verde'])
                    player.name_in_group = f'Participante A{player.unique_in_session_id}'
                    a_counter += 1  # Increment Role A counter for each Role A participant
                else:  # For Role B participant
                    player.name_in_group = f'Participante B{player.unique_in_session_id}'

class RoleReveal(Page):
    def vars_for_template(self):
        participant_role = self.participant.vars.get('participant_role', 'No asignado')
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
    timeout_seconds = 10 * 60  # 10 minutos

    def vars_for_template(self):
        # Set the start time at the beginning of the page
        self.participant.vars.setdefault('test_start_time', time.time())
        return {
            'participant_role': self.participant_role,
        }

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

    def before_next_page(self, **kwargs):  # Aceptar cualquier argumento adicional de palabras clave
        correct_answers = [1, 1, 1, 2, 4, 4, 1, 2]  # Suponiendo que estas son las opciones correctas para cada pregunta

        # Establecer variables uqX basadas en las respuestas de los participantes
        responses = [
            self.understanding_q1, self.understanding_q2, self.understanding_q3,
            self.understanding_q4, self.understanding_q5, self.understanding_q6,
            self.understanding_q7, self.understanding_q8
        ]

        for i, response in enumerate(responses):
            setattr(self, f'uq{i+1}', 1 if response != correct_answers[i] else 0)

        # Calcular 'hasmistake'
        self.hasmistake = sum(getattr(self, f'uq{i+1}') for i in range(len(responses)))


class ReviewMistakes(Page):
    def vars_for_template(self):
        mistakes = self.participant.vars.get('mistakes', [])
        feedback = []

        # Mensajes de retroalimentación para cada pregunta
        question_feedback = {
            'understanding_q1': "Explicación para la P1: No, los participantes en el rol B no descubren qué participantes en el rol A obtuvieron una puntuación entre el 50% superior en la prueba.",
            'understanding_q2': "Explicación de la P2: Los participantes en el rol B solo aprenden si cada uno de los participantes del rol A abrió una caja y si la caja contenía dinero. Por lo tanto, no conocen la identidad de los participantes del rol A ni si obtuvieron puntaje. en el 50% superior de la sesión.",
            'understanding_q3': "Explicación para la P3: No, los participantes en el rol B no reciben ninguna información sobre los resultados de la prueba. ",
            'understanding_q4': "Explicación para la P4: Sí, los participantes en el Rol A pueden elegir una casilla incluso si no saben qué contiene el dinero. ",
            'understanding_q5': "Explicación de la P5: El pago de los participantes en el Rol B depende de si la caja abierta por el participante del Rol A contenía el dinero y si la caja está cerrada. Además, solo uno de los cuatro participantes del Rol A coincidentes es elegido para determinar la recompensa del participante en el rol B.",
            'understanding_q6': "Explicación de la P6: El pago de los participantes en el Rol A depende de si la caja que abrieron contenía el dinero y si la caja está cerrada con llave.",
            'understanding_q7': "Explicación de la P7: Un participante en el rol A gana 4 euros cuando decide quedarse fuera, independientemente de otras condiciones del juego.",
            'understanding_q8': "Explicación de la P8: Un participante en el rol B gana 6 euros cuando decide quedarse fuera. Esta decisión es independiente de las acciones de los demás participantes."
        }

        for mistake in mistakes:
            feedback.append(question_feedback.get(mistake, "No hay retroalimentación disponible."))

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
    # Lógica para verificar respuestas...
    self.participant.vars['has_incorrect_answers'] = False  # Predeterminado a False

    # Ejemplo de lógica para verificar una respuesta
    if self.understanding_q1 != 1:  # Suponiendo que 1 es la respuesta correcta para q1
        self.participant.vars['has_incorrect_answers'] = True
        # Generar retroalimentación y almacenarla en vars del participante
        self.participant.vars['feedback'] = [
            {"question": "El texto de tu pregunta", "selected": "Respuesta seleccionada", "correct": "Respuesta correcta",
             "explanation": "Explicación"}]

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
    form_fields = ['decision_b']  # Utilizar el campo de decisión específico para el Rol B

    def is_displayed(self):
        return self.participant.vars.get('participant_role', 'Desconocido') == 'B'


class AllRoleAWaitPage(WaitPage):
    # Solo esperar por jugadores con Rol A
    wait_for_all_groups = True

    def is_displayed(self):
        return self.participant.vars.get('participant_role') == 'A'

    def after_all_players_arrive(self):
        pass  # No necesitas hacer nada aquí; solo esperar a todos los jugadores de Rol A.


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
                'question': "Can participants in Role B choose a box even if they do not know which one contains the money?",
                'correct': 2,  # "Yes" is the correct answer
                'explanation': "Yes, participants in Role B can choose a box even without knowing which one contains the money."
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
                'explanation': "Un participante en el rol A gana 4 Euros cuando decide mantenerse al margen."
            },
        {
            'field': 'understanding_q8',
            'question': "¿Cuánto gana un participante en el rol B cuando se mantienen al margen?",
            'correct': 2,  # "6 Euros" es la respuesta correcta
            'explanation': "Un participante en el rol B gana 6 Euros cuando decide mantenerse al margen."
        },
    ]

class RoleAPrivilege(Page):
    def is_displayed(self):
        # Display this page only to participants with Role 'A'
        return self.participant.vars.get('participant_role', 'Unknown') == 'A'

    def vars_for_template(self):
        players = self.subsession.get_players()
        A_players = [p for p in players if p.participant_role == 'A']  # Make sure participant_role is stored correctly

        # Sort Role A participants first by their test score in descending order, then by their test completion time in ascending order
        A_players_sorted = sorted(A_players, key=lambda x: (-x.test_score, x.test_completion_time))

        # Calculate the index to split the group into the top 50%
        top_50_cutoff_index = len(A_players_sorted) // 2

        # Determine if the current player is in the top 50%
        current_player = self  # Use self.player to refer to the current player instance
        in_top_50 = A_players_sorted.index(current_player) < top_50_cutoff_index

        # Assign privileged information if in the top 50%
        self.privileged_info = in_top_50  # It's better to assign this to player, not self
        box_with_money = self.box_with_money if in_top_50 else None

        return {
            'in_top_50': in_top_50,
            'box_with_money': box_with_money
        }

class RoleADecision(Page):
        form_model = 'player'
        form_fields = ['decision_a']

        def is_displayed(self):
            return self.participant.vars['participant_role'] == 'A'  # Actualizado de 'role' a 'participant_role'

def set_payoffs(group: Group):
    players_A = [p for p in group.get_players() if p.participant_role == 'A']
    player_B = [p for p in group.get_players() if p.participant_role == 'B'][0]

    # Almacenar IDs emparejados para el Rol B
    player_B.matched_a_ids = ','.join(str(p.unique_in_session_id) for p in players_A)

    for player_A in players_A:
        # Almacenar ID emparejado para el Rol A
        player_A.matched_b_id = player_B.unique_in_session_id

        # Calcular la ganancia incluyendo la tarifa de participación
        if player_A.decision_a == 'Abstenerse.':
            player_A.payoff = cu(4) + cu(5)
            player_A.made_for_b = "6"
        elif player_A.decision_a == player_A.box_with_money and random.random() <= Constants.chance_box_with_money:
            player_A.payoff = cu(12) + cu(5)
            player_A.made_for_b = "10"
        else:
            player_A.payoff = cu(5)
            player_A.made_for_b = "0"


    if player_B.decision_b == Constants.decision_B_stay_out:
        player_B.payoff = cu(6) + cu(5)
        for player_A in players_A:
            player_A.payoff = cu(4) + cu(5)
    else:
        chosen_A = random.choice(players_A)
        chosen_A.is_chosen = True
        chosen_A.chosen_for_b_id = player_B.unique_in_session_id  # Almacenar el ID del Rol A elegido en el Rol B

        # Ajustar la ganancia del Rol B basada en la ganancia del participante del Rol A elegido
        if chosen_A.payoff == cu(4) + cu(5):
            # Cuando el participante del Rol A elegido decidió "Mantenerse al margen"
            player_B.payoff = cu(6) + cu(5)
        elif chosen_A.payoff == cu(12) + cu(5):
            # Cuando el participante del Rol A elegido eligió la caja con dinero y ganó la lotería
            player_B.payoff = cu(10) + cu(5)
        else:
            # Cuando el participante del Rol A elegido eligió una caja pero no ganó o eligió la caja equivocada
            player_B.payoff = cu(5)



class ResultsWaitPage(WaitPage):


        after_all_players_arrive = 'set_payoffs'




class ExchangeDecision(Page):
    form_model = 'player'
    form_fields = ['typed_code']

    def is_displayed(self):
        return self.participant.vars['participant_role'] == 'A'

    def vars_for_template(self):
        # Asegurarse de que este método devuelva un diccionario con 'opt_out_code'
        opt_out_code = "Ab3dEfGh4IjKl5MnOp6Q"  # Definir aquí tu código de exclusión
        return {
            'opt_out_code': opt_out_code  # Esta es la forma correcta de pasar variables a tu plantilla
        }

    def before_next_page(self, **kwargs):
        correct_opt_out_code = "Ab3dEfGh4IjKl5MnOp6Q"

        # Determinar la acción basada en el código tecleado
        if self.typed_code == correct_opt_out_code:
            self.wants_to_see_results = False
        else:
            self.wants_to_see_results = True


class Decision(Page):
    form_model = 'player'
    form_fields = ['decision_made']

    def is_displayed(self):
        # Mostrar solo para los participantes del Grupo A que eligieron excluirse
        return self.participant_role == 'A'

    def vars_for_template(self):
        return {'opt_out_code': "Ab3dEfGh4IjKl5MnOp6Q"}

    def before_next_page(self, **kwargs):
        if self.decision_made == 'see_score':
            self.exchange_for_info = True
        elif self.decision_made == 'opt_out':
            # Asumir Falso hasta que ingresen exitosamente el código de exclusión
            self.exchange_for_info = False

class OptOutVerification(Page):
    form_model = 'player'
    form_fields = ['typed_code']

    def is_displayed(self):
        # Lógica para determinar si esta página debe mostrarse
        return self.participant_role == 'A' and self.decision_made == 'opt_out'

    def vars_for_template(self):
        # Inicializar error_message en None o una cadena vacía si no ha ocurrido ningún error
        error_message = self.session.vars.get('error_message', '')
        # Limpiar el mensaje de error después de que se haya recuperado para evitar que persista incorrectamente
        self.session.vars['error_message'] = ''
        return {
            'error_message': error_message
        }

    def before_next_page(self, **kwargs):
        correct_opt_out_code = "Ab3dEfGh4IjKl5MnOp6Q"
        if self.typed_code != correct_opt_out_code:
            # Establecer el mensaje de error si el código de exclusión es incorrecto
            self.session.vars['error_message'] = "Código de exclusión incorrecto. Por favor, inténtelo de nuevo."
            # Redirigir de nuevo a esta página o indicar la necesidad de corrección
            self._is_frozen = False  # Descongelar esta página para permitir reingreso


class Results(Page):
    def is_displayed(self):
        # Solo mostrar si el participante está en el Grupo A
        return self.participant_role == 'A' and self.decision_made == 'see_score'

    def get_random_code(self):
        # Genera un código alfanumérico aleatorio de 20 caracteres
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

            # Verificar si el jugador eligió intercambiar información
            display_info = self.exchange_for_info
            if display_info:
                test_score = self.test_score
                players_A = [p for p in self.subsession.get_players() if p.participant_role == 'A']
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
            'participant_role': self.participant_role,
            'test_score': test_score,
            'rank': rank,
            'total_A': total_A
        }


class InvestmentDecision(Page):
    form_model = 'player'
    form_fields = ['investment']

    def before_next_page(self, **kwargs):
        # Almacenar el resultado potencial de la lotería sin afectar el pago real
        if random.choice([True, False]):  # 50% de posibilidades de ganar la lotería
            self.lottery_outcome = self.investment * 2.5
        else:
            self.lottery_outcome = 0


class ExchangeForInfo(Page):
    form_model = 'player'
    form_fields = ['exchange_for_info']

    # Esta página solo se muestra a los participantes del Rol A
    def is_displayed(self):
        return self.participant.vars['participant_role'] == 'A'



# FUNCTIONS

class RoleBInformation(Page):
    def is_displayed(self):
        return self.participant.vars.get('participant_role') == 'B'

    def vars_for_template(self):
        role_a_info = []
        chosen_a_info = None

        # Recuperar los participantes del Rol A emparejados en el mismo grupo
        matched_as = [p for p in self.group.get_players() if p.participant.vars.get('participant_role') == 'A']

        # Obtener el ID del participante del Rol A elegido para el participante actual del Rol B
        chosen_a_id = self.field_maybe_none('chosen_for_b_id')


        for a in matched_as:
            decision = "decidió elegir una caja" if a.decision_a != 'Abstenerse.' else "decidió abstenerse"
            payoff = a.payoff - Constants.participation_fee
            made_for_b = a.made_for_b
            privileged_info = a.privileged_info

            istheone = "Este participante fue elegido al azar para determinar tu ganancia." if a.field_maybe_none('chosen_for_b_id') else " "
            role_a_info.append({
                'name': a.name_in_group,
                'decision': decision,
                'payoff': payoff,
                'istheone': istheone,
                'made_for_b': made_for_b,
                'privileged_info': privileged_info
            })

            if a.unique_in_session_id == chosen_a_id:
                chosen_a_info = {
                    'name': a.name_in_group,
                    'payoff': payoff
                }

        # Calcular la ganancia del Rol B sin la tarifa de participación
        role_b_payoff = self.payoff - Constants.participation_fee
        stayed_out = self.decision_b

        return {
            'role_a_info': role_a_info,
            'chosen_a_info': chosen_a_info,
            'role_b_payoff': role_b_payoff,
            'stayed_out': stayed_out

        }

#class SelectOneForPayment(WaitPage):

 #   def after_all_players_arrive(self):
        # Seleccionar a un jugador al azar para el pago
  #      paying_player = random.choice(self.subsession.get_players())
   #     paying_player.is_paid = True  # Necesitarás un campo para rastrear quién recibe el pago

        # Establecer los pagos a 0 para todos los demás jugadores
    #    for p in self.subsession.get_players():
     #       if p != paying_player:
      #          p.payoff += 0

class WaitForRoleBInformation(WaitPage):
    title_text = "Por favor espera"
    body_text = "Esperando a que otros participantes completen su parte."

    def is_displayed(self):
        # Esta WaitPage solo se muestra a los participantes del Rol A
        return self.participant_role == 'A'

    def after_all_players_arrive(self):
        pass  # No necesariamente necesitas hacer algo aquí

class DecisionPage(Page):
    form_model = 'player'
    form_fields = ['decision_1', 'decision_2', 'decision_3', 'decision_4']

class SpecialPaymentWaitPage(WaitPage):
    wait_for_all_groups = True
    def after_all_players_arrive(self):
        self.subsession.determine_special_payoffs()
        self.subsession.set_final_payoffs()
class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['is_student', 'study_level',  'is_employed', 'study_year', 'major', 'is_employed', 'country','age', 'gender', 'people_in_room_known']

class Money(Page):
    form_model = 'player'
    form_fields = ['temporary_name']  # This collects the name on the money page

    def vars_for_template(self):
        # Assume the existence of methods to calculate or retrieve already calculated values
        return {
            'final_payoff': self.payoff  # Assumes method exists to generate random code
        }

    def before_next_page(self, **kwargs):
        # Saving the payment information securely as previously defined
        save_payment_info(self.temporary_name, self.payoff)
        self.temporary_name = ""  # Clearing the name after use




page_sequence = [Introduction, AssignRolesWaitPage, RoleReveal, RavenTest, Instructions, UnderstandingQuestions, ReviewMistakes,  RoleBDecision, AllRoleAWaitPage, RoleAPrivilege, RoleADecision, ResultsWaitPage, RoleBInformation,  WaitForRoleBInformation, Decision, Results, InvestmentDecision, DecisionPage, SpecialPaymentWaitPage, Questionnaire, Money]
