from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
El juego del Ultimatum con dos tratamientos: respuesta directa y método de estrategia.
En el primero, un jugador hace una oferta y el otro acepta o rechaza.
It comes in two flavors, con y sin preguntas hipotéticas sobre la respuesta del segundo participante a ofertas distintas a de las que se hace. 
En el último tratamiento, el segundo participante recibe una lista de todas las posibles ofertas, y se le pregunta cuáles acepta o rechaza.
"""


class Constants(BaseConstants):
    name_in_url = 'ultimatum'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'ultimatum/Instructions.html'

    endowment = c(100)
    payoff_if_rejected = c(0)
    offer_increment = c(10)

    offer_choices = currency_range(0, endowment, offer_increment)
    offer_choices_count = len(offer_choices)

    keep_give_amounts = []
    for offer in offer_choices:
        keep_give_amounts.append((offer, endowment - offer))


class Subsession(BaseSubsession):
    def creating_session(self):
        # randomize to treatments
        for g in self.get_groups():
            if 'use_strategy_method' in self.session.config:
                g.use_strategy_method = self.session.config['use_strategy_method']
            else:
                g.use_strategy_method = random.choice([True, False])


def make_field(amount):
    return models.BooleanField(
        widget=widgets.RadioSelectHorizontal,
        label='¿Usted aceptaría una oferta de {}?'.format(c(amount)))


class Group(BaseGroup):
    use_strategy_method = models.BooleanField(
        doc="""Si este grupo usa el método de estrategia"""
    )

    amount_offered = models.CurrencyField(choices=Constants.offer_choices)

    offer_accepted = models.BooleanField(
        doc="si la cantidad ofertada es aceptada (método de respuesta directa)"
    )

    # for strategy method, see the make_field function above
    response_0 = make_field(0)
    response_10 = make_field(10)
    response_20 = make_field(20)
    response_30 = make_field(30)
    response_40 = make_field(40)
    response_50 = make_field(50)
    response_60 = make_field(60)
    response_70 = make_field(70)
    response_80 = make_field(80)
    response_90 = make_field(90)
    response_100 = make_field(100)


    def set_payoffs(self):
        p1, p2 = self.get_players()

        if self.use_strategy_method:
            self.offer_accepted = getattr(self, 'response_{}'.format(
                int(self.amount_offered)))

        if self.offer_accepted:
            p1.payoff = Constants.endowment - self.amount_offered
            p2.payoff = self.amount_offered
        else:
            p1.payoff = Constants.payoff_if_rejected
            p2.payoff = Constants.payoff_if_rejected


class Player(BasePlayer):
    pass
