from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
En un juego de subasta de valor común, los jugadores pujan simultáneamente por 
el objeto subastado.<br/>
Antes de pujar, se les da una estimación del valor real del artículo.
Este valor real se revela después de la puja.<br/>
Las ofertas son privadas. El jugador con la puja más alta gana la subasta, pero
el pago depende de la puja ofertada y del valor real.<br/>
"""


class Constants(BaseConstants):
    name_in_url = 'common_value_auction'
    players_per_group = None
    num_rounds = 1

    instructions_template = 'common_value_auction/Instructions.html'

    min_allowable_bid = c(0)
    max_allowable_bid = c(10)

    # Error margin for the value estimates shown to the players
    estimate_error_margin = c(1)


class Subsession(BaseSubsession):
    def creating_session(self):
        for g in self.get_groups():
            item_value = random.uniform(
                Constants.min_allowable_bid,
                Constants.max_allowable_bid
            )
            g.item_value = round(item_value, 1)


class Group(BaseGroup):
    item_value = models.CurrencyField(
        doc="""Valor común del artículo a subastar, aleatorio para el tratamiento"""
    )

    highest_bid = models.CurrencyField()

    def set_winner(self):
        players = self.get_players()
        self.highest_bid = max([p.bid_amount for p in players])

        players_with_highest_bid = [p for p in players if p.bid_amount == self.highest_bid]
        winner = random.choice(
            players_with_highest_bid)  # if tie, winner is chosen at random
        winner.is_winner = True

    def generate_value_estimate(self):
        minimum = self.item_value - Constants.estimate_error_margin
        maximum = self.item_value + Constants.estimate_error_margin
        estimate = random.uniform(minimum, maximum)

        estimate = round(estimate, 1)

        if estimate < Constants.min_allowable_bid:
            estimate = Constants.min_allowable_bid
        if estimate > Constants.max_allowable_bid:
            estimate = Constants.max_allowable_bid

        return estimate


class Player(BasePlayer):
    item_value_estimate = models.CurrencyField(
        doc="""Estimación del valor común, puede ser diferente para cada jugador"""
    )

    bid_amount = models.CurrencyField(
        min=Constants.min_allowable_bid, max=Constants.max_allowable_bid,
        doc="""Cantidad pujada por el jugador"""
    )

    is_winner = models.BooleanField(
        initial=False,
        doc="""Indica si el jugador es el ganador"""
    )

    def set_payoff(self):
        if self.is_winner:
            self.payoff = self.group.item_value - self.bid_amount
            if self.payoff < 0:
                self.payoff = 0
        else:
            self.payoff = 0
