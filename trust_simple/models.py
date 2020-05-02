from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


doc = """
Juego de confianza simple
"""


class Constants(BaseConstants):
    name_in_url = 'trust_simple'
    players_per_group = 2
    num_rounds = 1

    endowment = c(10)
    multiplier = 3

    instructions_template = 'trust_simple/Instructions.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    sent_amount = models.CurrencyField(
        choices=currency_range(0, Constants.endowment, c(1)),
        doc="""Cantidad enviada por P1""",
    )

    sent_back_amount = models.CurrencyField(
        doc="""Cantidad enviada de vuelta por P2""",
    )


class Player(BasePlayer):
    pass
