# your_app/tests.py

from otree.api import Bot
from otree.api import *

class PlayerBot(Bot):
    def play_round(self):
        # Loop through every page in this app
        for page_class in pages.page_sequence:
            # If the page has form fields, submit dummy data
            if getattr(page_class, 'form_fields', None):
                data = {}
                for field_name in page_class.form_fields:
                    # Grab the field’s current value just to inspect its type
                    current = getattr(self.player, field_name)
                    # Choose a dummy that will pass simple validation
                    if isinstance(current, (int, float)):
                        data[field_name] = 1
                    else:
                        data[field_name] = 'test'
                yield page_class, data
            else:
                # No form fields? Just advance
                yield page_class