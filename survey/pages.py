from otree.api import Currency as c, currency_range

from ._builtin import Page, WaitPage
from .models import Constants


class Demographics(Page):
    form_model = 'participante'
    form_fields = ['edad',
                   'género']


class CognitiveReflectionTest(Page):
    form_model = 'participante'
    form_fields = ['crt_bat',
                   'crt_widget',
                   'crt_lake']


page_sequence = [
    Demographics,
    CognitiveReflectionTest
]
