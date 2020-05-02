from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    pass


class Send(Page):
    """Esta página es solo para P1
    P1 envia la cantidad (todo, algo, o nada) a P2
    Esta cantidad es triplicada por el experimentador,
    es decir, si la cantidad enviada por P1 es 5, la cantidad recibida por P2 es 15"""

    form_model = 'group'
    form_fields = ['sent_amount']

    def is_displayed(self):
        return self.player.id_in_group == 1


class SendBackWaitPage(WaitPage):
    pass


class SendBack(Page):
    """Esta página es solo para P2
    P2 envia de vuelta algo de la cantidad (de la cantidad recibida triplicada) a P1"""

    form_model = 'group'
    form_fields = ['sent_back_amount']

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        tripled_amount = self.group.sent_amount * Constants.multiplier

        return {
                'tripled_amount': tripled_amount,
                'prompt': 'Please an amount from 0 to {}'.format(tripled_amount)}

    def sent_back_amount_max(self):
        return self.group.sent_amount * Constants.multiplier


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    """Esta página muestra las ganacias de cada jugador"""

    def vars_for_template(self):
        return {
            'tripled_amount': self.group.sent_amount * Constants.multiplier
        }


page_sequence = [
    Introduction,
    Send,
    SendBackWaitPage,
    SendBack,
    ResultsWaitPage,
    Results,
]
