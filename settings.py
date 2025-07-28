from os import environ

#SESSION_CONFIGS = [
 #   {
 #       'name': 'charity_allocation_experiment',
 #       'display_name': "Charity Allocation Experiment",
 #       'num_demo_participants': 1,
 #       'app_sequence': ['dots'],
 #   },
#]

SESSION_CONFIGS = [
    dict(
        name='Voted_Risk_T1a',
        display_name="Voted Risk Treatment 1a",
        num_demo_participants=4,
        app_sequence=['VR_T1a_plus1_part1', 'VR_T1a_plus1_part2'],
        group_by_arrival_time=True,  # correct for PRE
    ),
]


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=5.00, doc=""
)

PARTICIPANT_FIELDS = ['display_group_id']

MONITOR_TABLE_ROWS = [
    'id_in_session',
    'code',
    'display_group_id',  # Must match exact name
    'current_page_name',
    'page_index',
    'is_on_wait_page',
    'time_on_page',
    'last_request_timestamp',
]




SESSION_FIELDS = ['prolific_completion_url', 'display_group_id']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'GBP'
USE_POINTS = False
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 2

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '7897522741144'

INSTALLED_APPS = ['otree']
