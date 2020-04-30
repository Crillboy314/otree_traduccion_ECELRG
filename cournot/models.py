from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
En competencia de Cournot, las firmas deciden simultaneamente las unidades de productos
para la fabricación. El precio unitario de venta depende en el total de unidades producidas. En 
esta implementación, existen 2 firmas compitiendo por 1 período.
"""


class Constants(BaseConstants):
    name_in_url = 'cournot'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'cournot/Instructions.html'

    # Total production capacity of all players
    total_capacity = 60
    max_units_per_player = int(total_capacity / players_per_group)

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    unit_price = models.CurrencyField()

    total_units = models.IntegerField(
        doc="""Total de unidades producidas por los participantes"""
    )

    def set_payoffs(self):
        players = self.get_players()
        self.total_units = sum([p.units for p in players])
        self.unit_price = Constants.total_capacity - self.total_units
        for p in players:
            p.payoff = self.unit_price * p.units


class Player(BasePlayer):

    units = models.IntegerField(
        min=0, max=Constants.max_units_per_player,
        doc="""Cantidad de unidades a producir"""
    )

    def other_player(self):
        return self.get_others_in_group()[0]


