from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


class Constants(BaseConstants):
    name_in_url = 'encuesta'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    age = models.IntegerField(
        label='¿Cuántos años tiene?',
        min=13, max=125)

    gender = models.StringField(
        choices=['Masculino', 'Femenino', 'Otro'],
        label='¿Cuál es su género?',
        widget=widgets.RadioSelect)

    crt_bat = models.IntegerField(
        label='''
        Un bate y una pelota cuestan 22 dólares en total.
        El bate cuesta 20 dólares más que la pelota.
        ¿Cuántos dólares cuesta la pelota?'''
    )

    crt_widget = models.IntegerField(
        label='''
        "Si 5 máquinas en 5 minutos pueden hacer 5 dispositivos,
        ¿Cuántos minutos tomaría a 100 máquinas hacer 100 dispositivos?"
        '''
    )

    crt_lake = models.IntegerField(
        label='''
        En un lago, hay una superficie cubierta de nenúfares.
        Todos los días, esa extensión dobla su tamaño.
        Si tarda 48 días en cubrir todo el lago,
        ¿Cuántos días le tomaría cubrir la mitad del lago?
        '''
    )
