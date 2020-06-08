from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Introduction(Page):
    """Descripción del juego: Cómo jugar y devoluciones esperadas"""
    pass


class Contribute(Page):
    """Jugador: Elige cuánto contribuir"""

    form_model = 'player'
    form_fields = ['contribution']


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()

    body_text = "A la espera de que otros participantes contribuyan."


class Results(Page):
    """Pago de los jugadores: Cuánto ha ganado cada uno"""

    def vars_for_template(self):
        return {
            'total_earnings': self.group.total_contribution * Constants.multiplier,
        }


page_sequence = [
    Introduction,
    Contribute,
    ResultsWaitPage,
    Results
]
