from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


doc = """
Este es un "Dilema del Prisionero" de una sola vez. Dos participantes son preguntados por separado
si quieren cooperar o desertar. Sus elecciones determinan directamente sus
pagos.
"""


class Constants(BaseConstants):
    name_in_url = 'prisoner'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'prisoner/Instructions.html'

    # payoff if 1 player defects and the other cooperates""",
    betray_payoff = c(300)
    betrayed_payoff = c(0)

    # payoff if both players cooperate or both defect
    both_cooperate_payoff = c(200)
    both_defect_payoff = c(100)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    decision = models.StringField(
        choices=['Cooperate', 'Defect'],
        doc="""This player's decision""",
        widget=widgets.RadioSelect
    )

    def other_player(self):
        return self.get_others_in_group()[0]

    def set_payoff(self):

        payoff_matrix = {
            'Cooperate':
                {
                    'Cooperate': Constants.both_cooperate_payoff,
                    'Defect': Constants.betrayed_payoff
                },
            'Defect':
                {
                    'Cooperate': Constants.betray_payoff,
                    'Defect': Constants.both_defect_payoff
                }
        }

        self.payoff = payoff_matrix[self.decision][self.other_player().decision]
