from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


doc = """
Este juego de negociación involucra a 2 jugadores. Cada uno exige 
una porción de alguna cantidad disponible. Si la suma de las 
demandas no es mayor que la cantidad disponible, ambos jugadores reciben
porciones demandadas. De lo contrario, ambos no obtienen nada.
"""


class Constants(BaseConstants):
    name_in_url = 'bargaining'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'bargaining/Instructions.html'

    amount_shared = c(100)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_requests = models.CurrencyField()

    def set_payoffs(self):
        players = self.get_players()
        self.total_requests = sum([p.request for p in players])
        if self.total_requests <= Constants.amount_shared:
            for p in players:
                p.payoff = p.request
        else:
            for p in players:
                p.payoff = c(0)


class Player(BasePlayer):
    request = models.CurrencyField(
        doc="""
        Cantidad solicitada por el jugador.
        """,
        min=0, max=Constants.amount_shared
    )

    def other_player(self):
        return self.get_others_in_group()[0]
