from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants



class Introducción(Page):
    pass


class Reclamo(Page):

    form_model = 'participante'
    form_fields = ['reclamo']


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Resultados(Page):
    def vars_for_template(self):
        return {
            'other_player_claim': self.player.other_player().claim
        }


page_sequence = [
    Introduction,
    Claim,
    ResultsWaitPage,
    Results
]
